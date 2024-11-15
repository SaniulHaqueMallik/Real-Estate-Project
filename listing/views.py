from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from listing.choices import bedroom_choices, price_choices, state_choices



# Create your views here.
def listings(request):
    listing = Listing.objects.all().order_by('-list_date').filter(is_published = True)

    paginator = Paginator(listing, per_page= 3)
    page = request.GET.get('page',1)
    paged_listing = paginator.get_page(page)

    context = {
        'listing': paged_listing
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing' : listing
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    query_set = Listing.objects.order_by('-list_date')
    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query_set = query_set.filter(description__icontains = keywords)
            
    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_set = query_set.filter(city__iexact = city)
            
    # state
    if 'state' in request.GET:
        state = request.GET['state']
        query_set = query_set.filter(state__iexact = state)
    
    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_set = query_set.filter(bedrooms__lte = bedrooms)  
            
    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_set = query_set.filter(price__lte = price)
            
     
    context =  {
        'bedroom_choices':bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'listing': query_set,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
