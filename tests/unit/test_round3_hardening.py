"""
Round-3 hardening tests for global-context safety and remaining edge cases.
"""

from __future__ import annotations

import numpy as np
import pytest

import sciplot as sp
from sciplot._ext import plot3d
from sciplot._core.style import get_current_lang


class TestContextHardening:
    def test_style_context_enter_failure_does_not_leak_stack(self):
        # 非法 rcParams 应触发 __enter__ 失败，但上下文状态必须回滚。
        with pytest.raises(KeyError):
            with sp.style_context(non_existing_rc_key=1):
                pass

        assert sp.StyleContext.is_in_context() is False

    def test_setup_style_invalid_lang_does_not_pollute_global_lang(self):
        try:
            sp.setup_style(lang="en")
            assert get_current_lang() == "en"

            with pytest.raises(ValueError):
                sp.setup_style(lang="invalid-lang")

            assert get_current_lang() == "en"
        finally:
            sp.setup_style(lang="zh")


class TestBasicPlotHardening:
    def test_plot_multi_line_validates_x_list_length(self, cleanup_figures):
        x_list = [np.arange(3)]
        y_list = [np.arange(3), np.arange(3)]

        with pytest.raises(ValueError):
            sp.plot_multi_line(x_list, y_list)

    def test_plot_scatter_validates_length_mismatch(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_scatter(np.array([1, 2, 3]), np.array([1, 2]))


class TestPolarHardening:
    def test_plot_radar_rejects_nan_values(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_radar(["A", "B"], [[np.nan, 1.0]])


class Test3DHardening:
    def test_plot_3d_scatter_validates_lengths(self, cleanup_figures):
        with pytest.raises(ValueError):
            plot3d.plot_3d_scatter(
                np.array([1, 2, 3]),
                np.array([1, 2, 3]),
                np.array([1, 2]),
            )

    def test_plot_surface_validates_grid_shape(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(8).reshape(2, 4)
        with pytest.raises(ValueError):
            plot3d.plot_surface(X, Y, Z)

    def test_plot_contour_validates_grid_shape(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(8).reshape(2, 4)
        with pytest.raises(ValueError):
            plot3d.plot_contour(X, Y, Z)

    def test_plot_wireframe_validates_grid_shape(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(8).reshape(2, 4)
        with pytest.raises(ValueError):
            plot3d.plot_wireframe(X, Y, Z)

    def test_plot_contour_rejects_non_positive_levels(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(9).reshape(3, 3)
        with pytest.raises(ValueError, match="levels"):
            plot3d.plot_contour(X, Y, Z, levels=0)

    def test_plot_contour_rejects_invalid_levels_type(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(9).reshape(3, 3)
        with pytest.raises(ValueError, match="levels"):
            plot3d.plot_contour(X, Y, Z, levels=0.5)

    def test_plot_wireframe_rejects_non_positive_rstride(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(9).reshape(3, 3)
        with pytest.raises(ValueError, match="rstride"):
            plot3d.plot_wireframe(X, Y, Z, rstride=0)

    def test_plot_wireframe_rejects_non_positive_cstride(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(9).reshape(3, 3)
        with pytest.raises(ValueError, match="cstride"):
            plot3d.plot_wireframe(X, Y, Z, cstride=0)

    def test_plot_wireframe_rejects_non_int_stride(self, cleanup_figures):
        X, Y = np.meshgrid(np.arange(3), np.arange(3))
        Z = np.arange(9).reshape(3, 3)
        with pytest.raises(ValueError, match="rstride"):
            plot3d.plot_wireframe(X, Y, Z, rstride=1.5)


class TestNetworkHardening:
    def test_plot_network_from_matrix_requires_square(self):
        matrix = np.array([[1, 0, 1], [0, 1, 0]])
        with pytest.raises(ValueError):
            sp.plot_network_from_matrix(matrix)


class TestLayoutLangHardening:
    def test_create_subplots_preserves_current_lang(self, cleanup_figures):
        try:
            sp.setup_style(lang="en")
            sp.create_subplots(1, 1, venue="nature")
            assert get_current_lang() == "en"
        finally:
            sp.setup_style(lang="zh")

    def test_paper_subplots_preserves_current_lang(self, cleanup_figures):
        try:
            sp.setup_style(lang="en")
            sp.paper_subplots(1, 1, venue="nature")
            assert get_current_lang() == "en"
        finally:
            sp.setup_style(lang="zh")

    def test_create_gridspec_preserves_current_lang(self, cleanup_figures):
        try:
            sp.setup_style(lang="en")
            sp.create_gridspec(1, 1, venue="nature")
            assert get_current_lang() == "en"
        finally:
            sp.setup_style(lang="zh")
