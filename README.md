# Laboratorio API's 

SetMagic Productions es una empresa especializada en la provisión de servicios integrales para la realización de rodajes cinematográficos y audiovisuales. Nos dedicamos a facilitar tanto el atrezzo necesario para las producciones como los lugares idóneos para llevar a cabo los rodajes, ya sea en entornos al aire libre o en interiores.

**Servicios Ofrecidos:**

- **Atrezzo Creativo:** Contamos con un extenso catálogo de atrezzo que abarca desde accesorios hasta muebles y objetos temáticos para ambientar cualquier tipo de  escena.

- **Locaciones Únicas:** Nuestra empresa ofrece una amplia selección de locaciones, que incluyen desde escenarios naturales como playas, bosques y montañas, hasta espacios interiores como estudios, casas históricas y edificios emblemáticos.

- **Servicios de Producción:** Además de proporcionar atrezzo y locaciones, también ofrecemos servicios de producción audiovisual, incluyendo equipos de filmación, personal técnico y servicios de postproducción.

**Herramientas y Tecnologías:**

Para recopilar información sobre nuevas locaciones y tendencias en atrezzo, utilizamos herramientas de web scraping como Beautiful Soup y Selenium para extraer datos de sitios web relevantes y redes sociales especializadas en cine y producción audiovisual. También integramos APIs de plataformas de alquiler de locaciones y bases de datos de atrezzo para acceder a información actualizada y detallada.

**Almacenamiento de Datos:**

La información recopilada mediante web scraping y APIs se almacena en una base de datos no relacional MongoDB. Esta base de datos nos permite organizar eficientemente la información sobre locaciones, atrezzo, clientes y proyectos en curso, facilitando su acceso y gestión.

**Objetivo:**

Nuestro objetivo principal es proporcionar a nuestros clientes una experiencia fluida y personalizada en la búsqueda y selección de locaciones y atrezzo para sus proyectos audiovisuales. Utilizando tecnologías avanzadas y una amplia red de contactos en la industria, nos esforzamos por ofrecer soluciones creativas y de alta calidad que satisfagan las necesidades específicas de cada producción.


# Lab: APIs y Obtención de Datos de Localizaciones para Rodajes

En este laboratorio aprenderás a utilizar APIs para obtener información sobre localizaciones de rodaje en la Comunidad de Madrid. A lo largo de este ejercicio, implementarás funciones que te permitirán extraer coordenadas, buscar lugares de interés y almacenar la información en un formato que puedas reutilizar.

## Objetivo

Obtener información geográfica y sobre posibles localizaciones para rodajes en diferentes municipios de la Comunidad de Madrid, utilizando APIs como **Geopy** y **Foursquare**.

### Paso 1: Obtener Coordenadas de los Municipios

Primero, necesitas obtener las coordenadas geográficas (latitud y longitud) de cada municipio en la Comunidad de Madrid. Para esto, utilizarás la biblioteca **Geopy** y su funcionalidad para geocodificar. La lista de los municipios de la Comunidad de Madrid es:

```python
lista_municipios = ['acebeda-la', 'ajalvir', 'alameda-del-valle', 'alamo-el', 'alcala-de-henares', 'alcobendas', 'alcorcon', 'aldea-del-fresno', 'algete', 'alpedrete', 'ambite', 'anchuelo', 'aranjuez', 'arganda-del-rey', 'arroyomolinos', 'atazar-el', 'batres', 'becerril-de-la-sierra', 'belmonte-de-tajo', 'berrueco-el', 'berzosa-del-lozoya', 'boadilla-del-monte', 'boalo-el', 'braojos', 'brea-de-tajo', 'brunete', 'buitrago-del-lozoya', 'bustarviejo', 'cabanillas-de-la-sierra', 'cabrera-la', 'cadalso-de-los-vidrios', 'camarma-de-esteruelas', 'campo-real', 'canencia', 'carabana', 'casarrubuelos', 'cenicientos', 'cercedilla', 'cervera-de-buitrago', 'chapineria', 'chinchon', 'ciempozuelos', 'cobena', 'collado-mediano', 'collado-villalba', 'colmenar-del-arroyo', 'colmenar-de-oreja', 'colmenarejo', 'colmenar-viejo', 'corpa', 'coslada', 'cubas-de-la-sagra', 'daganzo-de-arriba', 'escorial-el', 'estremera', 'fresnedillas-de-la-oliva', 'fresno-de-torote', 'fuenlabrada', 'fuente-el-saz-de-jarama', 'fuentiduena-de-tajo', 'galapagar', 'garganta-de-los-montes', 'gargantilla-del-lozoya-y-pinilla-de-buitrago', 'gascones', 'getafe', 'grinon', 'guadalix-de-la-sierra', 'guadarrama', 'hiruela-la', 'horcajo-de-la-sierra-aoslos', 'horcajuelo-de-la-sierra', 'hoyo-de-manzanares', 'humanes-de-madrid', 'leganes', 'loeches', 'lozoya', 'lozoyuela-navas-sieteiglesias', 'madarcos', 'madrid', 'majadahonda', 'manzanares-el-real', 'meco', 'mejorada-del-campo', 'miraflores-de-la-sierra', 'molar-el', 'molinos-los', 'montejo-de-la-sierra', 'moraleja-de-enmedio', 'moralzarzal', 'morata-de-tajuna', 'mostoles', 'navacerrada', 'navalafuente', 'navalagamella', 'navalcarnero', 'navarredonda-y-san-mames', 'navas-del-rey', 'nuevo-baztan', 'olmeda-de-las-fuentes', 'orusco-de-tajuna', 'paracuellos-de-jarama', 'parla', 'patones', 'pedrezuela', 'pelayos-de-la-presa', 'perales-de-tajuna', 'pezuela-de-las-torres', 'pinilla-del-valle', 'pinto', 'pinuecar-gandullas', 'pozuelo-de-alarcon', 'pozuelo-del-rey', 'pradena-del-rincon', 'puebla-de-la-sierra', 'puentes-viejas-manjiron', 'quijorna', 'rascafria', 'reduena', 'ribatejada', 'rivas-vaciamadrid', 'robledillo-de-la-jara', 'robledo-de-chavela', 'robregordo', 'rozas-de-madrid-las', 'rozas-de-puerto-real', 'san-agustin-del-guadalix', 'san-fernando-de-henares', 'san-lorenzo-de-el-escorial', 'san-martin-de-la-vega', 'san-martin-de-valdeiglesias', 'san-sebastian-de-los-reyes', 'santa-maria-de-la-alameda', 'santorcaz', 'santos-de-la-humosa-los', 'serna-del-monte-la', 'serranillos-del-valle', 'sevilla-la-nueva', 'somosierra', 'soto-del-real', 'talamanca-de-jarama', 'tielmes', 'titulcia', 'torrejon-de-ardoz', 'torrejon-de-la-calzada', 'torrejon-de-velasco', 'torrelaguna', 'torrelodones', 'torremocha-de-jarama', 'torres-de-la-alameda', 'tres-cantos', 'valdaracete', 'valdeavero', 'valdelaguna', 'valdemanco', 'valdemaqueda', 'valdemorillo', 'valdemoro', 'valdeolmos-alalpardo', 'valdepielagos', 'valdetorres-de-jarama', 'valdilecha', 'valverde-de-alcala', 'velilla-de-san-antonio', 'vellon-el', 'venturada', 'villaconejos', 'villa-del-prado', 'villalbilla', 'villamanrique-de-tajo', 'villamanta', 'villamantilla', 'villanueva-de-la-canada', 'villanueva-del-pardillo', 'villanueva-de-perales', 'villar-del-olmo', 'villarejo-de-salvanes', 'villaviciosa-de-odon', 'villavieja-del-lozoya', 'zarzalejo']
```

