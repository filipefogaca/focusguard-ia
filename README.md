# FocusGuard AI – Detector de Sonolência via Webcam

## Objetivo do Projeto
Desenvolver uma aplicação de Inteligência Artificial capaz de monitorar o estudante pela webcam durante aulas online e identificar sinais de sonolência em tempo real. O sistema utiliza uma Rede Neural Convolucional (CNN) para classificar se os olhos do usuário estão abertos ou fechados, emitindo um alerta de voz após 5 segundos de inatividade detectada.

## Tecnologias Utilizadas
- **Python**: Linguagem principal.
- **TensorFlow / Keras**: Para construção e treinamento da CNN.
- **OpenCV**: Para captura de vídeo e detecção de face/olhos.
- **Streamlit**: Interface web moderna.
- **pyttsx3**: Alertas sonoros automáticos.

## Estrutura do Projeto
```
focusguard_ai/
│
├── app.py                 # Interface Streamlit e detecção em tempo real
├── train_model.py         # Script de treinamento da CNN
├── requirements.txt       # Dependências
├── README.md              # Documentação
├── models/
│   └── eye_model.h5       # Modelo treinado salvo
├── dataset/
│   └── data/              # Imagens de treino, validação e teste (awake/sleepy)
└── static/
    └── training_results.png
```

## Como Instalar e Rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Treine o modelo com o dataset de imagens:
   ```bash
   python train_model.py
   ```
3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

## Funcionamento
1. A webcam captura o rosto do usuário.
2. O OpenCV detecta a região dos olhos.
3. A CNN classifica a imagem do olho como "Atento" (awake) ou "Sonolento" (sleepy).
4. Se o estado "Sonolento" persistir por 5 segundos, um alerta de voz é ativado.

## Autores
- Desenvolvido para o trabalho final da disciplina de Deep Learning.
