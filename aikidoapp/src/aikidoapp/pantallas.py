from .gestor_pantallas import Pantalla
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, RIGHT, LEFT, CENTER
from pathlib import Path
from .gestores_app import GestoresApp


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
                                  margin_bottom=10, height=50,
                                  flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)

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
            icon=GestoresApp.iconos().obtener_icono("Recomendaciones-2.png"),
            on_press=lambda x: self.on_press("recomendaciones"),
            style=Pack(padding=10, margin_top=20,)
        )
        cuerpo.add(boton)

        return cuerpo

    def _crear_pie(self):
        pie = toga.Box(style=Pack(background_color="#343434"),color="#343434",
                                  margin_bottom=10, height=50,
                                  flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)

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

class PantallaRecomendaciones(PantallaGrupo):
    def _crear_cabecera(self):
        return toga.Label("RECOMENDACIONES", 
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
                                  margin_bottom=10, height=50,
                                  flex=0, )
        boton = toga.Button(
            icon=GestoresApp.iconos().obtener_icono("HOME-2.png"),
            on_press=lambda x: self.on_press("inicio"),
            style=Pack(padding=10, margin_top=10,background_color="#343434",color="#343434",height=50)
        )
        pie.add(boton)

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