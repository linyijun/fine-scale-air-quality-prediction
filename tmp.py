import json
import csv
import pandas as pd


prediction_file = 'data/2018-01-01 00:00:00-08:00_res.json'
predictions = json.load(open(prediction_file, 'r'))

location_file = 'data/locations.csv'
locations = {}
with open(location_file, 'r') as f:
    for line in f:
        line = line.split(',')
        locations[int(line[0])] = [float(line[1]), float(line[2])]
f.close()

output = []
for k, v in predictions.items():
    output.append([int(k), float(v)] + locations[int(k)])

with open('data/res.csv', 'w') as f:
    f.write('gid,prediction,lon,lat\n')
    for line in output:
        f.write(','.join([str(i) for i in line]) + '\n')



