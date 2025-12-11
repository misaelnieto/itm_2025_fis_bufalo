import random


def caza_del_tesoro():
    tablero = [["🌊", "🌊", "🌊"], ["🌊", "🌊", "🌊"], ["🌊", "🌊", "🌊"]]

    fila_tesoro = random.randint(0, 2)
    columna_tesoro = random.randint(0, 2)

    intentos = 0
    max_intentos = 5

    print("--- 🗺️ Caza del Tesoro 🗺️ ---")
    print("El tesoro está escondido en un tablero 3x3.")
    print(f"Tienes {max_intentos} intentos para encontrarlo.")

    def mostrar_tablero():
        print("\n  1 2 3 (Columnas)")
        print("  -----")
        for i, fila in enumerate(tablero):
            print(f"{i + 1}|{' '.join(fila)}")
        print("  -----\n")

    while intentos < max_intentos:
        mostrar_tablero()
        print(f"Intentos restantes: {max_intentos - intentos}")

        try:
            coordenadas = input(
                "Introduce la Fila y Columna separadas por coma (Ej: 1,3): "
            )

            fila_str, columna_str = coordenadas.split(",")

            fila = int(fila_str.strip()) - 1
            columna = int(columna_str.strip()) - 1

            if not (0 <= fila <= 2 and 0 <= columna <= 2):
                print("Coordenadas inválidas. Deben ser entre 1 y 3.")
                continue

        except:
            print("Entrada no válida. Asegúrate de usar el formato Fila,Columna.")
            continue

        intentos += 1

        if fila == fila_tesoro and columna == columna_tesoro:
            tablero[fila][columna] = "💰"
            mostrar_tablero()
            print(f"🎉 ¡Felicidades! Encontraste el tesoro en {intentos} intentos.")
            return

        else:
            tablero[fila][columna] = "X"
            print("❌ No hay tesoro aquí. ¡Sigue buscando!")

    mostrar_tablero()
    print("\n--- ¡Fin del juego! ---")
    print(
        f"Te quedaste sin intentos. El tesoro estaba en la Fila {fila_tesoro + 1}, Columna {columna_tesoro + 1}."
    )


if __name__ == "__main__":
    caza_del_tesoro()
