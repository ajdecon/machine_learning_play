
import urllib2, cookielib, BeautifulSoup

def scrapeACSAuthors(url):

	opener=urllib2.build_opener( urllib2.HTTPCookieProcessor( cookielib.CookieJar() ) )
	urllib2.install_opener(opener)

	data=urllib2.urlopen(url)
	soup=BeautifulSoup.BeautifulSoup(data)
	authorTags=soup.findAll(attrs={'class':'articleAuthors'})

	authorList=[]
	for tag in authorTags:
		curr_list=''
		for item in tag:
			try: curr_list+=item.string
			except: pass
		curr_names=[]
		for name in curr_list.split(','):
			for nameA in name.split(' and '):
				curr_names.append(nameA.strip())
		authorList.append( curr_names )
	
	return authorList

import numpy
def scrape_langmuir():
	lang_authors=[]

	for volume in numpy.arange(1,26):
		lang_authors.append([])
		for issue in numpy.arange(1,25):
			url='http://pubs.acs.org/toc/langd5/'+str(volume)+'/'+str(issue)
			try: 
				lang_authors[volume-1].append( scrapeACSAuthors(url) )
				print 'Vol %d Iss %d' % (volume,issue)
			
			except: print 'Volume %d Issue %d did not exist!' % (volume,issue)
	
	return lang_authors

def scrape_acs_journal(codename,maxvols,maxissues=52):
	authors=[]

	for volume in range(maxvols):
		authors.append([])
		failcount=0
		for issue in range(maxissues):
			url='http://pubs.acs.org/toc/'+codename+'/'+str(volume+1)+'/'+str(issue+1)
			try:
				authors[volume].append( scrapeACSAuthors(url) )
				print '%s v%d i%d' % (codename,volume+1,issue+1)
			except:
				print '%s v%d i%d failed!' % (codename,volume+1,issue+1)
				failcount+=1
			if failcount>3: break
	return authors

def avg_coauthors(volumeList):

	authorcount=[]
	titlecount=[]

	n=0
	for volume in volumeList:
		for issue in volume:
			n+=1
			authorcount.append(0)
			titlecount.append(len(issue))
			for article in issue:
				authorcount[n-1]+=len(article)
			authorcount[n-1]=float(authorcount[n-1])/len(issue)
	
	return authorcount,titlecount
