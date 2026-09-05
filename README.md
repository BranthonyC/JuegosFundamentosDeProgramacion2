# Juegos · Fundamentos de Programación 2

Dos juegos para entender **programación orientada a objetos** con Python, del curso
Fundamentos de Programación 2 de la **Universidad Da Vinci de Guatemala**.

Corren enteros en el navegador. **No hay servidor y no se envía nada a ninguna parte:**
tu nombre y tu avance viven solo en tu equipo, en `localStorage`.

| Juego | Qué practica |
|---|---|
| 🍪 [**Molde o Galleta**](molde-o-galleta/) — 25 tarjetas | Distinguir la **clase** (el molde) del **objeto** (la galleta) |
| 🧩 [**Armá la Clase**](armar-la-clase/) — 20 retos | Armar una clase pieza por pieza y separar **propiedades** de **métodos** |

---

## Cómo abrirlos

**En línea:** [codersatelier.com/college/fundamentos-2](https://codersatelier.com/college/fundamentos-2)

**En tu máquina:** cloná el repo y abrí `index.html` con doble clic. No hay que instalar nada
ni levantar ningún servidor — es HTML, CSS y JavaScript, en un solo archivo por juego.

```
git clone https://github.com/BranthonyC/JuegosFundamentosDeProgramacion2.git
```

---

## Cómo está armado

Cada juego es **un solo archivo** `index.html` con todo adentro: el marcado, los estilos y la
lógica. Nada de frameworks. Si querés ver cómo funciona algo, abrilo con tu editor y buscalo —
está todo ahí, en unas 600 líneas.

```
.
├── index.html                  portada con los dos juegos
├── molde-o-galleta/
│   └── index.html              el juego completo
└── armar-la-clase/
    ├── index.html              el juego completo
    └── retos.py                los 20 retos + su verificador
```

### `armar-la-clase/retos.py` — el archivo más interesante del repo

Los 20 retos **no se escriben a mano dentro del HTML**. Se definen en este archivo de Python,
que además **los verifica ejecutándolos de verdad** y recién entonces genera el JavaScript.

Cada rompecabezas tiene 2 huecos y 4 piezas, o sea **16 combinaciones posibles**. El script las
corre todas —176 en total— y exige que se cumplan tres cosas:

1. La combinación correcta **corre sin error**.
2. La combinación correcta **imprime algo**.
3. **Ninguna combinación incorrecta produce la misma salida** que la correcta.

Si algo de eso falla, el script sale con error y no genera nada.

> **Esa tercera regla atrapó dos retos que parecían bien.** En el del IVA, `self.iva` y
> `Producto.iva` *leen exactamente lo mismo*, así que ese hueco no distinguía nada. Y en el del
> termómetro, meter la fórmula de Fahrenheit dentro de un `if` daba `50.0`, que en Python es
> *truthy* — o sea que producía la respuesta correcta **por accidente**. Ninguno de los dos se
> veía a simple vista.

Si querés proponer un reto nuevo, agregalo ahí y volvé a correr el archivo: te dice si tu reto
se sostiene.

### Por qué el botón dice «Calificar» y no «Ejecutar»

La primera versión cargaba **Pyodide** (Python compilado a WebAssembly) para ejecutar el código
en vivo. Funcionaba, pero se quedaba colgada en algunos entornos: la política de seguridad del
navegador dejaba pasar el archivo `.js` pero **bloqueaba el `.wasm` que Pyodide descarga
después**, y la función que lo carga **se queda esperando en vez de fallar** — así que el
mensaje «Ejecutando…» no se iba nunca.

La solución no fue simular la salida. Fue **precalcular las 176 combinaciones ejecutándolas en
Python real** y guardar la salida o el error exacto de cada una. Cuando calificás tu armado, lo
que ves es el `SyntaxError` o el `AttributeError` auténtico que Python devolvería — solo que
calculado de antemano. Cero descargas, respuesta instantánea, y funciona sin conexión.

### El código de verificación

Al terminar, cada juego muestra un código de 6 caracteres. Sale de aplicar la función hash
**djb2** a `nombre + puntaje + fecha` y escribirla en base 36:

```js
var s = nombre.trim().toLowerCase() + "|" + aciertos + "|" + fecha;  // "2026-09-04"
var h = 5381;
for (var i = 0; i < s.length; i++) h = ((h * 33) ^ s.charCodeAt(i)) >>> 0;
var codigo = h.toString(36).toUpperCase().slice(0, 6);
```

No es criptografía y no pretende serlo: es un **dígito verificador**. Sirve para que editar el
puntaje en una captura sea incómodo, porque el código dejaría de cuadrar. Con los mismos tres
datos, cualquiera puede recalcularlo.

*(Detalle que cuesta una hora si no lo sabés: en tipografía monoespaciada el `0` y la `O` se
parecen mucho. Al comparar códigos a ojo, conviene tratarlos como equivalentes.)*

### El PDF de entrega

Al terminar podés escribir tu respuesta y bajar un PDF ya armado, con tu cabecera y tu
resultado. Se genera con [jsPDF](https://github.com/parallax/jsPDF) **dibujando el documento con
primitivas** —texto, rectángulos— en vez de tomarle una foto a la pantalla. Por eso pesa poco y
el texto se puede seleccionar y buscar.

---

## Para el que quiera hurgar

Algunas cosas del código que valen la pena mirar, si estás aprendiendo:

- **Todo funciona a toques, no solo arrastrando.** El *drag and drop* del navegador es incómodo
  en celular, así que cada pieza también se puede tocar para seleccionar y tocar el hueco para
  soltar. Buscá `addEventListener("click"` al lado de `dragstart`.
- **El tema claro/oscuro** se resuelve solo con variables CSS y `prefers-color-scheme`. No hay
  JavaScript decidiendo colores; el botón de tema solo escribe un atributo en `<html>`.
- **Nada se pierde si cerrás la pestaña.** El avance se guarda en `localStorage` en cada
  respuesta, y al volver te ofrece continuar. Fijate que **cada lectura y escritura va dentro de
  un `try`**: en modo incógnito o con las cookies bloqueadas, `localStorage` lanza excepción, y
  un juego que no lo contempla se cae al abrir.

---

## Licencia

[MIT](LICENSE) — usalo, copialo, adaptalo para tu curso. Si te sirve, avisame.

**Ing. Brandon Antony Chitay Coutiño**
Facultad de Ingeniería, Informática y Tecnología · Universidad Da Vinci de Guatemala
