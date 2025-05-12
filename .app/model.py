from ultralytics import YOLO
import streamlit as st

@st.cache_resource
def setup_model():
    try:
        model = YOLO("yolov8n-seg.pt")  # modelo leve com segmentação
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo YOLOv8: {e}")
        return None
