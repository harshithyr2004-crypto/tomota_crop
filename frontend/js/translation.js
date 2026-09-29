// -*- coding: utf-8 -*-
/**
 * Comprehensive Multi-Language Translation Manager (10 Indian Languages)
 * Translates EVERY UI string across both Login Screen and Multi-Page Working Dashboard.
 */

const UI_DICTIONARIES = {
    "kn": { // Kannada (ಕನ್ನಡ)
        "TomatoGuard AI": "ಟೊಮೆಟೊಗಾರ್ಡ್ ಎಐ",
        "Smart Crop Health Assistant": "ಸ್ಮಾರ್ಟ್ ಬೆಳೆ ಆರೋಗ್ಯ ಸಹಾಯಕ",
        "Welcome to TomatoGuard AI": "ಟೊಮೆಟೊಗಾರ್ಡ್ ಎಐ ಗೆ ಸುಸ್ವಾಗತ",
        "Sign in or use demo access to start two-stage crop health diagnosis.": "ಎರಡು-ಹಂತದ ಬೆಳೆ ರೋಗನಿರ್ಣಯವನ್ನು ಪ್ರಾರಂಭಿಸಲು ಲಾಗಿನ್ ಮಾಡಿ ಅಥವಾ ಡೆಮೊ ಪ್ರವೇಶ ಬಳಸಿ.",
        "Sign In": "ಲಾಗಿನ್ ಮಾಡಿ",
        "Register Farm": "ಹೊಸ ಖಾತೆ ತೆರೆಯಿರಿ",
        "Farmer / Username": "ರೈತ / ಬಳಕೆದಾರರ ಹೆಸರು",
        "Password": "ಪಾಸ್‌ವರ್ಡ್",
        "Sign In to Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಪ್ರವೇಶಿಸಿ",
        "Full Name": "ಪೂರ್ಣ ಹೆಸರು",
        "Farm Location (District / State)": "ಜಮೀನಿನ ಸ್ಥಳ (ಜಿಲ್ಲೆ / ರಾಜ್ಯ)",
        "Create Account": "ಖಾತೆ ರಚಿಸಿ",
        "OR": "ಅಥವಾ",
        "Instant Demo Access (One-Click)": "⚡ ತ್ವರಿತ ಡೆಮೊ ಪ್ರವೇಶ (ಒಂದು ಕ್ಲಿಕ್)",
        "Scanner & AI": "ಸ್ಕ್ಯಾನರ್ ಮತ್ತು ಎಐ",
        "Farmer Guidance": "ರೈತರ ಮಾರ್ಗದರ್ಶನ",
        "Ask AI Advisor": "ಎಐ ಸಲಹೆಗಾರನನ್ನು ಕೇಳಿ",
        "Scan Records": "ಸ್ಕ್ಯಾನ್ ದಾಖಲೆಗಳು",
        "Disease Library": "ರೋಗಗಳ ಮಾಹಿತಿ ಗ್ರಂಥಾಲಯ",
        "Logout": "ಲಾಗ್ ಔಟ್",
        "API Docs": "ಎಪಿಐ ವಿವರ",
        "Protect Your Tomato Crop With AI": "ಎಐ ತಂತ್ರಜ್ಞಾನದಿಂದ ನಿಮ್ಮ ಟೊಮೆಟೊ ಬೆಳೆಯನ್ನು ರಕ್ಷಿಸಿ",
        "Capture or upload a leaf image. Stage 1 MobileNetV2 verifies tomato authenticity; Stage 2 deep CNN identifies foliar diseases.": "ಎಲೆಯ ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿಯಿರಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. ಹಂತ 1 ಟೊಮೆಟೊ ಹೌದೆಂದು ಪರಿಶೀಲಿಸುತ್ತದೆ; ಹಂತ 2 ರೋಗವನ್ನು ಪತ್ತೆ ಮಾಡುತ್ತದೆ.",
        "STEP 1": "ಹಂತ 1",
        "Image Check": "ಚಿತ್ರ ಪರಿಶೀಲನೆ",
        "STEP 2": "ಹಂತ 2",
        "Tomato Gate": "ಟೊಮೆಟೊ ದೃಢೀಕರಣ",
        "STEP 3": "ಹಂತ 3",
        "Disease AI": "ರೋಗ ಪತ್ತೆ",
        "STEP 4": "ಹಂತ 4",
        "Leaf Image Scanner": "ಎಲೆ ಚಿತ್ರ ಸ್ಕ್ಯಾನರ್",
        "Upload Image": "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್",
        "Scan With Camera": "ಕ್ಯಾಮರಾ ಸ್ಕ್ಯಾನ್",
        "Drag & drop tomato leaf image here": "ಟೊಮೆಟೊ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಇಲ್ಲಿ ಎಳೆಯಿರಿ",
        "Browse Files": "ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ",
        "Lens": "ಲೆನ್ಸ್ ಬದಲಿಸಿ",
        "Snap Photo": "ಫೋಟೋ ತೆಗೆಯಿರಿ",
        "Close": "ಮುಚ್ಚಿ",
        "Run Two-Stage AI Diagnosis": "ಎಐ ರೋಗನಿರ್ಣಯವನ್ನು ಪ್ರಾರಂಭಿಸಿ",
        "One-Click Test Leaves (Tomato & Non-Tomato):": "ಪರೀಕ್ಷಾ ಚಿತ್ರಗಳು (ಟೊಮೆಟೊ ಮತ್ತು ಇತರ ವಸ್ತುಗಳು):",
        "Diagnostic Result": "ರೋಗನಿರ್ಣಯದ ಫಲಿತಾಂಶ",
        "Awaiting Scan": "ಸ್ಕ್ಯಾನ್ ಕಾಯುತ್ತಿದೆ",
        "No Leaf Analyzed Yet": "ಇನ್ನೂ ಯಾವುದೇ ಎಲೆಯನ್ನು ಪರಿಶೀಲಿಸಿಲ್ಲ",
        "Select a leaf sample on the left or upload an image to view two-stage verification and disease metrics.": "ಎಡಭಾಗದಲ್ಲಿರುವ ಮಾದರಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "NOT A TOMATO CROP": "⚠️ ಇದು ಟೊಮೆಟೊ ಬೆಳೆ ಅಲ್ಲ",
        "This image does not appear to belong to the tomato crop.": "ಈ ಚಿತ್ರವು ಟೊಮೆಟೊ ಬೆಳೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಕಾಣಿಸುತ್ತಿಲ್ಲ.",
        "Please upload or capture a clear image of a tomato leaf.": "ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ ಟೊಮೆಟೊ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ಸೆರೆಹಿಡಿಯಿರಿ.",
        "Stage 1 Tomato Confidence:": "ಹಂತ 1 ಟೊಮೆಟೊ ವಿಶ್ವಾಸಾರ್ಹತೆ:",
        "Required Gate Threshold: ≥ 75.0%": "ಅಗತ್ಯವಿರುವ ಕನಿಷ್ಠ ಮಿತಿ: ≥ 75.0%",
        "Supported Input:": "ಬೆಂಬಲಿತ ಚಿತ್ರಗಳು:",
        "Tomato Crop Verified": "ಟೊಮೆಟೊ ಬೆಳೆ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
        "Crop Health Score": "ಬೆಳೆ ಆರೋಗ್ಯ ಸ್ಕೋರ್",
        "AI-based indication": "ಎಐ ಆಧಾರಿತ ಸೂಚನೆ",
        "Disease Confidence": "ರೋಗದ ವಿಶ್ವಾಸಾರ್ಹತೆ",
        "Top Probability Predictions": "ಹೆಚ್ಚು ಸಂಭವನೀಯ ರೋಗಗಳು",
        "View Farmer Guidance ➔": "ರೈತರ ಪೂರ್ಣ ಮಾರ್ಗದರ್ಶನ ನೋಡಿ ➔",
        "Farmer Agronomy & Treatment Hub": "ರೈತರ ಕೃಷಿ ಮತ್ತು ಚಿಕಿತ್ಸಾ ಮಾಹಿತಿ ಕೇಂದ್ರ",
        "Action Protocols": "ಕಾರ್ಯ ಯೋಜನೆ",
        "Farmer Action Plan": "ರೈತರ ಕಾರ್ಯ ಯೋಜನೆ",
        "Time-Sequenced": "ಸಮಯ ಆಧಾರಿತ",
        "TODAY": "ಇಂದು",
        "NEXT 3 DAYS": "ಮುಂದಿನ 3 ದಿನಗಳು",
        "THIS WEEK": "ಈ ವಾರ",
        "Symptoms & Identification": "ರೋಗಲಕ್ಷಣಗಳು ಮತ್ತು ಗುರುತಿಸುವಿಕೆ",
        "Organic & Bio-Control Remedies": "ಸಾವಯವ ಮತ್ತು ಜೈವಿಕ ನಿಯಂತ್ರಣ ಕ್ರಮಗಳು",
        "Chemical Medications & Dosage Guidelines": "ರಾಸಾಯನಿಕ ಔಷಧಗಳು ಮತ್ತು ಪ್ರಮಾಣ",
        "Long-Term Agronomy Prevention": "ದೀರ್ಘಾವಧಿ ಮುನ್ನೆಚ್ಚರಿಕೆ ಕ್ರಮಗಳು",
        "Ask TomatoGuard AI Agronomy Assistant": "ಟೊಮೆಟೊಗಾರ್ಡ್ ಎಐ ಕೃಷಿ ಸಹಾಯಕರನ್ನು ಕೇಳಿ",
        "Quick Questions:": "ಸಾಮಾನ್ಯ ಪ್ರಶ್ನೆಗಳು:",
        "How do I spray neem oil?": "ಬೇವಿನ ಎಣ್ಣೆಯನ್ನು ಹೇಗೆ ಸಿಂಪಡಿಸಬೇಕು?",
        "What causes yellow leaves?": "ಎಲೆಗಳು ಹಳದಿಯಾಗಲು ಕಾರಣವೇನು?",
        "How to prevent Late Blight?": "ಅಂಗಮಾರಿ ರೋಗವನ್ನು ತಡೆಯುವುದು ಹೇಗೆ?",
        "How to control whiteflies?": "ಬಿಳಿ ನೊಣಗಳನ್ನು ಹೇಗೆ ನಿಯಂತ್ರಿಸಬೇಕು?",
        "Send Query": "ಕೇಳಿ",
        "Tomato Field Scan Records": "ಟೊಮೆಟೊ ತೋಟದ ಸ್ಕ್ಯಾನ್ ದಾಖಲೆಗಳು",
        "Clear All Records": "ಎಲ್ಲಾ ದಾಖಲೆಗಳನ್ನು ಅಳಿಸಿ",
        "Tomato Crop Pathology Encyclopedia (10 Categories)": "ಟೊಮೆಟೊ ಬೆಳೆ ರೋಗಗಳ ಮಾಹಿತಿ ಕೋಶ (10 ವಿಭಾಗಗಳು)"
    },
    "hi": { // Hindi (हिन्दी)
        "TomatoGuard AI": "टोमेटोगार्ड एआई",
        "Smart Crop Health Assistant": "स्मार्ट फसल स्वास्थ्य सहायक",
        "Welcome to TomatoGuard AI": "टोमेटोगार्ड एआई में आपका स्वागत है",
        "Sign in or use demo access to start two-stage crop health diagnosis.": "दो-चरणीय फसल स्वास्थ्य निदान शुरू करने के लिए साइन इन करें या डेमो का उपयोग करें।",
        "Sign In": "साइन इन करें",
        "Register Farm": "नया खाता बनाएं",
        "Farmer / Username": "किसान / उपयोगकर्ता नाम",
        "Password": "पासवर्ड",
        "Sign In to Dashboard": "डैशबोर्ड में प्रवेश करें",
        "Full Name": "पूरा नाम",
        "Farm Location (District / State)": "खेत का स्थान (जिला / राज्य)",
        "Create Account": "खाता बनाएं",
        "OR": "या",
        "Instant Demo Access (One-Click)": "⚡ तत्काल डेमो प्रवेश (एक क्लिक)",
        "Scanner & AI": "स्कैनर और एआई",
        "Farmer Guidance": "किसान मार्गदर्शन",
        "Ask AI Advisor": "एआई सलाहकार से पूछें",
        "Scan Records": "स्कैन रिकॉर्ड",
        "Disease Library": "रोग पुस्तकालय",
        "Logout": "लॉग आउट",
        "API Docs": "एपीआई डॉक्स",
        "Protect Your Tomato Crop With AI": "एआई के साथ अपनी टमाटर की फसल की रक्षा करें",
        "Capture or upload a leaf image. Stage 1 MobileNetV2 verifies tomato authenticity; Stage 2 deep CNN identifies foliar diseases.": "पत्ती की छवि कैप्चर या अपलोड करें। चरण 1 टमाटर की पुष्टि करता है; चरण 2 रोग की पहचान करता है।",
        "STEP 1": "चरण 1",
        "Image Check": "छवि जांच",
        "STEP 2": "चरण 2",
        "Tomato Gate": "टमाटर सत्यापन",
        "STEP 3": "चरण 3",
        "Disease AI": "रोग एआई",
        "STEP 4": "चरण 4",
        "Leaf Image Scanner": "पत्ती छवि स्कैनर",
        "Upload Image": "छवि अपलोड करें",
        "Scan With Camera": "कैमरे से स्कैन करें",
        "Drag & drop tomato leaf image here": "टमाटर की पत्ती की छवि यहाँ खींचें",
        "Browse Files": "फ़ाइल चुनें",
        "Lens": "लेंस बदलें",
        "Snap Photo": "फोटो लें",
        "Close": "बंद करें",
        "Run Two-Stage AI Diagnosis": "दो-चरणीय एआई निदान शुरू करें",
        "One-Click Test Leaves (Tomato & Non-Tomato):": "परीक्षण नमूने (टमाटर और अन्य वस्तुएं):",
        "Diagnostic Result": "निदान परिणाम",
        "Awaiting Scan": "स्कैन की प्रतीक्षा है",
        "No Leaf Analyzed Yet": "अभी तक कोई पत्ती जांची नहीं गई",
        "Select a leaf sample on the left or upload an image to view two-stage verification and disease metrics.": "बाईं ओर एक पत्ती का नमूना चुनें या छवि अपलोड करें।",
        "NOT A TOMATO CROP": "⚠️ यह टमाटर की फसल नहीं है",
        "This image does not appear to belong to the tomato crop.": "यह छवि टमाटर की फसल से संबंधित प्रतीत नहीं होती है।",
        "Please upload or capture a clear image of a tomato leaf.": "कृपया टमाटर की पत्ती की एक स्पष्ट छवि अपलोड या कैप्चर करें।",
        "Stage 1 Tomato Confidence:": "चरण 1 टमाटर विश्वास:",
        "Required Gate Threshold: ≥ 75.0%": "आवश्यक न्यूनतम सीमा: ≥ 75.0%",
        "Supported Input:": "समर्थित छवियां:",
        "Tomato Crop Verified": "टमाटर की फसल सत्यापित",
        "Crop Health Score": "फसल स्वास्थ्य स्कोर",
        "AI-based indication": "एआई-आधारित संकेत",
        "Disease Confidence": "रोग का विश्वास स्तर",
        "Top Probability Predictions": "शीर्ष संभावित रोग",
        "View Farmer Guidance ➔": "किसान मार्गदर्शन देखें ➔",
        "Farmer Agronomy & Treatment Hub": "किसान कृषि विज्ञान और उपचार केंद्र",
        "Action Protocols": "कार्य योजना",
        "Farmer Action Plan": "किसान कार्य योजना",
        "Time-Sequenced": "समयबद्ध",
        "TODAY": "आज",
        "NEXT 3 DAYS": "अगले 3 दिन",
        "THIS WEEK": "इस सप्ताह",
        "Symptoms & Identification": "लक्षण और पहचान",
        "Organic & Bio-Control Remedies": "जैविक और प्राकृतिक उपचार",
        "Chemical Medications & Dosage Guidelines": "रासायनिक दवाएं और खुराक निर्देश",
        "Long-Term Agronomy Prevention": "दीर्घकालिक रोकथाम के उपाय",
        "Ask TomatoGuard AI Agronomy Assistant": "टोमेटोगार्ड एआई कृषि सहायक से पूछें",
        "Quick Questions:": "अक्सर पूछे जाने वाले प्रश्न:",
        "How do I spray neem oil?": "नीम का तेल कैसे छिड़कें?",
        "What causes yellow leaves?": "पत्तियां पीली पड़ने का क्या कारण है?",
        "How to prevent Late Blight?": "झुलसा रोग से बचाव कैसे करें?",
        "How to control whiteflies?": "सफेद मक्खी पर नियंत्रण कैसे पाएं?",
        "Send Query": "पूछें",
        "Tomato Field Scan Records": "टमाटर खेत स्कैन रिकॉर्ड",
        "Clear All Records": "सभी रिकॉर्ड हटाएं",
        "Tomato Crop Pathology Encyclopedia (10 Categories)": "टमाटर फसल रोग विश्वकोश (10 श्रेणियां)"
    },
    "te": { // Telugu (తెలుగు)
        "TomatoGuard AI": "టొమాటోగార్డ్ AI",
        "Smart Crop Health Assistant": "స్మార్ట్ పంట ఆరోగ్య సహాయకుడు",
        "Welcome to TomatoGuard AI": "టొమాటోగార్డ్ AI కి స్వాగతం",
        "Sign In": "లాగిన్ చేయండి",
        "Register Farm": "నమోదు చేసుకోండి",
        "Instant Demo Access (One-Click)": "⚡ తక్షణ డెమో ప్రవేశం (ఒక క్లిక్)",
        "Scanner & AI": "స్కాన్ & AI",
        "Farmer Guidance": "రైతు మార్గదర్శకత్వం",
        "Ask AI Advisor": "AI సలహాదారుని అడగండి",
        "Scan Records": "స్కాన్ రికార్డులు",
        "Disease Library": "వ్యాధి సమాచారం",
        "Logout": "లాగ్ అవుట్",
        "Protect Your Tomato Crop With AI": "AI తో మీ టొమాటో పంటను రక్షించండి",
        "Upload Image": "చిత్రం అప్‌లోడ్ చేయండి",
        "Scan With Camera": "కెమెరాతో స్కాన్ చేయండి",
        "Run Two-Stage AI Diagnosis": "AI రోగ నిర్ధారణ ప్రారంభించండి",
        "NOT A TOMATO CROP": "⚠️ ఇది టొమాటో పంట కాదు",
        "This image does not appear to belong to the tomato crop.": "ఈ చిత్రం టొమాటో పంటకు చెందినదిగా కనిపించడం లేదు.",
        "Please upload or capture a clear image of a tomato leaf.": "దయచేసి టొమాటో ఆకు యొక్క స్పష్టమైన చిత్రాన్ని అప్‌లోడ్ చేయండి.",
        "Tomato Crop Verified": "టొమాటో పంట ధృవీకరించబడింది",
        "Crop Health Score": "పంట ఆరోగ్య స్కోరు",
        "Farmer Action Plan": "రైతు కార్యాచరణ ప్రణాళిక",
        "Symptoms & Identification": "లక్షణాలు మరియు గుర్తింపు",
        "Organic & Bio-Control Remedies": "సేంద్రీయ నివారణలు",
        "Chemical Medications & Dosage Guidelines": "రసాయన మందులు & మోతాదు",
        "Long-Term Agronomy Prevention": "దీర్ఘకాలిక నివారణ చర్యలు",
        "Ask TomatoGuard AI Agronomy Assistant": "టొమాటోగార్డ్ AI సహాయకుడిని అడగండి"
    },
    "ta": { // Tamil (தமிழ்)
        "TomatoGuard AI": "டொமேட்டோகார்ட் AI",
        "Smart Crop Health Assistant": "ஸ்மார்ட் பயிர் சுகாதார உதவியாளர்",
        "Welcome to TomatoGuard AI": "டொமேட்டோகார்ட் AI-க்கு நல்வரவு",
        "Sign In": "உள்நுழையவும்",
        "Register Farm": "பதிவு செய்யவும்",
        "Instant Demo Access (One-Click)": "⚡ உடனடி டெமோ அணுகல் (ஒரு கிளிக்)",
        "Scanner & AI": "ஸ்கேனர் & AI",
        "Farmer Guidance": "விவசாயி வழிகாட்டுதல்",
        "Ask AI Advisor": "AI ஆலோசகரிடம் கேளுங்கள்",
        "Scan Records": "ஸ்கேன் பதிவுகள்",
        "Disease Library": "நோய் நூலகம்",
        "Logout": "வெளியேறு",
        "Protect Your Tomato Crop With AI": "AI மூலம் உங்கள் தக்காளி பயிரைப் பாதுகாக்கவும்",
        "Upload Image": "படம் பதிவேற்றுக",
        "Scan With Camera": "கேமராவில் ஸ்கேன் செய்க",
        "Run Two-Stage AI Diagnosis": "AI நோய் கண்டறிதலைத் தொடங்கு",
        "NOT A TOMATO CROP": "⚠️ இது தக்காளி பயிர் அல்ல",
        "This image does not appear to belong to the tomato crop.": "இந்த படம் தக்காளி பயிரைச் சேர்ந்ததாகத் தெரியவில்லை.",
        "Please upload or capture a clear image of a tomato leaf.": "தயவுசெய்து தக்காளி இலையின் தெளிவான படத்தை பதிவேற்றவும்.",
        "Tomato Crop Verified": "தக்காளி பயிர் சரிபார்க்கப்பட்டது",
        "Crop Health Score": "பயிர் சுகாதார மதிப்பெண்",
        "Farmer Action Plan": "விவசாயி செயல் திட்டம்",
        "Symptoms & Identification": "அறிகுறிகள் & அடையாளம்",
        "Organic & Bio-Control Remedies": "இயற்கை & உயிரியல் சிகிச்சை",
        "Chemical Medications & Dosage Guidelines": "இரசாயன மருந்துகள் மற்றும் அளவு",
        "Long-Term Agronomy Prevention": "நீண்ட கால தடுப்பு முறைகள்",
        "Ask TomatoGuard AI Agronomy Assistant": "டொமேட்டோகார்ட் AI-யிடம் கேளுங்கள்"
    },
    "ml": { // Malayalam (മലയാളം)
        "TomatoGuard AI": "ടൊമാറ്റോഗാർഡ് AI",
        "Smart Crop Health Assistant": "സ്മാർട്ട് വിള ആരോഗ്യ സഹായി",
        "Welcome to TomatoGuard AI": "ടൊമാറ്റോഗാർഡ് AI-ലേക്ക് സ്വാഗതം",
        "Sign In": "ലോഗിൻ ചെയ്യുക",
        "Instant Demo Access (One-Click)": "⚡ ഡെമോ പ്രവേശനം (ഒരു ക്ലിക്ക്)",
        "Scanner & AI": "സ്കാനർ & AI",
        "Farmer Guidance": "കർഷക മാർഗ്ഗനിർദ്ദേശം",
        "Ask AI Advisor": "AI ഉപദേശകനോട് ചോദിക്കുക",
        "Scan Records": "സ്കാൻ റെക്കോർഡുകൾ",
        "Disease Library": "രോഗ വിവരങ്ങൾ",
        "Logout": "ലോഗ് ഔട്ട്",
        "Protect Your Tomato Crop With AI": "AI ഉപയോഗിച്ച് നിങ്ങളുടെ തക്കാളി കൃഷി സംരക്ഷിക്കുക",
        "Upload Image": "ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "Scan With Camera": "ക്യാമറ സ്കാൻ",
        "Run Two-Stage AI Diagnosis": "രോഗനിർണയം ആരംഭിക്കുക",
        "NOT A TOMATO CROP": "⚠️ ഇത് തക്കാളി കൃഷിയല്ല",
        "This image does not appear to belong to the tomato crop.": "ഈ ചിത്രം തക്കാളി കൃഷിയുമായി ബന്ധപ്പെട്ടതല്ല.",
        "Please upload or capture a clear image of a tomato leaf.": "ദയവായി തക്കാളി ഇലയുടെ വ്യക്തമായ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക.",
        "Tomato Crop Verified": "തക്കാളി കൃഷി സ്ഥിരീകരിച്ചു",
        "Crop Health Score": "വിള ആരോഗ്യ സ്കോർ",
        "Farmer Action Plan": "കർഷക കർമ്മ പദ്ധതി"
    },
    "mr": { // Marathi (मराठी)
        "TomatoGuard AI": "टोमॅटोगार्ड एआय",
        "Smart Crop Health Assistant": "स्मार्ट पीक आरोग्य सहाय्यक",
        "Welcome to TomatoGuard AI": "टोमॅटोगार्ड एआय मध्ये आपले स्वागत आहे",
        "Sign In": "साइन इन करा",
        "Instant Demo Access (One-Click)": "⚡ झटपट डेमो प्रवेश (एक क्लिक)",
        "Scanner & AI": "स्कॅनर आणि एआय",
        "Farmer Guidance": "शेतकरी मार्गदर्शन",
        "Ask AI Advisor": "एआय सल्लागाराला विचारा",
        "Scan Records": "स्कॅन नोंदी",
        "Disease Library": "रोग माहिती",
        "Logout": "लॉग आउट",
        "Protect Your Tomato Crop With AI": "एआय च्या मदतीने टोमॅटो पिकाचे रक्षण करा",
        "Upload Image": "फोटो अपलोड करा",
        "Scan With Camera": "कॅमेऱ्याने स्कॅन करा",
        "Run Two-Stage AI Diagnosis": "एआय रोग निदान सुरू करा",
        "NOT A TOMATO CROP": "⚠️ हे टोमॅटोचे पीक नाही",
        "This image does not appear to belong to the tomato crop.": "हा फोटो टोमॅटो पिकाचा वाटत नाही.",
        "Please upload or capture a clear image of a tomato leaf.": "कृपया टोमॅटोच्या पानाचा स्पष्ट फोटो अपलोड करा.",
        "Tomato Crop Verified": "टोमॅटो पीक सत्यापित",
        "Crop Health Score": "पीक आरोग्य स्कोअर",
        "Farmer Action Plan": "शेतकरी कृती योजना"
    },
    "bn": { // Bengali (বাংলা)
        "TomatoGuard AI": "টমেটোগার্ড এআই",
        "Smart Crop Health Assistant": "স্মার্ট ফসল স্বাস্থ্য সহকারী",
        "Welcome to TomatoGuard AI": "টমেটোগার্ড এআই-তে স্বাগতম",
        "Sign In": "সাইন ইন করুন",
        "Instant Demo Access (One-Click)": "⚡ তাত্ক্ষণিক ডেমো অ্যাক্সেস",
        "Scanner & AI": "স্ক্যানার এবং এআই",
        "Farmer Guidance": "কৃষক নির্দেশিকা",
        "Ask AI Advisor": "এআই উপদেষ্টাকে জিজ্ঞাসা করুন",
        "Scan Records": "স্ক্যান রেকর্ড",
        "Disease Library": "রোগের তথ্যশালা",
        "Logout": "লগ আউট",
        "Protect Your Tomato Crop With AI": "এআই দিয়ে আপনার টমেটো ফসল রক্ষা করুন",
        "Upload Image": "ছবি আপলোড করুন",
        "Scan With Camera": "ক্যামেরা দিয়ে স্ক্যান করুন",
        "Run Two-Stage AI Diagnosis": "এআই রোগ নির্ণয় শুরু করুন",
        "NOT A TOMATO CROP": "⚠️ এটি টমেটো ফসল নয়",
        "This image does not appear to belong to the tomato crop.": "এই ছবিটি টমেটো ফসলের সাথে সম্পর্কিত নয়।",
        "Please upload or capture a clear image of a tomato leaf.": "দয়া করে টমেটো পাতার একটি স্পষ্ট ছবি আপলোড করুন।",
        "Tomato Crop Verified": "টমেটো ফসল যাচাই করা হয়েছে",
        "Crop Health Score": "ফসল স্বাস্থ্য স্কোর",
        "Farmer Action Plan": "কৃষক কর্ম পরিকল্পনা"
    },
    "gu": { // Gujarati (ગુજરાતી)
        "TomatoGuard AI": "ટોમેટોગાર્ડ AI",
        "Smart Crop Health Assistant": "સ્માર્ટ પાક આરોગ્ય સહાયક",
        "Welcome to TomatoGuard AI": "ટોમેટોગાર્ડ AI માં આપનું સ્વાગત છે",
        "Sign In": "સાઇન ઇન કરો",
        "Instant Demo Access (One-Click)": "⚡ ત્વરિત ડેમો પ્રવેશો",
        "Scanner & AI": "સ્કેનર અને AI",
        "Farmer Guidance": "ખેડૂત માર્ગદર્શન",
        "Ask AI Advisor": "AI સલાહકારને પૂછો",
        "Scan Records": "સ્કેન રેકોર્ડ્સ",
        "Disease Library": "રોગ લાયબ્રેરી",
        "Logout": "લૉગ આઉટ",
        "Protect Your Tomato Crop With AI": "AI સાથે તમારા ટમેટાના પાકનું રક્ષણ કરો",
        "Upload Image": "છબી અપલોડ કરો",
        "Scan With Camera": "કેમેરાથી સ્કેન કરો",
        "Run Two-Stage AI Diagnosis": "AI રોગ નિદાન શરૂ કરો",
        "NOT A TOMATO CROP": "⚠️ આ ટમેટાનો પાક નથી",
        "This image does not appear to belong to the tomato crop.": "આ છબી ટમેટાના પાકની હોય તેવું લાગતું નથી.",
        "Please upload or capture a clear image of a tomato leaf.": "કૃપા કરીને ટમેટાના પાંદડાની સ્પષ્ટ છબી અપલોડ કરો.",
        "Tomato Crop Verified": "ટમેટાનો પાક ચકાસાયેલ છે",
        "Crop Health Score": "પાક આરોગ્ય સ્કોર",
        "Farmer Action Plan": "ખેડૂત કાર્ય યોજના"
    },
    "pa": { // Punjabi (ਪੰਜਾਬੀ)
        "TomatoGuard AI": "ਟੋਮੈਟੋਗਾਰਡ AI",
        "Smart Crop Health Assistant": "ਸਮਾਰਟ ਫ਼ਸਲ ਸਿਹਤ ਸਹਾਇਕ",
        "Welcome to TomatoGuard AI": "ਟੋਮੈਟੋਗਾਰਡ AI ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ",
        "Sign In": "ਸਾਈਨ ਇਨ ਕਰੋ",
        "Instant Demo Access (One-Click)": "⚡ ਤੁਰੰਤ ਡੈਮੋ ਪਹੁੰਚ",
        "Scanner & AI": "ਸਕੈਨਰ ਅਤੇ AI",
        "Farmer Guidance": "ਕਿਸਾਨ ਮਾਰਗਦਰਸ਼ਨ",
        "Ask AI Advisor": "AI ਸਲਾਹਕਾਰ ਨੂੰ ਪੁੱਛੋ",
        "Scan Records": "ਸਕੈਨ ਰਿਕਾਰਡ",
        "Disease Library": "ਬਿਮਾਰੀ ਲਾਇਬ੍ਰੇਰੀ",
        "Logout": "ਲਾਗ ਆਉਟ",
        "Protect Your Tomato Crop With AI": "AI ਨਾਲ ਆਪਣੀ ਟਮਾਟਰ ਦੀ ਫ਼ਸਲ ਦੀ ਰੱਖਿਆ ਕਰੋ",
        "Upload Image": "ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
        "Scan With Camera": "ਕੈਮਰੇ ਨਾਲ ਸਕੈਨ ਕਰੋ",
        "Run Two-Stage AI Diagnosis": "AI ਨਿਦਾਨ ਸ਼ੁਰੂ ਕਰੋ",
        "NOT A TOMATO CROP": "⚠️ ਇਹ ਟਮਾਟਰ ਦੀ ਫ਼ਸਲ ਨਹੀਂ ਹੈ",
        "This image does not appear to belong to the tomato crop.": "ਇਹ ਤਸਵੀਰ ਟਮਾਟਰ ਦੀ ਫ਼ਸਲ ਨਾਲ ਸੰਬੰਧਿਤ ਨਹੀਂ ਜਾਪਦੀ।",
        "Please upload or capture a clear image of a tomato leaf.": "ਕਿਰਪਾ ਕਰਕੇ ਟਮਾਟਰ ਦੇ ਪੱਤੇ ਦੀ ਇੱਕ ਸਾਫ਼ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ।",
        "Tomato Crop Verified": "ਟਮਾਟਰ ਦੀ ਫ਼ਸਲ ਦੀ ਪੁਸ਼ਟੀ ਕੀਤੀ ਗਈ",
        "Crop Health Score": "ਫ਼ਸਲ ਸਿਹਤ ਸਕੋਰ",
        "Farmer Action Plan": "ਕਿਸਾਨ ਕਾਰਜ ਯੋਜਨਾ"
    }
};

