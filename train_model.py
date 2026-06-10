import os
import tensorflow as tf
import matplotlib.pyplot as plt

# Configurações básicas
# O dataset agora está em dataset/data/train e dataset/data/val
TRAIN_DIR = 'dataset/data/train'
VAL_DIR = 'dataset/data/val'
MODEL_SAVE_PATH = 'models/eye_model.h5'
IMG_SIZE = (64, 64)
BATCH_SIZE = 32
EPOCHS = 15

def build_model():
    """
    Constrói a arquitetura da CNN.
    Classes: awake (0), sleepy (1)
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(2, activation='softmax') # Saída: [awake, sleepy]
    ])
    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train():
    # Pré-processamento e Data Augmentation
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True
    )

    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    # Carregamento do dataset
    print(f"Carregando dados de treino de {TRAIN_DIR}...")
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    print(f"Carregando dados de validação de {VAL_DIR}...")
    validation_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # Verificar classes
    print(f"Mapeamento de classes: {train_generator.class_indices}")

    # Construção do modelo
    model = build_model()
    model.summary()

    # Treinamento
    print("Iniciando treinamento da CNN...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator
    )

    # Salvar o modelo
    if not os.path.exists('models'):
        os.makedirs('models')
    model.save(MODEL_SAVE_PATH)
    print(f"Modelo salvo em {MODEL_SAVE_PATH}")

    # Plotar resultados
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Treino')
    plt.plot(history.history['val_accuracy'], label='Validação')
    plt.title('Acurácia do Modelo (Imagens)')
    plt.xlabel('Época')
    plt.ylabel('Acurácia')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Treino')
    plt.plot(history.history['val_loss'], label='Validação')
    plt.title('Loss do Modelo (Imagens)')
    plt.xlabel('Época')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.savefig('static/training_results.png')
    print("Gráficos de desempenho salvos em static/training_results.png")

if __name__ == "__main__":
    if os.path.exists(TRAIN_DIR):
        train()
    else:
        print(f"Erro: O diretório '{TRAIN_DIR}' não foi encontrado.")
