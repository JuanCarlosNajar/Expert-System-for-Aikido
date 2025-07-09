import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from .gestores_app import GestoresApp

class Pantalla:
    def __init__(self, nombre, cabecera=None, cuerpo=None, pie=None):
        self.nombre = nombre
        self.cabecera = cabecera or self._crear_cabecera()
        self.cuerpo = cuerpo or self._crear_cuerpo()
        self.pie = pie or self._crear_pie()

        # Caja contenedora de toda la pantalla (column layout)
        self.contenedor = toga.Box(style=Pack(direction=COLUMN,flex=1, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        self.contenedor.add(self.cuerpo)
        self.contenedor.add(self.pie)

    def _crear_cabecera(self):
        return toga.Box()  # Método a implementar en las pantallas derivadas
    
    def _crear_pie(self):
        return toga.Box()
    
    def _crear_cuerpo(self):
        return toga.Box()
    
    def mostrar(self):
        self.actualizar()
        return self.contenedor

    # Cada Pantalla derivada tiene que implementar lo que hace actualizar
    def actualizar(self):
        pass
    
    def salva_datos(self):
        pass

    def carga_datos(self):
        pass
    
    def on_press(self, contexto):
        GestoresApp.contextos().ir_a_contexto(contexto)
        GestoresApp.pantallas().ir_a(contexto)
        
    def on_press_anterior(self):
        GestoresApp.contextos().volver_contexto()
        GestoresApp.pantallas().volver()


class GestorPantallas:
    def __init__(self, ventana):
        self.ventana = ventana  # Instancia de toga.MainWindow o similar
        self.pantallas = []  # Lista de objetos Pantalla
        self.indice_actual = -1  # No hay pantalla activa al principio
        self.historial = [] # para guardar el historial de pantallas por las que vamos pasando

    def crear_pantalla(self, nombre, cabecera=None, cuerpo=None, pie=None):
        pantalla = Pantalla(nombre, cabecera, cuerpo, pie)
        self.pantallas.append(pantalla)
        if self.indice_actual == -1:
            self.indice_actual = 0
            self.mostrar_pantalla_actual()
        return pantalla
    
    def agregar_pantalla(self, pantalla):
        """Agrega una pantalla ya creada al gestor."""
        self.pantallas.append(pantalla)
        if self.indice_actual == -1:
            self.indice_actual = 0  # Activar la primera pantalla automáticamente
        print(f"[GestorPantallas] Pantalla '{pantalla.nombre}' agregada.")

    def mostrar_pantalla_actual(self):
        if 0 <= self.indice_actual < len(self.pantallas):
            pantalla = self.pantallas[self.indice_actual]
            self.ventana.content = pantalla.mostrar()
        print(f"[GestorPantallas] Mostrando pantalla: '{pantalla.nombre}'.")

    def ir_a(self, nombre):
        pantalla_actual = self.pantallas[self.indice_actual] 
            # Salva datos de la pantalla actual si corresponde
        if pantalla_actual and hasattr(pantalla_actual, "salva_datos"):
            pantalla_actual.salva_datos()
        for i, p in enumerate(self.pantallas):
            if p.nombre == nombre:
                if self.indice_actual != -1:
                    self.historial.append(self.indice_actual) # guardo la pantalla desde la que vengo
                self.indice_actual = i

                # Carga datos en la nueva pantalla si corresponde
                pantalla_actual = self.pantallas[self.indice_actual] 
                if hasattr(pantalla_actual, "carga_datos"):
                    pantalla_actual.carga_datos()
                self.mostrar_pantalla_actual()

                return
        print(f"[GestorPantallas] Pantalla '{nombre}' no encontrada.")

    # vuelve a la pantalla anterior, de la que venía
    def volver(self):
        if self.historial:
            self.indice_actual = self.historial.pop()
            self.mostrar_pantalla_actual()
        else:
            print("[GestorPantallas] No hay historial para volver.")

    def siguiente(self):
        if self.indice_actual < len(self.pantallas) - 1:
            self.indice_actual += 1
            self.mostrar_pantalla_actual()

    def anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_pantalla_actual()

    def liberar_pantalla(self, nombre):
        for i, p in enumerate(self.pantallas):
            if p.nombre == nombre:
                self.pantallas.pop(i)
                # Ajustar el índice si era la pantalla actual
                if i == self.indice_actual:
                    self.indice_actual = max(0, self.indice_actual - 1)
                    self.mostrar_pantalla_actual()
                return
        print(f"[GestorPantallas] No se puede liberar '{nombre}': no existe.")

    def resumen(self):
        return [p.nombre for p in self.pantallas]
