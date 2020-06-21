import sqlite3
import time
import zlib
import re

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

cur.execute('SELECT Date FROM Covid_BD')

main_list = list()
date_list = list()
case_list = list()
death_list = list()

cur.execute('SELECT Date, Total_Cases, Total_Deaths FROM Covid_BD')

prvCase = 0
prvDeath = 0

for date, case, death in cur:
    month = re.findall('([0-9]+-[0-9]+)-[0-9]+',date)
    month = month[0]

    if month not in date_list:
        date_list.append(month)

    caseEdge = case
    deathEdge = death
    #below if-statement is valid untill Year 2031
    if date.endswith('01-31') or date.endswith('02-28') or date.startswith('2024-02-29') or date.startswith('2028-02-29') or date.endswith('03-31') or date.endswith('04-30') or date.endswith('05-31') or date.endswith('06-30') or date.endswith('07-31') or date.endswith('08-31') or date.endswith('09-30') or date.endswith('10-31') or date.endswith('11-30') or date.endswith('12-31'):

        case_list.append(case)
        death_list.append(death)

caseEdge = caseEdge
deathEdge = deathEdge

case_list.append(caseEdge)
death_list.append(deathEdge)

main_list.append(date_list)
main_list.append(case_list)
main_list.append(death_list)

fhand = open('gline.js','w')
fhand.write("gline = [ ['Month','Total Cases','Total Deaths']")

count = 0

for i in range((len(main_list))+1):
    ilen = len(date_list)
    if count < ilen:
        fhand.write(",\n['")
        c = 0
        for idx in main_list:
            strng = str(idx[count])
            if re.search('^[0-9]+-[0-9]+',strng):
                fhand.write(strng+"'")
                c = c+1
            elif c != (len(case_list))-1:
                fhand.write(', '+strng)
                c = c+1
        count = count + 1
        fhand.write("]")
fhand.write("\n];")

fhand.close()

print("\nOutput written to gline.js")
print("Open gline.htm to visualize the data")
