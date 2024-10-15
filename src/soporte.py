# imports
from geopy.geocoders import Nominatim # type: ignore
from geopy.extra.rate_limiter import RateLimiter # type: ignore
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore
import requests # type: ignore

"""
Este módulo proporciona funciones para obtener datos geográficos y realizar búsquedas de lugares
usando la API de Foursquare. Incluye funciones para obtener coordenadas geográficas, extraer datos
relevantes de diccionarios y convertir la información en DataFrames de Pandas.

Funciones:
----------
- obtener_coordenadas(datos_input):
    Obtiene las coordenadas (latitud y longitud) de una lista de municipios utilizando la
    librería geopy para geocodificación. Devuelve un DataFrame con los nombres de los municipios,
    latitudes y longitudes.

- extract_values_categoria(dictionary):
    Extrae el ID de la categoría y el nombre de la categoría desde un diccionario. Devuelve una
    tupla con el ID y el nombre.

- extract_values_datos(dictionary):
    Extrae la dirección formateada de un diccionario. Devuelve la dirección como cadena de texto.

- extract_values_position(dictionary):
    Extrae la latitud y longitud desde un diccionario de geocodificación. Devuelve la latitud y longitud.

- extract_data_df(df, municipio):
    Convierte un DataFrame con datos de la API en un formato limpio. Extrae las categorías, la
    dirección, latitud y longitud de los registros, y asigna el nombre del municipio.

- get_data_places(municipio, categorias, distancia, latitud, longitud, token):
    Realiza una búsqueda de lugares en un municipio utilizando la API de Foursquare. Los resultados
    se filtran por categorías y se limitan a un radio específico. Devuelve un DataFrame con los
    resultados.

- get_all_data(df, token):
    Realiza búsquedas en múltiples municipios y categorías utilizando la API de Foursquare.
    Devuelve un DataFrame consolidado con la información obtenida de las búsquedas.

Constantes:
-----------
- lista_municipios:
    Lista de municipios en los que se realizarán las búsquedas de lugares.

Dependencias:
-------------
- geopy: Para la geocodificación de los municipios.
- tqdm: Para mostrar una barra de progreso durante las iteraciones.
- pandas: Para la manipulación de datos.
- requests: Para realizar solicitudes a la API de Foursquare.

"""

# constantes
lista_municipios = ['acebeda-la', 'ajalvir', 'alameda-del-valle', 'alamo-el', 'alcala-de-henares', 'alcobendas', 'alcorcon', 'aldea-del-fresno', 'algete', 'alpedrete', 'ambite', 'anchuelo', 'aranjuez', 'arganda-del-rey', 'arroyomolinos', 'atazar-el', 'batres', 'becerril-de-la-sierra', 'belmonte-de-tajo', 'berrueco-el', 'berzosa-del-lozoya', 'boadilla-del-monte', 'boalo-el', 'braojos', 'brea-de-tajo', 'brunete', 'buitrago-del-lozoya', 'bustarviejo', 'cabanillas-de-la-sierra', 'cabrera-la', 'cadalso-de-los-vidrios', 'camarma-de-esteruelas', 'campo-real', 'canencia', 'carabana', 'casarrubuelos', 'cenicientos', 'cercedilla', 'cervera-de-buitrago', 'chapineria', 'chinchon', 'ciempozuelos', 'cobena', 'collado-mediano', 'collado-villalba', 'colmenar-del-arroyo', 'colmenar-de-oreja', 'colmenarejo', 'colmenar-viejo', 'corpa', 'coslada', 'cubas-de-la-sagra', 'daganzo-de-arriba', 'escorial-el', 'estremera', 'fresnedillas-de-la-oliva', 'fresno-de-torote', 'fuenlabrada', 'fuente-el-saz-de-jarama', 'fuentiduena-de-tajo', 'galapagar', 'garganta-de-los-montes', 'gargantilla-del-lozoya-y-pinilla-de-buitrago', 'gascones', 'getafe', 'grinon', 'guadalix-de-la-sierra', 'guadarrama', 'hiruela-la', 'horcajo-de-la-sierra-aoslos', 'horcajuelo-de-la-sierra', 'hoyo-de-manzanares', 'humanes-de-madrid', 'leganes', 'loeches', 'lozoya', 'lozoyuela-navas-sieteiglesias', 'madarcos', 'madrid', 'majadahonda', 'manzanares-el-real', 'meco', 'mejorada-del-campo', 'miraflores-de-la-sierra', 'molar-el', 'molinos-los', 'montejo-de-la-sierra', 'moraleja-de-enmedio', 'moralzarzal', 'morata-de-tajuna', 'mostoles', 'navacerrada', 'navalafuente', 'navalagamella', 'navalcarnero', 'navarredonda-y-san-mames', 'navas-del-rey', 'nuevo-baztan', 'olmeda-de-las-fuentes', 'orusco-de-tajuna', 'paracuellos-de-jarama', 'parla', 'patones', 'pedrezuela', 'pelayos-de-la-presa', 'perales-de-tajuna', 'pezuela-de-las-torres', 'pinilla-del-valle', 'pinto', 'pinuecar-gandullas', 'pozuelo-de-alarcon', 'pozuelo-del-rey', 'pradena-del-rincon', 'puebla-de-la-sierra', 'puentes-viejas-manjiron', 'quijorna', 'rascafria', 'reduena', 'ribatejada', 'rivas-vaciamadrid', 'robledillo-de-la-jara', 'robledo-de-chavela', 'robregordo', 'rozas-de-madrid-las', 'rozas-de-puerto-real', 'san-agustin-del-guadalix', 'san-fernando-de-henares', 'san-lorenzo-de-el-escorial', 'san-martin-de-la-vega', 'san-martin-de-valdeiglesias', 'san-sebastian-de-los-reyes', 'santa-maria-de-la-alameda', 'santorcaz', 'santos-de-la-humosa-los', 'serna-del-monte-la', 'serranillos-del-valle', 'sevilla-la-nueva', 'somosierra', 'soto-del-real', 'talamanca-de-jarama', 'tielmes', 'titulcia', 'torrejon-de-ardoz', 'torrejon-de-la-calzada', 'torrejon-de-velasco', 'torrelaguna', 'torrelodones', 'torremocha-de-jarama', 'torres-de-la-alameda', 'tres-cantos', 'valdaracete', 'valdeavero', 'valdelaguna', 'valdemanco', 'valdemaqueda', 'valdemorillo', 'valdemoro', 'valdeolmos-alalpardo', 'valdepielagos', 'valdetorres-de-jarama', 'valdilecha', 'valverde-de-alcala', 'velilla-de-san-antonio', 'vellon-el', 'venturada', 'villaconejos', 'villa-del-prado', 'villalbilla', 'villamanrique-de-tajo', 'villamanta', 'villamantilla', 'villanueva-de-la-canada', 'villanueva-del-pardillo', 'villanueva-de-perales', 'villar-del-olmo', 'villarejo-de-salvanes', 'villaviciosa-de-odon', 'villavieja-del-lozoya', 'zarzalejo']


