import plotly as py
import plotly.graph_objs as go
from collections import defaultdict
from datetime import datetime


#py.offline.init_notebook_mode(connected=True) # this needed for iplot

def parseLine(line):
	line = line.strip()
	line = line.lstrip('{')
	line = line.rstrip('}')
	line = line.split(":")
	key = line[0].strip().strip('"')
	value = line[1].strip().strip('"')
	return (key,value)


def readData(fileName):
	data = []
	with open(fileName) as f:
		currentTraceName = ""
		currentHeader = ""
		timestamps = []
		values = []
		traces = defaultdict(list) #mapped by header 
		for line in f:
			if line.strip() != "":
				key,value = parseLine(line)
				if key == "name":
					if currentTraceName != "":
						trace = go.Scatter(
							x = timestamps,
							y = values, 
							name = currentTraceName
						)
						traces[currentHeader].append(trace)
						currentHeader = ""
						timestamps = []
						values = []
					currentTraceName = value
				elif key == "header":
					if currentHeader != "":
						trace = go.Scatter(
							x = timestamps,
							y = values, 
							name = currentTraceName
						)
						traces[currentHeader].append(trace) 
						timestamps = []
						values = []
					currentHeader = value
				else:
					date = datetime.fromtimestamp( int(key) ).strftime('%Y-%m-%d') 
					timestamps.append(date) #todo timestamp
					values.append(value)
	return traces
			



data = readData("chart_data.jl")


timestampCounts = defaultdict(int)
timestampValueSums = defaultdict(int)
#adapt every iteration
for trace in data["average"]:
	timestamps = trace.x
	values = trace.y
	i = 0
	while i < len(timestamps):
		timestampCounts[timestamps[i]] += 1
		timestampValueSums[timestamps[i]] += float(values[i])
		i += 1

traceCount = len(data["average"]) 
validData = []
for timestamp,count in timestampCounts.items():
	print(count)
	if count == traceCount:
		validData.append( (timestamp,timestampValueSums[timestamp] / traceCount ))

print (validData)



# Create a trace
#trace = go.Scatter(
    #x = [10,20,30,40,50],
    #y = [1,2,3,4,5]
#)
#trace2 = go.Scatter(
    #x = 12,
    #y = 17
#)

#data = [trace,trace2]

py.offline.plot(data["average"], filename='basic-line.html')
