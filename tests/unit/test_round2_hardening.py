"""
Round-2 hardening tests for plots and extension edge cases.
"""

from __future__ import annotations

from datetime import date

import matplotlib.dates as mdates
import numpy as np
import pytest

import sciplot as sp


class TestStatisticalHardening:
    def test_plot_qq_supports_t_distribution(self, cleanup_figures):
        data = np.random.randn(200)
        result = sp.plot_qq(data, distribution="t")
        assert result.fig is not None


class TestHierarchicalHardening:
    def test_clustermap_single_row_does_not_fail(self, cleanup_figures):
        data = np.random.rand(1, 5)
        result = sp.plot_clustermap(data, row_cluster=True, col_cluster=True)
        assert result.fig is not None

    def test_clustermap_single_column_does_not_fail(self, cleanup_figures):
        data = np.random.rand(5, 1)
        result = sp.plot_clustermap(data, row_cluster=True, col_cluster=True)
        assert result.fig is not None


class TestMultivariateHardening:
    def test_plot_parallel_color_by_index_out_of_range(self, cleanup_figures):
        data = np.random.rand(10, 3)
        with pytest.raises(ValueError):
            sp.plot_parallel(data, color_by=5)

    def test_plot_parallel_rejects_non_numeric_data(self, cleanup_figures):
        data = np.array([["a", "b"], ["c", "d"]], dtype=object)
        with pytest.raises(ValueError):
            sp.plot_parallel(data)

    def test_plot_parallel_zscore_not_clipped(self, cleanup_figures):
        data = np.array(
            [
                [0.0, 0.0, 0.0],
                [1.0, 1.0, 1.0],
                [2.0, 2.0, 2.0],
                [10.0, 10.0, 10.0],
            ]
        )
        result = sp.plot_parallel(data, normalize="zscore")
        y_min, y_max = result.ax.get_ylim()
        assert y_max > 1.05
        assert y_min < -0.05


class TestDistributionHardening:
    def test_plot_combo_validates_bar_lengths(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_combo(["A", "B"], bar_data={"series": [1]})

    def test_plot_combo_validates_line_lengths(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_combo(
                ["A", "B"],
                bar_data={"bar": [1, 2]},
                line_data={"line": [1]},
            )

    def test_plot_violin_rejects_empty_group(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_violin([np.array([]), np.array([1.0, 2.0, 3.0])])


class TestAdvancedHardening:
    def test_plot_heatmap_requires_2d_input(self, cleanup_figures):
        with pytest.raises(ValueError):
            sp.plot_heatmap(np.array([1, 2, 3]))

    def test_plot_heatmap_validates_label_lengths(self, cleanup_figures):
        matrix = np.random.rand(3, 4)
        with pytest.raises(ValueError):
            sp.plot_heatmap(matrix, row_labels=["r1"])
        with pytest.raises(ValueError):
            sp.plot_heatmap(matrix, col_labels=["c1"])


class TestTimeseriesHardening:
    def test_plot_timeseries_recognizes_date_objects(self, cleanup_figures):
        t = [date(2024, 1, d) for d in range(1, 8)]
        y = np.arange(7)

        result = sp.plot_timeseries(t, y)
        formatter = result.ax.xaxis.get_major_formatter()
        assert isinstance(formatter, mdates.DateFormatter)

    def test_plot_timeseries_requires_event_time(self, cleanup_figures):
        t = np.arange(5)
        y = np.arange(5)
        with pytest.raises(ValueError, match="events\\[0\\].*time"):
            sp.plot_timeseries(t, y, events=[{"label": "missing time"}])

    def test_plot_timeseries_requires_region_bounds(self, cleanup_figures):
        t = np.arange(5)
        y = np.arange(5)
        with pytest.raises(ValueError, match="shade_regions\\[0\\].*start"):
            sp.plot_timeseries(t, y, shade_regions=[{"end": 3}])

    def test_plot_multi_timeseries_requires_event_time(self, cleanup_figures):
        t = np.arange(5)
        y_list = [np.arange(5), np.arange(5) + 1]
        with pytest.raises(ValueError, match="events\\[0\\].*time"):
            sp.plot_multi_timeseries(t, y_list, events=[{"label": "missing time"}])

    def test_plot_timeseries_rejects_non_int_rolling_mean(self, cleanup_figures):
        t = np.arange(5)
        y = np.arange(5)
        with pytest.raises(TypeError, match="rolling_mean"):
            sp.plot_timeseries(t, y, rolling_mean="3")


class TestSlopeHardening:
    def test_plot_slope_rejects_non_finite_values(self, cleanup_figures):
        with pytest.raises(ValueError, match="不能包含 NaN 或 Inf"):
            sp.plot_slope(["A", "B"], [np.nan, 1.0], [2.0, 3.0])
