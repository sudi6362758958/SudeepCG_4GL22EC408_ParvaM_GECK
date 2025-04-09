from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('servies', views.servies, name='servies'),
    path('contact', views.contact, name='contact-us'),  #here we can give any name to the url in main file of created 
                                                        #ex:-  <a class="nav-link" href="{% url 'contact-us'%}">contact</a> if we give contact_us is not provide output.

]   