class TranslationManager {
    constructor() {
        this.currentLang = localStorage.getItem('tomatoguard_lang') || 'en';
        this.selectEl = document.getElementById('languageSelect');
        this.init();
    }

    init() {
        if (this.selectEl) {
            this.selectEl.value = this.currentLang;
            this.selectEl.addEventListener('change', (e) => {
                this.setLanguage(e.target.value);
            });
        }
        this.translateDOM();
    }

    setLanguage(langCode) {
        this.currentLang = langCode;
        localStorage.setItem('tomatoguard_lang', langCode);
        if (this.selectEl) this.selectEl.value = langCode;
        this.translateDOM();
    }

    translateText(key) {
        if (!key || this.currentLang === 'en') return key;
        const dict = UI_DICTIONARIES[this.currentLang];
        if (dict && dict[key]) {
            return dict[key];
        }
        return key;
    }

    translateDOM() {
        const textElements = document.querySelectorAll('[data-i18n]');
        textElements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (key) {
                el.textContent = this.translateText(key);
            }
        });

        // Translate text nodes for elements without data-i18n by exact match
        const allElements = document.querySelectorAll('button, label, h1, h2, h3, h4, p, span, option');
        allElements.forEach(el => {
            if (el.children.length === 0 && el.textContent.trim()) {
                const text = el.textContent.trim();
                const translated = this.translateText(text);
                if (translated !== text) {
                    el.textContent = translated;
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.translationManager = new TranslationManager();
});
