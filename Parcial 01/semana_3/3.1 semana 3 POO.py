class CalculadoraTemperaturas:
    def __init__(self, datos_temperaturas):
        self.datos = datos_temperaturas

    def calcular_promedios(self):
        promedios = {}
        for ciudad, semanas in self.datos.items():
            todas_temps = [temp for semana in semanas for temp in semana]
            promedios[ciudad] = sum(todas_temps) / len(todas_temps)
        return promedios

    def mostrar_resultados(self):
        for ciudad, promedio in self.calcular_promedios().items():
            print(f"Temperatura promedio en {ciudad}: {promedio:.2f}°C")


# Uso
datos_temperaturas =\
    {
    "Quito": [[12, 14, 15, 13, 16, 17, 15], [13, 15, 16, 14, 17, 18, 16]],
}

calculadora = CalculadoraTemperaturas(datos_temperaturas)
calculadora.mostrar_resultados()