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