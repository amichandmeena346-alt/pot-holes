import cv2
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ==========================================
# 1. PURANA POTHOLE DETECTION & MEASUREMENT CODE
# ==========================================
# Yahan aapka purana YOLO model loading aur measurement logic chalega


@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# 2. NAYA IRC CODE REFERENCE SEARCH ROUTINE
# ==========================================
IRC_KNOWLEDGE_BASE = {
    "subgrade_compaction": {
        "category": "Flexible & Rigid Base",
        "topic": "Subgrade & Embankment Compaction",
        "code": "IRC:36-2010 / MoRTH Section 300",
        "clause": "Clause 305.2.2 & Table 300-2",
        "detail": (
            "Subgrade layer (top 500mm) ke liye minimum compaction 97% MDD"
            " (Modified Proctor) zaroori hai."
        ),
        "tolerance": (
            "Density deficit > 2% hone par layer reject kar di jayegi."
        ),
    },
    "wmm_base": {
        "category": "Flexible Pavement",
        "topic": "Wet Mix Macadam (WMM)",
        "code": "IRC:109-2015 / MoRTH Section 400",
        "clause": "Clause 406.3 & Clause 6.3",
        "detail": (
            "Compacted thickness per layer 75mm-100mm honi chahiye. OMC control"
            " mixing ke time zaroori hai."
        ),
        "tolerance": (
            "Moisture Content: OMC ±0.5%. Surface Level Tolerance: +10mm /"
            " -10mm."
        ),
    },
    "dbm_bc_density": {
        "category": "Flexible Pavement",
        "topic": "Dense Bituminous Macadam (DBM) & Bituminous Concrete (BC)",
        "code": "IRC:110-2012 / MoRTH Section 500",
        "clause": "Clause 505 & Clause 507",
        "detail": (
            "Field Core Density minimum 92% of Theoretical Maximum Specific"
            " Gravity (Gmm) honi chahiye."
        ),
        "tolerance": (
            "Bitumen Content Tolerance: OBC ±0.3%. Temperature at laying: Min"
            " 140°C."
        ),
    },
    "pavements_pqc": {
        "category": "Rigid Pavement",
        "topic": "Pavement Quality Concrete (PQC) Grade & Strength",
        "code": "IRC:15-2017 / MoRTH Section 600",
        "clause": "Clause 602.3",
        "detail": (
            "PQC Minimum Grade M40. 28-days Flexural Strength minimum 4.5 MPa"
            " required hai."
        ),
        "tolerance": "Slump: 25 ± 15 mm (Slip-form) / 40 ± 15 mm (Fixed-form).",
    },
    "potholes": {
        "category": "Flexible Pavement",
        "topic": "Potholes & Surface Defects",
        "code": "IRC:82-2023",
        "clause": "Clause 4.2.1",
        "detail": (
            "Depth > 25mm ya Area > 0.1 sq.m ko High Severity Pothole classify"
            " kiya jata hai."
        ),
        "tolerance": "Max allowable depth before immediate repair: 15mm.",
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
