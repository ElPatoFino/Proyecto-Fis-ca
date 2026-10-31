import math

# Constante gravitatoria estándar (más aproximado a lo real)
G_ESTANDARD = 9.80665  # m/s²


def velocidad_inicial_resorte(k, x, m):
    """
    Calcula la velocidad inicial v0 de un proyectil impulsado por un resorte.
    
    Se parte del principio de conservación de la energía:
    Energía potencial elástica = Energía cinética
    (1/2) * k * x^2 = (1/2) * m * v0^2
    
    Despejando:
    v0 = sqrt((k * x^2) / m)
    
    Args:
        k (float): Constante elástica del resorte [N/m]
        x (float): Compresión del resorte [m]
        m (float): Masa del proyectil [kg]
    
    Returns:
        float: Velocidad inicial [m/s]
    
    Raises:
        ValueError: Si algún parámetro no cumple con las condiciones físicas.
    """
    if k <= 0:
        raise ValueError("La constante elástica k debe ser mayor a 0 (N/m)")
    if x < 0:
        raise ValueError("La compresión x no puede ser negativa (m)")
    if m <= 0:
        raise ValueError("La masa m debe ser mayor a 0 (kg)")
    
    # Cálculo de la velocidad inicial desde la energía del resorte
    v0 = math.sqrt((k * x**2) / m)
    return v0


def fuerza_resorte(k, x):
    """
    Calcula la fuerza ejercida por un resorte según la Ley de Hooke.
    F = k * x (fuerza máxima en compresión máxima)
    
    Args:
        k (float): Constante elástica del resorte [N/m]
        x (float): Compresión del resorte [m]
    
    Returns:
        float: Fuerza elástica [N]
    
    Raises:
        ValueError: Si algún parámetro no cumple con las condiciones físicas.
    """
    if k <= 0:
        raise ValueError("La constante elástica k debe ser mayor a 0 (N/m)")
    if x < 0:
        raise ValueError("La compresión x no puede ser negativa (m)")
    
    fuerza = k * x
    return fuerza


def energia_potencial_elastica(k, x):
    """
    Calcula la energía potencial elástica almacenada en un resorte comprimido.
    E = (1/2) * k * x^2
    
    Args:
        k (float): Constante elástica del resorte [N/m]
        x (float): Compresión del resorte [m]
    
    Returns:
        float: Energía potencial elástica [J]
    """
    if k <= 0:
        raise ValueError("La constante elástica k debe ser mayor a 0 (N/m)")
    if x < 0:
        raise ValueError("La compresión x no puede ser negativa (m)")
    
    energia = 0.5 * k * x**2
    return energia


def alcance_horizontal(v0, theta_grados, g=G_ESTANDARD):
    """
    Calcula el alcance horizontal teórico de un proyectil (sin resistencia del aire).
    
    Fórmula:
    R = (v0^2 * sin(2*theta)) / g
    
    El alcance máximo teórico se obtiene con theta = 45°, donde sin(90°)=1.
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Alcance horizontal [m]
    
    Raises:
        ValueError: Si algún parámetro no cumple con las condiciones físicas.
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    # Convertir ángulo a radianes y calcular sin(2*theta)
    theta_rad = math.radians(theta_grados)
    alcance = (v0**2 * math.sin(2 * theta_rad)) / g
    
    return alcance


def alcance_maximo(v0, g=G_ESTANDARD):
    """
    Calcula el alcance horizontal máximo teórico (a 45°).
    R_max = v0^2 / g
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Alcance máximo [m]
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    r_max = (v0**2) / g
    return r_max


def altura_maxima(v0, theta_grados, g=G_ESTANDARD):
    """
    Calcula la altura máxima alcanzada por el proyectil.
    H_max = (v0^2 * sin^2(theta)) / (2*g)
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Altura máxima [m]
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    theta_rad = math.radians(theta_grados)
    h_max = (v0**2 * (math.sin(theta_rad))**2) / (2 * g)
    return h_max


def tiempo_vuelo(v0, theta_grados, g=G_ESTANDARD):
    """
    Calcula el tiempo total de vuelo del proyectil.
    T = (2 * v0 * sin(theta)) / g
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Tiempo de vuelo [s]
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    theta_rad = math.radians(theta_grados)
    t_vuelo = (2 * v0 * math.sin(theta_rad)) / g
    return t_vuelo


