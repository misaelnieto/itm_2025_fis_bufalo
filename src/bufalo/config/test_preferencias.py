import unittest
import json
from pathlib import Path

# Importamos las funciones públicas y el nombre del archivo de configuración
# El punto (.) antes de preferencias es CRUCIAL para que funcione como paquete.
from .preferencias import obtener_preferencias, establecer_preferencia, PREFS_FILE

# Este es el contenido por defecto que esperamos
DEFAULTS_EXPECTED = {
    "unidad_preferida": "C",
    "decimales": 2
}

class PreferenciasTest(unittest.TestCase):
    
    # -----------------------------
    # GESTIÓN DE ARCHIVOS PARA LAS PRUEBAS
    # -----------------------------
    def setUp(self):
        """Se ejecuta antes de cada prueba. Garantiza que el archivo NO exista al inicio."""
        # Si el archivo existe de una prueba anterior, lo elimina
        if PREFS_FILE.exists():
            PREFS_FILE.unlink()

    def tearDown(self):
        """Se ejecuta después de cada prueba. Elimina el archivo que se haya creado."""
        # Limpia el archivo después de que la prueba termine
        if PREFS_FILE.exists():
            PREFS_FILE.unlink()

    # -----------------------------
    # PRUEBAS FUNCIONALES
    # -----------------------------
    def test_01_cargar_preferencias_por_defecto(self):
        """Prueba que devuelve los valores por defecto si el archivo no existe."""
        resultado = obtener_preferencias()
        self.assertEqual(resultado, DEFAULTS_EXPECTED)
        # Asegura que la función obtener_preferencias no haya creado el archivo si no existía
        self.assertFalse(PREFS_FILE.exists()) 

    def test_02_establecer_preferencia_crea_archivo(self):
        """Prueba que al establecer una preferencia, el archivo se crea y guarda el valor."""
        clave = "decimales"
        nuevo_valor = 3
        
        # 1. Establecer la preferencia
        self.assertTrue(establecer_preferencia(clave, nuevo_valor))
        
        # 2. Verificar que el archivo exista
        self.assertTrue(PREFS_FILE.exists())
        
        # 3. Cargar el contenido directamente para verificar el valor guardado
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            contenido = json.load(f)
            self.assertEqual(contenido[clave], nuevo_valor)

    def test_03_cargar_preferencias_guardadas(self):
        """Prueba que si el archivo existe, se cargan los valores guardados."""
        # 1. Establecer un valor y guardarlo
        establecer_preferencia("unidad_preferida", "F")
        
        # 2. Cargar las preferencias de nuevo
        resultado = obtener_preferencias()
        
        # 3. Verificar que el valor se haya cargado correctamente
        self.assertEqual(resultado["unidad_preferida"], "F")
        # El valor "decimales" debe seguir siendo el valor por defecto (2)
        self.assertEqual(resultado["decimales"], DEFAULTS_EXPECTED["decimales"]) 

    def test_04_manejar_archivo_corrupto(self):
        """Prueba que si el archivo existe pero no es JSON, regresa los valores por defecto."""
        # 1. Crear un archivo no JSON (simulando un archivo corrupto)
        with open(PREFS_FILE, "w", encoding="utf-8") as f:
            f.write("Esto no es JSON")
        
        # 2. Cargar las preferencias
        resultado = obtener_preferencias()
        
        # 3. Debe devolver los valores por defecto
        self.assertEqual(resultado, DEFAULTS_EXPECTED)


if __name__ == '__main__':
    unittest.main()