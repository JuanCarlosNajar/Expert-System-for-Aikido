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
from .gestor_ontología import GestorOntologia, Actividades, Contextos, Alumnos
from .gestor_experto import GestorExperto
from .contextos import ContextoGrupo
from collections import defaultdict
     
 
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

        actividades = Actividades(self.gestor_ontología.ontologia)
        fundamentos = actividades.fundamentos("carreras_con_arrastre")
        print("ACTIVIDAD ","carrera_con_arrastre")
        for f in fundamentos:
            print("fundamento: ", f.name)                     

        alumnos = Alumnos(self.gestor_ontología.ontologia)
        alumnos_grupo = alumnos.alumnos_grupo("grupo_A")
        print("ALUMNOS DE: grupo_A:")
        for a in alumnos_grupo:
            print(a)

        contextos = alumnos.contextos("alumno_02")
        print("CONTEXTOS DEL alumno_02:")
        for c in contextos:
            print(c)
        # Configurar los gestores de la aplicación
        GestoresApp.set_pantallas(self.gestor_pantallas)
        GestoresApp.set_contextos(self.gestor_contextos)
        GestoresApp.set_ontologia(self.gestor_ontología)

        # VERIFICAR EL FUNCIONAMIENTO DEL SISTEMA EXPERTO DE RECOMENDACIONES
        self.verificar_sistema_Experto()

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
        self.gestor_contextos=GestorContextos(self.contextos)

    def borraGrupoComados(self, group):
        """Elimina todos los comandos de un grupo específico."""
        commands_to_remove = []
        for cmd in list(self.commands):
            if isinstance(cmd, toga.Command) and cmd.group == group:
                commands_to_remove.append(cmd)
        for cmd in commands_to_remove:
            self.commands.remove(cmd)

    # VERIFICAMOS EL FUNCIONAMIENTO DEL SISTEMA EXPERTO
    def verificar_sistema_Experto(self):
        # CASO 1
        # SOLO INDICO GRUPO
        criterios_caso1 = {
            "grupo": "grupo_A",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
        """
        criterios_caso1 = {
            "grupo": "grupo_A",
            "alumnos": ["alumno_01", "alumno_02"], 
            "contextos_entrada": ["edad_6a8", "género_hombre", "género_mujer"],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": ["actividad_individual", "actividad_grupal"],
            "objetivos": ["obj_desarrollar_fuerza_explosiva","obj_mejorar_resistencia_muscular"]
    }
        """
     #   self.caso_prueba("CASO 1", criterios_caso1)
        # CASO 2
        # INDICO ALUMNO alumno_01
        criterios_caso2 = {
            "grupo": "",
            "alumnos": ["alumno_01"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
      #  self.caso_prueba("CASO 2", criterios_caso2)
        
        # CASO 3
        # INDICO ALUMNO alumno_01, FUNDAMENTO: "fundamentos_físicos"
        criterios_caso3 = {
            "grupo": "",
            "alumnos": ["alumno_01"], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": [],
            "objetivos": []
    }
       # self.caso_prueba("CASO 3", criterios_caso3)

        # CASO 4
        # INDICO ALUMNOs alumno_01 y alumno_02, FUNDAMENTO: "fundamentos_físicos"
        criterios_caso4 = {
            "grupo": "",
            "alumnos": ["alumno_01","alumno_02"], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": [],
            "objetivos": []
    }        
        # self.caso_prueba("CASO 4", criterios_caso4)
        # CASO 5
        # INDICO ALUMNOs alumno_01 y alumno_02, FUNDAMENTO: "fundamentos_técnicos"
        # MODALIDAD "actividad_individual"
        criterios_caso5 = {
            "grupo": "",
            "alumnos": ["alumno_01","alumno_02"], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_técnicos","fundamentos_valores"],
            "modalidades": [],
            "objetivos": []
    }
        self.caso_prueba("CASO 5", criterios_caso5)
        
    def caso_prueba(self, titulo, criterios):
        # IMPRIMO CRITERIOS

        # EVALUO EL CASO
        sistema_experto = GestorExperto()
        sistema_experto.iniciar(criterios)
        sistema_experto.evaluar()
        recomendaciones = sistema_experto.recomendaciones()

        # IMPRIMO RESULTADOS
        print("Caso de prueba: ", titulo)
        print("Grupo: ", criterios["grupo"])
        print("Alumnos: ", criterios["alumnos"])
        print("Contextos: ", criterios["contextos_entrada"])
        print("Fundamentos: ", criterios["fundamentos"])
        print("Objetivos: ", criterios["objetivos"])
        print("Modalidades: ", criterios["modalidades"])

        print("RECOMENDACIONES")
        for r in self.reestructura_recomendaciones(recomendaciones):
            print(r)
    
    def reestructura_recomendaciones(self, recomendaciones):
        agrupado = defaultdict(lambda: defaultdict(list))

        for actividad, contexto, alumnos in recomendaciones:
            agrupado[actividad][contexto].extend(alumnos)

        resultado = []
        for actividad, contextos in agrupado.items():
            actividad_entry = [actividad]
            for contexto, alumnos in contextos.items():
                actividad_entry.append([contexto, list(set(alumnos))])  # elimina duplicados si los hay
            resultado.append(actividad_entry)
        return resultado
def main():
    return AikidoTraining("Aikido Training", "org.beeware.aikidoapp",icon="icons/AikidoApp.png")
