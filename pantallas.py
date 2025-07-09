from .gestor_pantallas import Pantalla
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, LEFT, CENTER
from pathlib import Path
from .gestores_app import GestoresApp
from .gestor_ontología import *
from .gestor_recomendaciones import *
from .config import DEBUG

class PantallaGrupo(Pantalla):

    def __init__(self, nombre):
        super().__init__(nombre,self._crear_cabecera(), self._crear_cuerpo(), self._crear_pie())

    def _crear_cabecera(self):
        return toga.Label("GRUPOS", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow",flex=0))
    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(padding=10, margin_top=20,
                                     background_color="#282828", flex=1,
                                     ))
        cuerpo.add(toga.Label("Estamos en Grupos", style=Pack(padding=10)))  
        return cuerpo

    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie
    
    def actualizar(self):

        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        contexto = GestoresApp.contextos().get_contexto("grupos")        
        grupos = contexto.get_grupos()
        for g in grupos:
            # NUEVA LÍNEA
            linea_texto = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=10,
                                     background_color="#282828",
                                     ))
            linea_texto.add(
                toga.Button(icon=GestoresApp.iconos().obtener_icono("icono_grupo-2.png"),
                                    style=Pack(background_color="#282828"), 
                                    # al presionar abre la ficha del grupo, el nombre se lo
                                    # pasamos como parámetro del lambda
                                    on_press=lambda x, grupo=g: self.ver_ficha(grupo)
                                   )
                            )
            # TEXTO: nombre y comentario           
            texto = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=0,
                                     background_color="#282828",
                                     ))
            texto.add(toga.Label(g.name, style=Pack(color="white")))
            # comment devuelve una cadena de comentarios, por lo que comment[0] me devuelve solo el primero
            texto.add(toga.Label(g.comment[0], style=Pack(color="white")))
            linea_texto.add(texto)
            linea_texto.add(toga.Button(icon=GestoresApp.iconos().obtener_icono("SIGUIENTE-2.png"),
                                        style=Pack(background_color="#282828")))
            cuerpo.add(linea_texto)
            cuerpo.add(toga.Divider())

        self.contenedor = toga.Box(style=Pack(direction=COLUMN,flex=1, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo
    
    def ver_ficha(self, grupo):
        GestoresApp.contextos().ir_a_contexto("ficha_grupo")
        GestoresApp.contextos().contexto_activado().agregar_objeto(grupo)
        GestoresApp.pantallas().ir_a("ficha_grupo")



class PantallaInicio(Pantalla):
    def __init__(self, nombre):
        super().__init__(nombre,self._crear_cabecera(), self._crear_cuerpo(), self._crear_pie())

    def _crear_cabecera(self):
        return toga.Label("INICIO", 
                    style=Pack(font_size=15, text_align=LEFT, 
                               background_color="#343434", color="yellow",
                               flex=0))
    
    def _crear_cuerpo(self):

        cuerpo = toga.Box(style=Pack(padding=10, margin_top=20,
                                     background_color="#282828", flex=1,
                                     ))
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("Grupos-2.png"),
            on_press=lambda x: self.on_press("grupos"),
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("Alumnos-2.png"),
            on_press=lambda x: self.on_press("alumnos"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("Actividades-2.png"),
            on_press=lambda x: self.on_press("actividades"),
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("Problematicas-2.png"),
            on_press=lambda x: self.on_press("problemas"),
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("Recomendacion-2.png"),
            on_press=lambda x: self.on_press("recomendaciones"),
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)

        return cuerpo

    def _crear_pie(self):
        pie = toga.Box(style=Pack(direction=ROW,background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

class PantallaAlumnos(PantallaGrupo):
    def _crear_cabecera(self):
        return toga.Label("ALUMNOS", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))

class PantallaActividades(PantallaGrupo):
    def _crear_cabecera(self):
        return toga.Label("ACTIVIDADES", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))

class PantallaProblemas(PantallaGrupo):
    def _crear_cabecera(self):
        return toga.Label("PROBLEMATICAS", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))


class PantallaFichaGrupo(Pantalla):
    grupo = ""
    descripcion = ""

    def __init__(self, nombre):
        super().__init__(nombre,self._crear_cabecera(), self._crear_cuerpo(), self._crear_pie())

    def _crear_cabecera(self):
        return toga.Label("FICHA GRUPO", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
    def _crear_cuerpo(self):
        # CONTENEDOR PRINCIPAL DEL CUERPO
        cuerpo=toga.Box(style=Pack(direction=COLUMN, padding=10, margin_top=20,
                                     background_color="#282828", flex=1,
                                     ))
        # BOX-1: NOMBRE GRUPO
        #        LABEL + INPUT
        etiqueta=toga.Label("NOMBRE",style=Pack(padding=10, margin_top=20,
                                     color="#717476"))
        entrada = toga.TextInput(self.grupo)
        box1 = toga.Box(style=Pack(direction=ROW,flex=0))
        box1.add(etiqueta)
        box1.add(entrada)
        cuerpo.add(box1)
        # BOX-2: DESCRIPCIÓN
        #       LABEL + INPUT
        etiqueta=toga.Label("DESCRIPCIÓN",style=Pack(padding=10, margin_top=20,
                                     color="#717476"))
        entrada = toga.MultilineTextInput(self.descripcion)
        box2 = toga.Box(style=Pack(direction=COLUMN,flex=0))
        box2.add(etiqueta)
        box2.add(entrada)
        cuerpo.add(box2)
        # BOX-3: BOTONES
        #       BOX-ALUMNOS: BUTTON + LABEL
        #       BOX-PROBLEMATICAS: BUTTON + LABEL
        #       BOX-RECOMENDACIONES: BUTTON + LABEL
        box3 = toga.Box(style=Pack(direction=COLUMN,flex=0))

        box_alumnos=toga.Box(style=Pack(direction=ROW,flex=0))
        boton=toga.Button("ALUMNOS")
        etiqueta=toga.Label("ALUMNOS",style=Pack(padding=10, margin_top=20, color="#717476"))
        box_alumnos.add(boton)
        box_alumnos.add(etiqueta)

        box_problematicas=toga.Box(style=Pack(direction=ROW,flex=0))
        boton=toga.Button("PROBLEMATICAS")
        etiqueta=toga.Label("PROBLEMATICAS",style=Pack(padding=10, margin_top=20, color="#717476"))
        box_problematicas.add(boton)
        box_problematicas.add(etiqueta)

        box_recomendaciones=toga.Box(style=Pack(direction=ROW,flex=0))
        boton=toga.Button("RECOMENDACIONES")
        etiqueta=toga.Label("RECOMENDACIONES",style=Pack(padding=10, margin_top=20, color="#717476"))
        box_recomendaciones.add(boton)
        box_recomendaciones.add(etiqueta)

        box3.add(box_alumnos)
        box3.add(box_problematicas)
        box3.add(box_recomendaciones)
        cuerpo.add(box3)
        return cuerpo

    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie
    def actualizar(self):
        contexto = GestoresApp.contextos().contexto_activado()
        self.grupo = contexto.objetos[0].name
        self.descripcion = contexto.objetos[0].comment[0]
        print("GRUPO: ", self.grupo, self.descripcion)
        contexto.objetos.clear()

# MUESTRA UNA LISTA DE RECOMENDACIONES
# ES LA PANTALLA PRINCIPAL DE RECOMENDACIONES
class PantallaRecomendaciones(Pantalla):
    def _crear_cabecera(self):
        return toga.Label("RECOMENDACIONES", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla de recomendaciones")
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        content = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=0,
                                     background_color="#282828", 
                                     ))
        contexto = GestoresApp.contextos().get_contexto("recomendaciones")        
        recomendaciones = contexto.get_recomendaciones()
        for g in recomendaciones:
            # NUEVA LÍNEA
            linea_texto = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=10,
                                     background_color="#282828",
                                     ))
            linea_texto.add(
                toga.Button(icon=GestoresApp.iconos().obtener_icono("recomendacion-1.png"),
                                    style=Pack(background_color="#282828"), 
                                    # al presionar abre la ficha del grupo, el nombre se lo
                                    # pasamos como parámetro del lambda
                                    on_press=lambda x=g: self.ver_detalles(g.name)
                                   )
                            )
            # TEXTO: nombre y comentario           
            texto = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=0,
                                     background_color="#282828",
                                     ))
            texto.add(toga.Label(g.name, style=Pack(color="white")))
            # comment devuelve una cadena de comentarios, por lo que comment[0] me devuelve solo el primero
            if g.rcm_tiene_descripción:
                texto.add(toga.Label(g.rcm_tiene_descripción[0], style=Pack(color="white")))
                linea_texto.add(texto)
            """
            linea_texto.add(toga.Button(icon=GestoresApp.iconos().obtener_icono("SIGUIENTE-2.png"),
                                        style=Pack(background_color="#282828")))
            """
            content.add(linea_texto)
            content.add(toga.Divider())
        
        cuerpo.add(toga.ScrollContainer(content=content,style=Pack(flex=1)))
        self.contenedor = toga.Box(style=Pack(direction=COLUMN,flex=1, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo    
        
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("CREAR-1.png"),
            on_press=lambda x: self.on_press("rcm_datos_alta"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)

        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def ver_detalles(self,id):
        ctx = GestoresApp.contextos().contexto_activado() # objeto de tipo GestorRecomendaciones
        gr = ctx.objetos[0] # objeto de tipo GestorRecomendaciones
        gr.leer_recomendación(id) # lee la recomendación con el id
        datos = gr.leer_datos_recomendación(id)
        if DEBUG:
            print("LEER_DATOS_RECOMENDACIÓN:", datos)
        if ctx.objetos[1]:
            ctx.objetos[1] = datos
        else:
            ctx.agregar_objeto(datos)
        GestoresApp.pantallas().ir_a("rcm_detalles")

class PantallaRcmDetalles(Pantalla):
    datos = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de detalles de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        etiqueta = toga.Label("Recomendaciones - Detalles", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FILTROS-1.png"),
            on_press=lambda x: self.on_press("rcm_filtros_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))

        if self.datos:
            metadatos = self.datos["datos"]
            if  metadatos:
                texto = metadatos["descripcion"][0]
                texto += "\n" + "Creada el " 
                texto += metadatos["fecha_creacion"][0] if metadatos["fecha_creacion"] else "'sin fecha'"
                texto += "\n" + "Modificada el " 
                texto += metadatos["fecha_modificacion"][0] if metadatos["fecha_modificacion"] else "'sin fecha"
                texto += "\n" + "Evaluada como " 
                texto += metadatos["evaluacion"][0] if metadatos["evaluacion"] else "'sin evaluación'"
                texto += " el " 
                texto += metadatos["fecha_evaluacion"][0] if metadatos["fecha_evaluacion"] else "'sin fecha evaluación'"
        
                etiqueta = toga.Label(texto,
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            else:
                etiqueta = toga.Label("No hay datos disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla de detalles de recomendaciones")
        self.actualiza_datos()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN,flex=1, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_datos(self):
        if GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            self.datos = contexto.objetos[1] # objeto de tipo GestorRecomendaciones

class PantallaRcmDatos(Pantalla):
    datos = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de datoss de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Datos", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FILTROS-1.png"),
            on_press=lambda x: self.on_press("rcm_filtros_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.datos:
            linea_nombre = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=0,
                                     background_color="#282828",
                                     ))
            etiqueta = toga.Label("NOMBRE:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            linea_nombre.add(etiqueta)
            campo_nombre = toga.TextInput(value=self.datos["id"],
                                 style=Pack(font_size=15, text_align=LEFT, 
                                            color="#343434",background_color="#747779",
                                             padding=10, flex=1))
            linea_nombre.add(campo_nombre)
            cuerpo.add(linea_nombre)
            etiqueta = toga.Label("DESCRIPCIÓN:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            campo_descripcion = toga.MultilineTextInput(value=self.datos["descripcion"][0],
                                 style=Pack(font_size=15, text_align=LEFT, color="#343434",
                                            background_color="#747779",padding=10))
            cuerpo.add(campo_descripcion)
            
            etiqueta = toga.Label("EVALUACIÓN:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            evaluacion = self.datos["evaluacion"][0] if self.datos["evaluacion"] else "Sin evaluación"
            campo_evaluacion = toga.TextInput(value=evaluacion,
                                 style=Pack(font_size=15, text_align=LEFT, color="#343434",
                                            background_color="#747779",padding=10))
            cuerpo.add(campo_evaluacion)
            
            linea_fecha = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=0,
                                     background_color="#282828",
                                     ))
            etiqueta = toga.Label("FECHA EVALUACIÓN:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            linea_fecha.add(etiqueta)
            fecha_evaluacion = self.datos["fecha_evaluacion"][0] if self.datos["fecha_evaluacion"] else "Sin fecha evaluación"
            campo_fecha = toga.TextInput(value=fecha_evaluacion,
                                 style=Pack(font_size=15, text_align=LEFT, 
                                            color="#343434",background_color="#747779",
                                             padding=10, flex=1))
            linea_fecha.add(campo_fecha)
            cuerpo.add(linea_fecha)
 
        else:
            etiqueta = toga.Label("No hay datos disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla de datos de recomendaciones")
        self.actualiza_datos()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_datos(self):
        """ 
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            gestor = contexto.objetos[0] # objeto de tipo GestorRecomendaciones
            rcm = gestor.get_recomendaciones_obj() # objeto de tipo Recomendaciones
            self.datos = rcm.datos() # obtiene los datos de la recomendación
        """
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            datos = contexto.objetos[1] 
            self.datos = datos["datos"] # obtiene los datos de la recomendación

class PantallaRcmFiltros_1(Pantalla):
    criterios = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de filtros 1 de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Filtros - 1", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.criterios:
            linea_grupo = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=0,
                                     background_color="#282828",
                                     ))
            etiqueta = toga.Label("GRUPO:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            linea_grupo.add(etiqueta)
            campo_grupo = toga.Selection(value=self.criterios["grupo"],
                                 style=Pack(font_size=15, text_align=LEFT, 
                                            color="#343434",background_color="#747779",
                                             padding=10, flex=1))
            linea_grupo.add(campo_grupo)
            cuerpo.add(linea_grupo)
            # MUESTRA LOS ALUMNOS
            etiqueta = toga.Label("ALUMNOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            lista_alumnos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            for alumno in self.criterios["alumnos"]:
                checkbox_alumno = toga.Switch(text=alumno,value=True)
                lista_alumnos.add(checkbox_alumno)
            container_alumnos = toga.ScrollContainer(content = lista_alumnos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_alumnos)
         
              # MUESTRA LOS CONTEXTOS
            etiqueta = toga.Label("CONTEXTOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            lista_contextos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            for contexto in self.criterios["contextos"]:
                checkbox_contexto = toga.Switch(text=contexto,value=True)
                lista_contextos.add(checkbox_contexto)
            container_contextos = toga.ScrollContainer(content = lista_contextos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_contextos)   

             # MUESTRA BOTON SIGUIENTE PANTALLA FILTROS 2
            boton_box = toga.Box(style=Pack(direction=ROW, padding=0, flex=0))
            boton_box.add(toga.Box(style=Pack(flex=1))) # este box es para que el boton aparezca a la derecha del todo
 
            boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FLECHA-DER-1.png"),
                on_press=lambda x: self.on_press("rcm_filtros_2"),
                style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50,flex=0)
            )
            boton_box.add(boton)
            cuerpo.add(boton_box)
           
        else:
            etiqueta = toga.Label("No hay filtros disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla 1 de filtros  de recomendaciones")
        self.actualiza_criterios()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_criterios(self):
        """
         if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            gestor = contexto.objetos[0] # objeto de tipo GestorRecomendaciones
            rcm = gestor.get_recomendaciones_obj() # objeto de tipo Recomendaciones
            self.criterios = rcm.criterios() # obtiene los criterios de la recomendación
        """
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            datos = contexto.objetos[1]
            self.criterios = datos["criterios"] # obtiene los criterios de la recomendación

class PantallaRcmFiltros_2(Pantalla):
    criterios = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de filtros 2 de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Filtros - 2", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.criterios:
            # MUESTRA LOS FUNDAMENTOS
            etiqueta = toga.Label("FUNDAMENTOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            lista_fundamentos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            for fundamento in self.criterios["fundamentos"]:
                checkbox_fundamento = toga.Switch(text=fundamento,value=True)
                lista_fundamentos.add(checkbox_fundamento)
            container_fundamentos = toga.ScrollContainer(content = lista_fundamentos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_fundamentos)
  
             # MUESTRA LOS OBJETIVOS
            etiqueta = toga.Label("OBJETIVOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            lista_objetivos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            for objetivo in self.criterios["objetivos"]:
                checkbox_objetivo = toga.Switch(text=objetivo,value=True)
                lista_objetivos.add(checkbox_objetivo)
            container_objetivos = toga.ScrollContainer(content = lista_objetivos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_objetivos)
         
              # MUESTRA LOS CONTEXTOS
            etiqueta = toga.Label("MODALIDADES:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            lista_modalidades = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            for modalidad in self.criterios["modalidades"]:
                checkbox_modalidad = toga.Switch(text=modalidad,value=True)
                lista_modalidades.add(checkbox_modalidad)
            container_modalidades = toga.ScrollContainer(content = lista_modalidades,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_modalidades)   

             # MUESTRA BOTON SIGUIENTE PANTALLA FILTROS 2
            boton_box = toga.Box(style=Pack(direction=ROW, padding=0, flex=0))
            boton_box.add(toga.Box(style=Pack(flex=1))) # este box es para que el boton aparezca a la derecha del todo
 
            boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FLECHA-IZQ-1.png"),
                on_press=lambda x: self.on_press("rcm_filtros_1"),
                style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50,flex=0)
            )
            boton_box.add(boton)
            cuerpo.add(boton_box)

        else:
            etiqueta = toga.Label("No hay filtros disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla 1 de filtros  de recomendaciones")
        self.actualiza_criterios()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_criterios(self):
         if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            datos = contexto.objetos[1]
            self.criterios = datos["criterios"]

class PantallaRcmActividades_1(Pantalla):
    actividades_recomendadas = None # [{"id":"actividad_id", "actividad":"nombre", 
                                    # "desarrollo":"descripción", "beneficio":"beneficio"}]

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de actividades 1 de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Actividades", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FILTROS-1.png"),
            on_press=lambda x: self.on_press("rcm_filtros_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.actividades_recomendadas:
            # MUESTRA LAS ACTIVIDADES RECOMENDADAS
            content = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=0,
                                     background_color="#282828", 
                                     ))
            for actividad in self.actividades_recomendadas:
                arc_datos = actividad["datos"]
                arc_actividad = actividad["actividad"]
                # NUEVA LÍNEA
                linea_texto = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=10,
                                     background_color="#282828",
                                     ))
                linea_texto.add(
                    toga.Button(icon=GestoresApp.iconos().obtener_icono("Actividades-2.png"),
                                    style=Pack(background_color="#282828"), 
                                    # al presionar abre la ficha del grupo, el nombre se lo
                                    # pasamos como parámetro del lambda
                                    on_press=lambda x, id=arc_datos["id"]: self.ver_detalles(id)
                                   )
                            )
                # TEXTO: nombre y comentario           
                texto = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=0,
                                     background_color="#282828",
                                     ))
                texto.add(toga.Label(arc_datos["nombre"].upper(), style=Pack(color="white")))
                texto.add(toga.Label(arc_actividad["desarrollo"], style=Pack(color="white")))
                linea_texto.add(texto)
                content.add(linea_texto)
                content.add(toga.Divider())

            cuerpo.add(toga.ScrollContainer(content=content,style=Pack(flex=1)))
 
        else:
            etiqueta = toga.Label("No hay actividades disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla 1 de filtros  de recomendaciones")
        self.actualiza_actividades()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
 
    def actualiza_actividades(self):
         if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones")
            datos = contexto.objetos[1] 
            self.actividades_recomendadas=datos["actividades"]

    def ver_detalles(self,id):
        GestoresApp.contextos().ir_a_contexto("actividad_recomendada") # objeto de tipo GestorRecomendaciones
        if DEBUG:
            print("BUSCAR ACTIVIDAD RECOMENDADA ", id)
      # Busca la actividad seleccionada en la lista
        actividad = next((a for a in self.actividades_recomendadas if a["datos"]["id"] == id), None)
        if actividad:
            if DEBUG:
                print("ENCONTRADA ", actividad)
            GestoresApp.contextos().ir_a_contexto("actividad_recomendada")
            contexto = GestoresApp.contextos().get_contexto("actividad_recomendada")
            contexto.objetos.clear()
            contexto.objetos.append(actividad)
            GestoresApp.pantallas().ir_a("rcm_actividades_2")


