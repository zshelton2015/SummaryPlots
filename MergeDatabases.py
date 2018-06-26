# Merge a list of databases into one database
# Returns name of merged database
# Zach Eckert
# 6/25/2018

import sqlite3
from shutil import copyfile

def MergeDatabases(files,dirName):
    copyfile(files[0],"".join([dirName,"mergedDatabase.db"]))
    #copyfile(files[0],"mergedDatabase.db")
    outDatabase = sqlite3.connect("".join([dirName,"mergedDatabase.db"]))
    outCursor = outDatabase.cursor()
    for f in files[1:]:
        tmp = sqlite3.connect(f)
        cursor1 = tmp.cursor()
        tmpVals = cursor1.execute("SELECT * from qieshuntparams").fetchall()
        for row in tmpVals:
            outCursor.execute("""INSERT INTO qieshuntparams VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""",(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))
        cursor1.close()

    outDatabase.commit()
    


