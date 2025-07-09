from .gestor_contextos import Contexto
from .gestor_ontología import GestorOntologia
from .gestores_app import GestoresApp
from .gestor_recomendaciones import Recomendaciones, GestorRecomendaciones, Actividades_recomendadas
from .config import DEBUG

class ContextoGrupo(Contexto):
    def inicializar(self):
        super().inicializar()
        grupos = self.get_grupos()
        self.agregar_objeto(grupos)
        
    def get_grupos(self):
        return GestoresApp.ontologia().get_instancias_de_clase("Grupos")
    
class ContextoRecomendaciones(Contexto):
    def inicializar(self):
        super().inicializar()
        ontologia = GestoresApp.ontologia().get_ontologia()
        sistema_experto = GestoresApp.sistema_experto()
        gestor_recomendaciones = GestorRecomendaciones(ontologia,sistema_experto)
        self.agregar_objeto(gestor_recomendaciones)
        
    def get_recomendaciones(self):
        if DEBUG:
            print("Obteniendo recomendaciones del contexto...")
            print(type(self.objetos[0]))
        return self.objetos[0].get_instances() if self.objetos else None
    
class ContextoActividadRecomendada(Contexto):
    def inicializar(self):
        super().inicializar()
        actividad_recomendada = self.get_actividad_recomendada()
        self.agregar_objeto(actividad_recomendada)
        
    def get_actividad_recomendada(self):
        if DEBUG:
            print("GET ACTIVIDAD RECOMENDADA")
        gestor = GestoresApp.ontologia() # devuelve GestorOntologia
        ontologia = gestor.get_ontologia()  # devuelve la ontologia asociada al GestorOntologia
        return Actividades_recomendadas(ontologia) # devuelve un objeto de Actividad_Recomendada
    
class ContextoRecomendaciones_alta(Contexto):
    def inicializar(self):
        super().inicializar()
        ontologia = GestoresApp.ontologia().get_ontologia()
        sistema_experto = GestoresApp.sistema_experto()
        gestor_recomendaciones = GestorRecomendaciones(ontologia,sistema_experto)
        self.agregar_objeto(gestor_recomendaciones)
        self.agregar_objeto(gestor_recomendaciones.crear_datos_recomendacion())
        
    def get_recomendaciones(self):
        if DEBUG:
            print("Obteniendo recomendaciones del contexto...")
            print(type(self.objetos[0]))
        return self.objetos[0].get_instances() if self.objetos else None
