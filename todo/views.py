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
    return redirect(f'/lists/{list_.id}')

def list_items(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'todo/list.html', {'items':items})

def add_item(request, list_id):
    """
    Funcion para añadir un nuevo item a una lista existente
    """
    list_ = List.objects.get(id=list_id)
    item = Item.objects.create(text = request.POST['item_text'], list = list_)    
    return redirect(f'/lists/{list_.id}')
