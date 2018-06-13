import sqlite3
from ROOT import *
import glob


#_file = TFile("output.root","recreate")
histo = []
shuntstotal =[]
dbnames = []
dbnames = glob.glob("*.db")
cardname = ""

for database in dbnames:
    
    xyz1234 = sqlite3.connect(database)
 
    cursor = xyz1234.cursor()    
    cardname=database[25:46]

    nrange = cursor.execute("SELECT DISTINCT range FROM qieshuntparams;").fetchall()
    nshunt = cursor.execute("SELECT DISTINCT shunt FROM qieshuntparams;").fetchall()
    _file = TFile("%s.root"%cardname,"recreate")
    #convert list of tuples to list
    Range = nrange
    List_of_Ranges=[i[0] for i in Range]
    Shunt = nshunt
    List_of_Shunts=[j[0] for j in Shunt]
   
    for r in List_of_Ranges:
        for sh in List_of_Shunts:
	    values = cursor.execute("select slope from qieshuntparams where range=%i and shunt=%.1f;"%(r,sh)).fetchall()
            mnumb = cursor.execute("select min(slope),max(slope) from qieshuntparams where range=%i and shunt=%.1f;"%(r,sh)).fetchall()
            min,max=mnumb[0]
            min+=-0.1/sh
            max+=0.1/sh
            
            histo.append(TH1D("%s Slope R %i Sh %.1f"%(cardname,r,sh),"%s Slope R %i Sh %.1f"%(cardname,r,sh),100,min,max))  
             
            val = values
            List_of_Slopes=[k[0] for k in val]
 
            for slope in List_of_Slopes:
                histo[(len(histo)-1)].Fill(slope)
	    histo[(len(histo)-1)].Write()
		
            minimum,maximum = mnumb[0]
         
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
    _file.Close()



#_file.Close()
