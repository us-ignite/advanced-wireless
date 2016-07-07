from django.template.response import TemplateResponse
from us_ignite.mailinglist.views import *
from forms import EmailForm

def awt_frontpage(request):
    form = EmailForm()
    if request.method == 'POST':
        mailing_subscribe(request, 'awt')
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'awtmicrosite.html', context)
