

import csv
import pandas

file = open('workbook4.csv', 'rbU')

f = csv.reader(file)



# for row in f:
#     print row
viewing = []

for i, line in enumerate(f):
    if i == 0:
        date = line[3]
        print line[3]
    if i == 1:
        print line[0]
        time = line[6]
        print time

viewing.append(date + ' ' + time)
print viewing

# df = pandas.DataFrame.from_csv(f, header=0, sep=', ', index_col=0)
#
# print list(df.columns.values)

