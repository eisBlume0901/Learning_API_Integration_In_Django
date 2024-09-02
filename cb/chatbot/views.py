from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chatbot(request):
    return render(request, 'chatbot.html')