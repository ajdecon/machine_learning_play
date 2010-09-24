import random
import math

def connected(coauthors,depth=50):
	numauthors=len(coauthors)
	randomauthor=coauthors.keys()[ math.floor(random.random()*numauthors) ]
	print "Seed author: %s\n\n" % randomauthor

	

def pathlength(coauthors,author1name, author2name,depth=10,usednames=[]):

	try: start_list=coauthors[author1name]
	except KeyError: return 100
	if author2name in start_list: return 1
	if depth<2: return 1

	if author1name in usednames: return 100

	min_distance=depth
	goal_name=""
	usednames.append(author1name)

	for name in start_list:
		new_dist=pathlength(coauthors,name,author2name,min_distance-1,usednames)
		if (new_dist+1)<min_distance: 
			min_distance=new_dist+1
			goal_name=name

#	print "depth: %d name: %s" % (depth,name)
	return min_distance
