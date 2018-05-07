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

from HistoryTask import HistoryTask
from javafx.concurrent import Service

class HistoryService(Service):
	count = 0

	def __init__(self,hist_file,textArea):
		self.hist_file = hist_file
		self.textArea = textArea
		print("Log: Concurrency: History Service Initialized.")

	#@Override
	def createTask(self):
		HistoryService.count +=1
		print("Log: Concurrency: History Service ran " + str(HistoryService.count) + " time(s).")
		return HistoryTask(self.hist_file,self.textArea)