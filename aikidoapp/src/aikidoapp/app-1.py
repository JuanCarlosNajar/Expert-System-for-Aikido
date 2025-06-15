"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, LEFT, CENTER
import owlready2
from .custom_widgets import IconTextButton
from .gestor_contextos import EstadoContexto, Contexto
from .gestor_pantallas import GestorPantallas, Pantalla

class AikidoOWL():
    def __init__(self,nombre_owl):
        self.owl = nombre_owl
        ruta_iri = f"file://{self.owl.resolve().as_posix()}"
        self.onto = owlready2.get_ontology(ruta_iri).load()

        self.clases = self.onto.clases
        self.Grupos = next((sc for sc in self.clases.subclasses() if sc.name == "grupo"), None)
  
    def getGrupos(self):
        """
        Obtiene todos los grupos de la ontología.
        """

        if self.Grupos:
            grupos = [inst.name for inst in self.Grupos.instances()]
        else:
            grupos = []
        return grupos
 
class AikidoTraining(toga.App):
    def startup(self):
        # carga la ontología de Aikido
        archivo_owl = self.paths.app / "resources" / "aikido.owx"
        self.ontologia = AikidoOWL(archivo_owl)

        grupos = self.ontologia.getGrupos()
        print("Grupos de Aikido:", grupos)

        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
                # Contenido principal (puede estar vacío)


        main_box = toga.Box()
        main_box.style.update(background_color="#282828")
        main_box.style.update(direction=COLUMN, padding=10, flex=1)

        titulo = toga.Label("Inicio", style=Pack(color="yellow", font_size=20, text_align=CENTER, padding_top=20, padding_bottom=20))
        cuerpo = toga.Box()
        pie = toga.Box()


        """"
        cuerpo.add(toga.Button("Grupos",icon=icono,
                               style=Pack(
                    # --- Cambiar el ancho y alto ---
                    width=120,  # Ancho en píxeles
                    height=50,  # Alto en píxeles

                    # --- Cambiar el color de fondo ---
                    background_color="#343434",
                    color="#FFFFFF",  # Color del texto
                    )))
        
        """


    # En tu build()
        icon_path=self.paths.app/ "icons/grupos.png"
        boton = IconTextButton(icon_path, "Grupos", on_press=self.pulsado)
        cuerpo.add(boton)
        cuerpo.add(toga.Button("Alumnos"))
        cuerpo.add(toga.Button("Actividades"))
        cuerpo.add(toga.Button("Problemas"))
        cuerpo.add(toga.Button("Recomendaciones"))

        main_box.add(titulo)
        main_box.add(cuerpo)
        # main_box.add(pie)

               # Crear comandos y agruparlos para la menubar
        cmd_salir = toga.Command(
            self.salir,
            text="Salir",
            tooltip="Cerrar la aplicación",
            group=toga.Group("Archivo")  # Aparecerá como un menú 'Archivo'
        )

        cmd_ayuda = toga.Command(
            self.mostrar_ayuda,
            text="Acerca de",
            tooltip="Mostrar información de ayuda",
            group=toga.Group("Ayuda")
        )

        # Añadir los comandos al menú de la aplicación
        self.commands.add(cmd_salir)
        self.commands.add(cmd_ayuda)

        self.borraGrupoComados(toga.Group.FILE)  # Elimina comandos del grupo FILE
        self.borraGrupoComados(toga.Group.HELP)  # Elimina comandos del grupo HELP

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def pulsado(widget):
        print("¡Botón personalizado pulsado!")

    def borraGrupoComados(self, group):
        """Elimina todos los comandos de un grupo específico."""
        commands_to_remove = []
        for cmd in list(self.commands):
            if isinstance(cmd, toga.Command) and cmd.group == group:
                commands_to_remove.append(cmd)
        for cmd in commands_to_remove:
            self.commands.remove(cmd)

    def salir(self, widget):
        self.exit()

    def mostrar_ayuda(self, widget):
        self.main_window.info_dialog("Ayuda", "Esta es una app de ejemplo con menubar.")



def main():
    return AikidoTraining("Aikido Training", "org.beeware.aikidoapp",icon="icons/AikidoApp.png")
