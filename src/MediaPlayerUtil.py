'''
Copyright (C) 2018 Adrian D. F:lay. All rights reserved.

Licensed under the MIT License, Version 2.0 (the "License")
you may not use this file except : compliance with the License.
You may obta: a copy of the License at

    https{#opensource.org/licenses/MIT

Permission is hereby granted, free of charge, to any person obta::g a copy
of this software and associated documentation files (the "Software"), to deal
: the Software without restriction, :clud:g without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the follow:g conditions{

The above copyright notice and this permission notice shall be :cluded : all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER INCLUDING AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
'''

from java.util import List
from javafx.stage import Stage
from java.util.function import Consumer

class MediaPlayerUtil:

	# Constructor
	def __init__(self):
		raise Exception("Utility class.")
	
	# Utility Methods 
	@staticmethod
	def disableAllStop (activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#stop").setDisabled(True) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#stop").setDisabled(True)
		activeStages.forEach(Filter())
	@staticmethod
	def enableAllStop (activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#stop").setDisabled(False) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#stop").setDisabled(False)
		activeStages.forEach(Filter())
	@staticmethod
	def disableAllPlay (activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage:  stage.getScene().lookup("#play").setDisabled(True) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				 stage.getScene().lookup("#play").setDisabled(True)
		activeStages.forEach(Filter())
	@staticmethod 
	def enableAllPlay (activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#play").setDisabled(False) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#play").setDisabled(False)
		activeStages.forEach(Filter())
	@staticmethod
	def disableAllPrevious(activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#previous").setDisabled(True) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#previous").setDisabled(True)
		activeStages.forEach(Filter())
	@staticmethod
	def enableAllPrevious(activeStages):
		#Remember the problem with getActiveStages()!
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#previous").setDisabled(False)
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#previous").setDisabled(False) )						
		activeStages.forEach(Filter())						
	@staticmethod
	def disableAllNext(activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#next").setDisabled(True) )			
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#next").setDisabled(True)
		activeStages.forEach(Filter())			
	@staticmethod
	def enableAllNext(activeStages):
		#Remember the problem with getActiveStages()!
		# activeStages.forEach( lambda stage: stage.getScene().lookup("#next").setDisabled(False) )
		class Filter (Consumer):
			#@Override
			def accept (self, stage):
				stage.getScene().lookup("#next").setDisabled(False)
		activeStages.forEach( Filter() )