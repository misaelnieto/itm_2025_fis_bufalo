# Guía de uso: Comparador de seguidores y seguidos de Instagram

Este programa permite comparar tus seguidores y seguidos de Instagram para saber:
- Quiénes te siguen pero tú no los sigues.
- Quiénes sigues pero no te siguen de vuelta.

---

## 1. Archivos necesarios de Instagram

Debes descargar tu información desde Instagram:

1. Ve a tu perfil en la app o en la web.
2. Entra a **Configuración → Privacidad y seguridad → Descargar información**.
3. Solicita tu descarga en formato **JSON**.
4. Instagram te enviará un archivo comprimido (.zip) por correo.
5. Dentro del .zip encontrarás varias carpetas y archivos. Los que necesitas son:

- **followers_1.json** → contiene la lista de tus seguidores.
- **following.json** → contiene la lista de las cuentas que sigues.

👉 Estos archivos pueden estar en cualquier carpeta de tu computadora (por ejemplo, **Descargas**, **Escritorio** o **Documentos**).  
⚠️ **Importante:** siempre debes pasar **ambas rutas juntas** en el comando, sin importar si usas `--myfollows` o `--myfollowers`.

---

## 2. Cómo funciona el programa

El comando principal es:
uv run bufalo francisco comparar [opciones] RUTA\followers_1.json RUTA\following.json


### Opciones disponibles:
- `--myfollows` → muestra las personas que **tú sigues pero no te siguen de vuelta**.
- `--myfollowers` → muestra las personas que **te siguen pero tú no los sigues de vuelta**.

---

## 3. Ejemplos de uso

### Archivos en la carpeta Descargas:

uv run bufalo francisco comparar --myfollowers C:\Users\TuUsuario\Downloads\followers_1.json C:\Users\TuUsuario\Downloads\following.json


---

## 4. Resultados esperados

El programa imprimirá en consola algo como:

EJEMPLO 
=== Personas que sigues pero NO te siguen ===
- ana
- carlos
- sofia

o, si no hay diferencias:
✅ Todos los que sigues también te siguen


---

## 5. Pruebas automáticas

El proyecto incluye pruebas con `pytest` para verificar que todo funciona correctamente:
uv run pytest -v uv run pytest --cov

Puedes ver un reporte visual de cobertura con:
uv run pytest --cov --cov-report=html start msedge htmlcov\index.html


---

## 6. Notas finales

- Los archivos `followers_1.json` y `following.json` pueden estar en cualquier carpeta, siempre que se indique la ruta correcta.
- ⚠️ Siempre debes pasar **ambas rutas juntas** en el comando, sin importar la opción que uses.
- Si los archivos están en la misma carpeta donde ejecutas el comando, basta con poner solo el nombre.
- El programa solo funciona con los archivos oficiales exportados desde Instagram en formato JSON.
