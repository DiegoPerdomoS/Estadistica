import matplotlib.pyplot as plt
import numpy as np

def calcular_oro_necesario(
    smeechs_propios=0,      # Número de Smeechs que ya posees
    smeechs_tomados=0,      # X: Número de Smeechs ya tomados por otros jugadores
    otros_costo3_tomados=0, # Y: Número de otros campeones de costo 3 tomados por otros jugadores
    costo_reroll=2,         # Costo en oro de cada reroll
    costo_campeon=3,        # Costo en oro del campeón (3 en este caso)
    prob_costo3=0.4,        # Probabilidad de obtener un campeón de costo 3 (40%)
    total_tipos_costo3=13,  # Número total de tipos de campeones diferentes de costo 3
    copias_por_tipo=18,     # Número de copias por campeón de costo 3
    slots_por_reroll=5,     # Número de campeones mostrados en cada reroll
    copias_para_3estrellas=9 # Número de copias necesarias para conseguir un campeón 3 estrellas
):
    """
    Calcula el oro esperado necesario para conseguir un campeón específico de costo 3 a 3 estrellas.
    
    Args:
        smeechs_propios: Número de Smeechs que ya posees
        smeechs_tomados: Número de Smeechs ya tomados por otros jugadores
        otros_costo3_tomados: Número de otros campeones de costo 3 tomados por otros jugadores
        costo_reroll: Costo en oro de cada reroll
        costo_campeon: Costo en oro del campeón
        prob_costo3: Probabilidad de obtener un campeón de costo 3
        total_tipos_costo3: Número total de tipos de campeones diferentes de costo 3
        copias_por_tipo: Número de copias por campeón de costo 3
        slots_por_reroll: Número de campeones mostrados en cada reroll
        copias_para_3estrellas: Número de copias necesarias para conseguir un campeón 3 estrellas
        
    Returns:
        dict: Un diccionario con la información del oro necesario y probabilidades
    """
    # Verificar que los valores tengan sentido
    total_smeechs_usados = smeechs_propios + smeechs_tomados
    smeechs_disponibles = copias_por_tipo - total_smeechs_usados
    
    # Calcular cuántos Smeechs adicionales necesitamos para llegar a 3 estrellas
    smeechs_adicionales_necesarios = copias_para_3estrellas - smeechs_propios
    
    if smeechs_adicionales_necesarios <= 0:
        return {
            "mensaje": "¡Ya tienes suficientes Smeechs para 3 estrellas!",
            "oro_total_esperado": 0
        }
    
    if smeechs_disponibles < smeechs_adicionales_necesarios:
        return {
            "error": "No hay suficientes Smeechs disponibles en el pool para conseguir 3 estrellas",
            "smeechs_disponibles": smeechs_disponibles,
            "smeechs_adicionales_necesarios": smeechs_adicionales_necesarios
        }
    
    # Total de campeones de costo 3 en el pool
    total_costo3_pool = total_tipos_costo3 * copias_por_tipo
    
    # Total de campeones de costo 3 disponibles actualmente
    # Restamos los propios, los tomados por otros y los de otros tipos tomados
    total_costo3_disponibles = total_costo3_pool - total_smeechs_usados - otros_costo3_tomados
    
    # Probabilidad inicial de obtener un Smeech específico en un slot
    prob_smeech_por_slot = prob_costo3 * (smeechs_disponibles / total_costo3_disponibles)
    
    # Probabilidad de NO obtener un Smeech en un slot
    prob_no_smeech_por_slot = 1 - prob_smeech_por_slot
    
    # Probabilidad de NO obtener un Smeech en ninguno de los slots de un reroll
    prob_no_smeech_por_reroll = prob_no_smeech_por_slot ** slots_por_reroll
    
    # Probabilidad de obtener al menos un Smeech en un reroll
    prob_al_menos_un_smeech = 1 - prob_no_smeech_por_reroll
    
    # Simulación de la compra de Smeechs uno por uno
    total_rerolls = 0
    total_smeechs_comprados = 0
    smeechs_restantes = smeechs_disponibles
    
    for i in range(smeechs_adicionales_necesarios):
        # Actualizar probabilidad para este Smeech
        prob_smeech_actual = prob_costo3 * (smeechs_restantes / total_costo3_disponibles)
        prob_no_smeech_actual = 1 - prob_smeech_actual
        prob_no_smeech_reroll = prob_no_smeech_actual ** slots_por_reroll
        prob_al_menos_un_smeech_actual = 1 - prob_no_smeech_reroll
        
        # Rerolls esperados para este Smeech
        rerolls_para_este_smeech = 1 / prob_al_menos_un_smeech_actual
        
        total_rerolls += rerolls_para_este_smeech
        total_smeechs_comprados += 1
        
        # Actualizar contadores
        smeechs_restantes -= 1
        total_costo3_disponibles -= 1
    
    # Calcular oro total necesario
    oro_para_rerolls = total_rerolls * costo_reroll
    oro_para_comprar_smeechs = smeechs_adicionales_necesarios * costo_campeon
    oro_total = oro_para_rerolls + oro_para_comprar_smeechs
    
    return {
        "oro_total_esperado": round(oro_total, 2),
        "oro_para_rerolls": round(oro_para_rerolls, 2),
        "oro_para_comprar_smeechs": oro_para_comprar_smeechs,
        "rerolls_esperados": round(total_rerolls, 2),
        "smeechs_propios": smeechs_propios,
        "smeechs_adicionales_necesarios": smeechs_adicionales_necesarios,
        "probabilidad_smeech_por_slot": f"{prob_smeech_por_slot:.4f} ({prob_smeech_por_slot*100:.2f}%)",
        "probabilidad_smeech_por_reroll": f"{prob_al_menos_un_smeech:.4f} ({prob_al_menos_un_smeech*100:.2f}%)"
    }


