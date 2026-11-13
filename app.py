
import streamlit as st
from PIL import Image

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
    border: none;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌿 AMAZON FACE AI")
st.sidebar.caption("Inteligencia artificial amazónica")
pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    ["Inicio", "Análisis facial", "Base de referencias",
     "Resultados", "Modelo matemático", "Acerca del proyecto"]
)

if pagina == "Inicio":
    st.title("AMAZON FACE AI")
    st.subheader("Geometría facial e inteligencia artificial")

    st.markdown("""
    ### Tecnología al servicio de nuestra Amazonía

    Plataforma de investigación desarrollada en Python
    para analizar características geométricas faciales
    y compararlas con fotografías de referencia
    documentadas de los pueblos Awajún y Wampis.
    """)

    st.divider()
    st.subheader("Comienza tu análisis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📁 Subir fotografía")
        st.write("Selecciona una imagen desde tu dispositivo.")
        archivo = st.file_uploader(
            "Seleccionar imagen",
            type=["jpg", "jpeg", "png"]
        )
        if archivo:
            imagen = Image.open(archivo).convert("RGB")
            st.image(imagen, caption="Fotografía seleccionada",
                     use_container_width=True)

    with col2:
        st.markdown("### 📷 Activar cámara")
        st.write("Captura una fotografía utilizando tu cámara.")
        foto = st.camera_input("Tomar fotografía")

        if foto:
            imagen_camara = Image.open(foto).convert("RGB")
            st.image(imagen_camara, use_container_width=True)

    st.info("La comparación facial se incorporará en la siguiente etapa.")

elif pagina == "Análisis facial":
    st.title("Análisis facial")
    st.write("Aquí se realizará la detección de puntos y geometría facial.")

elif pagina == "Base de referencias":
    st.title("Base de referencias")
    st.write("Aquí se administrarán las fotografías autorizadas de referencia.")

elif pagina == "Resultados":
    st.title("Resultados")
    st.write("Aquí se mostrarán los porcentajes y categorías de similitud.")

    st.markdown("""
    - 90% – 100%: Muy parecido
    - 75% – 89%: Parecido
    - 50% – 74%: Similitud moderada
    - 0% – 49%: Baja similitud
    """)

elif pagina == "Modelo matemático":
    st.title("Modelo matemático")
    st.write("Metodología de extracción y comparación geométrica.")

elif pagina == "Acerca del proyecto":
    st.title("Acerca de AMAZON FACE AI")
    st.write("""
    Proyecto de investigación sobre visión computacional,
    análisis geométrico facial y comparación de muestras
    de referencia de la Amazonía peruana.
    """)
