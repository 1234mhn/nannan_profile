"""Shared helpers for fig1_route.py / fig2_model.py (1 data unit = 1 cm). 黑白灰 + 深蓝/暗红强调。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon
from scipy.ndimage import gaussian_filter

BLUE, RED = "#2F5597", "#C00000"
INK, GRAY, LGRAY, PALE, WHITE = "#1A1A1A", "#7F7F7F", "#BFBFBF", "#EFEFEF", "#FFFFFF"

plt.rcParams["font.family"] = ["STIXGeneral", "Noto Serif CJK SC"]
plt.rcParams["mathtext.fontset"] = "stix"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["svg.fonttype"] = "none"


def new_fig(w_cm, h_cm):
    fig = plt.figure(figsize=(w_cm / 2.54, h_cm / 2.54))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_cm)
    ax.set_ylim(0, h_cm)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, fc=WHITE, ec=INK, lw=0.8, r=0.03, ls="-", z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    ax.add_patch(p)
    return p


def text(ax, x, y, s, size=7, color=INK, ha="center", va="center", weight="normal", z=5, **kw):
    kw.setdefault("linespacing", 1.3)
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, zorder=z, **kw)


def line(ax, pts, color=INK, lw=0.8, ls="-", z=4):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="butt", solid_joinstyle="miter")


def arrow(ax, pts, color=INK, lw=0.8, head=0.22, ls="-", z=4):
    """直角折线箭头，箭头在最后一段。"""
    if len(pts) > 2:
        line(ax, pts[:-1], color, lw, ls, z)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    d =np.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / d, (y1 - y0) / d
    bx, by = x1 - ux * head, y1 - uy * head
    line(ax, [(x0, y0), (bx, by)], color, lw, ls, z)
    px, py = -uy, ux
    ax.add_patch(Polygon([(x1, y1), (bx + px * head * 0.30, by + py * head * 0.30),
                          (bx - px * head * 0.30, by - py * head * 0.30)],
                         closed=True, fc=color, ec=color, lw=0.3, zorder=z))


def dbl_arrow(ax, x0, x1, y, gap=0.10, lw=1.5, color=INK, z=4):
    """⇒ 双线粗箭头（水平向右）。"""
    for dy in (gap / 2, -gap / 2):
        ax.plot([x0, x1 - 0.12], [y + dy, y + dy], color=color, lw=lw, zorder=z, solid_capstyle="butt")
    ax.plot([x1 - 0.28, x1, x1 - 0.28], [y + 0.20, y, y - 0.20], color=color, lw=lw,
            zorder=z, solid_capstyle="butt", solid_joinstyle="miter")


def rich(ax, x, y, parts, size=9, ha="center", z=5):
    """依次排布 [(字符串, 颜色), ...]，用于同一行里分色的公式。"""
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    inv = ax.transData.inverted()
    objs, widths = [], []
    for s, c in parts:
        t = ax.text(0, y, s, fontsize=size, color=c, ha="left", va="center", zorder=z)
        (a, _), (b, _) = inv.transform(t.get_window_extent(r).get_points())
        objs.append(t)
        widths.append(b - a)
    total = sum(widths)
    cur = {"center": x - total / 2, "right": x - total}.get(ha, x)
    for t, w in zip(objs, widths):
        t.set_x(cur)
        cur += w
    return total


def mtext(ax, x, y, s, size=7, color=INK, ha="center", z=5):
    """中文与 $公式$ 混排：按 $ 切段分别渲染（mathtext 内无 CJK 字形）。"""
    import re
    parts = [(p, color) for p in re.split(r"(\$[^$]*\$)", s) if p]
    return rich(ax, x, y, parts, size=size, ha=ha, z=z)


def xray(seed=0, n=120, lesion=None):
    """极简合成胸片：深色背景、较暗肺野、较亮纵隔/心影/肋骨。lesion=(cx, cy, r) 为肺内亮斑。"""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:1:n * 1j, 0:1:n * 1j]
    img = 0.10 + 0.42 * np.exp(-(((xx - .5) / .40) ** 2 + ((yy - .55) / .50) ** 4))   # 躯干
    for sx in (-1, 1):                                                                    # 肺野
        cxl = .5 + sx * .185 + rng.normal(0, .005)
        img -= 0.40 * np.exp(-(((xx - cxl) / .13) ** 2 + ((yy - .45) / .32) ** 2) ** 1.6)
    img += 0.20 * np.exp(-((xx - .5) / .045) ** 2) * (yy > .08)                          # 脊柱/纵隔
    img += 0.22 * np.exp(-(((xx - .56) / .10) ** 2 + ((yy - .36) / .10) ** 2))           # 心影
    img += 0.12 * np.exp(-(((xx - .5) / .36) ** 2 + ((yy - .93) / .05) ** 2))            # 肩/锁骨
    for k in range(7):                                                                    # 肋骨
        yk = .20 + k * .075
        for sx in (-1, 1):
            curve = yk + 0.12 - 0.62 * np.abs(xx - .5) + 0.0 * sx
            img += 0.022 * np.exp(-((yy - curve) / .014) ** 2) * (np.abs(xx - .5) > .07) * (np.abs(xx - .5) < .30)
    if lesion:
        lx, ly, lr = lesion
        img += 0.30 * np.exp(-(((xx - lx) / lr) ** 2 + ((yy - ly) / lr) ** 2))
    img = gaussian_filter(img, 1.2) + rng.normal(0, .012, img.shape)
    return np.clip(img, 0, 1)[::-1]


def thumb(ax, x, y, w, h, **kw):
    ax.imshow(xray(**kw), cmap="gray", vmin=0, vmax=0.85, extent=(x, x + w, y, y + h),
              aspect="auto", zorder=3, interpolation="bilinear")
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=INK, lw=0.6, zorder=4))


def audit(fig, ax, pad=0.02):
    """检查文字出画布 / 压框线 / 互相重叠 (cm)。"""
    fig.canvas.draw()
    r, inv = fig.canvas.get_renderer(), ax.transData.inverted()
    x_hi, y_hi = ax.get_xlim()[1], ax.get_ylim()[1]
    boxes = [(p.get_x(), p.get_y(), p.get_x() + p.get_width(), p.get_y() + p.get_height())
             for p in ax.patches if isinstance(p, FancyBboxPatch)]
    items = []
    for t in ax.texts:
        if t.get_text().strip():
            (x0, y0), (x1, y1) = inv.transform(t.get_window_extent(r).get_points())
            y0, y1 = y0 + 0.16 * (y1 - y0), y1 - 0.16 * (y1 - y0)
            items.append((t.get_text().replace("\n", "|"), x0, y0, x1, y1))
    bad = []
    for s, x0, y0, x1, y1 in items:
        if x0 < 0 or y0 < 0 or x1 > x_hi or y1 > y_hi:
            bad.append(f"出画布: {s!r} [{x0:.2f},{x1:.2f}]x[{y0:.2f},{y1:.2f}]")
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        cont = [b for b in boxes if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]]
        if cont:
            b = min(cont, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
            if x0 < b[0] + pad or x1 > b[2] - pad or y0 < b[1] + pad or y1 > b[3] - pad:
                bad.append(f"出框/贴边: {s!r} [{x0:.2f},{x1:.2f}]x[{y0:.2f},{y1:.2f}] 框[{b[0]:.2f},{b[2]:.2f}]x[{b[1]:.2f},{b[3]:.2f}]")
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            if min(a[3], b[3]) - max(a[1], b[1]) > 0.01 and min(a[4], b[4]) - max(a[2], b[2]) > 0.01:
                bad.append(f"重叠: {a[0]!r} <-> {b[0]!r}")
    print("\n".join(bad) if bad else f"audit OK ({len(items)} texts)")
    return bad


def save(fig, stem):
    fig.savefig(f"{stem}.png", dpi=300)
    fig.savefig(f"{stem}.pdf")
