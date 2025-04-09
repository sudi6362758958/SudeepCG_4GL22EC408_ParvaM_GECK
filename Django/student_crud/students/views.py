from django.shortcuts import render

def index(request):
    return render(request, 'students/index.html')

def about(request):
    return render(request, 'students/about.html')

def servies(request):           #file as same as the name of the function ex: def servies(request):  if we give "serveice" it will not work
    return render(request, 'students/servies.html')   #give file name as same as the function name

def contact(request):
    return render(request, 'students/contact.html')