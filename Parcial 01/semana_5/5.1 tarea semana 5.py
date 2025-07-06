"""
Sistema de Gestión de Estudiantes Universitarios
===============================================
Este programa permite gestionar información básica de estudiantes universitarios,
calcular sus promedios académicos y determinar su estado académico (aprobado/reprobado).



"""


def calcular_promedio(nota1, nota2, nota3):
    """
    Calcula el promedio de tres notas académicas.

    Args:
        nota1 (float): Primera nota del estudiante
        nota2 (float): Segunda nota del estudiante
        nota3 (float): Tercera nota del estudiante

    Returns:
        float: Promedio calculado de las tres notas
    """
    promedio_final = (nota1 + nota2 + nota3) / 3
    return promedio_final


def determinar_estado_academico(promedio):
    """
    Determina si el estudiante aprueba o reprueba según su promedio.

    Args:
        promedio (float): Promedio académico del estudiante

    Returns:
        bool: True si aprueba (>=7.0), False si reprueba (<7.0)
    """
    nota_minima_aprobacion = 7.0  # Nota mínima para aprobar
    return promedio >= nota_minima_aprobacion


def mostrar_informacion_estudiante(nombre_completo, edad_estudiante, carrera_universitaria,
                                   nota_primer_parcial, nota_segundo_parcial, nota_tercer_parcial):
    """
    Muestra toda la información del estudiante y calcula su estado académico.

    Args:
        nombre_completo (str): Nombre completo del estudiante
        edad_estudiante (int): Edad del estudiante en años
        carrera_universitaria (str): Carrera que estudia
        nota_primer_parcial (float): Nota del primer parcial
        nota_segundo_parcial (float): Nota del segundo parcial
        nota_tercer_parcial (float): Nota del tercer parcial
    """
    # Calcular el promedio usando la función definida anteriormente
    promedio_estudiante = calcular_promedio(nota_primer_parcial, nota_segundo_parcial, nota_tercer_parcial)

    # Determinar si aprueba o reprueba
    ha_aprobado = determinar_estado_academico(promedio_estudiante)

    # Mostrar información completa del estudiante
    print("=" * 50)
    print("INFORMACIÓN DEL ESTUDIANTE")
    print("=" * 50)
    print(f"Nombre: {nombre_completo}")
    print(f"Edad: {edad_estudiante} años")
    print(f"Carrera: {carrera_universitaria}")
    print("-" * 30)
    print("NOTAS ACADÉMICAS:")
    print(f"Primer Parcial: {nota_primer_parcial:.2f}")
    print(f"Segundo Parcial: {nota_segundo_parcial:.2f}")
    print(f"Tercer Parcial: {nota_tercer_parcial:.2f}")
    print(f"Promedio Final: {promedio_estudiante:.2f}")
    print("-" * 30)

    # Mostrar estado académico usando condicional
    if ha_aprobado:
        estado_texto = "APROBADO ✓"
        print(f"Estado Académico: {estado_texto}")
        print("¡Felicitaciones! Has aprobado el semestre.")
    else:
        estado_texto = "REPROBADO ✗"
        print(f"Estado Académico: {estado_texto}")
        print("Necesitas mejorar tus calificaciones.")

    print("=" * 50)


def main():
    """
    Función principal que ejecuta el programa de gestión de estudiantes.
    Solicita datos al usuario y procesa la información académica.
    """
    print("SISTEMA DE GESTIÓN DE ESTUDIANTES UNIVERSITARIOS")
    print("=" * 50)

    # Variables de diferentes tipos de datos
    # String: Información personal del estudiante
    nombre_completo = input("Ingresa el nombre completo del estudiante: ")
    carrera_universitaria = input("Ingresa la carrera universitaria: ")

    # Integer: Edad del estudiante
    try:
        edad_estudiante = int(input("Ingresa la edad del estudiante: "))
    except ValueError:
        print("Error: La edad debe ser un número entero.")
        return

    # Float: Notas académicas (pueden tener decimales)
    try:
        print("\n Ingresa las tres notas del semestre (0.0 - 10.0):")
        nota_primer_parcial = float(input("Nota del primer parcial: "))
        nota_segundo_parcial = float(input("Nota del segundo parcial: "))
        nota_tercer_parcial = float(input("Nota del tercer parcial: "))

        # Validar que las notas estén en el rango correcto
        notas_validas = True
        for nota in [nota_primer_parcial, nota_segundo_parcial, nota_tercer_parcial]:
            if nota < 0.0 or nota > 10.0:
                notas_validas = False
                break

        if not notas_validas:  # Boolean: Validación de notas
            print("Error: Las notas deben estar entre 0.0 y 10.0")
            return

    except ValueError:
        print("Error: Las notas deben ser números válidos.")
        return

    # Procesar y mostrar la información del estudiante
    print("\nProcesando información...")
    mostrar_informacion_estudiante(nombre_completo, edad_estudiante, carrera_universitaria,
                                   nota_primer_parcial, nota_segundo_parcial, nota_tercer_parcial)

    # Boolean adicional: Preguntar si desea procesar otro estudiante
    continuar_programa = input("\n¿Deseas registrar otro estudiante? (s/n): ").lower() == 's'

    if continuar_programa:
        print("\n" + "=" * 50)
        main()  # Llamada recursiva para procesar otro estudiante
    else:
        print("\n¡Gracias por usar el Sistema de Gestión de Estudiantes!")


# Punto de entrada del programa
if __name__ == "__main__":
    main()