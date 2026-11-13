
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
TEXTO = "#173D2B"

# =====================================================
# DISEÑO Y COLORES
# =====================================================
st.markdown(f"""
<style>
.stApp {{
    background-color: {CREMA};
    color: {TEXTO};
}}

[data-testid="stSidebar"] {{
    background-color: {VERDE};
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

h1, h2, h3, h4, p, label {{
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
    font-weight: 900;
}}

.hero p {{
    color: white !important;
    font-size: 15px;
}}

.panel {{
    background: white;
    border: 1px solid #D9D2B8;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}}

.resultado {{
    background: #F2E8C9;
    border-left: 5px solid {DORADO};
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    color: {TEXTO};
}}

.nota {{
    background: #E8F0E9;
    border-left: 5px solid {VERDE2};
    padding: 14px;
    border-radius: 9px;
    margin: 12px 0;
}}

.stButton > button {{
    background-color: {DORADO};
    color: {VERDE} !important;
    border: 1px solid {VERDE};
    border-radius: 9px;
    font-weight: bold;
    min-height: 45px;
}}

[data-testid="stFileUploader"] {{
    background: white;
    padding: 10px;
    border-radius: 10px;
}}

[data-testid="stMetric"] {{
    background: white;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #D9D2B8;
}}

div[data-testid="stMarkdownContainer"] p {{
    color: {TEXTO};
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES GENERALES
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


# =====================================================
# ANÁLISIS GEOMÉTRICO Y TONALIDAD APARENTE
# =====================================================
def analizar_rostro(imagen):

    if imagen is None:
        return None, None, None, "No se recibió una imagen."

    imagen = ImageOps.exif_transpose(imagen).convert("RGB")
    ancho, alto = imagen.size

    if ancho < 50 or alto < 50:
        return None, None, None, "La imagen es demasiado pequeña."

    rgb = np.array(imagen)

    try:
        with mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5
        ) as detector:

            resultado = detector.process(rgb)

    except Exception as error:
        return None, None, None, f"Error al procesar: {error}"

    if not resultado.multi_face_landmarks:
        return None, None, None, "No se detectó un rostro claramente."

    puntos = resultado.multi_face_landmarks[0].landmark

    def punto(indice):
        return (
            puntos[indice].x * ancho,
            puntos[indice].y * alto
        )

    # Puntos de referencia
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
        return None, None, None, "No fue posible calcular las medidas."

    # Mediciones normalizadas
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
            (
                ((labio_sup[1] + labio_inf[1]) / 2)
                - frente[1]
            ) / altura_rostro
    }

    # =================================================
    # ESTIMACIÓN DE TONALIDAD APARENTE
    # =================================================
    # Se toman muestras pequeñas de dos zonas de mejilla.
    # Es una estimación visual, no una clasificación personal.
    muestras = []

    for indice in [123, 352]:

        x = int(puntos[indice].x * ancho)
        y = int(puntos[indice].y * alto)

        radio = max(3, int(min(ancho, alto) * 0.012))

        x1 = max(0, x - radio)
        x2 = min(ancho, x + radio)

        y1 = max(0, y - radio)
        y2 = min(alto, y + radio)

        recorte = rgb[y1:y2, x1:x2]

        if recorte.size > 0:
            muestras.append(
                np.median(
                    recorte.reshape(-1, 3),
                    axis=0
                )
            )

    tono = None

    if muestras:
        color = np.median(muestras, axis=0).astype(int)

        r = int(color[0])
        g = int(color[1])
        b = int(color[2])

        tono = {
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "rgb": (r, g, b)
        }

    # =================================================
    # DIBUJAR REFERENCIAS FACIALES
    # =================================================
    marcada = imagen.copy()
    dibujo = ImageDraw.Draw(marcada)

    referencias = [
        frente, menton,
        mejilla_izq, mejilla_der,
        ojo_izq, ojo_der,
        boca_izq, boca_der,
        nariz_izq, nariz_der,
        labio_sup, labio_inf
    ]

    lineas = [
        (frente, menton),
        (mejilla_izq, mejilla_der),
        (ojo_izq, ojo_der),
        (boca_izq, boca_der),
        (nariz_izq, nariz_der)
    ]

    for inicio, fin in lineas:
        dibujo.line(
            [inicio, fin],
            fill="#D6A82D",
            width=3
        )

    for x, y in referencias:
        radio = 5
        dibujo.ellipse(
            [
                x - radio,
                y - radio,
                x + radio,
                y + radio
            ],
            fill="#1B8A55",
            outline="white",
            width=2
        )

    return medidas, marcada, tono, None


# =====================================================
# DIFERENCIA MATEMÁTICA ENTRE MEDICIONES
# =====================================================
def diferencia_porcentual(a, b):

    promedio = (abs(a) + abs(b)) / 2

    if promedio == 0:
        return 0.0

    return abs(a - b) / promedio * 100


# =====================================================
# CARGA DE FOTOGRAFÍAS
# =====================================================
def obtener_entrada(titulo, clave):

    st.markdown(f"### {titulo}")

    archivo = st.file_uploader(
        "Seleccionar fotografía",
        type=["jpg", "jpeg", "png"],
        key=f"archivo_{clave}"
    )

    camara = st.camera_input(
        "Activar cámara",
        key=f"camara_{clave}"
    )

    seleccionado = archivo if archivo is not None else camara

    if seleccionado is not None:
        try:
            return cargar_imagen(seleccionado)
        except Exception:
            st.error("No se pudo abrir la fotografía.")

    return None


# =====================================================
# ENCABEZADO PRINCIPAL
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
st.sidebar.caption("Análisis visual y geométrico")


# =====================================================
# PÁGINA DE INICIO
# =====================================================
if opcion == "Inicio":

    st.title("Bienvenido a CRISTOFHER AMAZON AI")

    if PORTADA.exists():
        portada = Image.open(PORTADA)
        st.image(portada, use_container_width=True)
    else:
        st.markdown("""
        <div class="panel">
            <h2>🌳 AMAZONÍA PERUANA</h2>
            <p>Entorno de análisis visual y geométrico.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
        <h3>¿Qué puedes realizar?</h3>
        <p>• Cargar dos fotografías.</p>
        <p>• Utilizar la cámara de tu computadora.</p>
        <p>• Detectar puntos de referencia faciales.</p>
        <p>• Calcular proporciones geométricas.</p>
        <p>• Observar diferencias porcentuales entre mediciones.</p>
        <p>• Visualizar muestras de tonalidad aparente de piel.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "Selecciona «Comparación matemática» en el menú "
        "para comenzar."
    )


