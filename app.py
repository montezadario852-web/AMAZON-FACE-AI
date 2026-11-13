
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image

# ==========================================
# CONFIGURACION
# ==========================================

st.set_page_config(
    page_title="CRISTOFHER AMAZON AI",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# DISENO AMAZONIA PERUANA
# ==========================================

st.markdown("""
<style>
.stApp {
    background:
      radial-gradient(circle at 85% 5%, #285b3e, transparent 32%),
      linear-gradient(135deg,#06180f,#123c29,#071a12);
    color: #f5f0df;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#06170f,#16452e);
    border-right: 1px solid #d2ad59;
}
h1,h2,h3 {
    color: #e8cb82 !important;
}
p,label {
    color: #f5f0df;
}
.hero {
    background: linear-gradient(120deg,#16452e,#092117);
    border: 1px solid #d2ad59;
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 12px 35px #0007;
}
.hero-title {
    color: #f0d58e;
    font-size: 38px;
    font-weight: 900;
}
.hero-icons {
    font-size: 35px;
    letter-spacing: 7px;
}
.panel {
    background: #102b1e;
    border: 1px solid #927c49;
    border-radius: 16px;
    padding: 20px;
}
div.stButton > button {
    background: linear-gradient(90deg,#c49b45,#e8ce83);
    color: #142318;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    min-height: 44px;
}
[data-testid="stMetric"] {
    background: #123526;
    border: 1px solid #927c49;
    border-radius: 14px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DETECCION Y MEDICION FACIAL
# ==========================================

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils


def distancia(a, b):
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def analizar_fotografia(foto):

    imagen = np.array(foto.convert("RGB"))
    alto, ancho = imagen.shape[:2]

    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5
    ) as detector:

        resultado = detector.process(imagen)

    if not resultado.multi_face_landmarks:
        return None

    rostro = resultado.multi_face_landmarks[0]
    puntos = rostro.landmark

    def punto(i):
        return (
            puntos[i].x * ancho,
            puntos[i].y * alto
        )

    ancho_rostro = distancia(punto(234), punto(454))
    alto_rostro = distancia(punto(10), punto(152))

    if ancho_rostro <= 0 or alto_rostro <= 0:
        return None

    medidas = {
        "Distancia entre ojos":
            distancia(punto(33), punto(263)) / ancho_rostro,
        "Ancho de nariz":
            distancia(punto(98), punto(327)) / ancho_rostro,
        "Ancho de boca":
            distancia(punto(61), punto(291)) / ancho_rostro,
        "Relacion altura/ancho":
            alto_rostro / ancho_rostro
    }

    # Dibujar malla facial
    anotada = imagen.copy()

    mp_drawing.draw_landmarks(
        image=anotada,
        landmark_list=rostro,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing.DrawingSpec(
            color=(80, 210, 145),
            thickness=1,
            circle_radius=1
        )
    )

    # Calidad tecnica de la fotografia
    gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)

    brillo = float(np.mean(gris))
    nitidez = float(
        cv2.Laplacian(gris, cv2.CV_64F).var()
    )

    xs = np.array([p.x for p in puntos])
    proporcion = float(xs.max() - xs.min())

    calidad_brillo = np.clip(
        100 - abs(brillo - 127) * 0.9, 0, 100
    )

    calidad_nitidez = np.clip(
        nitidez / 150 * 100, 0, 100
    )

    calidad_tamano = np.clip(
        proporcion / 0.45 * 100, 0, 100
    )

    calidad = round(
        0.35 * calidad_brillo
        + 0.40 * calidad_nitidez
        + 0.25 * calidad_tamano
    )

    return {
        "imagen": anotada,
        "medidas": medidas,
        "calidad": calidad,
        "brillo": round(brillo, 2),
        "nitidez": round(nitidez, 2),
        "tamano": round(proporcion * 100, 2)
    }


# ==========================================
# MENU
# ==========================================

st.sidebar.markdown(
    "<h2 style='color:#e8cb82'>🌿 CRISTOFHER AMAZON AI</h2>",
    unsafe_allow_html=True
)

st.sidebar.caption(
    "Inteligencia artificial y geometria facial"
)

pagina = st.sidebar.radio(
    "MENU PRINCIPAL",
    ["Inicio", "Analisis facial", "Acerca del proyecto"],
    key="pagina"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌳 Amazonia peruana")
st.sidebar.caption("Naturaleza · Ciencia · Tecnologia")


# ==========================================
# INICIO
# ==========================================

if pagina == "Inicio":

    st.markdown("""
    <div class="hero">
        <div class="hero-icons">🌿 🌳 🦜 🌊 🌴</div>
        <div class="hero-title">CRISTOFHER AMAZON AI</div>
        <h3>Geometria facial e inteligencia artificial</h3>
        <p>
        Una herramienta experimental que utiliza vision
        computacional para detectar puntos faciales,
        calcular proporciones y visualizar resultados.
        </p>
        <p style="color:#e8cb82;font-weight:bold;">
        TECNOLOGIA INSPIRADA EN LA AMAZONIA PERUANA
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        with st.container(border=True):
            st.subheader("📷 Analisis facial")
            st.write(
                "Sube una fotografia o utiliza la camara "
                "para detectar puntos faciales."
            )
            st.button(
                "COMENZAR ANALISIS",
                use_container_width=True,
                on_click=lambda: st.session_state.update(
                    {"pagina": "Analisis facial"}
                )
            )

    with c2:
        with st.container(border=True):
            st.subheader("📊 Resultados")
            st.write(
                "Visualiza las medidas, los graficos "
                "y la calidad tecnica de cada fotografia."
            )
            st.write("Cada imagen se procesa individualmente.")

    st.markdown("### 🌱 Nuestra inspiracion")

    st.write(
        "La biodiversidad, los paisajes, los rios y "
        "la vegetacion de la Amazonia peruana inspiran "
        "la identidad visual de esta aplicacion."
    )

    st.info(
        "El analisis es geometrico y experimental. "
        "No identifica personas ni determina origen etnico."
    )


# ==========================================
# ANALISIS FACIAL
# ==========================================

elif pagina == "Analisis facial":

    st.title("📷 Analisis geometrico facial")

    st.write(
        "Selecciona una fotografia o activa la camara."
    )

    c1, c2 = st.columns(2)

    with c1:
        archivo = st.file_uploader(
            "SUBIR FOTOGRAFIA",
            type=["jpg", "jpeg", "png"]
        )

    with c2:
        camara = st.camera_input("ACTIVAR CAMARA")

    foto = camara if camara is not None else archivo

    if foto is not None:

        imagen = Image.open(foto).convert("RGB")

        st.image(
            imagen,
            caption="Fotografia seleccionada",
            use_container_width=True
        )

        if st.button(
            "🔍 ANALIZAR FOTOGRAFIA",
            use_container_width=True
        ):

            with st.spinner("Procesando fotografia..."):
                st.session_state["resultado"] = (
                    analizar_fotografia(imagen)
                )

        resultado = st.session_state.get("resultado")

        if resultado is None and "resultado" in st.session_state:
            st.error(
                "No se detecto un rostro. "
                "Prueba con una fotografia frontal y bien iluminada."
            )

        elif resultado is not None:

            st.success("Analisis completado.")

            st.markdown("## 🧭 Malla facial detectada")

            st.image(
                resultado["imagen"],
                caption="Puntos y conexiones geometricas",
                use_container_width=True
            )

            st.markdown("## 📊 Indicadores")

            calidad = resultado["calidad"]

            a, b, c = st.columns(3)

            a.metric("Calidad de captura", f"{calidad}%")
            b.metric("Medidas calculadas", len(resultado["medidas"]))
            c.metric("Nitidez", resultado["nitidez"])

            st.progress(calidad / 100)

            st.caption(
                "Este porcentaje representa calidad tecnica "
                "de captura, no semejanza entre personas."
            )

            st.markdown("## 📐 Medidas geometricas")

            datos = pd.DataFrame({
                "Caracteristica": list(resultado["medidas"].keys()),
                "Valor normalizado": list(resultado["medidas"].values())
            })

            grafico = px.bar(
                datos,
                x="Caracteristica",
                y="Valor normalizado",
                color="Valor normalizado",
                color_continuous_scale=["#286747", "#d9b65e"],
                title="Proporciones geometricas detectadas"
            )

            grafico.update_layout(
                paper_bgcolor="#102b1e",
                plot_bgcolor="#102b1e",
                font_color="#f5f0df",
                coloraxis_showscale=False
            )

            st.plotly_chart(
                grafico,
                use_container_width=True
            )

            st.dataframe(
                datos,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("## 📝 Interpretacion")

            if calidad >= 75:
                st.success(
                    "La fotografia presenta condiciones tecnicas "
                    "favorables para la deteccion y medicion."
                )
            elif calidad >= 50:
                st.warning(
                    "La calidad es intermedia. Se recomienda "
                    "mejorar iluminacion y enfoque."
                )
            else:
                st.error(
                    "La calidad es baja. Se recomienda tomar "
                    "otra fotografia."
                )

            detalles = pd.DataFrame({
                "Indicador": [
                    "Brillo promedio",
                    "Nitidez",
                    "Tamano relativo del rostro"
                ],
                "Valor": [
                    resultado["brillo"],
                    resultado["nitidez"],
                    f'{resultado["tamano"]}%'
                ]
            })

            st.markdown("### Detalles tecnicos")
            st.dataframe(
                detalles,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Las medidas son descriptores geometricos "
                "experimentales. No determinan identidad, etnia "
                "ni pertenencia a una comunidad."
            )

    else:
        st.info(
            "Primero sube una fotografia o activa la camara."
        )


# ==========================================
# ACERCA DEL PROYECTO
# ==========================================

elif pagina == "Acerca del proyecto":

    st.title("🌳 Acerca de CRISTOFHER AMAZON AI")

    st.markdown("""
    <div class="hero">
        <h2>Amazonia peruana y tecnologia</h2>
        <p>
        Aplicacion experimental de vision computacional
        para la deteccion de puntos faciales y el calculo
        de proporciones geometricas.
        </p>
        <div class="hero-icons">🌿 🌳 🦜 🐸 🌺 🌊</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Tecnologias utilizadas")

    st.write("- Python")
    st.write("- Streamlit")
    st.write("- MediaPipe")
    st.write("- OpenCV")
    st.write("- NumPy")
    st.write("- Pandas")
    st.write("- Plotly")

    st.markdown("### Objetivo")

    st.write(
        "Desarrollar una herramienta educativa para "
        "explorar la deteccion facial y el analisis "
        "geometrico mediante vision computacional."
    )

    st.warning(
        "La aplicacion no determina identidad ni origen "
        "etnico a partir de una fotografia."
    )


# ==========================================
# PIE DE PAGINA
# ==========================================

st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:#d9c58c;'>"
    "🌿 CRISTOFHER AMAZON AI | AMAZONIA PERUANA 🌿"
    "</p>",
    unsafe_allow_html=True
)





