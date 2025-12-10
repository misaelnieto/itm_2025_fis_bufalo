Herramientas de Aseguramiento de Calidad 🛡️

(Aplicado a mi módulo conversor)
(Jorge Omar Jaramillo Audeves)

Para que un módulo forme parte del proyecto Bufalo, no basta con que funcione: debe cumplir estándares de calidad, consistencia y correctitud.
En mi módulo conversor, estas herramientas fueron esenciales para garantizar que el código fuera claro, seguro y totalmente probado.

En este proyecto se utilizan tres herramientas principales:

1. Ruff 🧹
¿Qué es?

Ruff es un linter y formateador que revisa el estilo del código.

¿Cómo se aplicó en mi módulo?

Lo utilicé para asegurar que el archivo conversor.py estuviera limpio y ordenado:

Imports acomodados correctamente

Código con formato consistente

Sin espacios de más ni líneas innecesarias

Antes de pasar Ruff, mi archivo tenía un error de imports sin ordenar.
Ruff lo detectó y lo corrigió automáticamente.

Comandos usados:
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .

Resultado:

✔ All checks passed
✔ Código formateado y legible

2. Ty (mypy) 🔍
¿Qué es?

Ty es un verificador de tipos que asegura que el código use los tipos adecuados.

¿Cómo se aplicó en mi módulo?

El módulo conversor utiliza:

float para el parámetro valor

str para las unidades

Final[Dict[str, float]] para definir las unidades válidas

Ty confirmó que todos los tipos estaban correctamente usados y que las operaciones eran seguras.

Comando usado:
uv run ty check .

Resultado:

✔ Success: no issues found

3. pytest-cov 📊
¿Qué es?

Herramienta que mide qué porcentaje del código es cubierto por las pruebas.

¿Cómo se aplicó en mi módulo?

Creé pruebas en tests/test_conversor.py que validan:

Conversión correcta entre unidades (m → km, km → m, cm → m)

Manejo de errores cuando se ingresan unidades no válidas

La salida textual exacta que debe producir el comando

La integración con el CLI usando CliRunner

Comando usado:
uv run pytest --cov

Resultado para mi módulo:

✔ src/bufalo/modulos/conversor.py → 100% de cobertura
✔ Todas las pruebas pasaron (4/4)
✔ Sin funciones sin probar
✔ Sin ramas faltantes

Proceso de Calidad aplicado a mi módulo 🔄

El flujo que seguí fue:

Escribir las pruebas en test_conversor.py

Ejecutar pytest y ver fallos (Rojo)

Implementar el código mínimo para pasar las pruebas (Verde)

Organizar y documentar el código (Refactor)

Ejecutar todas las herramientas de calidad

Checklist final:
Verificación	Comando	Resultado
Formato correcto	uv run ruff format .	✔
Linter sin errores	uv run ruff check .	✔
Tipos correctos	uv run ty check .	✔
Pruebas pasando	uv run pytest	✔
Cobertura completa	uv run pytest --cov	100% en mi módulo

Todo mi módulo conversor cumple con los estándares del proyecto.

Comandos rápidos para validar calidad 🚀
uv run ruff format .
uv run ruff check .
uv run ty check .
uv run pytest --cov


Si estos comandos pasan sin errores, el código está listo para integrarse.

Resumen 📋

Mi módulo conversor cumple con todos los requisitos de calidad del proyecto:

Código limpio y ordenado

Tipos validados

100% de cobertura de pruebas

Integrado correctamente con Click

Compatible con las reglas del repositorio

Gracias a estas herramientas, el módulo no solo funciona, sino que es seguro, claro y mantenible.