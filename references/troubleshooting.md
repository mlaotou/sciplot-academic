# SciPlot 常见问题排查

---

## 安装问题

### `ModuleNotFoundError: No module named 'scienceplots'`

```bash
# 使用 uv
uv add scienceplots
```

---

### `ImportError: cannot import name 'sciplot'`

sciplot 模块不在 Python 路径中，三种解法：

```python
# 方法1：可编辑安装
# cd sciplot目录, 然后:
pip install -e .

# 方法2：手动添加路径
import sys
sys.path.insert(0, "/path/to/sciplot")

# 方法3：同目录相对导入
from . import sciplot
```

---

## 字体问题

### 中文显示为方块（□□□）

**原因**：未设置 `lang` 参数，或系统缺少 CJK 字体。

```python
# 正确做法：在 setup_style 中指定语言
setup_style("thesis", "rainbow-5", lang="zh-cn")
ax.set_xlabel("时间 (s)")   # 现在可以正常显示中文
```

检查字体是否安装：

```python
import matplotlib.font_manager as fm
fonts = [f.name for f in fm.fontManager.ttflist]
print("SimSun" in fonts)   # 应为 True
```

---

### LaTeX 参数说明

```python
# 中文推荐调用
setup_style("ieee", "rainbow-5", lang="zh-cn")  # ✓

# 即使传 use_latex=True，也会被自动忽略并保持禁用
setup_style("ieee", "rainbow-5", use_latex=True)                 # 参数兼容，不启用 LaTeX
```

SciPlot 默认始终禁用 LaTeX（`text.usetex=False`），以保证中文字体渲染稳定。

---

## 图形问题

### 图片太小/太大

```python
# 查询 venue 默认尺寸
from sciplot import get_venue_info
print(get_venue_info("ieee"))
# → {'figsize': (3.5, 3.0), ...}

# 自定义尺寸覆盖 venue 默认值
fig, ax = new_figure("ieee", figsize=(7, 5))
```

---

### 子图重叠

```python
# 使用 create_subplots()，它会自动等比缩放尺寸
fig, axes = create_subplots(2, 2, venue="ieee")

# 或手动调整并 tight_layout
import matplotlib.pyplot as plt
fig.tight_layout()
```

---

## 配色问题

### 颜色没有按预期循环

setup_style() 必须在创建图形之前调用：

```python
# ✓ 正确顺序
setup_style("ieee", "rainbow-5")
fig, ax = new_figure("ieee")
ax.plot(x, y1)   # 颜色1
ax.plot(x, y2)   # 颜色2

# ✗ 错误：先创建图形，后设置样式
fig, ax = new_figure("ieee")
setup_style("ieee", "rainbow-5")  # 此时配色已不生效
```

---

### 需要超过5条线但用的是人民币配色

人民币系列每组只有5色，线条更多时建议：

```python
# 方法1：改用离散彩虹（N = 线条数）
setup_style("ieee", "rainbow-8")

# 方法2：叠加线型区分
fig, ax = plot_multi_line(x, [y1,...,y7], use_linestyles=True)
```

---

## 保存问题

### `PermissionError`

文件被其他程序占用，关闭后重试，或更改保存路径：

```python
save(fig, "C:/temp/result")
```

---

### PNG 图片模糊

```python
save(fig, "result", dpi=2400)    # 提高分辨率
save(fig, "draft", dpi=150)      # 快速预览用低分辨率
```

---

## 验证与调试

### 列出所有可用选项

```python
from sciplot import list_venues, list_palettes, list_languages

print(list_venues())
# → ['ieee', 'nature', 'aps', 'springer', 'thesis', 'presentation', 'default']

print(list_palettes())
# → ['100yuan', '50yuan', ..., 'bright', 'muted', ..., 'rainbow-1', ..., 'rainbow-23']

print(list_languages())
# → ['zh', 'zh-cn', 'zh-tw', 'ja', 'ko']
```

---

### 基础功能自检

```python
import numpy as np
from sciplot import setup_style, new_figure, save

setup_style("default", "rainbow-3")
fig, ax = new_figure("default")
ax.plot([1, 2, 3], [1, 4, 2])
save(fig, "sciplot_test")
print("基础测试通过！")
```

---

## 性能优化

### 数据量大时绘图慢

```python
# 降采样绘制（每10个取1个）
ax.plot(x[::10], y[::10])

# 或开启栅格化（矢量图中复杂区域转位图）
ax.plot(x, y, rasterized=True)
```

---

## 错误速查表

| 错误信息                                      | 原因                   | 解决方案                               |
| --------------------------------------------- | ---------------------- | -------------------------------------- |
| `ValueError: 未知 venue 'xxx'`              | venue 名称拼写错误     | 调用 `list_venues()` 确认            |
| `ValueError: 未知配色方案 'xxx'`            | 配色名称错误           | 调用 `list_palettes()` 确认          |
| `ValueError: 未知 lang 'xxx'`               | 语言代码错误           | 调用 `list_languages()` 确认         |
| `ValueError: 离散彩虹颜色数 N 必须在 1–23` | N 超出范围             | 使用 `rainbow-1` 到 `rainbow-23`   |
| `PermissionError`                           | 文件被其他程序锁定     | 关闭文件后重试                         |
| `FileNotFoundError`                         | 输出目录不存在         | 先 `os.makedirs(dir, exist_ok=True)` |
| 中文显示乱码                                  | 未设置 lang 或缺少字体 | `setup_style(..., lang="zh-cn")`     |
