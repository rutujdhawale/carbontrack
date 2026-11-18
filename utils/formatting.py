"""Formatting utilities for CarbonTrack dashboard."""
from typing import Optional

# Brand color palette (from design spec)
BG_COLOR = "#F6F5F0"
SURFACE_COLOR = "#FFFFFF"
TEXT_COLOR = "#20231F"
MUTED_COLOR = "#777B72"
GREEN = "#356B4A"
LIGHT_GREEN = "#E6EEE7"
TERRACOTTA = "#B66A4A"
BORDER_COLOR = "#E4E2DA"

# Plotly categorical palette (adapted from dataviz skill)
PLOTLY_PALETTE = {
    "series_1": "#356B4A",   # Green - primary
    "series_2": "#B66A4A",   # Terracotta - secondary
    "series_3": "#2a78d6",   # Blue - tertiary
    "series_4": "#eb6834",   # Orange - quaternary
    "series_5": "#1baf7a",   # Aqua - quinary
}

# Status colors
STATUS_GOOD = "#0ca30c"
STATUS_WARNING = "#fab219"
STATUS_SERIOUS = "#ec835a"
STATUS_CRITICAL = "#d03b3b"

# Chart surface
CHART_SURFACE = "#FFFFFF"
GRIDLINE = "#E1E0D9"
BASELINE = "#C3C2B7"
PRIMARY_INK = "#20231F"
SECONDARY_INK = "#52514E"
MUTED_INK = "#898781"


def format_number(value: float, decimals: int = 0) -> str:
    """Format a number with commas and specified decimal places."""
    if value is None:
        return "N/A"
    try:
        return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"


def format_area(value: float) -> str:
    """Format area in hectares."""
    return f"{format_number(value, 0)} ha"


def format_production(value: float) -> str:
    """Format production in metric tons."""
    return f"{format_number(value, 0)} t"


def format_yield(value: float) -> str:
    """Format yield in t/ha."""
    return f"{format_number(value, 2)} t/ha"


def get_status_color(status: str) -> str:
    """Get color for a status string."""
    status_map = {
        "High Priority": STATUS_SERIOUS,
        "Moderate Priority": STATUS_WARNING,
        "Good": STATUS_GOOD,
        "Warning": STATUS_WARNING,
        "Serious": STATUS_SERIOUS,
        "Critical": STATUS_CRITICAL,
    }
    return status_map.get(status, MUTED_COLOR)


def get_plotly_layout(**kwargs) -> dict:
    """Return a consistent Plotly layout dictionary."""
    base_layout = {
        "paper_bgcolor": CHART_SURFACE,
        "plot_bgcolor": CHART_SURFACE,
        "font": {
            "family": "system-ui, -apple-system, Segoe UI, sans-serif",
            "color": PRIMARY_INK,
            "size": 12,
        },
        "margin": {"l": 60, "r": 30, "t": 40, "b": 50},
        "xaxis": {
            "gridcolor": GRIDLINE,
            "linecolor": BASELINE,
            "tickfont": {"color": MUTED_INK, "size": 11},
            "title": {"font": {"color": SECONDARY_INK, "size": 12}},
        },
        "yaxis": {
            "gridcolor": GRIDLINE,
            "linecolor": BASELINE,
            "tickfont": {"color": MUTED_INK, "size": 11},
            "title": {"font": {"color": SECONDARY_INK, "size": 12}},
        },
        "legend": {
            "font": {"color": SECONDARY_INK, "size": 11},
            "bgcolor": "rgba(0,0,0,0)",
        },
        "hovermode": "x unified",
        "hoverlabel": {
            "bgcolor": PRIMARY_INK,
            "font": {"color": "#FFFFFF", "size": 11},
        },
    }
    base_layout.update(kwargs)
    return base_layout


def apply_brand_theme(fig):
    """Apply brand theme to a Plotly figure."""
    fig.update_layout(**get_plotly_layout())
    return fig