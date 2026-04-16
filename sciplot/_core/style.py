"""
样式管理 - 期刊/场合样式配置
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import warnings


VENUES: Dict[str, tuple] = {
    "ieee":         (["science", "ieee",     "no-latex"], (3.5, 3.0),  8),
    "nature":       (["science", "nature",   "no-latex"], (7.0, 5.0), 10),
    "aps":          (["science",             "no-latex"], (3.4, 2.8),  8),
    "springer":     (["science",             "no-latex"], (6.0, 4.5), 10),
    "thesis":       (["science",             "no-latex"], (6.1, 4.3), 10),
    "presentation": (["science", "notebook", "no-latex"], (8.0, 5.5), 14),
    "default":      (["science", "nature",   "no-latex"], (7.0, 5.0), 10),
}

LANGUAGES: Dict[str, Tuple[str, str]] = {
    "zh":    ("cjk-sc-font", "SimSun"),
    "zh-cn": ("cjk-sc-font", "SimSun"),
    "en":    (None, "Times New Roman"),
}


def setup_style(
    venue: str = "nature",
    palette: str = "pastel",
    lang: Optional[str] = "zh",
) -> None:
    """
    配置 Matplotlib 绘图样式

    参数:
        venue   : 期刊/场合预设，默认 'nature'
                  'nature' | 'ieee' | 'aps' | 'springer' | 'thesis' | 'presentation'
        palette : 配色方案，默认 'pastel'
        lang    : 语言/字体，默认 'zh'（中文宋体）
                  'zh' | 'zh-cn' | 'en'

    示例:
        >>> from sciplot import setup_style
        >>> setup_style()
        >>> setup_style("ieee", "pastel-2")
    """
    if venue not in VENUES:
        raise ValueError(f"未知 venue '{venue}'，可用选项: {list(VENUES.keys())}")

    styles, _, fontsize = VENUES[venue]

    lang_style: Optional[str] = None
    cjk_font: Optional[str] = None
    if lang is not None:
        if lang not in LANGUAGES:
            raise ValueError(f"未知 lang '{lang}'，可用选项: {list(LANGUAGES.keys())}")
        lang_style, cjk_font = LANGUAGES[lang]
        if lang == "en":
            cjk_font = None
            lang_style = None

    plt.rcdefaults()
    active_styles = styles + ([lang_style] if lang_style else [])
    plt.style.use(active_styles)

    from sciplot._core.palette import apply_palette
    apply_palette(palette)

    plt.rcParams["text.usetex"] = False

    plt.rcParams["font.family"] = "serif"
    if cjk_font:
        plt.rcParams["font.serif"] = [
            cjk_font, "Noto Serif CJK SC", "Source Han Serif SC",
            "Times New Roman", "DejaVu Serif",
        ]
    else:
        plt.rcParams["font.serif"] = [
            "Times New Roman", "DejaVu Serif", "serif",
        ]
    plt.rcParams["axes.unicode_minus"] = False

    effective_fontsize = fontsize
    if venue == "ieee" and lang in {"zh", "zh-cn"}:
        effective_fontsize = max(7, fontsize - 1)

    plt.rcParams["font.size"]        = effective_fontsize
    plt.rcParams["axes.labelsize"]   = effective_fontsize
    plt.rcParams["axes.titlesize"]   = effective_fontsize
    plt.rcParams["xtick.labelsize"]  = max(6, effective_fontsize - 1)
    plt.rcParams["ytick.labelsize"]  = max(6, effective_fontsize - 1)
    plt.rcParams["legend.fontsize"]  = max(6, effective_fontsize - 1)
    plt.rcParams["axes.grid"]        = False


def reset_style() -> None:
    """重置 Matplotlib 为系统默认样式"""
    plt.rcdefaults()


def get_venue_info(venue: str) -> Dict[str, Any]:
    """获取期刊预设的详细配置"""
    if venue not in VENUES:
        raise ValueError(f"未知 venue '{venue}'")
    styles, figsize, fontsize = VENUES[venue]
    return {"name": venue, "styles": styles, "figsize": figsize, "fontsize": fontsize}


def list_venues() -> List[str]:
    """列出所有可用期刊预设名称"""
    return list(VENUES.keys())


def list_languages() -> List[str]:
    """列出所有可用语言代码"""
    return list(LANGUAGES.keys())
