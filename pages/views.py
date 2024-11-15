from django.shortcuts import render
from listing.models import Listing
from realtors.models import Realtor
from listing.choices import bedroom_choices, price_choices, state_choices

# Create your views here.
def index(request):
    listings = Listing.objects.filter(is_published = True).order_by('-list_date')[:3]
    context = {
        'listings': listings,
        'bedroom_choices':bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices   
    }
    print(context)
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.all().order_by('-hire_date')
    
    mvp_realtors = Realtor.objects.filter(is_mvp = True)
    
    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)