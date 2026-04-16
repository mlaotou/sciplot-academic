"""
配色管理 - 配色方案定义与应用
"""

from __future__ import annotations

from typing import Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib import cycler
import warnings


class _UserPaletteStore:
    """用户自定义配色存储器（单例模式）"""
    _palettes: Dict[str, List[str]] = {}

    @classmethod
    def set(cls, name: str, colors: List[str]) -> None:
        cls._palettes[name] = colors
        for i in range(1, len(colors) + 1):
            cls._palettes[f"{name}-{i}"] = colors[:i]

    @classmethod
    def get(cls, name: str) -> Optional[List[str]]:
        return cls._palettes.get(name)

    @classmethod
    def get_all_names(cls) -> List[str]:
        return list(cls._palettes.keys())


RMB_PALETTES: Dict[str, List[str]] = {
    "100yuan": ["#780018", "#AA0033", "#DD0022", "#CC0044", "#FA8095"],
    "50yuan":  ["#25362B", "#276E3D", "#56B76A", "#3C4061", "#8E8E99"],
    "20yuan":  ["#532F1A", "#6B4E25", "#7F5643", "#796A5D", "#BE9A62"],
    "10yuan":  ["#242F4D", "#465A66", "#6382AA", "#828E99", "#7F606D"],
    "5yuan":   ["#413A4C", "#63576F", "#56B76A", "#6F8DB1", "#B3A479"],
    "1yuan":   ["#3C3F27", "#5A5745", "#9DA780", "#937539", "#C5AB71"],
}

PASTEL_PALETTE: Dict[str, List[str]] = {
    "pastel":   ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe", "#a2d2ff"],
    "pastel-1": ["#cdb4db"],
    "pastel-2": ["#cdb4db", "#ffc8dd"],
    "pastel-3": ["#cdb4db", "#ffc8dd", "#ffafcc"],
    "pastel-4": ["#cdb4db", "#ffc8dd", "#ffafcc", "#bde0fe"],
}

EARTH_PALETTE: Dict[str, List[str]] = {
    "earth":   ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"],
    "earth-1": ["#264653"],
    "earth-2": ["#264653", "#2a9d8f"],
    "earth-3": ["#264653", "#2a9d8f", "#e9c46a"],
    "earth-4": ["#264653", "#2a9d8f", "#e9c46a", "#f4a261"],
}

OCEAN_PALETTE: Dict[str, List[str]] = {
    "ocean":   ["#88afd8", "#90bfcf", "#afd1bf", "#cfe5bb", "#e0eeb8"],
    "ocean-1": ["#88afd8"],
    "ocean-2": ["#88afd8", "#90bfcf"],
    "ocean-3": ["#88afd8", "#90bfcf", "#afd1bf"],
    "ocean-4": ["#88afd8", "#90bfcf", "#afd1bf", "#cfe5bb"],
}

RESIDENT_PALETTES: Dict[str, List[str]] = {
    **PASTEL_PALETTE,
    **EARTH_PALETTE,
    **OCEAN_PALETTE,
}

TOL_PALETTES: Dict[str, List[str]] = {
    "bright":   ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"],
    "high-vis": ["#DDAA33", "#BB5566", "#004488", "#DDDDDD"],
    "vibrant":  ["#EE7733", "#0077BB", "#33BBEE", "#EE3377", "#CC3311", "#009988", "#BBBBBB"],
    "muted":    ["#CC6677", "#332288", "#DDCC77", "#117733", "#88CCEE",
                 "#882255", "#44AA99", "#999933", "#AA4499"],
    "light":    ["#77AADD", "#EE8866", "#EEDD88", "#FFAABB", "#99DDFF",
                 "#44BB99", "#BBCC33", "#CCCCCC", "#DDDDDD"],
}

SCIENCEPLOTS_PALETTES = list(TOL_PALETTES.keys()) + [f"rainbow-{i}" for i in range(1, 24)]
CUSTOM_PALETTES = list(RMB_PALETTES.keys()) + list(RESIDENT_PALETTES.keys())
ALL_PALETTES = CUSTOM_PALETTES + SCIENCEPLOTS_PALETTES

DEFAULT_PALETTE = "pastel"


def apply_palette(palette: str) -> None:
    """将指定配色应用到 rcParams"""
    if palette in RESIDENT_PALETTES:
        plt.rcParams["axes.prop_cycle"] = cycler(color=RESIDENT_PALETTES[palette])
    elif palette.startswith("rainbow-"):
        n = int(palette.split("-")[1])
        if not (1 <= n <= 23):
            raise ValueError(f"离散彩虹颜色数 N 必须在 1–23 之间，当前: {n}")
        plt.style.use(f"discrete-rainbow-{n}")
    elif palette in TOL_PALETTES:
        plt.style.use(palette)
    elif palette in RMB_PALETTES:
        plt.rcParams["axes.prop_cycle"] = cycler(color=RMB_PALETTES[palette])
    elif _UserPaletteStore.get(palette):
        plt.rcParams["axes.prop_cycle"] = cycler(color=_UserPaletteStore.get(palette))
    else:
        raise ValueError(
            f"未知配色方案 '{palette}'。调用 list_palettes() 查看所有可用选项。"
        )


def set_custom_palette(
    colors: List[str],
    name: str = "custom",
) -> None:
    """
    设置自定义配色方案

    参数:
        colors: HEX 颜色列表
        name: 配色名称前缀

    示例:
        >>> set_custom_palette(["#E74C3C", "#3498DB", "#2ECC71"])
        >>> setup_style(palette="custom")
    """
    if not colors:
        raise ValueError("颜色列表不能为空")
    if len(colors) > 6:
        warnings.warn(
            f"自定义配色建议不超过 6 色，当前 {len(colors)} 色可能会影响可视化效果",
            UserWarning,
            stacklevel=2,
        )

    _UserPaletteStore.set(name, colors)
    plt.rcParams["axes.prop_cycle"] = cycler(color=colors)


def get_palette(name: str) -> List[str]:
    """获取配色方案的 HEX 颜色列表"""
    for palette_dict in (RMB_PALETTES, RESIDENT_PALETTES, TOL_PALETTES):
        if name in palette_dict:
            return palette_dict[name]
    user_palette = _UserPaletteStore.get(name)
    if user_palette:
        return user_palette
    raise ValueError(f"未知配色方案 '{name}'，rainbow-N 系列不支持直接获取颜色列表。")


def list_palettes() -> List[str]:
    """列出所有可用配色方案名称"""
    return ALL_PALETTES + _UserPaletteStore.get_all_names()


def list_all_palettes() -> List[str]:
    """list_palettes() 的别名"""
    return list_palettes()


def list_resident_palettes() -> List[str]:
    """列出三大常驻配色系"""
    return list(RESIDENT_PALETTES.keys())


def list_pastel_subsets() -> List[str]:
    """列出 pastel 子集名称"""
    return list(PASTEL_PALETTE.keys())


def list_earth_subsets() -> List[str]:
    """列出 earth 子集名称"""
    return list(EARTH_PALETTE.keys())


def list_ocean_subsets() -> List[str]:
    """列出 ocean 子集名称"""
    return list(OCEAN_PALETTE.keys())


def list_rmb_palettes() -> List[str]:
    """列出人民币配色方案名称"""
    return list(RMB_PALETTES.keys())


def list_tol_palettes() -> List[str]:
    """列出 Paul Tol 配色方案名称"""
    return list(TOL_PALETTES.keys())
