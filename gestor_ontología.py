# gestor_ontologia.py
"""
Nombre: GestorOntología
Fecha creación: 11/06/2025
Versión: 1.0
Descripción: A través de la librería Owlready2 gestionamos la ontología creada con Protégé en 
formato owl. Implementa el patrón Singleton para que se cree una única instancia del gestor
"""
from owlready2 import get_ontology, Thing
import itertools # importo herramientas de iteradores

"""
CREO LAS CLASES DE LAS ONTOLOGIAS
No podemos usar el método estándar de  owlready2 de class Actividades(onto.Actividades)
por que no tengo "onto" en el momento de la declaración y por que no coincide exactamente
con la declarada en la ontología
"""
# Clase para gestionar las Actividades
class Actividades:
    def __init__(self, ontologia):
        self.Actividades_fisicas = ontologia.Actividades_fisicas
        self.Actividades_tecnicas = ontologia.Actividades_técnicas
        self.Actividades_sociales_emocionales = ontologia.Actividades_sociales_emocionales
        self.Actividades_valores = ontologia.Actividades_valores

    # Crea un iterador único, uniendo los iteradores instances de los cuatro tipos de actividades
    def instances(self): 
        return itertools.chain(self.Actividades_fisicas.instances(),
                               self.Actividades_sociales_emocionales.instances(),
                               self.Actividades_tecnicas.instances(),
                               self.Actividades_valores.instances())


    # Devuelve una instancia de la "actividad" especificada
    def actividad(self, actividad):
        actividades = self.instances()
        for act in actividades:
            if act.name == actividad:
                return act   
        return None
    
    # Devuelve los objetivos de una actividad
    # Se ha sobrecargado el método, puedo llamarlo con el nombre de la actividad "actividad1"
    # o directamente con una instancia de Actividades
    def objetivos(self, actividad):
        objetivos = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # act_tiene_objetivo es una Object Property de Actividad
        if isinstance(act.act_tiene_objetivo,list): # compruebo si una lista o un solo elemento
            objetivos.extend(act.act_tiene_objetivo)
        elif act.act_tiene_objetivo: # compruebo que tenga al menos un elemento
            objetivos.append(act.act_tiene_objetivo)
        else:
            print("No se encontraron objetivos")
        return objetivos
    
    # Devuelve los fundamentos de una actividad
    # Se ha sobrecargado el método, puedo llamarlo con el nombre de la actividad "actividad1"
    # o directamente con una instancia de Actividades
    def fundamentos(self, actividad):
        fundamentos = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # act_tiene_fundamento es una Object Property de Actividad
        if isinstance(act.act_tiene_fundamento,list): # compruebo si una lista o un solo elemento
            fundamentos.extend(act.act_tiene_fundamento)
        elif act.act_tiene_fundamento: # compruebo que tenga al menos un elemento
            fundamentos.append(act.act_tiene_fundamento)
        else:
            print("No se encontraron fundamentos")
        return fundamentos  

    # Filtra las actividades por fundamento
    def actividades_fundamento(self, fundamento):
        actividades_filtro = []
        for actividad in self.instances():
            for f in self.fundamentos(actividad):
                if f.name == fundamento:
                    actividades_filtro.append(actividad.name)
        return list(set(actividades_filtro)) # elimino actividades repetidas
    
        # Filtra las actividades por objetivo
    def actividades_objetivo(self, objetivo):
        actividades_filtro = []
        for actividad in self.instances():
            for f in self.objetivos(actividad):
                if f.name == objetivo:
                    actividades_filtro.append(actividad.name)

        return list(set(actividades_filtro)) # elimino actividades repetidas
    # Devuelve las modalidades de una actividad
    # Se ha sobrecargado el método, puedo llamarlo con el nombre de la actividad "actividad1"
    # o directamente con una instancia de Actividades
    def modalidades(self, actividad):
        modalidades = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # act_tiene_fundamento es una Object Property de Actividad
        if isinstance(act.act_tiene_modalidad,list): # compruebo si una lista o un solo elemento
            modalidades.extend(act.act_tiene_modalidad)
        elif act.act_tiene_modalidad: # compruebo que tenga al menos un elemento
            modalidades.append(act.act_tiene_modalidad)
        else:
            print("No se encontraron modalidades")
        return modalidades  
    
    # Filtra las actividades por modalidad
    def actividades_modalidad(self, modalidad):
        actividades_filtro = []
        for actividad in self.instances():
            for m in self.modalidades(actividad):
                if m.name == modalidad:
                    actividades_filtro.append(actividad.name)
        return list(set(actividades_filtro)) # elimino actividades repetidas

    # Devuelve las funciones corporales beneficiadas por una actividad
    # Se ha sobrecargado el método, puedo llamarlo con el nombre de la actividad "actividad1"
    # o directamente con una instancia de Actividades
    def funciones_beneficiadas(self, actividad):
        funciones = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # act_tiene_beneficio es una Object Property de Actividad
        if isinstance(act.act_tiene_beneficio,list): # compruebo si una lista o un solo elemento
            funciones.extend(act.act_tiene_beneficio)
        elif act.act_tiene_beneficio: # compruebo que tenga al menos un elemento
            funciones.append(act.act_tiene_beneficio)
        else:
            print("No se encontraron beneficios")
        return funciones
    
    # Devuelve una lista con el nombre de todas las actividades
    def get_actividades(self):
        return [a.name for a in self.instances()]
    
    # Devuelve los contextos contraindicados para una actividad
    def contraindicaciones(self, actividad):
        contextos = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # act_tiene_contraindicación es una Object Property de Actividad
        if isinstance(act.act_tiene_contraindicación,list): # compruebo si una lista o un solo elemento
            contextos.extend(act.act_tiene_contraindicación)
        elif act.act_tiene_contraindicación: # compruebo que tenga al menos un elemento
            contextos.append(act.act_tiene_contraindicación)
        else:
            print("No se encontraron contraindicaciones")
        return contextos
    
