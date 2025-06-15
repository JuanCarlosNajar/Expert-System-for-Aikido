# GESTOR SISTEMA EXPERTO
# gestor_experto.py

from .gestores_app import GestoresApp
from experta import *


class ImpactoContextual(Fact):
    funcion = Field(str)

class Actividad(Fact):
    nombre = Field(str)
    funciones_usadas = Field(list)
    tipo = Field(str)
    fundamentos = Field(list)

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

    def obtener_contextos_de_alumno(alumno):
        contextos = []
        if hasattr(alumno, "tiene_edad"):
            edad = alumno.tiene_edad[0]
            if edad <= 8:
                contextos.append("edad_6a8")
            elif edad <= 10:
                contextos.append("edad_9a10")
            else:
                contextos.append("edad_11a12")
        if hasattr(alumno, "tiene_género"):
            contextos.append(alumno.tiene_género[0].name)
        return contextos

    # 3. Obtener funciones afectadas por los contextos
    def funciones_afectadas(onto, contextos):
        funciones = set()
        for imp in onto.Impacto_por_edad.instances():
            if imp.rango_edad and imp.rango_edad.name in contextos:
                funciones.update([f.name for f in imp.funcion_afectada])
        for imp in onto.Impacto_por_genero.instances():
            if imp.genero and imp.genero.name in contextos:
                funciones.update([f.name for f in imp.funcion_afectada])
        return funciones
    
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
    
    @Rule(ImpactoContextual(funcion=MATCH.f),
        Actividad(nombre=MATCH.nombre,
                    funciones_usadas=MATCH.funcs,
                    tipo=MATCH.tipo,
                    fundamentos=MATCH.funds),
        TEST(lambda f, funcs: f in funcs),
        TEST(lambda tipo, self: self.criterios.get("tipo_actividad") is None or tipo in self.criterios["tipo_actividad"]),
        TEST(lambda funds, self: self.criterios.get("fundamentos") is None or any(f in funds for f in self.criterios["fundamentos"])))
    def recomendar(self, nombre):
        self.recomendadas.append(nombre)

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
                                fundamentos["fundamentos_fisicos","fundamentos_valor"],
                                tipo="individual",))