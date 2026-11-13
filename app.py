
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path

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
# CSS: CONTRASTE Y VISIBILIDAD DE TODA LA APLICACIÓN
# =========================================================

st.markdown("""
<style>

/* ===== FONDO PRINCIPAL ===== */

.stApp {
    background-color: #FFF9E9 !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #FFF9E9 !important;
}

[data-testid="stMain"] {
    background-color: #FFF9E9 !important;
}

/* ===== TEXTOS PRINCIPALES ===== */

.stApp p,
.stApp li,
.stApp label,
.stApp span,
.stApp small,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li {
    color: #173D2B;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5 {
    color: #123D2B !important;
    font-weight: 900 !important;
}

/* ===== MENÚ LATERAL COMPLETO ===== */

[data-testid="stSidebar"] {
    background-color: #123D2B !important;
    border-right: 3px solid #F2C968 !important;
}

[data-testid="stSidebar"] > div {
    background-color: #123D2B !important;
}

/* Textos, títulos y párrafos del menú */

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Títulos del menú */

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F2C968 !important;
    font-weight: 950 !important;
}

/* Opciones del índice lateral */

[data-testid="stSidebar"] [data-testid="stRadio"] {
    background-color: #123D2B !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background-color: #205A3B !important;
    color: #FFFFFF !important;
    border: 1px solid #63866E !important;
    border-radius: 9px !important;
    padding: 10px 12px !important;
    margin: 5px 0 !important;
    font-weight: 850 !important;
    opacity: 1 !important;
}

/* Todos los textos dentro de cada opción */

[data-testid="stSidebar"] [data-testid="stRadio"] label * {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

/* Opción seleccionada */

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background-color: #F2C968 !important;
    border: 2px solid #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) * {
    color: #123D2B !important;
    font-weight: 950 !important;
}

/* ===== BOTONES ===== */

.stButton > button {
    background-color: #E2BD65 !important;
    color: #123D2B !important;
    border: 2px solid #98752D !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    font-weight: 900 !important;
    opacity: 1 !important;
}

.stButton > button *,
.stButton > button p {
    color: #123D2B !important;
}

.stButton > button:hover {
    background-color: #F5D989 !important;
    border: 2px solid #123D2B !important;
}

/* ===== CARGA DE ARCHIVOS ===== */

[data-testid="stFileUploader"] {
    background-color: #FFFFFF !important;
    border: 2px solid #B58B30 !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

[data-testid="stFileUploader"] section {
    background-color: #FFFFFF !important;
}

[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] button {
    color: #123D2B !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #E2BD65 !important;
    border: 1px solid #98752D !important;
}

/* ===== CÁMARA ===== */

[data-testid="stCameraInput"] {
    background-color: #FFFFFF !important;
    border: 2px solid #B58B30 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stCameraInput"] * {
    color: #123D2B !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stCameraInput"] button {
    background-color: #E2BD65 !important;
    color: #123D2B !important;
}

/* ===== CAMPOS DE TEXTO ===== */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #123D2B !important;
    border: 2px solid #B58B30 !important;
    border-radius: 8px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #5B665F !important;
    opacity: 1 !important;
}

/* ===== SELECTORES Y LISTAS DESPLEGABLES ===== */

.stSelectbox [data-baseweb="select"] {
    background-color: #FFFFFF !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #123D2B !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #FFFFFF !important;
}

[role="option"] {
    background-color: #FFFFFF !important;
    color: #123D2B !important;
    font-weight: 750 !important;
}

[role="option"]:hover {
    background-color: #F2E6C5 !important;
}

/* ===== RADIO Y CHECKBOX ===== */

[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #123D2B !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* ===== MÉTRICAS ===== */

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
    opacity: 1 !important;
}

/* ===== MENSAJES DE INFORMACIÓN ===== */

[data-testid="stAlert"] {
    background-color: #E8F0E6 !important;
    border: 2px solid #47734F !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #173D2B !important;
    opacity: 1 !important;
}

/* ===== TABLAS ===== */

[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}

/* ===== PORTADA ===== */

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

/* ===== TARJETAS ===== */

.panel {
    background-color: #FFFFFF !important;
    border: 2px solid #D9B45B;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
}

.panel h3,
.panel p,
.panel li {
    color: #173D2B !important;
}

/* ===== RESULTADOS ===== */

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
    font-size: 1.5rem;
    font-weight: 950;
}

/* ===== AVISOS PERSONALIZADOS ===== */

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

/* ===== SEPARADORES ===== */

hr {
    border-color: #D9B45B !important;
}

/* ===== BARRA DE PROGRESO ===== */

[data-testid="stProgress"] > div {
    background-color: #D7E3D7 !important;
}

[data-testid="stProgress"] [data-testid="stProgressBar"] {
    background-color: #205A3B !important;
}

/* ===== PIE DE PÁGINA ===== */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCIONES DE IMÁGENES
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


def preparar_imagen(imagen):
    return imagen.resize((256, 256))


# =========================================================
# SIMILITUD EN ESCALA DE GRISES
# =========================================================

def similitud_grises(img1, img2):

    a = np.asarray(
        preparar_imagen(img1).convert("L"),
        dtype=np.float32
    )

    b = np.asarray(
        preparar_imagen(img2).convert("L"),
        dtype=np.float32
    )

    diferencia = np.mean(np.abs(a - b))

    resultado = 100 * (1 - diferencia / 255)

    return float(np.clip(resultado, 0, 100))


# =========================================================
# SIMILITUD DE COLOR
# =========================================================

def histograma_rgb(imagen):

    matriz = np.asarray(preparar_imagen(imagen))
    histogramas = []

    for canal in range(3):

        hist, _ = np.histogram(
            matriz[:, :, canal],
            bins=32,
            range=(0, 256)
        )

        hist = hist.astype(float)
        hist = hist / (hist.sum() + 1e-10)

        histogramas.append(hist)

    return np.array(histogramas)


def similitud_color(img1, img2):

    h1 = histograma_rgb(img1)
    h2 = histograma_rgb(img2)

    interseccion = np.minimum(h1, h2).sum(axis=1)

    resultado = np.mean(interseccion) * 100

    return float(np.clip(resultado, 0, 100))


# =========================================================
# MODELO MATEMÁTICO
# =========================================================

def comparar_imagenes(img1, img2):

    gris = similitud_grises(img1, img2)
    color = similitud_color(img1, img2)

    total = 0.70 * gris + 0.30 * color

    return {
        "gris": gris,
        "color": color,
        "total": total
    }


# =========================================================
# INTERPRETACIÓN
# =========================================================

def interpretar(valor):

    if valor >= 85:
        return (
            "MUY SIMILARES",
            "Las imágenes presentan una elevada coincidencia "
            "en los indicadores visuales generales analizados."
        )

    elif valor >= 70:
        return (
            "SIMILARES",
            "Las imágenes comparten varias características "
            "visuales, aunque también presentan diferencias."
        )

    elif valor >= 50:
        return (
            "SIMILITUD MODERADA",
            "Se observan algunas coincidencias y diferencias "
            "en las características visuales."
        )

    return (
        "POCO SIMILARES",
        "Las imágenes presentan diferencias importantes "
        "en los indicadores visuales analizados."
    )


# =========================================================
# CABECERA
# =========================================================

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL Y ANÁLISIS VISUAL</p>
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
        text-align:center;
    ">
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
    Plataforma experimental para el análisis matemático
    de similitud visual entre imágenes y la presentación
    documental de fotografías amazónicas.
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
st.sidebar.markdown(
    "### ANÁLISIS VISUAL"
)
st.sidebar.markdown(
    "Tecnología desarrollada con Python y Streamlit."
)


# =========================================================
# SECCIÓN INICIO
# =========================================================

if seccion == "Inicio":

    st.title("BIENVENIDO A CRISTOFHER AMAZON AI")

    st.write("""
    Esta plataforma permite comparar dos imágenes mediante
    procedimientos matemáticos y mostrar sus resultados
    a través de porcentajes, gráficos e interpretaciones.
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="panel">
            <h3>📷 IMÁGENES</h3>
            <p>Carga fotografías desde tu dispositivo
            o utiliza la cámara.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
            <h3>📐 MATEMÁTICAS</h3>
            <p>Calcula indicadores de similitud
            mediante ecuaciones.</p>
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
        "Utiliza el índice lateral para ingresar "
        "a las diferentes secciones."
    )


