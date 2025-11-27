# ¿Qué es UV? 🔧

**UV** es una herramienta que nos ayuda a instalar y manejar programas de Python en nuestra computadora.

Piensa en UV como un asistente que:
- Descarga las librerías (piezas de código) que nuestro proyecto necesita
- Se asegura de que todas las versiones sean compatibles
- Ejecuta nuestros programas de Python de manera correcta

En este proyecto, usamos **UV** para:
- Instalar dependencias como `click` (para crear comandos de terminal)
- Ejecutar nuestro programa `bufalo`
- Correr las pruebas con `pytest`

---

## Instalación de UV en Windows 💻

### Paso 1: Abrir la Terminal

1. Presiona la tecla **Windows** en tu teclado
2. Escribe **PowerShell**
3. Haz clic en **Windows PowerShell** (aparecerá una ventana azul con texto blanco)

### Paso 2: Ejecutar el comando de instalación
Copia y pega este comando en la terminal, luego presiona **Enter**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex""
```

⏳ Espera unos segundos mientras UV se descarga e instala.

### Paso 3: Cerrar y volver a abrir la terminal

1. Cierra la ventana de PowerShell
2. Abre PowerShell nuevamente (repite el Paso 1)

Esto es necesario para que Windows reconozca el nuevo programa.

### Paso 4: Verificar que UV está instalado correctamente ✅

Escribe este comando en la terminal y presiona **Enter**:

```powershell
uv --version
```

Si ves algo como `uv 0.9.11` (el número puede variar), ¡UV está instalado correctamente! 🎉

Si ves un error, repite los pasos anteriores o pide ayuda a tu instructor.

---

## 📖 Navegación

> [!TIP]
> **Siguiente paso**: Ahora que tienes UV instalado, aprende sobre TDD y pytest.

- 🏠 [Volver al README](../README.md)
- ➡️ **Siguiente**: [TDD y pytest](Pytest.md)

