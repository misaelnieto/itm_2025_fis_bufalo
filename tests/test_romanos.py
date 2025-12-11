import pytest

from bufalo.modulos.romanos import entero_a_romano, main, romano_a_entero

# ==========================
#   Pruebas romano -> entero
# ==========================


def test_romano_I_es_1() -> None:
    assert romano_a_entero("I") == 1


def test_romano_V_es_5() -> None:
    assert romano_a_entero("V") == 5


def test_romano_X_es_10() -> None:
    assert romano_a_entero("X") == 10


def test_romano_L_es_50() -> None:
    assert romano_a_entero("L") == 50


def test_romano_C_es_100() -> None:
    assert romano_a_entero("C") == 100


def test_romano_D_es_500() -> None:
    assert romano_a_entero("D") == 500


def test_romano_M_es_1000() -> None:
    assert romano_a_entero("M") == 1000


def test_romano_IV_es_4() -> None:
    assert romano_a_entero("IV") == 4


def test_romano_IX_es_9() -> None:
    assert romano_a_entero("IX") == 9


def test_romano_XL_es_40() -> None:
    assert romano_a_entero("XL") == 40


def test_romano_XC_es_90() -> None:
    assert romano_a_entero("XC") == 90


def test_romano_CD_es_400() -> None:
    assert romano_a_entero("CD") == 400


def test_romano_CM_es_900() -> None:
    assert romano_a_entero("CM") == 900


def test_romano_MCMXC_es_1990() -> None:
    assert romano_a_entero("MCMXC") == 1990


def test_romano_MMXXV_es_2025() -> None:
    assert romano_a_entero("MMXXV") == 2025


def test_romano_MMDCLXVI_es_2666() -> None:
    assert romano_a_entero("MMDCLXVI") == 2666


def test_romano_minusculas_tambien_funciona() -> None:
    assert romano_a_entero("mcmxc") == 1990


# ==========================
#   Pruebas entero -> romano
# ==========================


def test_entero_a_romano_basicos() -> None:
    assert entero_a_romano(1) == "I"
    assert entero_a_romano(3) == "III"
    assert entero_a_romano(5) == "V"
    assert entero_a_romano(10) == "X"


def test_entero_a_romano_sustractivos() -> None:
    assert entero_a_romano(4) == "IV"
    assert entero_a_romano(9) == "IX"
    assert entero_a_romano(40) == "XL"
    assert entero_a_romano(90) == "XC"
    assert entero_a_romano(400) == "CD"
    assert entero_a_romano(900) == "CM"


def test_entero_a_romano_compuestos() -> None:
    assert entero_a_romano(58) == "LVIII"
    assert entero_a_romano(1994) == "MCMXCIV"
    assert entero_a_romano(2025) == "MMXXV"
    assert entero_a_romano(2666) == "MMDCLXVI"


def test_entero_a_romano_fuera_de_rango() -> None:
    with pytest.raises(ValueError):
        entero_a_romano(0)

    with pytest.raises(ValueError):
        entero_a_romano(4000)


# ================================
#   Pruebas del flujo interactivo
# ================================


def test_main_entero_a_romano(monkeypatch, capsys) -> None:
    # Simulamos que input() devuelve "18"
    monkeypatch.setattr("builtins.input", lambda _: "18")

    main()

    capturado = capsys.readouterr()
    assert "Conversor Romano <-> Entero" in capturado.out
    assert "18 en romano es: XVIII" in capturado.out


def test_main_romano_a_entero(monkeypatch, capsys) -> None:
    """
    Prueba el flujo interactivo cuando se ingresa un número romano.
    Simula escribir 'XIV' y verifica que imprima '14'.
    """
    monkeypatch.setattr("builtins.input", lambda _: "XIV")

    main()

    capturado = capsys.readouterr()
    assert "Conversor Romano <-> Entero" in capturado.out
    assert "XIV en entero es: 14" in capturado.out
