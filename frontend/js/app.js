// -*- coding: utf-8 -*-
/**
 * TomatoGuard AI - Main Application Orchestrator & Multi-Page Router
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // 1. Multi-Page Navigation Router
    // -------------------------------------------------------------
    const navLinks = document.querySelectorAll('.nav-link');
    const appPages = document.querySelectorAll('.app-page');
    const viewFullAdvisoryBtn = document.getElementById('viewFullAdvisoryBtn');

    function switchPage(targetPageId) {
        navLinks.forEach(link => {
            if (link.dataset.target === targetPageId) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        appPages.forEach(page => {
            if (page.id === targetPageId) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            const targetId = link.dataset.target;
            if (targetId) switchPage(targetId);
        });
    });

    if (viewFullAdvisoryBtn) {
        viewFullAdvisoryBtn.addEventListener('click', () => {
            switchPage('page-advisory');
        });
    }

    // -------------------------------------------------------------
    // 2. Scanner & Camera Controls
    // -------------------------------------------------------------
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const dropzonePrompt = document.getElementById('dropzonePrompt');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeImgBtn = document.getElementById('removeImgBtn');
    const scannerLaser = document.getElementById('scannerLaser');
    const diagnoseBtn = document.getElementById('diagnoseBtn');
    const btnSpinner = document.getElementById('btnSpinner');
    
    const modeUploadBtn = document.getElementById('modeUploadBtn');
    const modeCameraBtn = document.getElementById('modeCameraBtn');
    const switchCameraBtn = document.getElementById('switchCameraBtn');
    const captureBtn = document.getElementById('captureBtn');
    const closeCameraBtn = document.getElementById('closeCameraBtn');

    const samplesContainer = document.getElementById('samplesContainer');
    const catalogGrid = document.getElementById('catalogGrid');
    const languageSelect = document.getElementById('languageSelect');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

    let selectedFile = null;

    loadSamples();
    loadCatalog();

    languageSelect.addEventListener('change', (e) => {
        window.translationManager.setLanguage(e.target.value);
    });

    // Scanner Mode Switchers
    modeUploadBtn.addEventListener('click', () => {
        modeUploadBtn.classList.add('active');
        modeCameraBtn.classList.remove('active');
        window.cameraManager.closeCamera();
    });

    modeCameraBtn.addEventListener('click', async () => {
        modeCameraBtn.classList.add('active');
        modeUploadBtn.classList.remove('active');
        const opened = await window.cameraManager.openCamera();
        if (!opened) {
            modeUploadBtn.classList.add('active');
            modeCameraBtn.classList.remove('active');
        }
    });

    switchCameraBtn.addEventListener('click', () => {
        window.cameraManager.switchCamera();
    });

    closeCameraBtn.addEventListener('click', () => {
        window.cameraManager.closeCamera();
        modeUploadBtn.classList.add('active');
        modeCameraBtn.classList.remove('active');
    });

    captureBtn.addEventListener('click', async () => {
        const capturedFile = await window.cameraManager.captureSnapshot();
        if (capturedFile) {
            handleFileSelection(capturedFile);
            modeUploadBtn.classList.add('active');
            modeCameraBtn.classList.remove('active');
            runDiagnosisFlow();
        }
    });

    // Drag and Drop & Browsing
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropzone.addEventListener('click', () => {
        if (!selectedFile) fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelection(e.target.files[0]);
        }
    });

    ['dragenter', 'dragover'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('drag-over');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt.files && dt.files[0]) {
            handleFileSelection(dt.files[0]);
        }
    });

    removeImgBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploader();
    });

    diagnoseBtn.addEventListener('click', runDiagnosisFlow);

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', () => {
            window.predictionController.clearHistory();
        });
    }

    // -------------------------------------------------------------
    // 3. "Ask TomatoGuard" Assistant Query Form & Preset Chips
    // -------------------------------------------------------------
    const assistantForm = document.getElementById('assistantForm');
    const assistantInput = document.getElementById('assistantInput');
    const assistantChatBox = document.getElementById('assistantChatBox');
    const presetChips = document.querySelectorAll('.preset-chip');

    presetChips.forEach(chip => {
        chip.addEventListener('click', () => {
            assistantInput.value = chip.textContent;
            sendAssistantQuery(chip.textContent);
        });
    });

    assistantForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = assistantInput.value.trim();
        if (!text) return;
        sendAssistantQuery(text);
    });

    async function sendAssistantQuery(queryText) {
        appendChatMessage('user', queryText);
        assistantInput.value = '';

        try {
            const currentDisease = window.predictionController.currentDiseaseKey;
            const res = await fetch('/api/assistant/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: queryText,
                    current_disease: currentDisease
                })
            });

            const data = await res.json();
            appendChatMessage('bot', data.response);
        } catch (err) {
            appendChatMessage('bot', '⚠️ Could not connect to the advisory assistant. Please try again.');
        }
    }

    function appendChatMessage(sender, messageText) {
        const row = document.createElement('div');
        row.className = `chat-message ${sender}`;
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.textContent = messageText;
        row.appendChild(bubble);
        assistantChatBox.appendChild(row);
        assistantChatBox.scrollTop = assistantChatBox.scrollHeight;
    }

    // -------------------------------------------------------------
    // 4. File Handling & Diagnosis Flow
    // -------------------------------------------------------------
    function handleFileSelection(file) {
        selectedFile = file;
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
        selectedFile = null;
        fileInput.value = '';
        imagePreview.src = '';
        previewContainer.classList.add('hidden');
        dropzonePrompt.classList.remove('hidden');
        diagnoseBtn.disabled = true;
        window.predictionController.resetPipeline();
    }

    async function runDiagnosisFlow() {
        if (!selectedFile) return;

        diagnoseBtn.disabled = true;
        btnSpinner.classList.remove('hidden');
        dropzone.classList.add('is-scanning');

        try {
            await window.predictionController.runDiagnosis(selectedFile);
        } finally {
            diagnoseBtn.disabled = false;
            btnSpinner.classList.add('hidden');
            dropzone.classList.remove('is-scanning');
        }
    }

    async function loadSamples() {
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
                            handleFileSelection(file);
                            runDiagnosisFlow();
                        } catch (err) {
                            console.error('Failed to load sample blob:', err);
                        }
                    });
                    samplesContainer.appendChild(thumb);
                });
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
                    <p class="catalog-pathogen">${item.scientific_name || item.pathogen_type}</p>
                    <p class="catalog-desc">${item.symptoms_preview || 'Foliar pathology.'}</p>
                `;
                catalogGrid.appendChild(card);
            });
        } catch (e) {
            console.error('Failed to load catalog:', e);
        }
    }
});
