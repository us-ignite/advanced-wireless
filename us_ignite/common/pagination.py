from django.core.paginator import Paginator, EmptyPage
from django.conf import settings


def get_page_no(payload):
    """Determines the page number from the payload."""
    page_no = payload.get('page', 1)
    try:
        page_no = int(page_no)
    except ValueError:
        page_no = 1
    if page_no < 1:
        page_no = 1
    return page_no


def get_page(object_list, page_no):
    """Returns a ``Paginator`` page with the given details."""
    paginator = Paginator(object_list, settings.PAGINATOR_PAGE_SIZE)
    try:
        page = paginator.page(page_no)
    except EmptyPage:
        page = paginator.page(1)
    return page

