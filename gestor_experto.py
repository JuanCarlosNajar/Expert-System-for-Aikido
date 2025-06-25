# GESTOR SISTEMA EXPERTO
# gestor_experto.py
# Autor: Juan Carlos Nájar Compán
# Fecha última modificación: 24/06/2025
# Institución: Universidad Internacional de La Rioja
# TRABAJO FIN DE GRADO 2025

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

# Representa los criterios para realizar las recomendaciones 
class CriteriosUsuario(Fact):
    grupo = Field(str, default=None)            # "grupo_A"
    alumnos = Field(list, default=[])           # ["Lucas", "Ana"]
    contextos_entrada = Field(list, default=[]) # ["edad_6a8", "género_hombre", ...]
    fundamentos = Field(list, default=[])       # ["fundamentos_físicos"]
    modalidades = Field(list, default=[])       # ["actividad_grupal"]
    objetivos = Field(list, default=[])         # ["obj_mejorar_fuerza_superior"]

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

# Representa un alumno junto a los contextos que le afectan
class AlumnoConContextos(Fact):
    alumno = Field(str)
    # Lista de tuplas: (contexto1, [funcion_afectada1, ...])
    contextos_detallados = Field(list, default=[])


# IMPLEMENTACIÓN DEL MOTOR DE INFERENCIA DEL SISTEMA EXPERTO

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


    # PRIMERA REGLA
    # FILTRAR ACTIVIDADES POR CRITERIOS (MODALIDAD, OBJETIVOS, FUNDAMENTOS)
    # SOLO SE EXAMINARAN LAS ACTIVIDADES QUE CUMPLAN ESTOS CRITERIOS

    @Rule( 
        AS.actividad_criterios << CriteriosUsuario(
            modalidades=MATCH.modalidades & P(lambda x: x != []), # Verifica si modalidad existe y no está vacía 
            fundamentos=MATCH.fundamentos & P(lambda x: x != []), # Verifica si fundamentos existe y no está vacía 
            objetivos=MATCH.objetivos & P(lambda x: x != []) # Verifica si objetivos existe y no está vacía
        ),
        salience = 20   # le indico la prioridad de la regla
    )         
    def filtrar_actividades_por_criterios(self, actividad_criterios, modalidades, fundamentos, objetivos):
        """
            Aplica filtros de modalidad, objetivos y fundamentos de forma acumulativa (intersección).
        """

        actividades_candidatas_set = set() # Usar set para intersecciones eficientes

        # Primer filtro: Modalidad 
        
        if modalidades:
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
                self.declare(ActividadCandidata(nombre = actividad))    # marco la actividad para evaluarla
            self.declare(Fact(actividades_iniciales_filtradas=True))    # indico que he terminado de filtrar
        else:
            self.declare(Fact(no_actividades_candidatas=True)) # Marcador para el caso de no resultados

    # SEGUNDA REGLA
    # OBTENGO LOS ALUMNOS PARA LOS QUE VAMOS A HACER LAS RECOMENDACIONES Y SUS CONTEXTOS    
    @Rule(
        AS.criterios_entrada << CriteriosUsuario(),
        Fact(actividades_iniciales_filtradas=True),
        NOT(Fact(alumnos_con_contextos_procesados=True)),
        salience=15 # le indico la prioridad de la regla
    )
    def procesar_alumnos_y_contextos_agrupados(self, criterios_entrada):
        """
            Obtiene los alumnos y agrupa TODOS sus contextos válidos en un solo hecho AlumnoConContextos.
        """
        alumnos_a_procesar = []

        if criterios_entrada["alumnos"]:
            for alumno in criterios_entrada["alumnos"]:
                alumnos_a_procesar.append(alumno)
        elif criterios_entrada["grupo"]:
            alumnos_a_procesar = self.obtener_alumnos_grupo(criterios_entrada["grupo"])
        elif criterios_entrada["contextos_entrada"]: # no se ha especificado ni grupo ni alumnos pero si contextos
            alumnos_a_procesar = [a.name for a in self.todos_los_alumnos()]

        if alumnos_a_procesar:
            algun_alumno_con_contexto = False
            for alumno in alumnos_a_procesar:
                contextos_del_alumno = self.obtener_contextos_de_alumno(alumno)
                contextos_detallados_para_alumno = []
                for ctxt in contextos_del_alumno:
                    if criterios_entrada["contextos_entrada"]:
                        if ctxt in criterios_entrada["contextos_entrada"]:
                            funciones_afectadas = [f for f in self.obtener_funciones_afectadas(ctxt)]
                            contextos_detallados_para_alumno.append([ctxt, funciones_afectadas])
                    else:
                        funciones_afectadas = [f for f in self.obtener_funciones_afectadas(ctxt)]
                        contextos_detallados_para_alumno.append([ctxt, funciones_afectadas])
                
                if contextos_detallados_para_alumno:
                    algun_alumno_con_contexto = True
                    self.declare(AlumnoConContextos(
                        alumno=alumno,
                        contextos_detallados=contextos_detallados_para_alumno
                    ))
            if algun_alumno_con_contexto:
                self.declare(Fact(alumnos_con_contextos_procesados=True))
            else:
                # Si no hay ningún alumno con contextos válidos, NO declares alumnos_con_contextos_procesados
                # Así no se dispara la regla general
                self.declare(Fact(no_actividades_candidatas=True))
        else:
            self.declare(Fact(no_actividades_candidatas=True)) # indico que he terminado de procesar a los alumnos

    # TERCERA REGLA
    # REGLA CLAVE: Evalúa la actividad para un ALUMNO
    # SI LA ACTIVIDAD TIENE ALGUNA CONTRAINDICACIÓN PARA ALGUNOS DE LOS CONTEXTOS DEL ALUMNO, LA DESCARTAMOS
    # SI NO ES DESCARTADA, COMPROBAMOS SI APORTA BENEFICIOS PARA ALGUNO DE LOS CONTEXTOS DEL ALUMNO
    @Rule(
        AS.act_candidata_fact << ActividadCandidata(),
        AS.alumno_ctxt_fact << AlumnoConContextos(),
        Fact(alumnos_con_contextos_procesados=True),
        salience=10 # marca la prioridad de la regla
    )
    def evaluar_actividad_para_alumno(self, act_candidata_fact, alumno_ctxt_fact):
        """
        Evalúa si una ActividadCandidata es recomendable para un alumno,
        siguiendo la lógica: "primero contraindicaciones, luego beneficios/neutralidad".
        """
        print(f"Evaluando: Actividad '{act_candidata_fact['nombre']}' para Alumno '{alumno_ctxt_fact["alumno"]}'")

        actividad = act_candidata_fact["nombre"]
        alumno = alumno_ctxt_fact["alumno"]
        
        if not actividad or not alumno:
            return

        # Esto nos da los CONTEXTOS que contraindican la actividad
        contextos_que_contraindican_actividad = self.obtener_contraindicaciones(actividad)
        
        funciones_beneficiadas = {f for f in self.obtener_funciones_beneficiadas(actividad)}

        # 1. PASO: COMPROBAR SI LA ACTIVIDAD ESTÁ CONTRAINDICADA POR CUALQUIER CONTEXTO DEL ALUMNO
           
        for ctxt_alumno, funciones_afectadas_alumno in alumno_ctxt_fact["contextos_detallados"]:
            contexto_alumno = ctxt_alumno
            if not contexto_alumno: 
                continue

            # Verificar si este contexto del alumno es uno de los que contraindican la actividad
            if contexto_alumno in contextos_que_contraindican_actividad:
                print(f"  - Actividad '{actividad}' contraindicada para '{alumno}' por contexto '{contexto_alumno}'.")
                return

        # 2. PASO: EVALUAR BENEFICIOS Y NEUTRALIDAD (Solo si no está contraindicada globalmente)
        
        es_beneficiosa = False
        contexto_beneficiado = None # Para la salida, qué contexto específico la hizo beneficiosa

        for ctxt_alumno, funciones_afectadas_alumno in alumno_ctxt_fact["contextos_detallados"]:
            contexto_alumno = ctxt_alumno
            if not contexto_alumno: continue

            # "Si funciones_afectadas ESTÁN EN funciones_beneficiadas ENTONCES ACTIVIDAD ES RECOMENDABLE"
            if funciones_beneficiadas.intersection(set(funciones_afectadas_alumno)):
                es_beneficiosa = True
                contexto_beneficiado = ctxt_alumno # Registra el contexto que aporta el beneficio
                break # Encontramos un beneficio, podemos parar

        if es_beneficiosa:
            # "ACTIVIDAD ES RECOMENDABLE"
            self.declare(Recomendacion(
                actividad=actividad,
                contexto=contexto_beneficiado, # El contexto específico que la hizo beneficiosa
                alumno=alumno,
                razon="Beneficiosa"
            ))
            print(f"  --> {actividad} RECOMENDADA (Beneficiosa) para {alumno} por {contexto_beneficiado}.")
        else:
            #  "EN CASO CONTRARIO ACTIVIDAD NEUTRA"
            # Si no es beneficiosa (no hay intersección de funciones) y no está contraindicada, es neutra.
            # Se asocia a un contexto relevante del alumno o a un contexto general para el formato.
        
            contexto_para_neutra = alumno_ctxt_fact["contextos_detallados"][0][0] if alumno_ctxt_fact["contextos_detallados"] else "Contexto General"
            self.declare(Recomendacion(
                actividad=actividad,
                contexto=contexto_para_neutra,
                alumno=alumno,
                razon="Neutra y no contraindicada"
            ))
            print(f"  --> {actividad} RECOMENDADA (Neutra) para {alumno}.")

 
    # CUARTA REGLA
    # SI NO SE ESPECIFICARON ALUMNOS O LOS ALUMNOS NO TIENEN ASIGNADOS CONTEXTOS
    # ENTONCES TODAS LAS ACTIVIDADES SON VÁLIDAS
    @Rule(
        Fact(actividades_iniciales_filtradas=True),
        Fact(alumnos_con_contextos_procesados=True),
        NOT(AlumnoConContextos(alumno=W())), # Se dispara si no hay AlumnoConContextos hechos
        NOT(Fact(no_actividades_candidatas=True)),
        salience=9
    )
    def pasar_actividades_si_no_hay_alumnos_con_contextos_validos(self):
        """      
        Declara todas las ActividadesCandidatas como recomendaciones si no hay AlumnoConContextos hechos
        (ej., no se especificaron alumnos/grupo, o no se encontraron contextos válidos para ellos).
        En este caso, se asume que todas las actividades filtradas inicialmente son recomendables de forma general.
        """
        print("Regla: pasar_actividades_si_no_hay_alumnos_con_contextos_validos (No se aplican filtros de beneficio/contraindicación por alumno/contexto).")
        for act_cand_fact in list(self.facts.values()): # el list es para hacer una copia de facts.values
            if isinstance(act_cand_fact,ActividadCandidata):
                self.declare(Recomendacion(
                    actividad=act_cand_fact["nombre"],
                    contexto="Contexto_General",
                    alumno="Alumno_General",
                    razon="General (sin criterios de contexto/alumno específicos)"
                ))


    # QUINTA REGLA
    # REGLA FINAL, CUANDO YA SE HA TERMINADO DE FILTRAR Y EVALUAR LAS ACTIVIDADES
    @Rule(
        Fact(actividades_iniciales_filtradas=True), # Asegurarse de que el proceso principal ha pasado
        Fact(alumnos_con_contextos_procesados=True),  # Asegurarse de que los contextos se han procesado
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

    # obtener todos los alumnos
    def todos_los_alumnos(self):
        return self.alumnos.instances()
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
    
    # Obtener contraindicaciones de una actividad
    def obtener_contraindicaciones(self,actividad):
        return [f.name for f in self.actividades.contraindicaciones(actividad)]
    
    # Obtener todos los alumnos de un grupo
    def obtener_alumnos_grupo(self, grupo):
        return self.alumnos.alumnos_grupo(grupo)
    
    # Obtener todas las actividades
    def obtener_todas_las_actividades(self):
        return self.actividades.get_actividades()
     
    # devuelve los resultados de evaluar las reglas y los hechos
    def get_resultados(self):
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
        self._motor_sistema.run()

    def recomendaciones(self):
        return self._motor_sistema.get_resultados()
   
    def declara(self):
        criterios = self._motor_sistema.criterios    
        self._motor_sistema.declare(CriteriosUsuario(**criterios))
