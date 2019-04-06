from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>This is customer home page</h1>')