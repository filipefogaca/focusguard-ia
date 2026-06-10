# FocusGuard AI – Monitoramento Preventivo de Fadiga via Visão Computacional

## 👁️ Sobre o Projeto
O **FocusGuard AI** é um ecossistema de software focado em privacidade (**Edge Computing**) que utiliza Inteligência Artificial para monitorar, quantificar e mitigar a fadiga humana em tempo real. Diferente de sistemas reativos comuns, o FocusGuard atua de forma **preventiva**, utilizando a métrica internacional **PERCLOS** (Percentage of Eye Closure) para identificar sinais de exaustão antes mesmo da ocorrência de micro-sonos ou falhas de atenção.

O sistema foi projetado para ser flexível, atendendo a três cenários críticos:
1. **Educação (EAD):** Assistente de produtividade para aulas online.
2. **Trabalho (Home Office):** Prevenção de Burnout e cansaço visual.
3. **Segurança (Trânsito):** Mecanismo de alerta contra acidentes por sono ao volante.

---

## 🚀 Diferenciais Técnicos
- **Métrica PERCLOS:** Análise temporal da abertura ocular para detecção de fadiga acumulada.
- **Prevenção Antecipada:** Alertas emitidos em níveis (Atenção vs. Crítico).
- **Execução em Background:** Notificações push nativas que funcionam mesmo se o navegador estiver em segundo plano.
- **Privacidade Total:** Processamento 100% local; nenhuma imagem é enviada para a nuvem.

---

## 🛠️ Tecnologias Utilizadas
- **Python**: Linguagem base do ecossistema.
- **TensorFlow / Keras**: Criação e execução da Rede Neural Convolucional (CNN).
- **OpenCV**: Captura de vídeo e processamento de imagens em tempo real.
- **Streamlit**: Interface web interativa com telemetria de dados.
- **PyTTSx3**: Síntese de voz para alertas auditivos.
- **Plyer**: Integração com notificações nativas do sistema operacional.

---

## 📂 Estrutura do Projeto
```
focusguard_ai/
│
├── app.py                 # Aplicação principal (Interface e Lógica PERCLOS)
├── train_model.py         # Script de treinamento da CNN
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação principal
├── models/
│   └── eye_model.h5       # Modelo de Deep Learning treinado
├── dataset/
│   └── data/              # Base de imagens (awake/sleepy)
└── static/
    └── training_results.png # Gráficos de desempenho do modelo
```

---

## ⚙️ Como Instalar e Rodar

1. **Clonar o repositório e instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Treinar o modelo (opcional se já possuir o .h5):**
   ```bash
   python train_model.py
   ```

3. **Executar a aplicação:**
   ```bash
   streamlit run app.py
   ```

---

## 🧠 Funcionamento e Lógica
1. **Captura:** A webcam monitora o rosto do usuário via OpenCV.
2. **Segmentação:** O sistema isola a região dos olhos utilizando classificadores estruturais.
3. **Classificação (CNN):** Cada frame é analisado pela Rede Neural para determinar o estado ocular.
4. **Análise Temporal (PERCLOS):** O sistema calcula a porcentagem de fechamento nos últimos segundos.
5. **Ação Multimodal:**
   - **Fadiga Média:** Alerta suave por voz sugerindo uma pausa.
   - **Fadiga Alta:** Alerta sonoro crítico e notificação de desktop imediata.

---

## 👤 Autor
**Filipe Fogaça**  
**Rafael Rabelo**
**Gabriel Lana**
