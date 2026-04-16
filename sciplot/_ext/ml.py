"""
机器学习可视化扩展
用于绘制：PCA、聚类、决策树、特征重要性、混淆矩阵等
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Any, List, Optional, Tuple


def plot_pca(
    data: np.ndarray,
    labels: Optional[np.ndarray] = None,
    n_components: int = 2,
    venue: str = "nature",
    palette: str = "pastel",
    **kwargs
) -> Tuple[Figure, Axes]:
    """
    PCA 可视化
    """
    from sklearn.decomposition import PCA
    from sciplot._core.style import setup_style
    from sciplot._core.layout import new_figure

    setup_style(venue, palette)
    fig, ax = new_figure(venue)

    pca = PCA(n_components=n_components)
    data_pca = pca.fit_transform(data)

    if n_components == 2:
        if labels is not None:
            unique_labels = np.unique(labels)
            for i, label in enumerate(unique_labels):
                mask = labels == label
                ax.scatter(data_pca[mask, 0], data_pca[mask, 1],
                          label=f"Class {label}", **kwargs)
            ax.legend()
        else:
            ax.scatter(data_pca[:, 0], data_pca[:, 1], **kwargs)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    else:
        ax = fig.add_subplot(111, projection='3d')
        if labels is not None:
            unique_labels = np.unique(labels)
            for i, label in enumerate(unique_labels):
                mask = labels == label
                ax.scatter(data_pca[mask, 0], data_pca[mask, 1], data_pca[mask, 2],
                          label=f"Class {label}", **kwargs)
            ax.legend()
        else:
            ax.scatter(data_pca[:, 0], data_pca[:, 1], data_pca[:, 2], **kwargs)
        ax.set_xlabel(f"PC1")
        ax.set_ylabel(f"PC2")
        ax.set_zlabel(f"PC3")

    ax.tick_params(direction="in")
    return fig, ax


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: Optional[List[str]] = None,
    normalize: bool = False,
    cmap: str = "Blues",
    venue: str = "nature",
    **kwargs
) -> Tuple[Figure, Axes]:
    """
    混淆矩阵可视化
    """
    from sklearn.metrics import confusion_matrix
    from sciplot._core.style import setup_style
    from sciplot._core.layout import new_figure
    import itertools

    setup_style(venue)
    fig, ax = new_figure(venue)

    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    fig.colorbar(im, ax=ax)

    if labels is not None:
        ax.set_xticks(np.arange(len(labels)))
        ax.set_yticks(np.arange(len(labels)))
        ax.set_xticklabels(labels)
        ax.set_yticklabels(labels)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j, i, format(cm[i, j], '.2f' if normalize else 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black")

    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.tick_params(direction="in")

    return fig, ax


def plot_feature_importance(
    features: List[str],
    importance: np.ndarray,
    title: str = "Feature Importance",
    venue: str = "nature",
    palette: str = "pastel",
    **kwargs
) -> Tuple[Figure, Axes]:
    """
    特征重要性可视化
    """
    from sciplot._core.style import setup_style
    from sciplot._core.layout import new_figure

    setup_style(venue, palette)
    fig, ax = new_figure(venue)

    indices = np.argsort(importance)[::-1]
    sorted_features = [features[i] for i in indices]
    sorted_importance = importance[indices]

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]

    ax.barh(range(len(features)), sorted_importance, color=colors[0], **kwargs)
    ax.set_yticks(range(len(features)))
    ax.set_yticklabels(sorted_features)
    ax.invert_yaxis()
    ax.set_xlabel("Importance")
    ax.set_title(title)
    ax.tick_params(direction="in")

    return fig, ax


def plot_learning_curve(
    train_scores: np.ndarray,
    val_scores: np.ndarray,
    train_sizes: Optional[np.ndarray] = None,
    label_train: str = "Training",
    label_val: str = "Validation",
    venue: str = "nature",
    palette: str = "pastel",
    **kwargs
) -> Tuple[Figure, Axes]:
    """
    学习曲线可视化
    """
    from sciplot._core.style import setup_style
    from sciplot._core.layout import new_figure

    setup_style(venue, palette)
    fig, ax = new_figure(venue)

    if train_sizes is None:
        train_sizes = np.arange(1, len(train_scores) + 1)

    ax.plot(train_sizes, train_scores, label=label_train, marker='o', **kwargs)
    ax.plot(train_sizes, val_scores, label=label_val, marker='s', **kwargs)

    ax.set_xlabel("Training Examples")
    ax.set_ylabel("Score")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.tick_params(direction="in")

    return fig, ax
