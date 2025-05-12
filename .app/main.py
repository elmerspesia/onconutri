import streamlit as st
from model import setup_model
from food_detection import process_uploaded_images
from health_analysis import estimate_lifespan_gain, calculate_cancer_risk
from recommendation import recommend_diet

st.set_page_config(page_title="Análise Nutricional de Risco Oncológico", layout="wide")
st.title("🧬 Análise Nutricional de Risco Oncológico")

st.markdown("""
Faça o upload de até 30 imagens de pratos de comida para:

- Identificar os ingredientes em cada prato
- Calcular a composição percentual dos alimentos no prato
- Estimar o risco relativo de câncer baseado na dieta
- Obter recomendações alimentares personalizadas para redução de risco
- Avaliar o impacto potencial sobre a expectativa de vida
""")

uploaded_files = st.file_uploader(
    "📤 Envie as imagens dos pratos (até 30 imagens)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) > 30:
        st.warning("Limite máximo de 30 imagens excedido.")
    else:
        with st.spinner("🔍 Processando as imagens..."):
            model = setup_model()
            food_compositions = process_uploaded_images(uploaded_files, model)

        # Miniaturas
        st.subheader("📷 Miniaturas dos Pratos Enviados")
        cols = st.columns(min(len(food_compositions), 5))
        for idx, comp in enumerate(food_compositions):
            with cols[idx % len(cols)]:
                st.image(comp["image"], caption=comp["filename"], use_column_width=True)

        # Detalhes de cada prato
        st.subheader("📊 Ingredientes Identificados nos Pratos")
        for comp in food_compositions:
            st.image(comp["image"], caption=comp["filename"], use_container_width=True)
            st.markdown("**Ingredientes identificados:**")
            for food, percent, score in comp["foods"]:
                st.write(f"- {food} | {percent:.1%} do prato | Confiança: {score:.2f}")
            risk = calculate_cancer_risk(comp["foods"])
            st.markdown(f"**Risco estimado de câncer para este prato:** `{risk:.2f}`")

        # Avaliação geral
        st.subheader("🧬 Avaliação Geral da Dieta")
        gain_years, avg_risk = estimate_lifespan_gain(food_compositions)
        st.write(f"**Risco médio estimado de câncer baseado na dieta:** `{avg_risk:.2f}`")
        st.write(f"**Potencial de aumento na expectativa de vida com dieta otimizada:** `{gain_years} anos`")

        # Recomendações
        st.subheader("🥗 Recomendações Alimentares Personalizadas")
        suggestions = recommend_diet(food_compositions)
        if suggestions:
            for category, rec in suggestions.items():
                st.markdown(f"- ⚠️ Categoria frequente: **{category}** ({rec['current_count']} ocorrências)")
                st.markdown(f"  → Sugestões de substituição: {', '.join(rec['suggested_replacements'])}")
        else:
            st.success("Nenhuma recomendação crítica. A dieta parece saudável! 🎉")
