#!/usr/bin/env python
# Summary Plots For QIE Calibration
# Zach Shelton
#Located in Desktop/SummaryPlots
# Updated: 6/6/18 6:00PM CDT
# Imported Packages
import sqlite3
from ROOT import *
import pprint
import glob
import os
import sys
import argparse
from MergeDatabases import MergeDatabases
gROOT.SetBatch(True)


plotBoundaries_slope = [0.28, 0.33]

plotBoundaries_offset = [1, 16, 100, 800]


def SummaryPlot(options):
    date = options.date[0]
    run =options.run[0]
    #Bin Definitions
    bins = [0, 1, 2, 3]
    #FailedCards Def:
    failure = False
    fcard = []
    frange = []
    fshunt = []
    origshunt = .33
    FailedCards = {'Card': fcard, 'Ranges': frange, 'Shunts': fshunt}
    shunts = [1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11.5]
    #Canvases

    c = []
    c2 = []

    #Histogram Lists

    histoffset = []
    histshunt = []
    histslopes = []

    #Total Histograms

    totalhist = []

    #Max - min Variables
    maximum = 0
    minimum = 0
    #Failure Log File
    failurelog = "data/%s/Run_%s/SummaryPlots/Failed_Shunts_and_Ranges.txt"%(date,run)
    #Set Axes Digits
    files = glob.glob("data/%s/Run_%s/qieCalibrationParameters*.db"%(date,run))
    MergeDatabases(files, "data/%s/Run_%s/"%(date, run))
    xyz1234 = sqlite3.connect("data/%s/Run_%s/mergedDatabase.db"%(date, run))
    cursor = xyz1234.cursor()
    TGaxis.SetMaxDigits(3)
    #files = cursor.excute("Select distinct runDirectory from qieshuntparams").Fetchall()
    idlist = cursor.execute("Select distinct id from qieshuntparams").fetchall()
    if (options.all):
        for nameList in idlist:
            name = nameList[0]
            if not os.path.exists("data/%s/Run_%s/SummaryPlots"%(date, run)):
                os.makedirs("data/%s/Run_%s/SummaryPlots"%(date,run))
            if not os.path.exists("data/%s/Run_%s/SummaryPlots/%s/ImagesOutput"%(date,run,name)):
                os.makedirs("data/%s/Run_%s/SummaryPlots/%s/ImagesOutput"%(date,run,name))
            if not os.path.exists("data/%s/Run_%s/SummaryPlots/Log/"%(date,run)):
                os.makedirs("data/%s/Run_%s/SummaryPlots/Log"%(date,run))
            #if not os.path.exists("data/%s/Run_%s/SummaryPlots/TotalPlots"%(date, run)):
                #os.makedirs("data/%s/Run_%s/SummaryPlots/TotalPlots"%(date, run))
                # Modify rootout change title of output ROOT file
            rootout = TFile("data/%s/Run_%s/SummaryPlots/%s/%sSummaryPlots.root" %(date, run, name, name), "recreate")
            for r in bins:
                for sh in shunts:
                    if (r == 2 or r == 3) and (sh != 1):
                        continue
                    # Fetch Max and minimum values for slope of shunt
                    maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f and id = '%s';" % (r, sh,name)).fetchall()
                    maximum, minimum = maxmin[0]
                    maximums = max(plotBoundaries_slope[1]/sh, maximum+0.01)
                    minimums = min(plotBoundaries_slope[0]/sh, minimum-0.01)
                    #Creates Canvases for each Shunt and Range(TH1D)
                    c.append(TCanvas("Card %s Shunt %.1f  -  Range %i" % (name, sh, r), "histo"))
                    c[-1].Divide(2,1)
                    c[-1].cd(1)
                    #Create Histograms for the shunt slopes
                    histshunt.append(TH1D("SLOPE Sh: %.1f - R: %i" %(sh, r),"%s Shunt %.1f - Range %i" % (name, sh, r), 100, minimums, maximums))
                    histshunt[-1].SetTitle("SLOPE SH: %.1f R: %d"%(sh,r))
                    histshunt[-1].GetXaxis().SetTitle("Slope")
                    histshunt[-1].GetYaxis().SetTitle("Frequency")
                    gPad.SetLogy(1)
                    #Create Histograms for the Offsets
                    maxmin = cursor.execute("select max(offset),min(offset) from qieshuntparams where range=%i and shunt = %.1f and id = '%s';" % (r, sh,name)).fetchall()
                    maximum, minimum = maxmin[0]
                    maximumo  = max(plotBoundaries_offset[r], maximum)
                    minimumo  = min(-1*plotBoundaries_offset[r], minimum)

                    # Fills the histograms with the values fetched above


                    # Fetch the values of slope and offset for the corresponding shunt and range
                    values = cursor.execute("select slope,offset from qieshuntparams where shunt = %.1f and range = %i and id ='%s';"%(sh,r,name))
                    for val in values:
                        slope, offset = val
                        c[-1].cd(1)
                        histshunt[-1].Fill(slope)
                        histshunt[-1].Draw()
                    # Write the histograms to the file, saving them for later
                    # histshunt[-1].Draw()
                    # histoffset[-1].Draw()
                    # c2[-1].Write()
                    c[-1].Update()
                    #c[-1].SaveAs("data/%s/Run_%s/SummaryPlots/ImagesOutput/CARD_%s_SHUNT_%s_RANGE_%i.png"%(date, run, name, str(sh).replace(".",""), r))
                    c[-1].Print("data/%s/Run_%s/SummaryPlots/%s/ImagesOutput/SHUNT_%s_RANGE_%i_CARD_%s.png"%(date, run,name, str(sh).replace(".",""), r, name))
                    c[-1].Write()
                    maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f and id= '%s';" % (r, sh,name)).fetchall()
                    if passfail(sh,maxmin[0]):
                        FailedCards['Card'].append(name)
                        FailedCards['Shunts'].append(sh)
                        FailedCards['Ranges'].append(r)
                countbin = 0
            rootout.Close()
            if len(FailedCards)>1:
                outputText = open("data/%s/Run_%s/SummaryPlots/Failed_Shunts_and_Ranges.txt"%(date,run),"w+")
                outputText.write(str(FailedCards))
                outputText.close()
                print "WARNING CARD THE FOLLOWING CARDS HAVE ERRORS PLEASE CHECK LOG FOR INFO:"
                print FailedCards['Card']
    if (options.total):
        for nameList in idlist:
            print nameList
            name = nameList[0]
            print name
            if not os.path.exists("data/%s/Run_%s/SummaryPlots"%(date, run)):
                os.makedirs("data/%s/Run_%s/SummaryPlots"%(date,run))
            if not os.path.exists("data/%s/Run_%s/SummaryPlots"%(date, run)):
                os.makedirs("data/%s/Run_%s/SummaryPlots/TotalOutput"%(date,run))
                # Modify rootout change title of output ROOT file
            rootout = TFile("data/%s/Run_%s/SummaryPlots/summary_plot_total.root" %(date, run), "recreate")
            for r in bins:
                for sh in shunts:
                    if (r == 2 or r == 3) and (sh != 1):
                        continue
                    # Fetch the values of slope and offset for the corresponding shunt and range
                    values = cursor.execute("select slope,offset from qieshuntparams where range=%i and shunt=%.1f ;" % (r, sh)).fetchall()

                    # Fetch Max and minimum values for slope of shunt
                    maxmin = cursor.execute("select max(slope),min(slope) from qieshuntparams where range=%i and shunt = %.1f;" % (r, sh)).fetchall()
                    maximum, minimum = maxmin[0]
                    maximums = max(plotBoundaries_slope[1]/sh, maximum+0.01)
                    minimums = min(plotBoundaries_slope[0]/sh, minimum-0.01)
                    #Creates Canvases for each Shunt and Range(TH1D)
                    c.append(TCanvas("Shunt %.1f  -  Range %i" % (sh, r), "histo"))
                    #Create Histograms for the shunt slopes
                    histshunt.append(TH1D("SLOPE Sh: %.1f " %sh,"SLOPE Sh: %.1f " %sh, 100, minimums, maximums))
                    histshunt[-1].SetTitle("SLOPE SH: %.1f "%(sh))
                    histshunt[-1].GetXaxis().SetTitle("Slope")
                    histshunt[-1].GetYaxis().SetTitle("Frequency")
                    gPad.SetLogy(1)
                    # Fills the histograms with the values fetched above
                    for val in values:
                        slope, offset = val
                        c[-1].cd(1)
                        histshunt[-1].Fill(slope)
                        histshunt[-1].Draw()
                    # Write the histograms to the file, saving them for later
                    # histshunt[-1].Draw()
                    # histoffset[-1].Draw()
                    # c2[-1].Write()
                    c[-1].Update()
                    #c[-1].SaveAs("data/%s/Run_%s/SummaryPlots/ImagesOutput/CARD_%s_SHUNT_%s_RANGE_%i.png"%(date, run, name, str(sh).replace(".",""), r))
                    c[-1].Print("data/%s/Run_%s/SummaryPlots/TotalOutput/Total_SHUNT_%s_RANGE_%i.png"%(date, run, str(sh).replace(".",""), r))
                    c[-1].Write()

    return "Summary Plots Are Made!"

