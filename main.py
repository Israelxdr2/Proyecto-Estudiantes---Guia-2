from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

# Se crea UN solo controlador de cada tipo.
# A matrículas se le pasan los MISMOS estudiantes y materias.
estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribió otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # Los controladores devuelven la TUPLA (exito, mensaje)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Sirve para estudiantes, materias y matrículas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    # Recorre el DICCIONARIO del objeto: clave y valor a la vez
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ DE ESTUDIANTES
# =====================================================================

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: ")
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavía no hay estudiantes.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email, carnet, carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningún estudiante coincide con '{termino}'.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_est)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_est, cambios))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_est)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_est))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE MATERIAS
# =====================================================================

def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código: "),
        "creditos": pedir_entero("Créditos (1-10): "),
        "cupos": pedir_entero("Cupos iniciales: ")
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavía no hay materias.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(materia)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_materia, cambios))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminará: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_materia))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ DE MATRÍCULAS
# =====================================================================

def crear_matricula():
    imprimir_titulo("MATRICULAR ESTUDIANTE")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": pedir_entero("Periodo (ej. 20261): "),
    }
    if None in datos.values():
        imprimir_error("Todos los datos deben ser números enteros válidos")
        return pausa()

    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "Todavía no hay matrículas.")
    pausa()


def registrar_nota_matricula():
    imprimir_titulo("REGISTRAR NOTA")
    id_matrib = pedir_entero("Id de la matrícula: ")
    if id_matrib is None:
        imprimir_error("ID inválido")
        return pausa()

    try:
        nota = float(input("Ingrese la nota: "))
        mostrar_resultado(*matriculas.registrar_nota(id_matrib, nota))
    except ValueError:
        imprimir_error("La nota debe ser un número válido")
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO DE MATRÍCULA")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print("\n" + texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_matrib = pedir_entero("Id de la matrícula: ")
    if id_matrib and confirmar("Se devolverá el cupo a la materia. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_matrib))
    else:
        imprimir_info("Operación cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN DEL SISTEMA")
    
    # 1. Cuántos estudiantes
    total_est = len(estudiantes.leer())
    
    # 2. Carreras distintas (conjunto ordenado / sorted set)
    carreras = sorted({est.carrera for est in estudiantes.leer() if hasattr(est, "carrera") and est.carrera})
    
    # 3. Materias sin cupo
    sin_cupo = materias.materias_sin_cupo()
    
    # 4. Matrículas aprobadas (usando estado() == "Aprobado")
    aprobadas = 0
    for m in matriculas.leer():
        if hasattr(m, "estado") and m.estado() == "Aprobado":
            aprobadas += 1

    print(f"  Estudiantes registradas : {total_est}")
    print(f"  Carreras distintas      : {', '.join(carreras) or 'Ninguna'}")
    print(f"  Materias sin cupo       : {len(sin_cupo)}")
    print(f"  Matrículas aprobadas    : {aprobadas}")
    pausa()


# =====================================================================
# MENÚS: DICCIONARIOS tecla -> (texto, función)
# =====================================================================

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Matricular", crear_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota_matricula),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """Un solo bucle para los tres submenús."""
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:              # búsqueda por clave: instantánea
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:                    # la opción "Volver"
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN ESCOLAR")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")