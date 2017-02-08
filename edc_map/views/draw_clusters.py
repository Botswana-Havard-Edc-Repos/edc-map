from django.views.generic.base import TemplateView


class DrawCluster(TemplateView):

    template_name = 'edc_map/base_map.html'
    draw_cluster_view_base_html = 'edc_base/base.html'

    def get_context_data(self, **kwargs):
        context = super(DrawCluster, self).get_context_data(**kwargs)
        items = [[-24.659267, 25.924107, '1231231']]
        context.update(items=items)
        return context
