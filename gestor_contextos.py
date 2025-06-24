class EstadoContexto:
    SIN_INICIALIZAR = "sin_inicializar"
    INICIALIZADO = "inicializado"
    ACTIVO = "activo"
    INACTIVO = "inactivo"


class Contexto:
    def __init__(self, nombre, pantalla, objetos=None):
        """
        Inicializa un nuevo contexto.

        :param nombre: Nombre o identificador del contexto
        :param pantalla: Objeto o nombre de la pantalla asociada
        :param objetos: Lista de objetos interactivos en la pantalla
        """
        self.nombre = nombre
        self.pantalla = pantalla
        self.objetos = objetos if objetos is not None else []       
        self.estado = EstadoContexto.SIN_INICIALIZAR
        print(f"[{self.nombre}] Contexto creado con estado: {self.estado}.")

    def inicializar(self):
        """
        Marca el contexto como inicializado.
        """
        if self.estado == EstadoContexto.SIN_INICIALIZAR:
            self.estado = EstadoContexto.INICIALIZADO
            print(f"[{self.nombre}] Contexto inicializado.")
        else:
            print(f"[{self.nombre}] Ya está inicializado o activo.")

    def activar(self):
        """
        Activa el contexto, si está inicializado.
        """
        if self.estado == EstadoContexto.INICIALIZADO:
            self.estado = EstadoContexto.ACTIVO
            print(f"[{self.nombre}] Contexto activado.")
        elif self.estado == EstadoContexto.ACTIVO:
            print(f"[{self.nombre}] Ya está activo.")
        else:
            print(f"[{self.nombre}] No puede activarse porque no está inicializado.")

    def desactivar(self):
        """
        Desactiva el contexto, dejándolo como inicializado.
        """
        if self.estado == EstadoContexto.ACTIVO:
            self.estado = EstadoContexto.INICIALIZADO
            print(f"[{self.nombre}] Contexto desactivado.")
        else:
            print(f"[{self.nombre}] No está activo para desactivarlo.")

    def reiniciar(self):
        """
        Devuelve el contexto a estado sin inicializar.
        """
        self.estado = EstadoContexto.SIN_INICIALIZAR
        print(f"[{self.nombre}] Contexto reiniciado.")

    def agregar_objeto(self, objeto):
        """
        Agrega un objeto interactivo al contexto.
        """
        self.objetos.append(objeto)
        print(f"[{self.nombre}] Objeto añadido: {objeto}")

    def resumen(self):
        return {
            "nombre": self.nombre,
            "pantalla": self.pantalla,
            "estado": self.estado,
            "objetos": self.objetos,
        }

    def __str__(self):
        return f"Contexto('{self.nombre}', Estado: {self.estado}, Pantalla: {self.pantalla}, Objetos: {len(self.objetos)})"

class GestorContextos:
    def __init__(self, contextos=None):
        self.contextos = contextos if contextos is not None else []
        self.contexto_actual = None
        self.historial = []


    def agregar_contexto(self, contexto):
        self.contextos.append(contexto)
        print(f"[INFO] Contexto '{contexto.nombre}' agregado.")

    def ir_a_contexto(self, nombre_contexto):
        for ctx in self.contextos:
            if ctx.nombre == nombre_contexto:
                self.historial.append(self.contexto_actual)
                self._cambiar_contexto(ctx)
                return
        print(f"[ERROR] Contexto '{nombre_contexto}' no encontrado.")

    def volver_contexto(self):
        if self.historial:
            self.contexto_actual=self.historial.pop()

    # Es igual que ir_a_contexto pero si cambiar el contexto actual
    def get_contexto(self, nombre_contexto):
        for ctx in self.contextos:
            if ctx.nombre == nombre_contexto:
                self._cambiar_contexto(ctx)
                return ctx
        print(f"[ERROR] Contexto '{nombre_contexto}' no encontrado.")
        return None
    def get_pantalla(self, nombre_contexto):
        if nombre_contexto:
            for ctx in self.contextos:
                if ctx.nombre == nombre_contexto:
                    return ctx.pantalla
            print(f"[ERROR] Pantalla para el contexto '{nombre_contexto}' no encontrada.")
            pantalla = None
        else:
            pantalla = self.contexto_actual.pantalla
        return pantalla

    def ir_siguiente(self):
        if self.contexto_actual:
            idx = self.contextos.index(self.contexto_actual)
            if idx + 1 < len(self.contextos):
                self._cambiar_contexto(self.contextos[idx + 1])
            else:
                print("[INFO] Ya estás en el último contexto.")
        else:
            print("[ERROR] No hay contexto actual activo.")

    def ir_anterior(self):
        if self.contexto_actual:
            idx = self.contextos.index(self.contexto_actual)
            if idx > 0:
                self._cambiar_contexto(self.contextos[idx - 1])
            else:
                print("[INFO] Ya estás en el primer contexto.")
        else:
            print("[ERROR] No hay contexto actual activo.")

    def _cambiar_contexto(self, nuevo_contexto):
        if self.contexto_actual:
            self.contexto_actual.desactivar()
        nuevo_contexto.inicializar()
        nuevo_contexto.activar()
        self.contexto_actual = nuevo_contexto
        print(f"[INFO] Cambiado al contexto: '{nuevo_contexto.nombre}'.")

    def contexto_activado(self):
        return self.contexto_actual
