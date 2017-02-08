from model_mommy import mommy
from django.test import TestCase

from ..models import Section
from django.contrib.auth.models import User


class TestSectionPolygon(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tuser', email='tuser@bhp.org.bw', password='top_secret@321')

    def test_section_polygon(self):
        """Test that a section instance gets created."""
        mommy.make_recipe(
            'edc_map.section',
            location_identifier='123123123',
            user=self.user
        )
        self.assertEqual(Section.objects.all().count(), 1)

    def test_section_polygon2(self):
        """Assert that polygon properties return lists."""
        section = mommy.make_recipe(
            'edc_map.section',
            location_identifier='123123123',
            user=self.user
        )
        section = Section.objects.get(id=section.id)
        self.assertTrue(type(section.section_polygon_list) is list)
        self.assertTrue(type(section.sub_section_polygon_list) is list)
