# SciPlot Academic — 包使用 Skill (v1.4)

---
name: sciplot
description: >
  科研绘图技能（sciplot-academic 包版）。凡涉及学术图表、论文插图、数据可视化、
  matplotlib/scienceplots 绘图、期刊格式配图、毕设/竞赛图片等需求，必须调用本技能。
  本技能针对已安装 sciplot-academic 包的环境，直接 `import sciplot as sp` 使用，
  无需复制任何文件到项目目录。
  默认中文 + Nature 期刊样式 + pastel 配色，支持 IEEE/APS/Springer/学位论文，
  提供折线、散点、柱状、箱线、小提琴、热力图、误差条、置信区间、多子图等全类型图表。
---

## 0. 安装方式

用户在项目虚拟环境中一次性安装，之后所有项目均可直接导入：

```bash
# pip（通用）
pip install sciplot-academic

# uv（推荐，速度最快）
uv pip install sciplot-academic

# conda 环境（需先安装依赖）
conda install -c conda-forge matplotlib numpy
pip install scienceplots sciplot-academic
```

安装后，**在任何项目中**直接使用：

```python
import sciplot as sp
```

---

## 1. AI 快速入口（最常用路径）

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 200)

# ── 单线图 ──────────────────────────────────────────────────────
fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")

# ── 多线对比（≤4条线自动选 pastel/earth/ocean 子集）─────────────
fig, ax = sp.plot_multi(
    x, [np.sin(x), np.cos(x)],
    labels=["方法 A", "方法 B"],
    xlabel="迭代次数", ylabel="准确率 (%)"
)
sp.save(fig, "对比结果")

# ── 6条以上，手动指定 rainbow-N ──────────────────────────────
fig, ax = sp.plot_multi(x, [y1,y2,y3,y4,y5,y6], labels=[...], palette="rainbow-6")
```

> **`plot_multi` 智能配色**：N≤4 自动选 `pastel-N`（或 `earth-N`/`ocean-N`），N=5 用完整 5 色，N≥6 需手动指定 `rainbow-N`。

---

## 2. 三大核心函数

### `sp.setup_style(venue, palette, lang, use_latex)`

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `venue` | `"nature"` | 期刊/场合预设 |
| `palette` | `"pastel"` | 配色方案 |
| `lang` | `"zh"` | `"zh"`/`"zh-cn"` 中文宋体，`"en"` 英文 Times New Roman |
| `use_latex` | `False` | 已全局禁用（传 True 会警告并被忽略） |

```python
sp.setup_style()                           # 默认：nature + pastel + 中文
sp.setup_style(lang="en")                  # 英文模式
sp.setup_style("ieee", "pastel-2")         # IEEE + pastel前2色
sp.setup_style("ieee", "earth-3")          # IEEE + earth前3色
sp.setup_style("thesis", "100yuan")        # 学位论文 + 人民币红
sp.setup_style("nature", "rainbow-8")      # Nature + 8色彩虹
```

### `sp.new_figure(venue, figsize, **kwargs)`

```python
fig, ax    = sp.new_figure("ieee")
fig, axes  = sp.new_figure("thesis", nrows=1, ncols=2, sharex=True)
fig, ax    = sp.new_figure(figsize=(5.0, 3.5))   # 完全自定义
```

### `sp.save(fig, name, dpi, formats)`

```python
sp.save(fig, "figure_1")                             # PDF + PNG 1200 DPI（默认）
sp.save(fig, "word稿", formats=("png",), dpi=1200)   # 仅 PNG，Word 用
sp.save(fig, "投稿", formats=("pdf",))               # 仅 PDF，LaTeX 用
sp.save(fig, "draft", dpi=150, formats=("png",))     # 快速预览
```

---

## 3. Venues 与图尺寸

| Venue | 尺寸（英寸） | ≈ 厘米 | 字号 | 适用场景 |
|-------|------------|--------|------|----------|
| `nature` | 7.0 × 5.0 | 17.8 × 12.7 | 10pt | Nature/Science 双栏全图（默认） |
| `ieee` | 3.5 × 3.0 | 8.9 × 7.6 | 8pt | IEEE 单栏 |
| `aps` | 3.4 × 2.8 | 8.6 × 7.1 | 8pt | APS Physical Review 单栏 |
| `springer` | 6.0 × 4.5 | 15.2 × 11.4 | 10pt | Springer 期刊 |
| `thesis` | 6.1 × 4.3 | 15.5 × 10.9 | 10pt | 学位论文（A4 版心宽 15.5cm） |
| `presentation` | 8.0 × 5.5 | 20.3 × 14.0 | 14pt | 幻灯片/演示 |

---

## 4. Palettes 配色方案

### 三大常驻配色系（每种都有 1-4 色子集）

| 系列 | 风格 | 子集 |
|------|------|------|
| `pastel`（默认） | 柔和粉彩 | pastel-1/2/3/4 |
| `earth` | 大地色系 | earth-1/2/3/4 |
| `ocean` | 海洋蓝绿 | ocean-1/2/3/4 |

`plot_multi()` 根据线条数自动选对应子集，无需手动指定。

### 离散彩虹（6条线以上首选）

`rainbow-6` … `rainbow-23`，N = 线条数，颜色间距自动最优化。

### Paul Tol 色盲友好

`bright`(6) / `vibrant`(7) / `muted`(9) / `light`(9) / `high-vis`(4)

### 人民币系列（各5色）

`100yuan`(红) / `50yuan`(绿) / `20yuan`(棕) / `10yuan`(蓝) / `5yuan`(紫) / `1yuan`(橄榄)

---

## 5. 全图表函数速查

```python
import sciplot as sp

