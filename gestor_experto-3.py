# GESTOR SISTEMA EXPERTO
# gestor_experto.py

from .gestores_app import GestoresApp
from experta import *
from .gestor_ontología import Actividades, Alumnos, Grupos, Contextos
from collections.abc import * # Para facilitar la agrupación
from collections import defaultdict

#
# DEFINICIONES DE HECHOS
#

# Representa cada actividad a examinar
class ActividadCandidata(Fact):
    nombre = Field(str)


"""
criterios_usuario = {
    "grupo": "GrupoA",
    "alumnos": ["Lucas", "Ana"],
    "contextos": [ "edad_6a8", "género_hombre","género_mujer"]
    "fundamentos": ["fundamentos fisicos", "fundamentos técnicos"],
    "objetivos": ["objetivo1", "objetivo2"],
    "modalidades": ["grupal", "parejas"]
}
"""
# Representa los criterios para realizar las recomendaciones 
class CriteriosUsuario(Fact):
    grupo = Field(str, default=None)
    alumnos = Field(list, default=[])
    contextos_entrada = Field(list, default=[]) # ["edad_6a8", "género_hombre", ...]
    fundamentos = Field(list, default=[])
    modalidades = Field(list, default=[])
    objetivos = Field(list, default=[])

# Representa un contexto asociado a un alumno
class ContextoAlumno(Fact):
    alumno = Field(str)
    contexto = Field(str) 
    funciones_afectadas = Field(list, default=[])

# Representa las recomendaciones generadas
class Recomendacion(Fact):
    actividad = Field(str)
    contexto = Field(str)
    alumno = Field(str)
    razon = Field(str, default="") # Puede ser "Beneficiosa" o "Neutra"

