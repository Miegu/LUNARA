# pyrefly: ignore [missing-import]
import spiceypy as spice
# pyrefly: ignore [missing-import]
import numpy as np

spice.furnsh("kernels/naif0012.tls")
spice.furnsh("kernels/de440s.bsp")
spice.furnsh("kernels/pck00011.tpc")

# Fecha de la simulación
fecha = "2026-10-05T12:00:00"

# Convertir fecha a tiempo SPICE
et = spice.str2et(fecha)

# Posición de la Tierra respecto a la Luna
tierra, _ = spice.spkpos(
    "EARTH",
    et,
    "J2000",
    "NONE",
    "MOON"
)

# Posición del Sol respecto a la Luna
sol, _ = spice.spkpos(
    "SUN",
    et,
    "J2000",
    "NONE",
    "MOON"
)

print("\n=== NASA SPICE ===")
print("Fecha:", fecha)

print("\nTierra respecto a Luna:")
print(tierra)

print("\nSol respecto a Luna:")
print(sol)

print("\nDistancia Tierra-Luna:")
print(np.linalg.norm(tierra), "km")

print("\nDistancia Sol-Luna:")
print(np.linalg.norm(sol), "km")