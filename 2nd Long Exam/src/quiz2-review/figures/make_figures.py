"""Figures for the Quiz 2 review.  Run:  python make_figures.py"""
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from m55plot import BLUE, GREEN, GREY, RED, plt, save, setup  # noqa: E402

setup()


def fig_great_circle():
    """Quiz 2, Problem 1: sphere x^2+y^2+z^2=25 cut by the plane 3x-4z=0."""
    fig = plt.figure(figsize=(5.4, 4.8))
    ax = fig.add_subplot(projection="3d")
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 20))
    ax.plot_wireframe(5 * np.cos(u) * np.sin(v), 5 * np.sin(u) * np.sin(v), 5 * np.cos(v),
                      color=GREY, lw=0.25, alpha=0.5)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(4 * np.cos(t), 5 * np.sin(t), 3 * np.cos(t), color=BLUE, lw=1.4)
    tq = np.linspace(0, np.pi / 2, 100)
    ax.plot(4 * np.cos(tq), 5 * np.sin(tq), 3 * np.cos(tq), color=RED, lw=3,
            label=r"arc $P\to Q$, length $5\pi/2$")
    ax.scatter([4, 0], [0, 5], [3, 0], color="k", s=18)
    ax.text(4.3, 0, 3.4, "$P(4,0,3)$")
    ax.text(0, 5.4, 0.3, "$Q(0,5,0)$")
    s = np.linspace(-0.9, 0.9, 2)
    ax.plot(4 + 0 * s, 5 * s, 3 + 0 * s, color=GREEN, lw=1.8, label="tangent line at $P$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=15)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    save(fig, HERE, "great_circle")


if __name__ == "__main__":
    fig_great_circle()
