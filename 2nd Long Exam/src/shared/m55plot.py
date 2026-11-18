"""Shared matplotlib style for the MATH 55 reviewer figures.

Every figure script does

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "shared"))
    from m55plot import setup, save

so that all figures use Computer-Modern-like fonts that match the
Latin Modern text of the notes, and are written as vector PDFs.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Muted palette that prints well in greyscale
BLUE = "#1f4e79"
RED = "#b22222"
GREEN = "#2e7d32"
ORANGE = "#d2691e"
GREY = "#555555"


def setup():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["cmr10", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "axes.formatter.use_mathtext": True,
        "axes.unicode_minus": False,
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.linewidth": 0.7,
        "lines.linewidth": 1.4,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "pdf.fonttype": 42,
    })


def save(fig, outdir, name):
    out = Path(outdir) / f"{name}.pdf"
    fig.savefig(out)
    plt.close(fig)
    print("wrote", out.name)


def centre_axes(ax):
    """Draw x/y axes through the origin, textbook style."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_color(GREY)
    ax.spines["bottom"].set_color(GREY)
