
import streamlit as st
import mediapipe as mp
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from pathlib import Path

# ==================================================
# CHRISTOPHER AMAZON AI
# IDENTIFICACIÓN DE ROSTRO
# ==================================================

st.set_page_config(
    page_title="CHRISTOPHER AMAZON AI | Identificación de rostro",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ COLORES -----------------------

VERDE_OSCURO = "#0B1D14"
VERDE = "#153522"
VERDE_MEDIO = "#245239"
DORADO = "#D9B66F"
BLANCO = "#F5F5F0"

# ------------------ ESTILOS -----------------------

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at top right, #24452f 0%, transparent 35%),
        linear-gradient(135deg, #091810, #10291d, #142f20);
    color: #f5f5f0;
}

[data-testid="stSidebar"] {
    background: #091810;
    border-right: 1px solid #b99a58;
}

h1, h2, h3 {
    color: #e2c47e !important;
}

p, label, span {
    color: #f5f5f0;
}

.hero {
    background: linear-gradient(115deg, #10291d, #28533a);
    border: 1px solid #c7a65e;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 24px;
    box-shadow: 0 8px 30px rgba(0,0,0,.25);
}

.hero-brand {
    color: #e2c47e;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 3px;
}

.hero-title {
    color: #ffffff;
    font-size: clamp(28px, 4vw, 45px);
    font-weight: 900;
    line-height: 1.15;
    margin-top: 12px;
}

.hero-description {
    color: #e6eadf;
    font-size: 16px;
    margin-top: 12px;
}

.tarjeta {
    background: #193927;
    border: 1px solid #45684d;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 12px;
}

.metric-card {
    background: linear-gradient(145deg, #1b3c29, #10291d);
    border: 1px solid #c7a65e;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
}

.metric-value {
    color: #e2c47e;
    font-size: 30px;
    font-weight: 900;
}

.metric-label {
    color: #e8eadf;
    font-size: 13px;
}

div.stButton > button {
    background: linear-gradient(90deg, #d9b66f, #f0d99b);
    color: #10251b;
    border: none;
    border-radius: 10px;
    font-weight: 800;
    min-height: 45px;
}

div.stButton > button:hover {
    background: #ffffff;
    color: #10251b;
}

.stDownloadButton button {
    background: #d9b66f;
    color: #10251b;
    font-weight: bold;
    border-radius: 10px;
}

hr {
    border-color: #45684d;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# FUNCIONES DE IMÁGENES
# ==================================================

def abrir_imagen(archivo):
    imagen = Image.open(archivo).convert("RGB")
    return np.array(imagen)


def detectar_rostros_referencia(imagen):
    """
    Detecta rostros en la imagen de referencia
    y los recorta automáticamente.
    """

    recortes = []

    with mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.45
    ) as detector:

        resultado = detector.process(imagen)

        if resultado.detections:
            alto, ancho, _ = imagen.shape

            for deteccion in resultado.detections:

                caja = deteccion.location_data.relative_bounding_box

                x1 = max(0, int(caja.xmin * ancho))
                y1 = max(0, int(caja.ymin * alto))
                x2 = min(
                    ancho,
                    int((caja.xmin + caja.width) * ancho)
                )
                y2 = min(
                    alto,
                    int((caja.ymin + caja.height) * alto)
                )

                recorte = imagen[y1:y2, x1:x2]

                if recorte.size > 0:
                    recortes.append(recorte)

    return recortes


# ==================================================
# ANÁLISIS GEOMÉTRICO FACIAL
# ==================================================

def analizar_rostro(imagen):

    with mp.solutions.face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as detector:

        resultado = detector.process(imagen)

        if not resultado.multi_face_landmarks:
            return None, None

        rostro = resultado.multi_face_landmarks[0]
        alto, ancho, _ = imagen.shape

        def punto(indice):
            p = rostro.landmark[indice]
            return np.array([
                p.x * ancho,
                p.y * alto
            ])

        distancia_ojos = np.linalg.norm(
            punto(33) - punto(263)
        )

        ancho_rostro = np.linalg.norm(
            punto(234) - punto(454)
        )

        ancho_nariz = np.linalg.norm(
            punto(98) - punto(327)
        )

        ancho_boca = np.linalg.norm(
            punto(61) - punto(291)
        )

        alto_rostro = np.linalg.norm(
            punto(10) - punto(152)
        )

        if ancho_rostro <= 0:
            return None, None

        medidas = {
            "Distancia entre ojos": distancia_ojos / ancho_rostro,
            "Ancho relativo de nariz": ancho_nariz / ancho_rostro,
            "Ancho relativo de boca": ancho_boca / ancho_rostro,
            "Proporción alto/ancho": alto_rostro / ancho_rostro
        }

        # Dibujar malla facial
        imagen_malla = imagen.copy()

        mp.solutions.drawing_utils.draw_landmarks(
            image=imagen_malla,
            landmark_list=rostro,
            connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=
                mp.solutions.drawing_utils.DrawingSpec(
                    color=(70, 220, 140),
                    thickness=1,
                    circle_radius=1
                )
        )

        return medidas, imagen_malla


# ==================================================
# INTERPRETACIÓN AUTOMÁTICA
# ==================================================

def interpretar_resultado(medidas):

    if not medidas:
        return "No se encontraron medidas faciales."

    mayor = max(medidas, key=medidas.get)
    menor = min(medidas, key=medidas.get)

    texto = (
        "El procesamiento de la fotografía permitió detectar "
        "un rostro y calcular sus principales proporciones "
        "geométricas. "
        f"La medida relativa de mayor valor corresponde a: {mayor}. "
        f"La medida relativa de menor valor corresponde a: {menor}. "
        "Los valores describen las características geométricas "
        "observadas en esta imagen."
    )

    return texto


# ==================================================
# ENCABEZADO PRINCIPAL
# ==================================================

st.markdown("""
<div class="hero">
    <div class="hero-brand">CHRISTOPHER AMAZON AI</div>
    <div class="hero-title">IDENTIFICACIÓN DE ROSTRO</div>
    <div class="hero-description">
        Plataforma de procesamiento de imágenes y análisis
        geométrico facial mediante inteligencia artificial.
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# MENÚ LATERAL
# ==================================================

st.sidebar.markdown(
    "<h2>🌿 CHRISTOPHER AMAZON AI</h2>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Identificación de rostro",
        "Base de fotografías",
        "Acerca del proyecto"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Sistema académico de procesamiento facial")


# ==================================================
# CARGA DE IMAGEN DE REFERENCIA
# ==================================================

ruta_referencia = Path("rostros_referencia.png")

imagen_referencia = None

if ruta_referencia.exists():
    imagen_referencia = abrir_imagen(ruta_referencia)


# ==================================================
# PÁGINA DE INICIO
# ==================================================

if pagina == "Inicio":

    st.subheader("Bienvenido a nuestra plataforma")

    if imagen_referencia is not None:
        st.image(
            imagen_referencia,
            use_container_width=True,
            caption="Base fotográfica de referencia del proyecto"
        )
    else:
        st.warning(
            "No se encontró rostros_referencia.png. "
            "Verifica que esté en la carpeta principal del repositorio."
        )

    st.markdown("""
    <div class="tarjeta">
        <h3>¿Qué es CHRISTOPHER AMAZON AI?</h3>
        <p>
        Es una aplicación académica orientada al procesamiento
        digital de imágenes y al análisis geométrico de rostros.
        </p>
        <p>
        El proyecto cuenta con una base documental de fotografías
        de referencia relacionadas con los pueblos originarios
        Awajún y Wampis.
        </p>
        <p>
        La aplicación permite detectar rostros, calcular medidas
        geométricas y visualizar resultados de cada fotografía.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Selecciona «Identificación de rostro» en el menú lateral "
        "para cargar una fotografía o utilizar la cámara."
    )


# ==================================================
# IDENTIFICACIÓN DE ROSTRO
# ==================================================

elif pagina == "Identificación de rostro":

    st.subheader("Procesamiento de fotografía")

    st.write(
        "Selecciona una imagen desde tu dispositivo "
        "o utiliza la cámara para realizar el análisis."
    )

    columna1, columna2 = st.columns(2)

    with columna1:
        archivo = st.file_uploader(
            "📁 SUBIR FOTOGRAFÍA",
            type=["jpg", "jpeg", "png"]
        )

    with columna2:
        captura = st.camera_input("📷 ACTIVAR CÁMARA")

    imagen_usuario = None

    if archivo is not None:
        imagen_usuario = abrir_imagen(archivo)

    elif captura is not None:
        imagen_usuario = abrir_imagen(captura)

    if imagen_usuario is not None:

        st.markdown("### Vista previa de la fotografía")

        st.image(
            imagen_usuario,
            use_container_width=True
        )

        if st.button(
            "INICIAR IDENTIFICACIÓN DE ROSTRO",
            use_container_width=True
        ):

            with st.spinner("Procesando fotografía..."):

                medidas, imagen_malla = analizar_rostro(
                    imagen_usuario
                )

            if medidas is None:

                st.error(
                    "No se detectó un rostro. "
                    "Prueba con una fotografía frontal, "
                    "nítida y con buena iluminación."
                )

            else:

                st.success("Procesamiento facial completado.")

                st.markdown("---")
                st.subheader("Visualización del rostro detectado")

                st.image(
                    imagen_malla,
                    use_container_width=True,
                    caption="Malla de puntos faciales detectados"
                )

                st.markdown("---")
                st.subheader("Resultados de las mediciones")

                columnas = st.columns(4)

                for columna, (nombre, valor) in zip(
                    columnas, medidas.items()
                ):

                    columna.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-value">
                                {valor:.3f}
                            </div>
                            <div class="metric-label">
                                {nombre}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Tabla de datos
                datos = pd.DataFrame({
                    "Característica facial": list(medidas.keys()),
                    "Valor relativo": list(medidas.values())
                })

                st.markdown("---")
                st.subheader("Gráfico de proporciones faciales")

                grafico = px.bar(
                    datos,
                    x="Característica facial",
                    y="Valor relativo",
                    text_auto=".3f",
                    color="Valor relativo",
                    color_continuous_scale=[
                        "#245239",
                        "#D9B66F"
                    ]
                )

                grafico.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#10291D",
                    plot_bgcolor="#10291D",
                    font_color="white"
                )

                st.plotly_chart(
                    grafico,
                    use_container_width=True
                )

                st.subheader("Gráfico radial de características")

                radar = go.Figure()

                radar.add_trace(
                    go.Scatterpolar(
                        r=list(medidas.values()),
                        theta=list(medidas.keys()),
                        fill="toself",
                        name="Medidas faciales"
                    )
                )

                radar.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#10291D",
                    font_color="white",
                    polar=dict(
                        radialaxis=dict(
                            visible=True
                        )
                    )
                )

                st.plotly_chart(
                    radar,
                    use_container_width=True
                )

                st.markdown("---")
                st.subheader("Interpretación automática")

                st.markdown(
                    f"""
                    <div class="tarjeta">
                        <p>{interpretar_resultado(medidas)}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.subheader("Tabla detallada")

                st.dataframe(
                    datos,
                    use_container_width=True,
                    hide_index=True
                )

                archivo_csv = datos.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "DESCARGAR RESULTADOS",
                    data=archivo_csv,
                    file_name="resultados_identificacion.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    else:

        st.markdown("""
        <div class="tarjeta">
            <h3>Comienza tu análisis</h3>
            <p>
            Sube una fotografía o activa la cámara.
            El sistema detectará el rostro y calculará
            sus proporciones geométricas.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ==================================================
# BASE DE FOTOGRAFÍAS
# ==================================================

elif pagina == "Base de fotografías":

    st.subheader("Base fotográfica de referencia")

    if imagen_referencia is None:

        st.error(
            "No se encontró el archivo rostros_referencia.png."
        )

    else:

        st.image(
            imagen_referencia,
            use_container_width=True,
            caption="Imagen original de referencia"
        )

        st.markdown(
            "### Detección automática de rostros"
        )

        if st.button(
            "PROCESAR Y SEPARAR ROSTROS",
            use_container_width=True
        ):

            with st.spinner(
                "Detectando y recortando rostros..."
            ):

                rostros = detectar_rostros_referencia(
                    imagen_referencia
                )

            if not rostros:

                st.warning(
                    "No se detectaron rostros en la imagen. "
                    "Comprueba que los rostros sean visibles "
                    "y tengan suficiente resolución."
                )

            else:

                st.success(
                    f"Se detectaron {len(rostros)} rostros."
                )

                st.markdown("### Rostros detectados")

                columnas = st.columns(3)

                for i, rostro in enumerate(rostros):

                    with columnas[i % 3]:

                        st.image(
                            rostro,
                            caption=f"Referencia {i + 1}",
                            use_container_width=True
                        )

                st.info(
                    "Los recortes se muestran para revisar la "
                    "detección. Esta operación no determina "
                    "identidad ni pertenencia étnica."
                )


# ==================================================
# ACERCA DEL PROYECTO
# ==================================================

elif pagina == "Acerca del proyecto":

    st.subheader("Acerca de CHRISTOPHER AMAZON AI")

    st.markdown("""
    <div class="tarjeta">
        <h3>Descripción del proyecto</h3>
        <p>
        CHRISTOPHER AMAZON AI es una propuesta académica
        que emplea herramientas de visión artificial para
        procesar fotografías y analizar características
        geométricas del rostro.
        </p>

        <h3>Base documental</h3>
        <p>
        El proyecto utiliza fotografías de referencia
        recopiladas para documentar imágenes de personas
        de los pueblos originarios Awajún y Wampis.
        </p>

        <h3>Funciones principales</h3>
        <p>
        • Carga de fotografías.<br>
        • Captura mediante cámara.<br>
        • Detección de rostros.<br>
        • Recorte automático de rostros de referencia.<br>
        • Medición de proporciones faciales.<br>
        • Visualización mediante gráficos.<br>
        • Interpretación de resultados geométricos.
        </p>

        <h3>Consideración metodológica</h3>
        <p>
        Las mediciones describen características geométricas
        de las fotografías. No permiten establecer la identidad
        ni la pertenencia étnica de una persona.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("CHRISTOPHER AMAZON AI © 2026")






