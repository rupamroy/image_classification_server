import csv
import json

classList = [None] * 10

classList[0]=1
classList[2]=0
 
with open('log.csv', mode='a') as log_file:
    log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    log_writer.writerow(classList)