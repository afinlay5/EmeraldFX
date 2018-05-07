#! /usr/bin/env jython
"""
=================================================================================
LICENSE: GNU GPL V2 (https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

EmeraldFX, a web Browser written with JavaFX written in Jython, Java, & Python.
Copyright (C) <2018>  ADRIAN D. FINLAY.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Adrian D. Finlay, hereby disclaims all copyright interest in the program
`EmeraldFX' (which makes passes at compilers) written by Oracle Corporation, 
The Jython Development Tean.

Adrian D. Finlay, May 7, 2018
Adrian D. Finlay, Founder
www.adriandavid.me
Contact: adf5152@live.com
=================================================================================
"""

from java.lang import System #java.lang.System
from SessionHistoryElement import SessionHistoryElement
from HistoryDataElement import HistoryDataElement

from java.io import File #java.io.File
from java.io import FileWriter #java.io.FileWriter
from java.io import PrintWriter #java.io.PrintWriter
from java.io import BufferedWriter #java.io.BufferedWriter
from java.io import Serializable #java.io.Serializable
from java.util import ArrayList #java.util.ArrayList
from java.util import LinkedHashMap #java.util.LinkedHashMap
from java.time import LocalDateTime #java.time.LocalDateTime
from java.nio.file import Files #java.nio.file.Files

