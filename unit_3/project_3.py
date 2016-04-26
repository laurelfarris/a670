import math
import numpy as np
import astropy.constants as cst

G = cst.G.cgs.value
M = cst.M_sun.cgs.value
R = cst.R_sun.cgs.value

gamma = 5./3.
c = 7.2e5
grav = G*M/(R**2)
H  = c**2/(gamma*grav)
print H
