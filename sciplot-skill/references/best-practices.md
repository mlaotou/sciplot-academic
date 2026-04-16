# 最佳实践

## 黄金法则

- **Word 用 PNG 1200 DPI，LaTeX 用 PDF**
- **多子图总宽锁定**：用 `paper_subplots()` 或手动 `figsize=(6.1, h)`
- **刻度向内**：所有函数已自动 `tick_params(direction='in')`
- **无网格**：默认 `axes.grid=False`，保持简洁
- **色盲友好**：≥4 条线用 `use_linestyles=True`

---

## 场景速查

| 场景 | venue | formats | dpi | lang |
|------|-------|---------|-----|------|
| Word 单图 | `thesis` | png | 1200 | zh |
| Word 双图 | `thesis` | png | 1200 | zh |
| IEEE 投稿 | `ieee` | pdf | — | en |
| Nature 投稿 | `nature` | pdf | — | en |

---

## AI 脚本规范

**必须创建独立可运行的 Python 脚本**，通过 `import sciplot as sp` 使用本库。

### 标准模板

```python
"""
科研绘图脚本
依赖: pip install sciplot-academic
运行: python plot_result.py
"""
import numpy as np
import sciplot as sp

# 数据
x = np.linspace(0, 10, 200)
y1, y2 = np.sin(x), np.cos(x)

# Word 中文论文（PNG）
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, ax = sp.plot(x, y1, xlabel="时间 (s)", ylabel="幅度")
sp.save(fig, "word_single", formats=("png",), dpi=1200)

# Word 双子图
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, axes = sp.paper_subplots(1, 2, venue="thesis")
axes[0].plot(x, y1); axes[0].set_title("(a)")
axes[1].plot(x, y2); axes[1].set_title("(b)")
sp.add_panel_labels(axes)
sp.save(fig, "word_double", formats=("png",), dpi=1200)

# IEEE LaTeX（PDF）
sp.setup_style("ieee", "pastel-2", lang="en")
fig, ax = sp.new_figure("ieee")
ax.plot(x, y1, label="Method A")
ax.plot(x, y2, label="Method B")
sp.save(fig, "ieee_pdf", formats=("pdf",))

print("✓ 已保存")
```

---

## 能力边界

**不支持的图表类型**：

| 类型 | 推荐替代 |
|------|---------|
| 决策树 | `sklearn.tree.plot_tree` |
| 神经网络结构 | `PlotNeuralNet` |
| 流程图 | `graphviz` / `Mermaid` |
| 3D 图 | `plotly` |
| 地图 | `cartopy` |
