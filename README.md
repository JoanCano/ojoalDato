# RETO ABIERTO DE MOVILIDAD. **"Ojo al dato - esto se mueve"**



## Introducción

El siguiente proyecto se desarrolla con el interés de participar en el Reto Abierto de Movilidad **"Ojo al dato - Esto se mueve"**, promovido por El Ayto. de Zaragoza, la Fundación Ibercaja y la Fundación Zaragoza Ciudad del Conocimiento, a través de Etopia Centro de Arte y Tecnología.

El reto consiste en crear una visualización de datos proporcionados por estos organismos, o fabricados por uno mismo, que ayuden a comprender, analizar y mejorar la movilidad en los ámbitos de la sostenibilidad,la calidad de vida, la inclusión y los desequilibrios sociales, económicos, de género, etc; de la ciudad de Zaragoza y su área metropolitana.

## Integrantes

+ Héctor Ochoa
 + Github: https://github.com/Robot8A
 + twitter: https://twitter.com/HOchoa_
 + e-mail: cie.hochoa@gmail.com

+ Joan Cano
 + Web personal: https://joancano.github.io/
 + Github: https://github.com/JoanCano  
 + twitter: https://twitter.com/Joan_C_A   
 + e-mail: joancalad@gmail.com


## Propuesta

### Prototipo

[Programa Python](/prototipo/georreferenciarMuestra.py)
[Video](/prototipo/video.mp4)
[Visor Web](/prototipo/kepler.html)


### Memoria

#### Introducción
La ciudad de Zaragoza es una ciudad ciclista, y los datos hablan por si solos. Ya se le han atribuido otros nombres como "la ciudad de las Bicis", y con el reto **"Ojo al dato - Esto se mueve"**,
queremos mostrar cómo se mueven las bicicletas Zaragoza.

En primer lugar, es de mención el haber utilizado únicamente datos de los desplazamientos del servicio BiZi, por lo que toda la circulación de bicicletas propias no queda reflejado al no haber datos.

La movilidad de una persona al utilizar el servicio Bizi pensamos que no puede mostrarse de otra manera que a partir de un mapa, de manera que se han tenido que adecuar los datos proporcionados desde [BiZi](http://193.146.116.108/Bizi/). Estos datos están compuestor por los campos:
+ CustID: identificador
+ CustSex: género
+ LustroNacimiento: edad
+ DataTimeRemoval: fecha recogida 	
+ Removal_Station: parking de recogida
+ DateTime_Arrival: fecha llegada
+ Arrival_station: parking llegada
+ LocationLength: ???

#### Desarrollo del proyecto

Desafortunadamente no hay ningún campo con la localización de cada una de las estaciones del servicio BiZi, por lo que se tienen que enriquecer los datos.
Para proveer a la información disponible de un atributo de geolocalización, se han utilizado datos de [OpenStreetMap](https://www.openstreetmap.org/), cuales son libres bajo licencia [ODbL](https://opendatacommons.org/licenses/odbl/index.html).

Específicamente se han utilizado los datos  **amenity=bicycle_rental**, el cual cuenta con un campo de referencia (**ref**) que concuerda con las estaciones de referencia del servicio Bizi.
Gracias a estos datos se puede enriquecer la información proporciona por el servicio Bizi, siendo esta información ya unida desde la que se partió.

La cantidad de datos ha obligado al grupo a trabajar desde bases de datos, en concreto PostgreSQL/Postgis, desde donde se pueden realizar peticiones y crear todas las visualizaciones espaciales que se demanden. Finalmente se decidió trabajar la información por días, al ser una cantidad de datos manejable.

El siguiente paso a dar, era la creación de rutas, pues únicamente se puede disponer de dos tipos de coordenadas:
+ Inicio
+ Fin

De manera que para trazar las rutas aproximadas que los ciudadanos recorren cuando recogen una bici, se utilizó a través de un servidor propio [OSRM](http://project-osrm.org/), una aplicación de planificación de rutas en línea qué utiliza los datos de OSM.

El tercer paso es obtener las localizaciones de la ruta que nos está generando OSRM, para ello se crea un [programa](/prototipo/georreferenciarMuestra.py) en Python con el objetivo de que busque para cada viaje las coordenadas inicio y fin, después lance la petición al servidor devolviéndole este la ruta en formato [GeoJSON](https://es.wikipedia.org/wiki/GeoJSON). Es con el GeoJSON obtenido, el cual tiene una geometría **LineString** con el que se interpola un punto cada vez que el usuario ha de haber recorrido 10 segundos (sabemos la distancia total de la **linestring** y el tiempo total que ha tardado en llegar.

El fichero final resultante contiene los puntos interpolados y su tiempo asociado.

#### Resultados

Una vez se tiene la información preparada, se pueden lanzar muchas consultas a la base de datos, solamente con los datos que disponemos:
+ estación salida
+ estación llegada
+ género
+ lustro nacimiento

si agregamos el componente espacial, podemos realizar consultas como las siguiente:
+ ¿Cuáles son la estaciones donde llega más gente?¿Dónde menos?¿Qué género y edad tienen?
+ ¿Cuáles son la rutas más concurridas?
+ ¿Cuáles son los intervalos de tiempo con más o menos tránsito de bicis?
+ ¿Hay rutas más seguras que otras?¿Según la hora, qué ruta escoge el usuario?¿Difiere si es hombre o mujer?
+ ¿Hay carencia de paradas según el lugar de residencia?

Son muchas las cuestiones que se pueden plantear. El objetivo de nuestro es grupo es mostrar a la ciudadanía como se está moviendo Zaragoza en bici, a través del siguiente [vídeo](/prototipo/video.mp4) que muestran todos los recorridos en un solo día.

Sin embargo, hemos creado además el [siguiente visor](/prototipo/kepler.html) con los mismos datos para que cualquier usuario pueda interaccionar, promocionar, educar con él y participar activamente a mejorar tanto el servicio de Bizi como las infraestructuras ciclistas que tanto ayudan a solucionar los problemas de tráfico, la salud y a reducir los gases de efecto invernadero.
por la educación y la promoción.
