# coding=utf-8

from faker import Faker
from model_mommy.recipe import Recipe

from .models import Container, InnerContainer

fake = Faker()

container = Recipe(
    Container,
    name='A',
    map_area=',2000009-7,2000007-1,200974-04,2000091-5,201693-08',
    boundry='-25.32022065053892,25.26476764550216|-25.317028720815934,25.25984287261963|-25.326649141869385,25.268490314483643|',
    labels=None)

inner_container = Recipe(
    InnerContainer,
    name='1',
    device_id='10',
    map_area=',2000009-7,2000007-1,2000091-5,201693-08',
    boundry='-25.32022065053892,25.26476764550216|-25.317028720815934,25.25984287261963|-25.326649141869385,25.268490314483643|',
    labels=None)
