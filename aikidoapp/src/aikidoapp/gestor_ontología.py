# gestor_ontologia.py
"""
Nombre: GestorOntología
Fecha creación: 11/06/2025
Versión: 1.0
Descripción: A través de la librería Owlready2 gestionamos la ontología creada con Protégé en 
formato owl. Implementa el patrón Singleton para que se cree una única instancia del gestor
"""
from owlready2 import get_ontology, Thing


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