# Clase para gestionar los Grupos
class Grupos:
    def __init__(self,ontologia):
        self.grupo = ontologia.Grupo

class Contextos:
    def __init__(self,ontologia):
        self.contexto = ontologia.Clasificaciones
        self.ontologia = ontologia

    # Es necesario inferir el contexto edad a partir de la edad del alumno
    # Contexto_edad es una clase de la ontología
    def contexto_edad(self, edad):
        contextos_edad = self.ontologia.Contexto_edad.instances()
        for contexto in contextos_edad:
            if contexto.edad_final[0] >= edad >=contexto.edad_inicial[0]:
                return contexto
        return None

    # Es necesario inferir el contexto género a partir del género del alumno
    # Contexto_género es una clase de la ontología
    def contexto_genero(self, genero):
        contextos_genero = self.ontologia.Contexto_género.instances()
        for contexto in contextos_genero:
            if contexto.name == genero:
                return contexto
        return None    
    
    # Devuelve la instancia del contexto, "contexto1", solicitado.
    # Clasificaciones es una clase de la ontologia
    def contexto(self, contexto):
        for instancia in self.ontologia.Clasificaciones.instances():
            if instancia.name == contexto:
                return instancia
        return None
    
    # Devuelve las funciones corporales afectadas por los contextos
    # contexto es una instancia de la clase Clasificaciones, es decir, de los contextos
    def funciones_afectadas(self, contexto):
    
        funciones_afectadas = []

        # ctx_tiene_impacto es una Object Property de Contextos (Clasificaciones)
        if contexto:
            if isinstance(contexto,str):
                ctx = self.contexto(contexto)
            else:
                ctx = contexto
            for impacto in ctx.ctx_tiene_impacto:
                # funcion es una Object Property de Impactos
                # La propiedad 'funcion' puede ser una lista o una sola instancia
                if isinstance(impacto.funcion, list):
                    funciones_afectadas.extend(impacto.funcion)
                elif impacto.funcion:
                    funciones_afectadas.append(impacto.funcion)
                else:
                    print("No se encontró el contexto")

            # Eliminar duplicados si es necesario
            funciones_afectadas = list(set(funciones_afectadas))

        return funciones_afectadas
    
# Clase para gestionar los alumnos
class Alumnos():
    def __init__(self,ontologia):
        self.alumnos = ontologia.Alumnos
        self.ontologia = ontologia

    # Devuelve la instancia de un alumno, None si no lo encuentra
    def buscar(self, alumno):
        for a in self.alumnos.instances():
            if a.name == alumno:
                return a
        return None
    
    # Devuelve los alumnos de un grupo dado
    def alumnos_grupo(self, grupo):
        alumnos = []
        if grupo:
            todos = self.alumnos.instances()
            for alumno in todos:
                for g in alumno.es_alumno_de:
                    if g.name == grupo:
                        alumnos.append(alumno.name)
        return alumnos

    # Devuelve los contextos inferidos de un alumno
    # el parámetro alumno es una instancia de la clase Alumnos de la ontología
    def contextos_inferidos(self, alumno):
        contextos = []
        gestor_contextos = Contextos(self.ontologia)
        contexto_edad = gestor_contextos.contexto_edad(alumno.tiene_edad[0]) # tiene_edad es una Data Property
        if contexto_edad:
            contextos.append(contexto_edad)
        contexto_genero = gestor_contextos.contexto_genero(alumno.tiene_género[0]) # tiene_género es un Data property
        if contexto_genero:
            contextos.append(contexto_genero)
        return [c.name for c in contextos]
    
    # Devuelve los contextos explícitos de un alumno
    # el parámetro alumno es una instancia de la clase Alumnos de la ontología
    def contextos_explicitos(self, alumno):
        contextos = []
        # tiene_contexto es una Object Property de Impactos
        # La propiedad 'tiene_contexto' puede ser una lista o una sola instancia
        if isinstance(alumno.tiene_contexto, list):
            contextos.extend(alumno.tiene_contexto)
        elif alumno.tiene_contexto:
            contextos.append(alumno.tiene_contexto)
        else:
            print("No se encontraron contextos")
        return [c.name for c in contextos]
    
    # Devuelve los contextos de un alumno, dado su nombre, los inferidos y los explícitos
    def contextos(self, alumno):
        contextos=[]
        instancia_alumno = next((a for a in self.alumnos.instances() if a.name == alumno), None) 
        if instancia_alumno:
            contextos.extend(self.contextos_inferidos(instancia_alumno))
            contextos.extend(self.contextos_explicitos(instancia_alumno))
        return contextos

