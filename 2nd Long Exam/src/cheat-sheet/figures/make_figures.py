"""Figures for the Topics 5-7 cheat sheet (graph identification galleries).

Run:  py make_figures.py     (writes the PDFs into this folder)
"""
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from m55plot import BLUE, GREEN, GREY, ORANGE, RED, plt, save, setup  # noqa: E402

setup()


# ---------------------------------------------------------------- helpers
def curve_panel(ax, f, t0, t1, title, n=1500, elev=22, azim=-60, arrows=True):
    t = np.linspace(t0, t1, n)
    x, y, z = f(t)
    ax.plot(x, y, z, color=BLUE, lw=1.3)
    # start point (dot) and direction of increasing t (arrow)
    ax.scatter([x[0]], [y[0]], [z[0]], color=RED, s=14, depthshade=False)
    if arrows:
        # first stretch of the curve drawn thick red = direction of increasing t
        m = max(n // 25, 8) if n < 3000 else n // 80
        ax.plot(x[:m], y[:m], z[:m], color=RED, lw=3.0)
    ax.set_title(title, fontsize=9, pad=0)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel("$x$", labelpad=-12, fontsize=8)
    ax.set_ylabel("$y$", labelpad=-12, fontsize=8)
    ax.set_zlabel("$z$", labelpad=-12, fontsize=8)
    ax.tick_params(labelsize=5, pad=-4)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_alpha(0.15)


def field_panel(ax, U, V, title, lim=2.0, n=9, normalize=False, scale=None,
                color=BLUE, skip_origin=False):
    g = np.linspace(-lim, lim, n)
    X, Y = np.meshgrid(g, g)
    if skip_origin:
        mask = np.hypot(X, Y) > 1e-9
        X, Y = X[mask], Y[mask]
    with np.errstate(divide="ignore", invalid="ignore"):
        u = U(X, Y) * np.ones_like(X)
        v = V(X, Y) * np.ones_like(X)
    if normalize:
        m = np.hypot(u, v)
        m[m == 0] = 1
        u, v = u / m * 0.35, v / m * 0.35
    ax.quiver(X, Y, u, v, color=color, angles="xy", scale_units="xy", scale=scale,
              width=0.011, headwidth=3.6, headlength=4.2, headaxislength=3.8, minlength=0.4)
    ax.set_aspect("equal")
    ax.set_xlim(-lim * 1.2, lim * 1.2)
    ax.set_ylim(-lim * 1.2, lim * 1.2)
    ax.axhline(0, color=GREY, lw=0.5)
    ax.axvline(0, color=GREY, lw=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=9)


# ---------------------------------------------------------------- curves
CURVES_1 = [
    (lambda t: (np.cos(t), np.sin(t), t), 0, 4 * np.pi,
     r"$\langle\cos t,\ \sin t,\ t\rangle$" + "\nhelix up the $z$-axis (CCW)"),
    (lambda t: (np.sin(t), np.cos(t), t), 0, 4 * np.pi,
     r"$\langle\sin t,\ \cos t,\ t\rangle$" + "\nsame helix, CW, starts $(0,1,0)$"),
    (lambda t: (t, np.cos(t), np.sin(t)), 0, 4 * np.pi,
     r"$\langle t,\ \cos t,\ \sin t\rangle$" + "\nhelix along the $x$-axis"),
    (lambda t: (2 * np.cos(t), np.sin(t), t), 0, 4 * np.pi,
     r"$\langle 2\cos t,\ \sin t,\ t\rangle$" + "\nelliptical helix"),
    (lambda t: (t * np.cos(t), t * np.sin(t), t), 0, 6 * np.pi,
     r"$\langle t\cos t,\ t\sin t,\ t\rangle$" + "\nconical helix (on a cone)"),
    (lambda t: (t * np.cos(t), t, t * np.sin(t)), 0, 6 * np.pi,
     r"$\langle t\cos t,\ t,\ t\sin t\rangle$" + "\ncone opening along $y$"),
]
CURVES_2 = [
    (lambda t: (1 + t, 2 + 5 * t, -1 + 6 * t), -1, 1,
     r"$\langle 1+t,\ 2+5t,\ -1+6t\rangle$" + "\nline (all linear in $t$)"),
    (lambda t: (t, t ** 2, t ** 3), -1.5, 1.5,
     r"$\langle t,\ t^2,\ t^3\rangle$" + "\ntwisted cubic"),
    (lambda t: (np.cos(t), np.sin(t), 2 - np.sin(t)), 0, 2 * np.pi,
     r"$\langle\cos t,\ \sin t,\ 2-\sin t\rangle$" + "\ntilted ellipse (cyl. $\\cap$ plane)"),
    (lambda t: (np.cos(t), np.sin(t), np.cos(2 * t)), 0, 2 * np.pi,
     r"$\langle\cos t,\ \sin t,\ \cos 2t\rangle$" + "\n``pringle'' (2 ups, 2 downs)"),
    (lambda t: (np.cos(t), np.sin(t), 1 / (1 + t ** 2)), -12, 12,
     r"$\langle\cos t,\ \sin t,\ \frac{1}{1+t^2}\rangle$" + "\ncircle with one bump"),
    (lambda t: (np.cos(8 * t), np.sin(8 * t), np.exp(0.8 * t)), 0, 3,
     r"$\langle\cos 8t,\ \sin 8t,\ e^{0.8t}\rangle$" + "\nhelix, coils spread apart"),
]
CURVES_3 = [
    (lambda t: (np.cos(t) ** 2, np.sin(t) ** 2, t), 0, 4 * np.pi,
     r"$\langle\cos^2 t,\ \sin^2 t,\ t\rangle$" + "\nzigzag in plane $x+y=1$"),
    (lambda t: (t, 1 / (1 + t ** 2), t ** 2), -2.5, 2.5,
     r"$\langle t,\ \frac{1}{1+t^2},\ t^2\rangle$" + "\nparabola with a bump"),
    (lambda t: (np.sin(3 * t) * np.cos(t), np.sin(3 * t) * np.sin(t), t), 0, 2 * np.pi,
     r"$\langle\sin 3t\cos t,\ \sin 3t\sin t,\ t\rangle$" + "\nrose petals stacked up"),
    (lambda t: (np.sin(t), np.cos(t), np.sin(t) ** 2), 0, 2 * np.pi,
     r"$\langle\sin t,\ \cos t,\ \sin^2 t\rangle$" + "\non the cylinder $z=x^2$"),
    (lambda t: ((4 + np.sin(20 * t)) * np.cos(t), (4 + np.sin(20 * t)) * np.sin(t),
                np.cos(20 * t)), 0, 2 * np.pi,
     "toroidal spiral\n(wraps around a donut)"),
    (lambda t: ((2 + np.cos(1.5 * t)) * np.cos(t), (2 + np.cos(1.5 * t)) * np.sin(t),
                np.sin(1.5 * t)), 0, 4 * np.pi,
     "trefoil knot\n($r=2+\\cos 1.5t,\\ \\theta=t$)"),
]


def fig_curves(name, curves):
    fig = plt.figure(figsize=(6.6, 4.9))
    for k, (f, a, b, title) in enumerate(curves):
        ax = fig.add_subplot(2, 3, k + 1, projection="3d")
        curve_panel(ax, f, a, b, title, n=4000 if "spiral" in title else 1500)
    fig.subplots_adjust(wspace=0.05, hspace=0.25)
    save(fig, HERE, name)


# ---------------------------------------------------------------- 2D fields
def r_(X, Y):
    return np.hypot(X, Y)


FIELDS = [
    (lambda X, Y: X, lambda X, Y: Y, r"$\langle x,y\rangle$: radial OUT, grows", {}),
    (lambda X, Y: -X, lambda X, Y: -Y, r"$\langle -x,-y\rangle$: radial IN, grows", {}),
    (lambda X, Y: -Y, lambda X, Y: X, r"$\langle -y,x\rangle$: rotates CCW", {}),
    (lambda X, Y: Y, lambda X, Y: -X, r"$\langle y,-x\rangle$: rotates CW", {}),
    (lambda X, Y: Y, lambda X, Y: X, r"$\langle y,x\rangle$: saddle (hyperbolas)", {}),
    (lambda X, Y: X, lambda X, Y: -Y, r"$\langle x,-y\rangle$: saddle (other way)", {}),
    (lambda X, Y: 1 + 0 * X, lambda X, Y: 2 + 0 * X, r"$\langle 1,2\rangle$: constant", {"scale": 7}),
    (lambda X, Y: Y, lambda X, Y: 0 * X, r"$\langle y,0\rangle$: shear (rows)", {}),
    (lambda X, Y: 0 * X, lambda X, Y: X, r"$\langle 0,x\rangle$: shear (columns)", {}),
    (lambda X, Y: 1 + 0 * X, lambda X, Y: np.sin(Y), r"$\langle 1,\sin y\rangle$: all point right", {"lim": 3, "scale": 2.6, "n": 8}),
    (lambda X, Y: -X / r_(X, Y), lambda X, Y: -Y / r_(X, Y),
     r"$-\mathbf{x}/|\mathbf{x}|$: IN, all length 1", {"skip_origin": True, "scale": 3.2}),
    (lambda X, Y: -X / r_(X, Y) * np.minimum(1 / r_(X, Y) ** 2, 1.8),
     lambda X, Y: -Y / r_(X, Y) * np.minimum(1 / r_(X, Y) ** 2, 1.8),
     r"$-\mathbf{x}/|\mathbf{x}|^3$: IN, big near 0", {"skip_origin": True, "scale": 4}),
]


def fig_fields():
    fig, axes = plt.subplots(3, 4, figsize=(6.8, 5.6))
    for ax, (U, V, title, kw) in zip(axes.flat, FIELDS):
        kw = dict(kw)
        scale = kw.pop("scale", 5.5)
        field_panel(ax, U, V, None, scale=scale, n=kw.pop("n", 9), **kw)
        ax.set_title(title, fontsize=7.5)
    fig.subplots_adjust(wspace=0.08, hspace=0.25)
    save(fig, HERE, "fields_gallery")


# ---------------------------------------------------------------- 3D fields (slides Exercise 3)
def fig_fields3d():
    fig = plt.figure(figsize=(6.8, 2.1))
    specs = [
        (lambda X, Y, Z: (1 + 0 * X, 2 + 0 * X, 3 + 0 * X), r"$\langle 1,2,3\rangle$: all parallel"),
        (lambda X, Y, Z: (1 + 0 * X, 2 + 0 * X, Z), r"$\langle 1,2,z\rangle$: up top, down bottom"),
        (lambda X, Y, Z: (X, Y, 3 + 0 * X), r"$\langle x,y,3\rangle$: all up, fan out"),
        (lambda X, Y, Z: (X, Y, Z), r"$\langle x,y,z\rangle$: radial out"),
    ]
    g = np.linspace(-1, 1, 3)
    X, Y, Z = np.meshgrid(g, g, g)
    for k, (F, title) in enumerate(specs):
        ax = fig.add_subplot(1, 4, k + 1, projection="3d")
        U, V, W = F(X, Y, Z)
        ax.quiver(X, Y, Z, U, V, W, length=0.22, color=BLUE, linewidth=0.8,
                  arrow_length_ratio=0.35)
        ax.set_title(title, fontsize=7.5, pad=0)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_xlabel("$x$", labelpad=-14, fontsize=7)
        ax.set_ylabel("$y$", labelpad=-14, fontsize=7)
        ax.set_zlabel("$z$", labelpad=-14, fontsize=7)
        ax.view_init(elev=18, azim=-55)
    fig.subplots_adjust(wspace=0.0)
    save(fig, HERE, "fields3d_gallery")


# ---------------------------------------------------------------- level curves + gradient
def fig_contours():
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.5))
    specs = [
        (lambda X, Y: X ** 2 + Y ** 2, lambda X, Y: (2 * X, 2 * Y),
         r"$f=x^2+y^2$: circles, $\nabla f$ points OUT"),
        (lambda X, Y: X ** 2 - Y ** 2, lambda X, Y: (2 * X, -2 * Y),
         r"$f=x^2-y^2$: hyperbolas"),
        (lambda X, Y: X + 2 * Y, lambda X, Y: (1 + 0 * X, 2 + 0 * X),
         r"$f=x+2y$: lines, $\nabla f=\langle1,2\rangle$"),
    ]
    g = np.linspace(-2, 2, 200)
    GX, GY = np.meshgrid(g, g)
    q = np.linspace(-1.6, 1.6, 5)
    QX, QY = np.meshgrid(q, q)
    for ax, (f, gr, title) in zip(axes, specs):
        cs = ax.contour(GX, GY, f(GX, GY), levels=9, colors=GREY, linewidths=0.6)
        U, V = gr(QX, QY)
        ax.quiver(QX, QY, U, V, color=RED, angles="xy", scale_units="xy", scale=6,
                  width=0.008)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(title, fontsize=7.5)
    save(fig, HERE, "contours_gradient")


