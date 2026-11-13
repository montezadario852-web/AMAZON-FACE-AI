
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
PORTADA = BASE_DIR / "portada_amazonia.jpg"
GALERIA = BASE_DIR / "rostros_referencia.png"

# =====================================================
# ESTILOS VISUALES
# =====================================================

st.markdown("""
<style>

/* FONDO PRINCIPAL */
.stApp {
    background: #f4f1e7;
    color: #173d2b;
}

/* TEXTOS GENERALES */
html, body, [class*="css"],
p, label, span, small, li {
    color: #173d2b !important;
}

/* TÍTULOS */
h1, h2, h3, h4 {
    color: #174b32 !important;
    font-weight: 850 !important;
}

/* BARRA LATERAL CLARA */
[data-testid="stSidebar"] {
    background: #e8e3d2;
    border-right: 2px solid #c9a85d;
}

[data-testid="stSidebar"] * {
    color: #173d2b !important;
}

/* BOTONES */
.stButton > button {
    background: #dfbd69 !important;
    color: #173d2b !important;
    border: 2px solid #a98432 !important;
    border-radius: 11px !important;
    font-weight: 850 !important;
    min-height: 45px;
}

.stButton > button * {
    color: #173d2b !important;
}

/* CARGADOR DE ARCHIVOS */
[data-testid="stFileUploader"] {
    background: #fffdf6 !important;
    border: 2px dashed #b99b50 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploader"] * {
    color: #173d2b !important;
}

/* CÁMARA */
div[data-testid="stCameraInput"] {
    background: #fffdf6 !important;
    border: 2px solid #c9a85d !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

div[data-testid="stCameraInput"] label,
div[data-testid="stCameraInput"] label *,
div[data-testid="stCameraInput"] p,
div[data-testid="stCameraInput"] span,
div[data-testid="stCameraInput"] small {
    color: #173d2b !important;
    font-weight: 750 !important;
}

div[data-testid="stCameraInput"] button {
    background: #dfbd69 !important;
    color: #173d2b !important;
    border: 2px solid #a98432 !important;
    border-radius: 10px !important;
    font-weight: 850 !important;
}

div[data-testid="stCameraInput"] button * {
    color: #173d2b !important;
    fill: #173d2b !important;
}

/* IMÁGENES SIN DEFORMAR */
.stImage img {
    object-fit: contain !important;
    border-radius: 12px !important;
}

/* TARJETAS */
.tarjeta {
    background: #fffdf6;
    border: 1px solid #c9a85d;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
}

/* RESULTADO */
.resultado {
    background: #e8efdf;
    border: 2px solid #7d9b69;
    border-radius: 15px;
    padding: 22px;
    text-align: center;
}

/* PIE */
.pie {
    text-align: center;
    padding: 22px;
    color: #385b43;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES DE IMÁGENES
# =====================================================

def abrir_imagen(archivo):
    if archivo is None:
        return None

    try:
        imagen = Image.open(archivo)
        imagen = ImageOps.exif_transpose(imagen)
        return imagen.convert("RGB")
    except Exception:
        return None


def obtener_imagen(nombre, clave):
    st.markdown(f"### {nombre}")

    metodo = st.selectbox(
        f"¿Cómo ingresar {nombre.lower()}?",
        ["Subir fotografía", "Usar cámara"],
        key=f"metodo_{clave}"
    )

    archivo = None

    if metodo == "Subir fotografía":
        archivo = st.file_uploader(
            f"Selecciona {nombre.lower()}",
            type=["jpg", "jpeg", "png"],
            key=f"archivo_{clave}"
        )
    else:
        st.markdown(
            f"**Cámara para {nombre.lower()}**"
        )
        archivo = st.camera_input(
            " ",
            key=f"camara_{clave}"
        )

    if archivo is not None:
        return abrir_imagen(archivo)

    return None


# =====================================================
# COMPARACIÓN VISUAL GLOBAL
# =====================================================

def calcular_hash(imagen):
    """
    Calcula un hash perceptual sencillo de la estructura
    visual general de una imagen.
    """

    gris = imagen.convert("L")
    reducido = gris.resize((9, 8), Image.Resampling.LANCZOS)

    matriz = np.asarray(reducido, dtype=np.float32)

    diferencias = matriz[:, 1:] > matriz[:, :-1]

    return diferencias.flatten()


def similitud_estructura(imagen1, imagen2):
    hash1 = calcular_hash(imagen1)
    hash2 = calcular_hash(imagen2)

    distancia = np.count_nonzero(hash1 != hash2)

    total = len(hash1)

    return 1 - (distancia / total)


def histograma_color(imagen):
    """
    Compara la distribución general de colores RGB.
    """

    imagen = imagen.resize((128, 128))
    matriz = np.asarray(imagen)

    histogramas = []

    for canal in range(3):
        hist, _ = np.histogram(
            matriz[:, :, canal],
            bins=32,
            range=(0, 256)
        )

        hist = hist.astype(float)
        hist = hist / (np.linalg.norm(hist) + 1e-10)

        histogramas.extend(hist)

    return np.asarray(histogramas)


def similitud_color(imagen1, imagen2):
    h1 = histograma_color(imagen1)
    h2 = histograma_color(imagen2)

    distancia = np.linalg.norm(h1 - h2)

    similitud = 1 - (distancia / np.sqrt(2))

    return float(np.clip(similitud, 0, 1))


def comparar_imagenes(imagen1, imagen2):
    """
    Combina estructura visual y distribución de colores.
    El resultado es un indicador experimental de semejanza
    entre imágenes completas.
    """

    estructura = similitud_estructura(imagen1, imagen2)
    color = similitud_color(imagen1, imagen2)

    resultado = (
        estructura * 0.60 +
        color * 0.40
    )

    return resultado * 100, estructura * 100, color * 100


def interpretar_resultado(porcentaje):

    if porcentaje >= 85:
        return (
            "MUY SIMILAR",
            "Las imágenes presentan una semejanza visual global alta."
        )

    elif porcentaje >= 70:
        return (
            "SIMILAR",
            "Las imágenes comparten varias características visuales."
        )

    elif porcentaje >= 50:
        return (
            "MODERADAMENTE SIMILAR",
            "Las imágenes presentan algunas características visuales en común."
        )

    else:
        return (
            "POCO SIMILAR",
            "Las imágenes presentan diferencias visuales importantes."
        )


# =====================================================
# ENCABEZADO
# =====================================================

def encabezado():

    if PORTADA.exists():

        portada = abrir_imagen(PORTADA)

        if portada:
            st.image(
                portada,
                use_container_width=True
            )

    else:

        st.markdown("""
        <div style="
            background:linear-gradient(120deg,#103d2d,#315c3c);
            padding:65px 25px;
            border:3px solid #c9a85d;
            border-radius:18px;
            text-align:center;
        ">
            <div style="font-size:55px;">🌿</div>
            <h1 style="color:#f0d38b !important;">
                CRISTOFHER AMAZON AI
            </h1>
            <h3 style="color:#ffffff !important;">
                Inteligencia artificial y análisis visual
            </h3>
            <p style="color:#f5e9c9 !important;">
                Inspirado en la riqueza natural y cultural de la Amazonía peruana
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background:#e9e2ca;
        border-left:6px solid #b18b3d;
        border-radius:10px;
        padding:15px;
        margin-top:15px;
    ">
        <h2 style="color:#173d2b !important;">
            Sistema de comparación de imágenes
        </h2>
        <p style="color:#173d2b !important;">
            Compara dos fotografías y consulta sus características
            de semejanza visual global.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.markdown("""
<div style="text-align:center;padding:15px;">
    <div style="font-size:42px;">🌿</div>
    <h2>CRISTOFHER</h2>
    <h3>AMAZON AI</h3>
    <p>Comparación visual</p>
</div>
""", unsafe_allow_html=True)

opcion = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Comparar dos imágenes",
        "Galería amazónica",
        "Acerca del proyecto"
    ]
)


