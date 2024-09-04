from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages

# Load environment variables from .env file
load_dotenv()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def ask_googlegenerativeai(message):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="""Your name is AmberAI, a vibrant and cheerful character AI. 
        You are friendly and helpful to users especially to those that needs your assistance. 
        Always add emojis to your response to make it fun and engaging for users."""
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(message)
    model_response = response.text
    return model_response

def amberai(request):
    user = get_object_or_404(User, username=request.user.username)
    
    if request.method == 'POST':
        message = request.POST.get('message')  
        response = ask_googlegenerativeai(message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html', {'user': user})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f'Welcome back {username}!')
                return redirect('amberai')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html', {'form': form})

def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account was created successfully for {user}')
            return redirect('login')
        else:
            messages.error(request, "There was an error creating the account. Please try again.")

    return render(request, 'register.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('login')