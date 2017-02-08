from django.shortcuts import render
from django.template.response import TemplateResponse
from models import *
import random
# Create your views here.


def reverse_pitch(request):
    # "Static" text here. OPTIONAL
    intro = "US Ignite Will Convene Reverse Pitch Events in Nine Communities Throughout the United States "
    desc = "From Arizona to Texas to Vermont, US Ignite will co-host and sponsor multiple reverse pitch events for technologists and entrepreneurs throughout February and March. This reverse pitch competition is for makers, developers and entrepreneurs developing ultra high-bandwidth hardware, software and applications that want to impact their local community. Entrepreneurs will hear pitches from civic organizations and then compete for part of a prize pool of cash and in-kind services. US Ignite will co-sponsor these events in nine of the organization's Smart Gigabit Communities, which are a network of communities nationwide that have each committed to leverage next-generation smart city and Internet technologies to keep pace with the world's rapidly changing, technology-driven economy."

    random_int = random.uniform(0.1, 2.0)
    pitch_list = Pitch.objects.filter(active=True).order_by('order').all()[:6]
    context = {
        'intro': intro,
        'desc': desc,
        'pitch_list': pitch_list,
        'random_int': random_int
    }

    return TemplateResponse(request, 'smart_gigabit_communities/reverse_pitch.html', context)
