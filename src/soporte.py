# imports
from geopy.geocoders import Nominatim # type: ignore
from geopy.extra.rate_limiter import RateLimiter # type: ignore
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore

# constantes
lista_municipios = ['acebeda-la', 'ajalvir', 'alameda-del-valle', 'alamo-el', 'alcala-de-henares', 'alcobendas', 'alcorcon', 'aldea-del-fresno', 'algete', 'alpedrete', 'ambite', 'anchuelo', 'aranjuez', 'arganda-del-rey', 'arroyomolinos', 'atazar-el', 'batres', 'becerril-de-la-sierra', 'belmonte-de-tajo', 'berrueco-el', 'berzosa-del-lozoya', 'boadilla-del-monte', 'boalo-el', 'braojos', 'brea-de-tajo', 'brunete', 'buitrago-del-lozoya', 'bustarviejo', 'cabanillas-de-la-sierra', 'cabrera-la', 'cadalso-de-los-vidrios', 'camarma-de-esteruelas', 'campo-real', 'canencia', 'carabana', 'casarrubuelos', 'cenicientos', 'cercedilla', 'cervera-de-buitrago', 'chapineria', 'chinchon', 'ciempozuelos', 'cobena', 'collado-mediano', 'collado-villalba', 'colmenar-del-arroyo', 'colmenar-de-oreja', 'colmenarejo', 'colmenar-viejo', 'corpa', 'coslada', 'cubas-de-la-sagra', 'daganzo-de-arriba', 'escorial-el', 'estremera', 'fresnedillas-de-la-oliva', 'fresno-de-torote', 'fuenlabrada', 'fuente-el-saz-de-jarama', 'fuentiduena-de-tajo', 'galapagar', 'garganta-de-los-montes', 'gargantilla-del-lozoya-y-pinilla-de-buitrago', 'gascones', 'getafe', 'grinon', 'guadalix-de-la-sierra', 'guadarrama', 'hiruela-la', 'horcajo-de-la-sierra-aoslos', 'horcajuelo-de-la-sierra', 'hoyo-de-manzanares', 'humanes-de-madrid', 'leganes', 'loeches', 'lozoya', 'lozoyuela-navas-sieteiglesias', 'madarcos', 'madrid', 'majadahonda', 'manzanares-el-real', 'meco', 'mejorada-del-campo', 'miraflores-de-la-sierra', 'molar-el', 'molinos-los', 'montejo-de-la-sierra', 'moraleja-de-enmedio', 'moralzarzal', 'morata-de-tajuna', 'mostoles', 'navacerrada', 'navalafuente', 'navalagamella', 'navalcarnero', 'navarredonda-y-san-mames', 'navas-del-rey', 'nuevo-baztan', 'olmeda-de-las-fuentes', 'orusco-de-tajuna', 'paracuellos-de-jarama', 'parla', 'patones', 'pedrezuela', 'pelayos-de-la-presa', 'perales-de-tajuna', 'pezuela-de-las-torres', 'pinilla-del-valle', 'pinto', 'pinuecar-gandullas', 'pozuelo-de-alarcon', 'pozuelo-del-rey', 'pradena-del-rincon', 'puebla-de-la-sierra', 'puentes-viejas-manjiron', 'quijorna', 'rascafria', 'reduena', 'ribatejada', 'rivas-vaciamadrid', 'robledillo-de-la-jara', 'robledo-de-chavela', 'robregordo', 'rozas-de-madrid-las', 'rozas-de-puerto-real', 'san-agustin-del-guadalix', 'san-fernando-de-henares', 'san-lorenzo-de-el-escorial', 'san-martin-de-la-vega', 'san-martin-de-valdeiglesias', 'san-sebastian-de-los-reyes', 'santa-maria-de-la-alameda', 'santorcaz', 'santos-de-la-humosa-los', 'serna-del-monte-la', 'serranillos-del-valle', 'sevilla-la-nueva', 'somosierra', 'soto-del-real', 'talamanca-de-jarama', 'tielmes', 'titulcia', 'torrejon-de-ardoz', 'torrejon-de-la-calzada', 'torrejon-de-velasco', 'torrelaguna', 'torrelodones', 'torremocha-de-jarama', 'torres-de-la-alameda', 'tres-cantos', 'valdaracete', 'valdeavero', 'valdelaguna', 'valdemanco', 'valdemaqueda', 'valdemorillo', 'valdemoro', 'valdeolmos-alalpardo', 'valdepielagos', 'valdetorres-de-jarama', 'valdilecha', 'valverde-de-alcala', 'velilla-de-san-antonio', 'vellon-el', 'venturada', 'villaconejos', 'villa-del-prado', 'villalbilla', 'villamanrique-de-tajo', 'villamanta', 'villamantilla', 'villanueva-de-la-canada', 'villanueva-del-pardillo', 'villanueva-de-perales', 'villar-del-olmo', 'villarejo-de-salvanes', 'villaviciosa-de-odon', 'villavieja-del-lozoya', 'zarzalejo']

"""
    Obtiene las coordenadas geográficas (latitud y longitud) de una lista de ubicaciones.

    Esta función toma una lista de nombres de ubicaciones y utiliza la biblioteca Geopy para
    obtener sus coordenadas geográficas. Utiliza un limitador de tasa para evitar exceder
    los límites de solicitudes al servicio de geocodificación.

    Args:
        datos_input (list): Una lista de cadenas, donde cada cadena representa una ubicación (por ejemplo, nombre de un municipio).

    Returns:
        pandas.DataFrame: Un DataFrame con las columnas 'municipio', 'latitud' y 'longitud',
        donde cada fila corresponde a las coordenadas geográficas de cada ubicación en la lista de entrada.
"""
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