# 折线（简化入口）
sp.plot(x, y, xlabel="", ylabel="", title="", label="", venue="nature", palette="pastel")
sp.plot_multi(x, [y1,y2,...], labels=[...], xlabel="", ylabel="")

# 折线（完整参数）
sp.plot_line(x, y, ...)                                        # plot() 同名完整版
sp.plot_multi_line(x, y_list, use_linestyles=False, ...)       # 可叠加线型循环

# 分布类
sp.plot_scatter(x, y, s=20, alpha=0.7, ...)
sp.plot_histogram(data, bins=30, density=False, ...)
sp.plot_box(data_list, labels=[...], showfliers=True, ...)     # 箱线图
sp.plot_violin(data_list, labels=[...], showmedians=True, ...) # 小提琴图

# 误差/不确定性
sp.plot_errorbar(x, y, yerr, fmt="o", capsize=4, ...)
sp.plot_confidence(x, mean, std, alpha=0.25, label_mean="Mean", label_std="±1σ")

# 矩阵/对比
sp.plot_bar(categories, values, width=0.6, ...)
sp.plot_heatmap(data, cmap="Blues", show_values=False, fmt=".2f", ...)
```

---

## 6. 高级布局

### 规则子图

```python
fig, axes = sp.create_subplots(2, 2, venue="ieee", sharex=True)
axes[0,0].plot(x, y1);  axes[0,0].set_title("(a)")
sp.save(fig, "multi_panel", formats=("pdf",))
```

### GridSpec 不规则布局

```python
fig, gs = sp.create_gridspec(2, 3, venue="nature")
ax_top = fig.add_subplot(gs[0, :])    # 顶部通栏
ax_bl  = fig.add_subplot(gs[1, 0])
ax_bm  = fig.add_subplot(gs[1, 1])
ax_br  = fig.add_subplot(gs[1, 2])
sp.save(fig, "gridspec_layout")
```

### Word 多子图（手动控制总宽不超版心）

```python
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, axes = sp.new_figure("thesis", nrows=1, ncols=2, figsize=(6.1, 3.0))
axes[0].plot(x, y1);  axes[0].set_title("(a) 方法A");  axes[0].tick_params(direction="in")
axes[1].plot(x, y2);  axes[1].set_title("(b) 方法B");  axes[1].tick_params(direction="in")
fig.tight_layout()
sp.save(fig, "word双图", formats=("png",), dpi=1200)
```

### 双 Y 轴

```python
sp.setup_style("ieee", "pastel-2")
fig, ax1 = sp.new_figure("ieee")
ax1.plot(x, temp, color="#cdb4db", label="温度")
ax1.set_ylabel("温度 (K)", color="#cdb4db")
ax2 = sp.create_twinx(ax1)
ax2.plot(x, pressure, color="#ffc8dd", label="压力")
ax2.set_ylabel("压力 (Pa)", color="#ffc8dd")
sp.save(fig, "twin_y")
```

---

## 7. 工具函数

```python
sp.list_venues()              # ['nature','ieee','aps','springer','thesis','presentation','default']
sp.list_palettes()            # 所有配色名（含 rainbow-N）
sp.list_resident_palettes()   # 三大常驻配色系（含子集）
sp.list_pastel_subsets()      # ['pastel','pastel-1','pastel-2','pastel-3','pastel-4']
sp.list_earth_subsets()       # ['earth','earth-1','earth-2','earth-3','earth-4']
sp.list_ocean_subsets()       # ['ocean','ocean-1','ocean-2','ocean-3','ocean-4']
sp.list_tol_palettes()        # Paul Tol 配色
sp.list_rmb_palettes()        # 人民币配色
sp.list_languages()           # ['zh','zh-cn','en']
sp.get_venue_info("ieee")     # {'figsize': (3.5, 3.0), 'fontsize': 8, ...}
sp.get_palette("bright")      # 返回 HEX 列表（仅自定义配色，不含 rainbow-N）
sp.reset_style()              # 重置 matplotlib 为默认
```

---

## 8. AI 生成脚本的规范

**Claude 使用本技能后，必须在用户当前工作目录创建独立可运行的 Python 脚本**（如 `plot_result.py`），通过 `import sciplot as sp` 使用本库。**严禁直接执行或在脚本中写入 sciplot 源代码。**

### 标准脚本模板

```python
"""
科研绘图脚本 — 由 SciPlot 技能生成
依赖: pip install sciplot-academic
运行: python plot_result.py
"""
import numpy as np
import sciplot as sp

