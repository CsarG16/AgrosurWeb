# Versión en chino de la web de Agro Sur Latino

**Para:** dirección de Agro Sur Latino S.A.C.
**Preparado por:** equipo web (Sumak Soporte S.A.C.)
**Fecha:** noviembre 2026

---

## 1. Resumen

Tener la web en chino **no es solo traducir los textos**. Para que un comprador en China continental pueda usar la página, también hay que tener en cuenta que varios servicios que hoy usa la web **están bloqueados en China**: Google (fuentes y mapas), YouTube y WhatsApp. Si solo traducimos, la página en China cargaría lenta, el video no se vería y el botón de contacto no funcionaría.
ón | Con inteligencia artificial, con controles de calidad (ver sección 6) |

---

## 2. Qué haremos nosotros en la web

1. **Agregar el chino como tercer idioma**, con el selector **EN | ES | 中文** en el menú.
2. **Traducir toda la página**: menús, textos, productos, certificaciones, cotizador, mensajes del formulario y títulos para buscadores.
3. **Dejar de depender de Google Fonts y de servidores externos.** Las tipografías y los scripts se servirán desde nuestro propio servidor. Esto mejora la velocidad en **todos los países**, no solo en China.
4. **Usar las tipografías chinas del sistema** (PingFang, Microsoft YaHei, Noto Sans SC). Son las mismas que usan las webs corporativas chinas y no hay que descargar nada.
5. **Quitar Google Maps de la versión china** y mostrar la dirección escrita.
6. **Reemplazar WhatsApp por WeChat** en la versión china (si ustedes crean la cuenta, ver sección 3).
7. **Reemplazar el video de YouTube** por el video servido desde nuestro servidor (si ustedes nos envían el archivo, ver sección 3).
8. **Revisar el diseño página por página**, porque el texto en chino ocupa otro espacio y algunos estilos deben ajustarse.

---

## 3. Lo que necesitamos de ustedes

### 3.1 Crear una cuenta de WeChat (recomendado)

**WeChat (微信) es el equivalente chino de WhatsApp, y mucho más.** En China, WhatsApp está bloqueado y prácticamente nadie lo usa. Los compradores chinos esperan contactar a un proveedor por WeChat: allí negocian, comparten fichas técnicas, envían fotos de muestras y cierran pedidos.

Nuestra recomendación:

- Crear una cuenta de WeChat **a nombre de la empresa**, en un celular de la empresa (no en el personal de un trabajador), para que el contacto no se pierda si alguien deja la empresa.
- La cuenta se puede crear con un **número peruano**.
- Usar como nombre **"Agro Sur Latino"** junto con el nombre en chino de la empresa (ver 3.3) y el logo como foto de perfil.
- Una vez creada, nos envían el **código QR de la cuenta**: lo pondremos en la versión china de la web y en el pie de página.
- Tener presente que hay **13 horas de diferencia** con China (cuando en Lima son las 8:00 p. m., en Shanghái ya son las 9:00 a. m. del día siguiente). Conviene revisar WeChat a primera hora de la mañana y al final del día.

### 3.2 Enviarnos el video corporativo original (no el enlace de YouTube)

YouTube está bloqueado en China. Hoy el video aparece en **Inicio** y en **Sobre Nosotros**, y en China saldría como un recuadro negro, además de hacer más lenta la página.

- Necesitamos el **archivo original del video** (MP4, MOV u otro formato, en la mayor calidad posible), **no el enlace de YouTube**. Al descargar de YouTube se pierde calidad.
- Nosotros lo optimizaremos para la web y lo publicaremos en nuestro propio servidor. Así se verá en **todos los países, incluida China**, sin depender de YouTube.
- Se puede enviar por Google Drive, WeTransfer o un medio similar.

> **Sobre las plataformas de video chinas:** existen plataformas como Bilibili o Tencent Video, que sí funcionan en China y reemplazarían a YouTube. Sin embargo, **exigen registrarse con un número de teléfono chino** (y a veces con un documento de identidad chino). Si en el futuro la empresa tiene un socio, agente o distribuidor en China, se podría publicar el video allí. Mientras tanto, la solución de servir el video desde nuestro servidor es la más simple y funciona igual.

### 3.3 Definir el nombre de la empresa en chino (recomendado)

Las empresas extranjeras que trabajan con China suelen tener un **nombre comercial en chino**, porque los compradores lo usan en sus documentos, búsquedas y contactos. Ejemplos conocidos: Coca-Cola es 可口可乐 y Nestlé es 雀巢.

- Si **ya tienen** un nombre en chino (por ejemplo, en algún contrato, feria o documento de exportación), envíennoslo para usar exactamente el mismo.
- Si **no tienen**, podemos proponerles 2 o 3 opciones (por sonido, por significado o mixtas) para que ustedes elijan. Una vez elegido, conviene usarlo siempre igual: web, WeChat, tarjetas de presentación y proformas.

### 3.4 Confirmarnos estas decisiones

| Pregunta | Opciones |
|---|---|
| ¿La **proforma PDF** del cotizador también se genera en chino para visitantes de la versión china? | Sí / No (se queda en inglés) |
| ¿Tienen el **registro de exportador de alimentos ante la aduana china (GACC)**? | Ver sección 5.1 |

---

## 4. Por qué no basta con traducir

