# -*- coding: utf-8 -*-

"""
RS simulation (one pot / ideally mixed reactor) result analysis
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as pl
import matplotlib.collections as collections


def norm(dat):
	"""
	Normalize the data
	"""
	print(dat)
	dat = np.array(dat)
	dat  = dat / (max(dat)*1.0)
	print(dat)
	return dat
	
def importRSData(filename,n_header_l):
	f = open(filename, 'r')
	concs = np.genfromtxt(f,skip_header=n_header_l,skip_footer=1,delimiter=";")
	#concs[:,0] = concs[:,0] * 1e6 #time vector => 
	return concs
	

def plotRSTimeSeries(dat,name,titleStr,annotation,slice_min,slice_max,mode="standard",n_particles=10000,nCluster = 6):
	
	slice = range(slice_min,slice_max)
	#pl.rcParams.update({'font.size': 22})
	print("sm:"+str(slice_min)+" smax:"+str(slice_max))
	times_msec= (dat[slice,0]-dat[slice_min,0])*1e6
	print(str(slice_min)+"  "+str(slice_max))
	#print(dat)
	colors = ["#00539E","#314500","#BD007B","#F48F00","#00192F","#FF80D2","#FFCA80","#FFBBBB","#BBFFBB",]
	#labels = [\
	#	"19 (n=1)",
	#	"37 (n=2)",
	#	"55 (n=3)",
	#	"73 (n=4)",
	#	"91 (n=5)",
	#	"109 (n=6)",
	#	"127 (n=7)"]
	matplotlib.rc('mathtext', fontset='stixsans', default='regular') 
	labels = [\
		"$[H(H_2O)_{1}]^+$",
		"$[H(H_2O)_{2}]^+$",
		"$[H(H_2O)_{3}]^+$",
		"$[H(H_2O)_{4}]^+$",
		"$[H(H_2O)_{5}]^+$",
		"$[H(H_2O)_{6}]^+$",
		"$[H(H_2O)_{7}]^+$",
		"$[H(H_2O)_{8}]^+$",
		"$[H(H_2O)_{9}]^+$"]	
	if mode =="faims_acetone":
		labels = [\
		"$HAcn^+$",
		"$[HAcn(H_2O)_{1}]^+$",
		"$[HAcn(H_2O)_{2}]^+$",
		"$[HAcn(H_2O)_{3}]^+$",
		"$[HAcn(H_2O)_{4}]^+$"]
		nCluster = 5
	if mode =="young_reproduction": 
		nCluster = 4
	if mode=="faims":
		fig = pl.figure(figsize=(14, 9), dpi=240)
	else: 
		fig = pl.figure(figsize=(7, 6), dpi=180)
	ax1 = fig.add_subplot(111)
	ax1.patch.set_visible(False)
	ax1.set_zorder(2)
	for i in range(nCluster):
		if mode=="standard" or mode=="young_reproduction":		
			ax1.plot(times_msec,dat[slice,i+1],'-',label=labels[i],lw=2,color=colors[i])
		if mode in ["faims","faims_acetone","faims_phase","dms"]:
			ax1.plot(times_msec,dat[slice,i+4],'-',label=labels[i],lw=2,zorder=2,color=colors[i])

	ax1.set_ylabel('# particles')
	ax1.set_xlabel('t $[\mu s]$')
			

	leg = ax1.legend(loc='upper right',labelspacing=0.1)
	
	if mode in ["faims","faims_acetone","dms"]:
		collection = collections.BrokenBarHCollection.span_where(
			times_msec, ymin=0, ymax=n_particles, where=dat[slice,1]>0, facecolor='#80C3FF', alpha=0.3)
		ax1.add_collection(collection)

		ax2 = ax1.twinx()
		ax2.set_zorder(1)
		col = "#FF0000"
		temps= dat[slice,3]
		ax2.plot(times_msec,temps,color=col,label="temperature")
		pl.ylim([\
			np.min(temps)-np.min(temps)*0.2,
			np.max(temps)+np.max(temps)*0.5])
		ax2.set_ylabel('ion temperature (K)', color=col,zorder=1)
		for tl in ax2.get_yticklabels():
			tl.set_color(col)
		ax2.set_xlabel('t $[\mu s]$')

	pl.xlabel('t $[\mu s]$')
	pl.grid(True)
	pl.title(titleStr)
	
	# set some legend properties.  All the code below is optional.  The
	# defaults are usually sensible but if you need more control, this
	# shows you how
	#leg = ax1.get_legend()
	#ltext  = leg.get_texts()  # all the text.Text instance in the legend
	#llines = leg.get_lines()  # all the lines.Line2D instance in the legend
	#frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

	# see text.Text, lines.Line2D, and patches.Rectangle for more info on
	# the settable properties of lines, text, and rectangles
	#frame.set_facecolor('0.80')      # set the frame face color to light gray
	#pl.setp(ltext, fontsize=8)    # the legend text fontsize
	#plt.setp(llines, linewidth=1.5)      # the legend linewidth
	#pl.savefig(name+'.pdf', format='pdf')
	pl.savefig(name+'.png', format='png')
	pl.close()
	

#seperates the field phases (high and low field phase) of an DMS / FAIMS simulation
def seperateFieldPhasesFAIMS(rawdat):
	dat_high = rawdat[np.nonzero(rawdat[:,1]==1),:] #the high field period samples
	dat_low  = rawdat[np.nonzero(rawdat[:,1]==0),:] #the low field period samples

	return({"high":dat_high[0],"low":dat_low[0]}) #strangely, the array is packed in an additional one element array
		

# samplesize = the size of the sample (number of timesteps at the end to determine the mean sizes for)
def boxPlotFinalComponents(rawdat,name,titleStr,mode="standard",samplesize=100,n_particles=10000):

	if mode == "standard":
		dat = np.mean(rawdat[-samplesize:-1,1:10], axis = 0) 
	if mode in ["faims","dms"]:
		dat = np.mean(rawdat[-samplesize:-1,4:13], axis = 0) 
	if mode == "faims_acetone":
		dat = np.mean(rawdat[-samplesize:-1,4:8], axis = 0) 
	if mode == "young_reproduction":
		dat = np.mean(rawdat[-samplesize:-1,1:5], axis = 0) 

	print(dat)
	xlocations = np.array(range(len(dat)))+0.5
	labels = ["n=1","n=2","n=3","n=4","n=5","n=6","n=7","n=8","n=9"]
	width = 0.5
	
	pl.figure(figsize=(7, 6), dpi=180)
	pl.bar(xlocations, dat, width=width)
	
	pl.ylim((0, n_particles))
	pl.xticks(xlocations+ width/2, labels)
	pl.xlim(0, xlocations[-1]+width*2)

	pl.title(titleStr)	

	pl.savefig(name+'.pdf', format='pdf')
	pl.close()
	return(dat)
	

def normalizeVector(vec):
	return(vec / np.sum(vec))

# Calculates the mean cluster size from an vector of cluster abundances	
# clAb = vector of cluster abundances, ordered
def meanClusterSize(clAb):
	clAb = normalizeVector(clAb)
	result = 0
	for i in range(len(clAb)):
		result = result + (i+1)*clAb[i]
	return(result)


# Calculates the weighted mean cluster ion mobility from a vector of cluster abundances
# and a vector of individual cluster mobilities
# clAb = vector of cluster abundances, ordered

def weightedMeanClusterMobility(clAb,mobilities):
	clAb = normalizeVector(clAb)
	result = 0
	for i in range(len(clAb)):
		result = result + mobilities[i]*clAb[i]

	return(result)	



## modes: standard or  "faims"
def processRSFiles(filenames,titles,annotations,n_header_l,sliceMin,sliceMax,
	mode="standard",
	samplesize=4000,
	detailedPlotSamplesize=2000,
	componentSamples=100,
	n_particles=10000):

	for i in range(len(filenames)):
		f = filenames[i]
		print(f)
		t = titles[i]
		a = annotations[i]
		dat = importRSData(f,n_header_l)
		if mode in ["faims","faims_acetone","dms"]:
			plotRSTimeSeries(dat,f+"_ts",t,a,sliceMin,sliceMax[i],mode=mode,nCluster=9)
		else:
			plotRSTimeSeries(dat,f+"_ts",t,a,sliceMin,sliceMax[i],mode=mode,nCluster=6)

		if mode in ["dms"]:
			plotRSTimeSeries(dat,f+"_ts_detail",t,a,sliceMax[i]-detailedPlotSamplesize,sliceMax[i],mode=mode,nCluster=9)

		buf = boxPlotFinalComponents(dat,f+"_components",t,mode=mode,samplesize=componentSamples,n_particles=n_particles)

		if mode in ["faims","faims_acetone","dms"]:
			ds = seperateFieldPhasesFAIMS(dat)
			#plotRSTimeSeries(ds['high'],f+"_ts_high","RS Simulation. "+t+ " high field",a,0,len(ds['high']),mode="faims_phase")
			#plotRSTimeSeries(ds['low'], f+"_ts_low", "RS Simulation. "+t+ " low field" ,a,0,len(ds['low']), mode="faims_phase")
			cl_high= boxPlotFinalComponents(ds['high'],f+"_components_high",t+" high field",samplesize=samplesize,mode="faims",n_particles=n_particles)
			cl_low=  boxPlotFinalComponents(ds['low'],f+ "_components_low", t+" low field", samplesize=samplesize,mode="faims",n_particles=n_particles)
			fid = open(f+"_analysis.txt", 'w')
			fid.write("high:\n"+str(normalizeVector(cl_high))+"\n")
			fid.write(str("mean cluster size: "+str(meanClusterSize(cl_high))))
			fid.write("\nlow:\n"+str(normalizeVector(cl_low))+"\n")
			fid.write(str("mean cluster size: "+str(meanClusterSize(cl_low))))
			fid.close()

		if i>0:
			if mode in ["faims","faims_acetone","dms"]:
				clusterConcs['high'] = np.vstack(clusterConcs['high'],cl_high)
				clusterConcs['low'] = np.vstack(clusterConcs['low'],cl_low)
			else:
				clusterConcs = np.vstack([clusterConcs,buf])
		else:
			if mode in ["faims","faims_acetone","dms"]:
				print("len ds"+str(len(ds['high'])))
				print("len ds"+str(len(ds['low'])))
				clusterConcs = {'high':cl_high,'low':cl_low,'mean':buf}
			else:
				clusterConcs = buf

	return clusterConcs
		
		
