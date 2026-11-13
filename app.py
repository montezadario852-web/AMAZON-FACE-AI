
import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageChops
from pathlib import Path
import io

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
PORTADA = BASE_DIR / "portada_amazonia.jpg"
GALERIA = BASE_DIR / "rostros_referencia.png"

VERDE = "#123D2B"
VERDE_CLARO = "#1D563B"
DORADO = "#D9B45B"
CREMA = "#FFF9E9"
TEXTO = "#173D2B"
GRIS = "#53665A"

# ==========================================================
# ESTILOS: LETRAS GRANDES Y ALTO CONTRASTE
# ==========================================================

st.markdown("""
<style>
    .stApp {
        background-color: #FFF9E9;
        color: #173D2B;
    }

    html, body, [class*="css"] {
        color: #173D2B !important;
        font-family: Arial, Helvetica, sans-serif;
    }

    p, label, span, li, small, div {
        color: inherit;
    }

    h1, h2, h3, h4 {
        color: #123D2B !important;
        font-weight: 900 !important;
    }

    h1 { font-size: 2.7rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }

    [data-testid="stSidebar"] {
        background-color: #123D2B;
    }

    [data-testid="stSidebar"] * {
        color: #FFF9E9 !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F0CE78 !important;
    }

    .hero {
        background: linear-gradient(120deg, #123D2B, #276345);
        border: 3px solid #D9B45B;
        border-radius: 22px;
        padding: 35px 30px;
        margin-bottom: 25px;
        color: #FFF9E9;
    }

    .hero h1 {
        color: #F3D17B !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 8px;
    }

    .hero p {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
    }

    .subtitulo {
        color: #FFF9E9;
        text-align: center;
        font-size: 1.05rem;
        font-weight: bold;
    }

    .panel {
        background: #FFFFFF;
        border: 2px solid #D9B45B;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
    }

    .panel h3 {
        color: #123D2B !important;
    }

    .resultado {
        background: #E7F0E6;
        border: 2px solid #1D563B;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
    }

    .resultado-numero {
        color: #123D2B;
        font-size: 2.8rem;
        font-weight: 900;
    }

    .resultado-texto {
        color: #173D2B;
        font-size: 1.2rem;
        font-weight: 800;
    }

    .nota {
        background: #FFF1C9;
        border-left: 6px solid #B58B30;
        border-radius: 8px;
        padding: 14px;
        color: #49380F;
        font-size: 1rem;
        font-weight: 650;
    }

    .stButton > button {
        background-color: #D9B45B !important;
        color: #123D2B !important;
        border: 2px solid #98752D !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        min-height: 48px;
    }

    .stButton > button:hover {
        background-color: #F0CE78 !important;
        color: #123D2B !important;
        border: 2px solid #123D2B !important;
    }

    .stTextInput input,
    .stSelectbox div,
    .stFileUploader,
    [data-testid="stCameraInput"] {
        color: #173D2B !important;
        background-color: #FFFFFF !important;
    }

    [data-testid="stCameraInput"] {
        border: 2px solid #D9B45B !important;
        border-radius: 14px !important;
        padding: 14px !important;
    }

    [data-testid="stCameraInput"] label,
    [data-testid="stCameraInput"] label *,
    [data-testid="stCameraInput"] p,
    [data-testid="stCameraInput"] span,
    [data-testid="stCameraInput"] small {
        color: #173D2B !important;
        font-weight: 800 !important;
    }

    [data-testid="stCameraInput"] button {
        background: #D9B45B !important;
        color: #123D2B !important;
        border: 2px solid #98752D !important;
        font-weight: 900 !important;
    }

    [data-testid="stCameraInput"] button * {
        color: #123D2B !important;
        fill: #123D2B !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border: 2px dashed #98752D !important;
    }

    [data-testid="stFileUploader"] * {
        color: #173D2B !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #123D2B !important;
        font-weight: 900 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #173D2B !important;
        font-weight: 800 !important;
    }

    hr {
        border-color: #D9B45B !important;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FUNCIONES DE IMAGEN
# ==========================================================

def abrir_imagen(archivo):
    if archivo is None:
        return None

    try:
        imagen = Image.open(archivo)
        imagen = ImageOps.exif_transpose(imagen)
        return imagen.convert("RGB")
    except Exception:
        return None


def obtener_dhash(imagen):
    """
    Calcula una huella perceptual sencilla de la imagen.
    """
    gris = imagen.convert("L").resize((9, 8))
    pixeles = np.asarray(gris, dtype=np.int16)

    diferencias = pixeles[:, 1:] > pixeles[:, :-1]
    return diferencias.flatten()


def similitud_estructura(img1, img2):
    hash1 = obtener_dhash(img1)
    hash2 = obtener_dhash(img2)

    diferencias = np.count_nonzero(hash1 != hash2)
    total = len(hash1)

    return (1 - diferencias / total) * 100


def histograma_color(imagen):
    """
    Calcula histogramas normalizados para los tres canales RGB.
    """
    imagen = imagen.resize((256, 256))
    arreglo = np.asarray(imagen)

    histogramas = []

    for canal in range(3):
        hist, _ = np.histogram(
            arreglo[:, :, canal],
            bins=32,
            range=(0, 256)
        )

        hist = hist.astype(float)
        hist = hist / (hist.sum() + 1e-10)
        histogramas.append(hist)

    return np.array(histogramas)


def similitud_color(img1, img2):
    h1 = histograma_color(img1)
    h2 = histograma_color(img2)

    intersecciones = np.minimum(h1, h2).sum(axis=1)
    return float(np.mean(intersecciones) * 100)


def comparar_imagenes(img1, img2):
    estructura = similitud_estructura(img1, img2)
    color = similitud_color(img1, img2)

    resultado = (estructura * 0.60) + (color * 0.40)

    return {
        "estructura": estructura,
        "color": color,
        "resultado": resultado
    }


def interpretar_resultado(porcentaje):
    if porcentaje >= 85:
        return (
            "Muy similares",
            "Las imágenes presentan una alta coincidencia "
            "en las características visuales generales analizadas."
        )
    elif porcentaje >= 70:
        return (
            "Similares",
            "Las imágenes comparten varias características "
            "visuales, aunque también presentan diferencias."
        )
    elif porcentaje >= 50:
        return (
            "Similitud moderada",
            "Se observan algunas coincidencias visuales, "
            "pero también diferencias importantes."
        )
    else:
        return (
            "Poco similares",
            "Las características visuales generales "
            "presentan diferencias considerables."
        )


# ==========================================================
# PORTADA PRINCIPAL
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL Y ANÁLISIS VISUAL</p>
    <div class="subtitulo">
        Tecnología · Amazonía · Innovación · Investigación
    </div>
</div>
""", unsafe_allow_html=True)

