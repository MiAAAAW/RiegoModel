import streamlit as st
from streamlit_player import st_player

st.set_page_config(
    page_title='HIDROXYAPU',
    page_icon=':droplet:'
)

import base64
import streamlit as st
import base64

with open("logohy1.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")

    st.sidebar.markdown(
        f"""
        <div style="display:table;margin-top:-5%;margin-left:20%;">
            <img src="data:image/png;base64,{data}" width="100" height="150">
        </div>
        """,
        unsafe_allow_html=True,
    )




# Función para agregar una imagen de fondo
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/webp;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Llamar a la función con la imagen `1.webp`
add_bg_from_local('4.webp')

# Título e Introducción del Proyecto
st.title("HIDROXYAPU 🌾💧")
st.subheader("Introducción")
st.subheader("Solución Inteligente para la Predicción de Requerimientos de Riego")

# with st.sidebar:
#     st_player('https://youtu.be/LVbkPZeLh6U')

st.markdown("""
Este proyecto innovador está diseñado para predecir las necesidades de riego (IR) para diversos cultivos en la región. 
Utilizando modelos avanzados de inteligencia artificial como **Light Gradient Boosting Machines (LGBM)** y **Redes Neuronales Artificiales (ANN)**, 
**HidroxyApu** proporciona predicciones precisas de la evapotranspiración (ET) basadas en vastos conjuntos de datos. 
Estas predicciones se utilizan para calcular el IR, expresado en *milímetros de agua por unidad de área al día*.

Para comenzar, ingresa los datos meteorológicos actuales, selecciona el tipo de cultivo y su etapa de crecimiento, 
y elige el sistema de riego que utilizas. Sigue estos pasos:
""")

# Lista de combinaciones de factores meteorológicos
st.subheader("🔄 Factores Meteorológicos Disponibles")
st.write("Elige entre las siguientes combinaciones de factores meteorológicos:")
st.markdown("""
1. **Temperatura Media (C), Temperatura Máxima (C) y Temperatura Mínima (C):**
   - *Precisión Moderada*
   
2. **Temperatura Media (C), Temperatura Máxima (C), Temperatura Mínima (C) y Velocidad del Viento (m/s):**
   - *Alta Precisión*
   
3. **Temperatura Media (C), Temperatura Máxima (C), Temperatura Mínima (C), Velocidad del Viento (m/s), Humedad Relativa (%) y Presión Superficial (kPa):**
   - *Muy Alta Precisión*

*Nota: Si eliges una combinación diferente, se producirá un error. El orden de los factores no es importante.*
""")

# Lista de tipos de cultivos
st.subheader("🌱 Tipos de Cultivos Disponibles")
st.write("Selecciona entre los siguientes tipos de cultivos:")
st.markdown("""
1. **Garbanzos / Gramo**
2. **Algodón**
3. **Maíz de Campo**
4. **Soja**
5. **Maíz Dulce**
6. **Trigo de Invierno**
""")

# Lista de etapas de crecimiento
st.subheader("🌿 Etapas de Crecimiento")
st.write("Selecciona la etapa de crecimiento de tu cultivo:")
st.markdown("""
1. **Inicial**
2. **Media Estación**
3. **Final de Estación**
""")

st.subheader("🚰 Sistemas de Riego y Precipitación")
st.write("Elige entre los siguientes sistemas de riego:")
st.markdown("""
1. **Goteo**
2. **Aspersión**
3. **Superficie**
""")
st.write("Luego, ingresa la precipitación pronosticada para el día de hoy.")

# Instrucciones para ingresar datos
st.subheader("📝 Instrucciones para Ingresar Datos")
st.write("""
Una vez seleccionada toda la información relevante, ingresa los valores actuales para los factores meteorológicos elegidos y presiona **¡CALCULAR!**
""")

# Valores Kc e información sobre los cultivos
st.subheader("🔍 Información Clave")
st.write("""
Los valores Kc que se utilizan para ajustar la ET predicha por los modelos para los cultivos seleccionados son valores estándar 
proporcionados por la FAO. Puedes consultarlos en el siguiente enlace:
""")
st.markdown("[Valores de Coeficientes de Cultivo (Kc) de la FAO](https://openknowledge.fao.org/server/api/core/bitstreams/8802ddc9-86b6-4f13-96b7-4871dd3aee65/content)")

st.write("Las opciones de cultivos disponibles están basadas en los tipos más comúnmente cultivados en la región.")

# Mensaje de agradecimiento
st.subheader("🙏 ¡Gracias por Utilizar HidroxyApu!")
st.write("Esperamos que esta herramienta te ayude a optimizar el uso del agua en tus cultivos.")
