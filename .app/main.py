import streamlit as st
from model import setup_model
from food_detection import process_uploaded_images
from health_analysis import estimate_lifespan_gain, calculate_cancer_risk
from recommendation import recommend_diet

st.set_page_config(page_title="Análise Nutricional & Prevenção de Câncer", layout="wide")
st.title("🔍 Análise de Pratos e Riscos Nutricionais")

st.write("Faça o upload de até 10 imagens de pratos de comida para:")
st.markdown("""
- Identificar os ingredientes em cada prato
- Calcular a composição alimentar percentual
- Estimar o risco relativo de câncer
- Obter recomendações alimentares personalizadas
- Avaliar o impacto positivo na expectativa de vida
""")

uploaded_files = st.file_uploader("📤 Upload de imagens (máx. 10)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 10:
        st.warning("Limite máximo de 10 imagens.")
    else:
        with st.spinner("🔎 Processando imagens..."):
            model = setup_model()
            food_compositions = process_uploaded_images(uploaded_files, model)

        st.subheader("📊 Composição Alimentar dos Pratos")
        for comp in food_compositions:
            st.image(comp["image"], caption=comp["filename"], use_container_width=True)
            st.markdown("**Ingredientes identificados:**")
            for food, percent, score in comp["foods"]:
                st.write(f"- {food} | {percent:.1%} do prato | Confiança: {score:.2f}")
            risk = calculate_cancer_risk(comp["foods"])
            st.markdown(f"**Risco estimado de câncer para este prato:** `{risk:.2f}`")

        st.subheader("🧬 Avaliação Geral da Dieta")
        gain_years, avg_risk = estimate_lifespan_gain(food_compositions)
        st.write(f"**Risco médio de câncer na dieta:** `{avg_risk:.2f}`")
        st.write(f"**Estimativa de anos de vida adicionais com melhorias alimentares:** `{gain_years} anos`")

        st.subheader("🥗 Recomendações Alimentares Personalizadas")
        suggestions = recommend_diet(food_compositions)
        if suggestions:
            for category, rec in suggestions.items():
                st.markdown(f"- ⚠️ Categoria frequente: **{category}** ({rec['current_count']} ocorrências)")
                st.markdown(f"  → Sugestões de substituição: {', '.join(rec['suggested_replacements'])}")
        else:
            st.success("Nenhuma recomendação crítica. A dieta parece saudável! 🎉")
