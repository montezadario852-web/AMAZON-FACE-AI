
import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image
from pathlib import Path
import io

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
ARCHIVO_PORTADA = BASE_DIR / "portada_amazonia.jpg"
ARCHIVO_GALERIA = BASE_DIR / "rostros_referencia.png"

# ==========================================
# DISEÑO Y COLORES
# ==========================================

st.markdown("""
<style>

/* FONDO GENERAL */
.stApp {
    background-color: #f5f3e9;
    color: #173d2b;
}

/* TEXTOS GENERALES */
html, body, [class*="css"],
p, label, span, small {
    color: #173d2b;
}

/* TÍTULOS */
h1, h2, h3, h4 {
    color: #174b32 !important;
    font-weight: 800 !important;
}

/* BARRA LATERAL */
[data-testid="stSidebar"] {
    background-color: #103d2d;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* BOTONES GENERALES */
.stButton > button {
    background-color: #d9b65b !important;
    color: #173d2b !important;
    border: 2px solid #a98432 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

.stButton > button p,
.stButton > button span {
    color: #173d2b !important;
}

/* PANEL DE CÁMARA */
div[data-testid="stCameraInput"] {
    background-color: #f5f0df !important;
    padding: 22px !important;
    border-radius: 16px !important;
    border: 2px solid #c9a85d !important;
    color: #173d2b !important;
}

/* LETRAS DE LA CÁMARA */
div[data-testid="stCameraInput"] label,
div[data-testid="stCameraInput"] label *,
div[data-testid="stCameraInput"] p,
div[data-testid="stCameraInput"] span,
div[data-testid="stCameraInput"] small,
div[data-testid="stCameraInput"] div {
    color: #173d2b !important;
}

/* BOTONES DE LA CÁMARA */
div[data-testid="stCameraInput"] button {
    background-color: #e3bd62 !important;
    color: #173d2b !important;
    border: 2px solid #a98432 !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

/* TEXTO INTERNO DE LOS BOTONES */
div[data-testid="stCameraInput"] button *,
div[data-testid="stCameraInput"] button p,
div[data-testid="stCameraInput"] button span {
    color: #173d2b !important;
    fill: #173d2b !important;
}

/* ICONOS DE LA CÁMARA */
div[data-testid="stCameraInput"] button svg {
    color: #173d2b !important;
    fill: #173d2b !important;
}

/* CARGADOR DE IMÁGENES */
[data-testid="stFileUploader"] {
    background-color: #f5f0df;
    border: 2px dashed #b99b50;
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stFileUploader"] * {
    color: #173d2b !important;
}

/* IMÁGENES */
.stImage img {
    border-radius: 12px;
    object-fit: contain !important;
}

/* TARJETAS */
.tarjeta {
    background-color: #ffffff;
    border: 1px solid #d5c99f;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

/* PIE DE PÁGINA */
.pie {
    text-align: center;
    color: #52715c;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCIONES
# ==========================================

def cargar_imagen(archivo):
    try:
        return Image.open(archivo).convert("RGB")
    except Exception:
        return None


def detectar_rostros(imagen):
    mp_face_detection = mp.solutions.face_detection

    imagen_np = np.array(imagen)
    alto, ancho, _ = imagen_np.shape

    rostros = []

    with mp_face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    ) as detector:

        resultados = detector.process(imagen_np)

        if resultados.detections:
            for deteccion in resultados.detections:
                caja = deteccion.location_data.relative_bounding_box

                x = max(0, int(caja.xmin * ancho))
                y = max(0, int(caja.ymin * alto))
                w = int(caja.width * ancho)
                h = int(caja.height * alto)

                x2 = min(ancho, x + w)
                y2 = min(alto, y + h)

                if x2 > x and y2 > y:
                    recorte = imagen.crop((x, y, x2, y2))
                    rostros.append(recorte)

    return rostros


def mostrar_portada():
    if ARCHIVO_PORTADA.exists():
        portada = cargar_imagen(ARCHIVO_PORTADA)

        if portada:
            st.image(portada, use_container_width=True)

    st.markdown("""
    <div style="
        background:#103d2d;
        padding:25px;
        border-radius:15px;
        text-align:center;
        border:2px solid #c9a85d;
        margin-top:12px;
    ">
        <h1 style="color:#f0d38b !important;">
            CRISTOFHER AMAZON AI
        </h1>
        <p style="color:#ffffff !important;">
            Sistema de análisis y detección de rostros mediante
            inteligencia artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# MENÚ LATERAL
# ==========================================

st.sidebar.markdown("""
<div style="text-align:center; padding:15px;">
    <h2 style="color:#e3bd62 !important;">
        🌿 CRISTOFHER
    </h2>
    <p style="color:white !important;">
        AMAZON AI
    </p>
</div>
""", unsafe_allow_html=True)

opcion = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Análisis fotográfico",
        "Base fotográfica",
        "Acerca del proyecto"
    ]
)


# ==========================================
# INICIO
# ==========================================