if PORTADA.exists():
    portada = Image.open(PORTADA)
    st.image(portada, use_container_width=True)
else:
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #173D2B, #39734D);
        border: 3px solid #D9B45B;
        border-radius: 18px;
        padding: 45px 20px;
        text-align: center;
        margin-bottom: 20px;
    ">
        <div style="font-size: 4rem;">🌿</div>
        <div style="
            color: #F3D17B;
            font-size: 2rem;
            font-weight: 900;
        ">
            BIENVENIDOS A LA AMAZONÍA
        </div>
        <div style="
            color: white;
            font-size: 1.15rem;
            font-weight: bold;
        ">
            Espacio para la fotografía principal de la portada
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="nota">
    Plataforma de análisis visual orientada a la comparación
    matemática de características generales de imágenes y a la
    presentación documental de fotografías amazónicas.
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# MENÚ LATERAL
# ==========================================================

st.sidebar.markdown("# 🌿 MENÚ PRINCIPAL")
st.sidebar.markdown("### CRISTOFHER AMAZON AI")

opcion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Inicio",
        "Comparación de imágenes",
        "Galería amazónica",
        "Información del proyecto"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Proyecto de análisis visual**"
)
st.sidebar.markdown(
    "Interfaz diseñada para una presentación clara y comprensible."
)

# ==========================================================
# INICIO
# ==========================================================

