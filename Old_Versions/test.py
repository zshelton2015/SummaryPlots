import SummaryPlots
import glob
dbnames = []
dbnames = glob.glob("*.db")
for database in dbnames:
    print SummaryPlots.SummaryPlot(database)
#from SummaryPlots import SummaryPlot
