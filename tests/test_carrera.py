from carrera import main

def test_version():
    out = main(["version"])
    assert "v1.0" in out

def test_iniciar():
    out = main(["iniciar"])
    assert "2 jugadores" in out

def test_cpu():
    out = main(["cpu"])
    assert "CPU" in out

def test_invalido():
    out = main(["nada"])
    assert "no reconocido" in out.lower()
