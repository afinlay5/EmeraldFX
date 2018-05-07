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