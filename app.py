"""
Aikido Training Application
Autor: Juan Carlos Nájar Compán
Version: 1.0.0
Fecha: 8 de junio de 2025
"""
# --- MONKEY PATCH PARA ANDROID/PYTHON 3.10+ (collections.Mapping, MutableMapping, Sequence) ---
import collections
import collections.abc
import sys
if sys.version_info >= (3, 10):
    if not hasattr(collections, 'Mapping'):
        collections.Mapping = collections.abc.Mapping
    if not hasattr(collections, 'MutableMapping'):
        collections.MutableMapping = collections.abc.MutableMapping
    if not hasattr(collections, 'Sequence'):
        collections.Sequence = collections.abc.Sequence
# --- FIN MONKEY PATCH ---
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, LEFT, CENTER

from .config import DEBUG
from .gestor_contextos import *
from .gestor_pantallas import *
from .gestor_iconos import GestorIconos
from .pantallas import *
from .gestores_app import GestoresApp
from .gestor_ontología import GestorOntologia, Actividades, Contextos, Alumnos
from .gestor_experto import GestorExperto
from .contextos import *
from .gestor_recomendaciones import GestorRecomendaciones
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
           
        # Configurar los gestores de la aplicación
        GestoresApp.set_pantallas(self.gestor_pantallas)
        GestoresApp.set_contextos(self.gestor_contextos)
        GestoresApp.set_ontologia(self.gestor_ontología)
        GestoresApp.set_sistema_experto(GestorExperto())


        # VERIFICAR EL FUNCIONAMIENTO DEL SISTEMA EXPERTO DE RECOMENDACIONES
        # self.verificar_sistema_Experto()

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
        pantalla_rcm_detalles = PantallaRcmDetalles("rcm_detalles")
        pantalla_rcm_datos = PantallaRcmDatos("rcm_datos")
        pantalla_rcm_filtros_1 = PantallaRcmFiltros_1("rcm_filtros_1")
        pantalla_rcm_filtros_2 = PantallaRcmFiltros_2("rcm_filtros_2")
        pantalla_rcm_actividades_1 = PantallaRcmActividades_1("rcm_actividades_1")
        pantalla_rcm_actividades_2 = PantallaRcmActividades_2("rcm_actividades_2")
        pantalla_rcm_datos_alta = PantallaRcmDatos_alta("rcm_datos_alta")
        pantalla_rcm_filtros_1_alta = PantallaRcmFiltros_1_alta("rcm_filtros_1_alta")
        pantalla_rcm_filtros_2_alta = PantallaRcmFiltros_2_alta("rcm_filtros_2_alta")

        self.gestor_pantallas.agregar_pantalla(pantalla_inicio)
        self.gestor_pantallas.agregar_pantalla(pantalla_grupo)
        self.gestor_pantallas.agregar_pantalla(pantalla_alumnos)
        self.gestor_pantallas.agregar_pantalla(pantalla_actividades)
        self.gestor_pantallas.agregar_pantalla(pantalla_problemas)
        self.gestor_pantallas.agregar_pantalla(pantalla_recomendaciones)
        self.gestor_pantallas.agregar_pantalla(pantalla_ficha_grupo)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_detalles)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_datos)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_filtros_1)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_filtros_2)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_actividades_1)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_actividades_2)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_datos_alta)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_filtros_1_alta)
        self.gestor_pantallas.agregar_pantalla(pantalla_rcm_filtros_2_alta)

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
            ContextoRecomendaciones("recomendaciones", 
                     EstadoContexto.INACTIVO),
            Contexto("ficha_grupo", 
                     EstadoContexto.INACTIVO),
            ContextoActividadRecomendada("actividad_recomendada",
               EstadoContexto.INACTIVO),
            ContextoRecomendaciones_alta("recomendaciones_alta", 
                     EstadoContexto.INACTIVO),                            
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
        # INDICO  FUNDAMENTO: "fundamentos_físicos"
        criterios_caso1 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": [],
            "objetivos": []
    }

        # CASO 2
        # INDICO  OBJETIVOS
        criterios_caso2 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": ["obj_mejorar_desplazamientos_rodillas_postura"]
    }
        # CASO 3
        # INDICO  MODALIDADES
        criterios_caso3 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": ["actividad_juego"],
            "objetivos": []
    }
        # CASO 4
        # FILTRO VARIOS CAMPOS
        criterios_caso4 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": ["actividad_individual"],
            "objetivos": ["obj_desarrollar_fuerza_explosiva"]
    }
        # CASO 5
        # GRUPO SIN ALUMNOS
        criterios_caso5 = {
            "grupo": "grupo_D",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
       # CASO 6
        # GRUPO CON ALUMNOS
        criterios_caso6 = {
            "grupo": "grupo_C",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": [],
            "objetivos": []
    }

        # CASO 7
        # GRUPO CON ALUMNOS, ALGUNOS SELECCIONADOS
        criterios_caso7 = {
            "grupo": "grupo_C",
            "alumnos": ["alumno_7","alumno_9"], 
            "contextos_entrada": [],
            "fundamentos": ["fundamentos_físicos"],
            "modalidades": [],
            "objetivos": []
    }
        # CASO 8
        # SIN GRUPO, ALGUNOS ALUMNOS SELECCIONADOS
        criterios_caso8 = {
            "grupo": "",
            "alumnos": ["alumno_07","alumno_09"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
        # CASO 9
        # SIN GRUPO, SIN ALUMNOS SELECCIONADOS
        criterios_caso9 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
       # CASO 10
        # ALUMNOS SELECCIONADOS CON MISMO CONTEXTO
        criterios_caso10 = {
            "grupo": "",
            "alumnos": ["alumno_11","alumno_12"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
 
         # CASO 11
        # GRUPO HETEROGÉNEO, ALUMNOS CON DISTINTOS CONTEXTOS
        criterios_caso11 = {
            "grupo": "",
            "alumnos": ["alumno_01","alumno_02","alumno_03"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
        # CASO 14
        # contexto inferido, Actividad recomendable para un género (mujer, por ejemplo)
        criterios_caso14 = {
            "grupo": "",
            "alumnos": ["alumno_03","alumno_04"], 
            "contextos_entrada": ["género_mujer"],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
        # CASO 15
        # alumnos con varios contextos funcionales
        criterios_caso15 = {
            "grupo": "",
            "alumnos": ["alumno_02"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
           # CASO 16
        # alumnos con varios contextos funcionales
        criterios_caso16 = {
            "grupo": "",
            "alumnos": ["alumno_13"], 
            "contextos_entrada": [],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
    }
                  # CASO 17
        # actividad beneficiosa para un contexto específico
        criterios_caso17 = {
            "grupo": "",
            "alumnos": [], 
            "contextos_entrada": ["género_mujer"],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
        }
                         # CASO 20
        # no hay actividades que cumplan las condiciones
        criterios_caso20 = {
            "grupo": "grupo_D",
            "alumnos": [], 
            "contextos_entrada": ["género_mujer"],
            "fundamentos": [],
            "modalidades": [],
            "objetivos": []
        }
        self.caso_prueba("CASO 14", criterios_caso14)

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
        
        gr = GestorRecomendaciones(self.gestor_ontología.ontologia,sistema_experto)
        datos = {"descripcion": titulo, "evaluacion": "defectuosa", "fecha_creacion":"fecha", 
               "fecha_evaluacion":"fecha", "fecha_modificacion":"fecha",
              "motivo":"mis motivos tendré", "observaciones":"observo mucho"}
        nc = gr.nueva_recomendacion(datos, criterios, recomendaciones)
        recomendaciones_leidas = gr.leer_recomendación(nc.name)
        if DEBUG:
            print("Recomendaciones leídas: ", recomendaciones_leidas)
        self.gestor_ontología.guardar()


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
