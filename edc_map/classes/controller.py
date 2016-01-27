import copy

from collections import OrderedDict

from django.conf import settings
try:
    # Django versions >= 1.9
    from django.utils.module_loading import import_module
except ImportError:
    # Django versions < 1.9
    from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from ..exceptions import MapperError, AlreadyRegistered

from .mapper import Mapper


class Controller(object):

    """ Main controller of :class:`Mapping` objects. """

    def __init__(self, current_community=None):
        self.registry = OrderedDict()
        self.registry_by_code = OrderedDict()
        self.autodiscovered = False
        self.current_mapper = None
        self.current_community = current_community
        try:
            if not self.current_community:
                self.current_community = settings.CURRENT_COMMUNITY
        except AttributeError:
            pass

    def __repr__(self):
        return 'Controller({0.current_community})'.format(self)

    def __str__(self):
        return '{0.current_community} {0.map_code}'.format(self)

    def __iter__(self):
        return self.registry.itervalues()

    def register(self, mapper_cls):
        """Registers a given mapper class to the site registry."""
        if not issubclass(mapper_cls, Mapper):
            raise MapperError('Expected a subclass of Mapper.')
        if not mapper_cls.map_area or not mapper_cls.map_code:
            raise MapperError('Mapper class {0} is not correctly configured.'.format(mapper_cls))
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
        if self.current_community == mapper_cls.map_area:
            self.load_current_mapper(mapper_cls())

    def get_mapper(self, value):
        """Returns a mapper class for the given mapper name (map_area) or code (map_code)."""
        return self.registry.get(value) or self.registry_by_code.get(value)

    def load_current_mapper(self, mapper=None):
        """Loads the current mapper."""
        self.current_mapper = mapper or self.registry.get(self.current_community)
        if not self.current_mapper:
            raise MapperError(
                'Unable to load the mapper for the current community. Got {} not registered ({})'.format(
                    self.current_community, self.registry.keys()))
        elif self.current_mapper.map_area != self.current_community:
            raise MapperError(
                'Unable to load the current mapper. Current community does not match the '
                'mapper class. Got {0} != {1}'.format(
                    self.current_community, self.current_mapper.map_area))

    def sort_by_code(self):
        """Sorts the registries by map_code."""
        codes = []
        mappers = OrderedDict()
        mappers_by_code = OrderedDict()
        for mapper in self.registry_by_code.itervalues():
            codes.append(mapper.map_code)
        codes.sort()
        for code in codes:
            mappers.update({self.registry_by_code.get(code).map_area: self.registry_by_code.get(code)})
            mappers_by_code.update({self.registry_by_code.get(code).map_code: self.registry_by_code.get(code)})
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
        """Returns a dictionary of mappers by pair."""
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
        """Autodiscovers mapper classes in the mapper.py file of any INSTALLED_APP."""
        if not self.autodiscovered:
            module_name = module_name or 'mappers'
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_mappers.registry)
                    import_module('{}.{}'.format(app, module_name))
                except:
                    site_mappers.registry = before_import_registry
                    if module_has_submodule(mod, module_name):
                        raise
            self.autodiscovered = True
            self.autodiscovered = True

site_mappers = Controller()
