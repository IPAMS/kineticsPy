# -*- coding: utf-8 -*-

"""
OpenFOAM simulation result analysis
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import matplotlib.collections as collections
import re
from StringIO import StringIO

#speciesColors = ["#00539E","#314500","#BD007B","#F48F00","#00192F","#FF80D2","#FFCA80","#FFBBBB","#BBFFBB",]
#speciesLabels = [\
#		"$[H(H_{2}O)_{1}]^+$",
#		"$[H(H_{2}O)_{2}]^+$",
#		"$[H(H_{2}O)_{3}]^+$",
#		"$[H(H_{2}O)_{4}]^+$",
#		"$[H(H_{2}O)_{5}]^+$",
#		"$[H(H_{2}O)_{6}]^+$",
#		"$[H(H_{2}O)_{7}]^+$",
#		"$[H(H_{2}O)_{8}]^+$",
#		"$[H(H_{2}O)_{9}]^+$"]
#

speciesColors = ["#FF0000","#AA4400",
				 "#CC9900","#FFCC00",
				 "#CC9900","#AA4400",
				 "#FF0000",
				 
				 "#0022FF","#0099BB","#00DDFF","#00CC66"]


speciesLabels = [\
		"$[H(H_{2}O)_{1}]^+$",
		"$[H(H_{2}O)_{2}]^+$",
		"$[H(H_{2}O)_{3}]^+$",
		"$[H(H_{2}O)_{4}]^+$",
		"$[H(H_{2}O)_{5}]^+$",
		"$[H(H_{2}O)_{6}]^+$",
		"$[H(H_{2}O)_{7}]^+$",
		"$[Acn+H(H_{2}O)_{1}]^+$",
		"$[Acn+H(H_{2}O)_{2}]^+$",
		"$[Acn+H(H_{2}O)_{3}]^+$",
		"$[Acn+H(H_{2}O)_{4}]^+$"]

speciesLines = [None,None,None,None,
				 [10, 2],[10, 2],
				 [10, 2],
				 None,None,None,None,]

def norm(dat):
	"""
	Normalize the data
	"""
	print(dat)
	dat = np.array(dat)
	dat  = dat / (max(dat)*1.0)
	print(dat)
	return dat
	
def importConcentrationsFromFoamLog(filename,maxTimes=0):
	f = open(filename, 'r')
	patternTime = re.compile(r"""Time = (?P<T>.*)""")
	patternConcs = re.compile(r"""\s*Chemical Concentrations              = \d*\((?P<concsStr>.*)\)""")
	i=0

	concs = []
	times = []

	for line in f:
		matchTime = patternTime.match(line)
		if matchTime:
			T = float(matchTime.group("T"))
			times.append(T)
			#print(T)

		matchConcs = patternConcs.match(line)
		if matchConcs:
			#print(line)
			cbuf = matchConcs.group("concsStr").split()

			if i== 0:
				for j in range(len(cbuf)):
					concs.append([])				

			for j in range(len(cbuf)):
				concs[j].append(float(cbuf[j]))

			print(cbuf)
			i+=1

		if maxTimes>0 and i>maxTimes:
			break

	times = np.array(times).reshape(1,len(times))
	concs = np.array(concs)

	print(times)
	print(concs)

	result = np.transpose(np.vstack((times,concs)))

	return result

def plotWaterClusterTimeSeriesComparisonRS(datRS,datFoam,name,titleStr,annotation):


	times_msec_RS= datRS[:,1]*1e6
	times_msec_foam= datFoam[:,0]*1e6
	
	#matplotlib.rc('mathtext', fontset='stixsans', default='regular') 
	matplotlib.rc('text', usetex=True) 
	nCluster = 6

	fig = pl.figure(figsize=(10, 10), dpi=180)
	ax1 = fig.add_subplot(111)
	ax1.patch.set_visible(False)
	ax1.set_zorder(2)
	for i in range(nCluster):
		ax1.plot(times_msec_RS,datRS[:,i+1],'-',label=speciesLabels[i],lw=2,color=speciesColors[i])
		ax1.plot(times_msec_foam,datFoam[:,i+1],'-.',lw=2,color=speciesColors[i])

	ax1.set_ylabel('# particles')
	ax1.set_xlabel('t $[\mu s]$')
			

	#leg = ax1.legend(loc='upper right',labelspacing=0.1)

	pl.xlabel('t $[\mu s]$')
	pl.grid(True)
	pl.title(titleStr)

	pl.savefig(name+'.pdf', format='pdf')
	pl.savefig(name+'.png', format='png')

def plotWaterClusterTimeSeriesComparisonSimion(datSimion,datFoam,name,titleStr,annotation):


	times_msec_Simion= datSimion[:,1]#*1e6
	times_msec_foam= datFoam[:,0]*1e6
	
	matplotlib.rc('mathtext', fontset='stixsans', default='regular') 
	nCluster = 6

	fig = pl.figure(figsize=(7, 6), dpi=180)
	ax1 = fig.add_subplot(111)
	ax1.patch.set_visible(False)
	ax1.set_zorder(2)
	for i in range(nCluster):
		ax1.plot(times_msec_Simion,datSimion[:,i+2],'-',label=speciesLabels[i],lw=2,color=speciesColors[i])
		ax1.plot(times_msec_foam,datFoam[:,i+1],'-.',lw=2,color=speciesColors[i])

	ax1.set_ylabel('# particles')
	ax1.set_xlabel('t $[\mu s]$')
			

	leg = ax1.legend(loc='right',labelspacing=0.1)

	pl.xlabel('t $[\mu s]$')
	pl.grid(True)
	pl.title(titleStr)

	pl.savefig(name+'.pdf', format='pdf')
	pl.savefig(name+'.png', format='png')


def plotFoamWaterClusterTimeSeries(datFoam,name,titleStr,annotation):
	times_msec_foam= datFoam[:,0]*1e6
	
	matplotlib.rc('mathtext', fontset='stixsans', default='regular') 
	nCluster = len(datFoam[0,:])-1

	fig = pl.figure(figsize=(7, 4.5), dpi=180)
	ax1 = fig.add_subplot(111)
	ax1.patch.set_visible(False)
	ax1.set_zorder(2)
	for i in range(nCluster):
		if speciesLines[i]:
			ax1.plot(times_msec_foam,datFoam[:,i+1],'-',label=speciesLabels[i],lw=2,color=speciesColors[i],dashes=speciesLines[i])
		else:
			ax1.plot(times_msec_foam,datFoam[:,i+1],'-',label=speciesLabels[i],lw=2,color=speciesColors[i])

	ax1.set_ylabel('# particles')
	ax1.set_xlabel('t $[\mu s]$')
			

	#leg = ax1.legend(loc='upper right',labelspacing=0.1)

	pl.xlabel('t $[\mu s]$')
	pl.grid(True)
	pl.title(titleStr)

	pl.savefig(name+'.pdf', format='pdf')
	pl.savefig(name+'.png', format='png')

