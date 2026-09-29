document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const dropzonePrompt = document.getElementById('dropzonePrompt');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImgBtn = document.getElementById('removeImgBtn');
    const diagnoseBtn = document.getElementById('diagnoseBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    const samplesContainer = document.getElementById('samplesContainer');
    const catalogGrid = document.getElementById('catalogGrid');
    
    // Results DOM
    const emptyState = document.getElementById('emptyState');
    const diagnosisContent = document.getElementById('diagnosisContent');
    const severityBadge = document.getElementById('severityBadge');
    const diagnosisName = document.getElementById('diagnosisName');
    const pathogenName = document.getElementById('pathogenName');
    const gaugeValue = document.getElementById('gaugeValue');
    const confidenceFill = document.getElementById('confidenceFill');
    const probList = document.getElementById('probList');
    
    const symptomsText = document.getElementById('symptomsText');
    const organicText = document.getElementById('organicText');
    const chemicalText = document.getElementById('chemicalText');
    const preventionText = document.getElementById('preventionText');

    let currentFile = null;

    // Initialize Data
    loadSampleImages();
    loadCatalog();

    // Event Listeners: File Upload & Drag-Drop
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropzone.addEventListener('click', () => {
        if (!currentFile) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('drag-over');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt.files && dt.files[0]) {
            handleSelectedFile(dt.files[0]);
        }
    });

    removeImgBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploader();
    });

    diagnoseBtn.addEventListener('click', runDiagnosis);

    // Tab Switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = `tab-${btn.dataset.tab}`;
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add('active');
            }
        });
    });

    function handleSelectedFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (PNG, JPG, JPEG).');
            return;
        }

        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            dropzonePrompt.classList.add('hidden');
            previewContainer.classList.remove('hidden');
            diagnoseBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function resetUploader() {
        currentFile = null;
        fileInput.value = '';
        imagePreview.src = '';
        previewContainer.classList.add('hidden');
        dropzonePrompt.classList.remove('hidden');
        diagnoseBtn.disabled = true;
    }

    async function runDiagnosis() {
        if (!currentFile) return;

        // UI Loading State
        diagnoseBtn.disabled = true;
        btnSpinner.classList.remove('hidden');
        dropzone.classList.add('is-scanning');

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Prediction failed');
            }

            const data = await response.json();
            renderResults(data);
        } catch (error) {
            console.error(error);
            alert(`Error during diagnosis: ${error.message}`);
        } finally {
            diagnoseBtn.disabled = false;
            btnSpinner.classList.add('hidden');
            dropzone.classList.remove('is-scanning');
        }
    }

    function renderResults(data) {
        const pred = data.prediction;

        emptyState.classList.add('hidden');
        diagnosisContent.classList.remove('hidden');

        // Update Header & Badge
        diagnosisName.textContent = pred.common_name;
        pathogenName.textContent = `Pathogen / Cause: ${pred.pathogen}`;
        gaugeValue.textContent = `${pred.confidence}%`;
        confidenceFill.style.width = `${pred.confidence}%`;

        severityBadge.textContent = pred.is_healthy ? 'HEALTHY' : `SEVERITY: ${pred.severity.toUpperCase()}`;
        severityBadge.className = `chip sev-${pred.severity}`;

        // Top 3 Breakdown
        probList.innerHTML = '';
        data.top_predictions.forEach(item => {
            const row = document.createElement('div');
            row.className = 'prob-item';
            row.innerHTML = `
                <span class="prob-name" title="${item.common_name}">${item.common_name}</span>
                <div class="prob-bar-wrapper">
                    <div class="prob-bar" style="width: ${item.confidence}%"></div>
                </div>
                <span class="prob-pct">${item.confidence}%</span>
            `;
            probList.appendChild(row);
        });

        // Advisory Texts
        symptomsText.textContent = pred.symptoms;
        organicText.textContent = pred.organic_treatment;
        chemicalText.textContent = pred.chemical_treatment;
        preventionText.textContent = pred.prevention;

        // Scroll into view on mobile
        if (window.innerWidth < 960) {
            document.getElementById('resultsCard').scrollIntoView({ behavior: 'smooth' });
        }
    }

    async function loadSampleImages() {
        try {
            const res = await fetch('/api/samples');
            const data = await res.json();
            
            samplesContainer.innerHTML = '';
            if (data.samples && data.samples.length > 0) {
                data.samples.forEach(sample => {
                    const thumb = document.createElement('div');
                    thumb.className = 'sample-thumbnail';
                    thumb.innerHTML = `
                        <img src="${sample.image_url}" alt="${sample.common_name}" loading="lazy">
                        <div class="tooltip">${sample.common_name}</div>
                    `;
                    thumb.addEventListener('click', async () => {
                        try {
                            const imgBlob = await fetch(sample.image_url).then(r => r.blob());
                            const file = new File([imgBlob], sample.file_name, { type: 'image/jpeg' });
                            handleSelectedFile(file);
                            runDiagnosis();
                        } catch (err) {
                            console.error("Failed to load sample blob:", err);
                        }
                    });
                    samplesContainer.appendChild(thumb);
                });
            } else {
                samplesContainer.innerHTML = '<span style="font-size:12px; color:#64748b;">No sample images found</span>';
            }
        } catch (e) {
            samplesContainer.innerHTML = '<span style="font-size:12px; color:#64748b;">Samples unavailable</span>';
        }
    }

    async function loadCatalog() {
        try {
            const res = await fetch('/api/classes');
            const data = await res.json();

            catalogGrid.innerHTML = '';
            data.classes.forEach(item => {
                const card = document.createElement('div');
                card.className = 'catalog-card';
                card.innerHTML = `
                    <div class="catalog-header">
                        <h4 class="catalog-title">${item.common_name}</h4>
                        <span class="chip sev-${item.severity}">${item.severity}</span>
                    </div>
                    <p class="catalog-pathogen">${item.pathogen}</p>
                    <p class="catalog-desc">${item.symptoms}</p>
                `;
                catalogGrid.appendChild(card);
            });
        } catch (e) {
            console.error("Failed to load catalog:", e);
        }
    }
});
