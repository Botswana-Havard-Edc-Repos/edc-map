from ..models import Container, InnerContainer


class MapTestHelper:

    def allocate_objects_to_device(self, object_list=None, object_attr=None, device_id=None, map_area=None):
        object_attr = object_attr or 'plot_identifier'
        map_area = map_area or 'test_community'
        device_id = device_id or '99'
        object_labels = ','.join(
            [getattr(obj, object_attr) for obj in object_list])
        container = Container.objects.create(map_area=map_area)
        InnerContainer.objects.create(
            container=container,
            map_area=map_area,
            device_id=device_id,
            labels=object_labels)
