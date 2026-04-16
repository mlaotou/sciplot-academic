# 配色方案

## 三大常驻色系（推荐）

| 系列 | 风格 | 子集 |
|------|------|------|
| `pastel` | 柔和粉彩 | pastel-1/2/3/4 |
| `earth` | 大地色系 | earth-1/2/3/4 |
| `ocean` | 海洋蓝绿 | ocean-1/2/3/4 |

```python
sp.setup_style(palette="pastel-3")   # 使用前3色
sp.setup_style(palette="earth-2")    # 使用前2色
```

---

## 人民币系列（各 5 色）

| 配色 | 颜色 |
|------|------|
| `100yuan` | 红色 |
| `50yuan` | 绿色 |
| `20yuan` | 棕色 |
| `10yuan` | 蓝色 |
| `5yuan` | 紫色 |
| `1yuan` | 橄榄 |

---

## 自定义配色

### 简单自定义

```python
# 简单自定义配色
sp.set_custom_palette(["#E74C3C", "#3498DB"], name="brand")
sp.setup_style(palette="brand")     # 2 色
sp.setup_style(palette="brand-1")   # 只取第1色
```

### 注册完整配色方案

```python
# 注册完整配色方案（支持自动选择）
my_scheme = {
    "single":    ["#264653"],
    "double":    ["#264653", "#2a9d8f"],
    "triple":    ["#264653", "#2a9d8f", "#e9c46a"],
    "quadruple": ["#264653", "#2a9d8f", "#e9c46a", "#f4a261"],
    "quintuple": ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
}
sp.register_color_scheme("mytheme", my_scheme)

# 使用
sp.setup_style(palette="mytheme-triple")  # 明确使用3色
sp.plot_multi(x, [y1, y2, y3], palette="mytheme")  # 自动选择3色
```

---

## 智能配色选择

```python
# 自动根据数据量选择配色子集
sp.plot_multi(x, [y1, y2])        # 自动使用 pastel-2
sp.plot_multi(x, [y1, y2, y3])    # 自动使用 pastel-3
sp.plot_multi(x, [y1, y2, y3, y4]) # 自动使用 pastel-4
```
