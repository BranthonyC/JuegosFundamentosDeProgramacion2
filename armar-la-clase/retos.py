# -*- coding: utf-8 -*-
"""Fuente unica de los retos de "Arma la Clase".
Genera el JS y verifica ejecutando cada combinacion posible en Python real."""

P = []   # rompecabezas de codigo
def p(titulo, sub, plantilla, piezas, solucion, pistas):
    P.append(dict(tipo="codigo", titulo=titulo, sub=sub, plantilla=plantilla,
                  piezas=piezas, solucion=solucion, pistas=pistas))

p("La ficha del estudiante",
  "Completá la clase para que CADA estudiante guarde su propio nombre y carné.",
  'class Estudiante:\n    def __init__({0}, nombre, carne):\n        {1} = nombre\n        self.carne = carne\n\n    def presentarse({0}):\n        return f"Soy {self.nombre}, carne {self.carne}"\n\nana = Estudiante("Ana", "202612345")\nluis = Estudiante("Luis", "202698765")\nprint(ana.presentarse())\nprint(luis.presentarse())',
  ["self", "self.nombre", "nombre", "Estudiante.nombre"], [0, 1],
  {"2": "Sin <code>self.</code> guardás una variable local que se pierde al terminar el constructor.",
   "3": "Eso lo guarda en la CLASE, así que los dos estudiantes lo comparten. Mirá la salida: los dos se llaman igual."})

p("Crear la galleta, no el molde",
  "Falta fabricar el objeto y pedirle que actúe.",
  'class Perro:\n    def __init__(self, nombre):\n        self.nombre = nombre\n\n    def ladrar(self):\n        return f"{self.nombre} dice guau"\n\nfirulais = {0}\nprint({1})',
  ["Perro(\"Firulais\")", "firulais.ladrar()", "Perro", "Perro.ladrar()"], [0, 1],
  {"2": "Sin paréntesis no fabricás nada: le estás dando el molde a la variable.",
   "3": "Llamado desde la clase le falta el objeto. ¿A quién le pedís que ladre?"})

p("La cuenta de doña Mary",
  "El saldo va protegido y el retiro debe rechazar lo que no alcanza.",
  'class Cuenta:\n    def __init__(self, titular, saldo):\n        self.titular = titular\n        {0} = saldo\n\n    def retirar(self, monto):\n        if {1}:\n            print("Fondos insuficientes")\n            return\n        self._saldo -= monto\n\n    def mostrar(self):\n        print(f"{self.titular}: Q{self._saldo:.2f}")\n\nc = Cuenta("Mary", 500.0)\nc.retirar(1000.0)\nc.retirar(100.0)\nc.mostrar()',
  ["self._saldo", "monto > self._saldo", "self.saldo", "monto < self._saldo"], [0, 1],
  {"2": "El enunciado pide el saldo <em>protegido</em>: lleva guion bajo.",
   "3": "Al revés: si el monto es menor al saldo, sí alcanza."})

p("El producto de la tienda",
  "Vender descuenta del inventario, y el valor total se calcula: no se imprime.",
  'class Producto:\n    def __init__(self, nombre, precio, cantidad):\n        self.nombre = nombre\n        self.precio = precio\n        self.cantidad = cantidad\n\n    def vender(self, unidades):\n        self.cantidad {0} unidades\n\n    def valor_inventario(self):\n        {1} self.precio * self.cantidad\n\nazucar = Producto("Azucar", 7.5, 24)\nazucar.vender(4)\nprint(f"{azucar.nombre}: {azucar.cantidad} en bodega")\nprint(f"Valor: Q{azucar.valor_inventario():.2f}")',
  ["-=", "return", "+=", "print"], [0, 1],
  {"2": "Vender <em>quita</em> unidades, no las suma.",
   "3": "Si imprime en vez de devolver, no podés usar el resultado para sumar."})

