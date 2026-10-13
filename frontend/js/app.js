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
    // 3. "Ask TomatoGuard" Assistant Query Form, Preset Chips & AI Settings
    // -------------------------------------------------------------
    const assistantForm = document.getElementById('assistantForm');
    const assistantInput = document.getElementById('assistantInput');
    const assistantChatBox = document.getElementById('assistantChatBox');
    const assistantSubmitBtn = document.getElementById('assistantSubmitBtn');
    const presetChips = document.querySelectorAll('.preset-chip');
    const aiStatusBadge = document.getElementById('aiStatusBadge');

    // AI Settings Modal Elements
    const openAiSettingsBtn = document.getElementById('openAiSettingsBtn');
    const closeAiSettingsBtn = document.getElementById('closeAiSettingsBtn');
    const aiSettingsModal = document.getElementById('aiSettingsModal');
    const aiProviderSelect = document.getElementById('aiProviderSelect');
    const aiApiKeyInput = document.getElementById('aiApiKeyInput');
    const aiModelInput = document.getElementById('aiModelInput');
    const aiBaseUrlInput = document.getElementById('aiBaseUrlInput');
    const apiKeyGroup = document.getElementById('apiKeyGroup');
    const customUrlGroup = document.getElementById('customUrlGroup');
    const getKeyLink = document.getElementById('getKeyLink');
    const keyHint = document.getElementById('keyHint');
    const toggleApiKeyVisibility = document.getElementById('toggleApiKeyVisibility');
    const testAiKeyBtn = document.getElementById('testAiKeyBtn');
    const saveAiConfigBtn = document.getElementById('saveAiConfigBtn');
    const aiTestFeedback = document.getElementById('aiTestFeedback');

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
        if (assistantSubmitBtn) assistantSubmitBtn.disabled = true;

        // Show typing indicator
        const typingId = 'typing-' + Date.now();
        appendTypingIndicator(typingId);

        try {
            const currentDisease = window.predictionController ? window.predictionController.currentDiseaseKey : null;
            const res = await fetch('/api/assistant/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: queryText,
                    current_disease: currentDisease
                })
            });

            removeTypingIndicator(typingId);

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const data = await res.json();
            appendChatMessage('bot', data.response);
        } catch (err) {
            removeTypingIndicator(typingId);
            appendChatMessage('bot', '⚠️ Could not connect to the advisory assistant. Please check your internet connection or verify your API key in AI Settings.');
        } finally {
            if (assistantSubmitBtn) assistantSubmitBtn.disabled = false;
        }
    }

    function appendTypingIndicator(id) {
        const row = document.createElement('div');
        row.className = 'chat-message bot';
        row.id = id;
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.innerHTML = '<em>Thinking &amp; consulting AI Advisor...</em> <span class="typing-dots">⏳</span>';
        row.appendChild(bubble);
        assistantChatBox.appendChild(row);
        assistantChatBox.scrollTop = assistantChatBox.scrollHeight;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function formatMarkdownText(rawText) {
        if (!rawText) return '';
        let escaped = rawText
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Check for Markdown tables
        const tableRegex = /((?:\|.+?\|\r?\n)+)/g;
        escaped = escaped.replace(tableRegex, (match) => {
            const lines = match.trim().split(/\r?\n/);
            if (lines.length < 2) return match;
            let html = '<div style="overflow-x:auto;"><table>';
            lines.forEach((line, idx) => {
                const cells = line.split('|').map(c => c.trim()).filter((_, i, arr) => i > 0 && i < arr.length - 1);
                if (line.includes('---')) return; // separator
                if (idx === 0) {
                    html += '<thead><tr>' + cells.map(c => `<th>${c}</th>`).join('') + '</tr></thead><tbody>';
                } else {
                    html += '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
                }
            });
            html += '</tbody></table></div>';
            return html;
        });

        // Bold & Italic
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Headers
        escaped = escaped.replace(/^### (.*$)/gim, '<h4 style="color:#34d399;margin:8px 0 4px 0;">$1</h4>');
        escaped = escaped.replace(/^## (.*$)/gim, '<h3 style="color:#34d399;margin:10px 0 6px 0;">$1</h3>');

        // Bullet points
        escaped = escaped.replace(/^[•\-\*]\s+(.*$)/gim, '<li style="margin-left:14px;">$1</li>');

        // New lines to <br>
        escaped = escaped.replace(/\n\n+/g, '<br><br>');
        escaped = escaped.replace(/\n/g, '<br>');

        return escaped;
    }

    function appendChatMessage(sender, messageText) {
        const row = document.createElement('div');
        row.className = `chat-message ${sender}`;
        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble';

        if (sender === 'bot') {
            bubble.innerHTML = formatMarkdownText(messageText);
        } else {
            bubble.textContent = messageText;
        }

        row.appendChild(bubble);
        assistantChatBox.appendChild(row);
        assistantChatBox.scrollTop = assistantChatBox.scrollHeight;
    }

    // AI Provider & Key Settings Management
    if (openAiSettingsBtn && aiSettingsModal) {
        openAiSettingsBtn.addEventListener('click', () => {
            loadAiConfigIntoModal();
            aiSettingsModal.classList.remove('hidden');
        });

        closeAiSettingsBtn.addEventListener('click', () => {
            aiSettingsModal.classList.add('hidden');
        });

        aiSettingsModal.addEventListener('click', (e) => {
            if (e.target === aiSettingsModal) {
                aiSettingsModal.classList.add('hidden');
            }
        });

        if (toggleApiKeyVisibility) {
            toggleApiKeyVisibility.addEventListener('click', () => {
                if (aiApiKeyInput.type === 'password') {
                    aiApiKeyInput.type = 'text';
                    toggleApiKeyVisibility.textContent = '🔒';
                } else {
                    aiApiKeyInput.type = 'password';
                    toggleApiKeyVisibility.textContent = '👁️';
                }
            });
        }

        if (aiProviderSelect) {
            aiProviderSelect.addEventListener('change', updateProviderFormFields);
        }

        if (testAiKeyBtn) {
            testAiKeyBtn.addEventListener('click', async () => {
                const provider = aiProviderSelect.value;
                const apiKey = aiApiKeyInput.value.trim();
                const model = aiModelInput.value.trim();

                aiTestFeedback.className = 'test-feedback-box loading';
                aiTestFeedback.innerHTML = '⏳ Testing connection to AI service...';
                aiTestFeedback.classList.remove('hidden');

                try {
                    const res = await fetch('/api/assistant/test-key', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            provider: provider,
                            api_key: apiKey,
                            model: model
                        })
                    });
                    const data = await res.json();
                    if (data.success) {
                        aiTestFeedback.className = 'test-feedback-box success';
                        aiTestFeedback.innerHTML = `✅ <strong>Success!</strong> ${data.message}`;
                    } else {
                        aiTestFeedback.className = 'test-feedback-box error';
                        aiTestFeedback.innerHTML = `❌ <strong>Test failed:</strong> ${data.message || 'Check your key and try again.'}`;
                    }
                } catch (e) {
                    aiTestFeedback.className = 'test-feedback-box error';
                    aiTestFeedback.innerHTML = `❌ Connection error: ${e.message}`;
                }
            });
        }

        if (saveAiConfigBtn) {
            saveAiConfigBtn.addEventListener('click', async () => {
                const provider = aiProviderSelect.value;
                const apiKey = aiApiKeyInput.value.trim();
                const model = aiModelInput.value.trim();
                const baseUrl = aiBaseUrlInput ? aiBaseUrlInput.value.trim() : '';

                saveAiConfigBtn.disabled = true;
                saveAiConfigBtn.textContent = '💾 Saving...';

                try {
                    const res = await fetch('/api/assistant/config', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            provider: provider,
                            api_key: apiKey,
                            model: model,
                            base_url: baseUrl
                        })
                    });
                    const data = await res.json();
                    if (data.success) {
                        aiTestFeedback.className = 'test-feedback-box success';
                        aiTestFeedback.innerHTML = `✅ <strong>Settings Saved!</strong> Now running on ${provider.toUpperCase()}.`;
                        aiTestFeedback.classList.remove('hidden');
                        updateBadgeFromConfig(data.config);
                        setTimeout(() => {
                            aiSettingsModal.classList.add('hidden');
                            saveAiConfigBtn.disabled = false;
                            saveAiConfigBtn.textContent = '💾 Save & Connect';
                        }, 1200);
                    } else {
                        aiTestFeedback.className = 'test-feedback-box error';
                        aiTestFeedback.innerHTML = `❌ Failed to save: ${data.message}`;
                        aiTestFeedback.classList.remove('hidden');
                        saveAiConfigBtn.disabled = false;
                        saveAiConfigBtn.textContent = '💾 Save & Connect';
                    }
                } catch (e) {
                    aiTestFeedback.className = 'test-feedback-box error';
                    aiTestFeedback.innerHTML = `❌ Save failed: ${e.message}`;
                    aiTestFeedback.classList.remove('hidden');
                    saveAiConfigBtn.disabled = false;
                    saveAiConfigBtn.textContent = '💾 Save & Connect';
                }
            });
        }
    }

    function updateProviderFormFields() {
        const prov = aiProviderSelect.value;
        aiTestFeedback.classList.add('hidden');

        if (prov === 'free_cloud') {
            apiKeyGroup.classList.add('hidden');
            customUrlGroup.classList.add('hidden');
            aiModelInput.placeholder = 'Default: openai (cloud)';
            if (keyHint) keyHint.textContent = 'Zero setup required! Free Cloud AI works out of the box.';
        } else if (prov === 'gemini') {
            apiKeyGroup.classList.remove('hidden');
            customUrlGroup.classList.add('hidden');
            getKeyLink.href = 'https://aistudio.google.com/app/apikey';
            getKeyLink.textContent = 'Get Free Gemini Key ↗';
            getKeyLink.classList.remove('hidden');
            aiApiKeyInput.placeholder = 'Paste Gemini API Key (starts with AIzaSy...)';
            aiModelInput.placeholder = 'Default: gemini-1.5-flash';
            if (keyHint) keyHint.textContent = 'Google Gemini offers a 100% free tier at Google AI Studio.';
        } else if (prov === 'openai') {
            apiKeyGroup.classList.remove('hidden');
            customUrlGroup.classList.add('hidden');
            getKeyLink.href = 'https://platform.openai.com/api-keys';
            getKeyLink.textContent = 'Get OpenAI Key ↗';
            getKeyLink.classList.remove('hidden');
            aiApiKeyInput.placeholder = 'Paste OpenAI API Key (starts with sk-...)';
            aiModelInput.placeholder = 'Default: gpt-4o-mini';
            if (keyHint) keyHint.textContent = 'Keys are saved locally in .env and sent only to official OpenAI endpoints.';
        } else if (prov === 'groq') {
            apiKeyGroup.classList.remove('hidden');
            customUrlGroup.classList.add('hidden');
            getKeyLink.href = 'https://console.groq.com/keys';
            getKeyLink.textContent = 'Get Free Groq Key ↗';
            getKeyLink.classList.remove('hidden');
            aiApiKeyInput.placeholder = 'Paste Groq API Key (starts with gsk_...)';
            aiModelInput.placeholder = 'Default: openai/gpt-oss-120b';
            if (keyHint) keyHint.textContent = 'Groq Cloud provides ultra-fast LLM inference.';

        } else if (prov === 'custom') {
            apiKeyGroup.classList.remove('hidden');
            customUrlGroup.classList.remove('hidden');
            getKeyLink.classList.add('hidden');
            aiApiKeyInput.placeholder = 'Enter API Key for your custom endpoint';
            aiModelInput.placeholder = 'Model identifier';
            if (keyHint) keyHint.textContent = 'Any OpenAI-compatible server (vLLM, Ollama, OpenRouter, etc.)';
        }
    }

    async function loadAiConfigIntoModal() {
        try {
            const res = await fetch('/api/assistant/config');
            const cfg = await res.json();
            if (cfg && cfg.provider) {
                aiProviderSelect.value = cfg.provider;
                aiModelInput.value = cfg.model || '';
                if (cfg.has_custom_key && cfg.masked_key) {
                    aiApiKeyInput.value = cfg.masked_key;
                }
                if (aiBaseUrlInput && cfg.base_url) {
                    aiBaseUrlInput.value = cfg.base_url;
                }
                updateProviderFormFields();
                updateBadgeFromConfig(cfg);
            }
        } catch (e) {
            console.warn('Could not load AI config:', e);
        }
    }

    function updateBadgeFromConfig(cfg) {
        if (!aiStatusBadge) return;
        if (!cfg) return;
        if (cfg.has_custom_key) {
            aiStatusBadge.onclick = null;
            aiStatusBadge.style.cursor = 'default';
            if (cfg.provider === 'gemini') {
                aiStatusBadge.textContent = '⚡ Gemini AI Connected';
                aiStatusBadge.style.color = '#38bdf8';
                aiStatusBadge.style.borderColor = 'rgba(56, 189, 248, 0.4)';
            } else if (cfg.provider === 'openai') {
                aiStatusBadge.textContent = '🧠 OpenAI Connected';
                aiStatusBadge.style.color = '#a78bfa';
                aiStatusBadge.style.borderColor = 'rgba(167, 139, 250, 0.4)';
            } else if (cfg.provider === 'groq') {
                aiStatusBadge.textContent = '🚀 Groq Connected';
                aiStatusBadge.style.color = '#f59e0b';
                aiStatusBadge.style.borderColor = 'rgba(245, 158, 11, 0.4)';
            } else {
                aiStatusBadge.textContent = '🟢 AI Connected';
                aiStatusBadge.style.color = '#34d399';
                aiStatusBadge.style.borderColor = 'rgba(52, 211, 153, 0.4)';
            }
        } else {
            aiStatusBadge.textContent = '🔑 Connect AI Key to Enable Live Q&A';
            aiStatusBadge.style.color = '#fbbf24';
            aiStatusBadge.style.borderColor = 'rgba(251, 191, 36, 0.5)';
            aiStatusBadge.style.cursor = 'pointer';
            aiStatusBadge.title = 'Click to connect your Google Gemini or OpenAI API key';
            aiStatusBadge.onclick = () => {
                if (openAiSettingsBtn) openAiSettingsBtn.click();
            };
        }
    }

    // Initial check on load
    loadAiConfigIntoModal();


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

    // -------------------------------------------------------------
    // 5. Real-Time Live Farm Weather & Rain Forecast
    // -------------------------------------------------------------
    const weatherIcon = document.getElementById('weatherIcon');
    const weatherLocationName = document.getElementById('weatherLocationName');
    const btnDetectLocation = document.getElementById('btnDetectLocation');
    const btnRefreshWeather = document.getElementById('btnRefreshWeather');
    const currentTempDisplay = document.getElementById('currentTempDisplay');
    const weatherConditionText = document.getElementById('weatherConditionText');
    const tempRangeText = document.getElementById('tempRangeText');
    const rainStatusPill = document.getElementById('rainStatusPill');
    const rainPillBadge = document.getElementById('rainPillBadge');
    const rainChanceText = document.getElementById('rainChanceText');
    const rainAdvisoryBanner = document.getElementById('rainAdvisoryBanner');
    const rainAdvIcon = document.getElementById('rainAdvIcon');
    const rainAdvHeading = document.getElementById('rainAdvHeading');
    const rainAdvText = document.getElementById('rainAdvText');
    const weatherRainSum = document.getElementById('weatherRainSum');
    const weatherHumidity = document.getElementById('weatherHumidity');
    const weatherWind = document.getElementById('weatherWind');
    const weatherClouds = document.getElementById('weatherClouds');

    let currentLat = 13.1362;
    let currentLon = 78.1291;
    let currentLocationLabel = 'Kolar, Karnataka (Tomato Belt)';

    function getWeatherMeta(code) {
        if (code === 0) return { icon: '☀️', condition: 'Clear Sky' };
        if (code === 1) return { icon: '🌤️', condition: 'Mainly Clear' };
        if (code === 2) return { icon: '⛅', condition: 'Partly Cloudy' };
        if (code === 3) return { icon: '☁️', condition: 'Overcast Skies' };
        if (code >= 45 && code <= 48) return { icon: '🌫️', condition: 'Fog / Morning Mist' };
        if (code >= 51 && code <= 55) return { icon: '🌦️', condition: 'Light Drizzle' };
        if (code >= 61 && code <= 65) return { icon: '🌧️', condition: 'Rain' };
        if (code >= 80 && code <= 82) return { icon: '🌧️', condition: 'Rain Showers' };
        if (code >= 95) return { icon: '⛈️', condition: 'Thunderstorm' };
        return { icon: '🌤️', condition: 'Fair Weather' };
    }

    async function fetchLiveWeather(lat = currentLat, lon = currentLon, label = currentLocationLabel) {
        if (!currentTempDisplay) return;

        if (btnRefreshWeather) {
            btnRefreshWeather.style.transform = 'rotate(360deg)';
            btnRefreshWeather.style.transition = 'transform 0.6s ease';
            setTimeout(() => { btnRefreshWeather.style.transform = 'none'; }, 600);
        }

        try {
            const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,cloud_cover,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&timezone=auto`;
            const res = await fetch(url);
            if (!res.ok) throw new Error('Weather API error');
            const data = await res.json();

            const current = data.current;
            const daily = data.daily;
            const meta = getWeatherMeta(current.weather_code);

            // 1. Update Temperature & Condition
            weatherIcon.textContent = meta.icon;
            weatherLocationName.textContent = label;
            currentTempDisplay.textContent = Math.round(current.temperature_2m);
            weatherConditionText.textContent = meta.condition;

            const maxT = Math.round(daily.temperature_2m_max?.[0] ?? current.temperature_2m);
            const minT = Math.round(daily.temperature_2m_min?.[0] ?? (current.temperature_2m - 7));
            tempRangeText.textContent = `Today Max: ${maxT}°C • Min: ${minT}°C`;

            // 2. Will It Rain Today? Decision & Visual Status
            const rainProb = daily.precipitation_probability_max?.[0] ?? 0;
            const rainSum = daily.precipitation_sum?.[0] ?? current.precipitation ?? 0;
            const willRainToday = (rainProb >= 35) || (rainSum >= 0.5) || (current.weather_code >= 51 && current.weather_code <= 99);

            if (willRainToday) {
                rainPillBadge.textContent = '🌧️ Rain Expected Today';
                rainPillBadge.className = 'rain-pill-badge rain-yes';
                rainChanceText.textContent = `Probability: ${rainProb}% • Expected: ${rainSum.toFixed(1)} mm`;

                rainAdvisoryBanner.className = 'rain-advisory-banner rain-caution';
                rainAdvIcon.textContent = '⚠️';
                rainAdvHeading.textContent = 'Postpone Foliar Spraying (High Wash-Off Risk)';
                rainAdvText.textContent = `Rain is forecasted today (${rainProb}% chance, ~${rainSum.toFixed(1)} mm). Postpone chemical/organic foliar spraying to prevent pesticide wash-off. Inspect drainage ditches to avoid root rot.`;
            } else {
                rainPillBadge.textContent = '☀️ No Rain Today (Dry)';
                rainPillBadge.className = 'rain-pill-badge rain-no';
                rainChanceText.textContent = `Dry forecast: ${rainProb}% chance (0.0 mm)`;

                rainAdvisoryBanner.className = 'rain-advisory-banner';
                rainAdvIcon.textContent = '✅';
                rainAdvHeading.textContent = 'Safe Window for Spraying & Foliar Treatment';
                rainAdvText.textContent = `No rain forecasted today (${rainProb}% chance). Foliage will stay dry, providing an ideal window for protective bio-fungicide sprays, foliar fertilizers, or scheduled drip fertigation.`;
            }

            // 3. Micro-climate metrics
            weatherRainSum.textContent = `${rainSum.toFixed(1)} mm`;
            weatherHumidity.textContent = `${Math.round(current.relative_humidity_2m)}%`;
            weatherWind.textContent = `${Math.round(current.wind_speed_10m)} km/h`;
            weatherClouds.textContent = `${Math.round(current.cloud_cover)}%`;

        } catch (err) {
            console.error('Failed to load real-time weather:', err);
            weatherConditionText.textContent = 'Weather Offline (Using Local Sensor Default)';
            currentTempDisplay.textContent = '28';
            tempRangeText.textContent = 'Max: 30°C • Min: 20°C';
            rainPillBadge.textContent = '☀️ No Rain Today';
            rainPillBadge.className = 'rain-pill-badge rain-no';
            rainChanceText.textContent = 'Dry forecast (< 15%)';
            weatherHumidity.textContent = '55%';
            weatherWind.textContent = '12 km/h';
            weatherClouds.textContent = '20%';
            weatherRainSum.textContent = '0.0 mm';
        }
    }

    if (btnRefreshWeather) {
        btnRefreshWeather.addEventListener('click', () => fetchLiveWeather());
    }

    if (btnDetectLocation) {
        btnDetectLocation.addEventListener('click', () => {
            if (!('geolocation' in navigator)) {
                alert('Geolocation is not supported by your browser.');
                return;
            }
            btnDetectLocation.textContent = '🛰️ Locating...';
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    currentLat = pos.coords.latitude;
                    currentLon = pos.coords.longitude;
                    currentLocationLabel = `My Farm (${currentLat.toFixed(2)}°, ${currentLon.toFixed(2)}°)`;
                    btnDetectLocation.textContent = '✓ Located';
                    setTimeout(() => { btnDetectLocation.textContent = '📡 Auto-Detect'; }, 2000);
                    fetchLiveWeather(currentLat, currentLon, currentLocationLabel);
                },
                (err) => {
                    console.warn('Geolocation failed:', err.message);
                    btnDetectLocation.textContent = '📡 Auto-Detect';
                    alert('Could not retrieve GPS coordinates. Defaulting to regional farm location.');
                },
                { timeout: 8000 }
            );
        });
    }

    // Initialize real-time weather immediately on load
    fetchLiveWeather();

    // -------------------------------------------------------------
    // 6. Voice Spoken Audio Guidance (TTS)
    // -------------------------------------------------------------
    const speakAdvisoryBtn = document.getElementById('speakAdvisoryBtn');
    const stopAudioBtn = document.getElementById('stopAudioBtn');

    if (speakAdvisoryBtn && stopAudioBtn) {
        speakAdvisoryBtn.addEventListener('click', () => {
            if (!('speechSynthesis' in window)) {
                alert('Speech synthesis is not supported on this browser.');
                return;
            }

            window.speechSynthesis.cancel();
            const pred = window.predictionController.lastPredictionData;
            let textToSpeak = '';

            if (pred && pred.is_tomato) {
                textToSpeak = `TomatoGuard Agronomy Report for ${pred.disease}. `;
                if (pred.is_healthy) {
                    textToSpeak += `Your tomato crop is in healthy condition with a health score of ${pred.health_score} out of 100. Continue regular watering and balanced nitrogen feeding.`;
                } else {
                    textToSpeak += `Detected severity level ${pred.severity}. `;
                    if (pred.action_plan) {
                        textToSpeak += `Action for today: ${pred.action_plan.today}. `;
                        textToSpeak += `Action for the next three days: ${pred.action_plan.next_3_days}. `;
                    }
                    if (pred.organic_treatment && pred.organic_treatment.length > 0) {
                        textToSpeak += `Recommended organic treatment: ${pred.organic_treatment[0]}. `;
                    }
                    if (pred.chemical_treatment && pred.chemical_treatment.length > 0) {
                        textToSpeak += `Prescribed chemical treatment: ${pred.chemical_treatment[0]}. Strictly observe pre-harvest safety interval.`;
                    }
                }
            } else {
                textToSpeak = 'Welcome to TomatoGuard AI Farmer Guidance Hub. Please scan a tomato leaf to listen to customized prescription audio. Best general practice: maintain drip irrigation to keep canopy foliage dry, and rotate crops every two seasons.';
            }

            const utterance = new SpeechSynthesisUtterance(textToSpeak);
            utterance.rate = 0.95;
            utterance.pitch = 1.0;

            utterance.onstart = () => {
                speakAdvisoryBtn.classList.add('hidden');
                stopAudioBtn.classList.remove('hidden');
            };

            utterance.onend = () => {
                speakAdvisoryBtn.classList.remove('hidden');
                stopAudioBtn.classList.add('hidden');
            };

            utterance.onerror = () => {
                speakAdvisoryBtn.classList.remove('hidden');
                stopAudioBtn.classList.add('hidden');
            };

            window.speechSynthesis.speak(utterance);
        });

        stopAudioBtn.addEventListener('click', () => {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
            }
            speakAdvisoryBtn.classList.remove('hidden');
            stopAudioBtn.classList.add('hidden');
        });
    }

    // -------------------------------------------------------------
    // 7. Voice Query Assistant (Speech Recognition STT)
    // -------------------------------------------------------------
    const voiceMicBtn = document.getElementById('voiceMicBtn');
    if (voiceMicBtn) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-IN';

            recognition.onstart = () => {
                voiceMicBtn.classList.add('listening');
                voiceMicBtn.title = 'Listening to your voice... Speak now!';
            };

            recognition.onresult = (event) => {
                const speechText = event.results[0][0].transcript;
                if (speechText && assistantInput) {
                    assistantInput.value = speechText;
                    sendAssistantQuery(speechText);
                }
            };

            recognition.onerror = () => {
                voiceMicBtn.classList.remove('listening');
                voiceMicBtn.title = 'Voice mic ready';
            };

            recognition.onend = () => {
                voiceMicBtn.classList.remove('listening');
                voiceMicBtn.title = 'Voice mic ready';
            };

            voiceMicBtn.addEventListener('click', () => {
                try {
                    recognition.start();
                } catch (e) {
                    recognition.stop();
                }
            });
        } else {
            voiceMicBtn.addEventListener('click', () => {
                alert('Voice speech recognition is not supported in this browser. Please use Chrome or Edge.');
            });
        }
    }

    // -------------------------------------------------------------
    // 8. Farm Plots & Field Health Tracker
    // -------------------------------------------------------------
    const plotsGrid = document.getElementById('plotsGrid');
    const addNewPlotBtn = document.getElementById('addNewPlotBtn');
    const activePlotSelect = document.getElementById('activePlotSelect');

    const DEFAULT_PLOTS = [
        { id: 'plot-1', name: 'Plot North A (Hybrid)', area: '2.5 Acres', variety: 'Arka Rakshak F1', planted: '45 days ago' },
        { id: 'plot-2', name: 'Plot South B (Organic)', area: '1.8 Acres', variety: 'Pusa Ruby', planted: '30 days ago' },
        { id: 'plot-3', name: 'Greenhouse 1', area: '0.8 Acres', variety: 'Cherry Sensation', planted: '20 days ago' }
    ];

    function getPlots() {
        try {
            const saved = localStorage.getItem('tomatoguard_plots');
            return saved ? JSON.parse(saved) : DEFAULT_PLOTS;
        } catch (e) {
            return DEFAULT_PLOTS;
        }
    }

    function savePlots(plots) {
        localStorage.setItem('tomatoguard_plots', JSON.stringify(plots));
        syncPlotDropdown(plots);
        renderPlots();
    }

    function syncPlotDropdown(plots) {
        if (!activePlotSelect) return;
        const currentVal = activePlotSelect.value;
        activePlotSelect.innerHTML = '';
        plots.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.name;
            opt.textContent = p.name;
            activePlotSelect.appendChild(opt);
        });
        if (plots.some(p => p.name === currentVal)) {
            activePlotSelect.value = currentVal;
        }
    }

    function renderPlots() {
        if (!plotsGrid) return;
        const plots = getPlots();
        const history = JSON.parse(localStorage.getItem('tomatoguard_history') || '[]');

        plotsGrid.innerHTML = '';
        plots.forEach(plot => {
            const plotScans = history.filter(h => h.plot_name === plot.name);
            const totalScans = plotScans.length;
            let avgScore = 85;
            let latestCondition = 'Optimal Foliage Health';

            if (totalScans > 0) {
                const sum = plotScans.reduce((acc, curr) => acc + (parseInt(curr.health_score, 10) || 75), 0);
                avgScore = Math.round(sum / totalScans);
                latestCondition = plotScans[0].disease || 'Inspected';
            }

            let statusClass = 'status-green';
            let statusBadge = '🟢 Optimal';
            if (avgScore < 50) {
                statusClass = 'status-red';
                statusBadge = '🔴 Critical Action';
            } else if (avgScore < 75) {
                statusClass = 'status-yellow';
                statusBadge = '🟡 Attention Needed';
            }

            const card = document.createElement('div');
            card.className = `plot-card ${statusClass}`;
            card.innerHTML = `
                <div class="plot-card-header">
                    <div>
                        <h3 class="plot-name">${plot.name}</h3>
                        <p class="plot-sub">${plot.area} &bull; ${plot.variety}</p>
                    </div>
                    <span class="plot-status-badge">${statusBadge}</span>
                </div>
                <div class="plot-kpis">
                    <div class="plot-kpi-item">
                        <span class="plot-kpi-val">${avgScore}/100</span>
                        <span class="plot-kpi-lbl">Health Index</span>
                    </div>
                    <div class="plot-kpi-item">
                        <span class="plot-kpi-val">${totalScans}</span>
                        <span class="plot-kpi-lbl">Total Scans</span>
                    </div>
                    <div class="plot-kpi-item">
                        <span class="plot-kpi-val">${plot.planted}</span>
                        <span class="plot-kpi-lbl">Plant Age</span>
                    </div>
                </div>
                <div class="plot-last-scan">
                    <span>Recent Diagnosis:</span>
                    <strong>${latestCondition}</strong>
                </div>
                <div class="plot-actions-row">
                    <button type="button" class="btn btn-secondary btn-sm switch-plot-btn" data-plot-name="${plot.name}">
                        🌿 Scan This Plot
                    </button>
                </div>
            `;
            plotsGrid.appendChild(card);
        });

        // Attach switch plot buttons
        document.querySelectorAll('.switch-plot-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const plotName = e.currentTarget.dataset.plotName;
                if (activePlotSelect && plotName) {
                    activePlotSelect.value = plotName;
                }
                switchPage('page-scanner');
            });
        });
    }

    if (addNewPlotBtn) {
        addNewPlotBtn.addEventListener('click', () => {
            const plotName = prompt('Enter Farm Plot Name (e.g. Field East Block 3):');
            if (!plotName || !plotName.trim()) return;
            const area = prompt('Enter Area Size (e.g. 1.5 Acres):', '1.5 Acres') || '1.0 Acre';
            const variety = prompt('Enter Tomato Cultivar/Variety (e.g. Arka Vikas):', 'Arka Vikas') || 'Local Tomato';

            const plots = getPlots();
            plots.push({
                id: `plot-${Date.now()}`,
                name: plotName.trim(),
                area: area.trim(),
                variety: variety.trim(),
                planted: 'Newly Registered'
            });
            savePlots(plots);
        });
    }

    window.plotsManager = { renderPlots, getPlots };
    syncPlotDropdown(getPlots());
    renderPlots();
});

