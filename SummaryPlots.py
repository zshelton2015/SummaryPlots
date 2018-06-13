##Summary Plots For QIE Calibration
##Zach Shelton
##Located in Desktop/SummaryPlots
##Updated: 6/6/18 6:00PM CDT
##Imported Packages
import sqlite3
from ROOT import *
import pprint
def SummaryPlot(database):

    xyz1234 = sqlite3.connect(database)
    cursor = xyz1234.cursor()
    name = database[24:47]
    #Modify rootout change title of output ROOT file
    rootout = name
    rootout = TFile("%s.root"%name,"recreate")
    for x in bins:
        for k in shunts:
            #Fetch the values of slope and offset for the corresponding shunt and range
            values = cursor.execute("select slope,offset from qieshuntparams where range=%i and shunt=%.1f;"%(x,k)).fetchall()
            #Fetch Max and minimum values
            maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f;"%(x,k)).fetchall()
            #SQLITE3 values are tuples, this turns the tuple into 2 numbers that can be used for ROOT arguments
            maximum , minimum = maxmin[0]
            maximums= maximum+.1/k
            minimums= minimum-.1/k
            #Make a Canvas and histogram for the shunts that's added to the list
            c.append(TCanvas("%s Shunt%.1f V -  Range %i"%(name,k,x),"histo"))
            histshunt.append(TH1D("%s SLOPE Shunt %.1f - Range %i"%(name,k,x), "%s Shunt %.1f - Range %i"%(name,k,x),100,minimums,maximums))
            c.GetXaxis().SetTitle("Slope")
            c.GetYaxis().SetTitle("Frequency")
            maxmin = cursor.execute("select max(offset),min(offset) from qieshuntparams where range=%i and shunt = %.1f;"%(x,k)).fetchall()
            maximumo, minimumo = maxmin[0]
            maximumo+=k*5
            minimumo-=k*5
            #Make a Canvas and histogram for the offset that's added to the list
            c2.append(TCanvas("%s OFFSET  %.1f V Range %i"%(name,k,x) ,"histo"))
            histoffset.append(TH1D("%s OFFSET Shunt %.1f - Range %d"%(name,k,x), "%s Shunt %.1f - Range %d"%(name,k,x),50,minimumo,maximumo))
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
            if sh==1:
                if 0.283>minimum or maximum>0.326:
                    print "%s, %i, 1, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==1.5:
                if 0.185>minimum or maximum>0.22:
                    print "%s, %i, 1.5, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==2:
                if 0.143>minimum or maximum>0.168:
                    print "%s, %i, 2, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==3:
                if 0.095>minimum or maximum>0.115:
                    print "%s, %i, 3, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==4:
                if 0.072>minimum or maximum>0.085:
                    print "%s, %i, 4, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==5:
                if 0.0575>minimum or maximum>0.068:
                    print "%s, %i, 5, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==6:
                if 0.048>minimum or maximum>0.064:
                    print "%s, %i, 6, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==7:
                if 0.041>minimum or maximum>0.05:
                    print "%s, %i, 7, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==8:
                if 0.036>minimum or maximum>0.044:
                    print "%s, %i, 8, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==9:
                if 0.032>minimum or maximum>0.039:
                    print "%s, %i, 9, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==10:
                if 0.029>minimum or maximum>0.035:
                    print "%s, %i, 10, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==11:
                if 0.026>minimum or maximum>0.032:
                    print "%s, %i, 11, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
            if sh==11.5:
                if 0.025>minimum or maximum>0.031:
                    print "%s, %i, 11.5, Bad, %.4f, %.4f"%(cardname,r,minimum,maximum)
    rootout.Close()
return "Summary Plots Made!" ,