class PantallaRcmActividades_2(Pantalla):
    datos = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de ficha de actividad de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Ficha Actividad", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.datos:
            act_datos = self.datos["datos"]
            act_actividad = self.datos["actividad"]

            if DEBUG:
                print("PANTALLA_RCM_ACTIVIDADES_2:",self.datos)
            etiqueta = toga.Label(act_datos["nombre"].upper(),
                                 style=Pack(font_size=15, text_align=LEFT, color="#747779", padding=10))
            cuerpo.add(etiqueta)
            etiqueta = toga.Label(act_actividad["desarrollo"],
                                 style=Pack(font_size=15, text_align=LEFT, background_color="#343434", color="#747779", padding=10,height=350, width=550, flex=0))
            cuerpo.add(etiqueta)
            etiqueta = toga.Label("Recomendado para:",
                                 style=Pack(font_size=15, text_align=LEFT, color="#747779", padding=10, flex=0))
            cuerpo.add(etiqueta)
            texto = "Contexto: " + act_datos["contexto"]
            texto += "\n" + "Alumnos: "
            primero = True
            for a in act_datos["alumnos"]:
                if primero:
                    primero=False
                else:
                    texto += ", "
                texto += a
            etiqueta = toga.Label(texto,
                                 style=Pack(font_size=15, text_align=LEFT, background_color="#343434", color="#747779", padding=10,height=200, width=550, flex=0))
            cuerpo.add(etiqueta)
            espacio =toga.Box(style=Pack(flex=1))
            cuerpo.add(espacio)
             # MUESTRA BOTON ANTERIOR PANTALLA ACTIVIDADES 2
            boton_box = toga.Box(style=Pack(direction=ROW, padding=0, flex=0))
            boton_box.add(toga.Box(style=Pack(flex=1))) # este box es para que el boton aparezca a la derecha del todo
 
            boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FLECHA-IZQ-1.png"),
                on_press=lambda x: self.on_press_anterior(),
                style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50,flex=0)
            )
            boton_box.add(boton)
            cuerpo.add(boton_box)
        else:
            etiqueta = toga.Label("No hay actividades disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla ficha de actividades recomendadas")
        self.actualiza_datos()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("actividad_recomendada")
            if contexto.objetos:
                self.datos = contexto.objetos[0]

