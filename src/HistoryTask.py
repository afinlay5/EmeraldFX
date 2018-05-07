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

from java.lang import Double
from java.io import FileReader
from java.lang import Runnable
from java.lang import StringBuffer
from java.io import BufferedReader
from javafx.concurrent import Task
from javafx.application import Platform
from java.util.concurrent import CountDownLatch

class HistoryTask(Task):
	def __init__(self,hist_file,textArea):
		print("Log: Concurrency: History Task Initialized.")
		self.hist_file = hist_file
		self.textArea = textArea

	#@Override
	def call(self):
		#CountdownLatch
		latch = CountDownLatch(1)

		#Read History.txt into TextArea
		br = BufferedReader(FileReader(self.hist_file))

		#Runnable Inner Class
		class HistoryTaskRunnable (Runnable):
			def __init__(self, textArea, br):
				self.textArea = textArea
				self.br = br
				self.sbf = StringBuffer()
			#@Override
			def run(self):
				while True:
					line = self.br.readLine()
					if line != None:
						self.sbf.append(line + "\n")
						# self.textArea.appendText(line + "\n") - Very slow
					else:
						break
				#Add Text to TextArea
				self.textArea.setText(self.sbf.toString())
				self.textArea.appendText("") #Used to trigger event handler
				#Close Buffered Reader
				br.close()

		#Run Later
		Platform.runLater(HistoryTaskRunnable(self.textArea, br))
			
		#Set Starting positions
		textArea.setScrollLeft(Double.MAX_VALUE)
		textArea.setScrollTop(Double.MAX_VALUE)

		#Make the Application Thread wait
		latch.await()