import itertools
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import redirect
# from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from ..classes import site_mappers
from ..exceptions import MapperError


def save_cart(request, **kwargs):
    """Dispatch items in shopping cart to netbook.
    """
    #Make sure we have identifiers in our session
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        if 'identifiers' in request.session:
            if len(request.session['identifiers']) > 0:
                identifiers = request.session['identifiers']
                pks = mapper.item_model.objects.filter(**{'{0}__in'.format(mapper.identifier_field_attr): identifiers}).values_list('pk')
                selected = list(itertools.chain(*pks))
                content_type = ContentType.objects.get_for_model(mapper.item_model)
                return HttpResponseRedirect("/dispatch/bcpp/?ct={0}&items={1}".format(content_type.pk, ",".join(selected)))
                try:
                    del request.session['identifiers']
                    del request.session['icon']
                except KeyError:
                    pass