"""Figures for Lecture Notes & Reviewer No. 6 (directional derivatives, gradient).

Run:  python make_figures.py     (writes the PDFs into this folder)
"""
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from m55plot import BLUE, GREEN, GREY, ORANGE, RED, plt, save, setup  # noqa: E402

setup()


# ---------------------------------------------------------------------
# f(x,y) = 4 - x^2 - y^2/4  (Slides, Example 6.1) -- used several times
# ---------------------------------------------------------------------
def f61(x, y):
    return 4 - x**2 - y**2 / 4


def fig_surface_slice():
    """Surface, vertical plane through P in direction u, the cut curve and
    its tangent line whose slope is D_u f(1,2) = -1 - sqrt(3)/2."""
    fig = plt.figure(figsize=(6.2, 4.6))
    ax = fig.add_subplot(projection="3d")
    X, Y = np.meshgrid(np.linspace(-2, 2, 60), np.linspace(-3.2, 3.2, 60))
    Z = f61(X, Y)
    Z = np.where(Z < -1.5, np.nan, Z)
    ax.plot_surface(X, Y, Z, cmap="Blues", alpha=0.35, linewidth=0,
                    antialiased=True, rstride=2, cstride=2)

    x0, y0 = 1.0, 2.0
    a, b = np.cos(np.pi / 3), np.sin(np.pi / 3)
    s = np.linspace(-2.2, 1.0, 100)
    # curve of intersection with the vertical plane
    cx, cy = x0 + s * a, y0 + s * b
    ax.plot(cx, cy, f61(cx, cy), color=RED, lw=2.2, label="cut by vertical plane")
    # tangent line
    slope = -1 - np.sqrt(3) / 2
    s2 = np.linspace(-0.9, 0.9, 10)
    ax.plot(x0 + s2 * a, y0 + s2 * b, f61(x0, y0) + slope * s2, color="k", lw=1.6,
            label=r"tangent line, slope $D_{\mathbf{u}}f(1,2)$")
    # vertical plane (translucent)
    S, W = np.meshgrid(np.linspace(-2.2, 1.0, 2), np.linspace(-1.5, 4.5, 2))
    ax.plot_surface(x0 + S * a, y0 + S * b, W, color=ORANGE, alpha=0.15, linewidth=0)
    # the point and the direction u drawn in the xy-plane (z = -1.5)
    ax.scatter([x0], [y0], [f61(x0, y0)], color="k", s=18)
    ax.plot([x0, x0], [y0, y0], [-1.5, f61(x0, y0)], color=GREY, ls=":", lw=1)
    ax.quiver(x0, y0, -1.5, a, b, 0, color=GREEN, lw=2, arrow_length_ratio=0.25)
    ax.text(x0 + a + 0.1, y0 + b, -1.5, r"$\mathbf{u}$", color=GREEN)
    ax.text(x0 + 0.1, y0, f61(x0, y0) + 0.35, r"$P(1,2,2)$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_zlim(-1.5, 4.5)
    ax.view_init(elev=18, azim=150)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
    save(fig, HERE, "surface_slice")


def fig_contour_gradient():
    """Level curves of f61 with gradient vectors; tangent line at (1,2)."""
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    X, Y = np.meshgrid(np.linspace(-2.5, 2.5, 300), np.linspace(-4, 4, 300))
    cs = ax.contour(X, Y, f61(X, Y), levels=[-2, -1, 0, 1, 2, 3, 3.75],
                    colors=BLUE, linewidths=0.9, linestyles="solid")
    ax.clabel(cs, fontsize=7, fmt="%g")
    pts = [(1, 2), (-1.2, 1.5), (1.5, -1), (-1, -2.5), (0.6, 3.0), (-1.8, 0.4), (1.9, 1.2)]
    for (px, py) in pts:
        gx, gy = -2 * px, -py / 2
        ax.annotate("", xy=(px + 0.35 * gx, py + 0.35 * gy), xytext=(px, py),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.3))
        ax.plot(px, py, "o", color="k", ms=2.5)
    xs = np.linspace(0.2, 1.9, 2)
    ax.plot(xs, 4 - 2 * xs, color=GREEN, lw=1.3, ls="--")
    box = dict(fc="white", ec="none", alpha=0.9, pad=1.2)
    ax.text(1.12, 2.12, r"$(1,2)$", fontsize=9, bbox=box)
    ax.text(0.55, -0.55, r"tangent line $2x+y=4$", color=GREEN, fontsize=8, bbox=box)
    ax.text(-2.35, 3.55, r"$\nabla f(1,2)=\langle -2,-1\rangle$", color=RED, fontsize=8, bbox=box)
    ax.set_aspect("equal")
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-4, 4)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.grid(alpha=0.2)
    save(fig, HERE, "contour_gradient")


