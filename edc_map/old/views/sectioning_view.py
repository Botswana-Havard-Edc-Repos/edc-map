from django.views.generic.base import TemplateView

from ..classes import site_mappers, Sectioning
from ..constants import SECTIONS, SUB_SECTIONS


class SectioningView(TemplateView):

    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        context = super(SectioningView, self).get_context_data(kwargs)
        mapper_name = site_mappers.current_community
        mapper = site_mappers.get_mapper(mapper_name)
        sectioning = Sectioning()
        items = []
        item_identifiers = self.request.GET.get('identifiers')
        section = self.request.GET.get('section', '')
        sub_section = self.request.GET.get('sub_section')
        sections = SECTIONS
        sub_sections = SUB_SECTIONS
        if item_identifiers:
            item_identifiers = item_identifiers.split(",")
            items = mapper.item_model.objects.filter(
                **{'{0}__in'.format(mapper.identifier_field_attr): item_identifiers})
            for item in items:
                item.section = section
                item.save()
        items = mapper.item_model.objects.filter(section__isnull=True, area_name=mapper_name)
        locations = sectioning.prepare_map_points(items)
        landmarks = mapper.landmarks
        context.update({
            'mapper': mapper,
            'item_identifiers': item_identifiers,
            'section': section,
            'sub_section': sub_section,
            'locations': locations,
            'landmarks': landmarks,
            'sections': sections,
            'sub_sections': sub_sections,
        })
        return context

#     def post(self, request, *args, **kwargs):
#         self.context.update({
#         })
#         return render_to_response(self.template_name, self.context, context_instance=RequestContext(request))
