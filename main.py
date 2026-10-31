from fisica import velocidad_inicial_resorte, alcance_desde_resorte, G_ESTANDARD


def main():
    """
    Punto de entrada del programa.
    Calcula y muestra el alcance teórico de un proyectil impulsado por un resorte.
    """
    print("=" * 60)
    print("PROYECTIL IMPULSADO POR RESORTE - CÁLCULO TEÓRICO")
    print("=" * 60)
    
    # Parámetros del sistema (valores de ejemplo realistas)
    k = 200.0      # Constante elástica del resorte [N/m]
    x = 0.15       # Compresión del resorte [m]
    m = 0.2        # Masa del proyectil [kg]
    g = G_ESTANDARD  # Aceleración gravitatoria [m/s²]
    
    # Cálculo de la velocidad inicial
    v0 = velocidad_inicial_resorte(k, x, m)
    
    # Mostrar parámetros del sistema
    print("\nPARÁMETROS DEL SISTEMA:")
    print(f"  Constante elástica k = {k} N/m")
    print(f"  Compresión x         = {x} m")
    print(f"  Masa m               = {m} kg")
    print(f"  Gravedad g           = {g} m/s²")
    
    print("\n" + "-" * 60)
    print(f"VELOCIDAD INICIAL CALCULADA: v0 = {v0:.3f} m/s")
    print("-" * 60)
    
    # Probar con diferentes ángulos de lanzamiento
    angulos = [30, 45, 60]
    
    print("\nALCANCE HORIZONTAL PARA DISTINTOS ÁNGULOS (sin resistencia del aire):")
    print(f"{'Ángulo (°)':<15} {'Alcance (m)':<15}")
    print("-" * 30)
    
    for theta in angulos:
        alcance = alcance_desde_resorte(k, x, m, theta, g)
        print(f"{theta:<15} {alcance:<15.3f}")
    
    print("-" * 30)
    print("\nNota: El alcance máximo teórico ocurre a 45°.")
    print("=" * 60)


# Punto de entrada
if __name__ == "__main__":
    main()
