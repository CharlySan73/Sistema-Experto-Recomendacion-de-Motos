# Aqui sera el archivo de conexion entre la base de conocimientos y la interfaz 
# de usuario del sistema experto de recomendación de 
# motocicletas para concesionaria.
# Donde se llamaran las reglas y hechos de la base de conocimientos para ser 
# utilizados en la interfaz de usuario.
# Archivo de conexión entre la base de conocimientos Prolog
# y la interfaz del sistema experto de motocicletas.

from pyswip import Prolog
import os

prolog = Prolog()

RUTA_BASE = "c:/Users/uriel/Desktop/Semestres/10mo_Semestre/Logica y Funcional/programas/Sanchez Arenas_Fuentes Gonzalez"
RUTA_PROLOG = os.path.join(RUTA_BASE, "motos.pl").replace("\\", "/")
RUTA_GUARDADAS = os.path.join(RUTA_BASE, "motos_guardadas.pl").replace("\\", "/")


def cargar_base_conocimientos():
    try:
        prolog.consult(RUTA_PROLOG)
        if os.path.exists(RUTA_GUARDADAS):
            list(prolog.query("retractall(moto(_,_,_,_,_,_))"))
            prolog.consult(RUTA_GUARDADAS)

    except Exception as e:
        print(f"Error al cargar la base de conocimientos: {e}")


cargar_base_conocimientos()


def consultar_motos(consulta):
    try:
        return list(prolog.query(consulta))
    except Exception as e:
        print(f"Error al consultar Prolog: {e}")
        return []


def obtener_todas_las_motos():
    return consultar_motos(
        "moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio)"
    )


def buscar_por_marca(marca):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Marca = {marca.lower()}"
    )


def buscar_por_estilo(estilo):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Estilo = {estilo.lower()}"
    )


def buscar_por_precio(minimo, maximo):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Precio >= {minimo}, Precio =< {maximo}"
    )


def buscar_por_cilindrada(minimo, maximo):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Cilindrada >= {minimo}, Cilindrada =< {maximo}"
    )


def buscar_por_modelo(modelo):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Modelo = {modelo.lower()}"
    )


def buscar_por_anio(anio):
    return consultar_motos(
        f"moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio), Anio = {anio}"
    )


def agregar_moto(marca, modelo, estilo, cilindrada, precio, anio):
    consulta = (
        f"gestionarMoto(agregar, "
        f"{marca.lower()}, "
        f"{modelo.lower()}, "
        f"{estilo.lower()}, "
        f"{cilindrada}, "
        f"{precio}, "
        f"{anio})"
    )
    return consultar_motos(consulta)


def eliminar_moto(marca, modelo):
    consulta = (
        f"gestionarMoto(eliminar, "
        f"{marca.lower()}, "
        f"{modelo.lower()}, "
        f"_, _, _, _)"
    )
    return consultar_motos(consulta)


def actualizar_moto(marca, modelo, estilo, cilindrada, precio, anio):
    consulta = (
        f"gestionarMoto(actualizar, "
        f"{marca.lower()}, "
        f"{modelo.lower()}, "
        f"{estilo.lower()}, "
        f"{cilindrada}, "
        f"{precio}, "
        f"{anio})"
    )
    return consultar_motos(consulta)


def recomendar_moto_datos(uso, presupuesto, experiencia):
    return consultar_motos(
        f"recomendarMotoDatos({uso.lower()}, {presupuesto}, {experiencia.lower()}, Marca, Modelo, Estilo, Cilindrada, Precio, Anio)"
    )