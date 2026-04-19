"""
Hardening tests for hidden edge cases in core modules.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
import matplotlib.pyplot as plt

import sciplot as sp


@pytest.fixture(autouse=True)
def reset_config_state():
    """Keep config state isolated across tests."""
    sp.reset_config()
    yield
    sp.reset_config()


class TestConfigHardening:
    """Configuration normalization and validation edge cases."""

    def test_set_defaults_normalizes_formats_list(self):
        sp.set_defaults(formats=["PDF", " png "])
        assert sp.get_config("formats") == ("pdf", "png")

    def test_load_config_normalizes_formats(self, temp_dir):
        config_file = temp_dir / ".sciplot.toml"
        config_file.write_text(
            'venue = "thesis"\nlang = "zh"\ndpi = 600\nformats = ["PNG"]\n',
            encoding="utf-8",
        )

        loaded = sp.load_config(config_file)
        assert loaded is True
        assert sp.get_config("venue") == "thesis"
        assert sp.get_config("formats") == ("png",)

    def test_load_config_rejects_all_invalid_entries(self, temp_dir):
        config_file = temp_dir / ".sciplot.toml"
        config_file.write_text(
            'venue = "not-a-real-venue"\nformats = []\ndpi = 0\nlang = "xx"\n',
            encoding="utf-8",
        )

        loaded = sp.load_config(config_file)
        assert loaded is False
        assert sp.get_config("venue") == "nature"
        assert sp.get_config("formats") == ("pdf", "png")

    def test_set_defaults_rejects_invalid_palette(self):
        with pytest.raises(ValueError, match="palette"):
            sp.set_defaults(palette="not-a-palette")

    def test_set_defaults_rejects_invalid_formats(self):
        with pytest.raises(ValueError, match="不支持的格式"):
            sp.set_defaults(formats=["png", "badfmt"])

    def test_load_config_rejects_invalid_palette_and_formats(self, temp_dir):
        config_file = temp_dir / ".sciplot.toml"
        config_file.write_text(
            'palette = "not-a-palette"\nformats = ["png", "badfmt"]\n',
            encoding="utf-8",
        )

        loaded = sp.load_config(config_file)
        assert loaded is False
        assert sp.get_config("palette") == "pastel"
        assert sp.get_config("formats") == ("pdf", "png")

    def test_load_config_expands_user_home_path(self):
        config_file = Path.home() / f".sciplot-home-test-{uuid.uuid4().hex}.toml"
        config_file.write_text('venue = "ieee"\n', encoding="utf-8")
        try:
            loaded = sp.load_config(f"~/{config_file.name}")
            assert loaded is True
            assert sp.get_config("venue") == "ieee"
        finally:
            config_file.unlink(missing_ok=True)


class TestSaveHardening:
    """Save-path and format normalization edge cases."""

    def test_save_accepts_single_string_format(self, temp_dir, cleanup_figures):
        fig, ax = sp.plot([1, 2], [1, 2])
        paths = sp.save(fig, temp_dir / "single_format", formats="png")

        assert len(paths) == 1
        assert paths[0].suffix == ".png"
        assert paths[0].exists()

    def test_save_blocks_parent_escape_when_dir_set(self, temp_dir, cleanup_figures):
        fig, ax = sp.plot([1, 2], [1, 2])
        safe_dir = temp_dir / "safe"
        safe_dir.mkdir()

        with pytest.raises(ValueError):
            sp.save(fig, "../escape", formats="png", dir=safe_dir)

    def test_save_blocks_absolute_name_when_dir_set(self, temp_dir, cleanup_figures):
        fig, ax = sp.plot([1, 2], [1, 2])
        safe_dir = temp_dir / "safe"
        safe_dir.mkdir()

        with pytest.raises(ValueError):
            sp.save(fig, str(temp_dir / "escape"), formats="png", dir=safe_dir)


class TestPaletteDefensiveCopies:
    """Global palette state should not be mutable via returned lists."""

    def test_builtin_palette_get_returns_copy(self):
        palette = sp.get_palette("pastel")
        palette[0] = "#000000"

        fresh = sp.get_palette("pastel")
        assert fresh[0] != "#000000"

    def test_custom_palette_get_returns_copy(self):
        sp.set_custom_palette(["#111111", "#222222"], name="copy_test_palette")
        palette = sp.get_palette("copy_test_palette")
        palette.append("#333333")

        fresh = sp.get_palette("copy_test_palette")
        assert fresh == ["#111111", "#222222"]


class TestColorUtilityHardening:
    def test_rgb_to_hex_rejects_out_of_range(self):
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            sp.rgb_to_hex(1.2, 0.5, 0.5)
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            sp.rgb_to_hex(-0.1, 0.5, 0.5)

    def test_lighten_color_rejects_invalid_amount(self):
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            sp.lighten_color("#123456", 2.0)

    def test_darken_color_rejects_invalid_amount(self):
        with pytest.raises(ValueError, match="\\[0, 1\\]"):
            sp.darken_color("#123456", -1.0)

    def test_hex_to_rgb_rejects_invalid_hex_chars(self):
        with pytest.raises(ValueError, match="无效 HEX 颜色"):
            sp.hex_to_rgb("#GGGGGG")

    def test_generate_gradient_requires_integer_n(self):
        with pytest.raises(ValueError, match="n 必须是整数"):
            sp.generate_gradient("#000000", "#ffffff", 2.5)


class TestSmartUtilityHardening:
    def test_auto_rotate_labels_rejects_invalid_axis(self, cleanup_figures):
        fig, ax = plt.subplots()
        ax.plot([1, 2], [1, 2])
        with pytest.raises(ValueError, match="axis"):
            sp.auto_rotate_labels(ax, axis="z")

    def test_smart_legend_rejects_non_positive_ncols(self, cleanup_figures):
        fig, ax = plt.subplots()
        ax.plot([1, 2], [1, 2], label="line")
        with pytest.raises(ValueError, match="ncols"):
            sp.smart_legend(ax, ncols=0)

    def test_suggest_figsize_rejects_invalid_item_width(self):
        with pytest.raises(ValueError, match="item_width"):
            sp.suggest_figsize(10, item_width=0)

    def test_suggest_figsize_rejects_invalid_height_ratio(self):
        with pytest.raises(ValueError, match="height_ratio"):
            sp.suggest_figsize(10, height_ratio=-1)

    def test_check_color_contrast_rejects_invalid_threshold_and_hex(self):
        with pytest.raises(ValueError, match="threshold"):
            sp.check_color_contrast("#ffffff", "#000000", threshold=0)
        with pytest.raises(ValueError, match="bg_color"):
            sp.check_color_contrast("#ZZZ", "#000000")