class SistemaExperto(KnowledgeEngine):
    criterios = None
    resultados = []

    def __init__(self):
        super().__init__()
        # manejo de la ontología
        self.gestor_ontologia = GestoresApp.ontologia()
        self.ontologia = self.gestor_ontologia.get_ontologia()
        self.alumnos = Alumnos(self.ontologia)
        self.contextos = Contextos(self.ontologia)
        self.grupos = Grupos(self.ontologia)
        self.actividades = Actividades(self.ontologia)

        self.resultados = []
        self.init_criterios()
        self.init_resultados()

    """
    # lo he quitado por redundante 

    # Inicia el motor con los criterios del usuario 
    @DefFacts()
    def _initial_facts(self):
        yield CriteriosUsuario(**self.criterios) 
    """

    @Rule( 
        AS.actividad_criterios << CriteriosUsuario(
            modalidades=MATCH.modalidades & P(lambda x: x != []), # Verifica si modalidad existe y no está vacía 
            fundamentos=MATCH.fundamentos & P(lambda x: x != []), # Verifica si fundamentos existe y no está vacía 
            objetivos=MATCH.objetivos & P(lambda x: x != []) # Verifica si objetivos existe y no está vacía
        ),
        salience = 20
    )         
    def filtrar_actividades_por_criterios(self, actividad_criterios, modalidades, fundamentos, objetivos):
        """
            Aplica filtros de modalidad, objetivos y fundamentos de forma acumulativa (intersección).
        """
        print("FILTRAR ACTIVIDADES POR CRITERIOS")

        actividades_candidatas_set = set() # Usar set para intersecciones eficientes

        # Primer filtro: Modalidad 
        
    
        if modalidades: # 
            # Obtener actividades que tienen *al menos una* de las modalidades especificadas
            actividades_filtro = set()
            for m in modalidades: # 
                actividades_filtro.update(
                    self.obtener_actividades_por_modalidad(m)
                    ) 
            actividades_candidatas_set = actividades_filtro
        
        # Segundo filtro: Objetivos 
        if objetivos: # 
            actividades_filtro = set()
            for o in objetivos: # 
                actividades_filtro.update(
                    self.obtener_actividades_por_objetivo(o)
                    )  
            if actividades_candidatas_set: # Si ya había filtros previos
                actividades_candidatas_set = actividades_candidatas_set.intersection(actividades_filtro)
            else: # Si es el primer filtro
                actividades_candidatas_set = actividades_filtro

        # Tercer filtro: Fundamentos 
        if fundamentos: # 
            actividades_filtro = set()
            for f in fundamentos: # 
                actividades_filtro.update(
                    self.obtener_actividades_por_fundamento(f)
                    ) 
            if actividades_candidatas_set: # Si ya había filtros previos
                actividades_candidatas_set = actividades_candidatas_set.intersection(actividades_filtro)
            else: # Si es el primer filtro
                actividades_candidatas_set = actividades_filtro
        
        # Si no se especificaron filtros iniciales, se toman todas las actividades 
        if not (modalidades or objetivos or fundamentos):
            actividades_candidatas_set = set(self.obtener_todas_las_actividades()) 

        if actividades_candidatas_set:
            for actividad in actividades_candidatas_set:
                self.declare(ActividadCandidata(nombre = actividad))
            self.declare(Fact(actividades_iniciales_filtradas=True))
        else:
            self.declare(Fact(no_actividades_candidatas=True)) # Marcador para el caso de no resultados
    
    @Rule(
        AS.criterios_entrada << CriteriosUsuario(),
        Fact(actividades_iniciales_filtradas=True), # Esperar a que el filtrado inicial haya terminado
        NOT(Fact(contextos_y_alumnos_procesados=True)), # Evita que se dispare múltiples veces
        salience=15 # Prioridad media-alta, después del filtrado de actividades
    )
    def procesar_alumnos_y_contextos(self, criterios_entrada):
        """   
        Obtiene los alumnos y sus contextos, agrupándolos para el procesamiento posterior.
        """
        print("PROCESAR ALUMNOS Y CONTEXTOS")
        alumnos_a_procesar = []
        if criterios_entrada["alumnos"]: # Si se ha especificado el criterio alumnos
            # Asume que los alumnos en criterios_usuario.alumnos son nombres
            for nombre_alumno in criterios_entrada["alumnos"]: 
                if  self.alumnos.buscar(nombre_alumno): 
                    alumnos_a_procesar.append(nombre_alumno)
        elif criterios_entrada["grupo"]: # Si no se ha especificado alumnos, pero sí grupo
            alumnos_a_procesar = self.alumnos.alumnos_grupo(criterios_entrada["grupo"]) 

        # Agrupar contextos por alumno o procesar contextos directos si no hay alumnos 
        if alumnos_a_procesar: # 
            for alumno in alumnos_a_procesar: # 
                contextos_alumno = self.obtener_contextos_de_alumno(alumno) 
                for ctxt in contextos_alumno: 
                    if criterios_entrada["contextos_entrada"]: 
                        # La estructura de criterios_entrada.contextos_entrada es [Contexto1, Contexto2, ...]
                        
                    # si ese especifican contextos en los criterios, solo tengo en cuenta
                    # los contextos de los alumnos que están en estos criterios
                        if ctxt in criterios_entrada["contextos_entrada"]:
                            self.declare(ContextoAlumno(
                                alumno=alumno,
                                contexto=ctxt,
                                funciones_afectadas=self.obtener_funciones_afectadas(ctxt)
                            ))
                    else: # Si no se especificaron contextos en la entrada, se consideran todos los del alumno 
                        self.declare(ContextoAlumno(alumno=alumno, contexto=ctxt,
                                                   funciones_afectadas=self.obtener_funciones_afectadas(ctxt))) # 
        # Si no hay alumnos o grupo especificados, y tampoco hay contextos_input
        # O si hay contextos_input pero no se especifican alumnos
        # -> no se declararán ContextoAlumno hechos.
        # Esto hará que las reglas que dependen de ContextoAlumno no se disparen,
        # y la regla de "sin contextos" se encargará de pasar todas las ActividadesCandidatas.
        self.declare(Fact(contextos_y_alumnos_procesados=True)) # Marcador de que esta fase ha terminado

    @Rule(
        AS.act_candidata_fact << ActividadCandidata(),
        AS.ctxt_alumno_fact << ContextoAlumno(), # Para cada combinación de actividad candidata y contexto/alumno
        Fact(contextos_y_alumnos_procesados=True), # Esperar a que los contextos hayan sido procesados
        salience=10 # Prioridad para la evaluación de beneficios/contraindicaciones
    )
    def evaluar_actividad_para_contexto_y_alumno(self, act_candidata_fact, ctxt_alumno_fact):
        """  
        Evalúa si una ActividadCandidata es beneficiosa y no contraindicada para un contexto/alumno específico.
        Declara Recomendacion si cumple.
        """
        # print(f"Regla: evaluar_actividad_para_contexto_y_alumno para {act_candidata_fact.actividad_iri} y {ctxt_alumno_fact.alumno_iri} ({ctxt_alumno_fact.contexto_iri})") # Depuración

        print("EVALUAR ACTIVIDAD PARA CONTEXTO Y ALUMNO")

        actividad = act_candidata_fact["nombre"]
        contexto = ctxt_alumno_fact["contexto"]
        alumno = ctxt_alumno_fact["alumno"]
        
        if not actividad or not contexto or not alumno:
            return

        # 1. Comprobar contraindicaciones para este contexto/alumno
        funciones_perjudicadas_en_contexto = self.obtener_funciones_afectadas(contexto)
        funciones_afectadas_por_contexto_en_alumno = ctxt_alumno_fact["funciones_afectadas"]

        if set(funciones_perjudicadas_en_contexto).intersection(set(funciones_afectadas_por_contexto_en_alumno)):
            # print(f"- {actividad_instance.name} CONTRAINDICADA para {alumno_instance.name} por {contexto_instance.name}")
            return # Si está contraindicada para *este* par, no la declaramos como recomendación para este par.

        # 2. Comprobar beneficios para este contexto/alumno
        funciones_beneficiadas_por_actividad = self.obtener_funciones_beneficiadas(actividad)

        es_beneficiosa = False
        if funciones_beneficiadas_por_actividad and \
           set(funciones_beneficiadas_por_actividad).intersection(set(funciones_afectadas_por_contexto_en_alumno)):
            es_beneficiosa = True
        
        # 3. Lógica de declaración de Recomendacion
        if es_beneficiosa:
            self.declare(Recomendacion(
                actividad=actividad, contexto=contexto, alumno=alumno,
                razon="Beneficiosa"
            ))
        elif not funciones_beneficiadas_por_actividad: # y ya sabemos que no está contraindicada
            # Si no tiene beneficios explícitos y no está contraindicada, se considera "neutra/recomendable"
            self.declare(Recomendacion(
                actividad=actividad, contexto=contexto, alumno=alumno,
                razon="Neutra y no contraindicada"
            ))
        # Si no es ni beneficiosa ni neutra (es decir, no hay intersección en beneficios y no es contraindicada),
        # no declaramos una recomendación para este par actividad/contexto/alumno.
    @Rule(
        Fact(actividades_iniciales_filtradas=True),
        Fact(contextos_y_alumnos_procesados=True),
        NOT(ContextoAlumno(contexto=W())), # Esta regla se dispara si NO se declararon ContextoAlumno hechos
        # (es decir, no se especificaron alumnos/grupo, o los contextos del alumno no pasaron el filtro de entrada)
        # Y tampoco hay un hecho de "no_actividades_candidatas"
        NOT(Fact(no_actividades_candidatas=True)),
        salience=9 # Se ejecuta si la regla de evaluación con contextos no tiene hechos para dispararse
    )
    def pasar_actividades_si_no_hay_contextos_validos(self):
        """      
        Declara todas las ActividadesCandidatas como recomendaciones si no hay ContextoAlumno hechos
        para realizar un filtrado adicional (ej., no se especificaron alumnos o contextos).
        """
        print("Regla: pasar_actividades_si_no_hay_contextos_validos (No se aplican filtros de beneficio/contraindicación por contexto).") # Depuración
        for act_cand_fact in self.facts.values():
            # Si no se declararon ContextoAlumno, significa que el filtro de beneficios/contraindicaciones no se aplica.
            # Por lo tanto, todas las actividades que pasaron el filtro inicial son recomendables.
            # Se asocia a un contexto genérico "todos" y un "alumno" genérico si es necesario para el formato.
            if isinstance(fact,ActividadCandidata):
                self.declare(Recomendacion(
                    actividad=act_cand_fact.nombre,
                    contexto = "Contexto_General", # Contexto genérico
                    alumno = "Alumno_General",   # Alumno genérico
                    razon="General (sin criterios de contexto/alumno específicos)"
                ))

    @Rule(
        Fact(actividades_iniciales_filtradas=True), # Asegurarse de que el proceso principal ha pasado
        Fact(contextos_y_alumnos_procesados=True),  # Asegurarse de que los contextos se han procesado
        salience=-1 # Se ejecuta al final de todo
    )
    def recopilar_resultados(self):
        """   
        Recopila las recomendaciones detalladas y las imprime en el formato deseado.
        """
        print("\n--- RECOPILANDO RECOMENDACIONES FINALES ---") # Depuración
        # Estructura para agrupar: { (actividad, contexto): [alumno_1, alumno_2, ...] }
        agrupacion_recomendaciones = defaultdict(list)

        for rec_fact in self.facts.values():
            if isinstance(rec_fact,Recomendacion):
                key = (rec_fact["actividad"], rec_fact["contexto"])
                if rec_fact["alumno"] not in agrupacion_recomendaciones[key]: # Evitar duplicados de alumnos
                    agrupacion_recomendaciones[key].append(rec_fact["alumno"])
        
        recomendaciones_formateadas = []
        for (act, ctxt), alumnos in agrupacion_recomendaciones.items():
            actividad_nombre = act
            contexto_nombre = ctxt
            alumnos_nombres = sorted([a for a in alumnos])
            
            recomendaciones_formateadas.append([actividad_nombre, contexto_nombre, alumnos_nombres])

        # Ordenar las recomendaciones para una salida consistente
        recomendaciones_formateadas.sort(key=lambda x: (x[0], x[1], x[2]))

        if recomendaciones_formateadas:
            print("\n--- RECOMENDACIONES DETALLADAS ---")
            for rec in recomendaciones_formateadas:
                print(rec)
        else:
            print("No se encontraron actividades recomendadas para los criterios y contextos proporcionados.")

        self.resultados = recomendaciones_formateadas
        if self.resultados:
            print("AQUI SI TIENE VALORES")
        else:
            print("AQUI TAMPOCO TIENE VALORES")
     # Obtener los contextos del alumno
    def obtener_contextos_de_alumno(self,alumno):
        return self.alumnos.contextos(alumno)
    
    # Filtrar actividades por fundamento
    def obtener_actividades_por_fundamento(self,fundamento):
        return self.actividades.actividades_fundamento(fundamento)
    
    # Filtrar actividades por modalidad
    def obtener_actividades_por_modalidad(self,modalidad):
        return self.actividades.actividades_modalidad(modalidad)
        
    # Filtrar actividades por objetivo
    def obtener_actividades_por_objetivo(self, objetivo):
        return self.actividades.actividades_objetivo(objetivo)
           
    # Obtener todas las actividades
    def obtener_todas_las_actividades(self):
        return [a.name for a in self.actividades.instances()]
    
    # Obtener funciones afectadas por un contexto
    def obtener_funciones_afectadas(self, contexto):
        return self.contextos.funciones_afectadas(contexto)
    
    # Obtener funciones beneficiadas por una actividad
    def obtener_funciones_beneficiadas(self, actividad):
        return self.actividades.funciones_beneficiadas(actividad)
    
    # Obtener todas las actividades
    def obtener_todas_las_actividades(self):
        return self.actividades.get_actividades()
     
    # devuelve los resultados de evaluar las reglas y los hechos
    def get_resultados(self):
        if not self.resultados:
            print("EN GET_RESULTADOS ESTÁ VACIA")
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

    # inicializa los criterios que tienen que cumplir las actividades
    def init_criterios(self):
        self.criterios = {"grupo": None,
                    "alumnos": [],
                    "contextos_entrada": [],
                    "fundamentos": [],
                    "modalidades": [],
                    "objetivos": [],
                    }
        return self.criterios
    

"""
Forma de uso:
    miSistemaExperto = GestorExperto()
    miSistemaExperto.iniciar(criterios)
    miSistemaExperto.evaluar()
    recomendaciones = miSistemaExperto.recomendaciones()
"""
class GestorExperto:
    _motor_sistema = None

    def iniciar(self, criterios):
        self._motor_sistema = SistemaExperto()
        self._motor_sistema.set_criterios(criterios)
        
        
    def evaluar(self):
        self._motor_sistema.reset()
        self.declara()
        print("DEPURANDO EL MOTOR:")
        for f in self._motor_sistema.facts.values():
            print(repr(f))
        self._motor_sistema.run()

    def recomendaciones(self):
        return self._motor_sistema.get_resultados()
   
    def declara(self):
        criterios = self._motor_sistema.criterios    
        self._motor_sistema.declare(CriteriosUsuario(**criterios))
        print(criterios)