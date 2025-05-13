import streamlit as st
from model import setup_model
from food_detection import process_uploaded_images
from health_analysis import estimate_lifespan_gain, calculate_cancer_risk
from recommendation import recommend_diet, gerar_matriz_dieta

# Primeira instrução obrigatória
st.set_page_config(page_title="Análise Nutricional de Risco Oncológico", layout="wide")

# Função de login
def login_screen():
    st.title("🔐 Análise Nutricional de Risco Oncológico")
    st.subheader("Por favor, entre com suas credenciais")

    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            if usuario == "spesia123" and senha == "spesia123":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

# Controle de sessão
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    login_screen()
    st.stop()

# Menu lateral
menu = st.sidebar.selectbox("📚 Menu", [
    "Tela Principal",
    "Ranking de Risco Nutricional",
    "Consulta Oncológica",
    "Bot"
])

# Página: Ranking
if menu == "Ranking de Risco Nutricional":
    from risco_alimentos import show_ranking
    show_ranking()
    st.stop()

# Página: Consulta Médica Oncológica
if menu == "Consulta Oncológica":
    from consulta_oncologica import show_form
    show_form()
    st.stop()

# Página: Bot interativo
if menu == "Bot":
    from bot_nina import bot_nina_ui
    bot_nina_ui()
    st.stop()

# Página: Tela Principal
st.title("🧬 Análise Nutricional de Risco Oncológico")

st.markdown("""
Faça o upload de até 30 imagens de pratos de comida para:

- Identificar os ingredientes com precisão
- Calcular a composição alimentar percentual
- Estimar o risco relativo de câncer
- Gerar recomendações personalizadas
- Propor uma dieta semanal alternativa
""")

uploaded_files = st.file_uploader("📤 Envie até 30 imagens de pratos (jpg/png)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 30:
        st.warning("Limite de 30 imagens excedido.")
    else:
        with st.spinner("🔎 Processando..."):
            model = setup_model()
            food_compositions = process_uploaded_images(uploaded_files, model)

        st.subheader("📷 Miniaturas dos Pratos Enviados")
        cols = st.columns(min(len(food_compositions), 5))
        for idx, comp in enumerate(food_compositions):
            with cols[idx % len(cols)]:
                st.image(comp["image"], caption
