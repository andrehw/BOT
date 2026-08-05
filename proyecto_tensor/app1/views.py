import os
import pickle
import json
import random
import numpy as np
import nltk
from nltk.stem import SnowballStemmer
from django.http import JsonResponse
from django.shortcuts import render
from tf_keras.models import load_model

# Configuración básica
stemmer = SnowballStemmer('spanish')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGICA_PATH = os.path.join(BASE_DIR, 'logica_chat')

# VARIABLES GLOBALES (Para que se carguen solo una vez en RAM)
MODELO = None
WORDS = None
CLASSES = None
INTENTS = None

def cargar_ia():
    global MODELO, WORDS, CLASSES, INTENTS
    if MODELO is None:
        print("--- Cargando Cerebro del Chatbot en RAM ---")
        MODELO = load_model(os.path.join(LOGICA_PATH, 'chatbot_model.h5'))
        WORDS = pickle.load(open(os.path.join(LOGICA_PATH, 'words.pkl'), 'rb'))
        CLASSES = pickle.load(open(os.path.join(LOGICA_PATH, 'classes.pkl'), 'rb'))
        with open(os.path.join(LOGICA_PATH, 'intents.json'), 'r', encoding='utf-8') as f:
            INTENTS = json.load(f)

def chat_page(request):
    return render(request, 'chat.html')

def chatbot_api(request):
    if request.method == 'POST':
        # Aseguramos que la IA esté cargada
        cargar_ia()
        
        user_message = request.POST.get('message', '')
        
        # 1. Limpieza
        sentence_words = nltk.word_tokenize(user_message)
        sentence_words = [stemmer.stem(w.lower()) for w in sentence_words]
        
        # 2. Bolsa de Palabras
        bag = [0] * len(WORDS)
        for s in sentence_words:
            for i, w in enumerate(WORDS):
                if w == s:
                    bag[i] = 1
        
        # 3. Predicción
        prediction = MODELO.predict(np.array([bag]), verbose=0)
        results = [[i, r] for i, r in enumerate(prediction[0]) if r > 0.25]
        results.sort(key=lambda x: x[1], reverse=True)
        
        # 4. Respuesta
        if results:
            tag = CLASSES[results[0][0]]
            for i in INTENTS['intents']:
                if i['tag'] == tag:
                    response = random.choice(i['responses'])
                    break
        else:
            response = "Lo siento, no entiendo tu pregunta. ¿Podrías ser más específico?"
            
        return JsonResponse({'reply': response})
    
    return JsonResponse({'error': 'Método no permitido'}, status=400)
