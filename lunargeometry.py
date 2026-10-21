from pathlib import Path
# pyrefly: ignore [missing-import]
import spiceypy as spice
# pyrefly: ignore [missing-import]
import numpy as np 

"""
- posicion de un sitio en la superficie lunar
- elevacion y azimut del sol y la tierra
- visibilidad geométrica sobre el horizonte
"""

BASE_DIR = Path(__file__).resolve().parent

KERNEL_DIR = BASE_DIR / "kernels"

#Obtengo la dirección de los kernels.
LSK = KERNEL_DIR / "naif0012.tls"
SPK = KERNEL_DIR / "de440s.bsp"
PCK = KERNEL_DIR / "pck00011.tpc"

MOON = "MOON"
MOON_FRAME = "IAU_MOON" #sistema de coordenadas

KERNELS_LOADED = False

def load_kernels():
    global KERNELS_LOADED

    if KERNELS_LOADED:
        return
    
    kernels = [LSK, SPK, PCK]

    for kernel in kernels:
        if not kernel.exists():
            raise FileNotFoundError(
                f"No se encuentra el kernel : \n{kernel}"
            )
        spice.furnsh(str(kernel))
    KERNELS_LOADED = True

def normalize(vector):
    #normaliza un vector 3d.

    vector = np.asarray(vector, dtype=float)
    norm = np.linalg.norm(vector)

    if norm == 0:
        raise ValueError
    return vector / norm

def degrees(value): # radianes a segundos
    return np.degrees(value)

def get_moon_radii():
    #obtiene los radios de referencia de la Luna definidos en el PCK
    load_kernels()
    _, radii = spice.bodvrd(
        "MOON",
        "RADII",
        3
    )
    return np.asarray(radii, dtype=float)

def get_site_position(latitude,longitude,altitude = 0.0):
    #calcula la posicion de un sitio sobre la luna
    #latitude planetocéntrica en grados
    #longitud en grados
    #altitud sobre el elipsoide de referencia en km

    load_kernels()
    lat = np.radians(latitude)
    lon = np.radians(longitude)

    radii = get_moon_radii()
    radius = float(np.mean(radii)) + altitude

    x = radius * np.cos(lat) * np.cos(lon)
    y = radius * np.cos(lat) * np.sin(lon)
    z = radius * np.sin(lat)

    return np.array([x, y, z], dtype=float)

def get_local_up(latitude, longitude):
    lat = np.radians(latitude)
    lon = np.radians(longitude)

    up = np.array([
        np.cos(lat) * np.cos(lon),
        np.cos(lat) * np.sin(lon),
        np.sin(lat),
    ], dtype=float)

    return normalize(up)

def get_local_frame(latitude, longitude):
    # construcción del sistema de coordenadas.
    lat = np.radians(latitude)
    lon = np.radians(longitude)

    east = np.array(
        [
            -np.sin(lon),
            np.cos(lon),
            0.0
        ]
    )

    east = normalize(east)

    up = get_local_up(latitude,longitude)

    north = np.cross(up, east)
    north = normalize(north)

    return north, east, up

def get_body_position(body, date):
    # posicion de un cuerpo visto desde la luna
    load_kernels()
    et = spice.str2et(date)
    
    position, light_time = spice.spkpos(
        body,
        et,
        MOON_FRAME,
        "NONE",
        MOON
    )
    return np.array(position, dtype = float)

#ELEVACIÓN Y AZIMUT
def calculate_elevation_azimuth(
    target_position, #posicion del objeto respecto al centro lunar
    site_position, #posicion del observador respecto al centro lunar
    latitude, 
    longitude
    # retorno la elevacion sobre el horizonte en grados.
    # el azimut en grados, 0º norte, 90º este, 180º sur y 270º oeste
):
    north, east, up = get_local_frame(
        latitude,
        longitude
    )

    target_vector = (
        np.asarray(target_position)
        - np.asarray(site_position)
    )

    target_vector = normalize(target_vector)

    north_component = np.dot(target_vector, north)
    east_component = np.dot(target_vector, east)
    up_component = np.dot(target_vector, up)

    # Elevación
    horizontal_component = np.sqrt(
        north_component ** 2
        + east_component ** 2
    )

    elevation = np.degrees(
        np.arctan2(
            up_component,
            horizontal_component
        )
    )

    # Azimut
    azimuth = np.degrees(
        np.arctan2(
            east_component,
            north_component
        )
    )

    # Convertimos el resultado a [0, 360).
    azimuth = azimuth % 360.0

    return float(elevation), float(azimuth)

def calculate_body_visibility(body, latitude, longitude, date, altitude = 0.0):
    #calcula la geometría del cuerpo y devuelve body, elevation, azimuth, visible, site_position, body_position
    site_position = get_site_position(
        latitude,
        longitude,
        altitude
    )

    body_position = get_body_position(
        body,
        date
    )

    elevation, azimuth = calculate_elevation_azimuth(
        body_position,
        site_position,
        latitude,
        longitude
    )

    visible = elevation > 0.0

    return {
        "body": body,
        "elevation_deg": elevation,
        "azimuth_deg": azimuth,
        "visible": visible,
        "site_position_km": site_position,
        "body_position_km": body_position,
    }

# ! FUNCIÓN PRINCIPAL
def calculate_visibility(latitude, longitude, date, altitude = 0.0):
    #calcula la visibilidad del sol y la tierra desde cualquier sitio de la luna.
    load_kernels()

    sun = calculate_body_visibility(
        "SUN",
        latitude,
        longitude,
        date,
        altitude
    )

    earth = calculate_body_visibility(
        "EARTH",
        latitude,
        longitude,
        date,
        altitude
    )

    return {
        "date": date,

        "site": {
            "latitude_deg": latitude,
            "longitude_deg": longitude,
            "altitude_km": altitude,
        },

        "sun": {
            "elevation_deg": sun["elevation_deg"],
            "azimuth_deg": sun["azimuth_deg"],
            "visible": sun["visible"],
        },

        "earth": {
            "elevation_deg": earth["elevation_deg"],
            "azimuth_deg": earth["azimuth_deg"],
            "visible": earth["visible"],
        },
    }

if __name__ == "__main__":

    print("=" * 60)
    print("LUNAR SOUTH POLE - SPICE GEOMETRY TEST")
    print("=" * 60)

    # Ejemplo de sitio cercano al polo sur lunar.
    latitude = -89.2
    longitude = 23.1

    # Fecha de prueba.
    date = "2026-10-05T12:00:00"

    result = calculate_visibility(
        latitude=latitude,
        longitude=longitude,
        date=date
    )

    print()
    print(f"Date: {result['date']}")

    print()
    print("SITE")
    print(f"  Latitude : {result['site']['latitude_deg']}°")
    print(f"  Longitude: {result['site']['longitude_deg']}°")

    print()
    print("SUN")
    print(
        f"  Elevation: "
        f"{result['sun']['elevation_deg']:.3f}°"
    )
    print(
        f"  Azimuth  : "
        f"{result['sun']['azimuth_deg']:.3f}°"
    )
    print(
        f"  Visible  : "
        f"{result['sun']['visible']}"
    )

    print()
    print("EARTH")
    print(
        f"  Elevation: "
        f"{result['earth']['elevation_deg']:.3f}°"
    )
    print(
        f"  Azimuth  : "
        f"{result['earth']['azimuth_deg']:.3f}°"
    )
    print(
        f"  Visible  : "
        f"{result['earth']['visible']}"
    )

    print()
    print("=" * 60)