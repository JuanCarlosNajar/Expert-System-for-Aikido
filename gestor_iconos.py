# gestor_iconos.py
import toga
import os
from pathlib import Path

class GestorIconos:
    def __init__(self, ruta_base):
        """
        Inicializa el gestor de iconos con la ruta base donde se encuentran los iconos.
        :param ruta_base: Ruta base absoluta o relativa donde están almacenados los iconos.
        """
        if not ruta_base:
            ruta_base = Path(__file__).parent
        self.ruta_base = ruta_base / "icons"

    def obtener_icono(self, nombre_archivo):
        """
        Devuelve un objeto toga.Icon dado un nombre de archivo.

        :param nombre_archivo: Nombre del archivo de icono (por ejemplo: 'grupos.png').
        :param tamaño: Tamaño del icono (por defecto: 32).
        :return: Instancia de toga.Icon
        """
        ruta_icono = self.ruta_base / nombre_archivo

        if not os.path.exists(ruta_icono):
            print(f"[ADVERTENCIA] El icono '{nombre_archivo}' no se encontró en {self.ruta_base}")
            return None

        return toga.Icon(str(ruta_icono.resolve()))
