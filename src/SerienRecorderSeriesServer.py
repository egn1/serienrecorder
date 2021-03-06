# coding=utf-8

# This file contains the SerienRecoder Serien Server stuff

# Constants
SERIES_SERVER_URL = 'http://www.serienserver.de/cache/cache.php'

try:
	import xmlrpclib
except ImportError as ie:
	xmlrpclib = None

class SeriesServer:

	def __init__(self):
		# Check dependencies
		if xmlrpclib is not None:
			self.server = xmlrpclib.ServerProxy(SERIES_SERVER_URL, verbose=False)

	def getSeriesID(self, seriesName):
		return self.server.sp.cache.getID(seriesName)

	def getSeriesInfo(self, seriesID):
		seriesInfo = self.server.sp.cache.getSeriesInfo(seriesID)
		infoText = ""

		# Title
		if 'title' in seriesInfo:
			infoText += seriesInfo['title']

		# Fan count
		if 'fancount' in seriesInfo:
			infoText += ("\n\nDie Serie hat %s Fans" % seriesInfo['fancount'])

		# Rating
		if 'rating' in seriesInfo:
			infoText += (" und eine Bewertung von %s" % seriesInfo['rating'])

		# Sex
		if 'male' in seriesInfo and 'female' in seriesInfo and 'age' in seriesInfo:
			infoText += ("\nZielgruppe: %s (Männer: %s, Frauen: %s)" % (seriesInfo['age'], seriesInfo['male'], seriesInfo['female']))

		# Transmission info
		infoText += "\n\n"
		if 'seasons_and_episodes' in seriesInfo:
			glue = ', '
			infoText += "%s\n" % glue.join(seriesInfo['seasons_and_episodes'])

		if 'transmissioninfo' in seriesInfo:
			infoText += "%s\n" % seriesInfo['transmissioninfo']

		infoText += "\n"
		# Description
		if 'description' in seriesInfo:
			infoText += seriesInfo['description'].encode('utf-8')

		# Info
		if 'info' in seriesInfo:
			infoText += "\n\n%s" % seriesInfo['info']

		# Upfronts
		infoText += "\n\n"
		if 'upfronts' in seriesInfo:
			glue = '\n'
			infoText += "%s\n" % glue.join(seriesInfo['upfronts'])

		# Cast / Crew
		if 'cast' in seriesInfo:
			glue = "\n"
			infoText += "\n\nCast und Crew:\n%s\n\n%s" % (glue.join(seriesInfo['cast']).encode('utf-8'), glue.join(seriesInfo['crew']).encode('utf-8'))
		return infoText

	def getEpisodeInfo(self, url):
		episodeInfo = self.server.sp.cache.getEpisodeInfo(url)
		infoText = ""

		if 'season' in episodeInfo and 'episode' in episodeInfo:
			infoText += "Staffel: %s, Episode: %s\n" % (episodeInfo['season'], episodeInfo['episode'])

		# Title
		if 'title' in episodeInfo:
			infoText += "Titel: %s" % episodeInfo['title'].encode('utf-8')

		if 'otitle' in episodeInfo:
			infoText += "\n"
			infoText += "Originaltitel: %s" % episodeInfo['otitle'].encode('utf-8')

		# Rating
		if 'rating' in episodeInfo:
			infoText += "\n\n"
			infoText += episodeInfo['rating']

		# Transmissions
		infoText += "\n\n"
		if 'transmissions' in episodeInfo:
			glue = "\n"
			infoText += "%s\n" % glue.join(episodeInfo['transmissions']).encode('utf-8')

		if 'description' in episodeInfo:
			infoText += "\n\n"
			infoText += "%s\n" % episodeInfo['description'].encode('utf-8')

		# Cast / Crew
		if 'cast' in episodeInfo:
			glue = "\n"
			infoText += "\n\nCast und Crew:\n%s" % glue.join(episodeInfo['cast']).encode('utf-8')
		return infoText


	def doSearch(self, searchString):
		resultList = []
		try:
			searchResults = self.server.sp.cache.searchSeries(searchString)
			for searchResult in searchResults['results']:
				resultList.append((searchResult['name'].encode('utf-8'), searchResult['country_year'].encode('utf-8'), str(searchResult['id'])))
			if 'more' in searchResults:
				resultList.append(("... %s'%s'" % ("Es gibt weitere Ergebnisse für ", searchString.encode('utf-8')), str(searchResults['more']), "-1"))
		except:
			resultList = []
		return resultList

	def doGetCoverURL(self, seriesID, seriesName):
		return self.server.sp.cache.getCoverURL(int(seriesID), seriesName)

	def doGetWebChannels(self):
		return self.server.sp.cache.getWebChannels()

	def doGetPlanerData(self, planertype, offset, webChannels):
		return self.server.sp.cache.getPlanerData(int(planertype), int(offset), webChannels)

	def doGetEpisodes(self, seriesID, page):
		return self.server.sp.cache.getEpisodes(int(seriesID), int(page))

	def doGetTransmissions(self, seriesID, offset, webChannels):
		resultList = []
		transmissions = self.server.sp.cache.getTransmissions(int(seriesID), int(offset), webChannels)
		seriesName = transmissions['series']

		for event in transmissions['events']:
			if event['season'] is '':
				event['season'] = '0'
			resultList.append([seriesName.encode('utf-8'), event['channel'].encode('utf-8'), event['start'], event['end'], event['season'], event['episode'], event['title'].encode('utf-8'), "0"])

		return resultList