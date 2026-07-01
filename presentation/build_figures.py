#!/usr/bin/env python3
"""Build the figures for the HAB landscape slides from the traceable data JSON.

Reads presentation/data/{tools,models}.json and writes PNGs to presentation/figures/.
Small-N hygiene: raw counts only, every bar labelled, integer axes, N stated in titles.
Model universe is consistent: 14 nowcasting/forecasting models (is_model=true); the 1
literature review (is_model=false) is context, not counted. Deterministic.
"""
import json
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

tools = json.load(open(os.path.join(DATA, "tools.json"), encoding="utf-8"))["tools"]
MJSON = json.load(open(os.path.join(DATA, "models.json"), encoding="utf-8"))
models_all = MJSON["models"]
models = [m for m in models_all if m.get("is_model")]          # 14 forecasting/nowcasting models
n_models = len(models)
FEATURE_CLASSES = MJSON["_meta"]["feature_classes"]
FEAT2CLASS = {f: cls for cls, feats in FEATURE_CLASSES.items() for f in feats}

# palette
BLUE = "#3b6ea5"; NAVY = "#274c77"; GREEN = "#4c956c"; ORANGE = "#e07b39"
GREY = "#9aa5b1"; DGREY = "#555f6b"; RED = "#d62728"
CLASS_COLOR = {"weather": "#6baed6", "hydroclimate": "#4c956c", "static": "#9aa5b1",
               "earth-obs / bloom signal": "#8c6bb1", "chemistry": "#e07b39"}

S = 1.15  # +15% text everywhere (per request)
plt.rcParams.update({"font.size": round(11 * S, 1), "axes.spines.top": False,
                     "axes.spines.right": False, "font.family": "DejaVu Sans", "axes.titleweight": "bold"})


def lab(ax, bars, vals, horiz=False, pad=0.05, size=10):
    for b, v in zip(bars, vals):
        if horiz:
            ax.text(b.get_width() + pad, b.get_y() + b.get_height() / 2, str(v), va="center", ha="left",
                    fontsize=size * S, fontweight="bold")
        else:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + pad, str(v), ha="center", va="bottom",
                    fontsize=size * S, fontweight="bold")


def norm_access(a):
    a = a.lower()
    return "Freemium" if "freemium" in a else "Paid" if "paid" in a else "Free" if "free" in a else a


ORG_LABEL = {"federal": "Federal\ngov't", "state-local": "State /\nlocal gov't", "private": "Private\nsector"}
MTYPE_LABEL = {"empirical-RS": "Empirical\nsatellite", "statistical-ML": "Statistical\n/ ML",
               "mechanistic": "Physics-\nbased", "in-situ-sampling": "In-situ\nmonitoring"}
FEATURE_LABEL = {
    "water_temperature": "Water temperature", "nutrients": "Nutrients (N / P)",
    "satellite_reflectance": "Satellite reflectance / index", "precipitation": "Precipitation",
    "wind_mixing": "Wind / mixing", "hydrology_flow": "Hydrology / flow",
    "lake_morphology": "Lake depth / area", "prior_bloom_state": "Prior bloom state (persistence)",
    "pH": "pH", "dissolved_oxygen": "Dissolved oxygen",
    "phycocyanin_signal": "Phycocyanin (in-situ pigment)", "geolocation": "Geolocation (lat/lon)",
}
ALGO_FAMILY = {
    "M1": "Bayesian spatiotemporal", "M2": "Bayesian spatiotemporal",
    "M3": "Tree / boosting", "M5": "Tree / boosting", "M6": "Tree / boosting",
    "M8": "Tree / boosting", "M11": "Tree / boosting",
    "M4": "Deep learning (LSTM/CNN)", "M14": "Deep learning (LSTM/CNN)",
    "M7": "ANN / SVM", "M9": "Mechanistic / process-based", "M10": "Mechanistic / process-based",
    "M12": "Mechanistic / process-based", "M15": "Hyperspectral sensor",
}


def norm_signal(s):
    s = s.lower()
    if s.startswith("in-situ"):
        return "In-situ (± weather/physical)"
    if s == "fusion":
        return "Fusion (satellite + in-situ)"
    if s == "satellite":
        return "Satellite only"
    if s == "hybrid":
        return "Hybrid (ML + process)"
    return "Other"


