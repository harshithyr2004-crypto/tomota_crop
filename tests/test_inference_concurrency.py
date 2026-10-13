import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.services import binary_service, disease_service


@pytest.mark.parametrize(
    ("service_module", "service_class", "method_name", "expected_key", "output"),
    [
        (
            binary_service,
            binary_service.TomatoBinaryGateService,
            "verify_tomato",
            "is_tomato",
            np.array([[0.9]], dtype=np.float32),
        ),
        (
            disease_service,
            disease_service.TomatoDiseaseClassifierService,
            "diagnose",
            "common_name",
            np.array([[0.01] * 9 + [0.91]], dtype=np.float32),
        ),
    ],
)
def test_model_interpreter_access_is_serialized(
    monkeypatch,
    service_module,
    service_class,
    method_name,
    expected_key,
    output,
):
    class FakeInterpreter:
        def __init__(self):
            self._state_lock = threading.Lock()
            self._owner = None
            self.interleaved = False

        def _touch(self, reset_owner=False):
            thread_id = threading.get_ident()
            with self._state_lock:
                if self._owner not in (None, thread_id):
                    self.interleaved = True
                self._owner = None if reset_owner else thread_id
            time.sleep(0.002)

        def set_tensor(self, _index, _tensor):
            self._touch()

        def invoke(self):
            self._touch()

        def get_tensor(self, _index):
            self._touch(reset_owner=True)
            return output

    fake_interpreter = FakeInterpreter()
    service = object.__new__(service_class)
    service.interpreter = fake_interpreter
    service.input_details = [{"index": 0}]
    service.output_details = [{"index": 0}]
    service._inference_lock = threading.Lock()
    if service_module is binary_service:
        service.threshold = 0.75

    monkeypatch.setattr(
        service_module,
        "preprocess_for_mobilenet" if service_module is binary_service else "preprocess_for_disease_cnn",
        lambda _image: np.zeros((1, 224, 224, 3), dtype=np.float32),
    )

    predict = getattr(service, method_name)
    image = Image.new("RGB", (224, 224), (30, 120, 30))
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(lambda _: predict(image), range(12)))

    assert all(expected_key in result for result in results)
    assert fake_interpreter.interleaved is False
