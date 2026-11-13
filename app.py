
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
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).parent
PORTADA = BASE / "portada_amazonia.jpg"
GALERIA = BASE / "rostros_referencia.png"

# =====================================================
# COLORES
# =====================================================

VERDE = "#123D2B"
VERDE_CLARO = "#205A3B"
DORADO = "#E2BD65"
CREMA = "#FFF9E9"
TEXTO = "#173D2B"
BLANCO = "#FFFFFF"

# =====================================================
# DISEÑO Y VISIBILIDAD
# =====================================================

st.markdown("""
<style>

/* FONDO GENERAL */
.stApp {
    background-color: #FFF9E9 !important;
}

/* TEXTO GENERAL */
.stApp,
.stApp p,
.stApp li,
.stApp label,
.stApp small,
.stApp [data-testid="stMarkdownContainer"] {
    color: #173D2B !important;
}

/* TÍTULOS */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #123D2B !important;
    font-weight: 900 !important;
}

.stApp h1 {
    font-size: 2.5rem !important;
}

.stApp h2 {
    font-size: 2rem !important;
}

.stApp h3 {
    font-size: 1.45rem !important;
}

/* MENÚ LATERAL */
[data-testid="stSidebar"] {
    background-color: #123D2B !important;
}

[data-testid="stSidebar"] * {
    color: #FFF9E9 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F3D17B !important;
}

/* PORTADA */
.hero {
    background: linear-gradient(120deg, #123D2B, #276345);
    border: 3px solid #D9B45B;
    border-radius: 20px;
    padding: 35px 20px;
    text-align: center;
    margin-bottom: 22px;
}

.hero h1 {
    color: #F3D17B !important;
    font-size: 2.8rem !important;
    font-weight: 950 !important;
}

.hero p {
    color: #FFFFFF !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
}

/* TARJETAS */
.panel {
    background: #FFFFFF !important;
    border: 2px solid #D9B45B;
    border-radius: 15px;
    padding: 20px;
    margin: 12px 0;
}

.panel h3,
.panel p,
.panel li {
    color: #173D2B !important;
}

/* RESULTADOS */
.resultado {
    background: #E5F0E5 !important;
    border: 3px solid #205A3B;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.resultado-numero {
    color: #123D2B !important;
    font-size: 3.2rem;
    font-weight: 950;
}

.resultado-texto {
    color: #123D2B !important;
    font-size: 1.5rem;
    font-weight: 900;
}

/* AVISOS */
.nota {
    background: #FFF0C5 !important;
    border-left: 7px solid #B58B30;
    border-radius: 10px;
    padding: 17px;
    color: #49380F !important;
    font-weight: 750;
}

.nota p,
.nota span {
    color: #49380F !important;
}

/* BOTONES */
.stButton > button {
    background: #E2BD65 !important;
    color: #123D2B !important;
    border: 2px solid #98752D !important;
    border-radius: 11px !important;
    min-height: 48px;
    font-size: 1rem !important;
    font-weight: 900 !important;
}

.stButton > button * {
    color: #123D2B !important;
}

/* CAMPOS DE TEXTO */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #173D2B !important;
    border: 2px solid #98752D !important;
}

/* SELECTORES */
.stSelectbox [data-baseweb="select"] {
    background: #FFFFFF !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #173D2B !important;
}

/* CARGA DE IMÁGENES */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 2px solid #D9B45B !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploader"] * {
    color: #173D2B !important;
    font-weight: 750 !important;
}

[data-testid="stFileUploader"] button {
    background: #E2BD65 !important;
    color: #123D2B !important;
}

/* CÁMARA */
[data-testid="stCameraInput"] {
    background: #FFFFFF !important;
    border: 2px solid #D9B45B !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

[data-testid="stCameraInput"] * {
    color: #173D2B !important;
    font-weight: 800 !important;
}

[data-testid="stCameraInput"] button {
    background: #E2BD65 !important;
    color: #123D2B !important;
}

/* MÉTRICAS */
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #123D2B !important;
}

/* RADIO Y CASILLAS */
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #173D2B !important;
    font-weight: 800 !important;
}

/* SEPARADORES */
hr {
    border-color: #D9B45B !important;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES PARA PROCESAR IMÁGENES
# =====================================================

def cargar_imagen(archivo):

    if archivo is None:
        return None

    try:
        img = Image.open(archivo)
        img = ImageOps.exif_transpose(img)
        return img.convert("RGB")

    except Exception:
        return None


def preparar_imagen(img):

    return img.resize((256, 256))


# =====================================================
# SIMILITUD EN ESCALA DE GRISES
# =====================================================

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

    similitud = 100 * (1 - diferencia / 255)

    return float(np.clip(similitud, 0, 100))


# =====================================================
# SIMILITUD DE COLOR RGB
# =====================================================

def histograma_rgb(img):

    matriz = np.asarray(preparar_imagen(img))

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


# =====================================================
# MODELO MATEMÁTICO
# =====================================================

def comparar_imagenes(img1, img2):

    gris = similitud_grises(img1, img2)
    color = similitud_color(img1, img2)

    total = (0.70 * gris) + (0.30 * color)

    return {
        "gris": gris,
        "color": color,
        "total": total
    }


# =====================================================
# INTERPRETACIÓN
# =====================================================

def interpretar(porcentaje):

    if porcentaje >= 85:

        return (
            "MUY SIMILARES",
            "Las imágenes presentan una elevada coincidencia "
            "en los indicadores visuales generales analizados."
        )

    elif porcentaje >= 70:

        return (
            "SIMILARES",
            "Las imágenes comparten varias características "
            "visuales, aunque también presentan diferencias."
        )

    elif porcentaje >= 50:

        return (
            "SIMILITUD MODERADA",
            "Se observan algunas coincidencias y diferencias "
            "en las características visuales."
        )

    else:

        return (
            "POCO SIMILARES",
            "Las imágenes presentan diferencias importantes "
            "en los indicadores visuales analizados."
        )


# =====================================================
# PORTADA PRINCIPAL
# =====================================================

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
        border:3px solid #D9B45B;
        border-radius:18px;
        padding:55px 20px;
        text-align:center;
    ">
        <div style="font-size:65px;">🌿</div>

        <div style="
            color:#F3D17B;
            font-size:30px;
            font-weight:950;
        ">
            BIENVENIDOS A LA AMAZONÍA
        </div>

        <div style="
            color:#FFFFFF;
            font-size:19px;
            font-weight:800;
        ">
            Fotografía principal de la portada
        </div>
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


# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.markdown("# 🌿 CRISTOFHER AMAZON AI")
st.sidebar.markdown("## MENÚ PRINCIPAL")

seccion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Inicio",
        "Comparación matemática",
        "Galería amazónica",
        "Información del proyecto"
    ]
)


# =====================================================
# INICIO
# =====================================================

if seccion == "Inicio":

    st.title("BIENVENIDO A CRISTOFHER AMAZON AI")

    st.write("""
    Esta aplicación permite comparar dos imágenes mediante
    procedimientos matemáticos sencillos.

    Los resultados se presentan mediante porcentajes,
    ecuaciones, gráficos e interpretaciones.
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
        "Selecciona Comparación matemática en el menú "
        "para comenzar."
    )


