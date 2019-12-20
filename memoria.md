## Memoria


### Título proyecto - Zaragoza en ruta


### Descripción del prototipo y objetivo del mismo
La ciudad de Zaragoza es una ciudad ciclista, y los datos hablan por si solos. Ya se le han atribuido otros nombres como "la ciudad de las Bicis", 
y con el reto de **"Ojo al dato - Esto se mueve"** queremos mostrar a partir de mapas cómo se mueven las bicicletas de Zaragoza y así comprender mejor este 
tipo de movilidad, los horarios, rutas y personas que optan por un medio de transporte limpio y que recorren a dirio los carriles bici y calles de Zaragoza.

### Equipo que ha desarrollado el prototipo. Nombre y apellidos de todos los participantes y perfil profesional

Equipo:
+ Mapeado Colaborativo

Miembros:
+ Héctor Ochoa Ortiz. Informático
+ Joan Cano Aladid. Geógrafo

### Indicación de un representante del equipo

Joan Cano Aladid
+ e-mail: joancalad@gmail.com
+ Tlf: 686500085

### Problema que muestra o resuelve el prototipo

El principal problema que resuelve nuestro prototipo es la visualización de los recorridos que realiza un usuario del servicio Bizi incluyendo además una perspectiva 
de género y edad, que hasta ahora no se tenía.
A partir de este punto, gracias a tener una comprensión espacial del ruteado que hacen los usuarios se pueden llegar a tratar casos 
relacionados con la mejora del servicio Bizi o la planificación del viario ciclista de Zaragoza.

### Referencia a los datos que se han utilizado para el desarrollo del prototipo

En primer lugar, es de mención el haber utilizado únicamente datos de los desplazamientos del servicio BiZi, 
por lo que toda la circulación de bicicletas propias u otros servicios como de bicicletas eléctricas no queda reflejada al no haber datos libres.