# ---------------------------------------------------------------- drills
def label(ax, s):
    ax.text(0.03, 0.97, s, transform=ax.transAxes, fontsize=11, fontweight="bold",
            va="top", ha="left", bbox=dict(fc="white", ec="none", pad=1))


def fig_drill_curves():
    """Drill: r(t)=<t cos t, t sin t, t> among 4 curves (A conical along z is correct = C)."""
    fig = plt.figure(figsize=(6.6, 2.0))
    opts = [
        (lambda t: (np.cos(t), np.sin(t), t), 0, 4 * np.pi),
        (lambda t: (t, t ** 2, t ** 3), -1.5, 1.5),
        (lambda t: (t * np.cos(t), t * np.sin(t), t), 0, 6 * np.pi),
        (lambda t: (np.cos(t), np.sin(t), np.cos(2 * t)), 0, 2 * np.pi),
    ]
    for k, (f, a, b) in enumerate(opts):
        ax = fig.add_subplot(1, 4, k + 1, projection="3d")
        curve_panel(ax, f, a, b, "ABCD"[k], arrows=False)
    save(fig, HERE, "drill_curves")


def fig_drill_curves2():
    """Drill: <cos t, sin t, 2 - sin t> vs lookalikes. Correct = B."""
    fig = plt.figure(figsize=(6.6, 2.0))
    opts = [
        (lambda t: (np.cos(t), np.sin(t), 2 + 0 * t), 0, 2 * np.pi),
        (lambda t: (np.cos(t), np.sin(t), 2 - np.sin(t)), 0, 2 * np.pi),
        (lambda t: (np.cos(t), np.sin(t), 2 - np.cos(t)), 0, 2 * np.pi),
        (lambda t: (np.cos(t), np.sin(t), np.cos(2 * t) + 2), 0, 2 * np.pi),
    ]
    for k, (f, a, b) in enumerate(opts):
        ax = fig.add_subplot(1, 4, k + 1, projection="3d")
        curve_panel(ax, f, a, b, "ABCD"[k], arrows=False, elev=20, azim=-62)
        ax.set_zlim(0.5, 3.5)
    save(fig, HERE, "drill_curves2")