# =====================================================
# COMPARACIÓN MATEMÁTICA
# =====================================================

elif seccion == "Comparación matemática":

    st.title("COMPARACIÓN MATEMÁTICA DE IMÁGENES")

    st.write("""
    Selecciona dos fotografías para calcular sus
    semejanzas y diferencias visuales generales.
    """)

    st.markdown("""
    <div class="nota">
        El análisis compara imágenes completas.
        No identifica personas ni determina si dos rostros
        pertenecen a una misma persona.
    </div>
    """, unsafe_allow_html=True)

    izquierda, derecha = st.columns(2)

    img1 = None
    img2 = None

    with izquierda:

        st.markdown("""
        <div class="panel">
            <h3>📸 PRIMERA IMAGEN</h3>
            <p>Selecciona o toma la primera fotografía.</p>
        </div>
        """, unsafe_allow_html=True)

        archivo1 = st.file_uploader(
            "Cargar primera imagen",
            type=["jpg", "jpeg", "png"],
            key="imagen1"
        )

        camara1 = st.camera_input(
            "Activar cámara para la primera imagen",
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

            st.info("Todavía no has seleccionado la primera imagen.")

    with derecha:

        st.markdown("""
        <div class="panel">
            <h3>📸 SEGUNDA IMAGEN</h3>
            <p>Selecciona o toma la segunda fotografía.</p>
        </div>
        """, unsafe_allow_html=True)

        archivo2 = st.file_uploader(
            "Cargar segunda imagen",
            type=["jpg", "jpeg", "png"],
            key="imagen2"
        )

        camara2 = st.camera_input(
            "Activar cámara para la segunda imagen",
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

            st.info("Todavía no has seleccionado la segunda imagen.")

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

            # RESULTADO PRINCIPAL

            st.markdown("## RESULTADO GENERAL")

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

            # ECUACIÓN

            st.markdown("## ECUACIÓN MATEMÁTICA UTILIZADA")

            st.write("""
            Para obtener el resultado se utiliza una combinación
            ponderada de dos indicadores visuales.
            """)

            st.latex(
                r"S_v = 0.70S_g + 0.30S_c"
            )

            st.write("Donde:")

            st.latex(
                r"S_v = \text{Similitud visual total}"
            )

            st.latex(
                r"S_g = \text{Similitud en escala de grises}"
            )

            st.latex(
                r"S_c = \text{Similitud de color}"
            )

            # SUSTITUCIÓN

            st.markdown("### SUSTITUCIÓN DE VALORES")

            st.latex(
                rf"S_v = 0.70({datos['gris']:.2f})"
                rf" + 0.30({datos['color']:.2f})"
            )

            st.latex(
                rf"S_v = {total:.2f}\%"
            )

            # RESULTADOS PARCIALES

            st.markdown("## INDICADORES DEL ANÁLISIS")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "SIMILITUD EN ESCALA DE GRISES",
                    f"{datos['gris']:.2f} %"
                )

            with col2:

                st.metric(
                    "SIMILITUD DE COLOR",
                    f"{datos['color']:.2f} %"
                )

            # GRÁFICO

            st.markdown("## GRÁFICO COMPARATIVO")

            grafico = {
                "Indicador": [
                    "Escala de grises",
                    "Color",
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
                y="Porcentaje",
                horizontal=True
            )

            # INTERPRETACIÓN

            st.markdown("## INTERPRETACIÓN DE RESULTADOS")

            st.markdown(f"""
            <div class="panel">

                <h3>{categoria}</h3>

                <p>{explicacion}</p>

                <p>
                    El análisis en escala de grises obtuvo
                    <b>{datos['gris']:.2f} %</b>.
                </p>

                <p>
                    El análisis de color obtuvo
                    <b>{datos['color']:.2f} %</b>.
                </p>

                <p>
                    La combinación matemática de ambos indicadores
                    produjo un resultado de
                    <b>{total:.2f} %</b>.
                </p>

            </div>
            """, unsafe_allow_html=True)

            # OBSERVACIONES

            st.markdown("## OBSERVACIONES")

            st.write("""
            1. La comparación en escala de grises evalúa
               diferencias promedio entre píxeles.

            2. La comparación de color utiliza histogramas
               de los canales rojo, verde y azul (RGB).

            3. La iluminación, el encuadre y la orientación
               pueden modificar los resultados.

            4. Los porcentajes son indicadores experimentales,
               no probabilidades estadísticas ni resultados
               de una prueba de identidad.
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


# =====================================================
# GALERÍA DOCUMENTAL
# =====================================================

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


# =====================================================
# INFORMACIÓN DEL PROYECTO
# =====================================================

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


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL · ANÁLISIS VISUAL · AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)













