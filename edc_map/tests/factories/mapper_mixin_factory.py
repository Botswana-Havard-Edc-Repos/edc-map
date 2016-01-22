import factory

from ...models import MapperMixin


class MapperMixinFactory(factory.DjangoModelFactory):

    class Meta:
        model = MapperMixin

    gps_target_lon = factory.Sequence(lambda n: '2.123{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '2.12345{0}'.format(n))
