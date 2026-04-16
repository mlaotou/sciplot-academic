# SciPlot Academic

**中文科研绘图库** — 基于 Matplotlib + SciencePlots，专为中文科研场景优化

[![PyPI version](https://badge.fury.io/py/sciplot-academic.svg)](https://badge.fury.io/py/sciplot-academic)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 特性

- 🌈 **期刊样式** — Nature/IEEE/APS/Springer/Thesis 一键切换
- 🎨 **智能配色** — pastel/earth/ocean 三大常驻色系 + 自定义配色
- 📊 **丰富图表** — 折线/散点/柱状/箱线/小提琴/热力图等
- 🤖 **ML 可视化** — PCA/混淆矩阵/特征重要性（需 scikit-learn）
- 📐 **论文布局** — 预置 Word/LaTeX 子图尺寸

---

## 安装

```bash
# pip
pip install sciplot-academic

# uv（推荐）
uv pip install sciplot-academic

# ML 扩展依赖（可选）
uv pip install sciplot-academic[ml]
```

---

## 快速上手

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 200)

# 单线图
fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")  # → 结果图.pdf + 结果图.png

# 多线对比（自动 pastel-2 配色）
fig, ax = sp.plot_multi(x, [np.sin(x), np.cos(x)], labels=["方法 A", "方法 B"])
sp.save(fig, "对比")
```

---

## 图表类型

```python
sp.plot(x, y)                    # 折线图
sp.plot_multi(x, [y1, y2])       # 多线图（自动配色）
sp.plot_scatter(x, y)            # 散点图
sp.plot_bar(categories, values)  # 柱状图
sp.plot_box(data_list)           # 箱线图
sp.plot_violin(data_list)         # 小提琴图
sp.plot_errorbar(x, y, yerr)     # 误差条
sp.plot_confidence(x, mean, std)  # 置信区间
sp.plot_heatmap(data)             # 热力图
sp.plot_histogram(data)           # 直方图

# 机器学习（需安装 ml 扩展）
sp.plot_pca(data, labels)        # PCA 可视化
sp.plot_confusion_matrix(y_true, y_pred)  # 混淆矩阵
sp.plot_feature_importance(features, importance)  # 特征重要性
```

---

## 期刊样式

| venue | 尺寸 | 场景 |
|-------|------|------|
| `nature` | 7.0 × 5.0 | Nature/Science |
| `ieee` | 3.5 × 3.0 | IEEE 单栏 |
| `thesis` | 6.1 × 4.3 | 学位论文 |

---

## 配色方案

**三大常驻色系**（各有 1-4 色调子集）：
- `pastel` — 柔和粉彩
- `earth` — 大地色系
- `ocean` — 海洋蓝绿

**其他**：`rainbow-N`（1-23色）、`bright`、`vibrant`、`muted`、`100yuan`

```python
sp.set_custom_palette(["#E74C3C", "#3498DB", "#2ECC71"], name="mycolors")
sp.setup_style(palette="mycolors-2")
```

---

## 依赖

- `matplotlib >= 3.5.0`
- `numpy >= 1.20.0`
- `SciencePlots >= 2.0.0`

---

**License**: MIT
