# -*- coding: utf-8 -*-

"""
Cantera simulation result analysis
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import matplotlib.collections as collections
import re

speciesColors = ["#00539E","#314500","#BD007B","#F48F00","#00192F","#FF80D2","#FFCA80","#FFBBBB","#BBFFBB",]
speciesLabels = [\
		"$[H(H_{2}O)_{1}]^+$",
		"$[H(H_{2}O)_{2}]^+$",
		"$[H(H_{2}O)_{3}]^+$",
		"$[H(H_{2}O)_{4}]^+$",
		"$[H(H_{2}O)_{5}]^+$",
		"$[H(H_{2}O)_{6}]^+$",
		"$[H(H_{2}O)_{7}]^+$",
		"$[H(H_{2}O)_{8}]^+$",
		"$[H(H_{2}O)_{9}]^+$"]

def norm(dat):
	"""
	Normalize the data
	"""
	print(dat)
	dat = np.array(dat)
	dat  = dat / (max(dat)*1.0)
	print(dat)
	return dat
	
def importCanteraData(filename,n_header_l):
	f = open(filename, 'r')
	concs = np.genfromtxt(f,skip_header=n_header_l,skip_footer=0,delimiter=",")
	#concs[:,0] = concs[:,0] * 1e6 #time vector => 
	return concs


def plotWaterClusterTimeSeriesComparisonCantera(rawRS,rawCan,name,titleStr,annotation):


	times_msec_RS= rawRS[:,0]*1e6
	times_msec_can= rawCan[:,0]*1e6

	datRS = rawRS[:,1:7]
	datCan = rawCan[:,3:]

	datRS = datRS / np.max(datRS)
	datCan = datCan / np.max(datCan)
	
	#matplotlib.rc('mathtext', fontset='stixsans', default='regular') 
	matplotlib.rc('text') 
	nCluster = 6

	fig = pl.figure(figsize=(10, 10), dpi=180)
	ax1 = fig.add_subplot(111)
	ax1.patch.set_visible(False)
	ax1.set_zorder(2)
	for i in range(nCluster):
		ax1.plot(times_msec_RS,datRS[:,i],'-',label=speciesLabels[i],lw=2,color=speciesColors[i])
		ax1.plot(times_msec_can,datCan[:,i],'-',lw=2,color=speciesColors[i])

	ax1.set_ylabel('relative concentration')
	ax1.set_xlabel('t $[\mu s]$')

	pl.xlabel('t $[\mu s]$')
	pl.grid(True)
	pl.title(titleStr)

	#pl.savefig(name+'.pdf', format='pdf')
	pl.savefig(name+'.png', format='png')
