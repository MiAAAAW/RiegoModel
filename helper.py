possible_weather_factor_choices = [sorted(['Temperatura Media (C)', 'Temperatura Máxima (C)', 'Temperatura Mínima (C)']),
                                   sorted(['Temperatura Media (C)', 'Temperatura Máxima (C)', 'Temperatura Mínima (C)',
                                           'Velocidad del Viento (m/s)']),
                                   sorted(['Temperatura Media (C)', 'Temperatura Máxima (C)', 'Temperatura Mínima (C)',
                                           'Velocidad del Viento (m/s)',
                                           'Humedad Relativa (%)', 'Presión Superficial (kPa)'])]

factors_comb_mapped_to_model_and_type = {
    0: ('lgbm', 'modelos_guardados/lgbm_temp.pkl'),
    1: ('nn', 'modelos_guardados/nn_ws.keras'),
    2: ('nn', 'modelos_guardados/nn_all.keras')
}

crop_type_and_stage_to_kc = {
    'Garbanzos / Gramo': {'Inicial': 0.4, 'Media Estación': 1.0, 'Final de Estación': 0.35},
    'Algodón': {'Inicial': 0.35, 'Media Estación': 1.15, 'Final de Estación': 0.5},
    'Maíz de Campo': {'Inicial': 0.3, 'Media Estación': 1.20, 'Final de Estación': 0.35},
    'Maíz Dulce': {'Inicial': 0.3, 'Media Estación': 1.15, 'Final de Estación': 0.3},
    'Soja': {'Inicial': 0.4, 'Media Estación': 1.15, 'Final de Estación': 0.5},
    'Trigo de Invierno': {'Inicial': 0.3, 'Media Estación': 1.15, 'Final de Estación': 0.4}
}

irrigation_type_to_efficiency = {
    'Goteo': 0.9,
    'Aspersión': 0.75,
    'Superficie': 0.6
}
