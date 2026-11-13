
import streamlit as st
import numpy as np
import pandas as pd
import mediapipe as mp
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
import math

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent
PORTADA = BASE / "portada_amazonia.jpg"
GALERIA = BASE / "rostros_referencia.png"

VERDE = "#123D2B"
VERDE2 = "#205A3B"
DORADO = "#F2C968"
CREMA = "#FFF9E9"
BLANCO = "#FFFFFF"
TEXTO = "#173D2B"

# =========================================================
# CSS: DISEÑO Y VISIBILIDAD
# =========================================================

st.markdown("""
<style>
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #FFF9E9 !important;
}

.stApp p,
.stApp li,
.stApp label,
.stApp span,
.stApp small,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: #173D2B;
}

.stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stApp h5 {
    color: #123D2B !important;
    font-weight: 900 !important;
}

[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #123D2B !important;
}

[data-testid="stSidebar"] {
    border-right: 3px solid #F2C968 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F2C968 !important;
    font-weight: 950 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: #205A3B !important;
    color: #FFFFFF !important;
    border: 1px solid #63866E !important;
    border-radius: 9px !important;
    padding: 10px 12px !important;
    margin: 5px 0 !important;
    font-weight: 850 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background-color: #F2C968 !important;
    border: 2px solid #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) * {
    color: #123D2B !important;
    font-weight: 950 !important;
}

.stButton > button {
    background-color: #E2BD65 !important;
    color: #123D2B !important;
    border: 2px solid #98752D !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    font-weight: 900 !important;
}

.stButton > button *,
.stButton > button p {
    color: #123D2B !important;
}

.stButton > button:hover {
    background-color: #F5D989 !important;
    border: 2px solid #123D2B !important;
}

[data-testid="stFileUploader"],
[data-testid="stCameraInput"] {
    background-color: #FFFFFF !important;
    border: 2px solid #B58B30 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploader"] *,
[data-testid="stCameraInput"] * {
    color: #123D2B !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #E2BD65 !important;
    border: 1px solid #98752D !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #123D2B !important;
    border: 2px solid #B58B30 !important;
}

.stSelectbox [data-baseweb="select"] {
    background-color: #FFFFFF !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #123D2B !important;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 2px solid #D9B45B !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #123D2B !important;
}

[data-testid="stAlert"] {
    background-color: #E8F0E6 !important;
    border: 2px solid #47734F !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #173D2B !important;
}

.hero {
    background: linear-gradient(120deg, #123D2B, #286044);
    border: 3px solid #F2C968;
    border-radius: 20px;
    padding: 30px 15px;
    text-align: center;
    margin-bottom: 20px;
}

.hero h1 {
    color: #F2C968 !important;
    font-size: 2.7rem !important;
    font-weight: 950 !important;
}

.hero p {
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
    font-weight: 850 !important;
}

.panel {
    background-color: #FFFFFF !important;
    border: 2px solid #D9B45B;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
}

.panel h3, .panel p, .panel li {
    color: #173D2B !important;
}

.resultado {
    background-color: #E5F0E5 !important;
    border: 3px solid #205A3B;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.resultado-numero {
    color: #123D2B !important;
    font-size: 3rem;
    font-weight: 950;
}

.resultado-texto {
    color: #123D2B !important;
    font-size: 1.35rem;
    font-weight: 950;
}

.nota {
    background-color: #FFF0C5 !important;
    border-left: 7px solid #B58B30;
    border-radius: 10px;
    padding: 17px;
    color: #49380F !important;
    font-weight: 800;
}

.nota p {
    color: #49380F !important;
}

hr {
    border-color: #D9B45B !important;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCIONES GENERALES
# =========================================================

def cargar_imagen(archivo):
    if archivo is None:
        return None

    try:
        imagen = Image.open(archivo)
        imagen = ImageOps.exif_transpose(imagen)
        return imagen.convert("RGB")
    except Exception:
        return None


def distancia(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


# =========================================================
# ANÁLISIS GEOMÉTRICO FACIAL
# =========================================================

def analizar_rostro(imagen_pil):

    imagen = imagen_pil.convert("RGB")
    ancho, alto = imagen.size

    imagen_array = np.asarray(imagen)

    try:
        with mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        ) as detector:

            resultado = detector.process(imagen_array)

    except Exception as error:
        return None, None, str(error)

    if not resultado.multi_face_landmarks:
        return None, None, None

    puntos = resultado.multi_face_landmarks[0].landmark

    def punto(indice):
        return (
            puntos[indice].x * ancho,
            puntos[indice].y * alto
        )

    # Puntos de referencia seleccionados
    mejilla_izquierda = punto(234)
    mejilla_derecha = punto(454)

    frente = punto(10)
    menton = punto(152)

    ojo_izquierdo = punto(33)
    ojo_derecho = punto(263)

    boca_izquierda = punto(61)
    boca_derecha = punto(291)

    nariz_izquierda = punto(129)
    nariz_derecha = punto(358)

    centro_boca = punto(13)

    # Dimensiones principales
    ancho_facial = distancia(
        mejilla_izquierda,
        mejilla_derecha
    )

    alto_facial = distancia(
        frente,
        menton
    )

    if ancho_facial < 1 or alto_facial < 1:
        return None, None, None

    # Mediciones normalizadas
    medidas = {
        "Proporción alto/ancho facial":
            alto_facial / ancho_facial,

        "Distancia entre ojos":
            distancia(
                ojo_izquierdo,
                ojo_derecho
            ) / ancho_facial,

        "Ancho de la boca":
            distancia(
                boca_izquierda,
                boca_derecha
            ) / ancho_facial,

        "Ancho de la nariz":
            distancia(
                nariz_izquierda,
                nariz_derecha
            ) / ancho_facial,

        "Posición vertical de la boca":
            abs(centro_boca[1] - frente[1]) / alto_facial
    }

    # Dibujar referencias geométricas
    dibujo = imagen.copy()
    lienzo = ImageDraw.Draw(dibujo)

    puntos_dibujo = [
        mejilla_izquierda,
        mejilla_derecha,
        frente,
        menton,
        ojo_izquierdo,
        ojo_derecho,
        boca_izquierda,
        boca_derecha,
        nariz_izquierda,
        nariz_derecha
    ]

    lineas = [
        (mejilla_izquierda, mejilla_derecha),
        (frente, menton),
        (ojo_izquierdo, ojo_derecho),
        (boca_izquierda, boca_derecha),
        (nariz_izquierda, nariz_derecha)
    ]

    for p1, p2 in lineas:
        lienzo.line(
            [p1, p2],
            fill=(220, 160, 30),
            width=max(2, int(ancho / 250))
        )

    radio = max(3, int(ancho / 100))

    for x, y in puntos_dibujo:
        lienzo.ellipse(
            [
                (x-radio, y-radio),
                (x+radio, y+radio)
            ],
            fill=(20, 160, 70),
            outline=(255, 255, 255)
        )

    return medidas, dibujo, None


# =========================================================
# COMPARACIÓN DE MEDICIONES GEOMÉTRICAS
# =========================================================

def comparar_medidas(medidas1, medidas2):

    diferencias = {}
    coincidencias = {}

    for nombre in medidas1:

        valor1 = medidas1[nombre]
        valor2 = medidas2[nombre]

        mayor = max(abs(valor1), abs(valor2), 1e-9)

        diferencia = abs(valor1 - valor2) / mayor * 100

        diferencia = min(100, diferencia)

        coincidencia = 100 - diferencia

        diferencias[nombre] = diferencia
        coincidencias[nombre] = coincidencia

    # Promedio de las coincidencias de las mediciones
    porcentaje = float(
        np.mean(list(coincidencias.values()))
    )

    diferencia_media = float(
        np.mean(list(diferencias.values()))
    )

    return porcentaje, diferencia_media, diferencias, coincidencias


# =========================================================
# INTERPRETACIÓN DEL RESULTADO
# =========================================================

def interpretar_resultado(porcentaje):

    if porcentaje >= 85:
        return (
            "COINCIDENCIA GEOMÉTRICA ALTA",
            "Las proporciones geométricas medidas presentan "
            "diferencias pequeñas."
        )

    elif porcentaje >= 70:
        return (
            "COINCIDENCIA GEOMÉTRICA MODERADA",
            "Las mediciones presentan algunas diferencias."
        )

    elif porcentaje >= 50:
        return (
            "COINCIDENCIA GEOMÉTRICA INTERMEDIA",
            "Se observan diferencias apreciables entre "
            "las medidas analizadas."
        )

    else:
        return (
            "COINCIDENCIA GEOMÉTRICA BAJA",
            "Las mediciones presentan diferencias considerables."
        )


# =========================================================
# CABECERA PRINCIPAL
# =========================================================

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL Y ANÁLISIS FACIAL</p>
    <p>INNOVACIÓN TECNOLÓGICA DESDE LA AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)


if PORTADA.exists():
    imagen_portada = Image.open(PORTADA)
    st.image(imagen_portada, use_container_width=True)
else:
    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#123D2B,#39734D);
        border:3px solid #F2C968;
        border-radius:18px;
        padding:55px 20px;
        text-align:center;">
        <div style="font-size:65px;">🌿</div>
        <h2 style="color:#F2C968 !important;">
            BIENVENIDOS A LA AMAZONÍA
        </h2>
        <p style="color:white !important;">
            Portada amazónica de CRISTOFHER AMAZON AI
        </p>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="nota">
    Plataforma experimental para el análisis geométrico
    de las medidas faciales mediante métodos matemáticos.
</div>
""", unsafe_allow_html=True)

