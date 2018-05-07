"""
Copyright (C) 2018 Adrian D. Finlay. All rights reserved.

Licensed under the MIT License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://opensource.org/licenses/MIT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
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