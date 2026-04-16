# 扩展功能

## 机器学习可视化（ML 扩展）

需要安装：`pip install sciplot-academic[ml]`

```python
from sciplot._ext.ml import (
    plot_pca,
    plot_confusion_matrix,
    plot_feature_importance,
    plot_learning_curve
)

# PCA 可视化
fig, ax = plot_pca(data, labels=labels, venue="nature")

# 混淆矩阵
fig, ax = plot_confusion_matrix(y_true, y_pred, labels=["A", "B", "C"])

# 特征重要性
fig, ax = plot_feature_importance(features, importance, top_n=15)

# 学习曲线
fig, ax = plot_learning_curve(train_scores, val_scores, sizes)
```

---

## 3D 可视化（Plot3D 扩展）

```python
from sciplot._ext.plot3d import plot_surface, plot_contour, plot_3d_scatter

# 3D 曲面
fig, ax = plot_surface(X, Y, Z, xlabel="X", ylabel="Y", zlabel="Z")

# 等高线图
fig, ax = plot_contour(X, Y, Z, levels=15, filled=True)

# 3D 散点
fig, ax = plot_3d_scatter(x, y, z, c=colors, cmap="plasma")
```
