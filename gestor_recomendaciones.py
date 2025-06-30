# gestor_recomendaciones.py
"""
Nombre: GestorRecomendaciones
Fecha creación: 27/06/2025
Versión: 1.0
Descripción: Gestiona las recomendaciones: crearlas, guardarlas, consultarlas, etc.
"""
from .config import DEBUG
from .gestor_experto import GestorExperto
from .gestor_ontología import Alumnos, Contextos, Actividades, Grupos, Fundamentos, Objetivos
from uuid import uuid4
import datetime

class Actividades_recomendadas:
    def __init__(self, ontologia):
        self.actividades_recomendadas = ontologia.Actividades_recomendadas
        self.ontologia = ontologia
        self.actual = None

    # Devuelve la instancia de una actividad recomendada, None si no la encuentra
    # y actualiza la actividad recomendada actual
    def buscar(self, id):
        for arc in self.actividades_recomendadas.instances():
            if arc.name == id:
                self.actual = arc
                return arc
        self.actual = None
        return self.actual
    
    # Crea una nueva actividad recomendada con un identificador único
    def  crear(self):
        id = "arc_" + str(uuid4())
        if not self.buscar(id):
            self.actual = self.actividades_recomendadas(id)
            return self.actual
        return None
    
    # Elimina la entidad con el id proporcionado
    # Si no se proporciona id, elimina la entidad actual
    def borrar(self, id=None):
        borrado = False
        if id:
            if self.buscar(id):
                self.actual.destroy()
                self.actual = None
                borrado = True
            borrado=False
        else:
            if self.actual:
                self.actual.destroy()
                self.actual = None
                borrado = True
        return borrado

    def actividad(self, actividad=None):
        if self.actual:
            if actividad:
                onto_actividades = Actividades(self.ontologia)
                a = onto_actividades.actividad(actividad)
                if a:
                    self.actual.arc_tiene_actividad = [a]
            return self.actual.arc_tiene_actividad
        return None
    
    def recomendacion(self, recomendacion=None):
        if self.actual:
            if recomendacion:
                self.actual.arc_tiene_recomendación = [recomendacion]
            return self.actual.arc_tiene_recomendación
        return None

    def alumnos(self, alumnos=None):
        if self.actual:
            if alumnos:
                onto_alumnos = Alumnos(self.ontologia)
                lista_alumnos = []
                for alumno in alumnos:
                    a = onto_alumnos.buscar(alumno)
                    if a:
                        lista_alumnos.append(a)
                self.actual.arc_tiene_alumno = lista_alumnos
            return lista_alumnos
        return None
    
    def contexto(self, contexto=None):
        if self.actual:
            if contexto:
                onto_contextos = Contextos(self.ontologia)
                c = onto_contextos.buscar(contexto) # busca el contexto en la ontología
                if c:
                    self.actual.arc_tiene_contexto = [c] # asigna el contexto a la actividad recomendada               
            return self.actual
        return None

