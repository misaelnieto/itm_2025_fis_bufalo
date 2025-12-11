def romano_a_entero(romano: str) -> int:
    """Convierte un número romano válido a un entero.
    Soporta notación sustractiva: IV, IX, XL, XC, CD, CM."""
    valores = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    total = 0
    previo = 0

    for letra in reversed(romano.upper()):
        valor = valores[letra]
        if valor < previo:
            total -= valor
        else:
            total += valor
        previo = valor

    return total


def entero_a_romano(numero: int) -> str:
    """
    Convierte un entero entre 1 y 3999 a número romano estándar.
    """
    if numero < 1 or numero > 3999:
        raise ValueError("El número debe estar entre 1 y 3999.")

    valores = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    resultado = ""

    for valor, simbolo in valores:
        while numero >= valor:
            resultado += simbolo
            numero -= valor

    return resultado


def main() -> None:
    """
    Punto de entrada interactivo para el conversor.
    Pide un número por teclado y muestra la conversión.
    """
    print("Conversor Romano <-> Entero (1–3999)")
    dato = input("Escribe un número romano o entero: ")

    if dato.isdigit():
        numero = int(dato)
        print(f"{numero} en romano es: {entero_a_romano(numero)}")
    else:
        print(f"{dato} en entero es: {romano_a_entero(dato)}")


if __name__ == "__main__":  # pragma: no cover
    main()
