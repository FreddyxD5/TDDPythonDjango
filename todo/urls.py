from django.urls import path
from todo import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/new', views.new_list, name='new_list'),
    path('lists/<int:list_id>', views.list_items, name='list_items'),
    path('lists/the-only-list-in-the-world/', views.view_list, name='view_list')
]