class Recomendaciones:
    def __init__(self,ontologia):
        self.recomendaciones = ontologia.Recomendaciones_realizadas
        self.ontologia = ontologia
        self.actual =  None

    # Devuelve la instancia de una recomendación, None si no la encuentra
    # y actualiza la recomendación actual
    def buscar(self, id):
        for r in self.recomendaciones.instances():
            if r.name == id:
                self.actual = r
                return r
        self.actual = None
        return self.actual

    # Crea una nueva recomendación con un identificador único
    # si ya existe devuelve None
    def crear(self):
        id = "rcm_" + str(uuid4())

        if not self.buscar(id):
            self.actual = self.ontologia.Recomendaciones_realizadas(id)
            return self.actual
        return None
    
    # Borra las actividades recomendadas asociadas a la recomendación actual
    def borrar_actividades(self):
        if self.actual:
            actividades_recomendadas = Actividades_recomendadas(self.ontologia)
            for arc in self.actual.rcm_tiene_recomendaciones.instances():
                actividades_recomendadas.borrar(arc.name)
            return True
        return False

    # Elimina la entidad con el id proporcionado
    def  borrar(self, id=None):
        borrado = False
        if id:
            if self.buscar(id):
                if self.borrar_actividades():
                    self.actual.destroy()
                    self.actual = None
                    borrado = True
        else:
            if self.actual:
                self.actual.destroy()
                self.actual = None
                borrado = True
        return borrado
    # Si se proporciona una descripción la actualiza
    # si no devuelve la descripción actual
    def descripcion(self, descripcion=None):
        if self.actual:
            if descripcion:
                self.actual.rcm_tiene_descripción = [descripcion]        
            return self.actual.rcm_tiene_descripción
        return None
    
    # Si se proporciona una evaluación la actualiza
    # si no devuelve la evaluación actual
    def evaluacion(self, evaluacion=None):
        if self.actual:
            if evaluacion:
                self.actual.rcm_tiene_evaluación = [evaluacion]
            return self.actual.rcm_tiene_evaluación
        return None
    
    # Si se proporciona una fecha de creación la actualiza
    # si no devuelve la fecha de creación actual
    def fecha_creacion(self, fecha=None):
        if self.actual:
            if fecha:
                self.actual.rcm_tiene_fecha_creación = [fecha]
            return self.actual.rcm_tiene_fecha_creación
        return None

    def fecha_evaluacion(self, fecha=None):
        if self.actual:
            if fecha:
                self.actual.rcm_tiene_fecha_evaluación = [fecha]
            return self.actual.rcm_tiene_fecha_evaluación
        return None
    
    def fecha_modificacion(self, fecha=None):
        if self.actual:
            if fecha:
                self.actual.rcm_tiene_fecha_modificación = [fecha]
            return self.actual.rcm_tiene_fecha_modificación
        return None
    
    def motivo(self, motivo=None):
        if self.actual:
            if motivo:
                self.actual.rcm_tiene_motivo = [motivo]
            return self.actual.rcm_tiene_motivo
        return None
 
    def observaciones(self, observaciones=None):
        if self.actual:
            if observaciones:
                self.actual.rcm_tiene_observaciones = [observaciones]
            return self.actual.rcm_tiene_observaciones
        return None
    
    
    # rcm_tiene_grupo es una data property que indica el grupo al que se le hace la recomendación
    def grupo(self, grupo=None):
        if self.actual:
            if grupo:
                self.actual.rcm_tiene_grupo = grupo 
            return self.actual.rcm_tiene_grupo
        return None
    
    # Registra todos los alumnos a los que se les hace la recomendación
    # alumnos = ["alumno1","alumno2", ...]
    def alumnos(self, alumnos=None):
        if self.actual:
            if alumnos:
                onto_alumnos = self.ontologia.Alumnos()
                lista_alumnos = []
                for alumno in alumnos:
                    a = onto_alumnos.buscar(alumno)
                    if a:
                        lista_alumnos.append(a)
                self.actual.rcm_tiene_alumno = lista_alumnos
            return [alumno.name for alumno in self.actual.rcm_tiene_alumno.instances()]
        return None
    
    # Si se proporcionan los metadatos de la recomendación los actualiza
    # si no devuelve los metadatos actuales
    def datos(self, datos=None):
        if self.actual:
            if datos:
                self.descripcion(datos.get("descripcion", None))
                self.evaluacion(datos.get("evaluacion", None))
                self.fecha_creacion(datos.get("fecha_creacion", None))
                self.fecha_evaluacion(datos.get("fecha_evaluacion", None))
                self.fecha_modificacion(datos.get("fecha_modificacion", None))
                self.motivo(datos.get("motivo", None))
                self.observaciones(datos.get("observaciones", None))
            return {
                "descripcion": self.descripcion(),
                "evaluacion": self.evaluacion(),
                "fecha_creacion": self.fecha_creacion(),
                "fecha_evaluacion": self.fecha_evaluacion(),
                "fecha_modificacion": self.fecha_modificacion(),
                "motivo": self.motivo(),
                "observaciones": self.observaciones()
            }
        return None
    
    # Si se proporcionan los criterios de la recomendación los actualiza
    # si no devuelve los criterios actuales
    def criterios(self, criterios=None):
        if self.actual:
            if criterios:   # si se proporcionan los criterios los actualiza

                #GRUPO
                self.grupo(criterios.get("grupo", None)) # pongo el grupo de la recomendación

                #ALUMNOS
                onto_alumnos = Alumnos(self.ontologia)
                lista_alumnos = []
                for alumno in criterios.get("alumnos", []):
                    a = onto_alumnos.buscar(alumno)
                    if a:
                        lista_alumnos.append(a)
                self.actual.rcm_tiene_alumno = lista_alumnos # registro los alumnos de la recomendación

                # CONTEXTOS
                # Registro los contextos de la recomendación
                onto_contextos = Contextos(self.ontologia)
                lista_contextos = []
                for contexto in criterios.get("contextos_entrada", []):
                    c = onto_contextos.buscar(contexto)
                    if c:
                        lista_contextos.append(c)
                self.actual.rcm_tiene_contexto = lista_contextos

                # FUNDAMENTOS
                # Registro los fundamentos de la recomendación
                onto_fundamentos = Fundamentos(self.ontologia)
                lista_fundamentos = []
                for fundamento in criterios.get("fundamentos", []):
                    f = onto_fundamentos.buscar(fundamento)
                    if f:
                        lista_fundamentos.append(f)
                self.actual.rcm_tiene_fundamento = lista_fundamentos

                # OBJETIVOS
                # Registro los objetivos de la recomendación
                onto_objetivos = Objetivos(self.ontologia)
                lista_objetivos = []
                for objetivo in criterios.get("objetivos", []):
                    o = onto_objetivos.buscar(objetivo)
                    if o:
                        lista_objetivos.append(o)
                self.actual.rcm_tiene_objetivo = lista_objetivos

                # MODALIDADES
                # Registro las modalidades de la recomendación
                onto_modalidades = self.ontologia.Modalidad_actividades
                lista_modalidades = []
                for modalidad in criterios.get("modalidades", []):
                    m = onto_modalidades.buscar(modalidad)
                    if m:
                        lista_modalidades.append(m)
                self.actual.rcm_tiene_modalidad = lista_modalidades
                return criterios
            else: # si no se proporcionan los criterios devuelve los actuales              
                return {
                "grupo": self.grupo(),
                "alumnos": [alumno.name for alumno in self.actual.rcm_tiene_alumno.instances()],
                "contextos": [contexto.name for contexto in self.actual.rcm_tiene_contexto.instances()],
                "fundamentos": [fundamento.name for fundamento in self.actual.rcm_tiene_fundamento.instances()],
                "objetivos": [objetivo.name for objetivo in self.actual.rcm_tiene_objetivo.instances()],
                "modalidades": [modalidad.name for modalidad in self.actual.rcm_tiene_modalidad.instances()]
                }
        return None
    
    def set_recomendaciones(self, recomendaciones):
        if self.actual:
            devolver = True
            actividades_recomendadas_items = []
            nueva_arc = Actividades_recomendadas(self.ontologia)
            for rec in recomendaciones:
                actividad_nombre = rec[0]
                contexto_nombre = rec[1]
                alumnos = rec[2]
                nueva = nueva_arc.crear()
                if nueva:
                    nueva_arc.actividad(actividad_nombre)  # enlaza la actividad recomendada
                    nueva_arc.recomendacion(self.actual)  # enlaza la recomendación con la actividad recomendada
                    nueva_arc.contexto(contexto_nombre)  # enlaza el contexto con la actividad recomendada
                    nueva_arc.alumnos(alumnos)  # enlaza los alumnos con la actividad recomendada
                    actividades_recomendadas_items.append(nueva)                                       
        else:
            devolver = False
        return devolver

    def get_recomendaciones(self):
        """
        Devuelve una lista de recomendaciones en la forma:
        [[actividad, contexto, [alumno1, alumno2, ...]], ...]
        leyendo de la ontología todas las actividades recomendadas asociadas a la recomendación actual
        mediante la object property arc_tiene_recomendacion.
        self.actual tiene que contener la entidad o intancia de Recomendaciones_realizadas que
        se quiere consultar.
        """
        resultado = []
        if self.actual:
            # Buscar todas las instancias de Actividades_recomendadas que apunten a esta recomendación
            for arc in self.ontologia.Actividades_recomendadas.instances():
                # arc_tiene_recomendacion es una lista de recomendaciones asociadas a esta actividad recomendada
                if hasattr(arc, "arc_tiene_recomendación") and self.actual in arc.arc_tiene_recomendación:
                    # Obtener nombre de la actividad recomendada
                    actividad = arc.arc_tiene_actividad[0].name if hasattr(arc, "arc_tiene_actividad") and arc.arc_tiene_actividad else None
                    # Obtener contexto
                    contexto = arc.arc_tiene_contexto[0].name if hasattr(arc, "arc_tiene_contexto") and arc.arc_tiene_contexto else None
                    # Obtener alumnos
                    alumnos = [alumno.name for alumno in getattr(arc, "arc_tiene_alumno", [])]
                    resultado.append([actividad, contexto, alumnos])
        return resultado

