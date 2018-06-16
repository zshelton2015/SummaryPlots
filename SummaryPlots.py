# Summary Plots For QIE Calibration
# Zach Shelton
##Located in Desktop/SummaryPlots
# Updated: 6/6/18 6:00PM CDT
# Imported Packages
import sqlite3
from ROOT import *
import pprint
gROOT.SetBatch(True)
def SummaryPlot(database):
    bins = [0, 1, 2, 3]
    shunts = [1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11.5]
    xyz1234 = sqlite3.connect(database)
    cursor = xyz1234.cursor()
    fcard = []
    frange = []
    fshunt = []
    c = []
    c2 = []
    histoffset = []
    histshunt = []
    maximum = 0
    minimum = 0
    failure = False
    FailedCards = {'Card': fcard, 'Ranges': frange, 'Shunts': fshunt}
    name = database[24:46]
    # Modify rootout change title of output ROOT file
    rootout = name
    rootout = TFile("%s.root" % name, "recreate")
    TGaxis.SetMaxDigits(3)
    for r in bins:
        for sh in shunts:
            # Fetch the values of slope and offset for the corresponding shunt and range
            values = cursor.execute("select slope,offset from qieshuntparams where range=%i and shunt=%.1f;" % (r, sh)).fetchall()
            # Fetch Max and minimum values
            maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f;" % (r, sh)).fetchall()
            # SQLITE3 values are tuples, this turns the tuple into 2 numbers that can be used for ROOT arguments
            maximum , minimum = maxmin[0]


            ##############################
            if sh == 1:
                if 0.28 > minimum or maximum > 0.32:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .32
                    minimums = .28
            if sh == 1.5:
                if 0.185 > minimum or maximum > 0.22:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .22
                    minimums = .185
            if sh == 2:
                if 0.143 > minimum or maximum > 0.168:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .143
                    minimums = .168
            if sh == 3:
                if 0.095 > minimum or maximum > 0.115:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .095
                    minimums = .115
            if sh == 4:
                if 0.072 > minimum or maximum > 0.085:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .072
                    minimums = .085
            if sh == 5:
                if 0.0575 > minimum or maximum > 0.068:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .05
                    minimums = .07
            if sh == 6:
                if 0.048 > minimum or maximum > 0.064:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .048
                    minimums = .064
            if sh == 7:
                if 0.041 > minimum or maximum > 0.05:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .041
                    minimums = .05
            if sh == 8:
                if 0.036 > minimum or maximum > 0.044:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .036
                    minimums = .044
            if sh == 9:
                if 0.032 > minimum or maximum > 0.039:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .032
                    minimums = .039
            if sh == 10:
                if 0.029 > minimum or maximum > 0.035:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .029
                    minimums = .035
            if sh == 11:
                if 0.026 > minimum or maximum > 0.032:
                    maximums = maximum+(.1)
                    minimums = minimum - (.1)
                else:
                    maximums = .026
                    minimums = .032
            if sh == 11.5:
                if 0.025 > minimum or maximum > 0.031:
                    maximums = maximum+(.1)
                    minimums = minimum-(.1)
                else:
                    maximums = .025
                    minimums = .031
            #####################################
            # Mashe a Canvas and histogram for the shunts that's added to the list
            c.append(TCanvas("Card %s Shunt %.1f  -  Range %i" % (name, sh, r), "histo"))
            c[-1].Divide(2,1)
            c[-1].cd(1)
            histshunt.append(TH1D("SLOPE Sh: %.1f - R: %i" %(sh, r),"%s Shunt %.1f - Range %i" % (name, sh, r), 100, minimums, maximums))
            histshunt[-1].SetTitle("SLOPE SH: %.1f R: %d"%(sh,r))
            histshunt[-1].GetXaxis().SetTitle("Slope")
            histshunt[-1].GetYaxis().SetTitle("Frequency")
            gPad.SetLogy(1)
            maxmin = cursor.execute("select max(offset),min(offset) from qieshuntparams where range=%i and shunt = %.1f;" % (r, sh)).fetchall()
            if r = 0:
                maximumo, minimumo = maxmin[0]
                maximumo += (maximumo*.1)
                round(maximumo,2)
                round(minimumo,2)
                minimumo -= (minimumo*.1)
            if r = 1:
                maximumo, minimumo = maxmin[0]
                maximumo = 100
            if r = 2:
                maximumo, minimumo = maxmin[0]
                maximumo += (maximumo*.1)
                round(maximumo,2)
                round(minimumo,2)
                minimumo -= (minimumo*.1)
            if r = 3:
                maximumo, minimumo = maxmin[0]
                maximumo += (maximumo*.1)
                round(maximumo,2)
                round(minimumo,2)
                minimumo -= (minimumo*.1)


            # Make a Canvas and histogram for the offset that's added to the list
            #c2.append(TCanvas("%s OFFSET Shunt %.1f Range %i" % (name, sh, r), "histo"))
            c[-1].cd(2)
            histoffset.append(TH1D("OFFSET Sh: %.1f - R: %i" %(sh, r),"%s Shunt %.1f - Range %d" %(name, sh, r), 20, minimumo, maximumo))
            histoffset[-1].SetTitle("OFFSET SH: %.1f R: %d"%(sh,r))
            histoffset[-1].GetXaxis().SetTitle("Offset")
            histoffset[-1].GetYaxis().SetTitle("Frequency")
            gPad.SetLogy(1)
            # Fills the histograms with the values fetched above
            for val in values:
                slope, offset = val
                c[-1].cd(1)
                histshunt[-1].Fill(slope)
                histshunt[-1].Draw()
                c[-1].cd(2)
                histoffset[-1].Fill(offset)
                histoffset[-1].Draw()
            #Write the histograms to the file, saving them for later
            #histshunt[-1].Draw()
            #histoffset[-1].Draw()
            #c2[-1].Write()
            c[-1].Write()
            if sh == 1:
                if 0.283 > minimum or maximum > 0.326:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 1.5:
                if 0.185 > minimum or maximum > 0.22:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 2:
                if 0.143 > minimum or maximum > 0.168:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 3:
                if 0.095 > minimum or maximum > 0.115:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 4:
                if 0.072 > minimum or maximum > 0.085:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 5:
                if 0.0575 > minimum or maximum > 0.068:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 6:
                if 0.048 > minimum or maximum > 0.064:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 7:
                if 0.041 > minimum or maximum > 0.05:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 8:
                if 0.036 > minimum or maximum > 0.044:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 9:
                if 0.032 > minimum or maximum > 0.039:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 10:
                if 0.029 > minimum or maximum > 0.035:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 11:
                if 0.026 > minimum or maximum > 0.032:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if sh == 11.5:
                if 0.025 > minimum or maximum > 0.031:
                    print "Card %s in Shunt %.1f in Range %i failed" % (name, sh, r)
                    failure = True
            if failure:
                FailedCards['Card'].append(name)
                FailedCards['Shunts'].append(sh)
                FailedCards['Ranges'].append(r)
    rootout.Close()
    outputText = open("%s_Failed_Shunts_and_Ranges.txt"%name,"w+")
    outputText.write(str(FailedCards))
    outputText.close()
    return "Summary Plots Made!"
