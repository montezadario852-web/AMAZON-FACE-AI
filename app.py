

import streamlit as st
from PIL import Image, ImageOps
import os

st.set_page_config(
    page_title="AMAZON FACE AI",
    page_icon="🌿",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #102D22;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #0B2119;
}
h1, h2, h3, p, label {
    color: white !important;
}
.stButton button {
    background-color: #C7A65B;
    color: #102D22;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# MENÚ
st.sidebar.title("🌿 AMAZON FACE AI")
st.sidebar.caption("Inteligencia artificial amazónica")

pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Análisis facial",
        "Base de referencias",
        "Resultados",
        "Modelo matemático",
        "Acerca del proyecto"
    ]
)

# UBICACIÓN DE LA IMAGEN
RUTA_REFERENCIA = "rostros_referencia.png"

if pagina == "Inicio":
    st.title("AMAZON FACE AI")
    st.subheader("Geometría facial e inteligencia artificial")

    st.write(
        "Plataforma experimental para estudiar "
        "características geométricas faciales y "
        "compararlas con imágenes de referencia autorizadas."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📁 Subir fotografía")
        archivo = st.file_uploader(
            "Selecciona una fotografía",
            type=["jpg", "jpeg", "png"]
        )

        if archivo:
            imagen = Image.open(archivo).convert("RGB")
            st.image(imagen, caption="Fotografía seleccionada")

    with col2:
        st.subheader("📷 Activar cámara")
        foto = st.camera_input("Tomar fotografía")

        if foto:
            imagen = Image.open(foto).convert("RGB")
            st.image(imagen, caption="Fotografía capturada")

elif pagina == "Análisis facial":
    st.title("Análisis facial")
    st.info("Módulo experimental de análisis geométrico.")

elif pagina == "Base de referencias":
    st.title("Base de fotografías de referencia")

    if os.path.exists(RUTA_REFERENCIA):
        imagen = Image.open(RUTA_REFERENCIA).convert("RGB")
        st.image(
            imagen,
            caption="Imagen de referencia cargada",
            use_container_width=True
        )
        st.success("La imagen de referencia se encontró correctamente.")
    else:
        st.error("No se encontró rostros_referencia.png.")

elif pagina == "Resultados":
    st.title("Resultados")
    st.write("Aquí se presentarán los resultados cuando se implemente y valide el modelo.")

elif pagina == "Modelo matemático":
    st.title("Modelo matemático")
    st.write("Metodología de comparación geométrica facial.")

elif pagina == "Acerca del proyecto":
    st.title("Acerca de AMAZON FACE AI")
    st.write(
        "Proyecto experimental de visión computacional "
        "y análisis geométrico facial."
    )