p("Enseñale a presentarse",
  "El método __str__ tiene que DEVOLVER el texto para que print lo use.",
  'class Punto:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        {0} f"({self.x}, {self.y})"\n\np = Punto(3, 4)\n{1}',
  ["return", "print(p)", "print", "str(p)"], [0, 1],
  {"2": "<code>print</code> sin paréntesis no es válido ahí. Además <code>__str__</code> devuelve, no imprime.",
   "3": "Convierte a texto pero no muestra nada. Falta imprimirlo."})

p("Un método que reutiliza a otro",
  "es_impar no debe repetir la lógica: preguntale a es_par y devolvé lo contrario.",
  'class Numero:\n    def __init__(self, valor):\n        self.valor = valor\n\n    def es_par(self):\n        return self.valor % 2 == 0\n\n    def es_impar(self):\n        return {0}\n\nn = Numero(7)\nprint(n.es_par(), {1})',
  ["not self.es_par()", "n.es_impar()", "self.es_par()", "es_impar()"], [0, 1],
  {"2": "Eso devuelve lo mismo que es_par, no lo contrario. Falta el <code>not</code>.",
   "3": "Sin objeto delante, Python no sabe de quién es ese método."})

p("El IVA que todos comparten",
  "El IVA vive en la clase: si cambia, cambia para TODOS los productos.",
  'class Producto:\n    iva = 0.12\n\n    def __init__(self, nombre, precio):\n        self.nombre = nombre\n        self.precio = precio\n\n    def con_iva(self):\n        return {0} * (1 + Producto.iva)\n\na = Producto("Azucar", 10.0)\nb = Producto("Frijol", 20.0)\n{1} = 0.15\nprint(f"{a.con_iva():.2f} {b.con_iva():.2f}")',
  ["self.precio", "Producto.iva", "precio", "a.iva"], [0, 1],
  {"2": "No existe ninguna variable suelta con ese nombre dentro del metodo.",
   "3": "Eso se lo cambia solo a <em>a</em>. Mirá: el frijol se queda con el IVA viejo."})

p("Frío o no frío",
  "Convertir a Fahrenheit y decidir con el dato del propio objeto.",
  'class Termometro:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    def a_fahrenheit(self):\n        return {0}\n\n    def describir(self):\n        if {1}:\n            return "hace frio"\n        return "no hace frio"\n\nt = Termometro(10)\ncalor = Termometro(30)\nprint(t.a_fahrenheit())\nprint(t.describir())\nprint(calor.describir())',
  ["self.celsius * 9/5 + 32", "self.celsius < 15", "celsius * 9/5 + 32", "self.celsius > 15"], [0, 1],
  {"2": "Falta <code>self.</code>: el dato vive en el objeto.",
   "3": "Al revés. Con 10 grados hace frío, no calor."})

p("El carrito de la tienda",
  "Agregar mete el precio en la lista del objeto, y el total se le pide al carrito.",
  'class Carrito:\n    def __init__(self):\n        self.items = []\n\n    def agregar(self, precio):\n        {0}\n\n    def total(self):\n        return sum(self.items)\n\nc = Carrito()\nc.agregar(10.5)\nc.agregar(4.5)\nprint({1})',
  ["self.items.append(precio)", "c.total()", "items.append(precio)", "Carrito.total()"], [0, 1],
  {"2": "Sin <code>self.</code> no existe esa lista dentro del método.",
   "3": "Llamado desde la clase no sabe de qué carrito hablás."})

p("Contar los dígitos",
  "Con -305 tiene que dar 3: el signo no es un dígito.",
  'class Entero:\n    def __init__(self, valor):\n        self.valor = valor\n\n    def cantidad_digitos(self):\n        n = {0}\n        cuenta = 0\n        while n > 0:\n            n = n // 10\n            cuenta {1} 1\n        return cuenta\n\nprint(Entero(-305).cantidad_digitos())\nprint(Entero(7).cantidad_digitos())',
  ["abs(self.valor)", "+=", "self.valor", "-="], [0, 1],
  {"2": "Con un negativo el ciclo nunca arranca y te devuelve 0. Hay que quitarle el signo.",
   "3": "Estás restando: el contador se va a negativo."})