def fig_trio():
    """Trio activity: f = 200 exp(-x^2-3y^2), P(4,-1), Q(7,3).
    PQ is tangent to the level curve x^2+3y^2 = 19 through P, so D_u f(P) = 0."""
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    X, Y = np.meshgrid(np.linspace(-6, 8, 400), np.linspace(-4, 4.5, 400))
    ax.contour(X, Y, X**2 + 3 * Y**2, levels=[4, 9, 19, 30, 45], colors=BLUE,
               linewidths=0.8, linestyles="-")
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.sqrt(19) * np.cos(th), np.sqrt(19 / 3) * np.sin(th), color=BLUE, lw=2)
    ax.annotate("", xy=(7, 3), xytext=(4, -1),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.6))
    ax.annotate("", xy=(4 - 1.6, -1 + 1.2), xytext=(4, -1),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6))
    ax.plot([4, 7], [-1, 3], "o", color="k", ms=3)
    ax.text(4.15, -1.45, r"$P(4,-1)$", fontsize=9)
    ax.text(7.1, 3.0, r"$Q(7,3)$", fontsize=9)
    ax.text(5.9, 0.6, r"$\overrightarrow{PQ}=\langle 3,4\rangle$", color=GREEN, fontsize=9)
    ax.text(0.9, 0.4, r"$\nabla f(P)\parallel\langle -4,3\rangle$", color=RED, fontsize=9)
    ax.text(-5.9, 3.7, r"level curve $x^2+3y^2=19$ (where $f=200e^{-19}$)", color=BLUE, fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.grid(alpha=0.2)
    save(fig, HERE, "trio_activity")


def fig_du_theta():
    """D_u f(2,0) for f = x e^y as a function of the angle of u."""
    th = np.linspace(0, 2 * np.pi, 400)
    d = np.cos(th) + 2 * np.sin(th)
    th0 = np.arctan2(2, 1)
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.plot(th, d, color=BLUE)
    ax.axhline(0, color=GREY, lw=0.7)
    for yv, lab in [(np.sqrt(5), r"$\|\nabla f\|=\sqrt{5}$"), (-np.sqrt(5), r"$-\|\nabla f\|$")]:
        ax.axhline(yv, color=RED, lw=0.8, ls="--")
        ax.text(6.35, yv, lab, color=RED, fontsize=8, va="center")
    ax.plot([th0], [np.sqrt(5)], "o", color=RED, ms=4)
    ax.plot([th0 + np.pi], [-np.sqrt(5)], "o", color=RED, ms=4)
    for z0 in (th0 + np.pi / 2, th0 + 3 * np.pi / 2):
        ax.plot([z0], [0], "o", color=GREEN, ms=4)
    ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    ax.set_xticklabels(["$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_xlabel(r"angle $\theta$ of $\mathbf{u}=\langle\cos\theta,\sin\theta\rangle$")
    ax.set_ylabel(r"$D_{\mathbf{u}}f(2,0)$")
    ax.set_xlim(0, 2 * np.pi)
    save(fig, HERE, "du_vs_theta")


def fig_ellipsoid():
    """Ellipsoid x^2/4 + y^2 + z^2/9 = 3, tangent plane and normal at (-2,1,-3)."""
    fig = plt.figure(figsize=(5.6, 4.8))
    ax = fig.add_subplot(projection="3d")
    u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 50), np.linspace(0, np.pi, 30))
    r = np.sqrt(3)
    ax.plot_surface(2 * r * np.cos(u) * np.sin(v), r * np.sin(u) * np.sin(v),
                    3 * r * np.cos(v), color=BLUE, alpha=0.25, linewidth=0)
    p = np.array([-2.0, 1.0, -3.0])
    n = np.array([-1.0, 2.0, -2.0 / 3.0])
    # tangent plane 3x - 6y + 2z + 18 = 0  ->  z = (-18 - 3x + 6y)/2
    e1 = np.array([2.0, 1.0, 0.0]) / np.sqrt(5)          # tangent directions
    e2 = np.cross(n, e1); e2 /= np.linalg.norm(e2)
    S, T = np.meshgrid(np.linspace(-1.6, 1.6, 2), np.linspace(-1.6, 1.6, 2))
    PX, PY, PZ = (p[i] + S * e1[i] + T * e2[i] for i in range(3))
    ax.plot_surface(PX, PY, PZ, color=ORANGE, alpha=0.45, linewidth=0)
    ax.scatter(*p, color="k", s=16)
    ax.quiver(*p, *(1.2 * n), color=RED, lw=2, arrow_length_ratio=0.2)
    ax.text(*(p + 1.1 * n + np.array([0.0, 0.0, 0.5])), r"$\nabla F$", color=RED, fontsize=10)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.set_box_aspect((2 * r, r, 3 * r))
    ax.view_init(elev=-6, azim=50)
    save(fig, HERE, "ellipsoid_tangent_plane")


def fig_steepest():
    """Steepest-ascent path y = 2 x^{1/4} on the contour map of f61, from (1,2)."""
    fig, ax = plt.subplots(figsize=(5.0, 4.6))
    X, Y = np.meshgrid(np.linspace(-0.3, 2.2, 300), np.linspace(-0.3, 3.2, 300))
    cs = ax.contour(X, Y, f61(X, Y), levels=[0, 1, 2, 3, 3.5, 3.9], colors=BLUE, linewidths=0.8)
    ax.clabel(cs, fontsize=7, fmt="%g")
    xs = np.linspace(1e-4, 1, 300)
    ax.plot(xs, 2 * xs**0.25, color=RED, lw=2)
    for xm in (0.6, 0.15):
        ym = 2 * xm**0.25
        ax.annotate("", xy=(xm - 0.05, 2 * (xm - 0.05) ** 0.25), xytext=(xm, ym),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.plot([1], [2], "o", color="k", ms=3.5)
    ax.plot([0], [0], "o", color="k", ms=3.5)
    ax.text(1.05, 2.05, "start $(1,2)$", fontsize=9)
    ax.text(0.05, -0.22, "summit $(0,0)$", fontsize=9)
    ax.text(0.25, 2.75, r"path $y=2x^{1/4}$", color=RED, fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.grid(alpha=0.2)
    save(fig, HERE, "steepest_ascent")


if __name__ == "__main__":
    fig_surface_slice()
    fig_contour_gradient()
    fig_trio()
    fig_du_theta()
    fig_ellipsoid()
    fig_steepest()
