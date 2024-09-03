import numpy as np
import streamlit as st
from helper import possible_weather_factor_choices, crop_type_and_stage_to_kc, irrigation_type_to_efficiency

st.set_page_config(
    page_title='HIDROXYAPU',
    page_icon=':droplet:',
    layout='wide'
)

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



# Estilo CSS para mejores visuales
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)


def set_ok_button_true():
    st.session_state.ok_button = True


# Carga el mejor modelo configurado para una combinación particular de factores climáticos
def best_model_for_factors_comb(idx):
    from helper import factors_comb_mapped_to_model_and_type
    model_type, model_path = factors_comb_mapped_to_model_and_type[idx]
    if model_type == 'lgbm':
        import joblib
        model = joblib.load(model_path)
    else:
        from tensorflow.keras.models import load_model
        model = load_model(model_path)
    return model_type, model


# ETc es la evapotranspiración ajustada para cultivos.
# Calcula el ETc usando la evapotranspiración predicha por el modelo, el tipo de cultivo seleccionado y la etapa de crecimiento.
# Kc es un factor utilizado para ajustar la evapotranspiración predicha para un cultivo específico, teniendo en cuenta su etapa de crecimiento también.
def calculating_ETc(crop_choice, growth_stage, ETo):
    Kc = crop_type_and_stage_to_kc[crop_choice][growth_stage]
    return ETo * Kc


st.title('Requerimientos Hídricos del Cultivo 🌱')

col1, buff, col2 = st.columns([1, 0.1, 1])

with col1:
    st.subheader("🌾 **Selecciona Tu Cultivo y Etapa de Crecimiento**")
    crop_types = sorted(list(crop_type_and_stage_to_kc.keys()))
    crop_choice = st.selectbox('Tipo de Cultivo:', crop_types, help="Selecciona el tipo de cultivo que te interesa.")

    growth_stages = ['Inicial', 'Media Estación', 'Final de Estación']
    growth_stage = st.selectbox('Etapa de Crecimiento del Cultivo:', growth_stages,
                                help="Elige la etapa de crecimiento actual de tu cultivo.")

    st.divider()

    st.subheader("🚿 **Requisitos de Cálculo de Riego**")
    irrigation_types = ['Goteo', 'Aspersión', 'Superficie']
    irrigation_type = st.selectbox('Tipo de Riego:', irrigation_types,
                                help="Elige el tipo de riego que usas.")
    irrigation_efficiency = irrigation_type_to_efficiency[irrigation_type]

    estimated_precipitation = st.number_input('⛈️ Ingresa la lluvia estimada (mm/día):',
                                              help='La lluvia pronosticada para hoy en tu región.')
    if estimated_precipitation > 150:
        peff_percent = 0.6
    elif estimated_precipitation > 50:
        peff_percent = 0.75
    else:
        peff_percent = 0.9

with col2:
    st.subheader("☁️ **Selecciona Factores Climáticos**")
    weather_factors = ['Temperatura Media (C)', 'Temperatura Mínima (C)', 'Temperatura Máxima (C)', 'Velocidad del Viento (m/s)',
                       'Humedad Relativa (%)', 'Presión Superficial (kPa)']
    weather_factor_choices = st.multiselect('Factores Climáticos:', weather_factors,
                                            help="Elige los factores climáticos disponibles para hoy.")

    # Mantiene un seguimiento del estado del botón OK: si ha sido clicado o no.
    if 'ok_button' not in st.session_state:
        st.session_state.ok_button = False

    ok = st.button('OK', on_click=set_ok_button_true)
    if st.session_state.ok_button:
        if sorted(weather_factor_choices) not in possible_weather_factor_choices:
            st.error("🚫 ¡Por favor, elige una combinación válida de factores climáticos!")
        else:
            st.divider()

            model_inputs = []
            mean_temp = st.number_input("🌡️ Ingresa la Temperatura Media (C):", on_change=set_ok_button_true)
            model_inputs.append(mean_temp)

            max_temp = st.number_input("🌞 Ingresa la Temperatura Máxima (C):", on_change=set_ok_button_true)
            model_inputs.append(max_temp)

            min_temp = st.number_input("🌙 Ingresa la Temperatura Mínima (C):", on_change=set_ok_button_true)
            model_inputs.append(min_temp)

            if 'Velocidad del Viento (m/s)' in weather_factor_choices:
                wind_speed = st.number_input("🌬️ Ingresa la Velocidad del Viento (m/s):", on_change=set_ok_button_true)
                model_inputs.append(wind_speed)

            if 'Humedad Relativa (%)' in weather_factor_choices:
                relative_humidity = st.number_input("💧 Ingresa la Humedad Relativa (%):", on_change=set_ok_button_true)
                model_inputs.append(relative_humidity)

            if 'Presión Superficial (kPa)' in weather_factor_choices:
                surface_pressure = st.number_input("🌀 Ingresa la Presión Superficial (kPa):", on_change=set_ok_button_true)
                model_inputs.append(surface_pressure)

            calculate = st.button('CALCULAR')

            if calculate:
                st.divider()
                with st.spinner('Calculando 🔄'):
                    model_type, model = best_model_for_factors_comb(
                        possible_weather_factor_choices.index(sorted(weather_factor_choices))
                    )

                    # ETo es la evapotranspiración de referencia.
                    predicted_ETo = model.predict(np.array([model_inputs]))

                    # Algunos modelos devuelven un array 1D mientras que otros devuelven un array 2D. Por lo tanto, esta verificación es necesaria.
                    if len(predicted_ETo.shape) == 1:
                        predicted_ETo = predicted_ETo[0]
                    else:
                        predicted_ETo = predicted_ETo[0, 0]
                    ETc = calculating_ETc(crop_choice, growth_stage, predicted_ETo)

                    # El Requerimiento Hídrico del Cultivo (CWR) es el ETc en mm/día
                    crop_water_requirement = ETc

                    # La Precipitación Efectiva (Peff) es la cantidad de lluvia realmente disponible para el cultivo.
                    effective_precipitation = estimated_precipitation * peff_percent

                    # El Requerimiento Neto de Riego (NIR) es la cantidad de agua que necesita ser proporcionada a la planta a través del riego.
                    net_irrigation_requirement = crop_water_requirement - effective_precipitation

                    with st.expander('Valores Intermedios de Cálculo'):
                        st.write(f'**Evapotranspiración de Referencia:** {predicted_ETo:.2f} mm/día')
                        st.write(f'**Requerimiento Hídrico del Cultivo:** {ETc:.2f} mm/día')
                        st.write(f'**Precipitación Efectiva:** {effective_precipitation:.2f} mm/día')
                        st.write(f'**Requerimiento Neto de Riego:** {net_irrigation_requirement:.2f} mm/día')

                    # Si NIR < 0, entonces la planta obtendrá toda su agua de la precipitación y no necesitará ser regada. Por lo tanto, se realiza la verificación a continuación.
                    if net_irrigation_requirement > 0:

                        # Los sistemas de riego no son 100% eficientes y por lo tanto, el NIR se ajusta teniendo en cuenta
                        final_irrigation_amount = net_irrigation_requirement / irrigation_efficiency
                        st.success(f"✅ Necesitarás regar el cultivo con **{final_irrigation_amount:.2f} mm** "
                                   f"de agua por unidad de área del campo por día.")
                    else:
                        st.success(f"✅ Tu cultivo no necesita agua. ¡Estará adecuadamente regado por la lluvia!")
