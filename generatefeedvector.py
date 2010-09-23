import feedparser
import re

# Return title and dictionary of word counts for an RSS feed
def getwordcounts(url):

	#Parse the feed
	d=feedparser.parse(url)
	wc={}

	#print d.feed.title

	#Loop over all the entries
	for e in d.entries:
		if 'summary' in e: summary = e.summary
		else: summary = e.description

		# Extract a list of words

		words=getwords(e.title+' '+summary)
		for word in words:
			wc.setdefault(word,0)
			wc[word]+=1

	return d.feed.title,wc

def getwords(html):

	# Remove all html tags
	txt=re.compile(r'<[^>]+>').sub('',html)

	# Split words by all non-alpha characters.
	words=re.compile(r'[^[A-Z^a-z]+').split(txt)

	# Convert to lowercase
	return [word.lower() for word in words if word!='']

apcount={}
wordcounts={}
feedlist = [line for line in file('./data/feeddata/feedlist.txt')]
for feedurl in feedlist:
	try:
		title,wc=getwordcounts(feedurl)
	except:
		print 'Feed didn\'t work:', feedurl
		continue

	wordcounts[title]=wc
	for word,count in wc.items( ):
		apcount.setdefault(word,0)
		if count>1:
			apcount[word]+=1
wordlist = []
for w,bc in apcount.items():
	frac = float(bc)/len(feedlist)
	if frac>0.1 and frac < 0.5: wordlist.append(w)

out=file('./data/feeddata/blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
	try:
		print blog
		out.write(blog)
	except:
		#print 'Error writing to file for ',blog
		continue
	for word in wordlist:
		if word in wc: out.write('\t%d' % wc[word])
		else: out.write('\t0')
	out.write('\n')


