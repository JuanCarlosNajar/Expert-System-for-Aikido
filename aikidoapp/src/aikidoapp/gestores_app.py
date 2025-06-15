# gestores_app.py
"""
Este módulo sirve para declarar gestores globales, que pueden usarse desde cualquier módulo
de la aplicación, sin necesidad de declarar un objeto de estas clases gestoras, gracias a la 
utilización de @classmethod, directiva que convierte el método en un método de clase, que puede
ser llamado directamente, sin necesidad de declarar un objeto de esta clase.
Gestores implementados:
1) Gestor de contextos
2) Gestor de pantallas
3) Gestor de iconos
4) Gestor de ontología, de la base de conocimientos. Asumimos que gestionamos una única ontología.
""" 
class GestoresApp:
    _gestor_contextos = None
    _gestor_pantallas = None
    _gestor_iconos= None
    _gestor_ontologia = None

    @classmethod
    def set_contextos(cls, gestor_contextos):
        cls._gestor_contextos = gestor_contextos

    @classmethod
    def set_pantallas(cls, gestor_pantallas):
        cls._gestor_pantallas = gestor_pantallas

    @classmethod
    def set_iconos(cls, gestor_iconos):
        cls._gestor_iconos = gestor_iconos

    @classmethod
    def set_ontologia(cls, gestor_ontologia):
        cls._gestor_ontologia = gestor_ontologia

    @classmethod
    def contextos(cls):
        if cls._gestor_contextos is None:
            raise Exception("[ERROR] Gestor de contextos no ha sido inicializado.")
        return cls._gestor_contextos

    @classmethod
    def pantallas(cls):
        if cls._gestor_pantallas is None:
            raise Exception("[ERROR] Gestor de pantallas no ha sido inicializado.")
        return cls._gestor_pantallas

    @classmethod
    def iconos(cls):
        if cls._gestor_iconos is None:
            raise Exception("[ERROR] Gestor de iconos no ha sido inicializado.")
        return cls._gestor_iconos
    
    @classmethod
    def ontologia(cls):
        if cls._gestor_ontologia is None:
            raise Exception("[ERROR] Gestor de ontología no ha sido inicializado.")
        return cls._gestor_ontologia