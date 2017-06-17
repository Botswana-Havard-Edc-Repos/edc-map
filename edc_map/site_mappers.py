import copy
import sys

from collections import OrderedDict

from django.apps import apps as django_apps
from django.conf import settings
from django.utils.module_loading import import_module
from django.utils.module_loading import module_has_submodule

from .exceptions import MapperError, AlreadyRegistered


class SiteMapperInvalidMapArea(Exception):
    pass


class SiteMapperError(Exception):
    pass


class SiteMappers(object):

    """ Main controller of :class:`Mapping` objects.
    """

    def __init__(self, current_map_area=None):
        self.loaded = False
        self.registry = OrderedDict()
        self.registry_by_code = OrderedDict()
        self.autodiscovered = False
        self._current_map_area = current_map_area

    def __repr__(self):
        return 'Controller({0.current_map_area})'.format(self)

    def __str__(self):
        return '{0.current_map_area} {0.map_code}'.format(self)

    def __iter__(self):
        return self.registry.itervalues()

    def register(self, mapper_cls=None):
        """Registers a given mapper class to the site registry.
        """
        self.loaded = True
#         if not issubclass(mapper_cls, Mapper):
#             raise SiteMapperError('Expected a subclass of Mapper.')
        if not mapper_cls.map_area or not mapper_cls.map_code:
            raise SiteMapperError(
                'Mapper class {0} is not correctly configured.'.format(mapper_cls))
        if mapper_cls.map_area in self.registry:
            raise AlreadyRegistered(
                'The mapper class {0} is already registered ({1}, {2})'.format(
                    mapper_cls, mapper_cls.map_area, mapper_cls.map_code))
        if mapper_cls.map_code in [m.map_code for m in self.registry.values()]:
            raise AlreadyRegistered(
                'The mapper class {0} is already registered ({1}, {2})'.format(
                    mapper_cls, mapper_cls.map_area, mapper_cls.map_code))
        self.registry[mapper_cls.map_area] = mapper_cls()
        self.registry_by_code[mapper_cls.map_code] = mapper_cls()

    def get_mapper(self, value):
        """Returns a mapper class or raises for the given mapper
        name (map_area) or code (map_code).
        """
        try:
            mapper = self.registry[value]
        except KeyError:
            try:
                mapper = self.registry_by_code[value]
            except KeyError:
                raise SiteMapperError(
                    f'Invalid mapper map_area or map_code. Got \'{value}\'')
        return mapper

    @property
    def current_map_code(self):
        return self.current_mapper.map_code

    @property
    def current_map_area(self):
        if not self._current_map_area:
            try:
                self._current_map_area = settings.CURRENT_MAP_AREA
            except AttributeError:
                raise SiteMapperInvalidMapArea(
                    'Unable to determine the current map area. See setting.CURRENT_MAP_AREA')
        return self._current_map_area

    @property
    def current_mapper(self):
        """Loads the current mapper based on the current_map_area.
        """
        try:
            current_mapper = self.registry.get(self.current_map_area)
        except AttributeError:
            current_mapper = None
        if not current_mapper:
            raise SiteMapperError(
                'Unable to load the mapper for the current community. Got {} not registered ({})'.format(
                    self.current_map_area, self.registry.keys()))
        elif current_mapper.map_area != self.current_map_area:
            raise SiteMapperError(
                'Unable to load the current mapper. Current community does not match the '
                'mapper class. Got {0} != {1}'.format(
                    self.current_map_area, self.current_mapper.map_area))
        return current_mapper

    def sort_by_code(self):
        """Sorts the registries by map_code.
        """
        codes = []
        mappers = OrderedDict()
        mappers_by_code = OrderedDict()
        for mapper in self.registry_by_code.itervalues():
            codes.append(mapper.map_code)
        codes.sort()
        for code in codes:
            mappers.update({self.registry_by_code.get(
                code).map_area: self.registry_by_code.get(code)})
            mappers_by_code.update({self.registry_by_code.get(
                code).map_code: self.registry_by_code.get(code)})
        self.registry = mappers
        self.registry_by_code = mappers_by_code

    def sort_by_pair(self):
        pairs = []
        mappers = OrderedDict()
        for mapper in self.registry.itervalues():
            pairs.append(mapper.pair)
        pairs = list(set(pairs))
        for pair in pairs:
            for mapper in self.registry.itervalues():
                if mapper.pair == pair:
                    mappers[mapper.map_area] = mapper
        return mappers

    def get_by_pair(self, pair):
        """Returns a dictionary of mappers by pair.
        """
        mappers = {}
        for mapper in self.registry.itervalues():
            if mapper.pair == pair:
                mappers.update({mapper.map_area: mapper})
        return mappers

    def get_by_code(self, code):
        """Returns a mapper class for the given mapper code (map_code)."""
        return self.registry_by_code.get(code)

    @property
    def map_codes(self):
        map_codes = [m.map_code for m in self.registry.values()]
        map_codes.sort()
        return map_codes

    @property
    def map_areas(self):
        map_areas = [map_area for map_area in self.registry]
        map_areas.sort()
        return map_areas

    def autodiscover(self, module_name=None):
        """Autodiscovers mapper classes in the mapper.py file
        of any INSTALLED_APP.
        """
        module_name = module_name or 'mappers'
        sys.stdout.write(f' * checking for site {module_name} ...\n')
        for app in django_apps.app_configs:
            sys.stdout.write(f' * searching {app}           \r')
            try:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_mappers.registry)
                    import_module(f'{app}.{module_name}')
                    sys.stdout.write(
                        f' * registered mappers \'{module_name}\' from \'{app}\'\n')
                except MapperError:
                    site_mappers.registry = before_import_registry
                    if module_has_submodule(mod, module_name):
                        raise
            except ImportError:
                pass


site_mappers = SiteMappers()
