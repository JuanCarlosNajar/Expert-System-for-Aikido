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
        return itertools.chain(self.Actividades_fisicas,
                               self.Actividades_sociales_emocionales,
                               self.Actividades_tecnicas,
                               self.Actividades_valores)


    # Devuelve una isntancia de la "actividad" especificada
    def actividad(self, actividad):
        actividades = self.instances()
        act = None
        for a in actividades:
            if a.name == actividad:
                act = a
                break
        return act
    
    # Se ha sobrecargado el método, puedo llamarlo con el nombre de la actividad "actividad1"
    # o directamente con una instancia de Actividades
    def objetivos(self, actividad):
        objetivos = []
        if isinstance(actividad,str):
            act = self.actividad(actividad)
        else:
            act = actividad
        
        # tiene_objetivo es una Object Property de Actividad
        if isinstance(act.tiene_objetivo,list) # compruebo si una lista o un solo elemento
            objetivos.extend(act.tiene_objetivo)
        elif act.tiene_objetivo # compruebo que tenga al menos un elemento
            objetivos.append(act.tiene_objetivo)
        else:
            print("No se encontraron objetivos")
        return objetivos
    
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
        contextos_edad = self.ontología.Contexto_edad.instances()
        for contexto in contextos_edad:
            if contexto.edad_final >= edad >=contexto.edad_inicial:
                return contexto 
        return None

    # Es necesario inferir el contexto género a partir del género del alumno
    # Contexto_género es una clase de la ontología
    def contexto_genero(self, genero):
        contextos_genero = self.ontología.Contexto_género.instances()
        for contexto in contextos_genero:
            if contexto.name == genero:
                return contexto 
        return None    
    
    # Devuelve la instancia del contexto, "contexto1", solicitado.
    # Clasificaciones es una clase de la ontologia
    def contexto(self, contexto):
        contexto = None
        for instancia in self.ontologia.Clasificaciones.instances():
            if instancia.name == contexto:
                contexto = instancia
                break
        return contexto
    
    # Devuelve las funciones corporales afectadas por los contextos
    # contexto es una instancia de la clase Clasificaciones, es decir, de los contextos
    def funciones_afectadas(self, contexto):
    
        funciones_afectadas = []

        # ctx_tiene_impacto es una Object Property de Contextos (Clasificaciones)
        if contexto:
            for impacto in contexto.ctx_tiene_impacto:
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