class PantallaRcmDatos_alta(Pantalla):
    datos = None
    descripcion = None
    observaciones = None

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de datos de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Datos - Creación", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
        """
        botones = toga.Box(style=Pack(direction=ROW, alignment=RIGHT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        """
        """
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DETALLES-1.png"),
            on_press=lambda x: self.on_press("rcm_detalles"),
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        """
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FILTROS-1.png"),
            on_press=lambda x: self.on_press("rcm_filtros_1_alta"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)

        """
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("ACTIVIDADES-2.png"),
            on_press=lambda x: self.on_press("rcm_actividades_1"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
        """
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("GENERAR-1.png"),
            on_press=lambda x: self.generar_recomendacion(),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        if  self.datos:
            etiqueta = toga.Label("DESCRIPCIÓN:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            campo_descripcion = toga.MultilineTextInput(id="campo_descripcion",value=self.datos["descripcion"],
                                 style=Pack(font_size=15, text_align=LEFT, color="#343434",
                                            background_color="#747779",padding=10),
                                            on_change=self.cambia_datos)
            cuerpo.add(campo_descripcion)
            self.descripcion = campo_descripcion            
            etiqueta = toga.Label("OBSERVACIONES:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
            campo_observaciones = toga.MultilineTextInput(id="campo_observaciones", value=self.datos["observaciones"],
                                 style=Pack(font_size=15, text_align=LEFT, color="#343434",
                                            background_color="#747779",padding=10),
                                            on_change = self.cambia_datos)
            cuerpo.add(campo_observaciones)
            self.observaciones=campo_observaciones            
        else:
            etiqueta = toga.Label("No hay datos disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo

    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla de datos de alta de recomendaciones")
        self.actualiza_datos()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1] 
            self.datos = datos["datos"] # obtiene los datos de la recomendación

    def cambia_datos(self, widget):
        self.datos["descripcion"]=self.descripcion.value
        self.datos["observaciones"] = self.observaciones.value

    def salva_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1] 
            datos["datos"]["descripcion"] = self.datos["descripcion"]
            datos["datos"]["observaciones"]= self.datos["observaciones"]
    
    def carga_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1]
            if not self.datos:
                self.datos = datos["datos"] 
            self.datos["descripcion"] = datos["datos"]["descripcion"] 
            self.datos["observaciones"] = datos["datos"]["observaciones"]  

    def generar_recomendacion(self):
        if DEBUG:
            print("GENERAR RECOMENDACIÓN")
        contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
        datos = contexto.objetos[1]
        criterios = {
            "grupo": datos["criterios"]["grupo"],
            "alumnos": datos["criterios"]["alumnos"], 
            "contextos_entrada": datos["criterios"]["contextos"],
            "fundamentos": datos["criterios"]["fundamentos"],
            "modalidades": datos["criterios"]["modalidades"],
            "objetivos": datos["criterios"]["objetivos"]
            }
        gestor_ontologia = GestoresApp.ontologia()
        ontologia = gestor_ontologia.get_ontologia() 
        gestor_experto = GestoresApp.sistema_experto()
        gestor_recomendaciones = GestorRecomendaciones(ontologia,gestor_experto)
        recomendaciones = gestor_recomendaciones.generar_recomendaciones(criterios)
        metadatos = datos["datos"]
        criterios = datos["criterios"]
        rcm_datos = {"descripcion": metadatos["descripcion"], "evaluacion": metadatos["evaluacion"],
                    "fecha_creacion":metadatos["fecha_creacion"], 
                    "fecha_evaluacion":metadatos["fecha_evaluacion"], 
                    "fecha_modificacion":metadatos["fecha_modificacion"],
                    "motivo":metadatos["motivo"], 
                    "observaciones":metadatos["observaciones"]
                    }
        rcm_criterios = {
                        "grupo":criterios["grupo"], 
                        "alumnos":criterios["alumnos"], 
                         "contextos_entrada":criterios["contextos"], 
                         "fundamentos":criterios["fundamentos"], 
                         "objetivos":criterios["objetivos"], 
                         "modalidades":criterios["modalidades"]
                        }
        gestor_recomendaciones.nueva_recomendacion(rcm_datos,rcm_criterios,recomendaciones)
        gestor_ontologia.guardar()

