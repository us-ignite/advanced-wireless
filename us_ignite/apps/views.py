from django.template.response import TemplateResponse

from us_ignite.apps.models import Application
from us_ignite.common import pagination, forms


APPS_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('name', 'Name a-z'),
    ('-name', 'Name z-a'),
)


def app_list(request):
    """Lists the published ``Applications``"""
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=APPS_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Application.objects.filter(status=Application.PUBLISHED)
    if order_value:
        # TODO consider using non case-sensitive ordering:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
        'order_form': order_form,
    }
    return TemplateResponse(request, 'apps/object_list.html', context)
