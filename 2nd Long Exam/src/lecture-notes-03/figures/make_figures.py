"""Figures for Lecture Notes & Reviewer No. 7 (vector calculus).

Run:  python make_figures.py     (writes the PDFs into this folder)
"""
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from m55plot import BLUE, GREEN, GREY, ORANGE, RED, plt, save, setup  # noqa: E402

setup()
BOX = dict(fc="white", ec="none", alpha=0.9, pad=1.2)


def quiver_field(ax, U, V, lim=2.0, n=11, scale=None, color=BLUE, normalize=False):
    g = np.linspace(-lim, lim, n)
    X, Y = np.meshgrid(g, g)
    u, v = U(X, Y), V(X, Y)
    if normalize:
        m = np.hypot(u, v)
        m[m == 0] = 1
        u, v = u / m, v / m
    ax.quiver(X, Y, u, v, color=color, angles="xy", scale_units="xy", scale=scale,
              width=0.006, headwidth=4, headlength=5)
    ax.set_aspect("equal")
    ax.set_xlim(-lim * 1.15, lim * 1.15)
    ax.set_ylim(-lim * 1.15, lim * 1.15)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)


def fig_rotation():
    """Example 7.1: F = <-y, x>, arrows tangent to circles, |F| = r."""
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    th = np.linspace(0, 2 * np.pi, 200)
    for r in (1, 2, 3):
        ax.plot(r * np.cos(th), r * np.sin(th), color=GREY, lw=0.6, ls="--")
    pts = []
    for r in (1, 2, 3):
        for k in range(8 if r > 1 else 4):
            a = 2 * np.pi * k / (8 if r > 1 else 4) + (np.pi / 8 if r == 2 else 0)
            pts.append((r * np.cos(a), r * np.sin(a)))
    P = np.array(pts)
    ax.quiver(P[:, 0], P[:, 1], -P[:, 1], P[:, 0], angles="xy", scale_units="xy",
              scale=2.2, color=RED, width=0.007)
    ax.set_aspect("equal")
    ax.set_xlim(-4.4, 4.4)
    ax.set_ylim(-4.4, 4.4)
    ax.axhline(0, color=GREY, lw=0.6)
    ax.axvline(0, color=GREY, lw=0.6)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    save(fig, HERE, "rotation_field")


def fig_exercise1():
    """Slides Exercise 1: F = y i + (1/2)(y - x) j at the nine lattice points."""
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    for X in (-1, 0, 1):
        for Y in (-1, 0, 1):
            u, v = Y, 0.5 * (Y - X)
            ax.plot(X, Y, "o", color=BLUE, ms=4)
            if u or v:
                ax.annotate("", xy=(X + u, Y + v), xytext=(X, Y),
                            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4))
    ax.set_aspect("equal")
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([-2, -1, 0, 1, 2])
    ax.grid(alpha=0.3)
    ax.axhline(0, color=GREY, lw=0.7)
    ax.axvline(0, color=GREY, lw=0.7)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    save(fig, HERE, "exercise1")


def fig_exercise2():
    """Slides Exercise 2: the four fields, laid out like the slide."""
    fields = [
        (r"top left: $\mathbf{F}=-\dfrac{\langle x,y\rangle}{\sqrt{x^2+y^2}}$ (D)",
         lambda X, Y: -X / np.maximum(np.hypot(X, Y), 1e-9),
         lambda X, Y: -Y / np.maximum(np.hypot(X, Y), 1e-9), 3.5),
        (r"top right: $\mathbf{F}=\langle-\frac{1}{2},\frac{1}{2}\rangle$ (A)",
         lambda X, Y: -0.5 + 0 * X, lambda X, Y: 0.5 + 0 * Y, 1.6),
        (r"bottom left: $\mathbf{F}=\langle\frac{x}{2},\frac{y}{2}\rangle$ (B)",
         lambda X, Y: X / 2, lambda X, Y: Y / 2, 2.5),
        (r"bottom right: $\mathbf{F}=\langle 1,\sin y\rangle$ (C)",
         lambda X, Y: 1 + 0 * X, lambda X, Y: np.sin(Y), 2.2),
    ]
    fig, axs = plt.subplots(2, 2, figsize=(6.4, 6.6))
    for ax, (title, U, V, sc) in zip(axs.flat, fields):
        quiver_field(ax, U, V, lim=3, n=9, scale=sc)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, HERE, "exercise2")


def fig_exercise3():
    """Slides Exercise 3: F = <x, y, 3> in space."""
    fig = plt.figure(figsize=(4.8, 4.2))
    ax = fig.add_subplot(projection="3d")
    g = np.linspace(-1, 1, 4)
    X, Y, Z = np.meshgrid(g, g, np.array([-1.0, 0.0, 1.0]))
    ax.quiver(X, Y, Z, X, Y, 3 + 0 * Z, length=0.25, normalize=False, color=BLUE, lw=0.8)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.view_init(elev=15, azim=-60)
    save(fig, HERE, "exercise3")


