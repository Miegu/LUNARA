# pyrefly: ignore [missing-import]
import numpy as np

from lunargeometry import (
    get_site_position,
    get_local_frame,
    calculate_elevation_azimuth,
)

#COMPROBACIÓN DE LA ELEVACIÓN Y AZIMUT RESPECTO AL HORIZONTE LOCAL
latitude = -89.2
longitude = 23.1

site = get_site_position(latitude, longitude)
north, east, up = get_local_frame(latitude, longitude)

# Objetos de prueba situados a 100 km del observador
distance = 100.0

tests = [
    ("Vertical", up, 90.0, None),
    ("Norte", north, 0.0, 0.0),
    ("Este", east, 0.0, 90.0),
    ("Sur", -north, 0.0, 180.0),
    ("Oeste", -east, 0.0, 270.0),
]

print("\nVALIDACIÓN DEL HORIZONTE LOCAL\n")

all_passed = True

for name, direction, expected_el, expected_az in tests:
    target = site + distance * direction

    elevation, azimuth = calculate_elevation_azimuth(
        target,
        site,
        latitude,
        longitude,
    )

    elevation_ok = abs(elevation - expected_el) < 1e-6

    if expected_az is None:
        azimuth_ok = True  # El azimut no está definido en el cenit.
    else:
        azimuth_error = abs((azimuth - expected_az + 180) % 360 - 180)
        azimuth_ok = azimuth_error < 1e-6

    passed = elevation_ok and azimuth_ok
    all_passed &= passed

    status = "OK" if passed else "ERROR"

    print(
        f"{name:8} | "
        f"Elevación: {elevation:9.5f}° | "
        f"Azimut: {azimuth:9.5f}° | "
        f"{status}"
    )

print("\nRESULTADO:", "TODAS LAS PRUEBAS SUPERADAS" if all_passed
      else "HAY PRUEBAS QUE FALLAN")
