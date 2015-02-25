__author__ = 'Isaac'

import sys

class Interval:
	def __init__ (self, line):
		splitLine = line.split()
		self.start = int(splitLine[0])
		self.finish = int(splitLine[1])
	def __str__ (self):
		return str(self.start)+' '+str(self.finish)

intervals = [Interval(line) for line in sys.stdin]
solIntervals=[]
while intervals:
	nextPick=intervals.pop(0)
	intervals.insert(0, nextPick)
	earliestEnd=nextPick.finish
	for interval in intervals:
		start=interval.start
		end=interval.finish
		if end<earliestEnd:
			earliestEnd=end
			nextPick=interval
	solIntervals.append(nextPick)
	intervals.remove(nextPick)
	nextPickStart=nextPick.start
	nextPickEnd=nextPick.finish
	x=0
	while x<len(intervals):
		interval=intervals[x]
		start=interval.start
		end=interval.finish
		if start<nextPickEnd:
			intervals.remove(intervals[x])
			x-=1
		x+=1
for interval in solIntervals:
	print (str(interval.start)+" "+str(interval.finish))