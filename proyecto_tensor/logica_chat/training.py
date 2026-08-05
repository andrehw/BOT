import numpy as np
import pickle
import os

# Usamos tf_keras por compatibilidad con Python 3.13
from tf_keras.models import Sequential
from tf_keras.layers import Dense, Dropout
from tf_keras.optimizers import SGD

# 1. Cargar los datos procesados por train.py
base_path = 'chatbot_logic'
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
train_x, train_y = pickle.load(open('training_data.pkl', 'rb'))

# Convertir a arrays de numpy para la red neuronal
train_x = np.array(train_x)
train_y = np.array(train_y)

# 2. Definir la Red Neuronal Densa
model = Sequential()
# Capa de entrada: neuronas según el tamaño del vocabulario
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5)) # Evita que el bot memorice frases exactas

# Capa intermedia
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))

# Capa de salida: neuronas según la cantidad de etiquetas (tags)
model.add(Dense(len(train_y[0]), activation='softmax'))

# 3. Configuración del entrenamiento
# Usamos SGD (Descenso de Gradiente Estocástico)
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# 4. Entrenamiento
print(f"Iniciando entrenamiento con {len(train_x)} ejemplos...")
# 200 epochs es ideal para que el modelo aprenda sin sobreajustarse
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# 5. Guardar el modelo final
model.save('chatbot_model.h5')
print("\n¡Éxito! El cerebro del bot ha sido guardado como 'chatbot_model.h5'")