class PantallaRcmFiltros_1_alta(Pantalla):
    criterios = None
    filtro_grupos = None
    campo_grupos = None
    filtro_alumnos = None
    campo_alumnos = None
    checkboxes_alumnos = None
    filtro_contextos = None
    campo_contextos = None
    checkboxes_contextos = None
    _criterios_cargados = False # indica si es la primera vez o no

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de filtros 1 de alta de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Creación - Filtros - 1", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
       
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos_alta"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
       
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("GENERAR-1.png"),
            on_press=lambda x: self.generar_recomendacion,
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        
        if  self.criterios:     

            self.checkboxes_alumnos=[]
            self.checkboxes_contextos=[]
            lista_alumnos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            lista_contextos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))

            # Handlers
            def seleccionar_todos_alumnos(widget):
                if widget.value:
                    for cb in self.checkboxes_alumnos:
                        cb.value = True

            def deseleccionar_todos_alumnos(widget):
                if widget.value:
                    for cb in self.checkboxes_alumnos:
                        cb.value = False
            def seleccionar_todos_contextos(widget):
                if widget.value:
                    for cb in self.checkboxes_contextos:
                        cb.value = True

            def deseleccionar_todos_contextos(widget):
                if widget.value:
                    for cb in self.checkboxes_contextos:
                        cb.value = False
            linea_grupo = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding=0,
                                     background_color="#282828",
                                     ))
            etiqueta = toga.Label("GRUPO:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            linea_grupo.add(etiqueta)
            campo_grupo = toga.Selection(value=self.criterios["grupo"],
                                 style=Pack(font_size=15, text_align=LEFT, 
                                            color="#343434",background_color="#747779",
                                             padding=10, flex=1),
                                )
            campo_grupo.items =["grupo no seleccionado"] + sorted( [g.name for g in self.filtro_grupos])
            self.campo_grupos = campo_grupo
            linea_grupo.add(campo_grupo)
            cuerpo.add(linea_grupo)
            # MUESTRA LOS ALUMNOS
            linea_alumnos = toga.Box(style=Pack(direction=ROW, alignment="top"))
            etiqueta = toga.Label("ALUMNOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding_left=10))
            linea_alumnos.add(etiqueta)

            switch_seleccionar_alumnos = toga.Switch(text="Seleccionar todos",style=Pack(color = "white"),
                                            on_change=seleccionar_todos_alumnos)
            linea_alumnos.add(switch_seleccionar_alumnos)
            switch_deseleccionar_alumnos = toga.Switch(text="Deseleccionar todos",style=Pack(color="white"),
                                              on_change=deseleccionar_todos_alumnos)
            linea_alumnos.add(switch_deseleccionar_alumnos)
            cuerpo.add(linea_alumnos)
 
            
            for alumno in self.filtro_alumnos:
                seleccionado = alumno.name in self.criterios["alumnos"]
                checkbox_alumno = toga.Switch(text=alumno.name,value=seleccionado)
                lista_alumnos.add(checkbox_alumno)
                self.checkboxes_alumnos.append(checkbox_alumno)
            container_alumnos = toga.ScrollContainer(content = lista_alumnos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_alumnos)
         
              # MUESTRA LOS CONTEXTOS
            linea_contextos = toga.Box(style=Pack(direction=ROW, alignment="top"))
            etiqueta = toga.Label("CONTEXTOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding_left=10))
            linea_contextos.add(etiqueta)
            switch_seleccionar_contextos = toga.Switch(text="Seleccionar todos",style=Pack(color = "white"),
                                            on_change=seleccionar_todos_contextos)
            linea_contextos.add(switch_seleccionar_contextos)
            switch_deseleccionar_contextos = toga.Switch(text="Deseleccionar todos",style=Pack(color="white"),
                                              on_change=deseleccionar_todos_contextos)
            linea_contextos.add(switch_deseleccionar_contextos)
            cuerpo.add(linea_contextos)
            lista_ordenada = sorted( [g.name for g in self.filtro_contextos])
            for contexto in lista_ordenada:
                seleccionado = contexto in self.criterios["contextos"] 
                checkbox_contexto = toga.Switch(text=contexto,value=seleccionado)
                lista_contextos.add(checkbox_contexto)
                self.checkboxes_contextos.append(checkbox_contexto)
            container_contextos = toga.ScrollContainer(content = lista_contextos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_contextos)   

             # MUESTRA BOTON SIGUIENTE PANTALLA FILTROS 2
            boton_box = toga.Box(style=Pack(direction=ROW, padding=0, flex=0))
            boton_box.add(toga.Box(style=Pack(flex=1))) # este box es para que el boton aparezca a la derecha del todo
 
            boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FLECHA-DER-1.png"),
                on_press=lambda x: self.on_press("rcm_filtros_2_alta"),
                style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50,flex=0)
            )
            boton_box.add(boton)
            cuerpo.add(boton_box)
            
        else:
            etiqueta = toga.Label("No hay filtros disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo
    
    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla 1 de filtros  de recomendaciones")
        self.actualiza_criterios()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_criterios(self):
        if not self._criterios_cargados:
            if  GestoresApp.contextos():
                contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
                datos = contexto.objetos[1]
                self.criterios = datos["criterios"] # obtiene los criterios de la recomendación
                gestor_ontologia = GestoresApp.ontologia()
                ontologia = gestor_ontologia.get_ontologia()
                self.filtro_grupos = ontologia.Grupos.instances()
                alumnos = Alumnos(ontologia)
                self.filtro_alumnos = alumnos.instances()
                contextos = Contextos(ontologia)
                self.filtro_contextos = contextos.instances()
                self._criterios_cargados = True

    def salva_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1] 
            if self.campo_grupos.value == "grupo no seleccionado":
                datos["criterios"]["grupo"] = ""
            else: 
                datos["criterios"]["grupo"] = self.campo_grupos.value 
            datos["criterios"]["alumnos"]= [cb.text for cb in self.checkboxes_alumnos if cb.value]
            datos["criterios"]["contextos"] = [cb.text for cb in self.checkboxes_contextos if cb.value]
    
    def carga_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1]
            if not self.criterios:
                self.criterios = datos["criterios"] 
            self.criterios["grupo"] = datos["criterios"]["grupo"] 
            self.criterios["alumnos"] = datos["criterios"]["alumnos"]
            self.criterios["contextos"] = datos["criterios"]["contextos"]

    def generar_recomendacion(self):
        pass

