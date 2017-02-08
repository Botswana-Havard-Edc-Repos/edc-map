from faker import Faker
from model_mommy.recipe import Recipe

from edc_map.models import Section

fake = Faker()


section_polygon = [
    [-24.649897, 25.927687], [-24.650940, 25.922548],
    [-24.654294, 25.919158], [-24.658776, 25.919190],
    [-24.658376, 25.928771], [-24.649897, 25.927687]]
sub_section_polygon = [
    [-24.654203, 25.923278], [-24.657879, 25.923310],
    [-24.657889, 25.926164], [-24.654242, 25.926207],
    [-24.654203, 25.923278]]

section = Recipe(
    Section,
    section_name='A',
    sub_section_name='1',
    map_area='test_community',
    sub_section_polygon=sub_section_polygon,
    section_polygon=section_polygon
)
