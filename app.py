
import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DISEÑO VISUAL
# =====================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 90% 0%, #244b35 0%, transparent 35%),
        linear-gradient(135deg, #08170f, #10291c, #173b28);
    color: #f5f5ef;
}

[data-testid="stSidebar"] {
    background: #09180f;
    border-right: 1px solid #c7a65e;
}

[data-testid="stSidebar"] * {
    color: #f5f5ef;
}

h1, h2, h3 {
    color: #dfc17b !important;
}

p {
    color: #eeeeea;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #10291c, #28543a);
    border: 1px solid #c7a65e;
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,.22);
}

.brand {
    color: #e1c27a;
    font-size: 17px;
    font-weight: 900;
    letter-spacing: 3px;
}

.hero-title {
    color: white;
    font-size: clamp(28px, 4vw, 43px);
    font-weight: 900;
    margin-top: 14px;
    line-height: 1.15;
}

.hero-description {
    color: #e8eee7;
    font-size: 16px;
    margin-top: 12px;
    max-width: 800px;
    line-height: 1.6;
}

.panel {
    background: linear-gradient(145deg, #193b29, #10291c);
    border: 1px solid #45684d;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 18px;
}

.result-card {
    background: linear-gradient(145deg, #193b29, #10291c);
    border: 1px solid #c7a65e;
    border-radius: 20px;
    padding: 28px;
    text-align: center;
}

.result-title {
    color: #dfc17b;
    font-size: 24px;
    font-weight: 900;
}

.result-description {
    color: #f5f5ef;
    font-size: 16px;
    line-height: 1.7;
    margin-top: 15px;
}

div.stButton > button {
    background: linear-gradient(90deg, #d9b66f, #f0d99b);
    color: #10251b;
    border: none;
    border-radius: 11px;
    font-weight: 900;
    min-height: 45px;
}

div.stButton > button:hover {
    background: #ffffff;
    color: #10251b;
}

[data-testid="stImage"] img {
    object-fit: contain !important;
    width: 100%;
    height: auto !important;
    max-height: 650px;
    border-radius: 12px;
}

[data-testid="stFileUploader"] {
    background: #193b29;
    border: 1px dashed #c7a65e;
    border-radius: 14px;
    padding: 12px;
}

[data-testid="stCameraInput"] {
    background: #193b29;
    border-radius: 14px;
    padding: 12px;
}

hr {
    border-color: #45684d;
}

.footer {
    color: #c8c8bd;
    font-size: 12px;
    text-align: center;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES DE IMAGEN
# =====================================================

def abrir_imagen(archivo):
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)
    imagen = imagen.convert("RGB")
    return np.array(imagen)


def detectar_rostros(imagen):

    recortes = []
    coordenadas = []

    with mp.solutions.face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.50
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

                # Margen alrededor del rostro
                margen_x = int((x2 - x1) * 0.12)
                margen_y = int((y2 - y1) * 0.12)

                x1 = max(0, x1 - margen_x)
                y1 = max(0, y1 - margen_y)
                x2 = min(ancho, x2 + margen_x)
                y2 = min(alto, y2 + margen_y)

                recorte = imagen[y1:y2, x1:x2]

                if recorte.size > 0:
                    recortes.append(recorte)
                    coordenadas.append((x1, y1, x2, y2))

    return recortes, coordenadas


def interpretar_deteccion(numero):

    if numero == 0:
        return (
            "No se identificaron rostros en la fotografía. "
            "Intenta utilizar una imagen frontal, nítida "
            "y con iluminación adecuada."
        )

    elif numero == 1:
        return (
            "Se detectó un rostro en la fotografía. "
            "El sistema completó el procesamiento de la imagen "
            "y generó el recorte correspondiente."
        )

    else:
        return (
            f"Se detectaron {numero} rostros en la fotografía. "
            "El sistema procesó cada rostro por separado."
        )


# =====================================================
# BASE FOTOGRÁFICA
# =====================================================

RUTA_BASE = Path("rostros_referencia.png")

imagen_referencia = None
rostros_referencia = []

if RUTA_BASE.exists():

    imagen_referencia = abrir_imagen(RUTA_BASE)

    rostros_referencia, _ = detectar_rostros(
        imagen_referencia
    )


# =====================================================
# ENCABEZADO PRINCIPAL
# =====================================================

st.markdown("""
<div class="hero">

    <div class="brand">
        🌿 CRISTOFHER AMAZON AI
    </div>

    <div class="hero-title">
        IDENTIFICACIÓN DE ROSTRO
    </div>

    <div class="hero-description">
        Plataforma académica de procesamiento digital
        de imágenes y detección automática de rostros.
        Una herramienta para explorar fotografías y
        organizar una colección documental de referencia.
    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.markdown("""
<div style="text-align:center;padding:15px 5px;">
    <div style="font-size:35px;">🌿</div>
    <div style="color:#dfc17b;font-size:18px;font-weight:900;">
        CRISTOFHER
    </div>
    <div style="color:white;font-size:13px;letter-spacing:2px;">
        AMAZON AI
    </div>
</div>
""", unsafe_allow_html=True)

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

st.sidebar.caption(
    "Sistema académico de procesamiento de imágenes"
)


# =====================================================
# PÁGINA DE INICIO
# =====================================================

if pagina == "Inicio":

    st.subheader("Bienvenido a nuestra plataforma")

    st.write(
        "Explora las herramientas de procesamiento facial "
        "y la colección fotográfica documental del proyecto."
    )

    if imagen_referencia is not None:

        st.markdown(
            '<div class="panel"><h3>Base fotográfica de referencia</h3></div>',
            unsafe_allow_html=True
        )

        st.image(
            imagen_referencia,
            use_container_width=True,
            caption="Imagen original de referencia"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="panel">
                    <h3>{len(rostros_referencia)}</h3>
                    <p>Rostros detectados en la referencia</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                """
                <div class="panel">
                    <h3>Automático</h3>
                    <p>Procesamiento de fotografías</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                """
                <div class="panel">
                    <h3>Visual</h3>
                    <p>Organización de imágenes</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "No se encontró rostros_referencia.png. "
            "Verifica que esté en la carpeta principal del repositorio."
        )

    st.markdown("""
    <div class="panel">
        <h3>¿Qué permite realizar esta aplicación?</h3>
        <p>
        • Cargar fotografías desde un dispositivo.<br>
        • Utilizar la cámara.<br>
        • Detectar rostros automáticamente.<br>
        • Recortar rostros de imágenes de referencia.<br>
        • Visualizar los resultados del procesamiento.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# IDENTIFICACIÓN DE ROSTRO
# =====================================================

elif pagina == "Identificación de rostro":

    st.subheader("Procesamiento de fotografía")

    st.write(
        "Selecciona una fotografía o utiliza la cámara "
        "para detectar los rostros presentes en la imagen."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.markdown("""
        <div class="panel">
            <h3>📁 Subir fotografía</h3>
            <p>Selecciona una imagen desde tu dispositivo.</p>
        </div>
        """, unsafe_allow_html=True)

        archivo = st.file_uploader(
            "Seleccionar imagen",
            type=["jpg", "jpeg", "png"],
            key="archivo_usuario"
        )

    with col2:

        st.markdown("""
        <div class="panel">
            <h3>📷 Activar cámara</h3>
            <p>Captura una fotografía directamente.</p>
        </div>
        """, unsafe_allow_html=True)

        captura = st.camera_input(
            "Tomar fotografía",
            key="camara_usuario"
        )

    imagen_usuario = None

    if archivo is not None:
        imagen_usuario = abrir_imagen(archivo)

    elif captura is not None:
        imagen_usuario = abrir_imagen(captura)

    if imagen_usuario is not None:

        st.markdown("---")
        st.subheader("Vista previa")

        st.image(
            imagen_usuario,
            caption="Fotografía seleccionada",
            use_container_width=True
        )

        if st.button(
            "INICIAR DETECCIÓN DE ROSTRO",
            use_container_width=True
        ):

            with st.spinner("Procesando imagen..."):

                rostros_usuario, cajas = detectar_rostros(
                    imagen_usuario
                )

            numero = len(rostros_usuario)

            st.markdown("---")
            st.subheader("Resultado del procesamiento")

            if numero == 0:

                st.error(interpretar_deteccion(0))

            else:

                st.success(
                    f"Procesamiento completado: "
                    f"{numero} rostro(s) detectado(s)."
                )

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-title">
                            ROSTRO DETECTADO
                        </div>
                        <div style="
                            color:#dfc17b;
                            font-size:48px;
                            font-weight:900;
                            margin:10px;
                        ">
                            {numero}
                        </div>
                        <div class="result-description">
                            {interpretar_deteccion(numero)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("---")
                st.subheader("Fotografías procesadas")

                columnas = st.columns(3, gap="large")

                for i, rostro in enumerate(rostros_usuario):

                    with columnas[i % 3]:

                        st.image(
                            rostro,
                            caption=f"Rostro detectado {i + 1}",
                            use_container_width=True
                        )

                st.info(
                    "La detección identifica la presencia y ubicación "
                    "de rostros. No determina identidad ni pertenencia "
                    "a un grupo étnico."
                )

    else:

        st.markdown("""
        <div class="panel">
            <h3>Comienza tu procesamiento</h3>
            <p>
            Sube una fotografía o utiliza la cámara.
            La aplicación detectará los rostros y mostrará
            sus recortes sin deformar las imágenes.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# BASE DE FOTOGRAFÍAS
# =====================================================

elif pagina == "Base de fotografías":

    st.subheader("Base fotográfica de referencia")

    st.write(
        "Esta sección permite visualizar la fotografía original "
        "y revisar los rostros detectados automáticamente."
    )

    if imagen_referencia is None:

        st.error(
            "No se encontró rostros_referencia.png. "
            "Verifica el archivo en GitHub."
        )

    else:

        st.markdown("### Imagen original")

        st.image(
            imagen_referencia,
            use_container_width=True,
            caption="Colección fotográfica original"
        )

        st.markdown("---")

        st.subheader("Rostros detectados")

        if not rostros_referencia:

            st.warning(
                "No se detectaron rostros. "
                "Es posible que la imagen tenga rostros pequeños "
                "o una resolución insuficiente."
            )

        else:

            st.success(
                f"Se detectaron {len(rostros_referencia)} rostros."
            )

            columnas = st.columns(3, gap="large")

            for i, rostro in enumerate(rostros_referencia):

                with columnas[i % 3]:

                    st.image(
                        rostro,
                        caption=f"Imagen de referencia {i + 1}",
                        use_container_width=True
                    )


# =====================================================
# ACERCA DEL PROYECTO
# =====================================================

elif pagina == "Acerca del proyecto":

    st.subheader("Acerca de CRISTOFHER AMAZON AI")

    st.markdown("""
    <div class="panel">

        <h3>Descripción</h3>

        <p>
        CRISTOFHER AMAZON AI es una aplicación académica
        desarrollada para el procesamiento digital de imágenes
        y la detección automática de rostros.
        </p>

        <h3>Base documental</h3>

        <p>
        El proyecto cuenta con una colección documental de
        fotografías de referencia relacionadas con imágenes
        de personas de los pueblos originarios Awajún y Wampis.
        </p>

        <h3>Funciones principales</h3>

        <p>
        • Carga de fotografías.<br>
        • Captura mediante cámara.<br>
        • Detección automática de rostros.<br>
        • Recorte de rostros de referencia.<br>
        • Organización y visualización de imágenes.
        </p>

        <h3>Consideración metodológica</h3>

        <p>
        La detección facial permite localizar rostros en imágenes.
        No determina identidad, origen étnico ni pertenencia
        a una comunidad.
        </p>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown("""
<div class="footer">
    🌿 CRISTOFHER AMAZON AI<br>
    Plataforma académica de procesamiento de imágenes<br>
    © 2026
</div>
""", unsafe_allow_html=True)






