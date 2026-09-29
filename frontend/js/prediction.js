// -*- coding: utf-8 -*-
/**
 * Diagnostic Prediction & UI Pipeline Controller (Supports Multi-Page & Multilingual Updates)
 */

class PredictionController {
    constructor() {
        // DOM Elements - Scanner Page
        this.emptyState = document.getElementById('emptyState');
        this.nonTomatoCard = document.getElementById('nonTomatoCard');
        this.nonTomatoConfidence = document.getElementById('nonTomatoConfidence');
        this.qualityFailCard = document.getElementById('qualityFailCard');
        this.qualityFailReason = document.getElementById('qualityFailReason');
        this.qualityFailSuggestion = document.getElementById('qualityFailSuggestion');
        
        this.diagnosisContent = document.getElementById('diagnosisContent');
        this.diagnosisName = document.getElementById('diagnosisName');
        this.pathogenName = document.getElementById('pathogenName');
        this.bannerTomatoConf = document.getElementById('bannerTomatoConf');
        this.severityBadge = document.getElementById('severityBadge');
        this.healthScoreValue = document.getElementById('healthScoreValue');
        
        this.gaugeValue = document.getElementById('gaugeValue');
        this.confidenceFill = document.getElementById('confidenceFill');
        this.probList = document.getElementById('probList');
        this.aiSummaryText = document.getElementById('aiSummaryText');
        
        // DOM Elements - Dedicated Advisory Page
        this.advisoryActionToday = document.getElementById('advisoryActionToday');
        this.advisoryActionNext3 = document.getElementById('advisoryActionNext3');
        this.advisoryActionWeek = document.getElementById('advisoryActionWeek');
        this.advisorySymptomsList = document.getElementById('advisorySymptomsList');
        this.advisoryOrganicList = document.getElementById('advisoryOrganicList');
        this.advisoryChemicalList = document.getElementById('advisoryChemicalList');
        this.advisoryPreventionList = document.getElementById('advisoryPreventionList');

        // History
        this.historyGrid = document.getElementById('historyGrid');
        
        // Pipeline steps
        this.pipeStep1 = document.getElementById('pipeStep1');
        this.pipeStep2 = document.getElementById('pipeStep2');
        this.pipeStep3 = document.getElementById('pipeStep3');
        this.pipeStep4 = document.getElementById('pipeStep4');

        this.currentDiseaseKey = null;
        this.lastPredictionData = null;
        this.loadHistory();
    }

    setPipelineProgress(stepIndex, isSuccess = true) {
        const steps = [this.pipeStep1, this.pipeStep2, this.pipeStep3, this.pipeStep4];
        steps.forEach((s, idx) => {
            if (!s) return;
            s.classList.remove('active', 'completed', 'failed');
            if (idx < stepIndex) {
                s.classList.add('completed');
            } else if (idx === stepIndex) {
                s.classList.add(isSuccess ? 'active' : 'failed');
            }
        });
    }

    resetPipeline() {
        [this.pipeStep1, this.pipeStep2, this.pipeStep3, this.pipeStep4].forEach(s => {
            if (s) s.classList.remove('active', 'completed', 'failed');
        });
    }

