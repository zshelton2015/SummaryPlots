##Summary Plots For QIE Calibration
##Zach Shelton
##Located in Desktop/SummaryPlots
##Updated: 6/6/18 6:00PM CDT
##Imported Packages
import sqlite3
from ROOT import *
#Set Summary Plot Style
style = TStyle('Style', 'Summary Plots')
def SummaryPlot(database):
    xyz1234 = sqlite3.connect(database)
    cursor = xyz1234.cursor()
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
            c.append(TCanvas("%s Shunt%.1f V -  Range %i"%(name,k,x),"histo"))
            histshunt.append(TH1D("%s SLOPE Shunt %.1f - Range %i"%(database,k,x), "%s Shunt %.1f - Range %i"%(name,k,x),100,minimums,maximums))
            c.GetXaxis().SetTitle("Slope")
            c.GetYaxis().SetTitle("Frequency")
            maxmin = cursor.execute("select max(offset),min(offset) from qieshuntparams where range=%i and shunt = %.1f;"%(x,k)).fetchall()
            maximumo, minimumo = maxmin[0]
            maximumo+=k*5
            minimumo-=k*5
            #Make a Canvas and histogram for the offset that's added to the list
            c2.append(TCanvas("%s OFFSET  %.1f V Range %i"%(name,k,x) ,"histo"))
            histoffset.append(TH1D("%s OFFSET Shunt %.1f - Range %d"%(database,k,x), "%s Shunt %.1f - Range %d"%(name,k,x),50,minimumo,maximumo))
            c2.GetXaxis().SetTitle("Offset")
            c2.GetYaxis().SetTitle("Frequency")
            #Fills the histograms with the values fetched above
            for val in values:
                slope , offset = val
                histshunt[-1].Fill(slope)
                histoffset[-1].Fill(offset)
                #Write the histograms to the file, saving them for later
            histshunt[-1].Write()
            histoffset[-1].Write()
return "Summary Plots Made!" , 
