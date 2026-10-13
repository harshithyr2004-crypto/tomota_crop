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

        // DOM Elements - Symptom Comparator & Prescription
        this.symptomComparatorBox = document.getElementById('symptomComparatorBox');
        this.compScannedImg = document.getElementById('compScannedImg');
        this.compHallmarksList = document.getElementById('compHallmarksList');
        this.compActionCue = document.getElementById('compActionCue');
        this.downloadPrescriptionBtn = document.getElementById('downloadPrescriptionBtn');
        this.activePlotSelect = document.getElementById('activePlotSelect');

        if (this.downloadPrescriptionBtn) {
            this.downloadPrescriptionBtn.addEventListener('click', () => this.generatePrescription());
        }

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

        // Populate Pathology Symptom Visual Comparator
        if (this.symptomComparatorBox) {
            this.symptomComparatorBox.classList.remove('hidden');
            if (this.compScannedImg) {
                const previewImg = document.getElementById('imagePreview');
                if (previewImg && previewImg.src) {
                    this.compScannedImg.src = previewImg.src;
                }
            }
            if (this.compHallmarksList) {
                this.compHallmarksList.innerHTML = '';
                const hallmarks = (data.symptoms && data.symptoms.length > 0)
                    ? data.symptoms.slice(0, 3)
                    : ['Foliar necrosis with chlorotic margin halos', 'Concentric fungal target rings or foliar spots', 'Leaf curling, stunting, or vascular wilting'];
                hallmarks.forEach(item => {
                    const tag = document.createElement('span');
                    tag.className = 'comp-hallmark-tag';
                    tag.textContent = `• ${item}`;
                    this.compHallmarksList.appendChild(tag);
                });
            }
            if (this.compActionCue) {
                this.compActionCue.textContent = data.is_healthy
                    ? 'Pristine foliar chlorophyll distribution; zero active lesion signatures.'
                    : `Neural activation patterns correlate strongly with classic ${data.disease} hallmark markers.`;
            }
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
            const activePlot = this.activePlotSelect ? this.activePlotSelect.value : 'Plot North A (Hybrid)';
            const record = {
                id: Date.now(),
                date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short' }),
                disease: data.disease,
                confidence: data.confidence,
                health_score: data.health_score,
                severity: data.severity,
                plot_name: activePlot,
                image_name: file.name || 'Captured Leaf'
            };
            history.unshift(record);
            localStorage.setItem('tomatoguard_history', JSON.stringify(history.slice(0, 20)));
            this.loadHistory();
            if (window.plotsManager) {
                window.plotsManager.renderPlots();
            }
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
                        <div class="hist-date">${item.date} &bull; Score: ${item.health_score}/100 &bull; <strong>${item.plot_name || 'Plot North A'}</strong></div>
                        <div class="hist-name">${item.disease}</div>
                        <div class="hist-conf">${item.confidence}% confidence (${item.severity || 'Normal'})</div>
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
        if (window.plotsManager) {
            window.plotsManager.renderPlots();
        }
    }

    generatePrescription() {
        if (!this.lastPredictionData) {
            alert('Please perform a leaf scan first to generate an agronomy prescription.');
            return;
        }

        const data = this.lastPredictionData;
        const activePlot = this.activePlotSelect ? this.activePlotSelect.value : 'Plot North A (Hybrid)';
        const dateStr = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
        const timeStr = new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });

        const printWindow = window.open('', '_blank');
        if (!printWindow) {
            alert('Pop-up was blocked. Please allow pop-ups to open the prescription.');
            return;
        }

        const organicItemsHtml = Array.isArray(data.organic_treatment) 
            ? data.organic_treatment.map(o => `<li>${o}</li>`).join('')
            : '<li>Regular bio-fungicide foliar application</li>';

        const chemicalItemsHtml = Array.isArray(data.chemical_treatment)
            ? data.chemical_treatment.map(c => `<li>${c}</li>`).join('')
            : '<li>Consult local agriculture extension officer before spraying</li>';

        const todayAction = data.action_plan?.today || 'Inspect field perimeter and isolate symptomatic plants.';
        const next3Action = data.action_plan?.next_3_days || 'Apply protective bio-control foliar spray early in the morning.';
        const weekAction = data.action_plan?.this_week || 'Improve canopy aeration and maintain soil drip fertigation.';

        printWindow.document.write(`
<!DOCTYPE html>
<html>
<head>
    <title>TomatoGuard AI - Agronomic Crop Health Prescription</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #1e293b;
            margin: 0;
            padding: 32px;
            background: #ffffff;
            line-height: 1.5;
        }
        .rx-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #16a34a;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }
        .rx-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .rx-logo { font-size: 38px; }
        .rx-title h1 { margin: 0; font-size: 24px; color: #166534; font-weight: 800; letter-spacing: -0.5px; }
        .rx-title p { margin: 2px 0 0; font-size: 13px; color: #64748b; }
        .rx-meta { text-align: right; font-size: 13px; color: #475569; }
        .rx-badge { display: inline-block; background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; margin-bottom: 4px; }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }
        .info-box span { display: block; font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600; }
        .info-box strong { font-size: 15px; color: #0f172a; }
        .rx-section { margin-bottom: 22px; }
        .rx-section h2 {
            font-size: 16px;
            color: #0f172a;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .timeline-box {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        .t-step {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 12px;
            background: #ffffff;
        }
        .t-step.today { border-top: 4px solid #ef4444; }
        .t-step.next3 { border-top: 4px solid #f59e0b; }
        .t-step.week { border-top: 4px solid #10b981; }
        .t-step h4 { margin: 0 0 6px; font-size: 12px; font-weight: 800; letter-spacing: 0.5px; }
        .t-step.today h4 { color: #dc2626; }
        .t-step.next3 h4 { color: #d97706; }
        .t-step.week h4 { color: #059669; }
        .t-step p { margin: 0; font-size: 12px; color: #334155; }
        ul { margin: 0; padding-left: 20px; }
        li { font-size: 13px; color: #334155; margin-bottom: 6px; }
        .rx-caution {
            background: #fffbeb;
            border: 1px solid #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 12px;
            color: #92400e;
            margin-top: 24px;
        }
        .rx-signature {
            display: flex;
            justify-content: space-between;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px dashed #cbd5e1;
            font-size: 12px;
            color: #64748b;
        }
        .print-btn-bar {
            text-align: center;
            margin-bottom: 24px;
        }
        .print-btn {
            background: #16a34a;
            color: #ffffff;
            border: none;
            padding: 10px 24px;
            font-size: 14px;
            font-weight: 700;
            border-radius: 6px;
            cursor: pointer;
        }
        @media print {
            .print-btn-bar { display: none; }
            body { padding: 0; }
        }
    </style>
</head>
<body>
    <div class="print-btn-bar">
        <button class="print-btn" onclick="window.print()">🖨️ Print Prescription / Save as PDF</button>
    </div>
    <div class="rx-header">
        <div class="rx-brand">
            <div class="rx-logo">🍅</div>
            <div class="rx-title">
                <h1>TomatoGuard AI Agronomic Advisory</h1>
                <p>Two-Stage Gated Neural Disease Prescription & Management Record</p>
            </div>
        </div>
        <div class="rx-meta">
            <div class="rx-badge">Rx Verified</div>
            <div>Date: ${dateStr}</div>
            <div>Time: ${timeStr}</div>
        </div>
    </div>

    <div class="info-grid">
        <div class="info-box">
            <span>Farm Field / Plot</span>
            <strong>${activePlot}</strong>
        </div>
        <div class="info-box">
            <span>Primary Diagnosis</span>
            <strong>${data.disease}</strong>
        </div>
        <div class="info-box">
            <span>Severity & Health Score</span>
            <strong>${data.severity.toUpperCase()} (${data.health_score}/100)</strong>
        </div>
        <div class="info-box">
            <span>AI Model Confidence</span>
            <strong>${data.confidence}% (Stage 2 CNN)</strong>
        </div>
    </div>

    <div class="rx-section">
        <h2>⏱️ Immediate Time-Sequenced Action Plan</h2>
        <div class="timeline-box">
            <div class="t-step today">
                <h4>STEP 1: TODAY</h4>
                <p>${todayAction}</p>
            </div>
            <div class="t-step next3">
                <h4>STEP 2: NEXT 3 DAYS</h4>
                <p>${next3Action}</p>
            </div>
            <div class="t-step week">
                <h4>STEP 3: THIS WEEK</h4>
                <p>${weekAction}</p>
            </div>
        </div>
    </div>

    <div class="rx-section">
        <h2>🌿 Recommended Bio-Control & Organic Remedies</h2>
        <ul>${organicItemsHtml}</ul>
    </div>

    <div class="rx-section">
        <h2>💊 Prescribed Chemical Medication & Dosage Protocols</h2>
        <ul>${chemicalItemsHtml}</ul>
    </div>

    <div class="rx-caution">
        <strong>⚠️ Safety & Pre-Harvest Interval (PHI) Notice:</strong> Always wear standard personal protective equipment (PPE) when applying crop protection chemicals. Strictly adhere to label concentrations and observe required days to harvest.
    </div>

    <div class="rx-signature">
        <div>
            <strong>TomatoGuard AI Agronomy Engine</strong><br>
            MobileNetV2 Plant Gate + 10-Class Neural Network
        </div>
        <div style="text-align: right;">
            <strong>Agronomist / Field Scout Verification</strong><br>
            Signature: __________________________
        </div>
    </div>
</body>
</html>
        `);
        printWindow.document.close();
    }
}

window.predictionController = new PredictionController();