def trayectoria(v0, theta_grados, g=G_ESTANDARD, num_puntos=200):
    """
    Genera los puntos de la trayectoria parabólica de un proyectil.
    
    Ecuaciones del movimiento:
    x(t) = v0 * cos(theta) * t
    y(t) = v0 * sin(theta) * t - (1/2) * g * t^2
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
        num_puntos (int): Cantidad de puntos a generar
    
    Returns:
        tuple: (xs, ys) - Listas con las coordenadas de la trayectoria [m]
    
    Raises:
        ValueError: Si algún parámetro no cumple con las condiciones físicas.
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    if num_puntos < 2:
        raise ValueError("num_puntos debe ser al menos 2")
    
    t_vuelo = tiempo_vuelo(v0, theta_grados, g)
    
    if t_vuelo <= 0:
        return [0.0], [0.0]
    
    theta_rad = math.radians(theta_grados)
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)
    
    xs = []
    ys = []
    paso = t_vuelo / (num_puntos - 1)
    
    for i in range(num_puntos):
        t = paso * i
        xs.append(vx * t)
        ys.append(vy * t - 0.5 * g * t**2)
    
    if abs(ys[-1]) < 1e-9:
        ys[-1] = 0.0
    
    return xs, ys


def trayectoria_desde_resorte(k, x, m, theta_grados, g=G_ESTANDARD, num_puntos=200):
    """
    Genera la trayectoria parabólica a partir de las características del resorte.
    
    Args:
        k (float): Constante elástica del resorte [N/m]
        x (float): Compresión del resorte [m]
        m (float): Masa del proyectil [kg]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
        num_puntos (int): Cantidad de puntos a generar
    
    Returns:
        tuple: (xs, ys) - Listas con las coordenadas de la trayectoria [m]
    """
    v0 = velocidad_inicial_resorte(k, x, m)
    return trayectoria(v0, theta_grados, g, num_puntos)


def alcance_desde_resorte(k, x, m, theta_grados, g=G_ESTANDARD):
    """
    Calcula el alcance horizontal directamente desde las características del resorte.
    
    Combina ambos cálculos:
    1. v0 = sqrt((k*x^2)/m)
    2. R  = (v0^2 * sin(2*theta)) / g
    
    Args:
        k (float): Constante elástica del resorte [N/m]
        x (float): Compresión del resorte [m]
        m (float): Masa del proyectil [kg]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Alcance horizontal [m]
    """
    # Calcular velocidad inicial desde el resorte
    v0 = velocidad_inicial_resorte(k, x, m)
    
    # Calcular alcance horizontal con ese ángulo
    alcance = alcance_horizontal(v0, theta_grados, g)
    
    return alcance


def v0_necesario(alcance_deseado, theta_grados, g=G_ESTANDARD):
    """
    Calcula la velocidad inicial necesaria para alcanzar un alcance deseado.
    R = (v0^2 * sin(2*theta)) / g  =>  v0 = sqrt((R * g) / sin(2*theta))
    
    Args:
        alcance_deseado (float): Alcance horizontal deseado [m]
        theta_grados (float): Ángulo de lanzamiento [grados]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        float: Velocidad inicial necesaria [m/s]
    
    Raises:
        ValueError: Si es físicamente imposible o parámetros inválidos
    """
    if alcance_deseado < 0:
        raise ValueError("El alcance deseado no puede ser negativo (m)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    theta_rad = math.radians(theta_grados)
    sin2theta = math.sin(2 * theta_rad)
    
    if sin2theta <= 0:
        raise ValueError("Ángulo inválido. El alcance será cero o negativo con ese ángulo.")
    
    # Verificar si es físicamente posible (comparando con alcance máximo a 45°)
    # Para este ángulo en particular
    v0_cuadrado = (alcance_deseado * g) / sin2theta
    
    if v0_cuadrado < 0:
        raise ValueError("No es físicamente posible alcanzar ese alcance con ese ángulo.")
    
    v0 = math.sqrt(v0_cuadrado)
    return v0


def angulos_para_alcance(v0, alcance_deseado, g=G_ESTANDARD):
    """
    Calcula los ángulos posibles para alcanzar un alcance deseado con velocidad inicial dada.
    sin(2*theta) = (R * g) / v0^2
    
    Para un valor dado de sin(x)=y hay dos soluciones: x1 = arcsin(y), x2 = 180° - arcsin(y)
    Por lo tanto: 2*theta = x => theta1 = x/2, theta2 = (180°-x)/2 = 90° - theta1
    
    Args:
        v0 (float): Velocidad inicial [m/s]
        alcance_deseado (float): Alcance horizontal deseado [m]
        g (float): Aceleración gravitatoria [m/s²] (por defecto 9.80665)
    
    Returns:
        tuple: (theta1_grados, theta2_grados) - Dos ángulos posibles
              Retorna None si no es físicamente posible
    """
    if v0 < 0:
        raise ValueError("La velocidad inicial v0 no puede ser negativa (m/s)")
    if alcance_deseado < 0:
        raise ValueError("El alcance deseado no puede ser negativo (m)")
    if g <= 0:
        raise ValueError("La aceleración gravitatoria g debe ser mayor a 0 (m/s²)")
    
    r_max = alcance_maximo(v0, g)
    
    # Verificar si es físicamente posible
    if alcance_deseado > r_max + 1e-9:  # Pequeña tolerancia numérica
        return None
    
    if alcance_deseado == 0:
        return (0.0, 0.0)
    
    sin2theta = (alcance_deseado * g) / (v0**2)
    
    # Asegurar que esté en rango válido
    if sin2theta > 1.0:
        sin2theta = 1.0
    if sin2theta < -1.0:
        return None
    
    # Calcular 2*theta
    dos_theta = math.asin(sin2theta)
    dos_theta2 = math.pi - dos_theta  # 180° - dos_theta
    
    theta1 = math.degrees(dos_theta) / 2
    theta2 = math.degrees(dos_theta2) / 2
    
    return (theta1, theta2)


def k_necesario(v0_deseada, x, m):
    """
    Calcula la constante elástica k necesaria para obtener una velocidad inicial deseada.
    Desde (1/2)*k*x^2 = (1/2)*m*v0^2 => k = (m * v0^2) / x^2
    
    Args:
        v0_deseada (float): Velocidad inicial deseada [m/s]
        x (float): Compresión del resorte [m]
        m (float): Masa del proyectil [kg]
    
    Returns:
        float: Constante elástica necesaria [N/m]
    """
    if v0_deseada < 0:
        raise ValueError("La velocidad inicial deseada no puede ser negativa (m/s)")
    if x <= 0:
        raise ValueError("La compresión x debe ser mayor a 0 (m)")
    if m <= 0:
        raise ValueError("La masa m debe ser mayor a 0 (kg)")
    
    k = (m * v0_deseada**2) / (x**2)
    return k


def x_necesario(v0_deseada, k, m):
    """
    Calcula la compresión x necesaria para obtener una velocidad inicial deseada.
    Desde (1/2)*k*x^2 = (1/2)*m*v0^2 => x = v0 * sqrt(m/k)
    
    Args:
        v0_deseada (float): Velocidad inicial deseada [m/s]
        k (float): Constante elástica del resorte [N/m]
        m (float): Masa del proyectil [kg]
    
    Returns:
        float: Compresión necesaria [m]
    """
    if v0_deseada < 0:
        raise ValueError("La velocidad inicial deseada no puede ser negativa (m/s)")
    if k <= 0:
        raise ValueError("La constante elástica k debe ser mayor a 0 (N/m)")
    if m <= 0:
        raise ValueError("La masa m debe ser mayor a 0 (kg)")
    
    x = v0_deseada * math.sqrt(m / k)
    return x


def k_desde_fuerza(f, x):
    """
    Calcula la constante elástica k desde la fuerza aplicada y la deformación.
    Según la Ley de Hooke: F = k * x => k = F / x
    
    Args:
        f (float): Fuerza aplicada [N]
        x (float): Deformación/compresión del resorte [m]
    
    Returns:
        float: Constante elástica k [N/m]
    
    Raises:
        ValueError: Si algún parámetro no cumple con las condiciones físicas.
    """
    if f < 0:
        raise ValueError("La fuerza F no puede ser negativa (N)")
    if x <= 0:
        raise ValueError("La deformación x debe ser mayor a 0 (m)")
    
    k = f / x
    return k
