# -*- coding: utf-8 -*-
"""
Tomato Crop Disease & Agronomy Advisory Knowledge Base
"""

DISEASE_CATALOG = {
    "Tomato___Bacterial_spot": {
        "common_name": "Bacterial Spot",
        "scientific_name": "Xanthomonas perforans / euvesicatoria",
        "pathogen_type": "Bacterial",
        "severity": "High",
        "health_score_impact": 45,
        "symptoms": [
            "Small, dark brown to black circular lesions (1-3mm) on leaves and stems",
            "Lesions often surrounded by a noticeable yellow chlorotic halo",
            "Severe leaf blighting, yellowing, and premature foliage drop",
            "Scabby, rough, raised dark spots on green and ripe tomato fruit"
        ],
        "organic_treatment": [
            "Apply copper-based bactericides (e.g. Copper Hydroxide or Liquid Copper Octanoate) early in the morning.",
            "Use bio-control agents such as Bacillus subtilis (Serenade) or Bacillus amyloliquefaciens.",
            "Spray neem oil (0.5% concentration) to boost leaf surface immunity."
        ],
        "chemical_treatment": [
            "Apply Copper Oxychloride 50% WP (2.5g/L water) mixed with Mancozeb 75% WP (2g/L water).",
            "Streptomycin sulphate 9% + Tetracycline hydrochloride 1% SP (Plantomycin) at 0.5g/L (where authorized by local agricultural authority).",
            "Always adhere strictly to manufacturer label pre-harvest intervals (PHI)."
        ],
        "prevention": [
            "Use certified disease-free, hot-water treated seeds or resistant transplants.",
            "Avoid overhead sprinkler irrigation; use direct drip irrigation to keep foliage dry.",
            "Practice 2-3 year crop rotation with non-solanaceous crops (e.g., maize, beans).",
            "Sterilize pruning shears and stakes with 10% bleach solution between plants."
        ],
        "action_plan": {
            "today": "Immediately prune and safely destroy severely spotted lower leaves (do not compost).",
            "next_3_days": "Apply Copper Hydroxide or bio-bactericide spray across all adjacent plants.",
            "this_week": "Inspect field daily; sanitize all pruning equipment and transition fully to ground/drip irrigation.",
            "prevention": "Plan crop rotation away from solanaceous plants for the upcoming cycle."
        }
    },
    "Tomato___Early_blight": {
        "common_name": "Early Blight",
        "scientific_name": "Alternaria solani",
        "pathogen_type": "Fungal",
        "severity": "Medium-High",
        "health_score_impact": 40,
        "symptoms": [
            "Distinct concentric dark rings forming a 'target board' or 'bullseye' pattern",
            "Initial dark brown lesions start on the oldest lower foliage",
            "Surrounding tissue turns bright yellow (chlorosis), leading to leaf collapse",
            "Dark, sunken, leathery lesions at the stem end of developing fruits"
        ],
        "organic_treatment": [
            "Foliar application of bio-fungicide Trichoderma viride or Bacillus subtilis.",
            "Apply potassium bicarbonate or liquid copper fungicide at first sign of concentric spots.",
            "Organic neem oil formulation applied at 7-day intervals during warm, humid conditions."
        ],
        "chemical_treatment": [
            "Chlorothalonil 75% WP (2g/L) or Mancozeb 75% WP (2.5g/L water) at 7-10 day intervals.",
            "Azoxystrobin 23% SC (1ml/L) or Difenoconazole 25% EC (0.5ml/L) for established infections.",
            "Follow product label and rotate fungicide FRAC groups to prevent pathogen resistance."
        ],
        "prevention": [
            "Mulch heavily (straw or plastic) around plant base to prevent soil spore splashback.",
            "Prune lower suckers and leaves within 30cm of the soil surface.",
            "Provide ample spacing (60cm+) and trellising to promote rapid leaf drying.",
            "Avoid handling wet plants to prevent spreading fungal spores."
        ],
        "action_plan": {
            "today": "Strip and dispose of all lower leaves displaying concentric bullseye rings.",
            "next_3_days": "Apply protectant fungicide (Mancozeb or Copper) covering both leaf sides.",
            "this_week": "Apply thick organic mulch around base and prune dense inner canopy for airflow.",
            "prevention": "Maintain strict 3-year rotation away from potatoes, tomatoes, and eggplants."
        }
    },
    "Tomato___Late_blight": {
        "common_name": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "pathogen_type": "Oomycete / Water Mold",
        "severity": "Critical",
        "health_score_impact": 65,
        "symptoms": [
            "Rapidly expanding, irregular, water-soaked pale-to-dark brown/black lesions",
            "Delicate white cottony/fuzzy fungal growth on the underside of infected leaves in humid weather",
            "Total leaf and stem collapse within 2-4 days in cool, rainy conditions",
            "Large, firm, greasy-brown rot on green and ripening tomato fruits"
        ],
        "organic_treatment": [
            "Emergency removal and burial/burning of all infected plants (never leave in field or compost).",
            "Preventive sprays of Bordeaux mixture (1%) or Copper Oxychloride prior to cool wet spells.",
            "Bio-fungicides offer limited control once active lesions appear; rapid sanitation is essential."
        ],
        "chemical_treatment": [
            "Systemic rescue fungicides: Metalaxyl 8% + Mancozeb 64% WP (Ridomil MZ at 2.5g/L).",
            "Dimethomorph 50% WP (1g/L) or Cymoxanil + Mancozeb (2g/L).",
            "Ensure full coverage under leaf canopies; spray early morning after dew dries."
        ],
        "prevention": [
            "Plant certified late-blight resistant tomato hybrids (e.g., Mountain Magic, Defiant).",
            "Never plant tomatoes adjacent to potato fields.",
            "Ensure rapid soil drainage and avoid night-time irrigation.",
            "Monitor regional agricultural blight forecasting alerts."
        ],
        "action_plan": {
            "today": "CRITICAL: Inspect entire field immediately. Bag and remove heavily blighted plants.",
            "next_3_days": "Apply systemic anti-oomycete fungicide (Metalaxyl / Dimethomorph) across unaffected plants.",
            "this_week": "Cease overhead sprinkling; eliminate standing water and improve field air circulation.",
            "prevention": "Select certified resistant tomato cultivars for subsequent growing seasons."
        }
    },
    "Tomato___Leaf_Mold": {
        "common_name": "Leaf Mold",
        "scientific_name": "Passalora fulva (Cladosporium fulvum)",
        "pathogen_type": "Fungal",
        "severity": "Medium",
        "health_score_impact": 30,
        "symptoms": [
            "Pale yellow to light green diffuse patches on upper leaf surfaces",
            "Olive-green to velvety brown velvety mold growth on the corresponding lower leaf surface",
            "Infected leaves curl, wither, and drop prematurely from the bottom upward",
            "Primarily prevalent in greenhouses and high tunnels with relative humidity above 85%"
        ],
        "organic_treatment": [
            "Spray baking soda (potassium bicarbonate) solution (5g/L) with mild organic soap.",
            "Apply Copper Octanoate or bio-fungicide Bacillus subtilis (Serenade).",
            "Exhaust humid greenhouse air with high-volume ventilation fans."
        ],
        "chemical_treatment": [
            "Chlorothalonil 75% WP (2g/L) or Difenoconazole 25% EC (0.5ml/L).",
            "Fluopyram + Trifloxystrobin formulation for protected greenhouse cultivation."
        ],
        "prevention": [
            "Maintain greenhouse relative humidity strictly below 80-85%.",
            "Increase plant spacing and prune lower foliage to optimize canopy air movement.",
            "Utilize resistant hybrid varieties carrying Cladosporium resistance genes (Cf-genes)."
        ],
        "action_plan": {
            "today": "Open greenhouse side vents and turn on circulating fans to drop ambient humidity.",
            "next_3_days": "Prune out dense lower foliage showing olive mold undersides.",
            "this_week": "Apply potassium bicarbonate or copper fungicide spray if humidity remains high.",
            "prevention": "Install automated humidity control and space transplants at least 50cm apart."
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "common_name": "Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "pathogen_type": "Fungal",
        "severity": "Medium",
        "health_score_impact": 35,
        "symptoms": [
            "Numerous small (1.5 - 3mm), circular spots with ash-gray centers and dark brown margins",
            "Tiny black specks (pycnidia fruiting bodies) visible inside gray centers under hand lens",
            "Begins on oldest lower leaves and progresses steadily upward",
            "Leaves turn completely yellow, wither, and fall, exposing fruit to sunscald"
        ],
        "organic_treatment": [
            "Remove lower infected leaves as soon as first 1-2 spots appear.",
            "Liquid copper fungicide sprays applied every 7-10 days.",
            "Foliar sprays of biological Trichoderma harzianum or Bacillus subtilis."
        ],
        "chemical_treatment": [
            "Mancozeb 75% WP (2.5g/L) or Chlorothalonil 75% WP (2g/L).",
            "Azoxystrobin or Pyraclostrobin strobilurin fungicides for severe pressure."
        ],
        "prevention": [
            "Apply straw/plastic mulch immediately at transplanting to eliminate soil splash.",
            "Maintain 3-year rotation away from solanaceous species.",
            "Control solanaceous weeds (e.g. nightshade, horsenettle) around field borders.",
            "Clean and sanitize tomato support stakes after every season."
        ],
        "action_plan": {
            "today": "Prune off and discard lowest yellowing leaves with gray-centered spots.",
            "next_3_days": "Apply protective Mancozeb or Copper spray to cover both leaf surfaces.",
            "this_week": "Lay down mulch under all plants and adjust irrigation to drip lines only.",
            "prevention": "Ensure deep autumn plowing to bury crop debris where fungus overwinters."
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "common_name": "Two-Spotted Spider Mite",
        "scientific_name": "Tetranychus urticae",
        "pathogen_type": "Arachnid Pest",
        "severity": "Medium-High",
        "health_score_impact": 40,
        "symptoms": [
            "Fine yellow, white, or bronze speckling (stippling) on upper leaf surfaces",
            "Delicate silken webbing visible on undersides of leaves and growing tips",
            "Leaves become dry, bronzed, papery, and drop under heavy infestation",
            "Infestations explode rapidly during hot, dry, dusty weather conditions"
        ],
        "organic_treatment": [
            "High-pressure water spray directed to leaf undersides to knock down mite colonies.",
            "Apply insecticidal soap, neem oil (1%), or horticultural mineral oil.",
            "Release biological predatory mites (Phytoseiulus persimilis or Neoseiulus californicus)."
        ],
        "chemical_treatment": [
            "Abamectin 1.9% EC (0.5ml/L) or Spiromesifen 22.9% SC (1ml/L).",
            "Hexythiazox 5.45% EC (1ml/L) or Fenazaquin 10% EC (1.5ml/L).",
            "Rotate miticide modes of action (IRAC groups) to prevent rapid resistance buildup."
        ],
        "prevention": [
            "Keep farm roads and surrounding paths watered to reduce dust clouds.",
            "Ensure regular, adequate irrigation as drought-stressed plants attract mites.",
            "Avoid indiscriminate use of broad-spectrum synthetic pyrethroids that kill natural predators."
        ],
        "action_plan": {
            "today": "Wash underside of foliage with pressurized water jet to disrupt webs.",
            "next_3_days": "Apply insecticidal soap or Neem oil spray in the late afternoon.",
            "this_week": "If severe, apply targeted miticide (Abamectin/Spiromesifen); keep soil well-watered.",
            "prevention": "Introduce predatory mites early in the season and keep dust levels low."
        }
    },
    "Tomato___Target_Spot": {
        "common_name": "Target Spot",
        "scientific_name": "Corynespora cassiicola",
        "pathogen_type": "Fungal",
        "severity": "Medium",
        "health_score_impact": 35,
        "symptoms": [
            "Small brown pinpoint lesions expanding into large circular spots (up to 10mm)",
            "Light brown centers with dark brown borders and faint target-like concentric rings",
            "Upper canopy leaves can be infected directly during warm, humid rainfall periods",
            "Fruit lesions are deeply sunken and circular with dark margins"
        ],
        "organic_treatment": [
            "Copper hydroxide or copper sulfate sprays.",
            "Bio-fungicides like Bacillus amyloliquefaciens.",
            "Prompt removal of all infected canopy leaves."
        ],
        "chemical_treatment": [
            "Azoxystrobin 23% SC (1ml/L) or Boscalid + Pyraclostrobin.",
            "Chlorothalonil 75% WP (2g/L) for protective coverage."
        ],
        "prevention": [
            "Stake and trellis tomato vines to keep foliage off wet ground.",
            "Provide ample ventilation in greenhouse tunnels.",
            "Sanitize all tools and avoid moving through wet crops."
        ],
        "action_plan": {
            "today": "Prune out diseased foliage and destroy off-field.",
            "next_3_days": "Apply protectant fungicide (Chlorothalonil/Copper) before anticipated rain.",
            "this_week": "Stake loose vines and improve row airflow.",
            "prevention": "Implement standard 2-year crop rotation."
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "scientific_name": "Begomovirus (Transmitted by Bemisia tabaci Whitefly)",
        "pathogen_type": "Viral (Vector-borne)",
        "severity": "Critical",
        "health_score_impact": 60,
        "symptoms": [
            "Severe upward curling and cupping of young leaves ('spoon-shaped' foliage)",
            "Prominent yellowing (chlorosis) along leaf margins and interveinal areas",
            "Severe plant stunting with shortened internodes, giving a bushy appearance",
            "Heavy flower abortion with near-total cessation of fruit production"
        ],
        "organic_treatment": [
            "No chemical cure exists for viral infection inside plant tissue.",
            "Immediately rogue (uproot) and destroy all infected plants to protect remaining crop.",
            "Install yellow sticky traps (15-20 traps/acre) to monitor and capture whitefly vectors.",
            "Spray neem oil (0.5%) or insecticidal soap to suppress whitefly nymphs."
        ],
        "chemical_treatment": [
            "Target the whitefly vector: Imidacloprid 17.8% SL (0.5ml/L) or Thiamethoxam 25% WG (0.3g/L).",
            "Acetamiprid 20% SP (0.5g/L) or Spirotetramat 15.31% OD (1ml/L).",
            "Rotate insecticide classes to manage whitefly resistance."
        ],
        "prevention": [
            "Plant certified TYLCV-resistant hybrids (e.g. Tyking, Saria, Abhinav).",
            "Use 50-mesh insect-proof netting in nurseries and greenhouse vents.",
            "Use reflective silver mulches which repel incoming adult whiteflies.",
            "Maintain a 2-month host-free period between tomato cropping cycles."
        ],
        "action_plan": {
            "today": "Immediately remove, bag, and destroy stunted yellow-curled plants.",
            "next_3_days": "Erect yellow sticky cards and spray whitefly insecticide/neem formulation.",
            "this_week": "Inspect field borders for alternate weed hosts of whitefly.",
            "prevention": "Ensure all future plantings utilize proven TYLCV-resistant tomato hybrids."
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "scientific_name": "Tobamovirus",
        "pathogen_type": "Viral (Mechanically transmitted)",
        "severity": "High",
        "health_score_impact": 50,
        "symptoms": [
            "Mottled alternating light and dark green mosaic pattern on leaves",
            "Distorted, blistered, crinkled, or strap-like 'fern-like' leaves",
            "Severe plant stunting and uneven fruit ripening with internal brown vascular necrosis",
            "Highly stable virus spread easily by hands, tools, clothes, and seed"
        ],
        "organic_treatment": [
            "No cure exists once infected; rogue and burn infected plants immediately.",
            "Wash workers' hands and tools in 20% non-fat dry milk solution before handling plants.",
            "Dip grafting and pruning knives in 10% trisodium phosphate (TSP) or household bleach."
        ],
        "chemical_treatment": [
            "No chemical virucide available.",
            "Focus entirely on hygiene and chemical disinfection of equipment."
        ],
        "prevention": [
            "Purchase certified virus-free seed from reputable seed companies.",
            "Strict no-smoking policy near greenhouse/field (tobacco carries mosaic viruses).",
            "Select ToMV-resistant tomato varieties (designated with 'T' or 'ToMV')."
        ],
        "action_plan": {
            "today": "Uproot infected mosaic plants carefully to prevent sap contact with neighboring vines.",
            "next_3_days": "Disinfect all stakes, clips, and pruning shears in 10% bleach or milk solution.",
            "this_week": "Enforce strict tool hygiene and hand-washing protocols for all field workers.",
            "prevention": "Source exclusively certified disease-free and ToMV-resistant seeds."
        }
    },
    "Tomato___healthy": {
        "common_name": "Healthy Tomato Foliage",
        "scientific_name": "Solanum lycopersicum",
        "pathogen_type": "None (Healthy Plant)",
        "severity": "None",
        "health_score_impact": 0,
        "symptoms": [
            "Vibrant, deep green foliage with uniform chlorophyll distribution",
            "Crisp leaf margins without lesions, spots, yellowing, or curl",
            "Stout stems, active terminal shoot elongation, and normal flower/fruit set",
            "Zero silken webbing, bacterial oozing, or mold fuzz"
        ],
        "organic_treatment": [
            "Maintain routine bi-weekly organic nutrition with compost tea and liquid seaweed extract.",
            "Apply prophylactic neem oil spray (0.3%) once every 14 days to deter casual pests.",
            "Add vermicompost and mycorrhizal fungi around root zone to enhance nutrient uptake."
        ],
        "chemical_treatment": [
            "Maintain balanced N-P-K fertigation (e.g. 19:19:19 during vegetative, 13:0:45 during fruiting).",
            "Foliar spray of Calcium Nitrate (1g/L) + Boron (0.5g/L) to prevent blossom end rot."
        ],
        "prevention": [
            "Maintain consistent drip irrigation schedule (preventing drought-flood stress).",
            "Stake and prune suckers regularly on sunny mornings for rapid wound healing.",
            "Conduct bi-weekly scouting of lower canopy leaves for early detection of any emerging issues."
        ],
        "action_plan": {
            "today": "Continue standard routine care; inspect underside of leaves periodically.",
            "next_3_days": "Ensure consistent soil moisture to prevent blossom end rot.",
            "this_week": "Apply balanced micronutrient foliar spray (Calcium/Boron/Zinc).",
            "prevention": "Maintain regular weeding and scouting schedule throughout the season."
        }
    }
}
