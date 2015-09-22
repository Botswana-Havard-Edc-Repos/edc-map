from edc_map.classes.controller import site_mappers

from .mappers import TestPlotMapper1, TestPlotMapper2, TestPlotMapper3

site_mappers.register(TestPlotMapper1)
site_mappers.register(TestPlotMapper2)
site_mappers.register(TestPlotMapper3)
