from pyDatalog import pyDatalog

# Inicializar PyDatalog
pyDatalog.clear()

# Crear términos (variables y relaciones)
pyDatalog.create_terms('puntaje, transaccion, riesgo_monto, riesgo_ubicacion, riesgo_metodo')
pyDatalog.create_terms('T, M, U, PAGO, R1, R2, R3, P, UF')
pyDatalog.create_terms('bloquear, revisar, aprobar')
pyDatalog.create_terms('umbral_fraude')

# Definir el umbral de fraude como un hecho
+umbral_fraude(0.7)

# Definir hechos (riesgos asociados)
+riesgo_monto('mayor_5000', 0.9)
+riesgo_monto('entre_2000_5000', 0.7)
+riesgo_monto('menor_2000', 0.3)

+riesgo_ubicacion('internacional', 0.8)
+riesgo_ubicacion('local', 0.2)

+riesgo_metodo('tarjeta_credito', 0.7)
+riesgo_metodo('transferencia', 0.5)
+riesgo_metodo('efectivo', 0.1)

# Definir la regla para calcular el puntaje de riesgo
puntaje(T, P) <= (transaccion(T, M, U, PAGO) &
                  riesgo_monto(M, R1) &
                  riesgo_ubicacion(U, R2) &
                  riesgo_metodo(PAGO, R3) &
                  (P == (R1 + R2 + R3) / 3))

# Definir reglas de decisión basadas en el puntaje
bloquear(T) <= (puntaje(T, P) & umbral_fraude(UF) & (P > UF))
revisar(T) <= (puntaje(T, P) & umbral_fraude(UF) & (P >= 0.5) & (P <= UF))
aprobar(T) <= (puntaje(T, P) & (P < 0.5))

# Mapeo de respuestas válidas
monto_dict = {"1": "mayor_5000", "2": "entre_2000_5000", "3": "menor_2000"}
ubicacion_dict = {"i": "internacional", "l": "local"}
metodo_dict = {"1": "tarjeta_credito", "2": "transferencia", "3": "efectivo"}

# Bucle para ingresar datos manualmente
while True:
    print("\n--- INGRESAR NUEVA TRANSACCIÓN ---")
    trans_id = input("ID de la transacción: ").strip()

    monto = input("Categoría de monto (1: mayor_5000, 2: entre_2000_5000, 3: menor_2000): ").strip()
    monto = monto_dict.get(monto, "menor_2000")  # Valor por defecto

    ubicacion = input("Ubicación (internacional (i), local (l)): ").strip().lower()
    ubicacion = ubicacion_dict.get(ubicacion, "local")  # Valor por defecto

    metodo = input("Método de pago (1: tarjeta_credito, 2: transferencia, 3: efectivo): ").strip()
    metodo = metodo_dict.get(metodo, "efectivo")  # Valor por defecto

    # Agregar la nueva transacción a la base de datos
    +transaccion(trans_id, monto, ubicacion, metodo)

    # Evaluar la transacción
    resultado_puntaje = puntaje(trans_id, P).ask()

    if not resultado_puntaje:  # Si la lista está vacía, no se encontró resultado
        print("❌ ERROR: No se pudo calcular el puntaje. Revisa los valores ingresados.")
        continue

    puntaje_valor = resultado_puntaje[0][0]  # Obtener el primer resultado
    print(f"✅ Puntaje de Riesgo: {puntaje_valor:.2f}")

    if bloquear(trans_id).ask():
        print("🔴 FRAUDE DETECTADO: Transacción bloqueada.")
    elif revisar(trans_id).ask():
        print("⚠️ Revisión manual requerida.")
    elif aprobar(trans_id).ask():
        print("✅ Transacción aprobada.")

    # Preguntar si desea ingresar otra transacción
    continuar = input("¿Deseas ingresar otra transacción? (s/n): ").strip().lower()
    if continuar != "s":
        break
