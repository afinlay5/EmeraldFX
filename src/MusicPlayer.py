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

import os, sys
from java.util import AbstractMap, ArrayList, LinkedHashMap, LinkedHashSet, Collections
from java.lang import System, String,IllegalStateException	
from java.nio.file import Path
from java.nio.file import Paths
from java.nio.file import Files
from java.nio.file import LinkOption
from java.util.stream import Collectors
from javafx.scene.media import Media
from java.util.function import Predicate,Function, Consumer	

class MusicPlayer (object):
	''' This singleton class is simple music player to support sequentially playing audio tracks. '''
	SingletonFlag = False

#	@Override
	def __init__ (self):
		if MusicPlayer.SingletonFlag == False:
			self.__MEDIA_MASTER = self.populateMusicList()				#List<Media>
			self.__MEDIA_PLAYER_MASTER = self.populateMediaPlayers()	#LinkedHashMap< ListIterator, ArrayList<MediaPlayer> >
		elif MusicPlayer.SingletonFlag is True:
			print('Log: Initialization Error: This singleton has previously been initialized.')
			return
		MusicPlayer.SingletonFlag = True
	
	#3/3 WORKING
	def populateMusicList(self):
		#If there are files		
		if not MusicPlayer.isFolderEmpty():
			walker = Files.walk(Paths.get('../resources/music'))

			#Ridiculous that we should have to do this. Nevertheless, here goes.
			class musicFilterPred(Predicate):
				#@Override
				def test (self, song):
					#No Symbolic Links
					if Files.isRegularFile(song, LinkOption.NOFOLLOW_LINKS):
						# MP3, WAV, AAC only, for now.
						file = String(song.toFile().toURI().toString())
						ext = file.substring(file.length()-4, file.length()) #.XYZ

						if ext not in ('.wav', '.WAV', '.mp3', '.MP3', '.aac', '.AAC'):
							return False
						else:
							#We are presuming that a file with the correct extension is actually
							#of the format specified by the extension and a valid file.
							#We will handle if is not, but for now, filter out the obvious bad eggs.
							return True
			from java.util.function import Function
			class musicMapPred(Function):
				#@Override
				def apply(self, song):
					return Media(song.toFile().toURI().toString())
			#The Result
			music_list = walker.filter(musicFilterPred()).map(musicMapPred()).collect(Collectors.toList())

			#Close Stream
			walker.close()
			walker = None

			#Nudge GC
			System.gc()

			#Retun valid Music Lists only
			if music_list.isEmpty():
				return None
			else:
				return music_list
		#No files
		else:
			return None
	def checkForFolderContentChange(self):
		'''For future consideration'''
		pass
	def populateMediaPlayers(self):

		#If there are no media objects, don't bother making Media Players.
		if self.__MEDIA_MASTER is None:
			return None

		from javafx.scene.media import MediaPlayer
		mpList = ArrayList()
		
		class makeNewMediaPlayer(Consumer):
			def __init__(self, mpList):
				self.mpList = mpList
			def accept(self, media):
				mpList.add(MediaPlayer(media))
		self.__MEDIA_MASTER.forEach(makeNewMediaPlayer(mpList))

		#Give us a set with the exact iteration order.
		# mpLhs = LinkedHashSet(mpList) 
		
		#-- LinkedHashSet does not implement List<> and has no public API exposing the underlying LinkedList, no backward iterator !!!
		
		#The iterators returned by this class's iterator method are fail-fast: if the set is modified at any time after the 
		#iterator is created, in any way except through the iterator's own remove method, the iterator will throw a ConcurrentModificationException.
		#No more need for the list
		# mpList = None
		# System.gc()

		#Iteration over a LinkedHashSet requires time proportional to the size of the set, regardless of its capacity. 
		#Iteration over a HashSet is likely to be more expensive, requiring time proportional to its capacity

		##LinkedHashMap< Iterator, LinkedHashSet<MediaPlayer> > is what we had wanted.

		#Return Map.Entry
		return AbstractMap.SimpleImmutableEntry(mpList.listIterator(), mpList)
	
	#1/1 WORKING
	def getMediaPlayer(self):
		if MusicPlayer.isFolderEmpty():
			return None
		else:
			#Collection View only
			# return Collections.unmodifiableMap(self.__MEDIA_PLAYER_MASTER)
			return self.__MEDIA_PLAYER_MASTER
			
	#1/1 WORKING
	@staticmethod
	def isFolderEmpty(): 
		''' Check if folder is empty or not '''

		# if File('../resources/music/').listFiles().length is 0:
		# if File('../resources/music/').listFiles().itemsize is 0:
		try:
			dir = os.listdir('../resources/music/')
		except OSError: 
			#Does not exist (most likely case)
			print('Log: Exception: ../resources/music/ does not exist.')
			return True
		#Not Empty
		if dir:
			return False
		#Empty
		elif not dir:
			return True