import random
#version definitiva
def ruleta_de_la_suerte():
    print("--- R U L E T A  R U S A ---")
    
    # 1. Obtener la apuesta del usuario
    while True:
        try:
            apuesta = float(input("¿Cuánto dinero quieres apostar? "))
            if apuesta <= 0:
                print("Por favor, introduce una cantidad positiva.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número.")

    # 2. Obtener la elección del número del usuario
    while True:
        try:
            eleccion = int(input("Elige un número del 1 al 6: "))
            if 1 <= eleccion <= 6:
                break
            else:
                print("Elige un número válido entre 1 y 6.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

    # 3. Confirmación de la apuesta
    confirmacion = input(f"Has apostado ${apuesta} al número {eleccion}. ¿Estas Listo? (sí/no): ").lower()
    
    if confirmacion != 'sí' and confirmacion != 'si':
        print("\nDecisión cancelada. Tu dinero está a salvo. ¡Vuelve pronto!")
        return

    # 4. Simular el lanzamiento del dado
    print("\n--- ¡Gira la Ruleta! ---")
    
    # Genera un número aleatorio entre 1 y 6 (simulando un dado)
    resultado_dado = random.randint(1, 6)
    
    print(f"El dado ha caído en el número: **{resultado_dado}**")

    # 5. Comprobar el resultado
    if eleccion == resultado_dado:
        ganancia = apuesta * 2
        print(f"\n ¡GANASTE! Has acertado al número **{eleccion}**.")
        print(f"La ganancia se duplica. Ahora tienes **${ganancia:.2f}**.")
    else:
        print(f"\n PERDISTE. El número era el **{resultado_dado}**.")
        print(f"Has perdido tu apuesta de ${apuesta:.2f}.")
        print("Tu saldo final es $0.00 (de esta ronda). ¡Suerte la próxima vez!")

# Para ejecutar el juego
if __name__ == "__main__":
    ruleta_de_la_suerte()