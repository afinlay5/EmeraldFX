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

from java.util import ArrayList
from InvalidSHEOperationException import InvalidSHEOperationException

class SessionHistoryElement(ArrayList):
	#You could also implement java.lang.List()
	def __init__(self, HDE):
		ArrayList.__init__(self, 3)
		super(SessionHistoryElement,self).add(0,HDE.get(1)) #URL
		super(SessionHistoryElement,self).add(1,HDE.get(2)) #Title
		super(SessionHistoryElement,self).add(2,HDE.get(3)) #DateTime

	#@Override
	def add(self, E): 
		'''This might be broken, all others are OK'''
		raise InvalidSHEOperationException("add(E e)")
	#@Override
	def add(self, index, element):			
		raise InvalidSHEOperationException("add(int index, E element)")
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

#from java.util import Arrays
#test = SessionHistoryElement(Arrays.asList(1,2,3))
#test.sort(1)