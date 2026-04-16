# 语法糖功能（v1.7.1 新增）

SciPlot 提供三种语法糖，让绘图代码更简洁、更流畅。

---

## 1. Fluent Interface 链式调用

通过链式 API 实现流畅的绘图流程，支持多图层叠加。

### 基础用法

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 100)

# 最简链式调用
fig = sp.style("nature").palette("pastel").plot(x, np.sin(x)).save("output")

# 使用 chain() 入口
fig = sp.chain(venue="thesis", palette="ocean", lang="zh").plot(x, y).save("fig")
```

### 多图层叠加

```python
fig = (sp.style("ieee")
         .palette("earth")
         .plot(x, np.sin(x), label="sin")
         .scatter(x, np.cos(x), label="cos")
         .legend()
         .xlabel("时间 (s)")
         .ylabel("幅度")
         .title("三角函数")
         .save("multi_layer"))
```

### 链式方法速查

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `sp.style(venue)` | 设置期刊样式 | PlotChain |
| `sp.palette(name)` | 设置配色方案 | PlotChain |
| `sp.chain(venue, palette, lang)` | 完整链式入口 | PlotChain |
| `.plot(x, y, **kwargs)` | 添加折线 | FigureWrapper |
| `.scatter(x, y, **kwargs)` | 添加散点 | FigureWrapper |
| `.bar(x, y, **kwargs)` | 添加柱状图 | FigureWrapper |
| `.xlabel(label)` | 设置 X 轴标签 | FigureWrapper |
| `.ylabel(label)` | 设置 Y 轴标签 | FigureWrapper |
| `.title(title)` | 设置标题 | FigureWrapper |
| `.legend(**kwargs)` | 显示图例 | FigureWrapper |
| `.save(name, **kwargs)` | 保存图片 | list[Path] |
| `.show()` | 显示图形 | None |

---

## 2. Context Manager 上下文管理器

临时切换样式，不影响全局设置，支持嵌套使用。

### 基础用法

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 100)

# 临时切换样式
with sp.style_context("ieee", palette="earth"):
    fig, ax = sp.plot(x, np.sin(x))
    sp.save(fig, "ieee_style")

# 恢复默认样式继续绘图
fig, ax = sp.plot(x, np.cos(x))  # 使用默认 nature + pastel
```

### 嵌套上下文

```python
with sp.style_context("nature", palette="pastel"):
    fig1, ax1 = sp.plot(x, y1)  # nature + pastel
    
    with sp.style_context("ieee", palette="ocean"):
        fig2, ax2 = sp.plot(x, y2)  # ieee + ocean
    
    # 恢复为 nature + pastel
    fig3, ax3 = sp.plot(x, y3)
```

### 自定义 rcParams

```python
with sp.style_context("thesis", lang="zh", figure.dpi=200, font.size=14):
    fig, ax = sp.plot(x, y)
```

---

## 3. 简洁函数别名

更短更直观的函数名，适合快速绘图。

| 别名 | 完整名称 | 说明 |
|------|----------|------|
| `sp.line()` | `sp.plot_line()` | 折线图 |
| `sp.scatter()` | `sp.plot_scatter()` | 散点图 |
| `sp.bar()` | `sp.plot_bar()` | 柱状图 |
| `sp.hbar()` | `sp.plot_horizontal_bar()` | 水平柱状图 |
| `sp.hist()` | `sp.plot_histogram()` | 直方图 |
| `sp.box()` | `sp.plot_box()` | 箱线图 |
| `sp.violin()` | `sp.plot_violin()` | 小提琴图 |
| `sp.heatmap()` | `sp.plot_heatmap()` | 热力图 |
| `sp.area()` | `sp.plot_area()` | 面积图 |
| `sp.step()` | `sp.plot_step()` | 阶梯图 |
| `sp.errorbar()` | `sp.plot_errorbar()` | 误差条图 |

### 使用示例

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# 简洁别名
fig, ax = sp.line(x, y)
fig, ax = sp.scatter(x, y)
fig, ax = sp.bar(["A", "B"], [1, 2])
fig, ax = sp.hbar(["A", "B"], [1, 2])
fig, ax = sp.hist(data, bins=30)
fig, ax = sp.box([data1, data2])
fig, ax = sp.violin([data1, data2])
fig, ax = sp.heatmap(matrix)
fig, ax = sp.area(x, y)
fig, ax = sp.step(x, y)
fig, ax = sp.errorbar(x, y, yerr)
```

---

## 三种风格对比

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

# 风格 1: 传统 API
sp.setup_style("nature", "pastel")
fig, ax = sp.plot_line(x, y, xlabel="X", ylabel="Y")
sp.save(fig, "output")

# 风格 2: 链式调用
sp.style("nature").palette("pastel").plot(x, y).xlabel("X").ylabel("Y").save("output")

# 风格 3: 简洁别名
sp.setup_style("nature", "pastel")
fig, ax = sp.line(x, y, xlabel="X", ylabel="Y")
sp.save(fig, "output")
```

选择最适合你代码风格的写法！
