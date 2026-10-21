#COMPROBAMOS QUE EL TIEMPO CAMBIA LA GEOMETRÍA

from lunargeometry import calculate_visibility

latitude = -89.2
longitude = 23.1

dates = [
    "2026-10-05T00:00:00",
    "2026-10-05T06:00:00",
    "2026-10-05T12:00:00",
    "2026-10-05T18:00:00",
]

print("\nCOMPROBACIÓN DE LA GEOMETRÍA A LO LARGO DEL DÍA\n")

for date in dates:
    result = calculate_visibility(latitude, longitude, date)

    sun = result["sun"]
    earth = result["earth"]

    print(f"Fecha: {date}")
    print(
        f"  Sol    | Elevación: {sun['elevation_deg']:8.3f}° "
        f"| Azimut: {sun['azimuth_deg']:8.3f}° "
        f"| Visible: {sun['visible']}"
    )
    print(
        f"  Tierra | Elevación: {earth['elevation_deg']:8.3f}° "
        f"| Azimut: {earth['azimuth_deg']:8.3f}° "
        f"| Visible: {earth['visible']}"
    )
    print()
