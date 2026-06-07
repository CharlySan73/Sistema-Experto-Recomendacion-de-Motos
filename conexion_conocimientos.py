# Aqui sera el archivo de conexion entre la base de conocimientos y la interfaz 
# de usuario del sistema experto de recomendación de 
# motocicletas para concesionaria.
# Donde se llamaran las reglas y hechos de la base de conocimientos para ser 
# utilizados en la interfaz de usuario.
from pyswip import Prolog

prolog = Prolog()
prolog.consult("c:/Users/uriel/Desktop/Semestres/10mo_Semestre/Logica y Funcional/programas/Sistema experto/motos.pl")


def consultar_motos(consulta):
    try:
        return list(prolog.query(consulta))
    except Exception as e:
        print(f"Error al consultar Prolog: {e}")
        return []


def obtener_todas_las_motos():
    return consultar_motos("moto(Marca, Modelo, Estilo, Cilindrada, Precio, Anio)")


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
    consulta = f"gestionarMoto(agregar, {marca.lower()}, {modelo.lower()}, {estilo.lower()}, {cilindrada}, {precio}, {anio})"
    return consultar_motos(consulta)


def eliminar_moto(marca, modelo):
    consulta = f"gestionarMoto(eliminar, {marca.lower()}, {modelo.lower()}, _, _, _, _)"
    return consultar_motos(consulta)


def actualizar_moto(marca, modelo, estilo, cilindrada, precio, anio):
    consulta = f"gestionarMoto(actualizar, {marca.lower()}, {modelo.lower()}, {estilo.lower()}, {cilindrada}, {precio}, {anio})"
    return consultar_motos(consulta)

def recomendar_moto_datos(uso, presupuesto, experiencia):
    return consultar_motos(
        f"recomendarMotoDatos({uso.lower()}, {presupuesto}, {experiencia.lower()}, Marca, Modelo, Estilo, Cilindrada, Precio, Anio)"
    )