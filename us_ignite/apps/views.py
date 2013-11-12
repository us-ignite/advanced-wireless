from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse


from us_ignite.apps.forms import ApplicationForm, ApplicationLinkFormSet
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


def get_app_for_user(slug, user):
    """Validates the user can access the given app."""
    app = get_object_or_404(Application.active, slug__exact=slug)
    # Application is published, no need for validation:
    if app.is_visible_by(user):
        return app
    raise Http404


def app_detail(request, slug):
    app = get_app_for_user(slug, request.user)
    context = {
        'object': app,
        'can_edit': app.is_editable_by(request.user)
    }
    return TemplateResponse(request, 'apps/object_detail.html', context)


@login_required
def app_add(request):
    """View for adding an ``Application``."""
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            messages.success(
                request, 'The application "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ApplicationForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'apps/object_add.html', context)


@login_required
def app_edit(request, slug):
    app = get_object_or_404(Application.active, slug__exact=slug)
    if not app.is_editable_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=app)
        formset = ApplicationLinkFormSet(request.POST, instance=app)
        if form.is_valid() and formset.is_valid():
            instance = form.save()
            formset.save()
            messages.success(
                request, 'The application "%s" has been updated.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ApplicationForm(instance=app)
        formset = ApplicationLinkFormSet(instance=app)
    context = {
        'object': app,
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(request, 'apps/object_edit.html', context)