# ══ 数据区（替换为实际数据）══
x  = np.linspace(0, 10, 200)
y1 = np.sin(x)
y2 = np.cos(x)

# ══ Word 中文论文 — 单图（PNG 1200 DPI）══
fig, ax = sp.plot(
    x, y1,
    xlabel="时间 (s)", ylabel="幅度", label="sin(x)",
    venue="thesis", palette="pastel-1",
)
sp.save(fig, "word_single", formats=("png",), dpi=1200)

# ══ Word 中文论文 — 1行2列子图══
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, axes = sp.new_figure("thesis", nrows=1, ncols=2, figsize=(6.1, 3.0))
axes[0].plot(x, y1);  axes[0].set_title("(a) 方法A");  axes[0].tick_params(direction="in")
axes[1].plot(x, y2);  axes[1].set_title("(b) 方法B");  axes[1].tick_params(direction="in")
fig.tight_layout()
sp.save(fig, "word_double", formats=("png",), dpi=1200)

# ══ LaTeX IEEE 单栏投稿（PDF 矢量）══
sp.setup_style("ieee", "pastel-2", lang="en")
fig, ax = sp.new_figure("ieee")
ax.plot(x, y1, label="Method A")
ax.plot(x, y2, label="Method B")
ax.set_xlabel("Time (s)");  ax.set_ylabel("Amplitude")
ax.legend(frameon=False)
sp.save(fig, "latex_ieee", formats=("pdf",))

print("✓ 所有图片已保存")
```

### 场景选型速查

| 场景 | venue | figsize | formats | dpi | lang |
|------|-------|---------|---------|-----|------|
| Word 中文单图 | `thesis` | 默认 | `png` | 1200 | `zh` |
| Word 中文1×2子图 | `thesis` | `(6.1, 2.8)` | `png` | 1200 | `zh` |
| Word 中文2×2子图 | `thesis` | `(6.1, 5.0)` | `png` | 1200 | `zh` |
| LaTeX IEEE 单栏 | `ieee` | 默认 3.5×3.0 | `pdf` | — | `en` |
| LaTeX IEEE 双栏通栏 | `ieee` | `(7.16, 3.5)` | `pdf` | — | `en` |
| LaTeX Nature 单栏 | `nature` | `(3.5, 2.8)` | `pdf` | — | `en` |
| LaTeX Nature 双栏 | `nature` | 默认 7.0×5.0 | `pdf` | — | `en` |
| LaTeX 学位论文 | `thesis` | 默认 6.1×4.3 | `pdf` | — | `zh` |
| 幻灯片 | `presentation` | 默认 | `png` | 300 | `zh`/`en` |

---

## 9. 能力边界与替代方案

**SciPlot 专注于学术数据图表**，以下类型**不支持**：

| 不支持的图表类型 | 推荐替代方案 |
|-----------------|-------------|
| 决策树 | `sklearn.tree.plot_tree` / `graphviz` |
| 神经网络结构图 | `PlotNeuralNet` / `NN-SVG` |
| 流程图/拓扑图 | `graphviz` / `Mermaid` |
| 网络关系图 | `networkx` |
| 地理/地图 | `cartopy` / `folium` |
| 3D 图 | `matplotlib.pyplot3D` / `plotly` |
| 雷达图/桑基图/树状图 | `plotly` / `matplotlib` |

**AI 判断准则** — 遇到以下关键词时不调用 SciPlot，直接推荐替代方案：
```
决策树, 神经网络结构, 网络拓扑, 流程图, 地图, 地理, 3D, 三维,
雷达图, 蜘蛛图, 桑基图, 树状图, 甘特图, 时序图, 类图, 思维导图
```

---

## 10. 最佳实践

- **Word 用 PNG，LaTeX 用 PDF**：PDF 矢量格式勿插入 Word，PNG 勿插 LaTeX
- **Word 多图总宽锁定**：多子图用 `new_figure(figsize=(6.1, h))` 手动控制，避免超版心
- **刻度向内**：所有函数已自动 `tick_params(direction='in')`
- **不加网格**：默认 `axes.grid=False`，保持科研图简洁风格
- **色盲友好**：`plot_multi_line(use_linestyles=True)` 叠加线型区分，或选 `muted`/`bright`
- **IEEE 中文字号**：venue=ieee + lang=zh 自动下调 1pt，避免中文视觉偏大

---

## 11. 包版本信息

- 包名：`sciplot-academic`（PyPI）
- 导入名：`import sciplot as sp`
- 当前版本：1.4.0
- 三大配色系：pastel / earth / ocean
- 默认：Nature 样式 + pastel 配色 + 中文
