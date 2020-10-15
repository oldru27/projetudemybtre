from django.test import TestCase
from .models import Listing


listings = Listing.objects.order_by('-list_date').filter(is_published=True)

# Create your tests here.
