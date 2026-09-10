# -*- coding: utf-8 -*-
"""Fuente unica de los retos de "Que Imprime?" (Semana 4, Unidad 2).

Doce retos: 8 PREDICCIONES ("que imprime este programa?") intercaladas con
4 CHALLENGES de escribir codigo Python.

Los 4 challenges no son ejercicios inventados: son las piezas exactas de las
dos tareas de U2 que cierran el domingo 13-sep.
  C1 y C2 -> "Programacion con estilo de POO"  (clase CuentaBancaria)
  C3 y C4 -> "Clase Numero Entero"             (clase NumeroEntero, solo II24-FP2)

Al correr este archivo:
  1. ejecuta CADA programa en Python real y verifica que la opcion marcada
     como correcta sea de verdad lo que imprime;
  2. verifica que NINGUN distractor produzca la misma salida que la correcta
     (si no, el reto no distingue nada y hay que rediseniarlo);
  3. para cada challenge ejecuta TODA variante aceptada (deben dar la salida
     esperada) y TODA trampa (deben dar algo distinto, salvo las marcadas
     `misma_salida`, que corren bien pero violan la consigna de la tarea);
  4. escribe _datos.json.

    python3 _retos.py          -> verifica y regenera _datos.json
    python3 _retos.py --check   -> solo verifica (no escribe)

Sale con codigo 1 si algo no cuadra. Si tocas un reto, volve a correrlo.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))

# ══════════════════════════════════════════════════════════════════════
#  MOTOR: correr Python de verdad y quedarse con lo que imprime
# ══════════════════════════════════════════════════════════════════════

def correr(codigo):
    """Ejecuta el codigo en un subproceso y devuelve la salida como la ve
    el estudiante: lo que imprimio y, si revento, la ultima linea del
    traceback (que es la que se lee: 'AttributeError: ...')."""
    fd, ruta = tempfile.mkstemp(suffix=".py", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(codigo)
        p = subprocess.run([sys.executable, ruta], capture_output=True,
                           text=True, timeout=10)
    finally:
        os.unlink(ruta)
    partes = []
    if p.stdout.strip():
        partes.append(p.stdout.rstrip("\n"))
    if p.returncode != 0 and p.stderr.strip():
        lineas = [l for l in p.stderr.rstrip("\n").split("\n") if l.strip()]
        partes.append(lineas[-1].strip())
    return "\n".join(partes)


def norm(s):
    """Normalizacion para comparar codigo escrito a mano: sin espacios y con
    las comillas unificadas. Asi f'x' == f"x" y monto<=0 == monto <= 0.
    El juego (JS) usa exactamente esta misma regla."""
    return re.sub(r"\s+", "", (s or "")).replace("'", '"')


# ══════════════════════════════════════════════════════════════════════
#  PIEZAS DE CODIGO REUTILIZADAS
# ══════════════════════════════════════════════════════════════════════

MASCOTA = '''class Mascota:
    def __init__(self, nombre):
        self.nombre = nombre
        self._energia = 100

    @property
    def energia(self):
        return self._energia

    def jugar(self):
        self._energia -= 30
'''

RELOJ = '''class Reloj:
    def __init__(self, hora):
        self.__hora = hora
'''

RETOS = []


def prediccion(titulo, sub, codigo, opciones, correcta, porques):
    """opciones: lista de textos de salida. correcta: indice.
    porques: dict {indice: explicacion de por que ESA opcion es tentadora}."""
    RETOS.append(dict(tipo="prediccion", titulo=titulo, sub=sub, codigo=codigo,
                      opciones=opciones, correcta=correcta, porques=porques))


def challenge(titulo, sub, tarea, plantilla, huecos, esperado, trampas, pista_final):
    """huecos: lista de dicts {etiqueta, ayuda, acepta:[...], referencia}
    trampas: lista de dicts {codigo:[...por hueco...], porque, misma_salida?}"""
    RETOS.append(dict(tipo="challenge", titulo=titulo, sub=sub, tarea=tarea,
                      plantilla=plantilla, huecos=huecos, esperado=esperado,
                      trampas=trampas, pista_final=pista_final))


# ─────────────────────────────── 1 ───────────────────────────────
prediccion(
    "El nombre de la mascota",
    "Repaso de la Semana 3: cada objeto guarda sus propios datos.",
    MASCOTA + '''
firulais = Mascota("Firulais")
print(firulais.nombre)''',
    ["Firulais", "Mascota", "nombre",
     "AttributeError: 'Mascota' object has no attribute 'nombre'"],
    0,
    {1: "<code>Mascota</code> es la clase — el molde. Lo que imprimis es el dato guardado en el objeto.",
     2: "Eso seria el <em>nombre del atributo</em>, no su valor.",
     3: "Si existe: el constructor lo creo con <code>self.nombre = nombre</code>."})

# ─────────────────────────────── 2 ───────────────────────────────
prediccion(
    "Dos veces a jugar",
    "El metodo no devuelve nada, pero deja huella en el objeto.",
    MASCOTA + '''
firulais = Mascota("Firulais")
firulais.jugar()
firulais.jugar()
print(firulais.energia)''',
    ["40", "100", "70", "-60"],
    0,
    {1: "El estado del objeto <strong>si</strong> cambio: <code>jugar()</code> resto dos veces.",
     2: "Eso seria despues de <em>una</em> sola llamada. Fijate que hay dos.",
     3: "Arranca en 100, no en cero."})

# ─────────────────────────────── 3 ───────────────────────────────
challenge(
    "Las dos guardas de retirar()",
    "Escribi las dos condiciones que protegen el saldo. Es el paso 2 de la tarea.",
    "Programacion con estilo de POO",
    '''class CuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self._saldo = saldo_inicial

    def depositar(self, monto):
        self._saldo += monto

    def retirar(self, monto):
        if {0}:
            print("Monto invalido")
            return
        if {1}:
            print("Fondos insuficientes")
            return
        self._saldo -= monto

cuenta = CuentaBancaria("Ana", 500.0)
cuenta.depositar(250.0)
cuenta.retirar(100.0)
cuenta.retirar(1000.0)
cuenta.retirar(0.0)
cuenta.retirar(-50.0)
print(f"Saldo: Q{cuenta._saldo:.2f}")''',
    [
        dict(etiqueta="Rechazar monto invalido (cero o negativo)",
             ayuda="La condicion, sin el if ni los dos puntos. Ej: algo <= algo",
             acepta=["monto <= 0", "0 >= monto", "not monto > 0"],
             referencia="monto <= 0"),
        dict(etiqueta="Rechazar cuando no alcanza el saldo",
             ayuda="Acordate: el saldo protegido vive en self._saldo",
             acepta=["monto > self._saldo", "self._saldo < monto"],
             referencia="monto > self._saldo"),
    ],
    "Fondos insuficientes\nMonto invalido\nMonto invalido\nSaldo: Q650.00",
    [
        dict(codigo=["monto >= 0", "monto > self._saldo"],
             porque="Esa es <strong>la guarda invertida</strong> — la que salio mal en pantalla el martes. Con <code>&gt;= 0</code> rechazas TODO retiro valido: mira la salida, el retiro de Q100 nunca ocurrio."),
        dict(codigo=["monto <= 0", "monto < self._saldo"],
             porque="La segunda esta al reves: si el monto es <em>menor</em> al saldo, si alcanza. Estas rechazando justo los retiros buenos."),
        dict(codigo=["monto < 0", "monto > self._saldo"],
             porque="Casi, y el detalle es fino: con <code>&lt; 0</code> el retiro de <strong>cero</strong> se cuela como valido — contá los <code>Monto invalido</code> de la salida, falta uno. La tarea pide rechazar el cero tambien."),
        dict(codigo=["monto <= 0", "monto > self.saldo"],
             porque="El atributo lleva guion bajo: <code>self._saldo</code>. Asi como esta, el objeto no tiene ese atributo."),
    ],
    "Primera guarda: el monto tiene que ser positivo. Segunda: no se saca mas de lo que hay.")

# ─────────────────────────────── 4 ───────────────────────────────
prediccion(
    "Dos mascotas con el mismo nombre",
    "Se llaman igual. Son la misma?",
    MASCOTA + '''
firulais = Mascota("Firulais")
otra = Mascota("Firulais")
print(firulais is otra, firulais.nombre == otra.nombre)''',
    ["False True", "True True", "False False", "True False"],
    0,
    {1: "<code>is</code> pregunta si son el <em>mismo objeto en memoria</em>, no si se parecen. Son dos galletas distintas del mismo molde.",
     2: "Los nombres si son iguales: los dos dicen \"Firulais\".",
     3: "Justo al reves de lo que pasa."})

# ─────────────────────────────── 5 ───────────────────────────────
prediccion(
    "Meterle mano a la energia",
    "El pilar de hoy, en una linea.",
    MASCOTA + '''
firulais = Mascota("Firulais")
firulais.energia = 999
print(firulais.energia)''',
    None,   # se llena con la salida real + distractores
    0,
    {1: "Ese seria el resultado si <code>energia</code> fuera un atributo comun. Es un <code>@property</code> de solo lectura.",
     2: "No llega a imprimir: revienta en la linea de la asignacion.",
     3: "El property no ignora la asignacion en silencio — la rechaza con error."})

# ─────────────────────────────── 6 ───────────────────────────────
challenge(
    "El saldo, bien presentado",
    "El formato exacto que pide la tarea. Es donde se cae la mitad de las entregas.",
    "Programacion con estilo de POO",
    '''class CuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self._saldo = saldo_inicial

    def mostrar_saldo(self):
        print({0})

cuenta = CuentaBancaria("Ana", 650.0)
cuenta.mostrar_saldo()''',
    [
        dict(etiqueta="Lo que va dentro del print()",
             ayuda='Tiene que salir exactamente:  Titular: Ana | Saldo: Q650.00',
             acepta=[
                 'f"Titular: {self.titular} | Saldo: Q{self._saldo:.2f}"',
                 'f"Titular: {self.titular} | Saldo: Q{round(self._saldo, 2):.2f}"',
                 '"Titular: {} | Saldo: Q{:.2f}".format(self.titular, self._saldo)',
                 '"Titular: " + self.titular + " | Saldo: Q" + format(self._saldo, ".2f")',
                 '"Titular: " + self.titular + " | Saldo: Q" + f"{self._saldo:.2f}"',
             ],
             referencia='f"Titular: {self.titular} | Saldo: Q{self._saldo:.2f}"'),
    ],
    "Titular: Ana | Saldo: Q650.00",
    [
        dict(codigo=['f"Titular: {self.titular} | Saldo: Q{self._saldo}"'],
             porque="Sin <code>:.2f</code> Python imprime <code>650.0</code>, con un solo decimal. La tarea pide dos: <code>Q650.00</code>."),
        dict(codigo=['f"Titular: {titular} | Saldo: Q{self._saldo:.2f}"'],
             porque="Falta <code>self.</code>: dentro del metodo no existe ninguna variable suelta llamada <code>titular</code>."),
        dict(codigo=['f"Titular: {self.titular} - Saldo: Q{self._saldo:.2f}"'],
             porque="El separador que pide la tarea es la barra vertical <code>|</code>, no un guion. El formato se califica al caracter."),
    ],
    'Una f-string con los dos datos del objeto, y <code>:.2f</code> para forzar los dos decimales.')

# ─────────────────────────────── 7 ───────────────────────────────
prediccion(
    "La guarda al reves",
    "Este programa esta mal a proposito. Que hace de malo, exactamente?",
    '''class Cuenta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self._saldo = saldo

    def retirar(self, monto):
        if monto >= 0:                    # <-- ojo aqui
            print("Rechazado: monto invalido")
            return
        self._saldo -= monto

c = Cuenta("Mary", 1000.0)
c.retirar(200.0)
print(c._saldo)''',
    None,
    0,
    {1: "Eso seria con la guarda correcta (<code>monto &lt;= 0</code>): el retiro pasaria y descontaria.",
     2: "El saldo no sube: nadie deposito nada.",
     3: "No hay error de Python. El programa corre feliz — y por eso el bug es peligroso."})

# ─────────────────────────────── 8 ───────────────────────────────
prediccion(
    "El metodo con guion bajo, desde afuera",
    "Protegido... hasta donde?",
    '''class Cajero:
    def __init__(self, efectivo):
        self._efectivo = efectivo

    def _contar_billetes(self):
        return self._efectivo // 100

cajero = Cajero(2550)
print(cajero._contar_billetes())''',
    ["25", "AttributeError: metodo privado", "2550", "25.5"],
    0,
    {1: "En Python el guion bajo <strong>no bloquea nada</strong>. Es una senial entre programadores: \"esto es interno, no lo toques\".",
     2: "Eso seria el efectivo completo, sin dividir.",
     3: "<code>//</code> es division entera: devuelve <code>25</code>, no <code>25.5</code>."})

# ─────────────────────────────── 9 ───────────────────────────────
challenge(
    "es_impar sin repetir la logica",
    "Punto 1 de la tarea del Numero Entero: reusa es_par(), no copies la formula.",
    "Clase Numero Entero",
    '''class NumeroEntero:
    def __init__(self, valor):
        self.valor = valor

    def es_par(self):
        return self.valor % 2 == 0

    def es_impar(self):
        return {0}

print(NumeroEntero(7).es_impar(), NumeroEntero(12).es_impar())''',
    [
        dict(etiqueta="Lo que devuelve es_impar()",
             ayuda="Preguntale al propio objeto si es par, y devolve lo contrario.",
             acepta=["not self.es_par()", "self.es_par() == False",
                     "not self.es_par() == True"],
             referencia="not self.es_par()"),
    ],
    "True False",
    [
        dict(codigo=["self.es_par()"],
             porque="Eso devuelve lo <em>mismo</em> que <code>es_par()</code>, no lo contrario. Falta el <code>not</code>."),
        dict(codigo=["self.valor % 2 == 1"],
             misma_salida=True,
             porque="Corre y da la salida correcta, <strong>pero la tarea pide reusar <code>es_par()</code></strong>, no repetir la formula. Ademas con negativos te sorprende: <code>-3 % 2</code> da <code>1</code> en Python, pero en otros lenguajes da <code>-1</code>. Reusar el metodo te evita ese hoyo."),
        dict(codigo=["not es_par()"],
             porque="Sin <code>self.</code> Python no sabe a que objeto le estas preguntando."),
    ],
    "Un <code>not</code> delante de la pregunta que ya sabe responder el objeto.")

# ─────────────────────────────── 10 ───────────────────────────────
prediccion(
    "La puerta de servicio",
    "Aqui el atributo lleva DOS guiones bajos. Fijate en como se pide desde afuera.",
    RELOJ + '''
reloj = Reloj(7)
print(reloj._Reloj__hora)''',
    ["7", "AttributeError: 'Reloj' object has no attribute '_Reloj__hora'",
     "None", "_Reloj__hora"],
    0,
    {1: "Si existe con ese nombre: Python le cambio el nombre por dentro (<em>name mangling</em>) a <code>_Reloj__hora</code>.",
     2: "El constructor le puso 7.",
     3: "Eso imprimiria el texto, no el valor."})

# ─────────────────────────────── 11 ───────────────────────────────
prediccion(
    "Y ahora por su nombre original",
    "El mismo objeto del reto anterior, pedido como uno esperaria.",
    RELOJ + '''
reloj = Reloj(7)
print(reloj.__hora)''',
    None,
    0,
    {1: "Por ese nombre no: Python lo renombro a <code>_Reloj__hora</code> al compilar la clase.",
     2: "No es que devuelva vacio — revienta.",
     3: "Python no tiene atributos privados de verdad; tiene <em>name mangling</em>."})

# ─────────────────────────────── 12 ───────────────────────────────
challenge(
    "Contar digitos, con signo y todo",
    "Punto 1 de la tarea del Numero Entero: -305 tiene 3 digitos, no 4 ni 0.",
    "Clase Numero Entero",
    '''class NumeroEntero:
    def __init__(self, valor):
        self.valor = valor

    def cantidad_digitos(self):
        n = {0}
        cuenta = 0
        while n > 0:
            n = n // 10
            cuenta += 1
        return cuenta

print(NumeroEntero(-305).cantidad_digitos(), NumeroEntero(7).cantidad_digitos())''',
    [
        dict(etiqueta="Con que arranca n",
             ayuda="El ciclo solo avanza mientras n > 0. Que le pasa a un negativo?",
             acepta=["abs(self.valor)", "abs(self. valor)"],
             referencia="abs(self.valor)"),
    ],
    "3 1",
    [
        dict(codigo=["self.valor"],
             porque="Con <code>-305</code> el <code>while n &gt; 0</code> no arranca ni una vez y te devuelve <code>0</code>. Hay que quitarle el signo primero."),
        dict(codigo=["len(str(self.valor))"],
             porque="Cuenta el signo <code>-</code> como si fuera un digito: te da <code>4</code> para <code>-305</code>. Y la tarea pide contar con un ciclo."),
        dict(codigo=["valor"],
             porque="Sin <code>self.</code> no existe esa variable dentro del metodo."),
    ],
    "Una funcion de Python que devuelve el valor absoluto.")


# ══════════════════════════════════════════════════════════════════════
#  VERIFICACION
# ══════════════════════════════════════════════════════════════════════

FALLAS = []


def falla(msg):
    FALLAS.append(msg)
    print("  \033[31mFALLA\033[0m  " + msg)


def rellenar(plantilla, valores):
    out = plantilla
    for i, v in enumerate(valores):
        out = out.replace("{%d}" % i, v)
    return out


def verificar():
    for n, r in enumerate(RETOS, 1):
        et = "%2d. %s" % (n, r["titulo"])

        # ---------- PREDICCIONES ----------
        if r["tipo"] == "prediccion":
            real = correr(r["codigo"])
            if r["opciones"] is None:
                falla(et + " -> opciones=None y no se autogeneraron")
                continue
            if r["correcta"] != 0:
                falla(et + " -> por convencion la correcta se declara en el indice 0")
            if r["opciones"][r["correcta"]] != real:
                falla(et + " -> la opcion correcta no es lo que imprime.\n"
                      "         declarada: %r\n         real:      %r"
                      % (r["opciones"][r["correcta"]], real))
                continue
            for i, o in enumerate(r["opciones"]):
                if i != r["correcta"] and o == real:
                    falla(et + " -> el distractor %d es igual a la correcta: %r" % (i, o))
            if len(set(r["opciones"])) != len(r["opciones"]):
                falla(et + " -> hay opciones repetidas")
            for i in range(len(r["opciones"])):
                if i != r["correcta"] and str(i) not in {str(k) for k in r["porques"]}:
                    falla(et + " -> al distractor %d le falta su explicacion" % i)
            print("  ok    " + et + "  ->  %r" % (real if len(real) < 60 else real[:57] + "..."))

        # ---------- CHALLENGES ----------
        else:
            n_huecos = len(set(re.findall(r"\{(\d+)\}", r["plantilla"])))
            if n_huecos != len(r["huecos"]):
                falla(et + " -> la plantilla tiene %d huecos y se declararon %d"
                      % (n_huecos, len(r["huecos"])))
                continue

            # la referencia debe dar la salida esperada
            ref = [h["referencia"] for h in r["huecos"]]
            real = correr(rellenar(r["plantilla"], ref))
            if real != r["esperado"]:
                falla(et + " -> la solucion de referencia no da lo esperado.\n"
                      "         esperado: %r\n         real:     %r" % (r["esperado"], real))
                continue

            # toda variante aceptada debe dar la salida esperada
            for i, h in enumerate(r["huecos"]):
                if h["referencia"] not in h["acepta"]:
                    falla(et + " -> hueco %d: la referencia no esta en acepta[]" % i)
                for var in h["acepta"]:
                    combo = list(ref)
                    combo[i] = var
                    got = correr(rellenar(r["plantilla"], combo))
                    if got != r["esperado"]:
                        falla(et + " -> hueco %d: la variante aceptada %r no da lo esperado.\n"
                              "         real: %r" % (i, var, got))

            # normalizaciones no pueden chocar entre huecos distintos
            vistos = {}
            for i, h in enumerate(r["huecos"]):
                for var in h["acepta"]:
                    k = norm(var)
                    if k in vistos and vistos[k] != i:
                        falla(et + " -> %r se acepta en dos huecos distintos" % var)
                    vistos[k] = i

            # las trampas deben dar algo DISTINTO (salvo las marcadas)
            for t in r["trampas"]:
                if len(t["codigo"]) != len(r["huecos"]):
                    falla(et + " -> la trampa %r no trae un valor por hueco" % t["codigo"])
                    continue
                got = correr(rellenar(r["plantilla"], t["codigo"]))
                igual = (got == r["esperado"])
                if igual and not t.get("misma_salida"):
                    falla(et + " -> la trampa %r produce la MISMA salida que la correcta: "
                          "no distingue nada" % t["codigo"])
                if not igual and t.get("misma_salida"):
                    falla(et + " -> la trampa %r esta marcada misma_salida pero da %r"
                          % (t["codigo"], got))
                t["salida"] = got
                # una trampa tiene que fallar en AL MENOS un hueco: si todos sus
                # valores estan aceptados, entonces no es una trampa, es una solucion
                todos_ok = all(
                    norm(t["codigo"][i]) in {norm(a) for a in h["acepta"]}
                    for i, h in enumerate(r["huecos"]))
                if todos_ok and not t.get("misma_salida"):
                    falla(et + " -> la trampa %r es en realidad una solucion valida "
                          "en todos sus huecos" % t["codigo"])
            print("  ok    " + et + "  ->  %d hueco(s), %d variante(s), %d trampa(s)"
                  % (len(r["huecos"]),
                     sum(len(h["acepta"]) for h in r["huecos"]),
                     len(r["trampas"])))


def autogenerar_opciones():
    """Los retos con opciones=None son los que dependen del mensaje exacto de
    error de Python. Se corre el programa y la salida real se pone de primera;
    los distractores se declaran aqui, al lado, para que se lean juntos."""
    distractores = {
        "Meterle mano a la energia": ["999", "100", "(no imprime nada)"],
        "La guarda al reves": ["Rechazado: monto invalido\n800.0",
                               "Rechazado: monto invalido\n1200.0",
                               "TypeError: unsupported operand type(s)"],
        "Y ahora por su nombre original": ["7", "None", "_Reloj__hora"],
    }
    for r in RETOS:
        if r["tipo"] == "prediccion" and r["opciones"] is None:
            real = correr(r["codigo"])
            d = distractores.get(r["titulo"])
            if d is None:
                falla("sin distractores declarados para %r" % r["titulo"])
                r["opciones"] = [real]
            else:
                r["opciones"] = [real] + d
            r["correcta"] = 0


def barajar_opciones():
    """Los retos se declaran con la correcta en el indice 0 para poder leerlos.
    Si se publicaran asi, la respuesta seria siempre la A. Aca se permutan con
    una semilla fija derivada del titulo: el orden queda mezclado pero es el
    MISMO para todos los estudiantes, que es lo que permite compararse entre si."""
    import random
    for r in RETOS:
        if r["tipo"] != "prediccion":
            continue
        n = len(r["opciones"])
        orden = list(range(n))
        random.Random(r["titulo"]).shuffle(orden)      # orden[nuevo] = viejo
        r["opciones"] = [r["opciones"][v] for v in orden]
        r["porques"] = {str(nuevo): r["porques"][v]
                        for nuevo, v in enumerate(orden) if v in r["porques"]}
        r["correcta"] = orden.index(0)
    posiciones = [r["correcta"] for r in RETOS if r["tipo"] == "prediccion"]
    print("\n  posicion de la correcta: %s"
          % " ".join("ABCD"[p] for p in posiciones))
    if len(set(posiciones)) < 3:
        falla("las correctas quedaron concentradas en %d posicion(es) distintas"
              % len(set(posiciones)))


def main():
    solo_check = "--check" in sys.argv
    print("\n\033[1mQue Imprime? — verificacion contra Python %s\033[0m\n"
          % sys.version.split()[0])
    autogenerar_opciones()
    verificar()
    barajar_opciones()

    preds = sum(1 for r in RETOS if r["tipo"] == "prediccion")
    chals = len(RETOS) - preds
    print("\n  %d retos: %d predicciones + %d challenges" % (len(RETOS), preds, chals))

    if FALLAS:
        print("\n\033[31m%d falla(s). No se escribio _datos.json.\033[0m\n" % len(FALLAS))
        return 1

    if solo_check:
        print("\n\033[32mOK\033[0m — todo verificado (--check: no se escribio nada)\n")
        return 0

    datos = {"retos": RETOS, "python": sys.version.split()[0]}

    salida = os.path.join(AQUI, "_datos.json")
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print("\n  escrito _datos.json")

    # _cuerpo.html = _plantilla.html con los datos inyectados.
    # La plantilla es lo que se edita a mano; _cuerpo.html es generado.
    plantilla = os.path.join(AQUI, "_plantilla.html")
    if os.path.exists(plantilla):
        with open(plantilla, encoding="utf-8") as f:
            html = f.read()
        marca = "/*__DATOS__*/"
        if marca not in html:
            print("\n\033[31mFALLA\033[0m — _plantilla.html no trae la marca %s\n" % marca)
            return 1
        html = html.replace(marca, json.dumps(datos, ensure_ascii=False))
        destino = os.path.join(AQUI, "_cuerpo.html")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        print("  escrito _cuerpo.html (%.1f KB)" % (len(html.encode("utf-8")) / 1024.0))

    print("\n\033[32mOK\033[0m — todo verificado y regenerado\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