p("Dos objetos, dos vidas",
  "Que cada parqueo lleve su propia cuenta y no la comparta con el otro.",
  'class Parqueo:\n    def __init__(self, nombre, capacidad):\n        self.nombre = nombre\n        self.capacidad = capacidad\n        {0} = 0\n\n    def entrar(self):\n        if self.ocupados >= self.capacidad:\n            print(f"{self.nombre}: lleno")\n            return\n        self.ocupados += 1\n\n    def libres(self):\n        return {1}\n\noakland = Parqueo("Oakland", 2)\npradera = Parqueo("Pradera", 5)\noakland.entrar()\noakland.entrar()\noakland.entrar()\nprint(f"Oakland libres: {oakland.libres()}")\nprint(f"Pradera libres: {pradera.libres()}")',
  ["self.ocupados", "self.capacidad - self.ocupados", "ocupados", "self.ocupados - self.capacidad"], [0, 1],
  {"2": "Sin <code>self.</code> el contador se pierde al salir del constructor.",
   "3": "Te da negativo. Los libres son capacidad menos ocupados."})

C = []   # clasificacion tiene / hace
def c(titulo, sub, palabras):
    C.append(dict(tipo="clasif", titulo=titulo, sub=sub, palabras=palabras))

c("Un carro en un videojuego", "¿Qué TIENE el carro y qué HACE?",
  [["color","prop"],["velocidad","prop"],["acelerar()","met"],["placa","prop"],
   ["frenar()","met"],["tocar_bocina()","met"],["marca","prop"]])
c("Una cuenta bancaria", "La misma clase que armaste hace un par de retos.",
  [["titular","prop"],["depositar()","met"],["saldo","prop"],["retirar()","met"],
   ["numero_de_cuenta","prop"],["mostrar_saldo()","met"]])
c("Un estudiante de la UDV", "Ojo con las que parecen acción pero son dato.",
  [["carne","prop"],["inscribirse()","met"],["promedio","prop"],["entregar_tarea()","met"],
   ["carrera","prop"],["calcular_zona()","met"],["semestre","prop"]])
c("Tu celular", "Lo que traés en la bolsa, modelado como objeto.",
  [["modelo","prop"],["bateria","prop"],["llamar()","met"],["sacar_foto()","met"],
   ["color","prop"],["reiniciar()","met"]])
c("La tienda de doña Mary", "El negocio completo, no solo un producto.",
  [["nombre","prop"],["direccion","prop"],["vender()","met"],["inventario","prop"],
   ["reabastecer()","met"],["calcular_ganancia()","met"]])
c("Un parqueo", "El mismo del último rompecabezas.",
  [["capacidad","prop"],["ocupados","prop"],["entrar()","met"],["salir()","met"],
   ["tarifa_por_hora","prop"],["lugares_libres()","met"]])
c("Un libro de la biblioteca", "Cuidado: 'esta_disponible()' responde una pregunta, pero es acción.",
  [["titulo","prop"],["autor","prop"],["prestar()","met"],["isbn","prop"],
   ["devolver()","met"],["esta_disponible()","met"]])
c("La tarjeta del Transmetro", "La del reto opcional de la semana.",
  [["saldo","prop"],["pin","prop"],["recargar()","met"],["pagar_pasaje()","met"],
   ["numero","prop"],["cambiar_pin()","met"]])
c("Un perro", "El clásico, para cerrar.",
  [["nombre","prop"],["raza","prop"],["ladrar()","met"],["edad","prop"],
   ["correr()","met"],["comer()","met"]])

# intercalado: codigo, clasif, codigo, clasif... y al final los codigos que sobran
RETOS = []
i = j = 0
while i < len(P) or j < len(C):
    if i < len(P): RETOS.append(P[i]); i += 1
    if j < len(C): RETOS.append(C[j]); j += 1
