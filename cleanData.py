import csv
def cleanData():
    with open('Fall_2025.csv','r') as infile,open('Fall_2025_clean.csv', 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if(row[8] != "TBA"):
                print(row[5])
                writer.writerow(row)
     

            