def visualize_gold_needed():
    smeechs_propios_range = range(0, 9)
    resultados = []
    
    for smeechs in smeechs_propios_range:
        resultado = calcular_oro_necesario(smeechs_propios=smeechs)
        if "oro_total_esperado" in resultado:
            resultados.append(resultado["oro_total_esperado"])
        else:
            resultados.append(0)
    
    plt.figure(figsize=(10, 6))
    plt.plot(smeechs_propios_range, resultados, marker='o')
    plt.title('Oro Necesario vs. Smeechs Propios')
    plt.xlabel('Número de Smeechs que ya posees')
    plt.ylabel('Oro Total Esperado')
    plt.grid(True)
    plt.show()

def analisis_sensibilidad():
    parametros = {
        "smeechs_tomados": range(0, 6),
        "otros_costo3_tomados": range(0, 100, 10),
    }
    
    resultados = {}
    
    for param, valores in parametros.items():
        resultados[param] = []
        for valor in valores:
            kwargs = {param: valor}
            resultado = calcular_oro_necesario(**kwargs)
            if "oro_total_esperado" in resultado:
                resultados[param].append((valor, resultado["oro_total_esperado"]))
    
    # Visualize results
    for param, datos in resultados.items():
        x, y = zip(*datos)
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, marker='o')
        plt.title(f'Sensibilidad al parámetro: {param}')
        plt.xlabel(f'Valor de {param}')
        plt.ylabel('Oro Total Esperado')
        plt.grid(True)
        plt.show()

# Ejemplo de uso
resultado = calcular_oro_necesario(
    smeechs_propios=4,        # Ya tienes 3 Smeechs (necesitas 6 más para 3 estrellas)
    smeechs_tomados=0,        # 2 Smeechs ya tomados por otros jugadores
    otros_costo3_tomados=50,  # 30 otros campeones de costo 3 tomados
)

print(resultado)

analisis_sensibilidad()

visualize_gold_needed()