def fig_computer():
    """The three computer-generated fields shown on the slides."""
    specs = [
        (r"$\langle -y,\,x\rangle$", lambda X, Y: -Y, lambda X, Y: X, 5),
        (r"$\langle y,\,\sin x\rangle$", lambda X, Y: Y, lambda X, Y: np.sin(X), 6),
        (r"$\langle \ln(1+y^2),\,\ln(1+x^2)\rangle$", lambda X, Y: np.log(1 + Y**2),
         lambda X, Y: np.log(1 + X**2), 5),
    ]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.7))
    for ax, (title, U, V, lim) in zip(axs, specs):
        quiver_field(ax, U, V, lim=lim, n=11, scale=None)
        ax.set_title(title, fontsize=9)
        ax.tick_params(labelsize=7)
    fig.tight_layout()
    save(fig, HERE, "computer_fields")


def fig_gradient_field():
    """Example 7.2: grad(x^2 y - y^3) over the contour map."""
    fig, ax = plt.subplots(figsize=(4.8, 4.6))
    g = np.linspace(-2, 2, 300)
    X, Y = np.meshgrid(g, g)
    F = X**2 * Y - Y**3
    cs = ax.contour(X, Y, F, levels=[-3, -1.5, -0.5, 0, 0.5, 1.5, 3], colors=GREY,
                    linewidths=0.7, linestyles="solid")
    ax.clabel(cs, fontsize=6, fmt="%g")
    q = np.linspace(-1.8, 1.8, 10)
    QX, QY = np.meshgrid(q, q)
    ax.quiver(QX, QY, 2 * QX * QY, QX**2 - 3 * QY**2, color=RED, angles="xy",
              scale_units="xy", scale=28, width=0.005)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    save(fig, HERE, "gradient_field")


def fig_gravity():
    """Inverse-square field F = -x/|x|^3 (shape of gravity), in space."""
    fig = plt.figure(figsize=(4.6, 4.2))
    ax = fig.add_subplot(projection="3d")
    g = np.array([-2.0, -1.0, 1.0, 2.0])
    X, Y, Z = np.meshgrid(g, g, g)
    R = np.sqrt(X**2 + Y**2 + Z**2)
    ax.quiver(X, Y, Z, -X / R**3, -Y / R**3, -Z / R**3, length=2.2, color=BLUE, lw=0.8)
    ax.scatter([0], [0], [0], color="k", s=25)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    ax.view_init(elev=18, azim=-55)
    save(fig, HERE, "gravity_field")


def fig_matching_practice():
    """Practice matching problem: panels I-IV (answers in the solution)."""
    specs = [
        ("I", lambda X, Y: X, lambda X, Y: -Y),
        ("II", lambda X, Y: Y, lambda X, Y: -X),
        ("III", lambda X, Y: Y, lambda X, Y: 0 * X),
        ("IV", lambda X, Y: 2 + 0 * X, lambda X, Y: 1 + 0 * Y),
    ]
    fig, axs = plt.subplots(1, 4, figsize=(7.6, 2.2))
    for ax, (lab, U, V) in zip(axs, specs):
        quiver_field(ax, U, V, lim=2, n=7, scale=None)
        ax.set_title(lab, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, HERE, "matching_practice")


def fig_vortex():
    """F = <-y, x>/(x^2+y^2): curl-free but not conservative on the punctured plane."""
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    g = np.linspace(-2, 2, 11)
    X, Y = np.meshgrid(g, g)
    R2 = X**2 + Y**2
    R2[R2 == 0] = np.nan
    U, V = -Y / R2, X / R2
    mag = np.hypot(U, V)
    cap = np.minimum(mag, 1.6) / mag          # cap the huge arrows near the origin
    ax.quiver(X, Y, U * cap, V * cap, color=BLUE, angles="xy", scale_units="xy", scale=3.2,
              width=0.005)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=RED, lw=1.5)
    ax.plot([0], [0], "o", mfc="white", mec="k", ms=6)
    ax.text(0.55, -1.25, r"$\theta$ gains $2\pi$", color=RED, fontsize=9, bbox=BOX)
    ax.set_aspect("equal")
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.3, 2.3)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    save(fig, HERE, "vortex")


if __name__ == "__main__":
    fig_rotation()
    fig_exercise1()
    fig_exercise2()
    fig_exercise3()
    fig_computer()
    fig_gradient_field()
    fig_gravity()
    fig_matching_practice()
    fig_vortex()
