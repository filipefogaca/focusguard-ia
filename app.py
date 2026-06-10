import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
import time
import os
import pyttsx3
import threading
from plyer import notification

# Configurações de página
st.set_page_config(page_title="FocusGuard AI", page_icon="👁️", layout="wide")

# Estilo CSS customizado
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .atento { background-color: #28a745; }
    .fadiga { background-color: #ffc107; color: black; }
    .sonolento { background-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar motor de voz
def speak(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    
    # Notificação Desktop
    try:
        notification.notify(
            title='FocusGuard AI - Alerta!',
            message=text,
            app_name='FocusGuard AI',
            timeout=10
        )
    except:
        pass

    threading.Thread(target=run_speech).start()

# Carregar o modelo
@st.cache_resource
def load_trained_model():
    model_path = 'models/eye_model.h5'
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    return None

# Carregar classificadores do OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

st.title("👁️ FocusGuard AI")
st.subheader("Detector Preventivo de Sonolência (Métrica PERCLOS)")

col1, col2 = st.columns([2, 1])

with col2:
    st.info("### Monitoramento de Fadiga")
    status_placeholder = st.empty()
    perclos_placeholder = st.empty()
    timer_placeholder = st.empty()
    alerts_placeholder = st.empty()
    message_placeholder = st.empty()

with col1:
    run = st.checkbox('Iniciar Câmera')
    FRAME_WINDOW = st.image([])

# Variáveis de estado
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'alerts_count' not in st.session_state:
    st.session_state.alerts_count = 0
if 'last_alert_time' not in st.session_state:
    st.session_state.last_alert_time = 0
if 'eye_history' not in st.session_state:
    st.session_state.eye_history = [] # Agora vai guardar tuplas: (timestamp, status)

model = load_trained_model()

if not model:
    st.error("Modelo não encontrado!")
    run = False

camera = cv2.VideoCapture(0)

while run:
    ret, frame = camera.read()
    if not ret:
        st.error("Falha ao acessar a webcam.")
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    current_frame_sleepy = False
    current_time = time.time()
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Trava anti-nariz (55% superior do rosto)
        limite_superior_rosto = int(h * 0.55)
        roi_gray_eyes = gray[y:y+limite_superior_rosto, x:x+w]
        roi_color_eyes = frame[y:y+limite_superior_rosto, x:x+w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray_eyes, scaleFactor=1.1, minNeighbors=12)
        
        if len(eyes) == 0:
            current_frame_sleepy = True
        else:
            ex, ey, ew, eh = eyes[0]
            eye_img = roi_color_eyes[ey:ey+eh, ex:ex+ew]
            eye_img = cv2.resize(eye_img, (64, 64))
            eye_img = eye_img / 255.0
            eye_img = np.expand_dims(eye_img, axis=0)
            
            prediction = model(eye_img, training=False).numpy()
            if np.argmax(prediction) == 1:
                current_frame_sleepy = True
                cv2.rectangle(roi_color_eyes, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            else:
                current_frame_sleepy = False
                cv2.rectangle(roi_color_eyes, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # --- NOVO CÁLCULO DE PERCLOS BASEADO EM TEMPO REAL ---
    # Adiciona o momento exato do frame atual e o estado (1=fechado, 0=aberto)
    st.session_state.eye_history.append((current_time, 1 if current_frame_sleepy else 0))
    
    # JANELA DE TEMPO: Mantém no histórico apenas os frames dos últimos 4.0 segundos
    # (Se achar que ainda está rápido, mude para 5.0 ou 6.0)
    janela_segundos = 4.0 
    st.session_state.eye_history = [f for f in st.session_state.eye_history if current_time - f[0] <= janela_segundos]
    
    # Extrai apenas os estados (0s e 1s) para calcular a porcentagem média
    historico_estados = [f[1] for f in st.session_state.eye_history]
    perclos_value = sum(historico_estados) / len(historico_estados) if historico_estados else 0

    # Lógica de tempo e alertas
    session_duration = int(current_time - st.session_state.start_time)
    
    if perclos_value > 0.75: # Subimos ligeiramente para 75% para evitar falsos positivos de piscadas longas
        status_html = '<div class="status-card sonolento">🔴 SONOLENTO</div>'
        msg = "ALERTA CRÍTICO! Acorde!"
        
        if current_time - st.session_state.last_alert_time > 5:
            speak(msg)
            st.session_state.alerts_count += 1
            st.session_state.last_alert_time = current_time
    
    elif perclos_value > 0.40: # Limiar de fadiga ajustado para 40%
        status_html = '<div class="status-card fadiga">🟡 FADIGA DETECTADA</div>'
        msg = "Atenção: Você está demonstrando sinais de cansaço. Que tal uma pausa?"
        
        if current_time - st.session_state.last_alert_time > 30:
            speak("Sinais de cansaço detectados. Faça uma pausa.")
            st.session_state.last_alert_time = current_time
    
    else:
        status_html = '<div class="status-card atento">🟢 ATENTO</div>'
        msg = "Continue assim! Seu nível de atenção está bom."

    # Atualizar Interface
    FRAME_WINDOW.image(frame)
    status_placeholder.markdown(status_html, unsafe_allow_html=True)
    perclos_placeholder.metric("Índice de Fadiga (PERCLOS)", f"{perclos_value*100:.1f}%")
    timer_placeholder.metric("Tempo de Sessão", f"{session_duration // 60:02d}:{session_duration % 60:02d}")
    alerts_placeholder.metric("Alertas Emitidos", st.session_state.alerts_count)
    message_placeholder.write(f"**Status:** {msg}")

else:
    camera.release()