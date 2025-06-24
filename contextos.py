from .gestor_contextos import Contexto
from .gestor_ontología import GestorOntologia
from .gestores_app import GestoresApp

class ContextoGrupo(Contexto):
    def inicializar(self):
        super().inicializar()
        grupos = self.get_grupos()
        self.agregar_objeto(grupos)
        
    def get_grupos(self):
        return GestoresApp.ontologia().get_instancias_de_clase("Grupos")
