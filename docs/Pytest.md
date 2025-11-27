# ¿Qué es TDD? 🧪

**TDD** significa **Test-Driven Development** (Desarrollo Guiado por Pruebas).

Es una forma de programar donde **escribimos las pruebas ANTES de escribir el código**. Esto puede sonar extraño, pero tiene muchas ventajas:

- Nos aseguramos de que nuestro código funciona correctamente
- Detectamos errores más rápido
- Nuestro código es más fácil de entender y mantener
- Sabemos exactamente qué debe hacer nuestro programa antes de escribirlo

## El ciclo de TDD 🔄

TDD sigue tres pasos simples que se repiten:

1. **🔴 Rojo**: Escribimos una prueba que falla (porque el código aún no existe)
2. **🟢 Verde**: Escribimos el código mínimo necesario para que la prueba pase
3. **🔵 Refactor**: Mejoramos el código sin cambiar su comportamiento

---

## ¿Qué es pytest? 🔬

**pytest** es una herramienta de Python que nos ayuda a ejecutar nuestras pruebas automáticamente.

pytest:
- Busca archivos que empiecen con `test_`
- Ejecuta todas las funciones que empiecen con `test_`
- Nos dice cuáles pruebas pasaron ✅ y cuáles fallaron ❌
- Muestra mensajes claros cuando algo no funciona

---

## Estructura del proyecto Bufalo 📁

En este proyecto, organizamos nuestro código en dos lugares principales:

```
itm_2025_fis_tdd/
├── src/bufalo/modulos/     ← Aquí va el CÓDIGO de tu módulo
│   └── calculadora.py      ← Ejemplo: módulo calculadora
│
└── tests/                  ← Aquí van las PRUEBAS
    └── test_calculadora.py ← Ejemplo: pruebas de calculadora
```

### Regla importante:
- **Código del módulo**: `src/bufalo/modulos/nombre_modulo.py`
- **Pruebas del módulo**: `tests/test_nombre_modulo.py`

---

## Proceso para crear tu módulo con TDD 🛠️

Vamos a usar el módulo **calculadora** como ejemplo para entender el proceso.

### Paso 1: Crear el archivo de pruebas 📝

Primero, creamos el archivo de pruebas en `tests/test_calculadora.py`:

```python
from click.testing import CliRunner
from bufalo.modulos.calculadora import calculadora

def test_suma_dos_numeros() -> None:
    """Prueba que podemos sumar dos números."""
    runner = CliRunner()
    result = runner.invoke(calculadora, ["suma", "2", "3"])
    assert result.exit_code == 0
    assert "Resultado: 5.0" in result.output
```

### Paso 2: Ejecutar la prueba (debe fallar 🔴)

Ejecutamos pytest para ver que la prueba falla:

```powershell
uv run pytest tests/test_calculadora.py -v
```

La prueba fallará porque el módulo `calculadora.py` aún no existe. ¡Esto es normal en TDD!

### Paso 3: Crear el código mínimo 💻

Ahora creamos `src/bufalo/modulos/calculadora.py` con el código necesario:

```python
import click

@click.group()
def calculadora() -> None:
    """Comandos de la calculadora."""
    pass

@calculadora.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def suma(a: float, b: float) -> None:
    """Suma dos números."""
    result = a + b
    click.echo(f"Resultado: {result}")
```

### Paso 4: Ejecutar la prueba nuevamente (debe pasar 🟢)

```powershell
uv run pytest tests/test_calculadora.py -v
```

¡Ahora la prueba debe pasar! ✅

### Paso 5: Agregar más pruebas y funcionalidad 🔄

Repetimos el ciclo:
1. Escribimos una nueva prueba (por ejemplo, para resta)
2. Vemos que falla
3. Escribimos el código para que pase
4. Mejoramos el código si es necesario

---

## Comandos útiles de pytest 🎯

### Ejecutar todas las pruebas:
```powershell
uv run pytest
```

### Ejecutar pruebas de un archivo específico:
```powershell
uv run pytest tests/test_calculadora.py
```

### Ejecutar con más detalles (verbose):
```powershell
uv run pytest -v
```

### Ver cobertura de código:
```powershell
uv run pytest --cov
```

---

## Resumen para tu módulo 📋

Cuando crees tu propio módulo, sigue estos pasos:

1. **Crea tu archivo de pruebas**: `tests/test_tu_modulo.py`
2. **Escribe una prueba** que describa lo que quieres que haga tu código
3. **Ejecuta pytest** y confirma que falla (🔴 rojo)
4. **Crea tu módulo**: `src/bufalo/modulos/tu_modulo.py`
5. **Escribe el código** mínimo para que la prueba pase
6. **Ejecuta pytest** y confirma que pasa (🟢 verde)
7. **Mejora tu código** si es necesario (🔵 refactor)
8. **Repite** el proceso para cada nueva funcionalidad

¡Recuerda! En TDD, **las pruebas van primero**. Si escribes el código antes que las pruebas, no estás haciendo TDD. 🎓

---

## 📖 Navegación

> [!TIP]
> **Siguiente paso**: Aprende sobre las herramientas de aseguramiento de calidad.

- 🏠 [Volver al README](../README.md)
- ⬅️ **Anterior**: [Instalación de UV](Uv.md)
- ➡️ **Siguiente**: [Aseguramiento de Calidad](Calidad.md)

