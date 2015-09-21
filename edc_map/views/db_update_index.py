from django.shortcuts import render_to_response
from django.template import RequestContext


def db_update_index(request, **kwargs):
    """Update coordinates of a item form
    """

    template = "db_update.html"

    return render_to_response(
                template, kwargs,
            context_instance=RequestContext(request)
        )
