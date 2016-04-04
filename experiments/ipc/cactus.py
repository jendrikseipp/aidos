# -*- coding: utf-8 -*-

from collections import defaultdict
import os

from lab import tools

from downward.reports.plot import PlotReport


class CactusPlotReport(PlotReport):
    """
    Generate a cactus plot for a specific attribute.
    """
    def __init__(self, get_category=None, min_value=None, max_value=None, **kwargs):
        """
        ``kwargs['attributes']`` must contain exactly one attribute.

        The plot groups runs, then sorts the runs within each category by
        the given attribute (non-numeric values and None-values are ignored).
        The values are then used to plot a line that starts at (0,0), uses the
        sorted values as x coordinates increasing y by one for every value.
        Filters can be used to determine what is counted on the y-axis. A
        typical example is to use ``filter_coverage=1`` to count solved tasks.
        Note that this will currently produce a warning, because not all tasks
        will be present for all configs, which can be safely ignored.

        *get_category* can be a function that takes a run (dictionary of
        properties) and returns a category name. This name is used to group the
        runs in the plot. By default, runs are grouped by config.
        For example, to group by a more meaningful name use::

            def config_description_as_category(run):
                if run['config'] == 'c8cb6ed18fce-astar_lmcut':
                    return 'A*/LM-cut'
                if run['config'] == 'c8cb6ed18fce-astar_blind':
                    return 'A*/blind'

        *get_category* and *category_styles*
        (see :py:class:`PlotReport <downward.reports.plot.PlotReport>`) are best
        used together to name and style the plotted lines::

            def config_description_as_category(run):
                if run['config'] == 'c8cb6ed18fce-astar_lmcut':
                    return 'A*/LM-cut'
                if run['config'] == 'c8cb6ed18fce-astar_blind':
                    return 'A*/blind'

            styles = {
                'A*/LM-cut': {'linestyle': '--', 'c':'black'},
                'A*/blind':  {'linestyle': '---', 'c':'red'},
            }

            CactusPlotReport(attributes=['total_time'],
                             filter_coverage=1,
                             ylabel='Coverage',
                             get_category=config_description_as_category,
                             category_styles=styles)

        The plot is restricted to values between *min_value* and *max_value* which
        default to 0 and the largest value present in the data. If *min_value* is
        smaller than the smallest value in a category, the y-value 0 is repeated
        from *min_value* to the smallest value. If *max_value* is larger than the
        largest value in a category, the last y-value of that category is repeated
        from the largest value to *max_value*.
        """
        kwargs.setdefault('legend_location', (1.3, 0.5))
        PlotReport.__init__(self, **kwargs)
        assert self.attribute, 'CactusPlotReport needs exactly one attribute'
        # By default use config as the category.
        self.get_category = get_category or (lambda run: run.get('config'))
        # The default for the range depends on the data so it is set later.
        self.min_value = min_value
        self.max_value = max_value

    def _set_scales(self, xscale, yscale):
        self.yscale = yscale or 'linear'
        if xscale:
            self.xscale = xscale
        elif self.attribute and self.attribute in self.LINEAR:
            self.xscale = 'linear'
        else:
            self.xscale = 'log'
        scales = ['linear', 'log', 'symlog']
        assert self.xscale in scales, self.xscale
        assert self.yscale in scales, self.yscale

    def _fill_categories(self, runs):
        # Map category names to value tuples
        grouped_values = defaultdict(list)
        smallest_value = float('inf')
        largest_value = -float('inf')
        for run in runs:
            val = run.get(self.attribute)
            if val is None or not isinstance(val, (int, float)):
                continue
            category = self.get_category(run)
            grouped_values[category].append(val)
            smallest_value = min(smallest_value, val)
            largest_value = max(largest_value, val)
        min_value = self.min_value or min(0, smallest_value)
        max_value = self.max_value or largest_value
        assert min_value < max_value, (min_value, max_value)
        categories = {}
        for category, values in grouped_values.items():
            coords = []
            values.sort()
            for value, y in zip(values, xrange(len(values))):
                if min_value <= value <= max_value:
                    coords.append((value, y))
                    coords.append((value, y + 1))
            if coords:
                coords.insert(0, (min_value, coords[0][1]))
                coords.append((max_value, coords[-1][1]))
            categories[category] = coords
        return categories

    def _prepare_categories(self, categories):
        return categories

    def write(self):
        self.xlabel = self.xlabel or self.attribute

        suffix = '.' + self.output_format
        if not self.outfile.endswith(suffix):
            self.outfile += suffix
        tools.makedirs(os.path.dirname(self.outfile))
        self._write_plot(self.runs.values(), self.outfile)
