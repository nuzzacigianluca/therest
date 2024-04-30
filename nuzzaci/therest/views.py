from django.shortcuts import render

# Create your views here.
def therest(request):
    return render(request, 'therest/index.html')

def aboutview(request):
    return render(request, 'therest/about.html')

def bookview(request):
    return render(request, 'therest/book.html')