# -*- coding: utf-8 -*-

"""
Chemked simulation result analysis
"""

import numpy as np
import matplotlib.pyplot as pl


def norm(dat):
	"""
	Normalize the data
	"""
	print(dat)
	dat = np.array(dat)
	dat  = dat / (max(dat)*1.0)
	print(dat)
	return dat
	
def importChemkedData(filename,n_header_l):
	#n_header_l = 117 #the number of the header lines
	#n_conc_l = 599 #the number of the concentration log lines
	f = open(filename, 'r')
	concs = np.genfromtxt(f,skip_header=n_header_l)
	concs[:,1] = concs[:,1] * 1e6
	return concs
	

def plotChemkedTimeSeriesVal(dat,name,titleStr,annotation,slice_min,slice_max):
	
	slice = range(slice_min,slice_max)
	#pl.rcParams.update({'font.size': 22})
	
	pl.figure(figsize=(7, 6), dpi=180)
	pl.plot(
		dat[slice,1],dat[slice,2],'o-',
		dat[slice,1],dat[slice,3],'^-',
		dat[slice,1],dat[slice,4],'v-',
		dat[slice,1],dat[slice,5],'<-',
		dat[slice,1],dat[slice,6],'>-',
		dat[slice,1],dat[slice,7],'1-',
		dat[slice,1],dat[slice,8],'2-',
		dat[slice,1],dat[slice,9],'3-',
		dat[slice,1],dat[slice,10],'s-',
		lw=2
	)

	pl.legend((
			'19 (n=1)', 
			'37 (n=2)', 
			'55 (n=3)', 
			'73 (n=4)', 
			'91 (n=5)', 
			'109 (n=6)', 
			'127 (n=7)',
			'145 (n=8)',
			'163 (n=9)'), 'upper left')

	pl.xlabel('t $[\mu s]$')	
	pl.grid(True)
	pl.title(titleStr)
	
	# set some legend properties.  All the code below is optional.  The
	# defaults are usually sensible but if you need more control, this
	# shows you how
	leg = pl.gca().get_legend()
	ltext  = leg.get_texts()  # all the text.Text instance in the legend
	llines = leg.get_lines()  # all the lines.Line2D instance in the legend
	frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

	# see text.Text, lines.Line2D, and patches.Rectangle for more info on
	# the settable properties of lines, text, and rectangles
	#frame.set_facecolor('0.80')      # set the frame face color to light gray
	pl.setp(ltext, fontsize='small')    # the legend text fontsize
	#plt.setp(llines, linewidth=1.5)      # the legend linewidth
	pl.savefig(name+'.pdf', format='pdf')


def plotChemkedTimeSeriesSonja(dat,name,titleStr,annotation,slice_min,slice_max):
	
	slice = range(slice_min,slice_max)
	#pl.rcParams.update({'font.size': 22})
	
	pl.figure(figsize=(7, 6), dpi=180)
	pl.plot(
		dat[slice,1],dat[slice,8],'o-',
		dat[slice,1],dat[slice,3],'^-',
		dat[slice,1],dat[slice,4],'v-',
		dat[slice,1],dat[slice,2],'<-',
		dat[slice,1],dat[slice,5],'>-',
		dat[slice,1],dat[slice,6],'1-',
		dat[slice,1],dat[slice,7],'2-',
		lw=2
	)

	pl.legend((
			'19 (n=1)', 
			'37 (n=2)', 
			'55 (n=3)', 
			'73 (n=4)', 
			'91 (n=5)', 
			'109 (n=6)', 
			'127 (n=7)'), 'upper left')

	pl.xlabel('t $[\mu s]$')	
	pl.grid(True)
	pl.title(titleStr)
	
	# set some legend properties.  All the code below is optional.  The
	# defaults are usually sensible but if you need more control, this
	# shows you how
	leg = pl.gca().get_legend()
	ltext  = leg.get_texts()  # all the text.Text instance in the legend
	llines = leg.get_lines()  # all the lines.Line2D instance in the legend
	frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

	# see text.Text, lines.Line2D, and patches.Rectangle for more info on
	# the settable properties of lines, text, and rectangles
	#frame.set_facecolor('0.80')      # set the frame face color to light gray
	pl.setp(ltext, fontsize='small')    # the legend text fontsize
	#plt.setp(llines, linewidth=1.5)      # the legend linewidth
	pl.savefig(name+'.pdf', format='pdf')
	

def boxPlotFinalComponents(rawdat,name,titleStr):
	dat = rawdat[-1,2:10]
	xlocations = np.array(range(len(dat)))+0.5
	labels = ["n=1","n=2","n=3","n=4","n=5","n=6","n=7","n=8","n=9"]
	width = 0.5
	
	pl.figure(figsize=(7, 6), dpi=180)
	pl.bar(xlocations, dat, width=width)
	
	pl.ylim((0, 2.5e10))
	pl.xticks(xlocations+ width/2, labels)
	pl.xlim(0, xlocations[-1]+width*2)

	pl.title(titleStr)	

	pl.savefig(name+'.pdf', format='pdf')
	
def processChemkedFiles(filenames,titles,annotations,n_header_l,sliceMin,sliceMax):

	for i in range(len(filenames)):
		f = filenames[i]
		print(f)
		t = titles[i]
		a = annotations[i]
		c = importChemkedData(f,n_header_l)
		print(c[:,1])
		plotChemkedTimeSeriesVal(c,f+"_ts","Chemked Simulation. "+t,a,sliceMin,sliceMax)
		boxPlotFinalComponents(c,f+"_components",t)
		
		