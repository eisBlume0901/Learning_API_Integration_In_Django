from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def chatbot(request):
    if request.method == 'POST':
        try:
            message = request.POST.get('message')
            history = request.POST.get('history', '[]') 
            print(history)           

            # Configure the API key
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

            # Create the model
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 200,
                "response_mime_type": "text/plain",
            }

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
            )

            # Convert history to the expected format
            formatted_history = []

            i = 0
            for entry in history:
                if i % 2 == 0:
                    formatted_history.append({"role": "user", "parts": entry})
                formatted_history.append({"role": "model", "parts": entry})
                i=i+1


            # Start a chat session with formatted history
            chat_session = model.start_chat(history=formatted_history)
            
            # Send the user's message and get the response
            response = chat_session.send_message(message)
            model_response = response.text

            formatted_history.append({"role": "model", "parts": model_response})

            return JsonResponse({'response': model_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return render(request, 'chatbot.html')