st.divider()


# =========================================================
# ÍNDICE LATERAL
# =========================================================

st.sidebar.markdown("# 🌿 CRISTOFHER AMAZON AI")
st.sidebar.markdown("## ÍNDICE DE NAVEGACIÓN")
st.sidebar.markdown("---")

seccion = st.sidebar.radio(
    "SELECCIONA UNA SECCIÓN",
    [
        "Inicio",
        "Comparación matemática",
        "Galería amazónica",
        "Información del proyecto"
    ],
    key="menu_principal"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ANÁLISIS GEOMÉTRICO")
st.sidebar.markdown(
    "Tecnología desarrollada con Python y Streamlit."
)


# =========================================================
# SECCIÓN INICIO
# =========================================================

if seccion == "Inicio":

    st.title("BIENVENIDO A CRISTOFHER AMAZON AI")

    st.write("""
    Esta plataforma permite analizar las proporciones
    geométricas observables de dos rostros mediante
    puntos de referencia y procedimientos matemáticos.
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="panel">
            <h3>📷 FOTOGRAFÍAS</h3>
            <p>Carga imágenes desde tu dispositivo
            o utiliza la cámara.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
            <h3>📐 MATEMÁTICAS</h3>
            <p>Calcula distancias y proporciones
            geométricas faciales.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="panel">
            <h3>📊 RESULTADOS</h3>
            <p>Visualiza porcentajes, gráficos
            e interpretaciones.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Selecciona «Comparación matemática» "
        "en el menú lateral para comenzar."
    )


# =========================================================
# SECCIÓN COMPARACIÓN GEOMÉTRICA
# =========================================================

elif seccion == "Comparación matemática":

    st.title("COMPARACIÓN MATEMÁTICA FACIAL")

    st.write("""
    Carga dos fotografías frontales para analizar
    sus mediciones geométricas.
    """)

    st.markdown("""
    <div class="nota">
        El porcentaje representa coincidencia entre las
        mediciones geométricas observadas. No identifica
        personas ni determina si dos fotografías pertenecen
        a una misma persona.
    </div>
    """, unsafe_allow_html=True)

    izquierda, derecha = st.columns(2)

    img1 = None
    img2 = None

    with izquierda:

        st.subheader("📸 PRIMER ROSTRO")

        archivo1 = st.file_uploader(
            "Cargar primera fotografía",
            type=["jpg", "jpeg", "png"],
            key="imagen1"
        )

        camara1 = st.camera_input(
            "Tomar primera fotografía",
            key="camara1"
        )

        if camara1 is not None:
            img1 = cargar_imagen(camara1)
        elif archivo1 is not None:
            img1 = cargar_imagen(archivo1)

        if img1 is not None:
            st.image(
                img1,
                caption="PRIMERA FOTOGRAFÍA",
                use_container_width=True
            )
        else:
            st.info("Selecciona o toma la primera fotografía.")

    with derecha:

        st.subheader("📸 SEGUNDO ROSTRO")

        archivo2 = st.file_uploader(
            "Cargar segunda fotografía",
            type=["jpg", "jpeg", "png"],
            key="imagen2"
        )

        camara2 = st.camera_input(
            "Tomar segunda fotografía",
            key="camara2"
        )

        if camara2 is not None:
            img2 = cargar_imagen(camara2)
        elif archivo2 is not None:
            img2 = cargar_imagen(archivo2)

        if img2 is not None:
            st.image(
                img2,
                caption="SEGUNDA FOTOGRAFÍA",
                use_container_width=True
            )
        else:
            st.info("Selecciona o toma la segunda fotografía.")

    st.divider()

    if img1 is not None and img2 is not None:

        if st.button(
            "🔍 ANALIZAR MEDIDAS FACIALES",
            use_container_width=True
        ):

            with st.spinner("Detectando puntos y calculando medidas..."):

                medidas1, dibujo1, error1 = analizar_rostro(img1)
                medidas2, dibujo2, error2 = analizar_rostro(img2)

            if error1 or error2:
                st.error(
                    "Ocurrió un problema al procesar las fotografías. "
                    "Intenta nuevamente con imágenes JPG o PNG."
                )

            elif medidas1 is None or medidas2 is None:

                st.error(
                    "No se pudo detectar un rostro en una de las "
                    "fotografías. Utiliza imágenes frontales, claras "
                    "y con el rostro visible."
                )

            else:

                porcentaje, diferencia_media, diferencias, coincidencias = (
                    comparar_medidas(medidas1, medidas2)
                )

                categoria, explicacion = interpretar_resultado(
                    porcentaje
                )

                st.success("ANÁLISIS GEOMÉTRICO COMPLETADO")

                st.header("RESULTADO GENERAL")

                r1, r2 = st.columns(2)

                with r1:
                    st.markdown(f"""
                    <div class="resultado">
                        <div class="resultado-numero">
                            {porcentaje:.1f}%
                        </div>
                        <div class="resultado-texto">
                            COINCIDENCIA GEOMÉTRICA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with r2:
                    st.markdown(f"""
                    <div class="resultado">
                        <div class="resultado-numero">
                            {diferencia_media:.1f}%
                        </div>
                        <div class="resultado-texto">
                            DIFERENCIA GEOMÉTRICA
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.progress(
                    int(round(porcentaje))
                )

                st.subheader(categoria)
                st.write(explicacion)

                st.caption(
                    "Este porcentaje resume las diferencias entre "
                    "las proporciones geométricas seleccionadas. "
                    "No representa un porcentaje de parecido personal "
                    "ni una probabilidad de identidad."
                )

                # ---------------------------------------------
                # PUNTOS FACIALES
                # ---------------------------------------------

                st.divider()
                st.header("PUNTOS DE REFERENCIA FACIAL")

                g1, g2 = st.columns(2)

                with g1:
                    st.image(
                        dibujo1,
                        caption="Mediciones del primer rostro",
                        use_container_width=True
                    )

                with g2:
                    st.image(
                        dibujo2,
                        caption="Mediciones del segundo rostro",
                        use_container_width=True
                    )

                # ---------------------------------------------
                # TABLA DE MEDICIONES
                # ---------------------------------------------

                st.divider()
                st.header("TABLA DE MEDICIONES GEOMÉTRICAS")

                filas = []

                for nombre in medidas1:

                    filas.append({
                        "Característica": nombre,
                        "Rostro 1": round(medidas1[nombre], 4),
                        "Rostro 2": round(medidas2[nombre], 4),
                        "Diferencia (%)": round(
                            diferencias[nombre], 2
                        ),
                        "Coincidencia (%)": round(
                            coincidencias[nombre], 2
                        )
                    })

                tabla = pd.DataFrame(filas)

                st.dataframe(
                    tabla,
                    use_container_width=True,
                    hide_index=True
                )

                # ---------------------------------------------
                # GRÁFICO DE COINCIDENCIAS
                # ---------------------------------------------

                st.divider()
                st.header("GRÁFICO DE COINCIDENCIA POR MEDICIÓN")

                datos_grafico = pd.DataFrame({
                    "Característica": list(coincidencias.keys()),
                    "Coincidencia (%)": list(coincidencias.values())
                })

                st.bar_chart(
                    datos_grafico,
                    x="Característica",
                    y="Coincidencia (%)",
                    y_min=0,
                    y_max=100,
                    use_container_width=True
                )

                # ---------------------------------------------
                # GRÁFICO DE DIFERENCIAS
                # ---------------------------------------------

                st.header("GRÁFICO DE DIFERENCIAS")

                datos_diferencia = pd.DataFrame({
                    "Característica": list(diferencias.keys()),
                    "Diferencia (%)": list(diferencias.values())
                })

                st.bar_chart(
                    datos_diferencia,
                    x="Característica",
                    y="Diferencia (%)",
                    y_min=0,
                    y_max=100,
                    use_container_width=True
                )

                # ---------------------------------------------
                # EXPLICACIÓN MATEMÁTICA
                # ---------------------------------------------

                st.divider()
                st.header("MÉTODO MATEMÁTICO UTILIZADO")

                st.write(
                    "Primero se calcula la diferencia relativa "
                    "de cada medición:"
                )

                st.latex(
                    r"D_i = "
                    r"\frac{|M_{1i}-M_{2i}|}"
                    r"{\max(|M_{1i}|,|M_{2i}|)}"
                    r"\times 100"
                )

                st.write(
                    "Después se calcula la coincidencia descriptiva "
                    "de cada medición:"
                )

                st.latex(
                    r"C_i = 100-D_i"
                )

                st.write(
                    "Finalmente, se obtiene el promedio de las "
                    "coincidencias geométricas:"
                )

                st.latex(
                    r"C_{\mathrm{promedio}}="
                    r"\frac{\sum_{i=1}^{n} C_i}{n}"
                )

                st.markdown(f"""
                <div class="panel">
                    <h3>INTERPRETACIÓN AUTOMÁTICA</h3>
                    <p>{categoria}</p>
                    <p>{explicacion}</p>
                    <p>Coincidencia geométrica descriptiva:
                    <b>{porcentaje:.2f}%</b>.</p>
                    <p>Diferencia geométrica media:
                    <b>{diferencia_media:.2f}%</b>.</p>
                </div>
                """, unsafe_allow_html=True)

                st.info(
                    "Las mediciones pueden variar por la posición "
                    "del rostro, la expresión facial, la iluminación, "
                    "la perspectiva y la calidad de la fotografía."
                )

    else:

        st.info(
            "Selecciona las dos fotografías para habilitar "
            "el análisis geométrico."
        )


# =========================================================
# SECCIÓN GALERÍA
# =========================================================

elif seccion == "Galería amazónica":

    st.title("GALERÍA DOCUMENTAL AMAZÓNICA")

    st.write("""
    Espacio destinado a mostrar fotografías documentales
    relacionadas con la diversidad cultural de la Amazonía.
    """)

    if GALERIA.exists():

        galeria = Image.open(GALERIA)

        st.image(
            galeria,
            caption="Fotografías documentales de referencia",
            use_container_width=True
        )

    else:

        st.info(
            "Agrega el archivo rostros_referencia.png "
            "a tu repositorio para mostrar la galería."
        )

    st.markdown("""
    <div class="nota">
        Esta galería tiene una finalidad documental y cultural.
        No se utiliza para identificar personas ni clasificarlas.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SECCIÓN INFORMACIÓN
# =========================================================

elif seccion == "Información del proyecto":

    st.title("INFORMACIÓN DEL PROYECTO")

    st.markdown("""
    ### CRISTOFHER AMAZON AI

    **Descripción**

    Plataforma experimental desarrollada con Python,
    Streamlit y MediaPipe para analizar mediciones
    geométricas observables del rostro.

    **Tecnologías utilizadas**

    - Python.
    - Streamlit.
    - NumPy.
    - Pandas.
    - Pillow.
    - MediaPipe.

    **Métodos matemáticos**

    - Detección de puntos de referencia faciales.
    - Distancias euclidianas.
    - Normalización de proporciones.
    - Cálculo de diferencias relativas.
    - Promedio de coincidencias geométricas.
    - Representación gráfica de resultados.

    **Objetivo**

    Presentar mediciones geométricas mediante ecuaciones,
    porcentajes, gráficos e interpretaciones comprensibles.
    """)


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("---")

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL · ANÁLISIS GEOMÉTRICO · AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)














