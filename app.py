
import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path
from io import BytesIO
import zipfile

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

CARPETA = Path(__file__).parent
BASE_REFERENCIA = CARPETA / "rostros_referencia.png"
IMAGEN_PORTADA = CARPETA / "portada_amazonia.jpg"

# =====================================================
# ESTILOS
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background: #f2f6f2;
}

[data-testid="stSidebar"] {
    background: #103d2d;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(120deg, #103d2d, #286044);
    padding: 28px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
    border: 1px solid #c9a85d;
}

.hero-brand {
    color: #e8cc82;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    color: white;
    font-size: 30px;
    font-weight: 800;
    margin-top: 12px;
}

.hero p {
    color: #edf3ee;
    line-height: 1.7;
    font-size: 14px;
}

.panel {
    background: white;
    border: 1px solid #dce5dc;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}

.resultado {
    background: #e9f3eb;
    border-left: 5px solid #25834b;
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
}

.small-note {
    color: #637267;
    font-size: 12px;
}

/* OPCIONES DE CÁMARA Y FOTOGRAFÍA */

[data-testid="stRadio"] label {
    color: #174b35 !important;
    font-weight: 700 !important;
}

[data-testid="stRadio"] p {
    color: #174b35 !important;
    font-weight: 700 !important;
}

[data-testid="stCameraInput"] {
    background: #103d2d !important;
    padding: 18px !important;
    border-radius: 15px !important;
    border: 2px solid #c9a85d !important;
}

[data-testid="stCameraInput"] label,
[data-testid="stCameraInput"] p {
    color: white !important;
    font-weight: 700 !important;
}

[data-testid="stCameraInput"] button {
    background: #e3bd62 !important;
    color: #103d2d !important;
    border: none !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
}

[data-testid="stCameraInput"] button p {
    color: #103d2d !important;
}

[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 2px dashed #8ba994;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p {
    color: #174b35 !important;
    font-weight: 600 !important;
}

/* IMÁGENES SIN DISTORSIÓN */

[data-testid="stImage"] img {
    object-fit: contain !important;
    width: 100%;
    height: auto !important;
    max-height: 650px;
    border-radius: 12px;
}

h2, h3 {
    color: #174b35;
}

.stButton button {
    background: #174b35;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}

.stButton button:hover {
    background: #286746;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES
# =====================================================

def abrir_imagen(archivo):
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)
    return imagen.convert("RGB")


def detectar_rostros(imagen):
    mp_face = mp.solutions.face_detection
    imagen_np = np.array(imagen)
    recortes = []

    with mp_face.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.50
    ) as detector:

        resultado = detector.process(imagen_np)

        if resultado.detections:
            ancho, alto = imagen.size

            for deteccion in resultado.detections:
                caja = deteccion.location_data.relative_bounding_box

                x1 = max(0, int(caja.xmin * ancho))
                y1 = max(0, int(caja.ymin * alto))
                x2 = min(ancho, int((caja.xmin + caja.width) * ancho))
                y2 = min(alto, int((caja.ymin + caja.height) * alto))

                margen_x = int((x2 - x1) * 0.15)
                margen_y = int((y2 - y1) * 0.15)

                x1 = max(0, x1 - margen_x)
                y1 = max(0, y1 - margen_y)
                x2 = min(ancho, x2 + margen_x)
                y2 = min(alto, y2 + margen_y)

                if x2 > x1 and y2 > y1:
                    recortes.append(imagen.crop((x1, y1, x2, y2)))

    return recortes


def interpretar_deteccion(cantidad):
    if cantidad == 0:
        return (
            "No se detectaron rostros.",
            "Intenta con una fotografía más clara, "
            "con el rostro visible y bien iluminado."
        )

    if cantidad == 1:
        return (
            "Un rostro detectado.",
            "El sistema identificó un rostro en la fotografía "
            "y completó el procesamiento automático."
        )

    return (
        f"{cantidad} rostros detectados.",
        "El sistema encontró varios rostros y generó "
        "sus respectivos recortes fotográficos."
    )


def crear_zip(imagenes):
    memoria = BytesIO()

    with zipfile.ZipFile(memoria, "w") as archivo_zip:
        for i, imagen in enumerate(imagenes, start=1):
            buffer = BytesIO()
            imagen.save(buffer, format="PNG")
            archivo_zip.writestr(
                f"rostro_{i}.png",
                buffer.getvalue()
            )

    memoria.seek(0)
    return memoria


# =====================================================
# ENCABEZADO CON IMAGEN INDEPENDIENTE
# =====================================================

def encabezado():

    st.markdown("""
    <div class="hero">
        <div class="hero-brand">🌿 CRISTOFHER AMAZON AI</div>
        <h1>ANÁLISIS Y COMPARACIÓN FOTOGRÁFICA</h1>
        <p>
        Inteligencia artificial aplicada al procesamiento digital
        de imágenes y detección automática de rostros.
        Una herramienta académica para explorar y organizar
        fotografías documentales.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if IMAGEN_PORTADA.exists():
        portada = abrir_imagen(IMAGEN_PORTADA)

        st.image(
            portada,
            caption="Retrato documental de la Amazonía",
            use_container_width=True
        )
    else:
        st.warning(
            "Falta agregar portada_amazonia.jpg al repositorio "
            "para mostrar la fotografía de presentación."
        )


# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.markdown("""
<h2 style="color:#e8cc82 !important;">
🌿 CRISTOFHER AMAZON AI
</h2>
<p style="font-size:12px;">
Procesamiento digital de imágenes
</p>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Identificación de rostro",
        "Base fotográfica",
        "Acerca del proyecto"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Plataforma académica de análisis fotográfico")


# =====================================================
# INICIO
# =====================================================

if pagina == "Inicio":

    encabezado()

    st.markdown("## Explora las herramientas de la plataforma")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="panel">
        <h3>📤 Subir fotografía</h3>
        Selecciona una imagen desde tu dispositivo
        para realizar el procesamiento automático.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
        <h3>📷 Activar cámara</h3>
        Utiliza la cámara para capturar
        una fotografía directamente.
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""
        <div class="panel">
        <h3>🔎 Detectar rostros</h3>
        Localización automática y recorte
        de los rostros encontrados.
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="panel">
        <h3>🖼️ Base fotográfica</h3>
        Visualiza la colección documental
        de fotografías de referencia.
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Para comenzar, ingresa a Identificación de rostro "
        "en el menú lateral."
    )


# =====================================================
# IDENTIFICACIÓN DE ROSTRO
# =====================================================

elif pagina == "Identificación de rostro":

    encabezado()

    st.markdown("## Procesamiento de fotografía")

    st.markdown("""
    <div class="panel">
    Selecciona una de las siguientes opciones para ingresar
    tu fotografía y comenzar la detección automática.
    </div>
    """, unsafe_allow_html=True)

    opcion = st.radio(
        "¿Cómo deseas ingresar la fotografía?",
        [
            "📁 SUBIR FOTOGRAFÍA",
            "📷 ACTIVAR CÁMARA"
        ],
        horizontal=True
    )

    archivo = None

    if opcion == "📁 SUBIR FOTOGRAFÍA":

        st.markdown("### Seleccionar imagen")

        archivo = st.file_uploader(
            "Busca una fotografía en tu dispositivo",
            type=["jpg", "jpeg", "png"],
            key="subir_fotografia"
        )

    else:

        st.markdown("""
        <div style="
        background:#103d2d;
        color:white;
        padding:18px;
        border-radius:14px;
        border:2px solid #c9a85d;
        margin-bottom:12px;">
        <h3 style="color:#e8cc82;">
        📷 CÁMARA ACTIVADA
        </h3>
        <p style="color:white;">
        Permite el acceso a la cámara de tu dispositivo.
        Luego utiliza el botón de captura para tomar la fotografía.
        </p>
        </div>
        """, unsafe_allow_html=True)

        archivo = st.camera_input(
            "ACTIVAR CÁMARA Y TOMAR FOTOGRAFÍA",
            key="camara_fotografia"
        )

    if archivo is not None:

        imagen = abrir_imagen(archivo)

        st.markdown("### Fotografía seleccionada")

        st.image(
            imagen,
            caption="Imagen original",
            use_container_width=True
        )

        with st.spinner("Procesando imagen y detectando rostros..."):
            rostros = detectar_rostros(imagen)

        cantidad = len(rostros)
        titulo, interpretacion = interpretar_deteccion(cantidad)

        st.markdown("## Resultado del procesamiento")

        a, b = st.columns(2)

        with a:
            st.metric("Rostros detectados", cantidad)

        with b:
            st.metric(
                "Estado del procesamiento",
                "Completado" if cantidad > 0 else "Sin detección"
            )

        if cantidad > 0:
            st.success(titulo)
        else:
            st.warning(titulo)

        st.markdown(
            f"""
            <div class="resultado">
            <h3>Interpretación del resultado</h3>
            <p>{interpretacion}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if rostros:

            st.markdown("### Rostros encontrados")

            columnas = st.columns(min(3, cantidad))

            for i, rostro in enumerate(rostros):
                with columnas[i % len(columnas)]:
                    st.image(
                        rostro,
                        caption=f"Rostro detectado {i + 1}",
                        use_container_width=True
                    )

            archivo_zip = crear_zip(rostros)

            st.download_button(
                "📥 Descargar rostros detectados",
                data=archivo_zip,
                file_name="rostros_detectados.zip",
                mime="application/zip"
            )

        st.caption(
            "La detección indica la localización de rostros. "
            "No identifica personas ni determina pertenencia étnica."
        )


# =====================================================
# BASE FOTOGRÁFICA
# =====================================================

elif pagina == "Base fotográfica":

    encabezado()

    st.markdown("## Base de fotografías de referencia")

    if BASE_REFERENCIA.exists():

        imagen_base = abrir_imagen(BASE_REFERENCIA)

        st.markdown("### Colección documental")

        st.image(
            imagen_base,
            caption="Fotografía original de la colección",
            use_container_width=True
        )

        with st.spinner("Detectando rostros de la colección..."):
            rostros_base = detectar_rostros(imagen_base)

        if rostros_base:

            st.success(
                f"Se detectaron {len(rostros_base)} rostros."
            )

            st.markdown("### Rostros encontrados")

            columnas = st.columns(3)

            for i, rostro in enumerate(rostros_base):
                with columnas[i % 3]:
                    st.image(
                        rostro,
                        caption=f"Referencia {i + 1}",
                        use_container_width=True
                    )

            archivo_zip = crear_zip(rostros_base)

            st.download_button(
                "📥 Descargar recortes de referencia",
                data=archivo_zip,
                file_name="rostros_referencia.zip",
                mime="application/zip"
            )

        else:
            st.warning(
                "No se detectaron rostros en la fotografía. "
                "Prueba con una imagen de mayor resolución."
            )

    else:
        st.warning(
            "No se encontró rostros_referencia.png "
            "en la carpeta principal del proyecto."
        )

    st.caption(
        "Las fotografías se conservan como colección documental "
        "y no se utilizan para clasificar el origen étnico."
    )


# =====================================================
# ACERCA DEL PROYECTO
# =====================================================

elif pagina == "Acerca del proyecto":

    encabezado()

    st.markdown("## Acerca de la plataforma")

    st.markdown("""
    <div class="panel">
    <h3>CRISTOFHER AMAZON AI</h3>

    Es una plataforma académica orientada al procesamiento
    digital de imágenes mediante herramientas de inteligencia
    artificial.

    Su función principal es detectar rostros en fotografías,
    generar recortes automáticos y facilitar la organización
    de colecciones fotográficas documentales.

    <h3>Objetivos</h3>

    - Explorar técnicas de procesamiento digital de imágenes.
    - Detectar rostros automáticamente.
    - Organizar fotografías de referencia.
    - Facilitar la visualización de resultados.

    <h3>Alcance y limitaciones</h3>

    La aplicación no identifica personas ni determina
    pertenencia étnica u origen.
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
color:#64756a;
font-size:12px;
padding:12px;">
🌿 CRISTOFHER AMAZON AI<br>
Procesamiento digital de imágenes y detección de rostros
</div>
""", unsafe_allow_html=True)








