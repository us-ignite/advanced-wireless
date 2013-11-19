from django.template.response import TemplateResponse


def custom_404(request):
    return TemplateResponse(request, '404.html', {}, status=404)


def custom_500(request):
    return TemplateResponse(request, '500.html', {}, status=500)
