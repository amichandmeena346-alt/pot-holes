from flask import Flask, jsonify, render_template, request

app = Flask(_name_)

# Complete Flexible & Rigid Pavement IRC & MoRTH Database
IRC_KNOWLEDGE_BASE = {
    # --- FLEXIBLE PAVEMENT (BITUMINOUS & BASE) ---
    "subgrade_compaction": {
        "category": "Flexible & Rigid Base",
        "topic": "Subgrade & Embankment Compaction",
        "code": "IRC:36-2010 / MoRTH Section 300",
        "clause": "Clause 305.2.2 & Table 300-2",
        "detail": (
            "Subgrade layer (top 500mm) ke liye minimum compaction 97% MDD"
            " (Modified Proctor) zaroori hai. Embankment ke liye minimum 95%"
            " MDD required hai."
        ),
        "tolerance": (
            "Density deficit > 2% hone par layer reject kar di jayegi."
        ),
    },
    "gsb_granulated": {
        "category": "Flexible Pavement",
        "topic": "Granular Sub-Base (GSB)",
        "code": "IRC:37-2018 / MoRTH Section 400",
        "clause": "Clause 401.3 & Table 400-1",
        "detail": (
            "GSB material CBR value minimum 30% honi chahiye. Liquid Limit"
            " < 25% aur Plasticity Index < 6% hona chahiye."
        ),
        "tolerance": "Thickness Tolerance: +10mm / -15mm. Surface level ±10mm.",
    },
    "wmm_base": {
        "category": "Flexible Pavement",
        "topic": "Wet Mix Macadam (WMM)",
        "code": "IRC:109-2015 / MoRTH Section 400",
        "clause": "Clause 406.3 & Clause 6.3",
        "detail": (
            "Compacted thickness per layer 75mm-100mm honi chahiye. OMC"
            " (Optimum Moisture Content) control mixing ke time zaroori hai."
        ),
        "tolerance": (
            "Moisture Content: OMC ±0.5%. Surface Level Tolerance: +10mm /"
            " -10mm."
        ),
    },
    "prime_tack_coat": {
        "category": "Flexible Pavement",
        "topic": "Prime Coat & Tack Coat Application",
        "code": "MoRTH Section 500",
        "clause": "Clause 502 & Clause 503",
        "detail": (
            "Prime coat rate: Granular base par 0.7 to 1.0 kg/sq.m. Tack coat"
            " rate: Bituminous surface par 0.2 to 0.3 kg/sq.m (Emulsion RS-1)."
        ),
        "tolerance": (
            "Spray quantity variation ±0.05 kg/sq.m se zyada nahi honi chahiye."
        ),
    },
    "dbm_bc_density": {
        "category": "Flexible Pavement",
        "topic": "Dense Bituminous Macadam (DBM) & Bituminous Concrete (BC)",
        "code": "IRC:110-2012 / MoRTH Section 500",
        "clause": "Clause 505 & Clause 507",
        "detail": (
            "Field Core Density minimum 92% of Theoretical Maximum Specific"
            " Gravity (Gmm) honi chahiye. Air voids in mix 3% se 5% ke beech"
            " hone chahiye."
        ),
        "tolerance": (
            "Bitumen Content Tolerance: OBC ±0.3%. Temperature at laying: Min"
            " 140°C (for VG-30)."
        ),
    },
    "flexible_defects": {
        "category": "Flexible Pavement",
        "topic": "Potholes, Cracking & Rutting Distress",
        "code": "IRC:82-2023",
        "clause": "Clause 4.2 & Table 3",
        "detail": (
            "Potholes > 25mm depth ya Alligator Cracks > 3mm width ko High"
            " Severity distress mana jata hai. Rutting depth > 10mm hone par"
            " structural overlay zaroori hai."
        ),
        "tolerance": (
            "Immediate Patch Repair limit: Pothole area > 0.1 sq.m par Hot Mix"
            " / Cold Mix patching required."
        ),
    },
    "surface_roughness": {
        "category": "Flexible & Rigid Pavement",
        "topic": "Surface Evenness & Bump Integrator (BI)",
        "code": "IRC:SP:16-2019",
        "clause": "Clause 5.1 & Table 2",
        "detail": (
            "Riding quality check karne ke liye BI test hota hai. Highway ke"
            " liye BI Value < 2400 mm/km honi chahiye."
        ),
        "tolerance": (
            "BI > 3000 mm/km = Deficient. Immediate Profile Correction Course"
            " (PCC) ya milling required."
        ),
    },
    # --- RIGID PAVEMENT (CEMENT CONCRETE ROADS) ---
    "dlc_subbase": {
        "category": "Rigid Pavement",
        "topic": "Dry Lean Concrete (DLC) Sub-base",
        "code": "IRC:SP:49-2014 / MoRTH Section 600",
        "clause": "Clause 601.3",
        "detail": (
            "DLC ki minimum average 7-day compressive strength 10 MPa honi"
            " chahiye. Aggregate-Cement ratio 12:1 ya 14:1 hota hai."
        ),
        "tolerance": "Thickness Tolerance: +6mm / -10mm. Surface level ±6mm.",
    },
    "pavement_quality_concrete": {
        "category": "Rigid Pavement",
        "topic": "Pavement Quality Concrete (PQC) Grade & Strength",
        "code": "IRC:15-2017 / IRC:44-2017 / MoRTH Section 600",
        "clause": "Clause 602.3 & Table 600-3",
        "detail": (
            "PQC Minimum Grade M40 (or M45 for heavy traffic) hona chahiye."
            " 28-days characteristic Flexural Strength minimum 4.5 MPa (ya"
            " Compressive Strength > 48 MPa) required hai."
        ),
        "tolerance": (
            "Slump at paving plant: 25 ± 15 mm (Slip-form) / 40 ± 15 mm"
            " (Fixed-form)."
        ),
    },
    "dowel_tie_bars": {
        "category": "Rigid Pavement",
        "topic": "Dowel Bars & Tie Bars Alignment",
        "code": "IRC:15-2017 / IRC:58-2015",
        "clause": "Clause 8.4 & Clause 8.5",
        "detail": (
            "Transverse Contraction Joints par Dowel Bars (Mild Steel / TMT)"
            " aur Longitudinal Joints par Tie Bars ka placement level aur"
            " spacing exact honi chahiye."
        ),
        "tolerance": (
            "Dowel Bar alignment tolerance: Max 2mm misalignment per 300mm bar"
            " length."
        ),
    },
    "joint_sealing": {
        "category": "Rigid Pavement",
        "topic": "Concrete Joint Saw Cutting & Sealing",
        "code": "IRC:15-2017 / MoRTH Section 600",
        "clause": "Clause 602.10",
        "detail": (
            "Initial joint cutting paving ke 8 se 24 ghante ke andar depth"
            " T/4 to T/3 tak kar deni chahiye. Joints me Silicone / Polyurethane"
            " sealant bhara jana chahiye."
        ),
        "tolerance": (
            "Width of groove: 6mm to 10mm. Depth tolerance: ±2mm."
        ),
    },
    "pqc_curing": {
        "category": "Rigid Pavement",
        "topic": "PQC Curing & Protection",
        "code": "IRC:15-2017",
        "clause": "Clause 11.2",
        "detail": (
            "Liquid Curing Compound paving ke turant baad spray karna zaroori"
            " hai. Iske baad moist hessian/burlap cloth se minimum 14 din tak"
            " curing honi chahiye."
        ),
        "tolerance": (
            "Curing compound coverage rate: Minimum 0.2 litres/sq.m."
        ),
    },
    "rigid_defects": {
        "category": "Rigid Pavement",
        "topic": "Concrete Cracks, Spalling & Faulting",
        "code": "IRC:SP:83-2018",
        "clause": "Clause 5.3 & Table 4",
        "detail": (
            "Hairline plastic shrinkage cracks < 0.5mm ko slurry seal kar"
            " sakte hain. Structural/Full-depth cracks ya Corner Breaks me full"
            " slab replacement required hota hai."
        ),
        "tolerance": (
            "Joint Faulting/Stepping > 5mm hone par grinding ya slab jacking"
            " mandatory hai."
        ),
    },
}


@app.route("/search_irc", methods=["GET"])
def search_irc():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"results": []})

    matched_results = []
    for key, item in IRC_KNOWLEDGE_BASE.items():
        if (
            query in key
            or query in item["topic"].lower()
            or query in item["code"].lower()
            or query in item["detail"].lower()
            or query in item["category"].lower()
        ):
            matched_results.append(item)

    return jsonify({"results": matched_results})
