
import streamlit as st
import numpy as np
import pandas as pd
import mediapipe as mp
from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
import math

# =====================================================
# CONFIGURACIÓN GENERAL
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

VERDE = "#123D2B"
VERDE2 = "#205A3B"
DORADO = "#F2C968"
CREMA = "#FFF9E9"
BLANCO = "#FFFFFF"
TEXTO = "#173D2B"

# =====================================================
# ESTILOS VISUALES
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #FFF9E9;
    color: #173D2B;
}

header[data-testid="stHeader"] {
    background-color: #FFF9E9;
}

section[data-testid="stSidebar"] {
    background-color: #123D2B;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] label {
    color: #FFFFFF !important;
    font-weight: 700;
}

h1, h2, h3, h4, p, label, span, div {
    color: #173D2B;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

.hero {
    background: linear-gradient(120deg, #123D2B, #205A3B);
    padding: 28px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
    border-bottom: 5px solid #F2C968;
}

.hero h1 {
    color: #F2C968 !important;
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 8px;
}

.hero p {
    color: #FFFFFF !important;
    font-size: 15px;
    font-weight: 600;
}

.panel {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #D9D2BB;
    margin-bottom: 18px;
}

.resultado {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 16px;
    border: 2px solid #D7B45A;
    text-align: center;
    min-height: 145px;
}

.resultado-numero {
    color: #205A3B !important;
    font-size: 43px;
    font-weight: 900;
}

.resultado-texto {
    color: #173D2B !important;
    font-weight: 800;
    font-size: 15px;
}

.nota {
    background: #F4E8C5;
    border-left: 5px solid #C49A35;
    border-radius: 10px;
    padding: 15px;
    margin: 12px 0;
}

.stButton > button {
    background-color: #205A3B;
    color: white !important;
    border: 2px solid #F2C968;
    border-radius: 10px;
    font-weight: 800;
    min-height: 45px;
}

.stButton > button:hover {
    background-color: #123D2B;
    color: #F2C968 !important;
}

.stDownloadButton > button {
    background-color: #205A3B;
    color: white !important;
}

[data-testid="stFileUploader"] {
    background: #FFFFFF;
    padding: 12px;
    border-radius: 12px;
    border: 1px dashed #205A3B;
}

[data-testid="stCameraInput"] {
    background: #FFFFFF;
    padding: 10px;
    border-radius: 12px;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #D9D2BB;
}

[data-testid="stMetricLabel"] {
    color: #173D2B !important;
    font-weight: 800;
}

[data-testid="stMetricValue"] {
    color: #205A3B !important;
    font-weight: 900;
}

.stAlert {
    color: #173D2B !important;
}

div[data-baseweb="select"] * {
    color: #173D2B !important;
}

hr {
    border-color: #D7B45A;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCIONES DE IMAGEN
# =====================================================

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


def obtener_punto(landmarks, indice, ancho, alto):
    punto = landmarks[indice]
    return (
        punto.x * ancho,
        punto.y * alto
    )


# =====================================================
# DETECCIÓN Y MEDICIÓN GEOMÉTRICA
# =====================================================

def analizar_geometria(imagen):
    mp_face_mesh = mp.solutions.face_mesh

    imagen_rgb = np.array(imagen.convert("RGB"))
    alto, ancho, _ = imagen_rgb.shape

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as detector:

        resultado = detector.process(imagen_rgb)

    if not resultado.multi_face_landmarks:
        return None, None, "No se detectó un rostro. Intenta usar una fotografía más clara y frontal."

    landmarks = resultado.multi_face_landmarks[0].landmark

    # Puntos de referencia anatómica aproximada
    frente = obtener_punto(landmarks, 10, ancho, alto)
    menton = obtener_punto(landmarks, 152, ancho, alto)
    lado_izquierdo = obtener_punto(landmarks, 234, ancho, alto)
    lado_derecho = obtener_punto(landmarks, 454, ancho, alto)

    ojo_izquierdo = obtener_punto(landmarks, 33, ancho, alto)
    ojo_derecho = obtener_punto(landmarks, 263, ancho, alto)

    boca_izquierda = obtener_punto(landmarks, 61, ancho, alto)
    boca_derecha = obtener_punto(landmarks, 291, ancho, alto)

    nariz_izquierda = obtener_punto(landmarks, 98, ancho, alto)
    nariz_derecha = obtener_punto(landmarks, 327, ancho, alto)

    centro_boca = (
        (boca_izquierda[0] + boca_derecha[0]) / 2,
        (boca_izquierda[1] + boca_derecha[1]) / 2
    )

    ancho_rostro = distancia(lado_izquierdo, lado_derecho)
    alto_rostro = distancia(frente, menton)

    if ancho_rostro <= 0 or alto_rostro <= 0:
        return None, None, "No fue posible calcular las dimensiones del rostro."

    # Mediciones normalizadas
    medidas = {
        "Proporción alto/ancho": alto_rostro / ancho_rostro,
        "Distancia entre ojos": distancia(
            ojo_izquierdo, ojo_derecho
        ) / ancho_rostro,
        "Ancho de boca": distancia(
            boca_izquierda, boca_derecha
        ) / ancho_rostro,
        "Ancho de nariz": distancia(
            nariz_izquierda, nariz_derecha
        ) / ancho_rostro,
        "Posición vertical de boca": (
            (centro_boca[1] - frente[1]) / alto_rostro
        )
    }

    # Dibujar puntos y líneas de referencia
    imagen_anotada = imagen.copy()
    dibujo = ImageDraw.Draw(imagen_anotada)

    puntos = [
        frente, menton, lado_izquierdo, lado_derecho,
        ojo_izquierdo, ojo_derecho,
        boca_izquierda, boca_derecha,
        nariz_izquierda, nariz_derecha
    ]

    lineas = [
        (frente, menton),
        (lado_izquierdo, lado_derecho),
        (ojo_izquierdo, ojo_derecho),
        (boca_izquierda, boca_derecha),
        (nariz_izquierda, nariz_derecha)
    ]

    for inicio, fin in lineas:
        dibujo.line(
            (inicio[0], inicio[1], fin[0], fin[1]),
            fill="#E0A52B",
            width=max(2, ancho // 300)
        )

    radio = max(3, ancho // 100)

    for x, y in puntos:
        dibujo.ellipse(
            (x-radio, y-radio, x+radio, y+radio),
            fill="#D7A52C",
            outline="#FFFFFF",
            width=2
        )

    return medidas, imagen_anotada, None


# =====================================================
# COMPARACIÓN DE MEDIDAS
# =====================================================

def comparar_medidas(medidas_a, medidas_b):
    filas = []

    coincidencias = []
    diferencias = []

    for nombre in medidas_a:
        valor_a = float(medidas_a[nombre])
        valor_b = float(medidas_b[nombre])

        denominador = max(
            abs(valor_a),
            abs(valor_b),
            1e-9
        )

        diferencia = abs(valor_a - valor_b) / denominador * 100
        coincidencia = max(0, 100 - diferencia)

        coincidencias.append(coincidencia)
        diferencias.append(diferencia)

        filas.append({
            "Medición": nombre,
            "Fotografía A": valor_a,
            "Fotografía B": valor_b,
            "Diferencia (%)": diferencia,
            "Coincidencia geométrica (%)": coincidencia
        })

    porcentaje = float(np.mean(coincidencias))
    diferencia_media = float(np.mean(diferencias))

    return pd.DataFrame(filas), porcentaje, diferencia_media


def interpretar_resultado(porcentaje):
    if porcentaje >= 80:
        categoria = "COINCIDENCIA GEOMÉTRICA ALTA"
        explicacion = (
            "Las medidas geométricas seleccionadas presentan "
            "un nivel alto de concordancia numérica."
        )
    elif porcentaje >= 60:
        categoria = "COINCIDENCIA GEOMÉTRICA MEDIA"
        explicacion = (
            "Las medidas presentan una concordancia intermedia. "
            "Se observan diferencias en algunos indicadores."
        )
    else:
        categoria = "COINCIDENCIA GEOMÉTRICA BAJA"
        explicacion = (
            "Las medidas seleccionadas presentan diferencias "
            "numéricas importantes entre las fotografías."
        )

    return categoria, explicacion


# =====================================================
# ENCABEZADO
# =====================================================

st.markdown("""
<div class="hero">
    <h1>CRISTOFHER AMAZON AI</h1>
    <p>INTELIGENCIA ARTIFICIAL · ANÁLISIS VISUAL · AMAZONÍA</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MENÚ LATERAL
# =====================================================

with st.sidebar:
    st.markdown("## 🌿 CRISTOFHER AMAZON AI")
    st.markdown("---")

    pagina = st.radio(
        "MENÚ PRINCIPAL",
        [
            "Inicio",
            "Comparación matemática",
            "Galería amazónica",
            "Información del proyecto"
        ]
    )

    st.markdown("---")
    st.caption("Análisis geométrico de imágenes faciales")


# =====================================================
# PÁGINA DE INICIO
# =====================================================

if pagina == "Inicio":

    st.subheader("Bienvenido a CRISTOFHER AMAZON AI")

    if PORTADA.exists():
        st.image(
            Image.open(PORTADA),
            use_container_width=True
        )
    else:
        st.markdown("""
        <div class="panel" style="text-align:center;">
            <h2>🌿 AMAZONÍA PERUANA 🌿</h2>
            <p>
            Tecnología, investigación y análisis visual
            inspirados en la riqueza de la Amazonía.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <h3>¿Qué permite realizar esta aplicación?</h3>
        <p>
        Esta herramienta permite analizar dos fotografías y
        calcular diferencias y coincidencias entre determinadas
        proporciones geométricas faciales.
        </p>
        <p>
        El sistema utiliza puntos de referencia para obtener
        mediciones normalizadas y presentar sus resultados
        mediante tablas, porcentajes y gráficos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("INICIAR ANÁLISIS", use_container_width=True):
        st.session_state["ir_comparacion"] = True
        st.rerun()


# =====================================================
# PÁGINA DE COMPARACIÓN
# =====================================================

elif pagina == "Comparación matemática":

    st.subheader("📸 Comparación matemática de dos fotografías")

    st.markdown("""
    <div class="nota">
    <b>Instrucciones:</b> selecciona dos fotografías donde los
    rostros se encuentren visibles. Puedes cargar imágenes desde
    tu computadora o utilizar la cámara.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### FOTOGRAFÍA A")
        archivo_a = st.file_uploader(
            "Subir fotografía A",
            type=["jpg", "jpeg", "png"],
            key="foto_a"
        )
        camara_a = st.camera_input(
            "Activar cámara A",
            key="camara_a"
        )

    with col2:
        st.markdown("### FOTOGRAFÍA B")
        archivo_b = st.file_uploader(
            "Subir fotografía B",
            type=["jpg", "jpeg", "png"],
            key="foto_b"
        )
        camara_b = st.camera_input(
            "Activar cámara B",
            key="camara_b"
        )

    imagen_a = cargar_imagen(
        archivo_a if archivo_a is not None else camara_a
    )

    imagen_b = cargar_imagen(
        archivo_b if archivo_b is not None else camara_b
    )

    if imagen_a is not None and imagen_b is not None:

        st.markdown("---")
        st.markdown("### Fotografías seleccionadas")

        vista_a, vista_b = st.columns(2)

        with vista_a:
            st.image(
                imagen_a,
                caption="Fotografía A",
                use_container_width=True
            )

        with vista_b:
            st.image(
                imagen_b,
                caption="Fotografía B",
                use_container_width=True
            )

        if st.button(
            "🔍 ANALIZAR MEDIDAS GEOMÉTRICAS",
            use_container_width=True
        ):

            with st.spinner("Analizando puntos y medidas..."):

                medidas_a, anotada_a, error_a = analizar_geometria(
                    imagen_a
                )

                medidas_b, anotada_b, error_b = analizar_geometria(
                    imagen_b
                )

            if error_a or error_b:
                if error_a:
                    st.error("Fotografía A: " + error_a)
                if error_b:
                    st.error("Fotografía B: " + error_b)

            else:

                tabla, porcentaje, diferencia_media = comparar_medidas(
                    medidas_a,
                    medidas_b
                )

                categoria, explicacion = interpretar_resultado(
                    porcentaje
                )

                st.session_state["resultado_tabla"] = tabla
                st.session_state["resultado_porcentaje"] = porcentaje
                st.session_state["resultado_diferencia"] = diferencia_media
                st.session_state["resultado_categoria"] = categoria
                st.session_state["resultado_explicacion"] = explicacion
                st.session_state["anotada_a"] = anotada_a
                st.session_state["anotada_b"] = anotada_b

        # Mostrar resultados guardados
        if "resultado_tabla" in st.session_state:

            tabla = st.session_state["resultado_tabla"]
            porcentaje = st.session_state["resultado_porcentaje"]
            diferencia_media = st.session_state["resultado_diferencia"]
            categoria = st.session_state["resultado_categoria"]
            explicacion = st.session_state["resultado_explicacion"]

            st.markdown("---")
            st.header("RESULTADO DE LA COMPARACIÓN")

            r1, r2 = st.columns(2)

            with r1:
                st.markdown(f"""
                <div class="resultado">
                    <div class="resultado-numero">
                        {porcentaje:.1f}%
                    </div>
                    <div class="resultado-texto">
                        COINCIDENCIA GEOMÉTRICA
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                st.markdown(f"""
                <div class="resultado">
                    <div class="resultado-numero">
                        {diferencia_media:.1f}%
                    </div>
                    <div class="resultado-texto">
                        DIFERENCIA GEOMÉTRICA
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.progress(
                int(round(porcentaje)),
                text="Coincidencia entre las medidas seleccionadas"
            )

            st.markdown(f"""
            <div class="panel" style="text-align:center;">
                <h3>{categoria}</h3>
                <p>{explicacion}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="nota">
            El porcentaje expresa la concordancia numérica entre
            las medidas geométricas seleccionadas. No representa
            identidad ni parecido personal entre individuos.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.header("PUNTOS DE REFERENCIA DETECTADOS")

            p1, p2 = st.columns(2)

            with p1:
                st.image(
                    st.session_state["anotada_a"],
                    caption="Mediciones de la fotografía A",
                    use_container_width=True
                )

            with p2:
                st.image(
                    st.session_state["anotada_b"],
                    caption="Mediciones de la fotografía B",
                    use_container_width=True
                )

            st.markdown("---")
            st.header("TABLA DE RESULTADOS MATEMÁTICOS")

            tabla_mostrar = tabla.copy()

            columnas_redondeo = [
                "Fotografía A",
                "Fotografía B",
                "Diferencia (%)",
                "Coincidencia geométrica (%)"
            ]

            tabla_mostrar[columnas_redondeo] = (
                tabla_mostrar[columnas_redondeo].round(4)
            )

            st.dataframe(
                tabla_mostrar,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")
            st.header("GRÁFICO DE COINCIDENCIA POR MEDICIÓN")

            grafico = tabla.set_index("Medición")[
                ["Coincidencia geométrica (%)"]
            ]

            st.bar_chart(
                grafico,
                horizontal=True
            )

            st.header("INTERPRETACIÓN DE LOS RESULTADOS")

            for _, fila in tabla.iterrows():

                st.markdown(
                    f"""
                    <div class="panel">
                        <b>{fila['Medición']}</b>
                        <p>
                        Fotografía A: {fila['Fotografía A']:.4f}
                        </p>
                        <p>
                        Fotografía B: {fila['Fotografía B']:.4f}
                        </p>
                        <p>
                        Diferencia: {fila['Diferencia (%)']:.2f}%
                        </p>
                        <p>
                        Coincidencia geométrica:
                        {fila['Coincidencia geométrica (%)']:.2f}%
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("---")
            st.header("FUNDAMENTO MATEMÁTICO")

            st.markdown("""
            Para cada medida se calcula la diferencia relativa:

            \[
            D_i = \\frac{|A_i-B_i|}{\\max(|A_i|,|B_i|)}\\times100
            \]

            La coincidencia geométrica de cada medición se obtiene mediante:

            \[
            C_i = 100-D_i
            \]

            Finalmente, se calcula el promedio de las coincidencias:

            \[
            C_{promedio}=\\frac{C_1+C_2+\\cdots+C_n}{n}
            \]

            Donde:

            - \(A_i\): medida normalizada de la fotografía A.
            - \(B_i\): medida normalizada de la fotografía B.
            - \(D_i\): diferencia relativa porcentual.
            - \(C_i\): coincidencia geométrica de cada medición.
            - \(n\): número de mediciones consideradas.
            """)

            csv = tabla.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 DESCARGAR RESULTADOS EN CSV",
                data=csv,
                file_name="resultados_geometricos.csv",
                mime="text/csv",
                use_container_width=True
            )

    else:
        st.info(
            "Carga las dos fotografías o utiliza la cámara para comenzar."
        )


# =====================================================
# GALERÍA AMAZÓNICA
# =====================================================

elif pagina == "Galería amazónica":

    st.subheader("🌿 Galería amazónica")

    if GALERIA.exists():
        st.image(
            Image.open(GALERIA),
            caption="Material fotográfico de referencia visual",
            use_container_width=True
        )
    else:
        st.markdown("""
        <div class="panel">
            <h3>Galería de fotografías</h3>
            <p>
            Para mostrar tu galería, agrega el archivo
            rostros_referencia.png a la carpeta principal
            del proyecto.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "La galería es únicamente ilustrativa y documental. "
        "No se utiliza para clasificar personas."
    )


# =====================================================
# INFORMACIÓN DEL PROYECTO
# =====================================================

elif pagina == "Información del proyecto":

    st.subheader("Información del proyecto")

    st.markdown("""
    <div class="panel">
        <h3>CRISTOFHER AMAZON AI</h3>

        <p>
        Proyecto de análisis visual mediante herramientas
        de inteligencia artificial y procesamiento digital
        de imágenes.
        </p>

        <h4>Objetivo</h4>

        <p>
        Obtener mediciones geométricas normalizadas de dos
        fotografías y presentar sus diferencias y coincidencias
        mediante procedimientos matemáticos.
        </p>

        <h4>Tecnologías utilizadas</h4>

        <ul>
            <li>Python.</li>
            <li>Streamlit.</li>
            <li>MediaPipe Face Mesh.</li>
            <li>NumPy.</li>
            <li>Pandas.</li>
            <li>Pillow.</li>
        </ul>

        <h4>Consideración técnica</h4>

        <p>
        Los resultados dependen de la orientación, iluminación,
        resolución, expresión y posición de cada rostro.
        Las mediciones son descriptivas y no determinan
        identidad ni parecido personal.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:15px;">
    <p><b>CRISTOFHER AMAZON AI</b></p>
    <p>INTELIGENCIA ARTIFICIAL · AMAZONÍA PERUANA</p>
</div>
""", unsafe_allow_html=True)