# =====================================================
# COMPARACIÓN MATEMÁTICA
# =====================================================
elif opcion == "Comparación matemática":

    st.title("Análisis matemático de dos fotografías")

    st.markdown("""
    <div class="nota">
        <b>Procedimiento:</b> se analizan las proporciones geométricas
        de cada fotografía y se presenta por separado una muestra
        del color aparente de la piel. Los resultados no identifican
        personas ni determinan el parecido entre ellas.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        imagen1 = obtener_entrada("IMAGEN 1", "uno")

    with col2:
        imagen2 = obtener_entrada("IMAGEN 2", "dos")

    if imagen1 is not None:
        st.markdown("#### Vista previa de imagen 1")
        st.image(imagen1, use_container_width=True)

    if imagen2 is not None:
        st.markdown("#### Vista previa de imagen 2")
        st.image(imagen2, use_container_width=True)

    if st.button(
        "CALCULAR RESULTADOS",
        use_container_width=True
    ):

        if imagen1 is None or imagen2 is None:

            st.warning(
                "Debes cargar las dos fotografías o tomarlas con la cámara."
            )

        else:

            with st.spinner(
                "Analizando puntos y proporciones geométricas..."
            ):

                medidas1, marcada1, tono1, error1 = analizar_rostro(imagen1)
                medidas2, marcada2, tono2, error2 = analizar_rostro(imagen2)

            if error1:
                st.error(f"Imagen 1: {error1}")

            if error2:
                st.error(f"Imagen 2: {error2}")

            if not error1 and not error2:

                st.success(
                    "El análisis de las dos fotografías se completó."
                )

                # =====================================
                # REFERENCIAS FACIALES
                # =====================================
                st.markdown("## Puntos de referencia detectados")

                c1, c2 = st.columns(2)

                with c1:
                    st.markdown("**IMAGEN 1**")
                    st.image(
                        marcada1,
                        use_container_width=True
                    )

                with c2:
                    st.markdown("**IMAGEN 2**")
                    st.image(
                        marcada2,
                        use_container_width=True
                    )

                # =====================================
                # TONALIDAD APARENTE DE PIEL
                # =====================================
                st.markdown("---")
                st.markdown("## TONALIDAD APARENTE DE PIEL")

                tc1, tc2 = st.columns(2)

                with tc1:

                    st.markdown("### Imagen 1")

                    if tono1:

                        st.markdown(
                            f"""
                            <div style="
                                background-color:{tono1['hex']};
                                height:100px;
                                border-radius:12px;
                                border:2px solid #123D2B;
                            "></div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"**Código HEX:** `{tono1['hex']}`"
                        )

                        st.markdown(
                            f"**Código RGB:** `{tono1['rgb']}`"
                        )

                    else:
                        st.warning(
                            "No se pudo obtener una muestra de color."
                        )

                with tc2:

                    st.markdown("### Imagen 2")

                    if tono2:

                        st.markdown(
                            f"""
                            <div style="
                                background-color:{tono2['hex']};
                                height:100px;
                                border-radius:12px;
                                border:2px solid #123D2B;
                            "></div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"**Código HEX:** `{tono2['hex']}`"
                        )

                        st.markdown(
                            f"**Código RGB:** `{tono2['rgb']}`"
                        )

                    else:
                        st.warning(
                            "No se pudo obtener una muestra de color."
                        )

                st.caption(
                    "El color mostrado es una estimación de las zonas "
                    "muestreadas en cada fotografía. No se utiliza para "
                    "comparar personas ni determinar identidad."
                )

                # =====================================
                # TABLA DE MEDICIONES
                # =====================================
                st.markdown("---")
                st.markdown("## RESULTADOS MATEMÁTICOS")

                nombres = list(medidas1.keys())

                datos = []

                for nombre in nombres:

                    valor1 = medidas1[nombre]
                    valor2 = medidas2[nombre]

                    diferencia = diferencia_porcentual(
                        valor1,
                        valor2
                    )

                    datos.append({
                        "Medición geométrica": nombre,
                        "Imagen 1": round(valor1, 4),
                        "Imagen 2": round(valor2, 4),
                        "Diferencia relativa (%)": round(
                            diferencia,
                            2
                        )
                    })

                tabla = pd.DataFrame(datos)

                st.dataframe(
                    tabla,
                    use_container_width=True,
                    hide_index=True
                )

                # =====================================
                # GRÁFICO
                # =====================================
                st.markdown("## GRÁFICO DE DIFERENCIAS")

                grafico = tabla.set_index(
                    "Medición geométrica"
                )["Diferencia relativa (%)"]

                st.bar_chart(grafico)

                # =====================================
                # INTERPRETACIÓN
                # =====================================
                st.markdown("## INTERPRETACIÓN DE RESULTADOS")

                for fila in datos:

                    nombre = fila["Medición geométrica"]
                    diferencia = fila["Diferencia relativa (%)"]

                    if diferencia < 5:

                        interpretacion = (
                            "La diferencia numérica entre ambas "
                            "mediciones es pequeña."
                        )

                    elif diferencia < 15:

                        interpretacion = (
                            "La diferencia numérica entre ambas "
                            "mediciones es intermedia."
                        )

                    else:

                        interpretacion = (
                            "La diferencia numérica entre ambas "
                            "mediciones es considerable."
                        )

                    st.markdown(
                        f"""
                        <div class="resultado">
                            <b>{nombre}</b><br>
                            Diferencia relativa:
                            <b>{diferencia:.2f}%</b><br>
                            {interpretacion}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =====================================
                # FÓRMULA
                # =====================================
                st.markdown("---")
                st.markdown("## MÉTODO MATEMÁTICO")

                st.latex(
                    r"D(\%) = "
                    r"\frac{|M_1-M_2|}"
                    r"{\frac{|M_1|+|M_2|}{2}}"
                    r"\times 100"
                )

                st.write(
                    "M₁ y M₂ representan los valores de una misma "
                    "medición geométrica en cada fotografía. "
                    "La fórmula calcula su diferencia relativa."
                )

                # =====================================
                # DESCARGAR RESULTADOS
                # =====================================
                st.markdown("---")

                st.download_button(
                    "DESCARGAR RESULTADOS EN CSV",
                    data=tabla.to_csv(
                        index=False
                    ).encode("utf-8-sig"),
                    file_name="resultados_geometricos.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                st.markdown("""
                <div class="nota">
                    <b>Nota técnica:</b> las mediciones son aproximadas
                    y dependen de la detección de puntos faciales.
                    La estimación de color puede variar según las
                    condiciones de captura. Esta aplicación no realiza
                    reconocimiento de identidad, clasificación de origen
                    ni determinación de parecido entre personas.
                </div>
                """, unsafe_allow_html=True)


# =====================================================
# GALERÍA AMAZÓNICA
# =====================================================
elif opcion == "Galería amazónica":

    st.title("Galería amazónica")

    if GALERIA.exists():

        galeria = Image.open(GALERIA)
        st.image(
            galeria,
            use_container_width=True
        )

    else:

        st.info(
            "Agrega rostros_referencia.png a tu repositorio "
            "para mostrar la galería."
        )

    st.caption(
        "Galería documental. Las imágenes no se utilizan "
        "como base de datos de identificación."
    )


# =====================================================
# INFORMACIÓN DEL PROYECTO
# =====================================================
elif opcion == "Información del proyecto":

    st.title("Información del proyecto")

    st.markdown("""
    <div class="panel">
        <h3>CRISTOFHER AMAZON AI</h3>

        <p>
        Aplicación demostrativa desarrollada con Python y Streamlit.
        </p>

        <p>
        <b>Tecnologías utilizadas:</b>
        Python, MediaPipe, NumPy, Pandas y Pillow.
        </p>

        <p>
        <b>Procesamiento:</b>
        detección de puntos de referencia, cálculo de distancias,
        proporciones geométricas y estimación de muestras de color.
        </p>

        <p>
        <b>Resultados:</b>
        tablas, gráficos, diferencias porcentuales y muestras
        de tonalidad aparente de cada fotografía.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================
st.markdown("---")

st.markdown(
    f"""
    <p style="
        text-align:center;
        color:{VERDE};
        font-weight:bold;
    ">
        CRISTOFHER AMAZON AI · AMAZONÍA PERUANA
    </p>
    """,
    unsafe_allow_html=True
)
















