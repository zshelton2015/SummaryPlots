##Summary Plots For QIE Calibration
##Zach Shelton
##Located in Desktop/SummaryPlots
##Updated: 6/6/18 6:00PM CDT
##Imported Packages
import sqlite3
import glob
from ROOT import *
import numpy
import pprint
##Set up Style for Histograms

##Open Database and Create TFile
datbaseNames = []
databaseNames = glob.glob("*.db")
example = TFile("Shunt_Analysis.root","recreate")
####Lists of Histograms and Final Histograms
totalhist = []
histshunt = []
histoffset = []
cards = []
bin1 =[]
shunts1 = []
indcardmaxshunt =[]
indcardminshunt =[]
totalbins = []
bins = [0,1,2,3]
shunts = [1,1.5,2,3,4,5,6,7,8,9,10,11,11.5]
#Create Histograms for comparing total shunt values
for j in range(0,len(shunts)):
	#totalshunts.append(TCanvas("Total Shunts for %.1f"%shunts[j],"histo"))
	totalhist.append(TH1D("Total Shunts for %.1f"%shunts[j],"Total Shunts for %.1f"%shunts[j],200, 0 , .5))
for d in bins:
	totalbins.append(TH1D("Combined Slopes For Range %d"%d,"Combined Slopes For Range %d"%d,200,0,.5))
#for n
maximums=0
minimums=0
maximumo=0
minimumo=0
counter = 0
values = []
name = " "
slope = 0
offset =0;#defining all values
##For Loop Update: Now it runs through every database in Directory.##
##########################################
#		For-Loop Def Summary:			 #
#	For x in bins						 #
#		Runs through the 4 ranges		 #
#		For k in shunts					 #
#		For each shunt voltage defined	 #
#		above is examined and a TH1D is  #
#		made with the max and min with   #
#		extra space for ease of reading  #
#		two canvases and histogram lists #
#		are made to be filled be the 	 #
#		retrieved values from SQLITE3	 #
##########################################
for data in databaseNames:
	xyz1234 = sqlite3.connect(data)
	cursor = xyz1234.cursor()
	name = data[25:47]
	print "Analyzing card with ID containing " + name
	for x in bins:
		for k in shunts:
			#Fetch the values of slope and offset for the corresponding shunt and range
			values = cursor.execute("select slope,offset from qieshuntparams where range=%i and shunt=%.1f;"%(x,k)).fetchall()
			#Fetch Max and minimum values
			maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f;"%(x,k)).fetchall()
			#SQLITE3 values are tuples, this turns the tuple into 2 numbers that can be used for ROOT arguments
			maximums , minimums = maxmin[0]
			maximums+=.1/k
			minimums-=.1/k
			#Make a Canvas and histogram for the shunts that's added to the list
			#c.append(TCanvas("%s Shunt%.1f V -  Range %i"%(name,k,x),"histo"))
			histshunt.append(TH1D("%s SLOPE Shunt %.1f - Range %i"%(name,k,x), "%s Shunt %.1f - Range %i"%(name,k,x),100,minimums,maximums))
			histshunt[-1].GetXaxis().SetTitle("Slope")
			histshunt[-1].GetYaxis().SetTitle("Frequency")
			maxmin = cursor.execute("select max(offset),min(offset) from qieshuntparams where range=%i and shunt = %.1f;"%(x,k)).fetchall()
			maximumo, minimumo = maxmin[0]
			maximumo+=k*5
			minimumo-=k*5
			#Make a Canvas and histogram for the offset that's added to the list
			#c2.append(TCanvas("%s OFFSET  %.1f V Range %i"%(name,k,x) ,"histo"))
			histoffset.append(TH1D("%s OFFSET Shunt %.1f - Range %d"%(name,k,x), "%s Shunt %.1f - Range %d"%(name,k,x),50,minimumo,maximumo))
			histoffset[-1].GetXaxis().SetTitle("Offset")
			histoffset[-1].GetYaxis().SetTitle("Frequency")
			#Fills the histograms with the values fetched above
			for val in values:
				slope , offset = val
				histshunt[-1].Fill(slope)
				histoffset[-1].Fill(offset)
			#Write the histograms to the file, saving them for later
			histshunt[-1].Write()
			histoffset[-1].Write()
	name=""
	counter = 0
	for k in shunts:
		#Fetch the values of slope  for the corresponding range
		values = cursor.execute("select slope from qieshuntparams where shunt=%.1f;"%k).fetchall()
		for val in values:
			slope = float(val[0])
			totalhist[counter].Fill(slope)
			totalhist[counter].Write()
		counter+=1
	counter=0
	for x in bins:
		#Fetch the values of slope  for the corresponding range
		values = cursor.execute("select slope from qieshuntparams where range=%i;"%x).fetchall()
		for val in values:
			slope = float(val[0])
			totalbins[counter].Fill(slope)
			totalbins[counter].Write()
		counter+=1
	name = ""
	########################
#######################################
for data in databaseNames:
	xyz1234 = sqlite3.connect(data)
	cursor = xyz1234.cursor()
	name = data[25:46]
#PREVIOUS LOOPS USED TO CYCLE THROUGH DATABASES
###############################################
#Cycling through each total shunt histogram   #
#Each max and min from each range is test     #
#If a max or min is outside of a range from   #
#the mean then the value is flagged and		  #
# stored in a list							  #
###############################################
	count=0
	for k in totalhist:
		theoretical = .3/shunts[count]
		for rang in bins:
			maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f;"%(rang,shunts[count])).fetchall()


			maximums , minimums = maxmin[0]
			if maximums>(theoretical+(theoretical*.12)) or minimums<((theoretical-(theoretical*.12))):
				#These are the allowance from the total mean
				bin1.append(rang)
				shunts1.append(shunts[count])
				cards.append(name)
				#Warning statement
				print "WARNING: Values of Shunt Factor %.1f of card %s in range %i are outside of outside of expected width "%(shunts[count],name,rang)
				#if count >= len(shunts):
				#break
				#else:
		count=count+1
	name=""
#Control statement
#print bin1 , cards, shunts1
#Closing the file
example.Close()