if opcion == "Inicio":

    st.title("Bienvenido a CRISTOFHER AMAZON AI")

    st.write("""
    Esta plataforma permite analizar dos imágenes mediante
    procedimientos matemáticos sencillos y presentar los resultados
    de una forma visual, ordenada y entendible.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="panel">
            <h3>📷 Fotografías</h3>
            <p>Permite cargar imágenes desde el dispositivo
            o utilizar la cámara.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <h3>📊 Matemáticas</h3>
            <p>Calcula indicadores de similitud estructural
            y de distribución de colores.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="panel">
            <h3>🌳 Amazonía</h3>
            <p>Presenta una galería documental de fotografías
            de referencia.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Selecciona «Comparación de imágenes» en el menú "
        "lateral para comenzar."
    )

# ==========================================================
# COMPARACIÓN DE DOS IMÁGENES
# ==========================================================

elif opcion == "Comparación de imágenes":

    st.title("Comparación matemática de imágenes")

    st.write("""
    Carga dos fotografías para calcular y visualizar sus
    semejanzas y diferencias en características generales.
    """)

    st.markdown("""
    <div class="nota">
        IMPORTANTE: el resultado es un indicador experimental de
        similitud visual entre imágenes. No identifica personas,
        no verifica identidades y no determina parentescos.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    imagen1 = None
    imagen2 = None

    with col1:
        st.markdown("""
        <div class="panel">
            <h3>📸 IMAGEN 1</h3>
            <p>Primera fotografía de comparación</p>
        </div>
        """, unsafe_allow_html=True)

        archivo1 = st.file_uploader(
            "Seleccionar primera imagen",
            type=["jpg", "jpeg", "png"],
            key="archivo1"
        )

        camara1 = st.camera_input(
            "O tomar fotografía con la cámara",
            key="camara1"
        )

        if camara1 is not None:
            imagen1 = abrir_imagen(camara1)
        elif archivo1 is not None:
            imagen1 = abrir_imagen(archivo1)

        if imagen1 is not None:
            st.image(
                imagen1,
                caption="Primera imagen",
                use_container_width=True
            )
        else:
            st.info("Todavía no has seleccionado la primera imagen.")

    with col2:
        st.markdown("""
        <div class="panel">
            <h3>📸 IMAGEN 2</h3>
            <p>Segunda fotografía de comparación</p>
        </div>
        """, unsafe_allow_html=True)

        archivo2 = st.file_uploader(
            "Seleccionar segunda imagen",
            type=["jpg", "jpeg", "png"],
            key="archivo2"
        )

        camara2 = st.camera_input(
            "O tomar fotografía con la cámara",
            key="camara2"
        )

        if camara2 is not None:
            imagen2 = abrir_imagen(camara2)
        elif archivo2 is not None:
            imagen2 = abrir_imagen(archivo2)

        if imagen2 is not None:
            st.image(
                imagen2,
                caption="Segunda imagen",
                use_container_width=True
            )
        else:
            st.info("Todavía no has seleccionado la segunda imagen.")

    st.divider()

    if imagen1 is not None and imagen2 is not None:

        if st.button("🔍 REALIZAR COMPARACIÓN MATEMÁTICA", use_container_width=True):

            with st.spinner("Analizando las características visuales..."):

                datos = comparar_imagenes(imagen1, imagen2)

                porcentaje = datos["resultado"]
                categoria, interpretacion = interpretar_resultado(porcentaje)

            st.success("Análisis visual completado")

            st.markdown("## RESULTADO GENERAL")

            st.markdown(f"""
            <div class="resultado">
                <div class="resultado-numero">
                    {porcentaje:.2f} %
                </div>
                <div class="resultado-texto">
                    {categoria}
                </div>
                <p style="color:#173D2B; font-weight:700;">
                    Indicador de similitud visual general
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(
                min(max(int(round(porcentaje)), 0), 100)
            )

            st.markdown("## RESULTADOS MATEMÁTICOS")

            r1, r2 = st.columns(2)

            with r1:
                st.metric(
                    "Similitud estructural",
                    f"{datos['estructura']:.2f} %"
                )

            with r2:
                st.metric(
                    "Similitud de color",
                    f"{datos['color']:.2f} %"
                )

            st.markdown("### Gráfico de resultados")

            grafico = {
                "Indicador": [
                    "Estructura visual",
                    "Distribución de color",
                    "Resultado combinado"
                ],
                "Porcentaje": [
                    datos["estructura"],
                    datos["color"],
                    porcentaje
                ]
            }

            st.bar_chart(
                grafico,
                x="Indicador",
                y="Porcentaje",
                horizontal=True
            )

            st.markdown("## INTERPRETACIÓN")

            st.markdown(f"""
            <div class="panel">
                <h3>{categoria}</h3>
                <p style="font-size:1.1rem;">
                    {interpretacion}
                </p>
                <p>
                    El indicador estructural fue de
                    <b>{datos['estructura']:.2f} %</b>,
                    mientras que el indicador de color fue de
                    <b>{datos['color']:.2f} %</b>.
                </p>
                <p>
                    El resultado combinado utiliza una ponderación
                    de 60 % para estructura y 40 % para color.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("## CONSIDERACIONES DEL ANÁLISIS")

            st.write("""
            - La similitud estructural se estima mediante una huella
              perceptual de baja resolución.
            - La similitud de color se estima comparando histogramas
              de los canales RGB.
            - Los porcentajes son indicadores experimentales de
              similitud visual, no probabilidades estadísticas.
            - Cambios de iluminación, encuadre, tamaño y orientación
              pueden modificar los resultados.
            """)

            st.warning(
                "Este análisis no constituye una prueba de identidad "
                "ni una evaluación biométrica de los rostros."
            )

    else:
        st.info(
            "Selecciona las dos imágenes para habilitar "
            "la comparación matemática."
        )

# ==========================================================
# GALERÍA DOCUMENTAL
# ==========================================================

elif opcion == "Galería amazónica":

    st.title("Galería documental amazónica")

    st.write("""
    Este espacio está destinado a presentar fotografías de
    referencia relacionadas con la diversidad cultural y
    documental de la Amazonía.
    """)

    if GALERIA.exists():
        galeria = Image.open(GALERIA)
        st.image(
            galeria,
            caption="Material fotográfico documental de referencia",
            use_container_width=True
        )
    else:
        st.info(
            "Para mostrar tu galería, agrega el archivo "
            "rostros_referencia.png al repositorio."
        )

    st.markdown("""
    <div class="nota">
        Las fotografías de esta sección tienen una finalidad
        documental y cultural. No se utilizan para clasificar
        personas por origen étnico ni para determinar identidades.
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# INFORMACIÓN DEL PROYECTO
# ==========================================================

elif opcion == "Información del proyecto":

    st.title("Información del proyecto")

    st.markdown("""
    ### CRISTOFHER AMAZON AI

    **Descripción**

    Plataforma experimental desarrollada con Python y Streamlit
    para realizar análisis matemáticos de similitud visual entre
    dos imágenes.

    **Tecnologías utilizadas**

    - Python.
    - Streamlit.
    - NumPy.
    - Pillow.

    **Métodos de análisis**

    - Huella perceptual para estimar similitud estructural.
    - Histogramas RGB para comparar distribución de colores.
    - Ponderación matemática de indicadores.

    **Objetivo**

    Presentar resultados visuales y matemáticos de manera clara,
    comprensible y accesible para los usuarios.
    """)

    st.markdown("---")

    st.markdown("""
    <div class="hero">
        <h1>CRISTOFHER AMAZON AI</h1>
        <p>Innovación tecnológica desde la Amazonía</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.markdown("---")

st.markdown("""
<div style="
    background-color:#123D2B;
    padding:20px;
    border-radius:14px;
    text-align:center;
">
    <div style="
        color:#F3D17B;
        font-size:1.35rem;
        font-weight:900;
    ">
        CRISTOFHER AMAZON AI
    </div>
    <div style="
        color:#FFFFFF;
        font-size:1rem;
        font-weight:700;
    ">
        Inteligencia artificial · Análisis visual · Amazonía
    </div>
</div>
""", unsafe_allow_html=True)












