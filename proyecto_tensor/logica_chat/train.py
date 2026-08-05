import nltk
import json
import pickle
import numpy as np
from nltk.stem import SnowballStemmer

# 1. Configuración e Idioma
stemmer = SnowballStemmer('spanish')
nltk.download('punkt')
nltk.download('punkt_tab')

# Cargar el dataset
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '¡', '.', ',']

# 2. Preprocesamiento
for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# 3. Creación de la Bolsa de Palabras (Bag of Words)
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Convertir a listas antes de guardar para asegurar compatibilidad
train_x = [row[0] for row in training]
train_y = [row[1] for row in training]

# 4. GUARDAR LOS 3 ARCHIVOS (Aquí está la clave)
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))
# Este es el archivo que le faltaba a tu script de training:
pickle.dump((train_x, train_y), open('training_data.pkl', 'wb'))

print("¡Hecho! Se generaron: words.pkl, classes.pkl y training_data.pkl")
