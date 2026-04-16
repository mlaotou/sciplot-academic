# 快速上手

## 安装

```bash
# pip
pip install sciplot-academic

# uv（推荐）
uv pip install sciplot-academic

# ML 扩展（可选）
uv pip install sciplot-academic[ml]
```

## 第一个图表

```python
import sciplot as sp
import numpy as np

# 数据
x = np.linspace(0, 10, 200)

# 单线图（默认 nature + pastel + 中文）
fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")
```

## 多线对比

```python
# ≤4 条线自动选配色子集
fig, ax = sp.plot_multi(
    x, 
    [np.sin(x), np.cos(x)],
    labels=["方法 A", "方法 B"],
    xlabel="迭代次数", 
    ylabel="准确率 (%)"
)
sp.save(fig, "对比")
```

## 不同场景示例

### Word 中文论文

```python
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, ax = sp.plot(x, y, xlabel="时间 (s)", ylabel="幅度")
sp.save(fig, "word_single", formats=("png",), dpi=1200)

# 双子图
fig, axes = sp.paper_subplots(1, 2, venue="thesis")
axes[0].plot(x, y1); axes[0].set_title("(a)")
axes[1].plot(x, y2); axes[1].set_title("(b)")
sp.add_panel_labels(axes)
sp.save(fig, "word_double", formats=("png",), dpi=1200)
```

### IEEE LaTeX 投稿

```python
sp.setup_style("ieee", "pastel-2", lang="en")
fig, ax = sp.new_figure("ieee")
ax.plot(x, y1, label="Method A")
ax.plot(x, y2, label="Method B")
sp.save(fig, "ieee_pdf", formats=("pdf",))
```
