from lunargeometry import calculate_visibility

DATE = "2026-10-05T12:00:00"

# Coordenadas de prueba, no son recomendaciones de aterrizaje.
SITES = [
    ("Polo sur", -89.2, 23.1),
    ("Latitud alta A", -85.0, 23.1),
    ("Latitud alta B", -89.2, 60.0),
]

print(f"\nComparación para {DATE} UTC\n")

for name, lat, lon in SITES:
    result = calculate_visibility(
        latitude=lat,
        longitude=lon,
        date=DATE,
    )

    sun = result["sun"]
    earth = result["earth"]

    print(f"--- {name} ---")
    print(f"Coordenadas: {lat}°, {lon}°")
    print(
        f"Sol: elevación {sun['elevation_deg']:.3f}°, "
        f"azimut {sun['azimuth_deg']:.3f}°"
    )
    print(
        f"Tierra: elevación {earth['elevation_deg']:.3f}°, "
        f"azimut {earth['azimuth_deg']:.3f}°"
    )
    print()
