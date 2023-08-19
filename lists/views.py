from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    """home page"""

    return HttpResponse("<html><title>To-Do lists</title></html>")
