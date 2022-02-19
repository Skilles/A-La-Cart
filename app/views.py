from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def db(request):
    # Display every product in the database
    products = Product.objects.all()
    return render(request, "db.html", {'products': products})
