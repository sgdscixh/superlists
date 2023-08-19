""" views for lists app """
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    """home page"""

    return render(request, "home.html")
