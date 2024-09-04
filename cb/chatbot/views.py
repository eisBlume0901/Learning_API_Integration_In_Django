from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from django.contrib.auth import authenticate, login
from .forms import *

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
    if request.method == 'POST':
        message = request.POST.get('message')  
        response = ask_googlegenerativeai(message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html')

def login(request):

    return render(request, 'login.html')

def register(request):
    form = CustomUserCreationForm()

    content = {
        "form": form
    }
    return render(request, 'register.html', content)