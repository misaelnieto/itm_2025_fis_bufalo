from unittest.mock import patch

from click.testing import CliRunner

from bufalo.modulos.adivina import adivina, evaluar_intento

# ---------------------------
# PRUEBAS UNITARIAS
# ---------------------------

def test_evaluar_intento_gana():
    assert evaluar_intento(50, 50) == "ganaste"

def test_evaluar_intento_muy_bajo():
    assert evaluar_intento(50, 10) == "muy bajo"

def test_evaluar_intento_muy_alto():
    assert evaluar_intento(50, 90) == "muy alto"

# ---------------------------
# PRUEBAS CLI (Simulando escenarios)
# ---------------------------

def test_cli_jugar_gana():
    """Simula que el usuario adivina el número correctamente."""
    runner = CliRunner()
    
    with patch('bufalo.modulos.adivina.random.randint', return_value=50):
        result = runner.invoke(adivina, ["jugar"], input="50\n")
        
    assert result.exit_code == 0
    assert "ganaste" in result.output

def test_cli_jugar_pierde():
    """Simula que el usuario pierde para cubrir la línea 'Perdiste'."""
    runner = CliRunner()
    
    with patch('bufalo.modulos.adivina.random.randint', return_value=99):
        result = runner.invoke(adivina, ["jugar"], input="1\n2\n3\n")
    
    assert result.exit_code == 0
    assert "Perdiste. El número era 99" in result.output

def test_cli_dificil_gana():
    """Simula ganar en modo difícil."""
    runner = CliRunner()
    
    with patch('bufalo.modulos.adivina.random.randint', return_value=500):
        result = runner.invoke(adivina, ["dificil"], input="500\n")
        
    assert result.exit_code == 0
    assert "ganaste" in result.output

def test_cli_dificil_pierde():
    """Simula perder en modo difícil."""
    runner = CliRunner()
    
    with patch('bufalo.modulos.adivina.random.randint', return_value=1000):
        result = runner.invoke(adivina, ["dificil"], input="1\n2\n3\n")
        
    assert result.exit_code == 0
    assert "Perdiste. El número era 1000" in result.output