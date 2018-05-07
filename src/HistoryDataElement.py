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

from java.util import ArrayList #java.util.ArrayList
from java.time import LocalDateTime #java.time.LocalDateTime
from java.util import UUID #java.util.UUID

class HistoryDataElement(ArrayList):

	#Initializer
	def __init__(self,uuid,url,title,dateTime):    

		'''HistoryDataElements must have at least one UUID, URL, Title, & DateTime '''
		valid = (type(uuid) is UUID) and (isinstance(url,str))	and (isinstance(title,str)) and (type(dateTime) is LocalDateTime)

		if not valid:
			from InvalidHistoryDataElementException import InvalidHistoryDataElementException
			raise InvalidHistoryDataElementException()
		else:
			super(HistoryDataElement,self).add(0, uuid)
			super(HistoryDataElement,self).add(1, url)
			super(HistoryDataElement,self).add(2, title)
			super(HistoryDataElement,self).add(3, dateTime)
			print("Log: HistoryDataElement object constructed @ " +  str(LocalDateTime.now()) + " with UUID: " + str(self.get(0)))

	#Utility Methods	
	def getUUID(self):
		return self.get(0)
	def getURL(self):
		return self.get(1)
	def getTitle(self):
		return self.get(2)
	def getDateTime (self):
		return self.get(3)

	# @Override of java.lang.ArrayList's inherited add(T)
	def add(self,T):
		if type(T) is not LocalDateTime:
			print("You may only add another visit (java.time.LocalDateTime) to an existing URL.")
		else:
			ArrayList.add(self, T)	
	'''
	#@Override
	#def add(self, index, element):			
	#"Omitted because attempt to directly invoke superclass method was unsuccessful."
	#raise InvalidSHEOperationException("add(int index, E element)")
	'''
	#@Override
	def addAll(self, collection):
		raise InvalidSHEOperationException("addAll(Collection<? extends E> c)")
	#@Override
	def addAll(self, index, collection):
		raise InvalidSHEOperationException("addAll(int index, Collection<? extends E> c)")
	#@Override
	def clear(self):
		raise InvalidSHEOperationException("clear()")
	#@Override
	def isEmpty(self):
		print('SessionHistoryElement will always be of size: 3')
	#@Override
	def remove(self, E):
		raise InvalidSHEOperationException("remove(int index) or remove(Object o)")
	#@Override
	def removeAll(self, collection):
		raise InvalidSHEOperationException("removeAll(Collection<?> c)")
	#@Override
	def removeIF(self, filter):
		raise InvalidSHEOperationException("removeIf(Predicate<? super E> filter)")
	#@Override
	def removeRange(self, _from, to):
		raise InvalidSHEOperationException("removeRange(int fromIndex, int toIndex)")
	#@Override
	def replaceAll(self, op):
		raise InvalidSHEOperationException("replaceAll(UnaryOperator<E> operator)")
	#@Override
	def retainAll(self,collection):
		raise InvalidSHEOperationException("retainAll(Collection<?> c)")
	#@Override
	def set (self,index, e):
		raise InvalidSHEOperationException("set(int index, E element)")
	#Override
	def sort(self, comparator):
		raise InvalidSHEOperationException("sort(Comparator<? super E> c)")


#Test
# hde = HistoryDataElement(UUID.randomUUID(), "http://www.adriandavid.me/", "Adrian David | Homepage", LocalDateTime.now())
#hde = HistoryDataElement("fail", "http://www.adriandavid.me/", "Adrian David | Homepage", LocalDateTime.now())
#hde.add(9)