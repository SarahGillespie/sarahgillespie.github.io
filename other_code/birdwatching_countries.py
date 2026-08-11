"""
World Map Country Highlighter
Highlight specific countries in custom colors using geopandas + matplotlib.

Install dependencies:
    pip install geopandas matplotlib requests
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from adjustText import adjust_text
from pathlib import Path


# ──────────────────────────────────────────────
# 1. CONFIGURE YOUR HIGHLIGHTS HERE
#    Each group: { "label": str, "color": str, "countries": [list of country names] }
#    Country names must match Natural Earth data (see note below)
# ──────────────────────────────────────────────
HIGHLIGHT_GROUPS = [
    {
        "label": "Birdwatching Locations",
        "color": "#4a6741",   # forest green
        "countries": ["Canada", "United States of America", "Japan", "Germany", "Denmark", "Sweden", "Netherlands", "United Kingdom"],
    },
    # Add more groups as needed, e.g.:
    # {
    #     "label": "Another Group",
    #     "color": "#e05c2a",
    #     "countries": ["Brazil", "Argentina"],
    # },
]

# ──────────────────────────────────────────────
# 2. MAP STYLE SETTINGS
# ──────────────────────────────────────────────
MAP_TITLE        = "Sarah's Birdwatching Locales"
DEFAULT_COLOR    = "#d3d3d3"   # colour for non-highlighted countries
BORDER_COLOR     = "#bbbbbb"   # country border colour (now set directly in plot)
BORDER_WIDTH     = 0.4
BACKGROUND_COLOR = "#ffffff"   # figure background
OCEAN_COLOR      = "#f2f9ff"   # axes background (acts as ocean)
FIG_SIZE         = (18, 10)    # inches
DPI              = 150

OUTPUT_FILE = Path(__file__).parent / "Birdwatching_Locales.png"


# ──────────────────────────────────────────────
# 3. BUILD A LOOKUP: country name → (color, label)
# ──────────────────────────────────────────────
def build_highlight_lookup(groups):
    lookup = {}
    for group in groups:
        for country in group["countries"]:
            lookup[country] = {"color": group["color"], "label": group["label"]}
    return lookup


# ──────────────────────────────────────────────
# 4. DRAW THE MAP
# ──────────────────────────────────────────────
def draw_map():
    # Load Natural Earth 110m cultural vectors (countries with names).
    # geodatasets replaced the deprecated gpd.datasets removed in GeoPandas 1.0.
    # "naturalearth.land" only has land polygons (no country names), so we fetch
    # the cultural admin-0 shapefile directly from Natural Earth via URL.
    NE_URL = (
        "https://naciscdn.org/naturalearth/110m/cultural/"
        "ne_110m_admin_0_countries.zip"
    )
    world = gpd.read_file(NE_URL)

    lookup = build_highlight_lookup(HIGHLIGHT_GROUPS)

    # Assign a colour to every country row
    # Natural Earth admin-0 uses the column "NAME" for country names
    world["_color"] = world["NAME"].map(
        lambda name: lookup[name]["color"] if name in lookup else DEFAULT_COLOR
    )

    # ── Figure & axes ──
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    ax.set_facecolor(OCEAN_COLOR)

    # ── Drop Antarctica — saves a lot of vertical space ──
    world = world[world["NAME"] != "Antarctica"]

    # ── Plot countries ──
    world.plot(
        ax=ax,
        color=world["_color"],
        edgecolor="#bbbbbb",   # visible but subtle borders on all countries
        linewidth=0.4,
    )

    # ── Country name labels with auto-adjustment to reduce overlap ──
    # Some countries have centroids in water (archipelagos, fragmented coastlines).
    # Override their label position manually.
    CENTROID_OVERRIDES = {
        "Denmark":     (10.5, 56.0),   # Jutland peninsula
        "Netherlands": (5.3,  52.3),
        "Japan":       (136.0, 37.0),  # Honshu
    }

    texts = []
    for _, row in world.iterrows():
        centroid = row.geometry.centroid
        name = row["NAME"]
        is_highlighted = name in lookup
        x, y = CENTROID_OVERRIDES.get(name, (centroid.x, centroid.y))
        t = ax.text(
            x, y,
            row["ISO_A3_EH"],
            fontsize=6 if is_highlighted else 4,
            ha="center",
            va="center",
            color="#1a3a1a" if is_highlighted else "#666666",
            fontweight="bold" if is_highlighted else "normal",
            zorder=5 if is_highlighted else 3,
        )
        texts.append(t)

    adjust_text(
        texts,
        ax=ax,
        expand=(1.2, 1.4),
        force_text=(0.05, 0.1),
        max_move=6,
        only_move={"text": "xy", "static": "xy"},
    )

    # ── Legend ──
    legend_patches = [
        mpatches.Patch(color=g["color"], label=g["label"])
        for g in HIGHLIGHT_GROUPS
    ]
    ax.legend(
        handles=legend_patches,
        loc="lower left",
        fontsize=9,
        frameon=True,
        framealpha=0.9,
        edgecolor="#cccccc",
        title_fontsize=9,
    )

    # ── Title & cleanup ──
    ax.set_title(MAP_TITLE, fontsize=14, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=DPI, bbox_inches="tight")
    print(f"Saved as {OUTPUT_FILE}")
    plt.show()


if __name__ == "__main__":
    draw_map()