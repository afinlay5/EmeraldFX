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
LIABILITY, WHETHER INCLUDING AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
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