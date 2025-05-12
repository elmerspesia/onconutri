import streamlit as st
from model import setup_model
from food_detection import process_uploaded_images
from health_analysis import estimate_lifespan_gain, calculate_cancer_risk
from recommendation import recommend_diet
from transformers import pipeline

# Setup IA generativa (open-source, pode usar mistral, mixtral, falcon etc.)
generator = pipeline("text-generation", model="tiiuae/falcon-7b-instruct", max_new_tokens=512)

def generate_diet_suggestion(food_texts: list[str]) -> str:
    food_summary = ", ".join(food_texts)
    prompt = f"""
Considere a seguinte lista de alimentos que compõem a dieta de um paciente: {food_summary}.
Com base na literatura médica e científica atual sobre nutrição e prevenção de câncer,
gere uma dieta semanal personalizada (em português) que substitua alimentos com alto risco
por alternativas saudáveis, incluindo opções para café da manhã, almoço e jantar.
A dieta deve minimizar riscos oncológicos e promover longevidade.
"""
    response = generator(prompt)[0]["generated_text"]
    return response

# Título e instruções
st.set_page_config(page_title="Análise Nutricional de Risco Oncológico", layout="wide")
st.title("🧬 Análise Nutricional de Risco Oncológico")

st.markdown("""
Faça o upload de até 30 imagens de pratos de comida para:

- Identificar os ingredientes em cada prato
- Calcular a composição percentual dos alimentos
- Estimar o risco relativo de câncer com base na dieta
- Obter recomendações alimentares para reduzir esse risco
- Gerar uma dieta semanal personalizada baseada nas imagens reais
""")

uploaded_files = st.file_uploader(
    "📤 Envie imagens dos pratos (máximo 30)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 30:
        st.warning("Limite máximo de 30 imagens excedido.")
    else:
        with st.spinner("🔎 Processando imagens..."):
            model = setup_model()
            food_compositions = process_uploaded_images(uploaded_files, model)

        st.subheader("📷 Miniaturas dos Pratos")
        cols = st.columns(min(len(food_compositions), 5))
        for idx, comp in enumerate(food_compositions):
            with cols[idx % len(cols)]:
                st.image(comp["image"], caption=comp["filename"], use_column_width=True)

        st.subheader("📊 Ingredientes Identificados")
        all_ingredientes = []
        for comp in food_compositions:
            st.image(comp["image"], caption=comp["filename"], use_container_width=True)
            st.markdown("**Ingredientes:**")
            for food, percent, score in comp["foods"]:
                st.write(f"- {food} | {percent:.1%} do prato | Confiança: {score:.2f}")
                all_ingredientes.append(food)
            risk = calculate_cancer_risk(comp["foods"])
            st.markdown(f"**Risco estimado de câncer para este prato:** `{risk:.2f}`")

        st.subheader("🧬 Avaliação Geral da Dieta")
        gain_years, avg_risk = estimate_lifespan_gain(food_compositions)
        st.write(f"**Risco médio de câncer baseado na dieta:** `{avg_risk:.2f}`")
        st.write(f"**Estimativa de anos de vida adicionais com melhorias:** `{gain_years} anos`")

        st.subheader("🥗 Recomendações Alimentares")
        suggestions = recommend_diet(food_compositions)
        if suggestions:
            for category, rec in suggestions.items():
                st.markdown(f"- ⚠️ Categoria frequente: **{category}** ({rec['current_count']} ocorrências)")
                st.markdown(f"  → Substituir por: {', '.join(rec['suggested_replacements'])}")
        else:
            st.success("Nenhuma substituição crítica necessária.")

        st.subheader("📅 Dieta Semanal Personalizada")
        if all_ingredientes:
            dieta_texto = generate_diet_suggestion(all_ingredientes)
            st.markdown(dieta_texto)