if opcion == "Inicio":

    mostrar_portada()

    st.markdown("## Bienvenido a nuestra aplicación")

    st.write("""
    CRISTOFHER AMAZON AI es una aplicación experimental que
    utiliza herramientas de inteligencia artificial para
    detectar rostros en fotografías.

    Permite cargar una imagen desde el dispositivo o tomar
    una fotografía utilizando la cámara.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="tarjeta">
            <h3>📷 Cámara</h3>
            <p>Captura una fotografía directamente desde tu dispositivo.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tarjeta">
            <h3>🖼️ Fotografías</h3>
            <p>Carga imágenes para realizar la detección de rostros.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="tarjeta">
            <h3>🤖 Inteligencia artificial</h3>
            <p>Detecta y recorta automáticamente los rostros encontrados.</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# ANÁLISIS FOTOGRÁFICO
# ==========================================

elif opcion == "Análisis fotográfico":

    st.title("📷 ANÁLISIS FOTOGRÁFICO")

    st.write("""
    Selecciona una fotografía desde tu dispositivo o utiliza
    la cámara para realizar una captura.
    """)

    modo = st.radio(
        "Selecciona el método de ingreso:",
        ["Subir una fotografía", "Activar cámara"],
        horizontal=True
    )

    archivo = None

    if modo == "Subir una fotografía":

        st.subheader("🖼️ Cargar fotografía")

        archivo = st.file_uploader(
            "Selecciona una imagen",
            type=["jpg", "jpeg", "png"]
        )

    else:

        st.markdown("""
        <div style="
            background:#f5f0df;
            padding:20px;
            border:2px solid #c9a85d;
            border-radius:14px;
            margin-bottom:12px;
        ">
            <h3 style="color:#173d2b !important;">
                📷 ACTIVAR CÁMARA
            </h3>
            <p style="color:#173d2b !important;">
                Utiliza el botón para tomar tu fotografía.
                Los textos y controles están diseñados con colores
                oscuros para facilitar su lectura.
            </p>
        </div>
        """, unsafe_allow_html=True)

        archivo = st.camera_input(
            "",
            key="camara_fotografia"
        )

    if archivo is not None:

        imagen = cargar_imagen(archivo)

        if imagen is not None:

            st.markdown("---")
            st.subheader("Fotografía seleccionada")

            st.image(
                imagen,
                caption="Imagen original",
                use_container_width=True
            )

            if st.button("🔍 ANALIZAR FOTOGRAFÍA"):

                with st.spinner("Analizando la imagen..."):

                    try:
                        rostros = detectar_rostros(imagen)

                        st.markdown("---")
                        st.subheader("Resultados del análisis")

                        if len(rostros) > 0:

                            st.success(
                                f"Se detectaron {len(rostros)} rostro(s) "
                                "en la fotografía."
                            )

                            columnas = st.columns(
                                min(len(rostros), 3)
                            )

                            for i, rostro in enumerate(rostros):

                                with columnas[i % len(columnas)]:
                                    st.image(
                                        rostro,
                                        caption=f"Rostro detectado {i + 1}",
                                        use_container_width=True
                                    )

                            st.markdown("""
                            <div class="tarjeta">
                                <h3>Interpretación del resultado</h3>
                                <p>
                                El sistema identificó regiones faciales
                                en la fotografía y realizó sus respectivos
                                recortes. Este resultado corresponde a
                                una detección automática y no identifica
                                a la persona ni determina su origen étnico.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                        else:

                            st.warning(
                                "No se encontraron rostros. "
                                "Intenta con otra fotografía, procurando "
                                "que el rostro esté bien iluminado y visible."
                            )

                    except Exception as error:
                        st.error(
                            "Ocurrió un problema durante el análisis."
                        )
                        st.caption(str(error))


# ==========================================
# BASE FOTOGRÁFICA DOCUMENTAL
# ==========================================

elif opcion == "Base fotográfica":

    st.title("🖼️ BASE FOTOGRÁFICA DOCUMENTAL")

    st.write("""
    Esta sección presenta material fotográfico de carácter
    documental relacionado con comunidades y culturas de la
    Amazonía peruana.
    """)

    if ARCHIVO_GALERIA.exists():

        galeria = cargar_imagen(ARCHIVO_GALERIA)

        if galeria:
            st.image(
                galeria,
                caption="Galería fotográfica documental",
                use_container_width=True
            )

    else:

        st.info(
            "Todavía no se ha agregado la imagen "
            "'rostros_referencia.png' al proyecto."
        )

    st.warning("""
    Las fotografías de esta galería tienen una finalidad
    exclusivamente documental y cultural. No se utilizan para
    clasificar personas por origen étnico ni para determinar
    pertenencia a una comunidad.
    """)


# ==========================================
# ACERCA DEL PROYECTO
# ==========================================

elif opcion == "Acerca del proyecto":

    st.title("ℹ️ ACERCA DEL PROYECTO")

    st.markdown("""
    <div class="tarjeta">
        <h3>CRISTOFHER AMAZON AI</h3>
        <p>
        Es una aplicación experimental que integra herramientas
        de visión artificial para detectar rostros en fotografías.
        </p>

        <h3>Objetivo</h3>
        <p>
        Facilitar el análisis visual de imágenes mediante
        herramientas de inteligencia artificial.
        </p>

        <h3>Funciones principales</h3>
        <ul>
            <li>Carga de fotografías.</li>
            <li>Captura mediante cámara.</li>
            <li>Detección automática de rostros.</li>
            <li>Recorte de regiones faciales.</li>
            <li>Presentación de resultados.</li>
            <li>Galería fotográfica documental.</li>
        </ul>

        <h3>Consideraciones</h3>
        <p>
        La aplicación realiza detección facial. No identifica
        personas, no verifica identidades y no determina el
        origen étnico de las personas fotografiadas.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("""
<div class="pie">
    CRISTOFHER AMAZON AI |
    Análisis fotográfico mediante inteligencia artificial
</div>
""", unsafe_allow_html=True)










