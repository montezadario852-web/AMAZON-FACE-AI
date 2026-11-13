
import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
from io import BytesIO
import zipfile

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

CARPETA = Path(__file__).parent
BASE_REFERENCIA = CARPETA / "rostros_referencia.png"

# =========================================================
# DISEÑO VISUAL
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
}

.stApp {
    background: #f3f6f2;
}

[data-testid="stSidebar"] {
    background: #103d2d;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    background: linear-gradient(120deg, #103d2d, #205b40);
    padding: 28px;
    border-radius: 20px;
    color: white;
    margin-bottom: 22px;
    border: 1px solid #c8a75b;
}

.hero-brand {
    color: #e8cc82;
    font-size: 17px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero h1 {
    color: white;
    font-size: 31px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #e4eee7;
    font-size: 14px;
    line-height: 1.7;
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

h2, h3 {
    color: #174b35;
}

[data-testid="stImage"] img {
    object-fit: contain !important;
    width: 100%;
    height: auto !important;
    max-height: 650px;
    border-radius: 12px;
}

.stButton button {
    background: #174b35;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
    padding: 10px 18px;
}

.stButton button:hover {
    background: #286746;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCIONES DE IMÁGENES
# =========================================================

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
                    recorte = imagen.crop((x1, y1, x2, y2))
                    recortes.append(recorte)

    return recortes


def cargar_base():
    if BASE_REFERENCIA.exists():
        imagen = abrir_imagen(BASE_REFERENCIA)
        rostros = detectar_rostros(imagen)
        return imagen, rostros

    return None, []


def interpretar_deteccion(cantidad):
    if cantidad == 0:
        return (
            "No se detectaron rostros.",
            "Intenta utilizar una fotografía más clara, "
            "con el rostro visible y sin obstrucciones."
        )

    if cantidad == 1:
        return (
            "Un rostro detectado.",
            "El sistema identificó un rostro en la fotografía "
            "y completó el procesamiento automático."
        )

    return (
        f"{cantidad} rostros detectados.",
        "El sistema identificó varios rostros en la fotografía "
        "y generó sus respectivos recortes."
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


# =========================================================
# ENCABEZADO
# =========================================================

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

    if BASE_REFERENCIA.exists():
        portada = abrir_imagen(BASE_REFERENCIA)
        st.image(
            portada,
            caption="Colección fotográfica documental de referencia",
            use_container_width=True
        )
    else:
        st.info(
            "Agrega el archivo rostros_referencia.png al repositorio "
            "para mostrar la colección documental en la portada."
        )


# =========================================================
# MENÚ LATERAL
# =========================================================

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


# =========================================================
# PÁGINA DE INICIO
# =========================================================

if pagina == "Inicio":

    encabezado()

    st.markdown("## Explora las herramientas de la plataforma")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="panel">
        <h3>📤 Subir fotografía</h3>
        Selecciona una imagen desde tu dispositivo
        para procesarla automáticamente.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
        <h3>📷 Activar cámara</h3>
        Captura una fotografía directamente
        desde la cámara de tu dispositivo.
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
        Visualización de la colección
        documental de referencia.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="small-note">
    Las fotografías documentales se presentan para consulta
    y visualización. La aplicación no determina identidad,
    pertenencia étnica ni origen de las personas.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# IDENTIFICACIÓN Y DETECCIÓN
# =========================================================

elif pagina == "Identificación de rostro":

    encabezado()

    st.markdown("## Procesamiento de fotografía")

    st.markdown("""
    <div class="panel">
    Sube una fotografía o utiliza la cámara.
    El sistema detectará automáticamente los rostros
    que aparezcan en la imagen.
    </div>
    """, unsafe_allow_html=True)

    opcion = st.radio(
        "Selecciona el método de ingreso:",
        ["Subir fotografía", "Tomar fotografía con cámara"],
        horizontal=True
    )

    archivo = None

    if opcion == "Subir fotografía":
        archivo = st.file_uploader(
            "Selecciona una imagen",
            type=["jpg", "jpeg", "png"]
        )

    else:
        archivo = st.camera_input("Tomar fotografía")

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
            "La detección indica la localización de rostros; "
            "no constituye una identificación personal ni "
            "una medición de semejanza étnica."
        )


# =========================================================
# BASE FOTOGRÁFICA DOCUMENTAL
# =========================================================

elif pagina == "Base fotográfica":

    encabezado()

    st.markdown("## Base de fotografías de referencia")

    imagen_base, rostros_base = cargar_base()

    if imagen_base is not None:

        st.markdown("### Colección documental")

        st.image(
            imagen_base,
            caption="Imagen original de la colección",
            use_container_width=True
        )

        st.markdown("### Rostros detectados en la colección")

        if rostros_base:

            st.success(
                f"Se detectaron {len(rostros_base)} rostros "
                "en la fotografía de referencia."
            )

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
                "No se detectaron rostros. Prueba con una imagen "
                "de mayor resolución o con rostros más visibles."
            )

    else:
        st.warning(
            "No se encontró rostros_referencia.png. "
            "Agrega ese archivo a la carpeta principal del repositorio."
        )

    st.markdown("""
    <div class="small-note">
    Esta colección tiene carácter documental y de consulta.
    Sus imágenes no se utilizan para clasificar el origen
    étnico de las personas.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ACERCA DEL PROYECTO
# =========================================================

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

    La aplicación no identifica personas, no determina
    pertenencia étnica y no establece el origen de quienes
    aparecen en las fotografías.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PIE DE PÁGINA
# =========================================================

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







