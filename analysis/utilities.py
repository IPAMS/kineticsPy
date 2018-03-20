# -*- coding: utf-8 -*-

"""
some helper / utility functions for the analysis of kinetic results
"""

import numpy as np

def mobilityFromMassSDS(
		mass,
		temperature=273.15,
		pressure=1024,
		collisiongas_mass_amu=28.94515,
		collisiongas_diameter_nm=0.366) :
	"""Returns the ion mobility from the ion mass (in amu) estimated by the 
	algorithm used by the original SDS implementation

	Arguments:
	mass -- the ion mass in amu

	Keyword arguments: 
	temperature -- background temperature (in K)
	pressure -- the background pressure (in mbar)
	collisiongas_mass_amu -- the mass of the collision gas in amu (default is N_2)
	collisiongas_diameter_nm -- the diameter of the collision gas molecules in nm (default is N_2)
	"""
	
	dmass = mass**(1.0/3.0) * 0.120415405  #estimate ion diameter (nm) from mass
	logdm = np.log10(dmass)
	
	# Estimate Ko (10-4 m2 V-1 s-1) from dmass.
	Koair = 10.0**(4.9137 - 1.4491 * logdm - 0.2772 * logdm**2.0
	                + 0.0717 * logdm**3.0 ) * 1.0e-5
	
	#Scaling constant to convert from Koair to Kogas.
	C_air_to_gas =\
	((dmass + 0.366) / (dmass + collisiongas_diameter_nm) )**2.0 * np.sqrt(   # ((di + dair)/(di + dg))^2
	  # (mi * mair)/(mi + mair)reduced mass with air
	  mass * 28.94515 / (mass + 28.94515) /
	  # (mi * mgas)/(mi + mgas)reduced mass with gas
	  (mass * collisiongas_mass_amu / (mass + collisiongas_mass_amu))
	)
	
	k0 = Koair * C_air_to_gas   # Convert Koair to Kogas.
	                               # Ko (10-4 m2 V-1 s-1).
	    
	klocal = k0 * (1024 / pressure) * (temperature / 273.15)
	return(klocal)