def fig_drill_fields():
    """Drill: four 2D fields labelled I-IV.  I=<y,-x> II=<x,-y> III=<-x,-y> IV=<1,x>."""
    fig, axes = plt.subplots(1, 4, figsize=(6.8, 1.9))
    opts = [
        (lambda X, Y: Y, lambda X, Y: -X),
        (lambda X, Y: X, lambda X, Y: -Y),
        (lambda X, Y: -X, lambda X, Y: -Y),
        (lambda X, Y: 1 + 0 * X, lambda X, Y: X),
    ]
    for k, (ax, (U, V)) in enumerate(zip(axes, opts)):
        field_panel(ax, U, V, None, n=7, scale=4.5)
        label(ax, ["I", "II", "III", "IV"][k])
    save(fig, HERE, "drill_fields")


def fig_drill_gradient():
    """Drill: which plot is grad f for f = x^2 y ?  grad f = <2xy, x^2>. Correct = C."""
    fig, axes = plt.subplots(1, 4, figsize=(6.8, 1.9))
    opts = [
        (lambda X, Y: 2 * X, lambda X, Y: 2 * Y),            # grad of x^2+y^2
        (lambda X, Y: X ** 2, lambda X, Y: 2 * X * Y),       # swapped
        (lambda X, Y: 2 * X * Y, lambda X, Y: X ** 2),       # correct
        (lambda X, Y: -2 * X * Y, lambda X, Y: -X ** 2),     # negative
    ]
    for k, (ax, (U, V)) in enumerate(zip(axes, opts)):
        field_panel(ax, U, V, None, lim=1.5, n=7, normalize=True, scale=1)
        label(ax, "ABCD"[k])
    save(fig, HERE, "drill_gradient")


