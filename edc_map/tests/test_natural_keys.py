from django.test import TestCase

from edc_sync.tests import SyncTestHelper


class TestNaturalKey(TestCase):

    sync_test_helper = SyncTestHelper()

    def test_natural_key_attrs(self):
        self.sync_test_helper.sync_test_natural_key_attr(
            'edc_map',
            exclude_models=[
                'edc_map.landmark', 'edc_map.mapperdata', 'edc_map.testmodel'])

    def test_get_by_natural_key_attr(self):
        self.sync_test_helper.sync_test_get_by_natural_key_attr(
            'edc_map',
            exclude_models=[
                'edc_map.landmark', 'edc_map.mapperdata', 'edc_map.testmodel'])
