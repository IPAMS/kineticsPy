# -*- coding: utf-8 -*-

"""
simion / RS simulation result analysis
"""
import numpy as np
import matplotlib.pyplot as pl
from StringIO import StringIO

def importData(filename,n_header_l,n_conc_l):
	#n_header_l = 117 #the number of the header lines
	#n_conc_l = 599 #the number of the concentration log lines
	f = open(filename, 'r')
	l = f.readlines()
	
	#split the recorded file into two parts, the concentration logs and the ion record part
	conc_l = "" #the concentration log lines
	for i in range(n_header_l,n_header_l+n_conc_l):
		conc_l = conc_l+l[i]
	conc_io = StringIO(conc_l)

	ions_l = ""	#the ion record lines
	
	for i in range(n_header_l+n_conc_l+1,len(l)-1): #+1 to silently ignore the status / runtime length line in some of the SIMION / RS result files
		ions_l = ions_l+l[i]
	ions_io = StringIO(ions_l)
	
	
	#now parse the parts:
	concs = np.genfromtxt(conc_io,delimiter=",")
	if (ions_l != ""): 
		ions = np.genfromtxt(ions_io,delimiter=",")
	else:
		ions = None
	
	return concs,ions

def plotTimeSeries(dat,name,titleStr,annotation,slice_min,slice_max):
	
	subMin = 0 #minimal zoomed border 
	subMax = 20 #maximal zoomed border
	slice = range(slice_min,slice_max)
	
	pl.figure(figsize=(14, 6), dpi=80)
	pl.subplot(121) 
	pl.plot(
		dat[:,1],dat[:,2],
		dat[:,1],dat[:,3],
		dat[:,1],dat[:,4],
		dat[:,1],dat[:,5],
		dat[:,1],dat[:,6],
		dat[:,1],dat[:,7],
		#dat[:,1],dat[:,8],
		lw=2
	)
	
	pl.legend(('19 (n=1)', '37 (n=2)', '55 (n=3)', '73 (n=4)', '91 (n=5)', '109 (n=6)', '127 (n=7)'))
	pl.xlabel('t $[\mu s]$')
	pl.ylabel('Ion-Count')
	pl.grid(True)
	pl.title(titleStr)
	pl.annotate(annotation, xy=(-0.2, 0.03),
				xycoords='axes fraction',
				horizontalalignment='right', verticalalignment='bottom',
				rotation="vertical",
				fontsize=15)

	
	pl.subplot(122)
	pl.plot(
		dat[slice,1],dat[slice,2],#'o-',
		dat[slice,1],dat[slice,3],#'^-',
		dat[slice,1],dat[slice,4],#'v-',
		dat[slice,1],dat[slice,5],#'s-',
		dat[slice,1],dat[slice,6],#'*-',
		dat[slice,1],dat[slice,7],#'d-',
		#dat[slice,1],dat[slice,8],#'h-',
		lw=2
	)
	
	pl.legend(('19 (n=1)', '37 (n=2)', '55 (n=3)', '73 (n=4)', '91 (n=5)', '109 (n=6)', '127 (n=7)'))
	pl.xlabel('t $[\mu s]$')	
	pl.grid(True)
	pl.title("zoomed")
		
	pl.savefig(name+'.pdf', format='pdf')

def getTOFs(dat):
	return np.transpose(dat[np.nonzero(dat[:,5]>6),2])

def getMasses(dat):
	return np.transpose(dat[np.nonzero(dat[:,5]>6),3])


def generateTOFSpectrum(dat,nBins,min,max,name,titleStr,**kwargs):
	normalized = kwargs.pop('normalized',False)
	xlabel = kwargs.pop('xlabel',u'TOF [µs]')

	if normalized:
		visible = False
	else:	
		visible = True


	fig = pl.figure()
	tofs = getTOFs(dat)
	n, bins, patches = pl.hist(tofs, nBins, normed=normalized,range=[min,max], facecolor='green', edgecolor='green', alpha=0.9, visible=visible)


	if normalized:
		pl.step(bins[1:], n/np.max(n),linewidth=2)
		pl.ylim(0,1.0)
		pl.ylabel('normalized Ion-Count')
	else:
		pl.ylabel('Ion-Count')

	#
	pl.xlabel(xlabel)
	
	pl.title(titleStr)
	#plt.axis([40, 160, 0, 0.03])
	pl.grid(True)

	#print(n)
	#print(bins)
	
	return fig,np.mean(tofs),bins,n
	
	
