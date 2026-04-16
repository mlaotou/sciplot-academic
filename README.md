# SciPlot Academic

**期刊级科研绘图库** — 基于 Matplotlib + SciencePlots，专为中文科研场景优化

[![PyPI version](https://badge.fury.io/py/sciplot-academic.svg)](https://badge.fury.io/py/sciplot-academic)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 安装

```bash
# pip
pip install sciplot-academic

# uv（推荐）
uv pip install sciplot-academic

# conda（需要先 pip 安装 scienceplots）
conda install -c conda-forge matplotlib numpy
pip install scienceplots sciplot-academic
```

---

## 三行代码画出期刊图

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 200)

# 单线图（中文 + Nature 样式）
fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")   # → 结果图.pdf + 结果图.png（1200 DPI）

# 多线对比（2条线自动用 pastel-2 配色）
fig, ax = sp.plot_multi(
    x, [np.sin(x), np.cos(x)],
    labels=["方法 A", "方法 B"],
    xlabel="迭代次数", ylabel="准确率 (%)"
)
sp.save(fig, "对比结果")
```

---

## 核心特性

### 期刊样式（venue）

| venue | 尺寸（英寸） | 适用场景 |
|-------|------------|----------|
| `nature`（默认）| 7.0 × 5.0 | Nature/Science 双栏全图 |
| `ieee` | 3.5 × 3.0 | IEEE 单栏 |
| `aps` | 3.4 × 2.8 | APS Physical Review |
| `springer` | 6.0 × 4.5 | Springer 期刊 |
| `thesis` | 6.1 × 4.3 | 学位论文（A4 版心 15.5cm） |
| `presentation` | 8.0 × 5.5 | 幻灯片/演示 |

### 三大常驻配色系

| 配色 | 风格 | 子集 |
|------|------|------|
| `pastel`（默认） | 柔和粉彩 | pastel-1/2/3/4 |
| `earth` | 大地色系 | earth-1/2/3/4 |
| `ocean` | 海洋蓝绿 | ocean-1/2/3/4 |

`plot_multi()` 根据线条数自动选择对应子集（N≤4）。

其他配色：`rainbow-N`（N=1-23）、`bright`、`vibrant`、`muted`、`100yuan` 等。

### 图表类型

```python
sp.plot(x, y)                     # 单线图
sp.plot_multi(x, [y1, y2])        # 多线图（智能配色）
sp.plot_scatter(x, y)             # 散点图
sp.plot_bar(categories, values)   # 柱状图
sp.plot_box(data_list)            # 箱线图
sp.plot_violin(data_list)         # 小提琴图
sp.plot_errorbar(x, y, yerr)      # 误差条图
sp.plot_confidence(x, mean, std)  # 置信区间图
sp.plot_heatmap(data)             # 热力图
sp.plot_histogram(data)           # 直方图
```

---

## Word 论文 vs LaTeX 论文

### Word 中文论文 → 保存为 PNG

```python
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, ax = sp.new_figure("thesis")        # 6.1in ≈ A4 Word 版心宽
ax.plot(x, y, label="结果")
ax.set_xlabel("时间 (s)"); ax.set_ylabel("幅度")
ax.legend()
sp.save(fig, "word图", formats=("png",), dpi=1200)
```

### LaTeX IEEE 投稿 → 保存为 PDF

```python
sp.setup_style("ieee", "pastel-2", lang="en")
fig, ax = sp.new_figure("ieee")          # 3.5in = \columnwidth
ax.plot(x, y1, label="Method A")
ax.plot(x, y2, label="Method B")
ax.set_xlabel("Time (s)"); ax.set_ylabel("Accuracy")
ax.legend(frameon=False)
sp.save(fig, "fig1", formats=("pdf",))
# LaTeX: \includegraphics[width=\columnwidth]{fig1.pdf}
```

---

## 依赖

- `matplotlib >= 3.5.0`
- `numpy >= 1.20.0`
- `SciencePlots >= 2.0.0`

---

## License

MIT License
