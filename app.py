
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------
st.set_page_config(
    page_title="AMAZON FACE AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# ESTILO VISUAL: AMAZONÍA PERUANA
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(circle at 85% 8%, #245b42 0%, transparent 28%),
      linear-gradient(135deg, #071b14, #102d20 55%, #071811);
    color: #f5f2e8;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#06170f,#123b29);
    border-right: 1px solid #bd9b4b;
}
h1,h2,h3 { color: #f0d28a !important; }
p, label, span { color: #f1eee4; }
.hero {
    padding: 28px;
    border: 1px solid #b99549;
    border-radius: 22px;
    background: linear-gradient(120deg,#123b29,#0a2118);
    box-shadow: 0 12px 35px #0006;
}
.hero-title {
    font-size: 42px;
    font-weight: 900;
    color: #f1d58e;
    letter-spacing: 2px;
}
.hero-subtitle {
    font-size: 18px;
    color: #f6f0df;
}
.panel {
    padding: 20px;
    border: 1px solid #8c7946;
    border-radius: 17px;
    background: #10291f;
    margin-bottom: 14px;
}
.small-note {
    color: #c8d7c9;
    font-size: 13px;
}
div.stButton > button {
    background: linear-gradient(90deg,#c49b45,#e5c879);
    color: #142318;
    border: 0;
    border-radius: 12px;
    font-weight: bold;
}
[data-testid="stMetric"] {
    background: #123526;
    border: 1px solid #927a42;
    border-radius: 14px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FUNCIONES DE ANÁLISIS
# --------------------------------------------------
mp_face_mesh = mp.solutions.face_mesh

def distancia(p1, p2):
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))

def analizar_fotografia(imagen_pil):
    imagen = np.array(imagen_pil.convert("RGB"))
    alto, ancho = imagen.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as detector:
        resultado = detector.process(imagen)

    if not resultado.multi_face_landmarks:
        return None, None, None

    puntos = resultado.multi_face_landmarks[0].landmark

    def punto(indice):
        return (puntos[indice].x * ancho,
                puntos[indice].y * alto)

    # Medidas geométricas normalizadas
    ancho_rostro = distancia(punto(234), punto(454))
    alto_rostro = distancia(punto(10), punto(152))

    if ancho_rostro <= 0:
        return None, None, None

    medidas = {
        "Distancia entre ojos": distancia(punto(33), punto(263)) / ancho_rostro,
        "Ancho de nariz": distancia(punto(98), punto(327)) / ancho_rostro,
        "Ancho de boca": distancia(punto(61), punto(291)) / ancho_rostro,
        "Relación altura/ancho": alto_rostro / ancho_rostro
    }

    # Dibujar malla y puntos detectados
    imagen_malla = imagen.copy()

    conexiones = [
        (33, 263), (234, 454), (10, 152),
        (98, 327), (61, 291), (33, 234),
        (263, 454), (10, 33), (10, 263)
    ]

    for a, b in conexiones:
        pa = tuple(np.round(punto(a)).astype(int))
        pb = tuple(np.round(punto(b)).astype(int))
        cv2.line(imagen_malla, pa, pb, (218, 181, 91), 2)

    for indice in [10, 33, 61, 98, 152, 234, 263, 291, 327, 454]:
        px_, py_ = np.round(punto(indice)).astype(int)
        cv2.circle(imagen_malla, (px_, py_), 5, (60, 230, 150), -1)

    # Indicador técnico orientativo de calidad de captura
    gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    brillo = float(np.mean(gris))
    nitidez = float(cv2.Laplacian(gris, cv2.CV_64F).var())
    proporcion_rostro = ancho_rostro / ancho

    puntaje_brillo = np.clip(100 - abs(brillo - 130) * 0.7, 0, 100)
    puntaje_nitidez = np.clip(nitidez / 150 * 100, 0, 100)
    puntaje_tamano = np.clip(proporcion_rostro / 0.45 * 100, 0, 100)

    calidad = round(
        0.35 * puntaje_brillo
        + 0.35 * puntaje_nitidez
        + 0.30 * puntaje_tamano
    )

    return imagen_malla, medidas, calidad

# --------------------------------------------------
# MENÚ LATERAL
# --------------------------------------------------
st.sidebar.markdown("## 🌿 AMAZON FACE AI")
st.sidebar.caption("Tecnología y análisis geométrico facial")
pagina = st.sidebar.radio(
    "NAVEGACIÓN",
    ["Inicio", "Análisis facial", "Acerca del proyecto"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("🌳 **Amazonía peruana**")
st.sidebar.caption("Naturaleza · Ciencia · Tecnología")

# --------------------------------------------------
# PORTADA
# --------------------------------------------------
if pagina == "Inicio":
    st.markdown("""
    <div class="hero">
      <div class="hero-title">🌿 AMAZON FACE AI</div>
      <div class="hero-subtitle">
        Geometría facial e inteligencia artificial
      </div>
      <p>Una herramienta experimental para visualizar
      características geométricas del rostro mediante visión
      computacional.</p>
      <div style="font-size:35px;">🌳 🦜 🍃 🌊 🌴</div>
      <p style="color:#e5c879;font-weight:bold;">
        TECNOLOGÍA AL SERVICIO DE NUESTRA AMAZONÍA
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📷 Análisis facial")
        st.write("Carga una fotografía o utiliza la cámara para detectar puntos y medidas geométricas.")
        st.button(
            "Ir al análisis facial",
            on_click=lambda: st.session_state.update(
                {"ir_analisis": True}
            )
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📊 Resultados visuales")
        st.write("Visualiza las medidas detectadas, los gráficos y la calidad de la fotografía.")
        st.markdown("**Análisis individual de cada imagen.**")
        st.markdown('</div>', unsafe_allow_html=True)

    st.info(
        "Esta aplicación analiza geometría facial. "
        "No determina identidad, origen étnico ni pertenencia "
        "a pueblos indígenas."
    )

# --------------------------------------------------
# ANÁLISIS FACIAL
# --------------------------------------------------
elif pagina == "Análisis facial":
    st.title("📷 Análisis geométrico facial")
    st.write(
        "Selecciona una fotografía o toma una imagen con tu cámara."
    )

    col1, col2 = st.columns(2)

    with col1:
        archivo = st.file_uploader(
            "Subir fotografía",
            type=["jpg", "jpeg", "png"]
        )

    with col2:
        camara = st.camera_input("Activar cámara")

    imagen_seleccionada = camara if camara is not None else archivo

    if imagen_seleccionada is not None:
        imagen = Image.open(imagen_seleccionada).convert("RGB")

        st.markdown("### Fotografía seleccionada")
        st.image(imagen, use_container_width=True)

        if st.button("🔍 ANALIZAR FOTOGRAFÍA", use_container_width=True):
            with st.spinner("Detectando puntos faciales..."):
                imagen_malla, medidas, calidad = analizar_fotografia(imagen)

            if imagen_malla is None:
                st.error(
                    "No se detectó un rostro con suficiente claridad. "
                    "Prueba con una fotografía frontal, iluminada y nítida."
                )
            else:
                st.success("Se detectó un rostro y se calcularon sus medidas.")

                st.markdown("## 🧭 Visualización geométrica")
                st.image(
                    imagen_malla,
                    caption="Puntos y líneas geométricas detectadas",
                    use_container_width=True
                )

                st.markdown("## 📐 Medidas calculadas")

                datos = pd.DataFrame({
                    "Característica": list(medidas.keys()),
                    "Valor normalizado": list(medidas.values())
                })

                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Calidad técnica de captura", f"{calidad}%")
                with c2:
                    st.metric("Características calculadas", len(medidas))

                grafico = px.bar(
                    datos,
                    x="Característica",
                    y="Valor normalizado",
                    color="Valor normalizado",
                    color_continuous_scale=["#39765a", "#d9b65e"],
                    title="Distribución de medidas geométricas"
                )
                grafico.update_layout(
                    paper_bgcolor="#10291f",
                    plot_bgcolor="#10291f",
                    font_color="#f5f2e8",
                    coloraxis_showscale=False
                )
                st.plotly_chart(grafico, use_container_width=True)

                st.dataframe(
                    datos,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("## 📝 Interpretación técnica")

                if calidad >= 75:
                    st.success(
                        "La fotografía presenta condiciones técnicas "
                        "favorables para la detección y medición."
                    )
                elif calidad >= 50:
                    st.warning(
                        "La calidad de captura es intermedia. "
                        "Se recomienda mejorar la iluminación, el enfoque "
                        "o el tamaño del rostro en la imagen."
                    )
                else:
                    st.error(
                        "La calidad de captura es baja. "
                        "Se recomienda tomar otra fotografía."
                    )

                st.caption(
                    "El porcentaje representa una estimación técnica "
                    "de calidad de captura basada en iluminación, nitidez "
                    "y tamaño del rostro. No representa similitud, "
                    "probabilidad de identidad ni origen étnico."
                )

    else:
        st.info("Primero sube una fotografía o activa la cámara.")

# --------------------------------------------------
# INFORMACIÓN DEL PROYECTO
# --------------------------------------------------
elif pagina == "Acerca del proyecto":
    st.title("🌳 Acerca de AMAZON FACE AI")

    st.markdown("""
    <div class="panel">
      <h3>Identidad amazónica y tecnología</h3>
      <p>
      AMAZON FACE AI es una aplicación experimental que utiliza
      técnicas de visión computacional para detectar puntos faciales
      y calcular proporciones geométricas en fotografías.
      </p>
      <p>
      Su presentación está inspirada en la biodiversidad,
      los paisajes y la riqueza natural de la Amazonía peruana.
      </p>
      <div style="font-size:34px;">🌿 🌳 🦜 🐸 🌺 🌊</div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Tecnologías utilizadas")
    st.write("- Python")
    st.write("- Streamlit")
    st.write("- OpenCV")
    st.write("- MediaPipe")
    st.write("- Plotly")
    st.write("- NumPy")

    st.warning(
        "Las medidas faciales son descriptores geométricos "
        "experimentales. No permiten determinar la etnia, "
        "identidad ni comunidad de una persona."
    )

st.markdown("---")
st.caption("AMAZON FACE AI | Proyecto experimental | Amazonía peruana")