class GestorOntologia:
    _instance = None

    # Implementa el patrón Singleton
    def __new__(cls, ruta_ontologia=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar(ruta_ontologia)
        return cls._instance

    # Inicializa y carga la ontología.
    # Este método solo se llama desde el constructor de la clase
    def _inicializar(self, ruta_ontologia):
        print("INICIALIZAR ONTOLOGIA")
        if hasattr(self, "_inicializado"):
            return
        if not ruta_ontologia:
            raise ValueError("Debes proporcionar una ruta a la ontología al inicializar por primera vez.")
        self.ruta = ruta_ontologia
        self.ontologia = get_ontology(self.ruta).load()
        self._inicializado = True
        print(f"[Ontología] Cargada desde: {self.ruta}")

    # Devuelve la ontología cargada
    def get_ontologia(self):
        return self.ontologia

    # Param:
    #       nombre: nombre de la clase en la ontología
    
    def get_clase(self, nombre):
        # return self.ontologia.search_one(iri="*" + nombre)
        return self.ontologia.search_one(iri="*" + nombre)

    # Param:
    #       nombre: nombre de la instancia a buscar en la ontología
    def get_individuo(self, nombre):
        return self.ontologia.search_one(iri="*" + nombre)

    def crear_individuo(self, clase_nombre, individuo_nombre):
        clase = self.get_clase(clase_nombre)
        if clase:
            nuevo = clase(individuo_nombre)
            print(f"[Ontología] Individuo '{individuo_nombre}' creado de la clase '{clase_nombre}'")
            return nuevo
        else:
            print(f"[ERROR] Clase '{clase_nombre}' no encontrada.")
            return None

    def eliminar_individuo(self, nombre):
        individuo = self.get_individuo(nombre)
        if individuo:
            individuo.destroy()
            print(f"[Ontología] Individuo '{nombre}' eliminado.")
        else:
            print(f"[ERROR] Individuo '{nombre}' no encontrado.")

    def get_propiedades_de_clase(self, clase_nombre):
        clase = self.get_clase(clase_nombre)
        if clase:
            propiedades = list(clase.get_class_properties())
            print(f"[Ontología] Propiedades de la clase '{clase_nombre}': {[p.name for p in propiedades]}")
            return propiedades
        else:
            print(f"[ERROR] Clase '{clase_nombre}' no encontrada.")
            return []

    def get_propiedades_de_individuo(self, nombre_individuo):
        individuo = self.get_individuo(nombre_individuo)
        if not individuo:
            print(f"[ERROR] Individuo '{nombre_individuo}' no encontrado.")
            return {}

        propiedades = {}
        for prop in self.ontologia.object_properties():
            valores = getattr(individuo, prop.name)
            if valores:
                propiedades[prop.name] = valores

        for prop in self.ontologia.data_properties():
            valores = getattr(individuo, prop.name)
            if valores:
                propiedades[prop.name] = valores

        print(f"[Ontología] Propiedades de '{nombre_individuo}': {list(propiedades.keys())}")
        return propiedades

    def get_instancias_de_clase(self, clase_nombre):
        clase = self.get_clase(clase_nombre)
        if clase:
            if clase.instances():
                instancias = list(clase.instances())
                print(f"[Ontología] Instancias de '{clase_nombre}': {[i.name for i in instancias]}")
                return instancias
            else:
                return None
        else:
            print(f"[ERROR] Clase '{clase_nombre}' no encontrada.")
            return []

    def guardar(self, ruta=None):
        ruta_destino = ruta if ruta else self.ruta
        self.ontologia.save(file=ruta_destino, format="rdfxml")
        print(f"[Ontología] Guardada en: {ruta_destino}")
