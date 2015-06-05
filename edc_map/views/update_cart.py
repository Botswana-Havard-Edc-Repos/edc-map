from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def update_cart(request, **kwargs):
    """Removes item identifier(s) from cart.

    Uses template :template:`bhp_map/templates/view_cart.html`
    """

    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        update_error = 0
        items = []
        payload = []
        message = None
        deleted_ids = request.POST.getlist('identifiers')
        # We have item identifiers to remove from cart
        if deleted_ids:
            if len(deleted_ids) == 0:
                message = "Please select at least one Item to remove from the cart"
                update_error = 1
            else:
                if 'identifiers' in request.session:
                    a = request.session['identifiers']
                    request.session['identifiers'] = [x for x in a if x not in deleted_ids]
                    message = "{0} was/were removed".format(mapper.session_to_string(deleted_ids, False))
        identifiers = request.session['identifiers']
        cart_size = len(request.session['identifiers'])
        icon = request.session.get('icon', None)
        option = request.POST.get('option', 'save')
        if option == 'preview':
            items = mapper.item_model.objects.filter(**{'{0}__in'.format(mapper.identifier_field_attr): identifiers, mapper.item_selected_field: 1})
            icon = request.session['icon']
            payload = mapper.prepare_map_points(items,
                icon,
                request.session['identifiers'],
                'egg-circle'
                )
        return render_to_response(
            'view_cart.html', {
                'payload': payload,
                'mapper_name': mapper_name,
                'identifiers': identifiers,
                'cart_size': cart_size,
                'selected_icon': icon,
                'message': message,
                'option': option,
                'update_error': update_error
                },
                context_instance=RequestContext(request)
            )
