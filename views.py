from abc import ABC, abstractmethod

from models import Estudiante,Materia,Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# =====================================================================
# CLASE BASE (ABSTRACTA)
# =====================================================================
# Solo dice QUÉ métodos debe tener todo controlador.
# CÓMO se hace cada uno lo escribe cada controlador, de la forma más simple.
class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass


# =====================================================================
# CONTROLADOR DE CLIENTES
# =====================================================================
class EstudianteController(CrudBase):

    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)

        # Leemos el JSON y convertimos cada diccionario en un objeto Cliente
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email","carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
        
        for campo in ("nombre", "apellido", "email", "carnet"):
            if campo in datos and str(datos[campo]).strip() == "":
                return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email):
                return f"Email inválido: '{email}'"
            usados = {c.email for c in self.lista if c.id != id_actual}
            if email in usados:
                return "Ese email ya está registrado"
        
        if "carnet" in datos:
            carnet= str(datos["carnet"]).strip().upper()
            
            carnet_usados={c.carnet for c in self.lista if c.id != id_actual}
            if carnet in carnet_usados:
                return "Este carnet ya esta registrado"
            

    def leer(self):
        return self.lista 

    def obtener(self, id_estudiante):
        for estudiante in self.lista:
            if estudiante.id == id_estudiante:
                return estudiante
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for est in self.lista:
            if (texto in est.nombre.lower()
                    or texto in est.apellido.lower()
                    or texto in est.email
                    or texto in est.carnet
                    or texto in est.carrera.lower()):
                encontrados.append(est)
        return encontrados

    def siguiente(self):
        mayor = 0
        for est in self.lista:
            if est.id > mayor:
                mayor = est.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        estudiante = Estudiante(self.siguiente(),
                          str(datos["nombre"]).strip().title(),
                          str(datos["apellido"]).strip().title(),
                          str(datos["email"]).strip().lower(),
                          str(datos.get("carnet", "")).strip().upper(),
                          str(datos.get("carrera", "")).strip().title())
        self.lista.append(estudiante)
        self.guardar()
        return True, f"estudiante creado: {estudiante.etiqueta()}"

    def actualizar(self, id_estudiante, datos):
        estudiante = self.obtener(id_estudiante)
        if estudiante is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        if not datos:
            return False, "No se indicó ningún cambio"

        # DIFERENCIA de conjuntos: campos que no existen en un cliente
        permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
        desconocidos = set(datos) - permitidos
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Se valida ANTES de tocar el objeto: si algo falla, no cambia nada
        error = self.validar(datos, id_estudiante)
        if error:
            return False, error

        for campo, valor in datos.items():
            valor = str(valor).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            setattr(estudiante, campo, valor)

        self.guardar()
        return True, f"estudiante {id_estudiante} actualizado"

    def eliminar(self, id_estudiante):
        est = self.obtener(id_estudiante) 
        if est is None:
            return False, f"No existe un estudiante con id {id_estudiante}"
        
        self.lista.remove(est)
        self.guardar()
        return True, f"Estudiante {id_estudiante} eliminado" 

# =====================================================================
# CONTROLADOR DE PRODUCTOS
# =====================================================================
class MateriaController(CrudBase):

    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos", "cupos"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"
                
        for campo in ("nombre", "codigo", "creditos", "cupos"):
            if campo in datos and str(datos[campo]).strip() == "":
                return f"El campo {campo} es obligatorio"

        if "codigo" in datos:
            codigo = str(datos["codigo"]).strip().upper()
            codigos_usados = {m.codigo for m in self.lista if m.id != id_actual}
            if codigo in codigos_usados:
                return "Ese código de materia ya está registrado"

        # Validar créditos entre 1 y 10
        if "creditos" in datos:
            try:
                creditos = int(datos["creditos"])
                if not (1 <= creditos <= 10):
                    return "Los créditos deben estar entre 1 y 10"
            except ValueError:
                return "Los créditos deben ser un número entero"

        # Validar cupos entre 0 y CUPOS_MAXIMOS
        if "cupos" in datos:
            try:
                cupos = int(datos["cupos"])
                if not (0 <= cupos <= Materia.CUPOS_MAXIMOS):
                    return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
            except ValueError:
                return "Los cupos deben ser un número entero"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_materia):
        for materia in self.lista:
            if materia.id == id_materia:
                return materia
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados

        for materia in self.lista:
            if texto in materia.nombre.lower() or texto in materia.codigo.lower():
                encontrados.append(materia)
        return encontrados

    def siguiente(self):
        mayor = 0
        for materia in self.lista:
            if materia.id > mayor:
                mayor = materia.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        
        materia = Materia(self.siguiente(),
                            str(datos["nombre"]).strip().title(),
                            str(datos["codigo"]).strip().upper(),
                            int(datos["creditos"]),
                            int(datos.get("cupos", 0)))         
        self.lista.append(materia)
        self.guardar()
        return True, f"materia creada: {materia.etiqueta()}"

    def actualizar(self, id_materia, datos):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"
        if not datos:
            return False, "No se indicó ningún cambio"

        desconocidos = set(datos) - {"nombre", "codigo", "cupos","creditos"}
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        error = self.validar(datos, id_materia)
        if error:
            return False, error

        if "nombre" in datos:
            materia.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos:
            materia.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos:
            materia.creditos = int(datos["creditos"])
        if "cupos" in datos:
            materia.cupos = int(datos["cupos"])

        self.guardar()
        return True, f"Materia {id_materia} actualizada"

    def eliminar(self, id_materia):
        materia = self.obtener(id_materia)
        if materia is None:
            return False, f"No existe una materia con id {id_materia}"

        self.lista.remove(materia)
        self.guardar()
        return True, f"Materia {id_materia} eliminada"
    
    def materias_sin_cupo(self):
        return [m for m in self.lista if m.cupos == 0]


