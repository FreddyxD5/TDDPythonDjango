from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    """
    return homepage
    """
    # if request.method == 'POST':
    #     return render(request,'todo/home.html',{'new_item_text':request.POST['item_text']})
    print('bro wtf')
    print(request.POST.get('item_text'))
    return render(request,'todo/home.html',{'new_item_text':request.POST.get('item_text', ''),})
