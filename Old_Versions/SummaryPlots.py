import SummaryPlot
import glob
import sys

dbnames = []

arg = ''
#ex: python SummaryPlots.py -c **.db
if (sys.argv[1] == '-t' or sys.argv[1] == '-total'):
    arg = 't'
    data = 'eh'
    print SummaryPlot.SummaryPlot(data, arg, sys.argv[2], sys.argv[3])
    dbnames = glob.glob("data/%s/Run_%d/qiecalibrations*.db"%())
elif sys.argv[1]=='-a':
    arg = 'a'
    for data in dbnames:
        print data
        print SummaryPlot.SummaryPlot(data, arg, sys.argv[2], sys.argv[3])
    dbnames = glob.glob("data/%s/Run_%d/qiecalibrations*.db"%(sys.argv[2],sys.argv[3]))
else:
     database = sys.argv[1]
     print SummaryPlot.SummaryPlot(database, arg, sys.argv[2], sys.argv[3])
     dbnames = glob.glob("data/%s/Run_%d/qiecalibrations*.db"%(sys.argv[2],sys.argv[3]))
#from SummaryPlots import SummaryPlot
