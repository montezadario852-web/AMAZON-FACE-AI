
import streamlit as st
import mediapipe as mp
import numpy as np
import cv2
from PIL import Image
from pathlib import Path
from io import BytesIO

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
CARPETA_NEUTRAL = BASE_DIR / "base_neutral"
ARCHIVO_PORTADA = BASE_DIR / "portada_amazonia.jpg"
ARCHIVO_GALERIA = BASE_DIR / "rostros_referencia.png"

CARPETA_NEUTRAL.mkdir(exist_ok=True)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: #f3f6f1;
}
[data-testid="stSidebar"] {
    background: #103d2d;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #103d2d, #1d6347);
    padding: 30px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 22px;
    border: 2px solid #c9a85d;
}
.hero h1 {
    color: #f0d38b;
    font-size: 34px;
    margin-bottom: 8px;
}
.hero p {
    color: white;
    font-size: 16px;
}
.panel {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #dce5dc;
    margin-bottom: 18px;
}
.resultado {
    background: #103d2d;
    color: white;
    padding: 24px;
    border-radius: 15px;
    text-align: center;
    border: 2px solid #c9a85d;
}
.resultado h2 {
    color: #f0d38b;
    font-size: 30px;
}
div[data-testid="stCameraInput"] {
    background: #103d2d !important;
    padding: 20px !important;
    border-radius: 15px !important;
    border: 2px solid #c9a85d !important;
}
div[data-testid="stCameraInput"] label,
div[data-testid="stCameraInput"] label *,
div[data-testid="stCameraInput"] p,
div[data-testid="stCameraInput"] span {
    color: white !important;
}
div[data-testid="stCameraInput"] button,
div[data-testid="stCameraInput"] button * {
    color: #103d2d !important;
}
div[data-testid="stCameraInput"] button {
    background: #e3bd62 !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}
.stButton button {
    background: #176343;
    color: white;
    border: 1px solid #c9a85d;
    border-radius: 10px;
    font-weight: bold;
}
.stButton button:hover {
    background: #c9a85d;
    color: #103d2d;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DETECCIÓN DE ROSTROS
# --------------------------------------------------

mp_face = mp.solutions.face_detection

def detectar_rostros(imagen_pil):
    imagen_rgb = np.array(imagen_pil.convert("RGB"))
    alto, ancho, _ = imagen_rgb.shape

    with mp_face.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    ) as detector:
        resultado = detector.process(imagen_rgb)

    rostros = []

    if resultado.detections:
        for deteccion in resultado.detections:
            caja = deteccion.location_data.relative_bounding_box

            x1 = max(0, int(caja.xmin * ancho))
            y1 = max(0, int(caja.ymin * alto))
            x2 = min(ancho, int((caja.xmin + caja.width) * ancho))
            y2 = min(alto, int((caja.ymin + caja.height) * alto))

            if x2 > x1 and y2 > y1:
                recorte = imagen_rgb[y1:y2, x1:x2]
                if recorte.size:
                    rostros.append(recorte)

    return imagen_rgb, rostros

# --------------------------------------------------
# COMPARACIÓN VISUAL EXPERIMENTAL
# --------------------------------------------------

def obtener_descriptores(rostro):
    gris = cv2.cvtColor(rostro, cv2.COLOR_RGB2GRAY)
    gris = cv2.resize(gris, (300, 300))

    orb = cv2.ORB_create(nfeatures=500)
    puntos, descriptores = orb.detectAndCompute(gris, None)

    return descriptores


def comparar_rostros(rostro_a, rostro_b):
    desc_a = obtener_descriptores(rostro_a)
    desc_b = obtener_descriptores(rostro_b)

    if desc_a is None or desc_b is None:
        return 0.0

    if len(desc_a) < 2 or len(desc_b) < 2:
        return 0.0

    comparador = cv2.BFMatcher(cv2.NORM_HAMMING)
    coincidencias = comparador.knnMatch(desc_a, desc_b, k=2)

    buenas = []
    for pareja in coincidencias:
        if len(pareja) == 2:
            m, n = pareja
            if m.distance < 0.75 * n.distance:
                buenas.append(m)

    denominador = max(1, min(len(desc_a), len(desc_b)))
    return len(buenas) / denominador


def interpretar_similitud(valor):
    if valor >= 0.18:
        return "MUY SIMILAR", "success", (
            "Se encontraron varias coincidencias visuales entre "
            "las imágenes de referencia."
        )
    elif valor >= 0.10:
        return "SIMILAR", "info", (
            "Se encontraron algunas coincidencias visuales."
        )
    elif valor >= 0.05:
        return "MODERADAMENTE SIMILAR", "warning", (
            "Se encontraron coincidencias visuales limitadas."
        )
    elif valor > 0:
        return "POCO SIMILAR", "warning", (
            "Se encontraron pocas coincidencias visuales."
        )
    else:
        return "SIN COINCIDENCIA SUFICIENTE", "secondary", (
            "No se encontraron suficientes características "
            "para establecer una comparación."
        )


def cargar_referencias():
    extensiones = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
    archivos = []

    for extension in extensiones:
        archivos.extend(CARPETA_NEUTRAL.glob(extension))

    return archivos


def analizar_con_base_neutral(rostro):
    archivos = cargar_referencias()
    resultados = []

    for archivo in archivos:
        try:
            referencia = Image.open(archivo).convert("RGB")
            _, rostros_referencia = detectar_rostros(referencia)

            for rostro_ref in rostros_referencia:
                valor = comparar_rostros(rostro, rostro_ref)
                resultados.append({
                    "archivo": archivo.name,
                    "valor": valor
                })
        except Exception:
            continue

    resultados.sort(key=lambda x: x["valor"], reverse=True)
    return resultados

# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

def encabezado():
    if ARCHIVO_PORTADA.exists():
        portada = Image.open(ARCHIVO_PORTADA)
        st.image(portada, use_container_width=True)

    st.markdown("""
    <div class="hero">
        <h1>CRISTOFHER AMAZON AI</h1>
        <h3>Análisis y comparación fotográfica</h3>
        <p>
        Tecnología de visión artificial para la detección de rostros
        y comparación visual de fotografías de referencia.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# MENÚ LATERAL
# --------------------------------------------------

st.sidebar.markdown("# 🌿 AMAZON AI")
st.sidebar.markdown("---")

opcion = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "🏠 Inicio",
        "📷 Análisis fotográfico",
        "🗂️ Base fotográfica",
        "ℹ️ Acerca del proyecto"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("CRISTOFHER AMAZON AI · 2026")

# --------------------------------------------------
# INICIO
# --------------------------------------------------

if opcion == "🏠 Inicio":
    encabezado()

    st.markdown("""
    <div class="panel">
        <h2 style="color:#176343;">Bienvenido a nuestra aplicación</h2>
        <p>
        Esta herramienta permite cargar fotografías o utilizar la cámara
        para detectar rostros y realizar una comparación visual experimental
        con una colección de imágenes neutrales e independientes.
        </p>
        <p>
        La colección documental de fotografías Awajún y Wampis se presenta
        por separado y no se utiliza para clasificar ni comparar el origen
        étnico de las personas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Funciones", "04")
        st.caption("Módulos principales")

    with c2:
        st.metric("Entrada", "Foto / Cámara")
        st.caption("Dos formas de analizar")

    with c3:
        st.metric("Comparación", "Experimental")
        st.caption("Base neutral independiente")

    st.info(
        "Para comenzar, ingresa a «Análisis fotográfico» "
        "desde el menú lateral."
    )

# --------------------------------------------------
# ANÁLISIS FOTOGRÁFICO
# --------------------------------------------------

elif opcion == "📷 Análisis fotográfico":
    encabezado()

    st.markdown("## 📸 Selecciona cómo ingresar la fotografía")

    metodo = st.radio(
        "Método de ingreso",
        ["📁 SUBIR FOTOGRAFÍA", "📷 ACTIVAR CÁMARA"],
        horizontal=True
    )

    archivo_imagen = None

    if metodo == "📁 SUBIR FOTOGRAFÍA":
        archivo_imagen = st.file_uploader(
            "Selecciona una fotografía",
            type=["jpg", "jpeg", "png", "webp"]
        )

    else:
        st.markdown("""
        <div style="
            background:#103d2d;
            padding:16px;
            border-radius:12px;
            color:white;
            border:2px solid #c9a85d;
            margin-bottom:12px;">
            <h3 style="color:#f0d38b;">📷 Cámara fotográfica</h3>
            <p style="color:white;">
            Permite el acceso a la cámara y toma una fotografía
            con el rostro visible.
            </p>
        </div>
        """, unsafe_allow_html=True)

        archivo_imagen = st.camera_input(
            "ACTIVAR CÁMARA Y TOMAR FOTOGRAFÍA",
            key="camara_fotografia"
        )

    if archivo_imagen is not None:
        imagen = Image.open(archivo_imagen).convert("RGB")

        st.markdown("### Fotografía ingresada")
        st.image(imagen, caption="Imagen original", use_container_width=True)

        if st.button("🔍 ANALIZAR FOTOGRAFÍA", use_container_width=True):
            with st.spinner("Analizando la fotografía..."):
                imagen_rgb, rostros = detectar_rostros(imagen)

            st.markdown("---")
            st.markdown("## RESULTADOS DEL ANÁLISIS")

            if len(rostros) == 0:
                st.error(
                    "No se detectó ningún rostro. "
                    "Intenta con una fotografía frontal y bien iluminada."
                )

            else:
                st.success(f"Se detectaron {len(rostros)} rostro(s).")

                for indice, rostro in enumerate(rostros, start=1):
                    st.markdown(f"### Rostro {indice}")

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.image(
                            rostro,
                            caption=f"Rostro detectado {indice}",
                            use_container_width=True
                        )

                    with col2:
                        resultados = analizar_con_base_neutral(rostro)

                        if not resultados:
                            st.warning(
                                "Todavía no hay fotografías válidas en "
                                "la base neutral. Agrega imágenes autorizadas "
                                "a la carpeta base_neutral."
                            )
                        else:
                            mejor = resultados[0]
                            etiqueta, nivel, interpretacion = (
                                interpretar_similitud(mejor["valor"])
                            )

                            st.markdown(
                                f"""
                                <div class="resultado">
                                    <p>RESULTADO DE COMPARACIÓN VISUAL</p>
                                    <h2>{etiqueta}</h2>
                                    <p>Referencia más coincidente:
                                    {mejor["archivo"]}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            st.write("")
                            st.markdown("**Interpretación automática**")
                            st.write(interpretacion)

                            st.caption(
                                "La comparación es experimental y se basa "
                                "en características visuales de las imágenes. "
                                "No identifica personas ni determina origen "
                                "étnico. La categoría no es una probabilidad."
                            )

# --------------------------------------------------
# GALERÍA DOCUMENTAL
# --------------------------------------------------

elif opcion == "🗂️ Base fotográfica":
    encabezado()

    st.markdown("## Galería documental Awajún y Wampis")

    st.write(
        "Esta sección conserva las fotografías como material "
        "documental y cultural. No se utilizan para generar "
        "resultados de comparación facial."
    )

    if ARCHIVO_GALERIA.exists():
        galeria = Image.open(ARCHIVO_GALERIA)
        st.image(
            galeria,
            caption="Colección documental de referencia",
            use_container_width=True
        )
    else:
        st.warning(
            "No se encontró rostros_referencia.png. "
            "Sube el archivo al directorio principal del proyecto."
        )

    st.markdown("---")
    st.markdown("## Base neutral de comparación")

    referencias = cargar_referencias()

    st.write(
        f"Fotografías disponibles para comparación: **{len(referencias)}**"
    )

    st.caption(
        "Esta base debe contener imágenes independientes, autorizadas "
        "y no seleccionadas por origen étnico."
    )

    with st.expander("Ver fotografías de la base neutral"):
        if referencias:
            columnas = st.columns(4)
            for i, archivo in enumerate(referencias):
                try:
                    foto = Image.open(archivo).convert("RGB")
                    with columnas[i % 4]:
                        st.image(foto, use_container_width=True)
                        st.caption(archivo.name)
                except Exception:
                    pass
        else:
            st.info(
                "La carpeta base_neutral está vacía. "
                "Agrega fotografías autorizadas para comenzar."
            )

# --------------------------------------------------
# INFORMACIÓN
# --------------------------------------------------

elif opcion == "ℹ️ Acerca del proyecto":
    encabezado()

    st.markdown("""
    ## Acerca de CRISTOFHER AMAZON AI

    CRISTOFHER AMAZON AI es una aplicación experimental desarrollada
    con Python y herramientas de visión artificial.

    ### Objetivos
    - Detectar rostros en fotografías.
    - Permitir el ingreso de imágenes y el uso de cámara.
    - Realizar comparaciones visuales experimentales con fotografías
      de una base neutral independiente.
    - Presentar interpretaciones automáticas de los resultados.
    - Conservar una galería documental de fotografías Awajún y Wampis.

    ### Consideraciones
    La comparación visual experimental no constituye una identificación
    personal, una verificación de identidad ni una evaluación de origen
    étnico. Sus categorías no representan probabilidades científicas.

    Las fotografías utilizadas deben contar con autorización para su uso.
    """)