# =========================================================
# SECCIÓN COMPARACIÓN
# =========================================================

elif seccion == "Comparación matemática":

    st.title("COMPARACIÓN MATEMÁTICA DE IMÁGENES")

    st.write("""
    Selecciona dos fotografías para calcular sus
    semejanzas y diferencias visuales generales.
    """)

    st.markdown("""
    <div class="nota">
        El sistema compara imágenes completas.
        No identifica personas ni determina si dos rostros
        pertenecen a una misma persona.
    </div>
    """, unsafe_allow_html=True)

    izquierda, derecha = st.columns(2)

    img1 = None
    img2 = None

    with izquierda:

        st.subheader("📸 PRIMERA IMAGEN")

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
                caption="PRIMERA IMAGEN",
                use_container_width=True
            )
        else:
            st.info("Selecciona o toma la primera fotografía.")

    with derecha:

        st.subheader("📸 SEGUNDA IMAGEN")

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
                caption="SEGUNDA IMAGEN",
                use_container_width=True
            )
        else:
            st.info("Selecciona o toma la segunda fotografía.")

    st.divider()

    if img1 is not None and img2 is not None:

        if st.button(
            "🔍 CALCULAR SIMILITUD MATEMÁTICA",
            use_container_width=True
        ):

            with st.spinner("Analizando las imágenes..."):

                datos = comparar_imagenes(img1, img2)
                total = datos["total"]
                categoria, explicacion = interpretar(total)

            st.success("ANÁLISIS COMPLETADO")

            st.header("RESULTADO GENERAL")

            st.markdown(f"""
            <div class="resultado">
                <div class="resultado-numero">
                    {total:.2f} %
                </div>
                <div class="resultado-texto">
                    {categoria}
                </div>
                <p style="color:#173D2B !important;">
                    Indicador experimental de similitud visual
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(round(total)))

            st.header("ECUACIÓN MATEMÁTICA")

            st.write("""
            Se utiliza una combinación ponderada de dos
            indicadores visuales:
            """)

            st.latex(r"S_v = 0.70S_g + 0.30S_c")

            st.write("Donde:")

            st.latex(r"S_v = \text{Similitud visual total}")
            st.latex(r"S_g = \text{Similitud en escala de grises}")
            st.latex(r"S_c = \text{Similitud de color RGB}")

            st.subheader("SUSTITUCIÓN DE VALORES")

            st.latex(
                rf"S_v = 0.70({datos['gris']:.2f})"
                rf" + 0.30({datos['color']:.2f})"
            )

            st.latex(rf"S_v = {total:.2f}\%")

            st.header("INDICADORES DEL ANÁLISIS")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "ESCALA DE GRISES",
                    f"{datos['gris']:.2f} %"
                )

            with col2:
                st.metric(
                    "SIMILITUD DE COLOR",
                    f"{datos['color']:.2f} %"
                )

            st.header("GRÁFICO COMPARATIVO")

            grafico = {
                "Indicador": [
                    "Escala de grises",
                    "Color RGB",
                    "Similitud total"
                ],
                "Porcentaje": [
                    datos["gris"],
                    datos["color"],
                    total
                ]
            }

            st.bar_chart(
                grafico,
                x="Indicador",
                y="Porcentaje"
            )

            st.header("INTERPRETACIÓN DE RESULTADOS")

            st.markdown(f"""
            <div class="panel">
                <h3>{categoria}</h3>
                <p>{explicacion}</p>
                <p>La similitud en escala de grises fue
                <b>{datos['gris']:.2f} %</b>.</p>
                <p>La similitud de color fue
                <b>{datos['color']:.2f} %</b>.</p>
                <p>El resultado combinado fue
                <b>{total:.2f} %</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            st.header("OBSERVACIONES")

            st.write("""
            - La escala de grises evalúa diferencias promedio
              entre los píxeles de ambas imágenes.
            - El indicador RGB compara histogramas de color.
            - La iluminación, el encuadre y la orientación
              pueden modificar los resultados.
            - Los porcentajes son indicadores experimentales,
              no probabilidades ni pruebas de identidad.
            """)

            st.warning(
                "Una similitud visual elevada no demuestra "
                "que las imágenes correspondan a la misma persona."
            )

    else:

        st.info(
            "Selecciona las dos imágenes para habilitar "
            "la comparación matemática."
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
        No se utiliza para clasificar personas por origen étnico
        ni para determinar identidades.
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

    Plataforma experimental desarrollada con Python y
    Streamlit para comparar características visuales
    generales de dos imágenes.

    **Tecnologías utilizadas**

    - Python.
    - Streamlit.
    - NumPy.
    - Pillow.

    **Métodos matemáticos**

    - Comparación de píxeles en escala de grises.
    - Comparación de histogramas RGB.
    - Combinación ponderada de indicadores.

    **Objetivo**

    Presentar resultados matemáticos mediante ecuaciones,
    porcentajes, gráficos e interpretaciones comprensibles.
    """)


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.markdown("---")

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL · ANÁLISIS VISUAL · AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)