class PantallaRcmFiltros_2_alta(Pantalla):
    criterios = None
    filtro_fundamentos = None
    campo_fundamentos = None
    checkboxes_fundamentos = None
    filtro_objetivos = None
    campo_objetivos = None
    checkboxes_objetivos = None
    filtro_modalidades = None
    campo_modalidades = None
    checkboxes_modalidades = None
    _criterios_cargados = False

    def _crear_cabecera(self):
        if DEBUG:
            print("Creando cabecera de pantalla de filtros 2 de alta de recomendaciones")
        cabecera = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=0
                                     ))
        etiqueta = toga.Label("Recomendaciones - Creación - Filtros - 2", 
                    style=Pack(font_size=15, text_align=LEFT, color="yellow"))
        cabecera.add(etiqueta)

        botones = toga.Box()
       
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("DATOS-1.png"),
            on_press=lambda x: self.on_press("rcm_datos_alta"), # el lambda hace que se pase por el método
                                                         # por referencia, sin que se ejecute
            style=Pack(padding=10, margin_top=20,)
        )
        botones.add(boton)
       
        cabecera.add(botones)

        return cabecera
    
    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  height=70, flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("GENERAR-1.png"),
            on_press=lambda x: self.generar_recomendacion,
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)
        pie.add(toga.Box(style=Pack(flex=1))) # deja un espacio en medio de los dos botones
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("SALIDA-2.png"),
            on_press=lambda x: self.on_press_anterior(),
            style=Pack(padding=10, margin_top=20,background_color="#343434",color="#343434", height=50)
        )
        pie.add(boton)
        return pie

    def _crear_cuerpo(self):
        cuerpo = toga.Box(style=Pack(direction=COLUMN, alignment=LEFT, padding=5, margin_top=5,
                                     background_color="#282828", flex=1
                                     ))
        
        
        if  self.criterios:     

            self.checkboxes_fundamentos=[]
            self.checkboxes_objetivos=[]
            self.checkboxes_modalidades=[]
            lista_fundamentos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            lista_objetivos = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))
            lista_modalidades = toga.Box(style=Pack(direction=COLUMN, background_color="#747779"))

            # Handlers
            def seleccionar_todos_fundamentos(widget):
                if widget.value:
                    for cb in self.checkboxes_fundamentos:
                        cb.value = True

            def deseleccionar_todos_fundamentos(widget):
                if widget.value:
                    for cb in self.checkboxes_fundamentos:
                        cb.value = False
            def seleccionar_todos_objetivos(widget):
                if widget.value:
                    for cb in self.checkboxes_objetivos:
                        cb.value = True

            def deseleccionar_todos_objetivos(widget):
                if widget.value:
                    for cb in self.checkboxes_objetivos:
                        cb.value = False
            def seleccionar_todos_modalidades(widget):
                if widget.value:
                    for cb in self.checkboxes_modalidades:
                        cb.value = True

            def deseleccionar_todos_modalidades(widget):
                if widget.value:
                    for cb in self.checkboxes_modalidades:
                        cb.value = False
            # MUESTRA LOS FUNDAMENTOS
            linea_fundamentos = toga.Box(style=Pack(direction=ROW, alignment="top"))
            etiqueta = toga.Label("FUNDAMENTOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding_left=10))
            linea_fundamentos.add(etiqueta)

            switch_seleccionar_fundamentos = toga.Switch(text="Seleccionar todos",style=Pack(color = "white"),
                                            on_change=seleccionar_todos_fundamentos)
            linea_fundamentos.add(switch_seleccionar_fundamentos)
            switch_deseleccionar_fundamentos = toga.Switch(text="Deseleccionar todos",style=Pack(color="white"),
                                              on_change=deseleccionar_todos_fundamentos)
            linea_fundamentos.add(switch_deseleccionar_fundamentos)
            cuerpo.add(linea_fundamentos)
            lista_ordenada = sorted( [g.name for g in self.filtro_fundamentos])
            for fundamento in lista_ordenada:
                seleccionado = fundamento in self.criterios["fundamentos"] 
                checkbox_fundamento = toga.Switch(text=fundamento,value=seleccionado)
                lista_fundamentos.add(checkbox_fundamento)
                self.checkboxes_fundamentos.append(checkbox_fundamento)
            container_fundamentos = toga.ScrollContainer(content = lista_fundamentos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_fundamentos)
         
              # MUESTRA LOS OBJETIVOS
            linea_objetivos = toga.Box(style=Pack(direction=ROW, alignment="top"))
            etiqueta = toga.Label("OBJETIVOS:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding_left=10))
            linea_objetivos.add(etiqueta)
            switch_seleccionar_objetivos = toga.Switch(text="Seleccionar todos",style=Pack(color = "white"),
                                            on_change=seleccionar_todos_objetivos)
            linea_objetivos.add(switch_seleccionar_objetivos)
            switch_deseleccionar_objetivos = toga.Switch(text="Deseleccionar todos",style=Pack(color="white"),
                                              on_change=deseleccionar_todos_objetivos)
            linea_objetivos.add(switch_deseleccionar_objetivos)
            cuerpo.add(linea_objetivos)
            lista_ordenada = sorted( [g.name for g in self.filtro_objetivos])
            for objetivo in lista_ordenada:
                seleccionado = objetivo in self.criterios["objetivos"] 
                checkbox_objetivo = toga.Switch(text=objetivo,value=seleccionado)
                lista_objetivos.add(checkbox_objetivo)
                self.checkboxes_objetivos.append(checkbox_objetivo)
            container_objetivos = toga.ScrollContainer(content = lista_objetivos,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_objetivos)   
             # MUESTRA LAS MODALIDADES
            linea_modalidades = toga.Box(style=Pack(direction=ROW, alignment="top"))
            etiqueta = toga.Label("MODALIDADES:",
                                 style=Pack(font_size=15, text_align=LEFT, color="white", padding_left=10))
            linea_modalidades.add(etiqueta)
            switch_seleccionar_modalidades = toga.Switch(text="Seleccionar todos",style=Pack(color = "white"),
                                            on_change=seleccionar_todos_modalidades)
            linea_modalidades.add(switch_seleccionar_modalidades)
            switch_deseleccionar_modalidades = toga.Switch(text="Deseleccionar todos",style=Pack(color="white"),
                                              on_change=deseleccionar_todos_modalidades)
            linea_modalidades.add(switch_deseleccionar_modalidades)
            cuerpo.add(linea_modalidades)
            lista_ordenada = sorted( [g.name for g in self.filtro_modalidades])
            for modalidad in lista_ordenada:
                seleccionado = modalidad in self.criterios["modalidades"] 
                checkbox_modalidad = toga.Switch(text=modalidad,value=seleccionado)
                lista_modalidades.add(checkbox_modalidad)
                self.checkboxes_modalidades.append(checkbox_modalidad)
            container_modalidades = toga.ScrollContainer(content = lista_modalidades,style=Pack(padding=10, background_color="#282828"))
            cuerpo.add(container_modalidades)   

             # MUESTRA BOTON SIGUIENTE PANTALLA FILTROS 2
            boton_box = toga.Box(style=Pack(direction=ROW, padding=0, flex=0))
            boton_box.add(toga.Box(style=Pack(flex=1))) # este box es para que el boton aparezca a la derecha del todo
 
            boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("FLECHA-IZQ-1.png"),
                on_press=lambda x: self.on_press("rcm_filtros_1_alta"),
                style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50,flex=0)
            )
            boton_box.add(boton)
            cuerpo.add(boton_box)
            
        else:
            etiqueta = toga.Label("No hay filtros disponibles",
                               style=Pack(font_size=15, text_align=LEFT, color="white", padding=10))
            cuerpo.add(etiqueta)
        return cuerpo
    
    def actualizar(self):
        if DEBUG:
            print("Actualizando pantalla 2 de filtros de alta de recomendaciones")
        self.actualiza_criterios()
        self.contenedor = toga.Box(style=Pack(direction=COLUMN, padding=0, background_color="#282828"))
        self.contenedor.add(self.cabecera)
        cuerpo = self._crear_cuerpo()
        self.contenedor.add(cuerpo)
        self.contenedor.add(self.pie)
        self.contenedor.refresh()
        self.cuerpo = cuerpo   
    
    def actualiza_criterios(self):
        if not self._criterios_cargados:
            if  GestoresApp.contextos():
                contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
                datos = contexto.objetos[1]
                self.criterios = datos["criterios"] # obtiene los criterios de la recomendación
                gestor_ontologia = GestoresApp.ontologia()
                ontologia = gestor_ontologia.get_ontologia()
                fundamentos = ontologia.Tipos_fundamentos
                self.filtro_fundamentos = fundamentos.instances()
                objetivos = Objetivos(ontologia)
                self.filtro_objetivos = objetivos.instances()
                modalidades = ontologia.Modalidad_actividades
                self.filtro_modalidades = modalidades.instances()
                self._criterios_cargados = True
    
    def salva_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1] 
            datos["criterios"]["fundamentos"]= [cb.text for cb in self.checkboxes_fundamentos if cb.value]
            datos["criterios"]["objetivos"] = [cb.text for cb in self.checkboxes_objetivos if cb.value]
            datos["criterios"]["modalidades"] = [cb.text for cb in self.checkboxes_modalidades if cb.value]
    
    def carga_datos(self):
        if  GestoresApp.contextos():
            contexto = GestoresApp.contextos().get_contexto("recomendaciones_alta")
            datos = contexto.objetos[1]
            if not self.criterios:
                self.criterios = datos["criterios"] 
            self.criterios["fundamentos"] = datos["criterios"]["fundamentos"] 
            self.criterios["objetivos"] = datos["criterios"]["objetivos"]
            self.criterios["modalidades"] = datos["criterios"]["modalidades"]
    
    def generar_recomendacion(self):
        pass