class GestorRecomendaciones:
    ontologia = None
    sistema_experto = None
    recomendaciones = None
    actividades_recomendadas = None

    # Se ejecuta al iniciar crear un objeto de esta clase
    # ontologia = la ontología, no el gestor de ontologia
    # sistema_experto = GestorExperto
    def __init__(self, ontologia = None, sistema_experto =  None):
        if ontologia:
            self.ontologia = ontologia
            self.recomendaciones = Recomendaciones(ontologia)
            self.actividades_recomendadas = Actividades_recomendadas(ontologia)
        self.sistema_experto = (sistema_experto if sistema_experto else None) 
        
    # Si especifica una ontología la enlaza con ella
    # en todo caso devuelve la ontología con la que está enlazada
    def ontologia(self, ontologia = None):
        if ontologia:
            self.ontologia = ontologia
            self.recomendaciones = Recomendaciones(ontologia)
            self.actividades_recomendadas = Actividades_recomendadas(ontologia)
        return self.ontologia
    
    # Si especifica un sistema experto lo enlaza con él
    # en todo caso devuelve el sistema experto con el que está enlazada
    def sistema_experto(self, sistema_experto = None):
        if sistema_experto:
            self.sistema_experto = sistema_experto
        return self.sistema_experto  
    
    # Método para genera recomendaciones en base a unos criterios
    def generar_recomendaciones(self, criterios):
        if not self.sistema_experto:
            self.sistema_Experto = GestorExperto()
        self.sistema_experto.iniciar(criterios)
        self.sistema_experto.evaluar()
        return self.sistema_experto.recomendaciones()
        
    # Hace un commit de todos los cambios realizados en la ontología
    def salvar(self):
        if self.ontologia:
           # self.ontologia.save()
            return False

    # Método para crear una nueva recomendación en la ontología
    # Recomendación: [datos, criterios, recomendaciones]
    # datos = {"descripción": "", "evaluación": "", "fecha_creación":"fecha", 
    #           "fecha_evaluación":"fecha", "fecha_modificación":"fecha",
    #          "motivo":"motivo", "observaciones":"observaciones"}
    # criterios = [grupo, alumnos, contextos, fundamentos, objetivos, modalidades]
    # recomendaciones = [[actividad, contexto, alumnos]]
    # tanto la entidad recomendación como la de recomendaciones necesitan de un identificador único
    # recomendación --> rcm_tiene_recomendaciones --> actividad_recomendada  
    # actividad_recomendada --> es_recomendación --> recomendación
    def nueva_recomendacion(self, datos, criterios, recomendaciones):
        nueva_rcm = self.recomendaciones.crear() # creo una recomendación con un identificador único
        if nueva_rcm:
            # guardo los metadatos de la recomendación
            self.recomendaciones.datos(datos) # guardo los datos de la recomendación
            self.recomendaciones.criterios(criterios) # guardo los criterios de la recomendación
            self.recomendaciones.set_recomendaciones(recomendaciones) # guardo las recomendaciones de la recomendación
            # guardo la recomendación en la ontología
        self.salvar()         # hago un commit de los cambios realizados en la ontología
        return nueva_rcm
    
    # Método para leer una recomendación desde la ontología
    # id = identificador de la recomendación en la ontología
    def leer_recomendación(self, id):
        if DEBUG:
            print("Leyendo recomendación con id:", id)
        recomendacion = []
        rcm = self.recomendaciones.buscar(id)
        if rcm:
            recomendacion = self.recomendaciones.get_recomendaciones()  # obtiene las recomendaciones asociadas a la recomendación
        return recomendacion

     

  