import random
import pytest
import dado 

from src.bufalo.modulos.dado import ruleta_de_la_suerte
#version definitiva
def _ruleta_de_la_suerte():
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

@pytest.mark.parametrize(
    "inputs,expected_error_message,expected_prompt_count",
    [
        (["0", "10"], "Por favor, introduce una cantidad positiva.", 2),
        (["-5", "10"], "Por favor, introduce una cantidad positiva.", 2),
        (["abc", "10"], "Entrada inválida. Por favor, introduce un número.", 2),
    ],
)
def test_ruleta_de_la_suerte_valida_entradas_invalidas_y_muestra_mensajes(monkeypatch, capsys, inputs, expected_error_message, expected_prompt_count):
    # Simular secuencia de entradas del usuario
    entradas = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    # Ejecutar función
    ruleta_de_la_suerte()

    # Capturar salida estándar
    captured = capsys.readouterr().out

    # Se debe mostrar el mensaje de error esperado
    assert expected_error_message in captured

    # El prompt debe aparecer tantas veces como entradas se simulan
    prompt = "¿Cuánto dinero quieres apostar? "
    assert captured.count(prompt) == expected_prompt_count

    # La cabecera del juego debe mostrarse al inicio
    assert "--- R U L E T A  R U S A ---" in captured


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

def _run_juego_con_entradas(monkeypatch, entradas, resultado_dado=None):
    """
    Helper para ejecutar la función principal del juego simulando entradas de usuario
    y, opcionalmente, controlando el valor devuelto por random.randint.
    """
    # Ajusta aquí el nombre real de la función a probar
    juego_fn = dado.jugar_dado

    # Simular input() con la lista de entradas proporcionadas
    entradas_iter = iter(entradas)
    monkeypatch.setattr("builtins.input", lambda _: next(entradas_iter))

    # Stub de random.randint si se proporciona un resultado esperado
    if resultado_dado is not None:
        monkeypatch.setattr("random.randint", lambda a, b: resultado_dado)

    # Ejecutar la función bajo prueba
    juego_fn()


def test_cancelacion_apuesta_no_ejecuta_lanzamiento(monkeypatch, capsys):
    """
    Flujo: ['10', '3', 'no']
    Debe cancelar la apuesta antes de llamar a random.randint y mostrar el mensaje de cancelación.
    """
    original_randint = random.randint

    def _randint_no_deberia_ser_llamado(*_args, **_kwargs):
        pytest.fail("random.randint debería NO ser llamado en el flujo de cancelación")

    monkeypatch.setattr("random.randint", _randint_no_deberia_ser_llamado)

    _run_juego_con_entradas(monkeypatch, ["10", "3", "no"])

    # Restauramos manualmente por si otros tests dependen del comportamiento real
    random.randint = original_randint

    salida = capsys.readouterr().out
    assert "Decisión cancelada. Tu dinero está a salvo. ¡Vuelve pronto!" in salida


@pytest.mark.parametrize("confirmacion", ["sí", "si"])
def test_confirmacion_apuesta_ejecuta_lanzamiento(monkeypatch, capsys, confirmacion):
    """
    Flujos: ['10', '3', 'sí'] / ['10', '3', 'si']
    Debe ejecutar el lanzamiento del dado (random.randint) y mostrar el resultado.
    """
    resultado_controlado = 4

    _run_juego_con_entradas(
        monkeypatch,
        ["10", "3", confirmacion],
        resultado_dado=resultado_controlado,
    )

    salida = capsys.readouterr().out
    assert "Decisión cancelada. Tu dinero está a salvo. ¡Vuelve pronto!" not in salida
    assert "--- ¡Gira la Ruleta! ---" in salida
    assert f"El dado ha caído en el número: **{resultado_controlado}**" in salida

# Para ejecutar el juego
if __name__ == "__main__":
    ruleta_de_la_suerte()