import unittest
import sys
import os
# Añadimos la raíz del proyecto al path para que pueda encontrar 'bufalo'
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..')) # Vamos 3 niveles arriba

# Importamos la función que vamos a probar
from .temperatura import c_a_f, f_a_c
# Importamos la función de configuración (Ahora debería funcionar)
from bufalo.config.preferencias import establecer_preferencia 

class TemperaturaTest(unittest.TestCase):
    
    # Esta función se ejecuta antes de cada prueba y se asegura de que la
    # preferencia de decimales esté configurada al menos a 2 para empezar.
    def setUp(self):
        establecer_preferencia("decimales", 2)


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


if __name__ == '__main__':
    unittest.main()