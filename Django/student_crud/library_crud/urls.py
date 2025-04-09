from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_list, name='library_list'),
    path('create', views.create_library, name='create_library'),
    path('<int:pk>', views.view_library, name='view_library'),
    path('<int:pk>/edit/', views.edit_library, name='edit_library'),
    path('<int:pk>/delete/', views.delete_library, name='delete_library'),
    path('search/', views.search_library, name='search_library'),
    
]