# =====================================================================
# CONTROLADOR DE VENTAS
# =====================================================================
class MatriculaController(CrudBase):

    def __init__(self, estudiantes, materias, archivo="data/matricula.json"):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)

        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        self.gestor.guardar(datos)

    def validar(self, datos):
        try:
            estudiante_id = int(datos.get("estudiante_id", 0))
            materia_id = int(datos.get("materia_id", 0))
            periodo = int(datos.get("periodo", 0))
        except (TypeError, ValueError):
            return "estudiante_id, materia_id, periodo deben ser números enteros"

        # 1. El estudiante debe existir
        if self.estudiantes.obtener(estudiante_id) is None:
            return f"No existe un estudiante con id {estudiante_id}"

        # 2. La materia debe existir
        materia = self.materias.obtener(materia_id)
        if materia is None:
            return f"No existe una materia con id {materia_id}"

        # 3. La materia debe tener cupo (asumiendo que pedimos 1 cupo por matrícula)
        if not materia.hay_cupo():
            return f"La materia {materia.nombre} ya no tiene cupos disponibles"

        # 4. No se puede matricular dos veces al mismo estudiante en la misma materia y periodo
        for mat in self.lista:
            if mat.estudiante_id == estudiante_id and mat.materia_id == materia_id and mat.periodo == periodo:
                return "El estudiante ya está matriculado en esta materia para este periodo"

        return None

    def leer(self):
        return self.lista

    def obtener(self, id_matricula):
        for matricula in self.lista:
            if matricula.id == id_matricula:
                return matricula
        return None

    def buscar(self, texto):
        texto = texto.strip()
        encontradas = []
        if texto == "":
            return encontradas

        for matricula in self.lista:
            if texto in matricula.fecha:
                encontradas.append(matricula)
        return encontradas

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error

        materia = self.materias.obtener(int(datos["materia_id"]))
        
        matricula = Matricula(
            self.siguiente(),
            int(datos["estudiante_id"]),
            materia.id,
            int(datos["periodo"]),
            float(datos.get("nota", 0))
        )        

        # Ocupamos un cupo en la materia y guardamos los cambios en materias.json
        materia.ocupar_cupo()
        self.materias.guardar()

        self.lista.append(matricula)
        self.guardar()
        return True, f"Matrícula {matricula.id} registrada con éxito"

    def actualizar(self, id_matricula, datos):
        # Una matrícula registrada no se modifica por completo, pero sí podemos usarlo para registrar nota
        return False, "Utilice el método registrar_nota para actualizar la calificación"

    def eliminar(self, id_matricula):
        """Retirar matrícula: se borra y el cupo vuelve a la materia."""
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            materia.liberar_cupo()
            self.materias.guardar()

        self.lista.remove(matricula)
        self.guardar()
        return True, f"Matrícula {id_matricula} retirada y cupo devuelto"

    # --- MÉTODOS ESPECÍFICOS DE MATRÍCULAS ---

    def registrar_nota(self, id_matricula, nota):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return False, f"No existe la matrícula {id_matricula}"

        if not Materia.es_nota_valida(nota):
            return False, f"Nota inválida: '{nota}'"

        matricula.nota = float(nota)
        self.guardar()
        return True, f"Nota {nota} registrada para la matrícula {id_matricula}"

    def certificado(self, id_matricula):
        matricula = self.obtener(id_matricula)
        if matricula is None:
            return None

        estudiante = self.estudiantes.obtener(matricula.estudiante_id)
        materia = self.materias.obtener(matricula.materia_id)

        texto = f"CERTIFICADO DE MATRÍCULA #{matricula.id} · Fecha: {matricula.fecha}\n"
        texto += f"Estudiante: {estudiante.nombre_completo() if estudiante else 'Eliminado'}\n"
        texto += f"Materia   : {materia.nombre if materia else 'Eliminada'} ({materia.codigo if materia else 'N/A'})\n"
        texto += f"Periodo   : {matricula.periodo}\n"
        texto += "-" * 42 + "\n"
        texto += f"Nota final: {matricula.nota} - Estado: {matricula.estado()}"
        return texto

    def matriculas_por_estudiante(self):
        agrupadas = {}
        for matricula in self.lista:
            if matricula.estudiante_id not in agrupadas:
                agrupadas[matricula.estudiante_id] = []
            agrupadas[matricula.estudiante_id].append(matricula)
        return agrupadas

    def promedio_de_estudiante(self, estudiante_id):
        matriculas_est = [m for m in self.lista if m.estudiante_id == estudiante_id and m.nota > 0]
        if not matriculas_est:
            return 0.0
        suma = sum(m.nota for m in matriculas_est)
        return round(suma / len(matriculas_est), 2)
    