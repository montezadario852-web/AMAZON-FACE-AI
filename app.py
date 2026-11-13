
import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="AMAZON FACE AI",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# DISEÑO VISUAL
# ==========================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #061B11, #103923);
    color: white;
}

section[data-testid="stSidebar"] {
    background: #041F14;
    border-right: 2px solid #B9953B;
}

h1, h2, h3, p, label {
    color: white !important;
}

.gold {
    color: #E7BD50;
}

.hero {
    background: linear-gradient(110deg, #062719, #17462D);
    border: 2px solid #C39B3B;
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #E7BD50 !important;
    font-size: 43px;
    font-weight: 900;
}

.hero h3 {
    font-size: 21px;
}

.hero p {
    font-size: 17px;
}

.panel {
    background: linear-gradient(145deg, #0B3823, #062719);
    border: 2px solid #C49D42;
    border-radius: 17px;
    padding: 22px;
    min-height: 150px;
}

.stButton button {
    background: #DDB447;
    color: #102719;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    min-height: 45px;
}

.stButton button:hover {
    background: #F1CE69;
    color: #102719;
}

/* PANEL DE RESULTADOS */

.result-card {
    background: linear-gradient(130deg, #062719, #0B3823);
    border: 2px solid #D4AD45;
    border-radius: 20px;
    padding: 25px;
    margin-top: 15px;
    box-shadow: 0 0 20px rgba(213,173,66,0.18);
}

.result-title {
    color: #E8BD4F;
    font-size: 27px;
    font-weight: 900;
    text-align: center;
}

/* ARO ANIMADO */

.gauge {
    width: 205px;
    height: 205px;
    border-radius: 50%;
    background: conic-gradient(
        #EBC34F 0deg,
        #D49C26 250deg,
        #17442C 250deg,
        #17442C 360deg
    );
    margin: 22px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: girar 8s linear infinite;
    box-shadow: 0 0 25px rgba(230,184,58,0.38);
}

.gauge-inner {
    width: 165px;
    height: 165px;
    border-radius: 50%;
    background: #082719;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: contragiro 8s linear infinite;
}

.percentage {
    font-size: 49px;
    font-weight: 900;
    color: white;
    animation: brillo 2s ease-in-out infinite;
}

@keyframes girar {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes contragiro {
    from { transform: rotate(0deg); }
    to { transform: rotate(-360deg); }
}

@keyframes brillo {
    0%, 100% { text-shadow: 0 0 5px #E7BD50; }
    50% { text-shadow: 0 0 22px #E7BD50; }
}

/* CATEGORIA */

.category {
    display: inline-block;
    background: linear-gradient(90deg, #E3B53C, #F5D66A);
    color: #102719;
    padding: 11px 35px;
    border-radius: 35px;
    font-size: 23px;
    font-weight: 900;
    text-align: center;
    margin: 10px auto;
}

/* INTERVALOS */

.interval-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 9px 0;
}

.interval-number {
    width: 125px;
    text-align: center;
    padding: 12px 5px;
    border-radius: 10px;
    font-weight: 900;
    color: #071B10;
}

.interval-name {
    flex: 1;
    padding: 12px 9px;
    border-radius: 10px;
    font-weight: 900;
    background: #103B24;
    color: white;
}

.green1 { background: #078D43; }
.green2 { background: #35BD29; }
.yellow { background: #EFC23B; }
.red { background: #E63333; }

@media (max-width: 700px) {
    .gauge {
        width: 170px;
        height: 170px;
    }
    .gauge-inner {
        width: 138px;
        height: 138px;
    }
    .percentage {
        font-size: 39px;
    }
    .interval-number {
        width: 105px;
        font-size: 12px;
    }
    .interval-name {
        font-size: 12px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# ARCHIVO DE REFERENCIA
# ==========================================

RUTA_REFERENCIA = "rostros_referencia.png"


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.markdown("""
<h1 style="color:#E7BD50 !important; font-size:27px;">
🌿 AMAZON FACE AI
</h1>
<p style="color:white;">Inteligencia artificial amazónica</p>
<hr style="border-color:#B9953B;">
""", unsafe_allow_html=True)

pagina = st.sidebar.radio(
    "MENÚ PRINCIPAL",
    [
        "Inicio",
        "Análisis facial",
        "Base de referencias",
        "Resultados",
        "Modelo matemático",
        "Acerca del proyecto"
    ]
)


# ==========================================
# FUNCION DE INTERVALOS
# ==========================================

def mostrar_intervalos():

    st.markdown("""
    <div class="interval-row">
        <div class="interval-number green1">
            90 – 100%
        </div>
        <div class="interval-name">
            MUY PARECIDO
        </div>
    </div>

    <div class="interval-row">
        <div class="interval-number green2">
            75 – 89%
        </div>
        <div class="interval-name">
            PARECIDO
        </div>
    </div>

    <div class="interval-row">
        <div class="interval-number yellow">
            50 – 74%
        </div>
        <div class="interval-name">
            SIMILITUD MODERADA
        </div>
    </div>

    <div class="interval-row">
        <div class="interval-number red">
            0 – 49%
        </div>
        <div class="interval-name">
            BAJA SIMILITUD
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# INICIO
# ==========================================

if pagina == "Inicio":

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("""
        <div class="hero">
            <h1>AMAZON FACE AI</h1>
            <h3>Geometría facial e inteligencia artificial</h3>
            <hr style="border-color:#D2AC45;">
            <p><b>Tecnología al servicio de nuestra Amazonía</b></p>
            <p>
            Plataforma experimental para el análisis
            de características geométricas faciales
            y su comparación con imágenes de referencia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if os.path.exists(RUTA_REFERENCIA):
            st.image(
                RUTA_REFERENCIA,
                use_container_width=True
            )
        else:
            st.info("Imagen de referencia pendiente de cargar.")

    st.markdown("## COMIENZA TU ANÁLISIS")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📁 Subir fotografía")

        archivo = st.file_uploader(
            "Selecciona una fotografía",
            type=["jpg", "jpeg", "png"]
        )

        if archivo:
            imagen = Image.open(archivo).convert("RGB")
            st.image(imagen, caption="Fotografía seleccionada",
                     use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📷 Activar cámara")

        foto = st.camera_input("Capturar fotografía")

        if foto:
            imagen = Image.open(foto).convert("RGB")
            st.image(imagen, caption="Fotografía capturada",
                     use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # RESULTADO VISUAL DE EJEMPLO

    st.markdown("""
    <div class="result-card">
        <div class="result-title">
            RESULTADO DE COMPARACIÓN
        </div>

        <div class="gauge">
            <div class="gauge-inner">
                <div class="percentage">85%</div>
                <div style="color:#E7BD50;font-weight:bold;">
                    SIMILITUD
                </div>
            </div>
        </div>

        <div style="text-align:center;">
            <div class="category">PARECIDO</div>
        </div>

        <p style="text-align:center;">
            Ejemplo ilustrativo de presentación del resultado
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## CLASIFICACIÓN DE RESULTADOS")

    mostrar_intervalos()


# ==========================================
# ANALISIS FACIAL
# ==========================================

elif pagina == "Análisis facial":

    st.title("🔎 ANÁLISIS FACIAL")

    st.write("""
    En esta sección se implementará la detección
    de puntos faciales y el análisis de características
    geométricas.
    """)

    st.info(
        "La comparación automática se incorporará "
        "cuando se complete el modelo."
    )


# ==========================================
# BASE DE REFERENCIAS
# ==========================================

elif pagina == "Base de referencias":

    st.title("📂 BASE DE FOTOGRAFÍAS DE REFERENCIA")

    if os.path.exists(RUTA_REFERENCIA):

        imagen = Image.open(RUTA_REFERENCIA)

        st.image(
            imagen,
            caption="Base de imágenes de prueba",
            use_container_width=True
        )

        st.success("Imagen de referencia cargada correctamente.")

    else:
        st.error("No se encontró rostros_referencia.png")


# ==========================================
# RESULTADOS
# ==========================================

elif pagina == "Resultados":

    st.title("📊 RESULTADOS DE COMPARACIÓN")

    st.markdown("""
    <div class="result-card">
        <div class="result-title">RESULTADO DE EJEMPLO</div>

        <div class="gauge">
            <div class="gauge-inner">
                <div class="percentage">85%</div>
                <div style="color:#E7BD50;font-weight:bold;">
                    SIMILITUD
                </div>
            </div>
        </div>

        <div style="text-align:center;">
            <div class="category">PARECIDO</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## INTERVALOS DE CLASIFICACIÓN")

    mostrar_intervalos()

    st.caption(
        "El 85% es un valor demostrativo. "
        "No representa todavía una medición real del modelo."
    )


# ==========================================
# MODELO MATEMATICO
# ==========================================

elif pagina == "Modelo matemático":

    st.title("📐 MODELO MATEMÁTICO")

    st.write("""
    El proyecto utilizará características geométricas
    y distancias normalizadas para realizar comparaciones
    experimentales entre imágenes faciales.
    """)


# ==========================================
# ACERCA DEL PROYECTO
# ==========================================

elif pagina == "Acerca del proyecto":

    st.title("🌿 ACERCA DE AMAZON FACE AI")

    st.write("""
    AMAZON FACE AI es una aplicación experimental
    desarrollada en Python para estudiar características
    geométricas faciales y compararlas con imágenes
    de referencia documentadas.

    La aplicación permite seleccionar fotografías
    o utilizar una cámara para realizar pruebas
    de análisis mediante visión computacional.
    """)

    st.warning(
        "La similitud geométrica no determina la identidad "
        "ni la pertenencia étnica de una persona."
    )


