# 布局系统

## 期刊样式与尺寸

| venue | 尺寸（英寸） | 适用场景 |
|-------|-------------|----------|
| `nature` | 7.0 × 5.0 | Nature/Science 双栏全图 |
| `ieee` | 3.5 × 3.0 | IEEE 单栏 |
| `aps` | 3.4 × 2.8 | APS Physical Review |
| `springer` | 6.0 × 4.5 | Springer 期刊 |
| `thesis` | 6.1 × 4.3 | 学位论文（A4 版心） |
| `presentation` | 8.0 × 5.5 | 幻灯片 |

---

## 规则子图

```python
fig, axes = sp.create_subplots(2, 2, venue="ieee", sharex=True)
axes[0,0].plot(x, y)
sp.save(fig, "multi")
```

---

## 论文子图布局（推荐）

```python
# 精确匹配论文版心
fig, axes = sp.paper_subplots(1, 2, venue="thesis")
axes[0].plot(x, y1); axes[0].set_title("(a)")
axes[1].plot(x, y2); axes[1].set_title("(b)")
sp.save(fig, "1x2_thesis", formats=("png",), dpi=1200)
```

---

## 面板标签

```python
fig, axes = sp.paper_subplots(1, 3, venue="thesis")
# ... 绘图 ...
sp.add_panel_labels(axes)              # (a) (b) (c)
sp.add_panel_labels(axes, style="A")   # (A) (B) (C)
sp.add_panel_labels(axes, labels=["实验", "对照", "基准"])  # 自定义
```

---

## GridSpec 不规则布局

```python
fig, gs = sp.create_gridspec(2, 3, venue="nature")
ax_top = fig.add_subplot(gs[0, :])   # 顶部通栏
ax_l = fig.add_subplot(gs[1, 0])
ax_m = fig.add_subplot(gs[1, 1])
ax_r = fig.add_subplot(gs[1, 2])
```