def obtener_coordenadas(datos_input):

    geolocator = Nominatim(user_agent="user_agent")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    list_datos = []

    for i in tqdm(datos_input):
        location = geocode(i)
        datos_in = []
        datos_in.append(i)
        datos_in.append(location.latitude)
        datos_in.append(location.longitude)
        list_datos.append(datos_in)


    df = pd.DataFrame(list_datos)

    df = df.rename(columns = {0: 'municipio', 
                    1: 'latitud',
                    2: 'longitud'})

    return df

def extract_values_categoria(dictionary):
    id_categoria = dictionary[0]['id']
    categoria = dictionary[0]['name']
    return id_categoria, categoria

def extract_values_datos(dictionary):
    direccion = dictionary['formatted_address']
    return direccion

def extract_values_position(dictionary):
    main = dictionary['main']
    latitude = main['latitude']
    longitude = main['longitude']

    return latitude, longitude

def extract_data_df(df, municipio):
    df['municipio']=pd.DataFrame(columns=["municipio"])
    df['municipio'] = municipio
    try:
        df[['id_categoria', 'categoria']] = df['categories'].apply(lambda x: pd.Series(extract_values_categoria(x)))
        df['direccion'] = df['location'].apply(lambda x: pd.Series(extract_values_datos(x)))
        df[['latitud', 'longitud']] = df['geocodes'].apply(lambda x: pd.Series(extract_values_position(x)))
        df = df.drop(['categories', 'location','geocodes'], axis=1)
    except:
        pass
    return df


def get_data_places(municipio, categorias, distancia ,latitud, longitud, token):
    
    url = f"https://api.foursquare.com/v3/places/search?ll={latitud}%2C{longitud}&radius={distancia}&categories={categorias}&fields=fsq_id%2Cname%2Clocation%2Ccategories%2Cdistance%2Cgeocodes&sort=DISTANCE&limit=50"
    
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    
    response = requests.get(url, headers=headers)
    resultado = response.json()

    df = pd.DataFrame(resultado['results'])

    return extract_data_df(df,municipio)
 
def get_all_data(df,token):

    # Categorias seleccionadas
    # 16032	Landmarks and Outdoors > Park
    # 17114	Retail > Shopping Mall
    # 13065	Dining and Drinking > Restaurant
    # 17043	Retail > Fashion Retail > Clothing Store
    # 11006	Business and Professional Services > Audiovisual Service

    lista_municip = df.values.tolist()
    distancia = 2000
    categoria = [16032,17114,13065,17043,11006]
    result = []
    df_final = pd.DataFrame(result)

    for e in lista_municip:
        for c in tqdm(categoria):
            df_temp = get_data_places(e[0],c,distancia,e[1],e[2],token)
            df_final = pd.concat([df_temp, df_final], ignore_index=True)
            
    return pd.DataFrame(df_final)