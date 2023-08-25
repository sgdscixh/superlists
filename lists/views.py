""" views for lists app """
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from lists.models import Item


# Create your views here.
def home_page(request: HttpRequest) -> HttpResponse:
    """home page view"""
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/the-only-list-in-the-world/")

    return render(request, "home.html")


def view_list(request: HttpRequest) -> HttpResponse:
    """view list"""
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