def fig_drill_contour():
    """Drill: contour map with points P, Q; read sign of directional derivatives."""
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    g = np.linspace(-3, 3, 300)
    X, Y = np.meshgrid(g, g)
    Zf = 10 - X ** 2 - 2 * Y ** 2
    cs = ax.contour(X, Y, Zf, levels=[-6, -2, 2, 6, 8], colors=GREY, linewidths=0.8)
    ax.clabel(cs, fontsize=7, fmt="%d")
    for (px, py, s) in [(2, 0, "P"), (0, 1.2, "Q")]:
        ax.plot(px, py, "o", color=RED, ms=4)
        ax.text(px + 0.12, py + 0.12, s, fontsize=10, color=RED)
    ax.set_aspect("equal")
    ax.axhline(0, color=GREY, lw=0.4); ax.axvline(0, color=GREY, lw=0.4)
    ax.set_xticks([-2, 0, 2]); ax.set_yticks([-2, 0, 2])
    save(fig, HERE, "drill_contour")


if __name__ == "__main__":
    fig_curves("curves_gallery_1", CURVES_1)
    fig_curves("curves_gallery_2", CURVES_2)
    fig_curves("curves_gallery_3", CURVES_3)
    fig_fields()
    fig_fields3d()
    fig_contours()
    fig_drill_curves()
    fig_drill_curves2()
    fig_drill_fields()
    fig_drill_gradient()
    fig_drill_contour()