1. Instalar y configurar la biblioteca de Geopy para realizar la geocodificación.

2. Crear una función que reciba una lista de municipios y devuelva un DataFrame con los nombres de los municipios y sus respectivas coordenadas (latitud y longitud).

3. Validar los datos obtenidos para verificar si hay municipios sin coordenadas y resolver posibles problemas, como nombres incorrectos o faltantes.


### Paso 2: Buscar Localizaciones Relevantes con la API de Foursquare

Una vez obtenidas las coordenadas de los municipios, utilizarás la API de Foursquare para buscar servicios que pueden ser importantes en un rodaje (ej: parques, edificios históricos, plazas).

En este punto es importante que reflexiones sobre los servicios o establecimientos clave que considerarías relevantes para establecer una empresa de servicios para rodajes. No hay una única respuesta correcta, ya que depende de la estrategia y visión que tengas. Al menos deberás elegir 5 tipos de servicios que puedan influir en la decisión de ubicación. Ejemplos de estos servicios pueden incluir:

- Parques o áreas verdes para rodajes exteriores.

- Centros comerciales que faciliten acceso a diferentes necesidades logísticas.

- Bares o restaurantes para el catering del equipo.

- Tiendas especializadas en disfraces o vestuario.

- Alquileres de equipos audiovisuales.

Es crucial entender que esta selección depende de la naturaleza y enfoque de la empresa. Tal vez para algunos proyectos sea más importante estar cerca de áreas residenciales o lugares con buena conexión de transporte. Otros proyectos podrían priorizar la proximidad a tiendas especializadas o servicios de entretenimiento. Es vuestra decisión! 

1. Crear una cuenta en [Foursquare](https://location.foursquare.com/developer/) y obtener la API Key necesaria para realizar las solicitudes. Leer la documentación para entender como funciona. 

2. Definir una función para realizar búsquedas de lugares cercanos a las coordenadas de cada municipio. Esta función debe permitir filtrar los resultados por categoría y distancia.

3. Explorar las categorías disponibles en Foursquare y seleccionar aquellas que se ajusten a los servicios clave que decidáis para vuestra estrategia.

4. Aplicar la función de búsqueda a cada municipio, recopilando información sobre los lugares relevantes.

Recuerda que la elección de categorías es un punto de análisis clave en este ejercicio, ya que la información que obtendréis será fundamental para decidir la ubicación ideal para vuestra empresa. Aseguraos de justificar vuestras decisiones y considerar diferentes perspectivas. Para cada una de los municipios deberás sacar la información de todos los servicios elegidos. 

### Paso 3: Limpieza de la Información

La información obtenida de Foursquare puede incluir muchos detalles innecesarios. Tu objetivo es quedarte únicamente con los campos relevantes para tu análisis (nombre, dirección, coordenadas, tipo de lugar, etc.).


1. Explorar la estructura de los datos obtenidos para identificar los campos importantes y limpiar la información.

2. Eliminar duplicados y valores nulos para garantizar la consistencia y calidad de los datos.

### Paso 4: Almacenamiento de los Datos

Una vez que tengas la información limpia y organizada, almacénala en un archivo CSV que puedas reutilizar en futuros análisis.