# =====================================================
# INICIO
# =====================================================

if opcion == "Inicio":

    encabezado()

    st.markdown("## Bienvenido a CRISTOFHER AMAZON AI")

    st.write("""
    Esta aplicación permite ingresar dos fotografías y realizar
    una comparación experimental de su semejanza visual general.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="tarjeta">
            <h3>📷 Imagen 1</h3>
            <p>Sube una fotografía o utiliza la cámara.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tarjeta">
            <h3>📷 Imagen 2</h3>
            <p>Ingresa la segunda fotografía que deseas comparar.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="tarjeta">
            <h3>📊 Resultado</h3>
            <p>Consulta el indicador de semejanza visual y su interpretación.</p>
        </div>
        """, unsafe_allow_html=True)

    st.info(
        "Entra en «Comparar dos imágenes» para comenzar."
    )


# =====================================================
# COMPARAR DOS IMÁGENES
# =====================================================

elif opcion == "Comparar dos imágenes":

    st.title("🔍 COMPARACIÓN DE DOS IMÁGENES")

    st.write("""
    Ingresa dos fotografías para analizar su semejanza visual.
    Puedes cargar imágenes desde tu dispositivo o tomarlas
    directamente con la cámara.
    """)

    col1, col2 = st.columns(2)

    with col1:
        imagen1 = obtener_imagen("IMAGEN 1", "uno")

        if imagen1:
            st.image(
                imagen1,
                caption="Primera fotografía",
                use_container_width=True
            )

    with col2:
        imagen2 = obtener_imagen("IMAGEN 2", "dos")

        if imagen2:
            st.image(
                imagen2,
                caption="Segunda fotografía",
                use_container_width=True
            )

    st.markdown("---")

    if st.button(
        "🔎 COMPARAR LAS DOS IMÁGENES",
        use_container_width=True
    ):

        if imagen1 is None or imagen2 is None:

            st.error(
                "Debes ingresar las dos fotografías antes de comparar."
            )

        else:

            with st.spinner("Analizando las características visuales..."):

                porcentaje, estructura, color = comparar_imagenes(
                    imagen1,
                    imagen2
                )

                categoria, interpretacion = interpretar_resultado(
                    porcentaje
                )

            st.markdown("---")
            st.title("📊 RESULTADOS DE LA COMPARACIÓN")

            st.markdown(
                f"""
                <div class="resultado">
                    <h2 style="color:#173d2b !important;">
                        {categoria}
                    </h2>
                    <div style="
                        font-size:58px;
                        font-weight:900;
                        color:#174b32;
                    ">
                        {porcentaje:.2f}%
                    </div>
                    <p style="color:#173d2b !important;">
                        Indicador experimental de semejanza visual global
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Interpretación")

            st.success(interpretacion)

            st.markdown("### Componentes del análisis")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "Semejanza de estructura visual",
                    f"{estructura:.2f}%"
                )

            with c2:
                st.metric(
                    "Semejanza de distribución de colores",
                    f"{color:.2f}%"
                )

            st.markdown("### Fotografías comparadas")

            r1, r2 = st.columns(2)

            with r1:
                st.image(
                    imagen1,
                    caption="Imagen 1",
                    use_container_width=True
                )

            with r2:
                st.image(
                    imagen2,
                    caption="Imagen 2",
                    use_container_width=True
                )

            st.markdown("""
            <div class="tarjeta">
                <h3>Consideraciones del resultado</h3>
                <p>
                El porcentaje es un indicador experimental calculado
                a partir de características visuales generales,
                principalmente estructura y distribución de colores.
                </p>
                <p>
                No representa una probabilidad estadística ni una
                medición validada de parecido facial. No permite
                identificar personas ni determinar su origen étnico.
                </p>
            </div>
            """, unsafe_allow_html=True)


# =====================================================
# GALERÍA AMAZÓNICA DOCUMENTAL
# =====================================================

elif opcion == "Galería amazónica":

    st.title("🌳 GALERÍA AMAZÓNICA DOCUMENTAL")

    st.write("""
    Espacio destinado a presentar fotografías de carácter
    documental sobre la diversidad cultural y natural de la Amazonía.
    """)

    if GALERIA.exists():

        galeria = abrir_imagen(GALERIA)

        if galeria:
            st.image(
                galeria,
                caption="Galería documental amazónica",
                use_container_width=True
            )

    else:

        st.info(
            "Agrega el archivo rostros_referencia.png "
            "al repositorio para mostrar la galería."
        )

    st.warning("""
    Las fotografías de esta sección tienen finalidad documental.
    No se utilizan para clasificar personas por etnia, comunidad
    u origen cultural.
    """)


# =====================================================
# ACERCA DEL PROYECTO
# =====================================================

elif opcion == "Acerca del proyecto":

    st.title("ℹ️ ACERCA DEL PROYECTO")

    st.markdown("""
    <div class="tarjeta">
        <h2>CRISTOFHER AMAZON AI</h2>

        <p>
        Aplicación experimental orientada a la comparación visual
        de dos imágenes mediante técnicas básicas de procesamiento
        digital.
        </p>

        <h3>Objetivo</h3>

        <p>
        Obtener un indicador de semejanza visual global entre
        dos fotografías.
        </p>

        <h3>Funciones</h3>

        <ul>
            <li>Ingreso de dos fotografías.</li>
            <li>Captura de imágenes mediante cámara.</li>
            <li>Análisis de estructura visual.</li>
            <li>Comparación de distribución de colores.</li>
            <li>Porcentaje experimental de semejanza.</li>
            <li>Interpretación automática del resultado.</li>
        </ul>

        <h3>Limitaciones</h3>

        <p>
        El método no es un sistema biométrico ni un sistema
        de reconocimiento de identidad. Sus porcentajes no
        están calibrados como probabilidades.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("""
<div class="pie">
    🌿 CRISTOFHER AMAZON AI
    <br>
    Comparación experimental de imágenes
    <br>
    Amazonía peruana
</div>
""", unsafe_allow_html=True)











