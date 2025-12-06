# 🦬 Proyecto Bufalo

Herramienta CLI para aprender **Desarrollo Guiado por Pruebas (TDD)** en Python.

Cada estudiante implementará su propio módulo como un comando CLI, siguiendo las mejores prácticas de desarrollo de software.

---

## 🎯 Objetivo de la Tarea

Tu tarea es implementar un **módulo con comandos CLI** siguiendo este proceso:

1. **Escribir pruebas** que describan lo que debe hacer tu módulo (TDD)
2. **Implementar el código** para que las pruebas pasen
3. **Verificar la calidad** con herramientas de análisis estático
4. **Contribuir tu trabajo** mediante un Pull Request

---

## 📚 Guías de Aprendizaje

Sigue estas guías en orden para completar tu tarea:

### 1. [Instalación de UV](docs/UV.md) 🔧

Instala y configura UV, el administrador de paquetes que usaremos en el proyecto.


### 2. [TDD y pytest](docs/pytest.md) 🧪
Aprende qué es TDD, cómo funciona pytest, y cómo escribir pruebas para tu módulo.

### 3. [Aseguramiento de Calidad](docs/Calidad.md) 🛡️
Conoce las herramientas que verifican la calidad de tu código: Ruff, Ty y pytest-cov.

### 4. [Contribuyendo al Proyecto](docs/Branch.md) 🤝
Aprende a hacer commits, subir tu código a GitHub y crear un Pull Request.

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.12+
- UV instalado (ver [guía de instalación](docs/UV.md))

### Configuración Inicial
```powershell
# Clonar el repositorio
git clone <url-del-repositorio>
cd itm_2025_fis_tdd

# Instalar dependencias
uv sync

# Verificar que todo funciona
uv run bufalo --help
```

---

## 📁 Estructura del Proyecto

```
itm_2025_fis_tdd/
├── src/bufalo/
│   ├── cli.py              # CLI principal con autodiscovery
│   └── modulos/            # Aquí va TU módulo
│       └── calculadora.py  # Ejemplo de módulo
│
├── tests/                  # Aquí van TUS pruebas
│   └── test_calculadora.py # Ejemplo de pruebas
│
└── docs/                   # Documentación del proyecto
    ├── UV.md
    ├── pytest.md
    ├── Calidad.md
    └── Branch.md
```

---

## ✅ Comandos Esenciales

```powershell
# Ejecutar tu CLI
uv run bufalo

# Ejecutar pruebas
uv run pytest

# Verificar calidad del código
uv run ruff format .    # Formatear
uv run ruff check .     # Linter
uv run ty .             # Tipos

# Ver cobertura de pruebas
uv run pytest --cov
```

---

## 🎓 Ejemplo: Módulo Calculadora

El proyecto incluye un módulo de ejemplo (`calculadora`) que puedes usar como referencia:

```powershell
# Probar el módulo calculadora
uv run bufalo calculadora suma 1 2 3
uv run bufalo calculadora divide 10 2

# Ver las pruebas del módulo
# Archivo: tests/test_calculadora.py (extensivamente documentado)
```

---

## 💡 Recursos Adicionales

- **Documentación de Click**: https://click.palletsprojects.com/
- **Documentación de pytest**: https://docs.pytest.org/
- **Guía de TDD**: Consulta [docs/pytest.md](docs/pytest.md)

---

## 🆘 ¿Necesitas Ayuda?

1. Revisa las guías en la carpeta `docs/`
2. Consulta el código de ejemplo en `src/bufalo/modulos/calculadora.py`
3. Pregunta a tu instructor o compañeros

¡Buena suerte con tu módulo! 🚀