# ================= FIGURE 1: tools — 3 stacked barplots (vertical column) =================
def fig_tools_stack():
    fc = [t for t in tools if "forecast" in t["horizon"].lower()]   # forward-looking tools
    org_fc = Counter(t["org_type"] for t in fc)
    acc_fc = Counter(norm_access(t["access"]) for t in fc)
    mt_fc = Counter(t["model_type"] for t in fc)

    fig, axes = plt.subplots(3, 1, figsize=(5.5, 7.4))
    fig.suptitle(f"HAB tools landscape  (N = {len(tools)})", fontsize=13.5, fontweight="bold", y=0.996)

    def panel(ax, counter, fc_counter, order, labeler, bar_colors, title):
        vals = [counter[k] for k in order]
        bars = ax.bar([labeler(k) for k in order], vals, color=bar_colors, zorder=3)
        for k, b in zip(order, bars):
            f = fc_counter.get(k, 0)
            if f > 0:
                ax.bar(b.get_x() + b.get_width() / 2, f, width=b.get_width(), facecolor="none",
                       edgecolor=RED, linewidth=2.4, zorder=5)
                ax.text(b.get_x() + b.get_width() / 2, f - 0.05, str(f), ha="center", va="top",
                        fontsize=8.5, fontweight="bold", color=RED,
                        bbox=dict(facecolor="white", edgecolor="none", pad=0.4, alpha=0.75))
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 0.12, str(v), ha="center", va="bottom",
                    fontsize=9.5, fontweight="bold")
        ax.set_title(title, fontsize=11.5)
        ax.set_ylim(0, max(vals) + 1.4); ax.set_yticks(range(0, max(vals) + 2, max(1, (max(vals) + 1) // 5)))
        ax.tick_params(axis="x", labelsize=8.7); ax.tick_params(axis="y", labelsize=8.7)

    o = [k for k, _ in Counter(t["org_type"] for t in tools).most_common()]
    panel(axes[0], Counter(t["org_type"] for t in tools), org_fc, o, lambda k: ORG_LABEL.get(k, k),
          [NAVY if k == "federal" else BLUE if k == "state-local" else GREEN for k in o], "Who makes them")

    a = [k for k in ["Free", "Freemium", "Paid"] if Counter(norm_access(t["access"]) for t in tools).get(k)]
    panel(axes[1], Counter(norm_access(t["access"]) for t in tools), acc_fc, a, lambda k: k,
          [GREEN if k == "Free" else ORANGE if k == "Paid" else BLUE for k in a], "Cost of access")

    m = [k for k, _ in Counter(t["model_type"] for t in tools).most_common()]
    panel(axes[2], Counter(t["model_type"] for t in tools), mt_fc, m, lambda k: MTYPE_LABEL.get(k, k),
          [BLUE] * len(m), "How they work")

    fig.text(0.5, 0.012, "Red outline = # that forecast ahead\n(vs. nowcast / observation only)",
             ha="center", fontsize=8.6, style="italic", color=RED)
    fig.tight_layout(rect=[0, 0.055, 1, 0.965])
    fig.savefig(os.path.join(FIG, "fig1_tools_panel.png"), dpi=200)
    plt.close(fig)
    print("wrote fig1_tools_panel.png (3x1 stack, red forecast overlays)")


# ================= FIGURE 2: feature frequency (hero) =================
def fig_feature_frequency():
    reported = [m for m in models if m["features_reported"]]
    n = len(reported)
    presence = Counter(); topcount = Counter()
    for m in reported:
        for f in m["features"]:
            presence[f] += 1
        for f in m["top_features"]:
            topcount[f] += 1
    feats = [f for f, _ in presence.most_common()][::-1]
    pres_vals = [presence[f] for f in feats]
    top_vals = [topcount.get(f, 0) for f in feats]

    fig, ax = plt.subplots(figsize=(13.2, 7.2))
    ypos = list(range(len(feats)))
    colors = [CLASS_COLOR[FEAT2CLASS[f]] for f in feats]
    bars = ax.barh(ypos, pres_vals, color=colors, zorder=3)
    # red-border overlay = # models where the feature is the TOP-ranked predictor
    for i, (f, t) in enumerate(zip(feats, top_vals)):
        if t > 0:
            ax.barh(i, t, facecolor="none", edgecolor=RED, linewidth=2.6, zorder=5)
    ax.set_yticks(ypos)
    ax.set_yticklabels([FEATURE_LABEL.get(f, f) for f in feats], fontsize=11.5 * S)
    for i, (p, t) in enumerate(zip(pres_vals, top_vals)):
        ax.text(p + 0.08, i, f"{p}", va="center", ha="left", fontsize=10.5 * S, fontweight="bold")
        if t:
            ax.text(t + 0.08, i - 0.02, f"{t}★", va="center", ha="left", fontsize=8.5 * S,
                    fontweight="bold", color=RED)
    ax.set_xlabel("Number of models", fontsize=12.6, labelpad=4)
    ax.set_xlim(0, max(pres_vals) + 1.4); ax.set_xticks(range(0, max(pres_vals) + 2))
    ax.set_title(f"What drives freshwater HAB models  (features used across {n} of {n_models} models)",
                 fontsize=15, pad=12)
    # legends: feature classes + red-border meaning
    class_handles = [Patch(facecolor=CLASS_COLOR[c], label=c) for c in CLASS_COLOR]
    red_handle = Patch(facecolor="white", edgecolor=RED, linewidth=2.4,
                       label="red outline = # models where it's the #1 predictor")
    leg = ax.legend(handles=class_handles + [red_handle], title="Feature class",
                    loc="lower right", fontsize=10.4, title_fontsize=11, frameon=True)
    leg.get_frame().set_edgecolor(GREY)
    fig.text(0.5, 0.055, "Water temperature & nutrients are the near-universal inputs; water temperature is most often the #1 predictor.",
             ha="center", fontsize=9.8, style="italic", color=DGREY)
    fig.text(0.5, 0.022, "But that is a correlational, model-internal signal (often a seasonal proxy) — phycocyanin, nutrients or geolocation lead in some models.",
             ha="center", fontsize=9.8, style="italic", color=DGREY)
    fig.tight_layout(rect=[0, 0.09, 1, 0.99])
    fig.savefig(os.path.join(FIG, "fig2_feature_frequency.png"), dpi=200)
    plt.close(fig)
    print(f"wrote fig2_feature_frequency.png ({n} of {n_models} models; class-coloured, red-border top-predictor)")


# ================= FIGURE 3: models context (algorithm + data signal) =================
def fig_models_context():
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 3.6))
    fig.suptitle(f"The research frontier at a glance  (N = {n_models} models)", fontsize=15, fontweight="bold")

    ax = axes[0]
    c = Counter(ALGO_FAMILY[m["id"]] for m in models)
    order = [k for k, _ in c.most_common()][::-1]
    vals = [c[k] for k in order]
    bars = ax.barh(order, vals, color=BLUE, zorder=3)
    lab(ax, bars, vals, horiz=True, size=10)
    ax.set_title("Type of algorithm", fontsize=13.2)
    ax.set_xlim(0, max(vals) + 1.2); ax.set_xticks(range(0, max(vals) + 2))
    ax.tick_params(axis="y", labelsize=9.5 * S)

    ax = axes[1]
    c = Counter(norm_signal(m["data_signal"]) for m in models)
    order = [k for k, _ in c.most_common()][::-1]
    vals = [c[k] for k in order]
    colors = [ORANGE if "In-situ" in k else BLUE for k in order]
    bars = ax.barh(order, vals, color=colors, zorder=3)
    lab(ax, bars, vals, horiz=True, size=10)
    ax.set_title("What data signal they use", fontsize=13.2)
    ax.set_xlim(0, max(vals) + 1.2); ax.set_xticks(range(0, max(vals) + 2))
    ax.tick_params(axis="y", labelsize=9.5 * S)

    fig.text(0.5, 0.02, "Most frontier ML is in-situ-driven (and non-US: Korea / China / Germany dominate). "
             "Tree/boosting counts include ensembles. The 168-study review is context, not a model.",
             ha="center", fontsize=9.2, style="italic", color=DGREY)
    fig.tight_layout(rect=[0, 0.08, 1, 0.92])
    fig.savefig(os.path.join(FIG, "fig3_models_context.png"), dpi=200)
    plt.close(fig)
    print(f"wrote fig3_models_context.png (N={n_models})")


if __name__ == "__main__":
    fig_tools_stack()
    fig_feature_frequency()
    fig_models_context()
    print("figures ->", FIG)