    async runDiagnosis(file) {
        if (!file) return;

        // Reset UI states
        this.hideAllOutputs();
        this.setPipelineProgress(0); // Step 1: Image Check active

        const currentLang = window.translationManager ? window.translationManager.currentLang : 'en';
        const formData = new FormData();
        formData.append('file', file);
        formData.append('target_language', currentLang);

        try {
            this.setPipelineProgress(1); // Step 2: Tomato Gate

            const response = await fetch('/api/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Prediction failed');
            }

            const data = await response.json();
            this.lastPredictionData = data;
            this.renderResponse(data, file);
        } catch (error) {
            console.error('Diagnosis Error:', error);
            alert(`⚠️ Error during diagnosis: ${error.message}`);
            if (this.emptyState) this.emptyState.classList.remove('hidden');
            this.resetPipeline();
        }
    }

    hideAllOutputs() {
        if (this.emptyState) this.emptyState.classList.add('hidden');
        if (this.nonTomatoCard) this.nonTomatoCard.classList.add('hidden');
        if (this.qualityFailCard) this.qualityFailCard.classList.add('hidden');
        if (this.diagnosisContent) this.diagnosisContent.classList.add('hidden');
    }

    renderResponse(data, file) {
        this.hideAllOutputs();

        // 1. Check Quality Pass
        if (data.is_quality_passed === false) {
            this.setPipelineProgress(0, false);
            if (this.qualityFailCard) this.qualityFailCard.classList.remove('hidden');
            if (this.qualityFailReason) this.qualityFailReason.textContent = data.message || 'Image quality low.';
            if (this.qualityFailSuggestion) this.qualityFailSuggestion.textContent = data.suggestion || 'Please capture a clear leaf photo.';
            if (this.severityBadge) {
                this.severityBadge.textContent = 'QUALITY FAILED';
                this.severityBadge.className = 'chip sev-High';
            }
            return;
        }

        // 2. Check Stage 1 Tomato Verification Gate
        // STRICT REQUIREMENT: Non-tomato images (and different crops) are rejected and NEVER show disease results!
        if (data.is_tomato === false) {
            this.setPipelineProgress(1, false); // Step 2 Failed
            if (this.nonTomatoCard) this.nonTomatoCard.classList.remove('hidden');
            if (this.nonTomatoConfidence) this.nonTomatoConfidence.textContent = `${data.tomato_confidence}%`;
            if (this.severityBadge) {
                this.severityBadge.textContent = window.translationManager ? window.translationManager.translateText('NOT A TOMATO CROP') : 'NOT A TOMATO CROP';
                this.severityBadge.className = 'chip sev-High';
            }

            // CRITICAL: NEVER show disease info for non-tomato
            this.currentDiseaseKey = null;
            return;
        }

        // 3. Stage 2 Tomato Disease Diagnosis (Valid Tomato Leaf Confirmed)
        this.setPipelineProgress(3, true); // Completed all 4 steps
        if (this.diagnosisContent) this.diagnosisContent.classList.remove('hidden');
        this.currentDiseaseKey = data.raw_class;

        // Banner details
        const diagnosisBanner = document.getElementById('diagnosisBanner');
        const healthScoreCircle = document.getElementById('healthScoreCircle');

        if (diagnosisBanner) {
            diagnosisBanner.className = data.is_healthy ? 'diagnosis-banner is-healthy-banner' : 'diagnosis-banner is-diseased-banner';
        }

        if (this.diagnosisName) {
            this.diagnosisName.textContent = data.is_healthy ? `🌱 ${data.disease}` : `⚠️ ${data.disease}`;
        }

        if (this.pathogenName) {
            this.pathogenName.textContent = data.is_healthy 
                ? `Status: Healthy Foliage — No Pathogens Detected (${data.scientific_name || 'Solanum lycopersicum'})` 
                : `Pathogen: ${data.pathogen_type || 'N/A'} (${data.scientific_name || ''})`;
        }

        if (this.bannerTomatoConf) this.bannerTomatoConf.textContent = `${data.tomato_confidence}% Tomato`;

        if (this.severityBadge) {
            this.severityBadge.textContent = data.is_healthy ? 'HEALTHY CROP' : `SEVERITY: ${data.severity.toUpperCase()}`;
            this.severityBadge.className = data.is_healthy ? 'chip sev-Healthy' : `chip sev-${data.severity}`;
        }

        if (this.healthScoreValue) this.healthScoreValue.textContent = data.health_score;
        if (healthScoreCircle) {
            if (data.is_healthy || data.health_score >= 80) {
                healthScoreCircle.style.color = '#10b981';
            } else if (data.health_score >= 50) {
                healthScoreCircle.style.color = '#f59e0b';
            } else {
                healthScoreCircle.style.color = '#ef4444';
            }
        }

        if (this.gaugeValue) this.gaugeValue.textContent = `${data.confidence}%`;
        if (this.confidenceFill) {
            this.confidenceFill.style.width = `${data.confidence}%`;
            this.confidenceFill.style.background = data.is_healthy 
                ? 'linear-gradient(90deg, #10b981, #34d399)' 
                : 'linear-gradient(90deg, #ef4444, #f59e0b)';
        }


        // Top 3 Probabilities
        if (this.probList) {
            this.probList.innerHTML = '';
            if (data.top_predictions) {
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
                    this.probList.appendChild(row);
                });
            }
        }

        if (this.aiSummaryText) {
            this.aiSummaryText.textContent = data.ai_summary || `Detected ${data.disease}. Review the action plan and treatment guidance below.`;
        }

        // Update Dedicated Farmer Guidance Hub Page
        const plan = data.action_plan || {};
        if (this.advisoryActionToday) this.advisoryActionToday.textContent = plan.today || 'Inspect crop thoroughly.';
        if (this.advisoryActionNext3) this.advisoryActionNext3.textContent = plan.next_3_days || 'Apply recommended spray.';
        if (this.advisoryActionWeek) this.advisoryActionWeek.textContent = plan.this_week || 'Improve canopy air movement.';

        this.populateList(this.advisorySymptomsList, data.symptoms);
        this.populateList(this.advisoryOrganicList, data.organic_treatment);
        this.populateList(this.advisoryChemicalList, data.chemical_treatment);
        this.populateList(this.advisoryPreventionList, data.prevention);

        // Save to Scan History
        this.saveScanHistory(data, file);
    }

    populateList(ulElement, items) {
        if (!ulElement) return;
        ulElement.innerHTML = '';
        if (Array.isArray(items)) {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                ulElement.appendChild(li);
            });
        }
    }

    saveScanHistory(data, file) {
        try {
            const history = JSON.parse(localStorage.getItem('tomatoguard_history') || '[]');
            const record = {
                id: Date.now(),
                date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
                disease: data.disease,
                confidence: data.confidence,
                health_score: data.health_score,
                severity: data.severity,
                image_name: file.name || 'Captured Leaf'
            };
            history.unshift(record);
            localStorage.setItem('tomatoguard_history', JSON.stringify(history.slice(0, 15)));
            this.loadHistory();
        } catch (e) {
            console.error('History save error:', e);
        }
    }

    loadHistory() {
        try {
            const history = JSON.parse(localStorage.getItem('tomatoguard_history') || '[]');
            if (!this.historyGrid) return;
            this.historyGrid.innerHTML = '';
            if (history.length === 0) {
                this.historyGrid.innerHTML = '<div class="no-history-msg">No previous scans recorded in this session.</div>';
                return;
            }

            history.forEach(item => {
                const card = document.createElement('div');
                card.className = 'history-card';
                card.innerHTML = `
                    <div class="logo-icon" style="font-size:24px;">🍃</div>
                    <div class="history-info">
                        <div class="hist-date">${item.date} &bull; Score: ${item.health_score}/100</div>
                        <div class="hist-name">${item.disease}</div>
                        <div class="hist-conf">${item.confidence}% confidence</div>
                    </div>
                `;
                this.historyGrid.appendChild(card);
            });
        } catch (e) {
            console.error('History load error:', e);
        }
    }

    clearHistory() {
        localStorage.removeItem('tomatoguard_history');
        this.loadHistory();
    }
}

window.predictionController = new PredictionController();