def shuntboundaries(tuple1,sh):
    maxi , mini = tuple1
    maxis=0
    minis =0
    if sh == 0:
        if 0.28 > mini or maxi > 0.32:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .32
            minis = .28
    if sh == 1.5:
        if 0.185 > mini or maxi > 0.22:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .22
            minis = .185
    if sh == 2:
        if 0.143 > mini or maxi > 0.168:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .143
            minis = .168
    if sh == 3:
        if 0.095 > mini or maxi > 0.115:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .095
            minis = .115
    if sh == 4:
        if 0.072 > mini or maxi > 0.085:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .072
            minis = .085
    if sh == 5:
        if 0.0575 > mini or maxi > 0.068:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .05
            minis = .07
    if sh == 6:
        if 0.048 > mini or maxi > 0.064:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .048
            minis = .064
    if sh == 7:
        if 0.041 > mini or maxi > 0.05:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .041
            minis = .05
    if sh == 8:
        if 0.036 > mini or maxi > 0.044:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .036
            minis = .044
    if sh == 9:
        if 0.032 > mini or maxi > 0.039:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .032
            minis = .039
    if sh == 10:
        if 0.029 > mini or maxi > 0.035:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .029
            minis = .035
    if sh == 11:
        if 0.026 > mini or maxi > 0.032:
            maxis = maxi+(.1)
            minis = mini - (.1)
        else:
            maxis = .026
            minis = .032
    if sh == 11.5:
        if 0.025 > mini or maxi > 0.031:
            maxis = maxi+(.1)
            minis = mini-(.1)
        else:
            maxis = .025
            minis = .031
    return maxis,minis
