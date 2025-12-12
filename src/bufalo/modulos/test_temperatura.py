import unittest
import os
import sys

# Añadimos la raíz del proyecto al path para asegurar que la importación funcione
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..')) 

# 1. Importación ABSOLUTA completa para temperatura
from src.bufalo.modulos.temperatura import c_a_f, f_a_c, convertir 

# 2. Importación ABSOLUTA completa para preferencias
from src.bufalo.config.preferencias import establecer_preferencia

class TemperaturaTest(unittest.TestCase):
    
    # Esta función se ejecuta antes de cada prueba y se asegura de que la configuración
    # esté reseteada a un estado conocido.
    def setUp(self):
        establecer_preferencia("decimales", 2)
        establecer_preferencia("unidad_preferida", "C") 

    def test_01_c_a_f_redondeo_defecto(self):
        """Prueba la conversión C a F usando los decimales por defecto (2)."""
        self.assertEqual(c_a_f(22.5), 72.50) 
        self.assertEqual(c_a_f(3.333333), 38.00) 

    def test_02_f_a_c_redondeo_defecto(self):
        """Prueba la conversión F a C usando los decimales por defecto (2)."""
        self.assertEqual(f_a_c(50.0), 10.00)
        self.assertEqual(f_a_c(35), 1.67) 

    def test_03_cambiar_decimales_a_tres(self):
        """Prueba que la función respeta el cambio a 3 decimales."""
        establecer_preferencia("decimales", 3)
        self.assertEqual(f_a_c(35), 1.667)
        self.assertEqual(c_a_f(3.333333), 38.000)

    def test_04_cambiar_decimales_a_cero(self):
        """Prueba que la función respeta el cambio a 0 decimales (entero)."""
        establecer_preferencia("decimales", 0)
        self.assertEqual(f_a_c(35), 2)
        self.assertEqual(c_a_f(3.333333), 38)
        
    def test_05_convertir_a_unidad_preferida_celsius(self):
        """Prueba que convertir() usa f_a_c cuando unidad_preferida es 'C'."""
        self.assertEqual(convertir(50), 10.00) 
        self.assertEqual(convertir(35), 1.67) 

    def test_06_convertir_a_unidad_preferida_fahrenheit(self):
        """Prueba que convertir() usa c_a_f cuando unidad_preferida es 'F'."""
        establecer_preferencia("unidad_preferida", "F")
        self.assertEqual(convertir(22.5), 72.50)
        self.assertEqual(convertir(10), 50.00)


if __name__ == '__main__':
    unittest.main()