En segundo lugar se han tenido que adecuar los datos proporcionados desde [BiZi](http://193.146.116.108/Bizi/) 
se han tenido que adecuar para poder empezar a trabajar con ellos. Estos datos están compuestos por los campos:

+ **CustID:** identificador
+ **CustSex:** género
+ **LustroNacimiento:** edad
+ **DataTimeRemoval:** fecha recogida 	
+ **Removal_Station:** parking de recogida
+ **DateTime_Arrival:** fecha llegada
+ **Arrival_station:** parking llegada
+ **LocationLength:** Longitud estimada del recorrido en Km (no usado en nuestra visualización)

Desafortunadamente no hay ningún campo con la localización de cada una de las estaciones del servicio BiZi, por lo que se tienen que enriquecer los datos.
Para proveer a la información disponible de un atributo de geolocalización, se han utilizado datos de [OpenStreetMap](https://www.openstreetmap.org/), los 
cuales son libres y están bajo licencia [ODbL](https://opendatacommons.org/licenses/odbl/index.html). En concreto se han utilizado los 
etiquetados como **amenity=bicycle_rental**, los cuales cuentan con un campo de referencia (**ref**) que concuerda con las estaciones del servicio Bizi.

Gracias a estos datos se pudo enriquecer la información proporcionada por el servicio Bizi, siendo esta información desde la que se partió.

La cantidad de datos ha obligado al grupo a trabajar desde bases de datos, en concreto [PostgreSQL](https://www.postgresql.org)/[Postgis](https://postgis.net), 
desde donde se pueden realizar peticiones y crear todas las visualizaciones espaciales que se demanden. Finalmente se decidió trabajar la información 
por días, al ser una cantidad de datos manejable.

El siguiente paso a dar fue la creación de rutas, pues únicamente se puede disponer de dos tipos de coordenadas debido a los atributos disponibles:
+ Inicio
+ Fin

De manera que para trazar las rutas aproximadas que los ciudadanos recorren cuando recogen una bici, se utilizó [OSRM](http://project-osrm.org/) a 
través de un servidor propio, una aplicación de planificación de rutas en línea que utiliza los datos de OSM.

El tercer paso fue obtener las localizaciones de la ruta que nos puede generar OSRM a partir de un punto de inicio y otro de fin, 
para ello se crea un [programa](/prototipo/georreferenciarMuestra.py) en Python con el objetivo de que busque para cada viaje las coordenadas inicio y fin
en nuestro fichero de datos inicial y después lance la petición al servidor devolviéndole este la ruta en formato [GeoJSON](https://es.wikipedia.org/wiki/GeoJSON). 
Es con el GeoJSON obtenido, el cual tiene una geometría *LineString* con el que se interpola un punto cada vez que el usuario ha de haber recorrido 
10 segundos (sabemos la distancia total de la *linestring* y el tiempo total que ha tardado en llegar.

El fichero final resultante contiene los puntos interpolados y su tiempo asociado.

### ¿Por qué los datos han permitido la visualización del problema y/o la búsqueda de la solución? Breve descripción del trabajo realizado con los datos

Los datos proporcionados por BiZi ya muestran evidencias del cómo está funcionando el servicio Bizi, es decir, las estaciones que reciben más afluencia de 
usuarios, el perfil demográfico que tienen, el género, ya son datos que se conocen. Sin embargo, no conocíamos las rutas que siguen.

Hay que destacar que el prototipo va más allá de ofrecer una mejor visualización de los datos, puesto que ahora tenemos un componente espacial que antes 
no se tenía. Esto quiere decir que los datos que *a priori* teníamos ahora nos permiten generar mucha más información y útil, sobre todos 
a la hora de planificar para la ciudad de Zaragoza el servicio Bizi y en general para todos los ciudadanos que circulan en bicicleta en lugar de 
otro tipo de transporte, ya que ahora disponemos de una manera precisa las rutas que escogen o por qué barrios circulan. Sabemos exactamente 
dónde actuar y puede que con mayor rigor el por qué, al tener más información por ejemplo, de por qué una estación de bicis tiene un bajo número
de usuarios.

### ¿Por qué es importante este problema? Evaluación del problema, cuantitativo (tamaño) y cualitativo (testimonios, informes o cualquier otra fuente que haya podido permitir su evaluación)

El movimiento en bicicleta de Zaragoza es una actividad diaria que atañe a toda la ciudad. Sin embargo puede que todos los ciudadanos no puedan conseguir
tener este servicio o simplemente cambiar su habitual medio de transporte por que no tienen tanto una estación como un carril bici cerca.

La importancia de un problema es reconocerlo, y con los datos anteriores proporcionados, se podían llegar a tener algunas conclusiones de cṕmo estaba 
funcionando el servicio Bizi, al poseer los datos de información como:
+ estación salida
+ estación llegada
+ género
+ lustro nacimiento

pero, ¿y si agregamos el componente espacial?, podemos realizar consultas como las siguientes:
+ ¿Cuáles son la estaciones/barrios donde llega más gente?¿Dónde menos?¿Qué género y edad tienen?
+ ¿Cuáles son la rutas más concurridas?
+ ¿Cuáles son los intervalos de tiempo con más o menos tránsito de bicis y de dónde parte?
+ ¿Hay rutas más seguras que otras? Según la hora, ¿qué ruta escoge el usuario?¿Difiere si es hombre o mujer?
+ ¿Hay carencia de paradas según el lugar de residencia?

### Descripción de usuarios beneficiados con el desarrollo del prototipo y/o visualización de datos

Si se trata de usuarios, ahora mismo se benefician de tener una visualización rápida de los lugares donde hay una estación Bizi 
y de los carriles bici disponibles. Además pueden ver las rutas que suelen recorrer los usuarios.

Un posible desarrollo del prototipo pasaría por tener todas las estaciones monitorizadas en tiempo real y poder seleccionar en una aplicación 
la estación de inicio y fin para que nos crease la ruta más rápida.

### Identificación de soluciones que inspira el prototipo

Se identifica claramente como los dos primeros anillos de la ciudad de Zaragoza son los más concurridos durante todo el día y muchos de ellos recorren
tramos en los que no existe carril bici.

También se identifica que desde los anillos exteriores, la mayoría de viajes no retornan y todos se dirigen al centro.

### Conclusiones y próximos pasos

Son muchas las cuestiones que se pueden plantear. El objetivo de nuestro grupo es concienciar a la ciudadanía de cómo se está moviendo Zaragoza en bici, 

de que es una ciudad ciclista que crece como muestra el siguiente [vídeo](/prototipo/video.mp4) con todos los recorridos en un solo día.

Sin embargo, hemos creado además el [siguiente visor](/prototipo/kepler.html) con los mismos datos pero preparados para interactuar con ellos, para que 
cualquier usuario pueda interaccionar, promocionar, educar con él y participar activamente a mejorar tanto el servicio de Bizi como las 
infraestructuras ciclistas que tanto ayudan a solucionar los problemas de tráfico, la salud y a reducir los gases de efecto invernadero.

El [prototipo](/prototipo/kepler.html) muestra los recorridos de cada usuario del servicio BiZi por tiempo y género.


