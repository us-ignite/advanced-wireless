from django.shortcuts import render
from django.template.response import TemplateResponse
from models import *
# Create your views here.


def reverse_pitch(request):
    # "Static" text here. OPTIONAL
    intro = "Donec sed odio dui. Maecenas faucibus mollis interdum. Maecenas sed diam eget risus varius blandit" \
            " sit amet non magna. Integer posuere erat a ante venenatis dapibus posuere velit aliquet."
    desc = "Praesent commodo cursus magna, vel scelerisque nisl consectetur et. Lorem ipsum dolor sit amet," \
           " consectetur adipiscing elit. Aenean lacinia bibendum nulla sed consectetur." \
           " Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. " \
           "Vestibulum id ligula porta felis euismod semper." \
           " Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor." \
           " Cras mattis consectetur purus sit amet fermentum. Duis mollis," \
           " est non commodo luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit." \
           " Aenean lacinia bibendum nulla sed consectetur. Integer posuere erat a ante venenatis dapibus posuere velit aliquet." \
           "Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor." \
           " Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh," \
           " ut fermentum massa justo sit amet risus. Praesent commodo cursus magna," \
           " vel scelerisque nisl consectetur et. Maecenas sed diam eget risus varius blandit sit amet non magna." \
           " Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus."

    pitch_list = Pitch.objects.filter(active=True).order_by('order').all()[:6]
    context = {
        'intro': intro,
        'desc': desc,
        'pitch_list': pitch_list
    }

    return TemplateResponse(request, 'smart_gigabit_communities/reverse_pitch.html', context)
