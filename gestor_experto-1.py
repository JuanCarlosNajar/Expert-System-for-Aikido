# GESTOR SISTEMA EXPERTO
# gestor_experto.py

from .gestores_app import GestoresApp
from experta import *


class Actividad(Fact):
    nombre = Field(str)
    grupo = Field(str)
    alumnos = Field(list)
    contextos = Field(list)
    fundamentos = Field(list)
    tipo = Field(str)

"""
criterios_usuario = {
    "grupo": "GrupoA",
    "alumnos": ["Lucas", "Ana"],
    "contextos": ["edad_6a8", "género_hombre"],
    "fundamentos": ["Autocontrol", "Respeto"],
    "tipo_actividad": ["grupal", "parejas"]
}
"""
class SistemaExperto(KnowledgeEngine):
    criterios = None
    def __init__(self):
        super().__init__()
        self.init_criterios()
        self.init_resultados()

    
    #EVALUAN LAS CONDICIONES DE LAS REGLAS

    # Evalua el grupo
    def eval_grupo(self, grupo):
        criterio= self.criterios.get("grupo")
        if criterio is None or criterio == []: #significa que da igual el grupo
            evaluacion = True
        else:
            evaluacion= (grupo == criterio)  # Evalua el grupo
        return evaluacion
    
    # Evalua los alumnos
    def eval_alumnos(self, alumnos):                               
        criterio = self.criterios.get("alumnos")
        if criterio is None or criterio == []: #significa que da igual el alumno
            evaluacion = True
        else:
            # Evalua si es alguno de los alumnos
            # HABRÍA QUE PENSAR SI UTILIZAMOS all() POR SI TIENEN QUE ESTAR TODOS LOS ALUMNOS 
            evaluacion = any(a in alumnos for a in criterio)  
        return evaluacion
    
    # Evalua los contextos: contexto_edad, contexto_género, etc.
    def eval_contexto(self, contextos):                           
        criterio = self.criterios.get("contexto")
        if criterio is None or criterio == []: #significa que dan igual los contextos
            evaluacion = True
        else:
            # Evalua si cumple con todos los contexto
            # HABRÍA QUE PENSAR SI UTILIZAMOS any() POR SI BASTA CON QUE ESTÉ ALGUNO DE ELLOS 
            evaluacion = all(a in contextos for a in criterio)  
        return evaluacion

    # Evalua los fundamentos: fundamentos_físicos, fundamentos_sociales_y_emocionales, etc.
    def eval_fundamentos(self, fundamentos):                        
        criterio = self.criterios.get("fundamentos")
        if criterio is None or criterio == []: #significa que dan igual los fundamentos
            evaluacion = True
        else:
            # Evalua si cumple con todos los contexto
            # HABRÍA QUE PENSAR SI UTILIZAMOS any() POR SI BASTA CON QUE ESTÉ ALGUNO DE ELLOS 
            evaluacion = all(a in fundamentos for a in criterio)  
        return evaluacion

    def eval_tipo(self, tipo_actividad):                 # Evalua los tipos de actividad: actividad_grupal, actividad_por_parejas, etc.
        criterio = self.criterios.get("tipo_actividad")
        if criterio is None or criterio == []: #significa que dan igual los fundamentos
            evaluacion = True
        else:
            # Evalua si cumple con alguno de los tipos de actividad
            evaluacion = (tipo_actividad in  criterio)  
        return evaluacion
    
    # devuelve los resultados de evaluar las reglas y los hechos
    def resultados(self):
        return self.resultados

    # inicializa los resultados
    def init_resultados(self):
        self.resultados =  []
        return self.resultados
    
    # Establece los criterios si se le pasa el parámetro, devuelve los criterios en cualquier caso
    def set_criterios(self, criterios):
        if not criterios is None:
            self.criterios = criterios
        return self.criterios

    # inicializa los criterios que tienen que cumplir las activiades
    def init_criterios(self):
        self.criterios = {"grupo": None,
                    "alumnos": None,
                    "contextos": None,
                    "fundamentos": None,
                    "tipo_actividad": None
                    }
        return self.criterios
    
    @Rule(Actividad(nombre=MATCH.nombre,
                    grupo=MATCH.grupo,
                    alumnos=MATCH.alumnos,
                    contextos=MATCH.contextos,
                    fundamentos=MATCH.fundamentos,
                    tipo=MATCH.tipo
                    ))
    def recomendar(self, nombre, grupo, alumnos, contextos, fundamentos, tipo):
     
        if self.criterios.get("grupo") and not self.eval_grupo(grupo):
            return 
        if self.criterios.get("alumnos") and not self.eval_alumnos(alumnos):
            return 
        if self.criterios.get("contextos") and not self.eval_contextos(contextos):
            return
        if self.criterios.get("fundamentos") and not self.eval_fundamentos(fundamentos):
            return
        if self.criterios.get("tipo_actividad") and not self.eval_tipo(tipo):
            return

        self.resultados.append(nombre)

class GestorExperto:
    _motor_sistema = None

    def iniciar(self, criterios):
        self._motor_sistema = SistemaExperto(
        self.motor_sistema.set_criterios(criterios)
        )
        
    def evaluar(self):
        self._motor_sistema.run()

    def get_resultados(self):
        return self._motor_sistema.resultados()
   
    def declara(self):    
        self._motor_sistema.declare(Actividad(  nombre="Estiramiento",grupo="GrupoA", 
                                              alumnos=["Juan","Pepe"], 
                                fundamentos=["fundamentos_fisicos","fundamentos_valor"],
                                tipo="individual",))