def calcular_promedio_temperaturas(datos_temperaturas):
    promedios_ciudades = {}
    for ciudad, temperaturas_semanales in datos_temperaturas.items():
        temperaturas_totales = []
        for temperaturas_semanales in temperaturas_semanales:
            temperaturas_totales.extend(temperaturas_semanales)
        promedio = sum(temperaturas_totales) / len(temperaturas_totales)
        promedios_ciudades[ciudad] = promedio
    return promedios_ciudades


datos_temperaturas = {
    "Quito": [[12, 14, 15, 13, 16, 17, 15], [13, 15, 16, 14, 17, 18, 16]],


}

promedios = calcular_promedio_temperaturas(datos_temperaturas)
for ciudad, promedio in promedios.items():
    print(f"Temperatura promedio en {ciudad}: {promedio:.2f} grados")