def passfail(sh,tuple1):
    failure = False
    origshunt = .33
    maximum, minimum = tuple1

    if sh == 1:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:
            failure = True
    if sh == 1.5:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 2:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 3:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 4:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 5:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 6:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 7:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 8:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 9:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 10:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 11:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    if sh == 11.5:
        if (origshunt/sh)-(origshunt/sh)*.1 > minimum or maximum > (origshunt/sh)+(origshunt/sh)*.1:

            failure = True
    return failure
uid = []
dbnames = []
arg = ''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This produces Sumamry Plots for runs')
    parser.add_argument('-a','--all', action="store_true", dest='all', default=False, help = "Creates plots for all files and a combined database")
    parser.add_argument('-f','--files', action="append", dest = 'dbnames', help  = "Creates Summary Plots for a  file(s) list with -f [FILENAME] -f [FILENAME]")
    parser.add_argument('-u','--uniqueID', action="append", dest = 'uid', help  = "Creates Summary Plots for a  file(s) based on Unique IDs list with -u [UniqueID] -u [UniqueID]")
    parser.add_argument('-t','--total', action="store_true", dest="total", default = False, help = "Creates total histograms for each shunt")
    parser.add_argument('-d','--date', required=True, action="append", dest="date", help = "Enter date in format XX-XX-XXXX(Required)")
    parser.add_argument('-r','--run', required=True, action="append", dest="run", type = int,help = "Enter the number run(Required)")
    options = parser.parse_args()
    date = options.date[0]
    run = options.run[0]
    all = options.all
    total = options.all
    if len(dbnames)!=0:
        arg = 'f'
    elif len(uid)!=0:
        arg = 'u'
    elif all:
        arg = 'a'
    elif total:
        arg = 't'
    print SummaryPlot(options)
