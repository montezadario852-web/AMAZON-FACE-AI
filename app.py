
import streamlit as st
import numpy as np
import pandas as pd
import mediapipe as mp
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
import math

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

VERDE = "#123D2B"
VERDE2 = "#205A3B"
DORADO = "#F2C968"
CREMA = "#FFF9E9"
BLANCO = "#FFFFFF"
TEXTO = "#173D2B"

BASE = Path(__file__).parent
PORTADA = BASE / "portada_amazonia.jpg"
GALERIA = BASE / "rostros_referencia.png"

# =========================================================
# ESTILOS
# =========================================================
st.markdown(f"""
<style>
.stApp {{
    background: {CREMA};
    color: {TEXTO};
}}
[data-testid="stSidebar"] {{
    background: {VERDE};
}}
[data-testid="stSidebar"] * {{
    color: white !important;
}}
h1, h2, h3, h4, p, label, span {{
    color: {TEXTO};
}}
.hero {{
    background: linear-gradient(120deg, {VERDE}, {VERDE2});
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 24px;
    border: 2px solid {DORADO};
}}
.hero h1 {{
    color: {DORADO} !important;
    font-size: 34px;
    margin-bottom: 8px;
}}
.hero p {{
    color: white !important;
    font-size: 15px;
    margin: 0;
}}
.panel {{
    background: white;
    border: 1px solid #D9D2B8;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
}}
.resultado {{
    background: #F2E8C9;
    border-left: 5px solid {DORADO};
    padding: 16px;
    border-radius: 10px;
    margin: 12px 0;
}}
.nota {{
    background: #E8F0E9;
    border-left: 5px solid {VERDE2};
    padding: 14px;
    border-radius: 9px;
    margin: 12px 0;
}}
.stButton > button {{
    background: {DORADO};
    color: {VERDE} !important;
    border: 1px solid {VERDE};
    border-radius: 9px;
    font-weight: bold;
}}
[data-testid="stFileUploader"] {{
    background: white;
    border-radius: 10px;
    padding: 10px;
}}
[data-testid="stMetric"] {{
    background: white;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #D9D2B8;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES
# =========================================================
mp_face_mesh = mp.solutions.face_mesh

def cargar_imagen(archivo):
    if archivo is None:
        return None
    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)
    return imagen.convert("RGB")

def distancia(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )

def analizar_rostro(imagen):
    """Obtiene proporciones geométricas normalizadas del rostro."""
    if imagen is None:
        return None, None, "No se recibió una imagen."

    imagen = ImageOps.exif_transpose(imagen).convert("RGB")
    ancho, alto = imagen.size

    if ancho < 50 or alto < 50:
        return None, None, "La imagen es demasiado pequeña."

    rgb = np.array(imagen)

    try:
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5
        ) as face_mesh:
            resultado = face_mesh.process(rgb)
    except Exception as error:
        return None, None, f"No se pudo procesar la imagen: {error}"

    if not resultado.multi_face_landmarks:
        return None, None, "No se detectó un rostro claramente."

    puntos = resultado.multi_face_landmarks[0].landmark

    def punto(indice):
        return (
            puntos[indice].x * ancho,
            puntos[indice].y * alto
        )

    # Referencias geométricas de Face Mesh
    frente = punto(10)
    menton = punto(152)
    mejilla_izq = punto(234)
    mejilla_der = punto(454)
    ojo_izq = punto(33)
    ojo_der = punto(263)
    boca_izq = punto(61)
    boca_der = punto(291)
    nariz_izq = punto(129)
    nariz_der = punto(358)
    labio_sup = punto(13)
    labio_inf = punto(14)

    altura_rostro = distancia(frente, menton)
    ancho_rostro = distancia(mejilla_izq, mejilla_der)

    if altura_rostro <= 0 or ancho_rostro <= 0:
        return None, None, "No fue posible calcular las proporciones."

    # Medidas relativas: no dependen del tamaño de la fotografía.
    medidas = {
        "Proporción altura/ancho del rostro":
            altura_rostro / ancho_rostro,

        "Distancia entre ojos/ancho del rostro":
            distancia(ojo_izq, ojo_der) / ancho_rostro,

        "Ancho de boca/ancho del rostro":
            distancia(boca_izq, boca_der) / ancho_rostro,

        "Ancho de nariz/ancho del rostro":
            distancia(nariz_izq, nariz_der) / ancho_rostro,

        "Posición vertical de la boca":
            (((labio_sup[1] + labio_inf[1]) / 2) - frente[1])
            / altura_rostro
    }

    # Dibujo de puntos y referencias geométricas
    marcada = imagen.copy()
    dibujo = ImageDraw.Draw(marcada)

    referencias = [
        frente, menton, mejilla_izq, mejilla_der,
        ojo_izq, ojo_der, boca_izq, boca_der,
        nariz_izq, nariz_der, labio_sup, labio_inf
    ]

    lineas = [
        (frente, menton),
        (mejilla_izq, mejilla_der),
        (ojo_izq, ojo_der),
        (boca_izq, boca_der),
        (nariz_izq, nariz_der)
    ]

    for inicio, fin in lineas:
        dibujo.line([inicio, fin], fill="#D6A82D", width=3)

    for x, y in referencias:
        radio = 5
        dibujo.ellipse(
            [x-radio, y-radio, x+radio, y+radio],
            fill="#1B8A55",
            outline="white",
            width=2
        )

    return medidas, marcada, None

def diferencia_porcentual(a, b):
    """Diferencia relativa entre dos medidas, no entre identidades."""
    promedio = (abs(a) + abs(b)) / 2
    if promedio == 0:
        return 0.0
    return abs(a - b) / promedio * 100

def obtener_entrada(titulo, clave):
    st.markdown(f"### {titulo}")

    archivo = st.file_uploader(
        "Cargar fotografía",
        type=["jpg", "jpeg", "png"],
        key=f"archivo_{clave}"
    )

    camara = st.camera_input(
        "O tomar fotografía con la cámara",
        key=f"camara_{clave}"
    )

    seleccionado = archivo if archivo is not None else camara

    if seleccionado is not None:
        try:
            return cargar_imagen(seleccionado)
        except Exception:
            st.error("No se pudo abrir la imagen.")
    return None

# =========================================================
# ENCABEZADO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL · ANÁLISIS GEOMÉTRICO · AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# MENÚ
# =========================================================
opcion = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Comparación matemática",
        "Galería amazónica",
        "Información del proyecto"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("🌿 **CRISTOFHER AMAZON AI**")
st.sidebar.caption("Herramienta demostrativa de análisis geométrico.")

# =========================================================
# INICIO
# =========================================================
if opcion == "Inicio":
    st.title("Bienvenido")

    if PORTADA.exists():
        portada = Image.open(PORTADA)
        st.image(portada, use_container_width=True)
    else:
        st.markdown(
            '<div class="panel"><h3>🌳 Amazonía peruana</h3>'
            '<p>Entorno de análisis geométrico de rostros.</p></div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="panel">
        <h3>¿Qué permite realizar esta aplicación?</h3>
        <p>Detectar puntos de referencia faciales y calcular proporciones
        geométricas normalizadas de dos fotografías.</p>
        <p>Los resultados presentan las medidas de cada imagen y las
        diferencias matemáticas entre ellas.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Entra en «Comparación matemática» para cargar dos fotografías "
        "o utilizar la cámara."
    )

# =========================================================
# COMPARACIÓN MATEMÁTICA
# =========================================================
elif opcion == "Comparación matemática":
    st.title("Análisis matemático de medidas faciales")

    st.markdown("""
    <div class="nota">
        <b>Alcance del análisis:</b> se calculan proporciones geométricas
        visibles de cada fotografía. Los porcentajes representan diferencias
        entre mediciones, no un porcentaje de parecido entre personas.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        imagen1 = obtener_entrada("IMAGEN 1", "uno")

    with col2:
        imagen2 = obtener_entrada("IMAGEN 2", "dos")

    if imagen1 is not None:
        st.markdown("#### Fotografía 1")
        st.image(imagen1, use_container_width=True)

    if imagen2 is not None:
        st.markdown("#### Fotografía 2")
        st.image(imagen2, use_container_width=True)

    if st.button("CALCULAR MEDIDAS GEOMÉTRICAS", use_container_width=True):
        if imagen1 is None or imagen2 is None:
            st.warning("Primero debes cargar las dos fotografías o tomarlas con la cámara.")
        else:
            with st.spinner("Calculando puntos y proporciones geométricas..."):
                medidas1, marcada1, error1 = analizar_rostro(imagen1)
                medidas2, marcada2, error2 = analizar_rostro(imagen2)

            if error1:
                st.error(f"Imagen 1: {error1}")

            if error2:
                st.error(f"Imagen 2: {error2}")

            if not error1 and not error2:
                st.success("Se calcularon las medidas de ambas fotografías.")

                st.markdown("## Referencias geométricas detectadas")
                c1, c2 = st.columns(2)

                with c1:
                    st.markdown("**Imagen 1**")
                    st.image(marcada1, use_container_width=True)

                with c2:
                    st.markdown("**Imagen 2**")
                    st.image(marcada2, use_container_width=True)

                nombres = list(medidas1.keys())

                datos = []
                for nombre in nombres:
                    valor1 = medidas1[nombre]
                    valor2 = medidas2[nombre]
                    diferencia = diferencia_porcentual(valor1, valor2)

                    datos.append({
                        "Medición geométrica": nombre,
                        "Imagen 1": round(valor1, 4),
                        "Imagen 2": round(valor2, 4),
                        "Diferencia relativa (%)": round(diferencia, 2)
                    })

                tabla = pd.DataFrame(datos)

                st.markdown("## Resultados numéricos")
                st.dataframe(
                    tabla,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("## Diferencias por medición")

                grafico = tabla.set_index("Medición geométrica")[
                    "Diferencia relativa (%)"
                ]
                st.bar_chart(grafico)

                st.markdown("## Interpretación de resultados")

                for fila in datos:
                    nombre = fila["Medición geométrica"]
                    diferencia = fila["Diferencia relativa (%)"]

                    if diferencia < 5:
                        interpretacion = (
                            "Las dos mediciones presentan una diferencia "
                            "numérica pequeña."
                        )
                    elif diferencia < 15:
                        interpretacion = (
                            "Las mediciones presentan una diferencia "
                            "numérica intermedia."
                        )
                    else:
                        interpretacion = (
                            "Las mediciones presentan una diferencia "
                            "numérica considerable."
                        )

                    st.markdown(
                        f"""
                        <div class="resultado">
                            <b>{nombre}</b><br>
                            Diferencia relativa: <b>{diferencia:.2f}%</b><br>
                            {interpretacion}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("## Método matemático")

                st.latex(
                    r"D(\\%) = "
                    r"\\frac{|M_1-M_2|}"
                    r"{\\frac{|M_1|+|M_2|}{2}}"
                    r"\\times 100"
                )

                st.write(
                    "Donde M₁ y M₂ son los valores de una misma medición "
                    "geométrica obtenidos en cada fotografía. Un valor menor "
                    "indica que esa medición específica tiene valores más "
                    "cercanos; no representa parecido entre personas."
                )

                st.download_button(
                    "DESCARGAR RESULTADOS EN CSV",
                    data=tabla.to_csv(index=False).encode("utf-8-sig"),
                    file_name="resultados_geometricos.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.warning(
                    "Los resultados dependen de la detección automática "
                    "de puntos y de la posición del rostro. Son mediciones "
                    "aproximadas con fines demostrativos; no identifican "
                    "personas ni determinan parentesco, identidad u origen."
                )

# =========================================================
# GALERÍA
# =========================================================
elif opcion == "Galería amazónica":
    st.title("Galería amazónica")

    if GALERIA.exists():
        st.image(GALERIA, use_container_width=True)
    else:
        st.info(
            "Agrega el archivo rostros_referencia.png al repositorio "
            "para mostrar aquí la galería."
        )

    st.caption(
        "Galería documental. Las imágenes no se utilizan como base "
        "de datos de identificación."
    )

# =========================================================
# INFORMACIÓN
# =========================================================
elif opcion == "Información del proyecto":
    st.title("Información del proyecto")

    st.markdown("""
    <div class="panel">
        <h3>CRISTOFHER AMAZON AI</h3>
        <p>Aplicación demostrativa desarrollada con Python y Streamlit.</p>
        <p><b>Tecnologías:</b> Python, MediaPipe, NumPy, Pandas y Pillow.</p>
        <p><b>Procedimiento:</b> detección de puntos faciales, cálculo de
        distancias y normalización de proporciones geométricas.</p>
        <p><b>Resultado:</b> tabla de mediciones y diferencias porcentuales
        entre valores geométricos de dos fotografías.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "La herramienta no realiza reconocimiento facial ni emite "
        "conclusiones sobre la identidad o el parecido de las personas."
    )

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:{VERDE};'>"
    "CRISTOFHER AMAZON AI · AMAZONÍA PERUANA</p>",
    unsafe_allow_html=True
)















