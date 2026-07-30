"""Synthetic vertical payments GTM data."""
import numpy as np, pandas as pd

RNG = np.random.default_rng(42)

VERTICALS = [
    ("Unattended Retail", 4.2, 0.24, "High growth, low penetration"),
    ("Parking", 2.8, 0.18, "Fragmented operators, ISO channel"),
    ("Vending", 1.9, 0.31, "Mature but underserved on connected devices"),
    ("Medical / Healthcare", 6.8, 0.11, "Regulatory-heavy, slow adoption"),
    ("Transportation", 3.4, 0.19, "Contactless-driven, high volume"),
    ("EV Charging", 2.1, 0.42, "Fastest-growing, new entrants"),
    ("Kiosks (QSR)", 3.9, 0.28, "Operator-driven, integrator-led"),
]
COMPETITORS = ["Stripe Terminal", "Adyen", "Square", "Worldpay", "Elavon", "Verifone Cloud"]

def build_vertical_opportunity():
    rows = []
    for name, tam, cagr, note in VERTICALS:
        nmi_share = max(0.005, RNG.normal(0.04, 0.02))
        pipeline = tam * 1e9 * nmi_share * RNG.uniform(0.15, 0.45)
        win_rate = min(0.55, max(0.15, RNG.normal(0.32, 0.08)))
        rows.append(dict(vertical=name, tam_gbp_bn=tam, cagr=cagr,
                         nmi_share=nmi_share, pipeline_gbp=pipeline,
                         win_rate=win_rate, dynamic=note,
                         priority_score=round((tam * cagr * 10) + (win_rate * 15), 1)))
    return pd.DataFrame(rows).sort_values("priority_score", ascending=False)

def build_competitive_grid():
    rows = []
    axes = ["Pricing", "Device breadth", "Vertical depth", "ISO channel",
            "Certification speed", "API developer experience", "Unattended fit"]
    for c in ["NMI"] + COMPETITORS:
        for a in axes:
            score = round(RNG.uniform(3.5, 4.8) if c == "NMI" else RNG.uniform(2.2, 4.5), 1)
            rows.append(dict(vendor=c, axis=a, score=score))
    return pd.DataFrame(rows)

def build_launch_tracker():
    rows = [
        ("Unattended EV Charging bundle", "EV Charging", "Q3 launch", 78, "On track"),
        ("Medical device certification pack", "Medical / Healthcare", "Q4 launch", 42, "At risk"),
        ("Parking ISO enablement toolkit", "Parking", "In market", 92, "Live"),
        ("Vending SmartPOS refresh", "Vending", "Q3 launch", 65, "Monitor"),
        ("Kiosks QSR reference architecture", "Kiosks (QSR)", "Q4 launch", 55, "Monitor"),
        ("Transportation contactless upgrade", "Transportation", "In market", 88, "Live"),
    ]
    return pd.DataFrame(rows, columns=["initiative", "vertical", "stage", "readiness", "status"])

FEATURE_WORDS = {"api", "endpoint", "throughput", "latency", "sdk", "mm", "kg", "spec",
                 "voltage", "port", "usb", "iso", "emv", "encryption", "keys", "bytes",
                 "hardware", "gateway", "device", "terminal", "chipset", "protocol"}
SOLUTION_WORDS = {"revenue", "growth", "operator", "customer", "reduce", "increase",
                  "faster", "downtime", "conversion", "checkout", "adopt", "expand",
                  "outcome", "success", "reliability", "uptime", "acceptance", "pipeline",
                  "market", "vertical", "business", "value", "roi", "efficiency"}

def score_message(text):
    words = [w.lower().strip(".,;:()!?") for w in text.split() if w.strip()]
    if not words: return dict(feature=0, solution=0, verdict="Empty", ratio=0)
    f = sum(1 for w in words if w in FEATURE_WORDS)
    s = sum(1 for w in words if w in SOLUTION_WORDS)
    ratio = s / max(f + s, 1)
    if ratio >= 0.65: v = "Solution-forward"
    elif ratio >= 0.4: v = "Balanced"
    else: v = "Feature/spec-led - rewrite"
    return dict(feature=f, solution=s, verdict=v, ratio=ratio)

def build_channel_health():
    rows = []
    channels = ["Direct sales", "ISO partners", "Software integrators", "Reseller channel"]
    for ch in channels:
        for v, *_ in VERTICALS:
            adoption = min(1, max(0.1, RNG.normal(0.55, 0.18)))
            pipeline = RNG.uniform(200000, 4200000)
            enablement = RNG.choice(["Complete", "In progress", "Gap"], p=[0.55, 0.3, 0.15])
            rows.append(dict(channel=ch, vertical=v, adoption=adoption,
                             pipeline=pipeline, enablement=enablement))
    return pd.DataFrame(rows)