def plotTOFSpectrum(dat,nBins,min,max,name,titleStr):
	print("PLOT TOF SPECTRUM......")
	print(titleStr)
	print(nBins)
	print(name)


	plot,meanTOF,binPositions,binAbundances = generateTOFSpectrum(dat,nBins,min,max,name,titleStr)
	pl.savefig(name+'.pdf', format='pdf')

	return meanTOF


def processFiles(filenames,n_header_l,n_conc_l,**kwargs):
	titles = kwargs.pop('titles',filenames)
	annotations = kwargs.get('annotations')
	sliceLimits = kwargs.pop('sliceLimits',[0, 500])
	tofLimits = kwargs.pop('tofLimits',[100, 30000])
	tofBins = kwargs.pop('tofBins',1000)
	
	meanTOFs = []
	for i in range(len(filenames)):
		f = filenames[i]
		t = titles[i]
		if annotations: 
			a = annotations[i]
		else:
			a = " "
		c,ions = importData(f+".rec",n_header_l,n_conc_l)
		plotTimeSeries(c,f+"_concs","SDS-KS: Concs. "+t,a,sliceLimits[0],sliceLimits[1])
		meanTOFs.append(plotTOFSpectrum(ions,tofBins,tofLimits[0],tofLimits[1],f+"_tofs",f+" "+a))
		plotTOFSpectrum(ions,tofBins,tofLimits[0],tofLimits[1],f+"_tofs",f+" "+a)
	return meanTOFs
	
def getTOFsAndMeanClMasses(filenames,n_header_l,n_conc_l):
	meanTOFs = []
	meanMasses=[]
	for i in range(len(filenames)):
		f = filenames[i]
		print(f)
		c,ions = importData(f+".rec",n_header_l,n_conc_l)
		
		tofs = getTOFs(ions)
		meanTOFs.append(np.mean(tofs))
		
		masses = getMasses(ions)
		meanMasses.append(np.mean(masses))
		
	
	return np.array(meanTOFs),np.array(meanMasses)

def getMeanPeakTOFs(filenames,n_header_l,n_conc_l):
	"""
	Gets the mean TOF times of the individual peaks (mass seperated tof times)
	and performs some calculations with it (for data analysis purposes)
	"""
	meanTofs = []
	for i in range(len(filenames)):
		f = filenames[i]
		print(f)
		
		c,ions = importData(f+".rec",n_header_l,n_conc_l)
		
		tofs = getTOFs(ions)
		masses = getMasses(ions)

		#mass separated TOFs: msepTofs
		msepTofs = {}

		#fill the mass seperated tofs dictionary with the data:
		for j in range(len(masses)): 
			tof = tofs[j][0]
			mass= masses[j][0]

			if mass in msepTofs:
				msepTofs[mass].append(tof)
			else:
				msepTofs[mass]= [tof]

		actualMeanTofs = {}

		waterClusterMasses = [19.0,37.0,55.0,73.0,91.0,109.0,127.0]
		waterClusterMeanTofs = []
		acnMonomerMasses = [59.0,77.0,95.0,113.0,131.0]
		acnMonomerMeanTofs = []
		for mass in msepTofs:
			print(mass)
			#print(np.mean(np.array(msepTofs[tofs])))
			actualMeanTofs[mass] = np.mean(np.array(msepTofs[mass]))
			print(actualMeanTofs[mass])
			if mass in waterClusterMasses: 
				waterClusterMeanTofs.append(actualMeanTofs[mass])
			if mass in acnMonomerMasses:
				acnMonomerMeanTofs.append(actualMeanTofs[mass])


		actualMeanTofs["water_cluster"]=np.mean(np.array(waterClusterMeanTofs))
		actualMeanTofs["acn_monomer"]  =np.mean(np.array(acnMonomerMeanTofs))

		meanTofs.append(actualMeanTofs)



	return meanTofs

	






	


	
		