#Ideally we would want this class to be a Singleton.
#However, the plumbing for this concept isn't so elegantly available in Python 2.7
class BrowserSession: #BrowserSession(Serializable):
	'''THIS CLASS IS A SINGLETON'''

	#Browser History Flag
	IS_HISORY_CLEARED = False
	#Singleton Flag
	SINGLETON_SWITCH = False


	#Initializer
	def __init__(self, HDE):

		'''Was not aware of JavaFX's WebHistory class... for future consideration'''

		if BrowserSession.SINGLETON_SWITCH is True:
			raise Exception("Singleton: Only one instance of this class is allowed.")

		#All Data for the Browser Session
		self.__AllURLs = LinkedHashMap() #LinkedHashMap <URL, UUID>
		self.__AllTitles = LinkedHashMap() #LinkedHashMap <Title, UUID>
		#Functioning under assumption that all LocalDatetimes will be unique at least up to 
		#a microsecond (10^-6). We could not (under circumstances of itended use) get two of the same exact times.
		self.__AllDateTimes = LinkedHashMap() #LinkedHashMap <LocalDateTime, UUID>	
		
		#Set Initial value for SessionHistoryElement
		self.__currentSessionHistoryElement = SessionHistoryElement(HDE)
		self.__currentSessionHistoryElementList = ArrayList()
		self.__currentSessionHistoryElementList.add(self.__currentSessionHistoryElement)

		#Set Initial values for current, UUID, URL, Title, DateTime
		self.__currentUUID = HDE.getUUID()   	 #java.util.UUID
		self.__currentURL = HDE.getURL()   		 #java.lang.String
		self.__currentTitle =  HDE.getTitle() 	 #java.lang.String
		self.__currentDateTime = HDE.getDateTime()  # The default page's corresponding LocalDateTime	

		#List for navigating URLs
		self.__Navigation = ArrayList()
		self.__Navigation.add(self.__currentURL)

		#Add Intial values to master collections
		self.__AllURLs.put (self.__currentURL, self.__currentUUID, ) 
		self.__AllTitles.put (self.__currentTitle, self.__currentUUID )
		self.__AllDateTimes.put (self.__currentDateTime, self.__currentUUID )	
		
		#Bidirectional Iterator to walk browser history
		self.__iterator = self.__Navigation.listIterator(1);

		#Add a SessionHistoryElement to the Session's History
		self.__SessionHistory = LinkedHashMap()
		#java.util.LinkedHashMap<UUID, List<SessionHistoryElement>>
		self.__SessionHistory.put(self.__currentUUID, self.__currentSessionHistoryElementList)

		#Facilities for writing history to file
		self.__writeHistoryEntry = PrintWriter( BufferedWriter( FileWriter( File("../resources/history/HISTORY.csv"), True) ) )

		#Upon instantiation, if we already have a history file with valid entries, set the flag to resumed
		if File("../resources/history/HISTORY.csv").length() > 0L:
			self.__JUST_RESUMED_FLAG = True
		else:
			self.__JUST_RESUMED_FLAG = False
				
		#Log
		print("\nLog: BrowserSession successfully instantiated @ " +  str(LocalDateTime.now()))
		print("Log: BrowserSession(Default Page Info):  T:\"" + self.__currentTitle + "\" , U:\""+ self.__currentURL + "\"\n")

		#Flip Singleton switch
		BrowserSession.SINGLETON_SWITCH = True

	## Utility Methods ##
	#4/4 WORKING
	def getTitleByUUID(self, UUID):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None		
		#Grab SessionHistoryElementList by UUID
		sheList = self.__SessionHistory.get(UUID)
		
		if sheList is None:
			print("Log: -------There is no data associated with this UUID: \"" + str(UUID) + "\"")
			return None
		else:
			#No matter which SessionHistoryElement we grab, they all
			#will have the same Title
			return sheList.get(0).get(1)
	def getURLByUUID(self, UUID):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		#Grab SessionHistoryElementList by UUID
		sheList = self.__SessionHistory.get(UUID)

		if sheList is None:
			print("Log: -------There is no data associated with this UUID: \"" + str(UUID) + "\"")
			return None
		else:
			#No matter which SessionHistoryElement we grab, they all
			#will have the same URL
			return sheList.get(0).get(0)
	def getDateTimesByUUID(self, UUID):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		#List Holding LocalDateTimes found
		dtList = ArrayList()

		#Determine if it's there to begin with
		if not self.__AllDateTimes.containsValue(UUID):
			print("No visit found for this UUID: \"" + str(UUID) + "\"")
			return None
		else:
			#filter = lambda K,V: dtList.add(K) if self.__AllDateTimes.get(K) == UUID else None
			#self.__AllDateTimes.forEach(filter)
			
			for dt in self.__AllDateTimes.keySet():
				if self.__AllDateTimes.get(dt) == UUID:
					dtList.add(dt)		
		return dtList
	def getSessionHistoryElementListByUUID(self, UUID):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__SessionHistory.get(UUID)
	
	#2/2 WORKING
	def getUUIDbyURL (self, URL):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None
		urls = self.__AllURLs.keySet()
		#First figure out if the URL was visited
		for _url in urls:
			if _url == URL:
				UUID = self.__AllURLs.get(_url)
				return UUID
		#It's not there
		else:
			return False
	def getDateTimesByURL(self, url):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		#Find the UUID associated with the URL.
		UUID = self.__AllURLs.get(url)
		#Find the DateTimes associated with this URL.
		dateTimesbyURL = ArrayList()
		#for ( Set<Map.Entry<K,V>> : LinkedHashMap<LocalDateTime, UUID> )
		for entry in self.__AllDateTimes.entrySet():
			if entry.getValue() == UUID:
				dateTimesbyURL.add(entry.getKey())
		if dateTimesbyURL.isEmpty() is True:
			print("Log: -------There is no data associated with this UUID: \"" + str(url) + "\"")
			return None
		else:
			return dateTimesbyURL	

	#2/2 WORKING
	def getCurrentSessionHistoryElement(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentSessionHistoryElement
	def getCurrentSessionHistoryElementList(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentSessionHistoryElementList

	#3/3 WORKING
	def getAllURLs(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__AllURLs.keySet()
	def getAllTitles(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__AllTitles.keySet()
	def getAllDateTimes(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__AllDateTimes.keySet()

	#5/5 WORKING
	def getCurrentUUID(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentUUID
	def getCurrentURL(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentURL
	def getCurrentTitle(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentTitle
	def getCurrentDateTime(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__currentDateTime
	def getNumVisits(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		#Tally amount of DateTimes
		return self.__AllDateTimes.keySet().size()
	
	#6/6 WORKING - '''Do not use these arbitrarily/outside of this class! They rely on each other!!'''
	def __setCurrentUUID(self, UUID):	
		'''Set Current UUID'''	
		self.__currentUUID = UUID
	def __setCurrentURL(self, URL):	
		'''Set Current URL'''			
		self.__currentURL = URL
	def __setCurrentTitle(self, Title):	
		'''Set Current Title'''	
		self.__currentTitle = Title
	def __setCurrentDateTime(self, DateTime):			
		'''Set Current LocalDateTime'''			
		self.__currentDateTime = DateTime
		#Update Master List
		self.__AllDateTimes.put(DateTime, self.getCurrentUUID())
	def __setCurrentSessionHistoryElement(self, newSHE):		
		'''Set Current Session History Element'''			
		self.__currentSessionHistoryElement = newSHE
	def __setCurrentSessionHistoryElementList(self, newSHEList):		
		'''Set Current Session History Element List'''			
		self.__currentSessionHistoryElementList = newSHEList
		
	#4/4 WORKING
	def hasNext(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		return self.__iterator.hasNext()
	def hasPrevious(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		# For our purposes, ignore index 0.
		elif self.__iterator.previousIndex() == 0:
			return False
		else:
			return self.__iterator.hasPrevious()
	def hasVisited(self, URL):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		elif self.__AllURLs.keySet().contains(URL):
			return True
		else:
			return False
	def isHistoryCleared(self):
		'''Check if the history is cleared'''
		return BrowserSession.IS_HISORY_CLEARED

	#2/2 WORKING - '''Do not use these arbitrarily/outside of this class! They rely on each other!!'''
	def __updateDateTimeMasterListByUUID(self, UUID, dateTime):	
		'''Add a DateTime to master collection by UUID'''
		self.__AllDateTimes.put(dateTime, UUID)
	def __updateSessionHistoryListByUUID(self, UUID, sheList):			
		'''Update SessionHistoryList by UUID'''
		self.__SessionHistory.put(UUID, sheList)
	
	#2/2 WORKING
	def getCurrentSessionHistoryEntry(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		from java.util.AbstractMap import SimpleImmutableEntry
		return SimpleImmutableEntry(self.__currentUUID, self.__currentSessionHistoryElement)
	def getPreviousSessionHistoryEntry(self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None	

		from java.util.AbstractMap import SimpleImmutableEntry
		'''
			Avoid tampering with existing iterator
			That is there for doing page navigation
			Note that last entry is defined in terms of last visit (LocalDateTime)
			Start at the end of the ArrayList<LocalDateTime> list.
			The Map's size will be equivilant to the size of the set from Map.keySet()
		'''
		if self.__AllDateTimes.size() == 1:	
			print ('Log: -------Operation Failed: There is no prior session history data.')
			print ('The CurrentSessionHistoryEntry(Key): ' + str(self.getCurrentSessionHistoryEntry().getKey()) )
			print ('The CurrentSessionHistoryEntry(Value): ' + str(self.getCurrentSessionHistoryEntry().getValue()) )
			return None
		else:

			#Grab the previous DateTime
			DT = ArrayList(self.__AllDateTimes.keySet()).listIterator(self.__AllDateTimes.size()-1).previous();
			
			#Grab The Associated UUID
			UUID = self.__AllDateTimes.get(DT)		

			#Get SessionHistoryElementList
			sheList = self.getSessionHistoryElementListByUUID(UUID)

			#Iterate through the list to find the correct SessionHistoryElement by DateTime
			for she in sheList:	
				if she.get(2) == DT:
					#Return as java.util.AbstractMap.SimpleImmutableEntry<UUID, SHE>
					return SimpleImmutableEntry(UUID, she)
	def getHistoryWriter(self):
		return self.__writeHistoryEntry 
	#6/6 WORKING
	def addVisit(self, HDE):	

		#Write to History File
		self.writeHistoryToFile(HDE.getDateTime(), HDE.getUUID(), HDE.getURL(), HDE.getTitle())

		#If this is a new entry
		if self.__SessionHistory.get(HDE.getUUID()) is None:
			#Update the Session History
			SHE = SessionHistoryElement(HDE)
			SHEList = ArrayList()
			SHEList.add(SHE)
			self.__updateSessionHistoryListByUUID(HDE.getUUID(),SHEList)
			
			#Update the Data for the Browser Session
			self.__AllURLs.put(HDE.getURL(),HDE.getUUID())
			self.__AllTitles.put(HDE.getURL(), HDE.getUUID())
			self.__updateDateTimeMasterListByUUID(HDE.getUUID(), HDE.getDateTime())

			#Update the currentSessionHistoryElement, currentSessionHistoryElementList
			self.__currentSessionHistoryElement = SHE
			self.__currentSessionHistoryElementList = ArrayList()
			self.__currentSessionHistoryElementList.add(SHE)

			#Update Current Session Information
			self.__setCurrentUUID(HDE.getUUID())
			self.__setCurrentURL(HDE.getURL())
			self.__setCurrentTitle(HDE.getTitle())
			self.__setCurrentDateTime(HDE.getDateTime())

		#Existing entry, just update a visit(LocalDateTime)
		else:
			#Update the SessionHistory
			sheList = self.__SessionHistory.get(HDE.getUUID())
			sheList.add(SessionHistoryElement(HDE))

			#Add a visit
			self.__updateDateTimeMasterListByUUID(HDE.getUUID(), HDE.getDateTime())
			self.__setCurrentDateTime(HDE.getDateTime())

		#Update the Navigable List
		self.__Navigation.add(HDE.getURL())

		#Let clients know the BrowserSession is no longer empty
		if BrowserSession.IS_HISORY_CLEARED is True:
			BrowserSession.IS_HISORY_CLEARED = False

		#Update the iterator, move it to the most recent
		#This is almost certainly not efficient. Something to consider for the future.
		self.__iterator = self.__Navigation.listIterator(self.__Navigation.size()-1)
	def navigateBackward(self):
		''' 
			Returns the URL to go back to or 'None' if none exists.
			Some of these checks are unecessary, provided we make use of hasPrevious().
		'''
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Backward Operation Failed: There is no previous page.")
			return None			
		#Can't go back
		elif self.__iterator.previousIndex() == -1:
			print("Log: -------Backward Operation Failed: There is no previous page.")
			return None
			#We will null check and respond with dialog box in EmeraldFX.py
		#Let's go back
		else :
			#Position iterator between n-1 and n-2
			if self.__iterator.nextIndex() == self.__Navigation.size():
				self.__iterator.previous() # We already know the first URL, so discard
				UUID = self.getUUIDbyURL(self.__currentURL)
			else: 
				#Grab UUID associated with the previous DateTime, move the iterator back one
				UUID = self.getUUIDbyURL(self.__iterator.previous())

			#DT that we navigated backwards
			backwards_dt = LocalDateTime.now()
			
			#Update Current Session Information
			self.__setCurrentUUID(UUID)
			self.__setCurrentTitle(self.getTitleByUUID(UUID))
			self.__setCurrentURL(self.getURLByUUID(UUID))
			self.__setCurrentDateTime(backwards_dt)

			#Add to DateTime Master List
			self.__updateDateTimeMasterListByUUID(UUID,backwards_dt)

			#URL
			URL = str(self.getURLByUUID(UUID))

			#Create a new HistoryDataElement - UUID, URL, Title, DateTime)
			newHDE = HistoryDataElement(UUID, URL, str(self.getTitleByUUID(UUID)), backwards_dt)

			#Create new CurrentSessionHistoryElement
			newSHE = SessionHistoryElement(newHDE)

			#Grab existing SessionHistoryElementList and update it, then set it as the CurrentSessionHistoryElementList
			updSHEList = self.getSessionHistoryElementListByUUID(UUID)
			updSHEList.add(newSHE)
			
			#Update CurrentSessionHistoryElement, CurrentSessionHistoryElementList
			self.__setCurrentSessionHistoryElement(newSHE)
			self.__setCurrentSessionHistoryElementList(updSHEList)

			#Update SessionHistory Master List
			#self.__updateSessionHistoryListByUUID(UUID, updSHEList)
			#Unnecessary ^ the List<SessionHistoryElement> is already updated and will function properly
			#when calling getPreviousSessionHistoryEntry()

			#Logs
			print("Log: -------Navigated Backwards to: \"" + str(URL) + "\"@" + str(backwards_dt))

			#Write to History File
			self.writeHistoryToFile(newHDE.getDateTime(), newHDE.getUUID(), newHDE.getURL(), newHDE.getTitle())

			#Let clients know the BrowserSession is no longer empty
			if BrowserSession.IS_HISORY_CLEARED is True:
				BrowserSession.IS_HISORY_CLEARED = False

			return URL
	def navigateForward(self):
		''' 
			Returns the URL to go forward to or 'None' if none exists.
			Some of these checks are unecessary, provided we make use of hasNext().
		'''
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Forward Operation Failed: There is no subsequent page.")
			return None			
		#Can't go forward
		elif self.__iterator.nextIndex() == self.__Navigation.size():
			print("Log: -------Forward Operation Failed: There is no subsequent page.")
			return None 
			#We will null check and respond with dialog box in EmeraldFX.py
		#Let's go forward
		else:
			#Grab UUID associated with the subsequent DateTime, advance iterator
			UUID = self.getUUIDbyURL(self.__iterator.next())
	
			#Grab URL based on UUID
			URL = self.getURLByUUID(UUID)

			#DT that we navigated backwards
			forwards_dt = LocalDateTime.now()
			
			#Update Current Session Information
			self.__setCurrentUUID(UUID)
			self.__setCurrentTitle(self.getTitleByUUID(UUID))
			self.__setCurrentURL(self.getURLByUUID(UUID))
			self.__setCurrentDateTime(forwards_dt)

			#Add to DateTime Master List
			self.__updateDateTimeMasterListByUUID(UUID,forwards_dt)

			#Create a new HistoryDataElement - UUID, URL, Title, DateTime)
			newHDE = HistoryDataElement(UUID, str(self.getURLByUUID(UUID)), str(self.getTitleByUUID(UUID)), forwards_dt)

			#Create new CurrentSessionHistoryElement
			newSHE = SessionHistoryElement(newHDE)

			#Grab existing SessionHistoryElementList and update it, then set it as the CurrentSessionHistoryElementList
			updSHEList = self.getSessionHistoryElementListByUUID(UUID)
			updSHEList.add(newSHE)
			
			#Update CurrentSessionHistoryElement, CurrentSessionHistoryElementList
			self.__setCurrentSessionHistoryElement(newSHE)
			self.__setCurrentSessionHistoryElementList(updSHEList)

			#Logs
			print("Log: -------Navigated Forwards to: \"" + str(URL) + "\"@" + str(forwards_dt))

			#Write to History File
			self.writeHistoryToFile(newHDE.getDateTime(), newHDE.getUUID(), newHDE.getURL(), newHDE.getTitle())

			#Let clients know the BrowserSession is no longer empty
			if BrowserSession.IS_HISORY_CLEARED is True:
				BrowserSession.IS_HISORY_CLEARED = False

			return URL
	def removeVisit(self):
		''' For future consideration '''
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		pass
	def removeVisitsByURL (self):
		''' For future consideration '''
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: There is no Browser History.")
			return None			
		pass
	def clearHistory (self):
		if BrowserSession.IS_HISORY_CLEARED is True:
			print("Log: -------Operation Aborted: The Browser History is already clear.")
			return	
		else:
			BrowserSession.IS_HISORY_CLEARED = True

		self.__AllURLs.clear()
		self.__AllTitles.clear()
		self.__AllDateTimes.clear()

		self.__currentURL = None
		self.__currentUUID = None
		self.__currentTitle = None
		self.__currentDateTime = None

		self.__currentSessionHistoryElement = None
		self.__currentSessionHistoryElementList.clear()
		# self.__currentSessionHistoryElementList.removeAll(self.__currentSessionHistoryElementList)

		self.__SessionHistory.clear()
		self.__iterator = None

		#Log
		print("Log: BrowserSession History successfully reset @ " +  str(LocalDateTime.now()))
		print("Log: BrowserSession(Default Page Info):  T:\"" + str(self.__currentTitle) + "\" , U:\""+ str(self.__currentURL) + "\"")

		#Delete Files
		File("../resources/history/HISTORY.csv").delete() if File("../resources/history/HISTORY.csv").exists() else None
		File("../resources/history/HISTORY.txt").delete() if File("../resources/history/HISTORY.txt").exists() else None
		print("Log: BrowserSession History File successfully deleted @ " +  str(LocalDateTime.now()) + '\n')

		#Nudge GC
		System.gc()
	
	#3/3 WORKING
	def writeHistoryToFile(self, DateTime, UUID, URL, Title):
		'''
			History will be stored in a CSV as follows (for now):
			DateTime,UUID,URL,Title
		'''

		#New History File
		if not File("../resources/history/HISTORY.csv").exists():
			self.__writeHistoryEntry = PrintWriter( BufferedWriter( FileWriter( File("../resources/history/HISTORY.csv"), True) ) )
			self.__writeHistoryEntry.println('LocalDateTime,UUID,URL,Title')
			self.__writeHistoryEntry.println('LDT:' + str(self.__currentDateTime) + "," + 'UUID:' + str(self.__currentUUID) + "," + 'URL:' + str(self.__currentURL) + "," + 'T' + str(self.__currentTitle))			
			return
		#Default History File
		elif File("../resources/history/HISTORY.csv").exists() and File("../resources/history/HISTORY.csv").length() == 0L:
			self.__writeHistoryEntry.println('LocalDateTime,UUID,URL,Title')
			self.__writeHistoryEntry.println( 'LDT:' + str(self.getCurrentDateTime()) + ',UUID:' + str(self.getCurrentUUID() ) + ",URL:"+ str(self.getCurrentURL() ) + ",T:" + str(self.getCurrentTitle()))	
		#Browser Resumed
		elif File("../resources/history/HISTORY.csv").length() > 0L and self.__JUST_RESUMED_FLAG:
			self.__writeHistoryEntry.println("\nBROWSER RESUMED @ " +str(LocalDateTime.now()))
			entry = 'LDT:' + str(DateTime) + "," + 'UUID:' + str(UUID) + "," + 'URL:' + str(URL) + "," + 'T:' + str(Title)
			self.__writeHistoryEntry.println(entry)
			self.__JUST_RESUMED_FLAG = False
		#Ordinary entry
		else:
			entry = 'LDT:' + str(DateTime) + "," + 'UUID:' + str(UUID) + "," + 'URL:' + str(URL) + "," + 'T:' + str(Title)
			self.__writeHistoryEntry.println(entry)	
	@staticmethod 
	def closeHistoryWriter(self):
		'''Close History Writer Stream'''
		self.__writeHistoryEntry.print("BROWSER CLOSED @ " +str(LocalDateTime.now()))
		self.__writeHistoryEntry.close()
		print("Log: History: History Writer successfully closed @ " +  str(LocalDateTime.now()) )
	def triggerHistoryWrite(self):
		self.__writeHistoryEntry.close()
		System.gc()
		self.__writeHistoryEntry = PrintWriter( BufferedWriter( FileWriter( File("../resources/history/HISTORY.csv"), True) ) )

'''
from java.util import UUID
bs = BrowserSession(HistoryDataElement(UUID.randomUUID(),"url","title",LocalDateTime.now()))
bs.writeHistoryToFile("Now", "UUID1", "URL", "boogawooga")
bs.writeHistoryToFile("Later", "UUID2", "URL", "boogawoo")
bs.clearHistory()
bs.writeHistoryToFile("Later", "UUID2", "URL", "boogawoo")
bs.writeHistoryToFile("Last", "UUID3", "URL", "booga")
BrowserSession.closeHistoryWriter(bs)
'''