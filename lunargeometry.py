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