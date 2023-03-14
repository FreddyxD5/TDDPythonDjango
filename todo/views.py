"""
todo view
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from todo.models import Item, List

# Create your views here.

def home_page(request):
    """
    return homepage
    """
    return render(request,'todo/home.html')

def view_list(request):
    """
    Vista de lista de items
    """
    list_ = List.objects.create()
    items = Item.objects.all()
    return render(request, 'todo/list.html',{'items':items})

def new_list(request):
    """
    Nuevo item 
    """
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = list_)
    return redirect('/lists/the-only-list-in-the-world/')

def list_items(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'todo/list.html', {'items':items})
