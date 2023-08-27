""" views for lists app """
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from lists.models import Item, List


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    """home page view"""
    return render(request, "home.html")


def view_list(request: HttpRequest) -> HttpResponse:
    """view list"""
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest) -> HttpResponse:
    """new list"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect("/lists/the-only-list-in-the-world/")
