"""
Aikido Training Application
Autor: Juan Carlos Nájar Compán
Version: 1.0.0
Fecha: 8 de junio de 2025
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, LEFT, CENTER

from .gestor_contextos import EstadoContexto, Contexto, GestorContextos
from .gestor_pantallas import GestorPantallas, Pantalla
from .gestor_iconos import GestorIconos
from .pantallas import PantallaInicio, PantallaGrupo, PantallaAlumnos, PantallaActividades
from .pantallas import PantallaProblemas, PantallaRecomendaciones, PantallaFichaGrupo
from .gestores_app import GestoresApp
from .gestor_ontología import GestorOntologia
from .contextos import ContextoGrupo

     
 
class AikidoTraining(toga.App):
    def startup(self):
        # Crear la ventana principal
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.gestor_iconos = GestorIconos(self.paths.app)
        GestoresApp.set_iconos(self.gestor_iconos)

        # Inicializar el gestor de pantallas
        self.gestor_pantallas = GestorPantallas(self.main_window)
        # Inicializar el gestor de contextos
        self.gestor_contextos = None
        self.crearContextos()

        # Inicializa la ontología
        archivo_owl = self.paths.app / "resources" / "aikido.owl"
        self.gestor_ontología = GestorOntologia(str(archivo_owl.resolve()))

        # Configurar los gestores de la aplicación
        GestoresApp.set_pantallas(self.gestor_pantallas)
        GestoresApp.set_contextos(self.gestor_contextos)
        GestoresApp.set_ontologia(self.gestor_ontología)

        self.gestor_contextos.ir_a_contexto("inicio")
        self.gestor_pantallas.ir_a("inicio")

        self.borraGrupoComados(toga.Group.FILE)  # Elimina comandos del grupo FILE
        self.borraGrupoComados(toga.Group.HELP)  # Elimina comandos del grupo HELP

        # Mostrar la ventana principal
        self.main_window.show()

    def crearContextos(self):
        print("[INFO] Creando contextos...")
        # Crear los contextos de entrenamiento
        pantalla_inicio =  PantallaInicio("inicio")
        pantalla_grupo =    PantallaGrupo("grupos")
        pantalla_alumnos = PantallaAlumnos("alumnos")
        pantalla_actividades = PantallaActividades("actividades")
        pantalla_problemas = PantallaProblemas("problemas")
        pantalla_recomendaciones = PantallaRecomendaciones("recomendaciones")
        pantalla_ficha_grupo = PantallaFichaGrupo("ficha_grupo")    

        self.gestor_pantallas.agregar_pantalla(pantalla_inicio)
        self.gestor_pantallas.agregar_pantalla(pantalla_grupo)
        self.gestor_pantallas.agregar_pantalla(pantalla_alumnos)
        self.gestor_pantallas.agregar_pantalla(pantalla_actividades)
        self.gestor_pantallas.agregar_pantalla(pantalla_problemas)
        self.gestor_pantallas.agregar_pantalla(pantalla_recomendaciones)
        self.gestor_pantallas.agregar_pantalla(pantalla_ficha_grupo)


        self.contextos = [
            Contexto("inicio", 
                    pantalla_inicio,
                    EstadoContexto.ACTIVO),
            ContextoGrupo("grupos", 
                     EstadoContexto.INACTIVO),
            Contexto("alumnos", 
                     EstadoContexto.INACTIVO),
            Contexto("actividades", 
                     EstadoContexto.INACTIVO),
            Contexto("problemas", 
                     EstadoContexto.INACTIVO),
            Contexto("recomendaciones", 
                     EstadoContexto.INACTIVO),
            Contexto("ficha_grupo", 
                     EstadoContexto.INACTIVO)
        ]
        # Inicializar el gestor de contextos
        self.gestor_contextos = GestorContextos(self.contextos)

    def borraGrupoComados(self, group):
        """Elimina todos los comandos de un grupo específico."""
        commands_to_remove = []
        for cmd in list(self.commands):
            if isinstance(cmd, toga.Command) and cmd.group == group:
                commands_to_remove.append(cmd)
        for cmd in commands_to_remove:
            self.commands.remove(cmd)



def main():
    return AikidoTraining("Aikido Training", "org.beeware.aikidoapp",icon="icons/AikidoApp.png")