| Lo que usa hoy la web | ¿Funciona en China? | Qué haremos |
|---|---|---|
| Google Fonts (tipografías) | ❌ Bloqueado: la página se queda "cargando" | Servir las tipografías desde nuestro servidor |
| Scripts externos (iconos, animaciones) | ⚠️ Lento o inestable | Servirlos desde nuestro servidor |
| Video de YouTube | ❌ Bloqueado | Video propio (necesitamos el archivo original) |
| Enlace a Google Maps | ❌ Bloqueado | Mostrar la dirección escrita |
| WhatsApp | ❌ Bloqueado | WeChat (necesitamos la cuenta) |
| Servidor de la web (PythonAnywhere) | ✅ Accesible | Sin cambios. Será algo más lenta que desde Perú, pero funciona |

> **Sobre un servidor en China:** no es necesario. Alojar una web dentro de China exige una licencia del gobierno chino (ICP), que solo pueden obtener empresas con presencia legal en China. Para una web de exportación como esta, el servidor actual es suficiente.

---

## 5. Otras recomendaciones

### 5.1 Registro ante la aduana china (GACC)

Desde 2022, China exige que las empresas extranjeras que exportan alimentos a China estén **registradas ante su aduana (GACC)**. Si Agro Sur Latino ya tiene ese registro, **mostrar el número de registro en la versión china es un argumento de confianza muy fuerte** para un importador chino, porque le confirma que puede importar sin problemas. Si no lo tienen, conviene consultarlo con **SENASA** antes de captar compradores chinos.

### 5.2 Correo electrónico

Gmail y otros servicios de Google están bloqueados en China. El correo de la empresa (`@agrosurlatino.com`) funciona sin problema para recibir mensajes de China. Recomendamos **no publicar ni usar direcciones @gmail.com** para el contacto con clientes chinos.

### 5.3 Redes sociales

Facebook, Instagram, LinkedIn y X (Twitter) también están bloqueados en China. En la versión china **no mostraremos esos enlaces** y dejaremos como contacto WeChat y el correo.

### 5.4 Presencia en plataformas B2B

Los importadores chinos buscan proveedores principalmente en **Baidu** (el buscador chino) y en plataformas B2B como **Alibaba.com** o **Made-in-China.com**, más que en Google. Una web extranjera tarda en aparecer en Baidu, así que recomendamos evaluar un **perfil de proveedor en Alibaba.com** que enlace a la versión china de la web. Suele traer contactos más rápido que la web sola.

### 5.5 Datos comerciales que los compradores chinos esperan ver

Podemos incluir en la versión china (si ustedes lo confirman):

- **Puertos de destino habituales en China**: Shanghái, Qingdao, Tianjin, Ningbo y Guangzhou (Nansha), como sugerencias en el cotizador.
- **Formas de pago aceptadas**, por ejemplo transferencia (T/T) o carta de crédito (L/C).
- **Plazo de respuesta** (por ejemplo, "respondemos en menos de 24 horas"), considerando la diferencia horaria.
- **Capacidad de suministro** (toneladas por mes o por año) y **muestras disponibles**.

### 5.6 Fechas importantes

El **Año Nuevo Chino** (enero o febrero, según el año) paraliza el comercio en China durante 1 o 2 semanas. Las semanas previas suelen ser de mucha demanda y conviene tenerlo en cuenta para planificar el stock y las respuestas.

---

## 6. Sobre la traducción con inteligencia artificial

Como ya se conversó con ustedes, la traducción se hará con inteligencia artificial, porque no contamos con un traductor nativo de chino. Para asegurar la mejor calidad posible:

- **Se traduce a partir del inglés y del español a la vez**, lo que reduce ambigüedades.
- **Se hace una retrotraducción** (del chino de vuelta al español) para detectar frases que hayan cambiado de sentido.
- **Se usa un glosario fijo** para nombres de productos, certificaciones e Incoterms, de modo que toda la web diga lo mismo (por ejemplo: quinua = 藜麦, chía = 奇亚籽, FOB = 离岸价).
- **Se usa un registro comercial formal**, como el de las webs corporativas chinas.

**Recomendación:** si más adelante tienen contacto con un comprador, agente o socio chino de confianza, o pueden contratar a un revisor nativo, conviene que revise los textos. Todos los textos de la web están en **un solo archivo**, así que la revisión y las correcciones son sencillas.

---

## 7. Lista de pendientes

**De Agro Sur Latino:**

- [ ] Crear la cuenta de WeChat de la empresa y enviarnos el código QR
- [ ] Enviarnos el archivo original del video corporativo
- [ ] Enviarnos el nombre de la empresa en chino, o pedirnos opciones para elegir
- [ ] Confirmar si la proforma PDF también debe salir en chino
- [ ] Confirmar si tienen registro GACC (y el número, para mostrarlo)
- [ ] Confirmar los datos comerciales para la versión china (puertos, pagos, plazos, capacidad)

**Del equipo web:**

- [ ] Servir tipografías y scripts desde nuestro servidor (beneficia a todos los idiomas)
- [ ] Preparar la web para el tercer idioma (`/zh/` y selector EN | ES | 中文)
- [ ] Traducir todos los textos y el contenido de productos al chino simplificado
- [ ] Adaptar la versión china: WeChat, video propio y dirección sin Google Maps
- [ ] Revisar el diseño de cada página en chino
- [ ] Probar la velocidad de carga desde China con herramientas de medición desde servidores chinos
