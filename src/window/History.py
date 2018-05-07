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

import ComboShortcutKeys

from HistoryService import HistoryService
from BrowserSession import BrowserSession

from java.io import File
from java.time import LocalDateTime
from java.lang import Thread, String
from javafx.fxml import FXMLLoader, LoadException
from javafx.scene import Scene
from java.nio.file import Files
from javafx.application import Platform
from java.util.function import Consumer
from javafx.scene.image import Image, ImageView
from javafx.beans.value import ChangeListener
from javafx.scene.input import KeyEvent
from javafx.scene.layout import VBox

class EmeraldFX_History:

	def __init__(self, app, stage, BS):
		self.app = app
		self.stage = stage
		self.BS = BS

		#Supply an icon
		try:
			self.stage.getIcons().addAll(self.app._EmeraldFX__ICONS.get(0),self.app._EmeraldFX__ICONS.get(1),self.app._EmeraldFX__ICONS.get(2),self.app._EmeraldFX__ICONS.get(3),self.app._EmeraldFX__ICONS.get(4))
		except NullPointerException:
			print("Log: The application's icon file could not be found.")

	def show(self):
		#Root Pane
		root = VBox()
		#FXML Loader
		fxmlLoader = FXMLLoader()

		#TextArea
		from javafx.scene.control import TextArea
		textArea = TextArea("Loading . . .")

		#Configure Text Area
		textArea.setEditable(False)
		textArea.setPrefHeight(600)


		#Bottom Bar, Current Stylesheet
		if self.app.getCurrentTheme() == "Dark":
			fxmlLoader.setLocation(File("../resources/fxml/history_url_tab_dark.fxml").toURI().toURL()) #For some odd reason this is broken?
			bottom_bar = self.app.bottom_bar_dt
		elif self.app.getCurrentTheme() == "Light":
			fxmlLoader.setLocation(File("../resources/fxml/history_url_tab_light.fxml").toURI().toURL())
			bottom_bar = ImageView( Image(String(File('../resources/icons/bottom_bar_lt.png').toURI().toString()), True))
		#Think about future themes
		else:
			pass

		#URL Bar
		try:
			url_bar = fxmlLoader.load() #BROKEN - For some reason this breaks after a couple toggles.
		except LoadException as e:
			print('Log: Exception: An FXML Load Exception has occured.' + str(e.getCause()))
			

		#Add Children to root pane
		root.getChildren().addAll(url_bar, textArea, bottom_bar)

		#Fill Width, assume Theme of Main Stage
		root.setFillWidth(True)

		#Set scene, title
		scene = Scene(root,1350,625)

		#We are leaving the default controls for now.

		#Make sure the Text Area's scroll bar is always visible.
		scene.getStylesheets().add(File("../resources/themes/text-area_scroll-pane.css").toURI().toString())
		self.stage.setScene(scene)
		self.stage.setTitle("History - EmeraldFX")

		#Position History Stage
		self.stage.setX(self.app.getMainStage().getX())
		self.stage.setY(self.app.getMainStage().getY()+52)

		#Display History Stage
		self.stage.show()

		#It is CSV, let us display as plain text.
		history_csv = File("../resources/history/HISTORY.csv")
		history_txt = File("../resources/history/HISTORY.txt")

		#Delete text copy if it exists
		history_txt.delete() if history_txt.exists() else None

		#Copy
		Files.copy(history_csv.toPath(), history_txt.toPath())

		#Prevent Resizing 
		self.stage.setResizable(False)

		#Flush Stream
		self.BS.triggerHistoryWrite()


		#GetController instance
		controller = fxmlLoader.getController()
	

		''' Failed Attempts '''
		#WebView
		# webView = WebView()
		#Grab Web Engine
		# webEng = webView.getEngine()
		#Enable JS
		# webEng.setJavaScriptEnabled(True)

		#Attempt #1 - Start scrolling from the bottom - FAILED
		# webEng.executeScript("window.scrollTo(" + "0" + ", " + "600" + ");")

		#Attempt #2 - Scroll Pane - FAILED
		# from javafx.scene.control import ScrollPane
		# wv_scroll = ScrollPane()
		# wv_scroll.setVbarPolicy(ScrollPane.ScrollBarPolicy.ALWAYS)
		# wv_scroll.setContent(webView)
		# wv_scroll.setFitToWidth(True)
		# wv_scroll.setFitToHeight(True)
		# wv_scroll.setVvalue(wv_scroll.getVmin())

		#Load History
		# try:
			# webEng.load(history_txt.toURI().toString())
		# except Exception as e:
			# print ('Log: Load Exception: Error Loading History: ' + str(e.getCause()))
			# return

		#Attempt #3 - Execute Script for Scroll Bar - FAILD
		# webEng.executeScript(
			# "function scrollDown() { window.scrollTo(0,400); }" +
      		# "scrollDown();"
  		# )


		#Set Position of Scroll Bar
		class AnonInnerCL_TA(ChangeListener):
			"""Inner Class for Scrolling Down"""
			def __init__(self,textArea):
				self.textArea = textArea
			#@Override
			def changed (self, observable, old, new):
				if new > old:
					from java.lang import Double
					self.textArea.setScrollTop(Double.MAX_VALUE)
				else:
					pass
		textArea.textProperty().addListener( AnonInnerCL_TA(textArea))
		

		#Show History after it is loaded
		if self.stage.isShowing(): #May or may not be broken. If there is litle to no delay, "Loading . . ." will not be noticed.
			#Load History on separate thread.
			#Clear initial text: Loading . . .
			textArea.clear()
			#Instantate Service
			service = HistoryService(history_txt, textArea)
			#Algorithm improved. Start service
			service.start()


		'''Add resources to controller'''
		#Theme Resources
		controller.addThemeResources(self.app.getMainStage(), self.stage, self.app.getMainStage().getScene(), self.app.getCurrentTheme(), textArea) #(Stage mainStage, Stage histStage, Scene scene, String theme, TextArea textArea)
		#Clear Resource
		controller.addClearResources(self.BS.isHistoryCleared())  #(boolean)
		#Quit Resources
		controller.addQuitResources(self.app.getAllStages() , self.BS.getHistoryWriter() ) #(List<Stages>, PrintWriter)
		#Media Resources
		MMC = self.app.getMediaControls()
		controller.addMediaResources(MMC)

		#Create Bidirectional Bindings between Main Stage's media controls and history's controls
		from javafx.beans.binding import Bindings

		MMC_IT = MMC.listIterator()
		HMC = controller.getMediaControls()


		#Set history media controls to current state
		class HMCC(Consumer):
			def __init__(self, MMC_IT):
				self.MMC_IT= MMC_IT
			#@Override
			def accept(self, button):
				button.setDisabled(MMC_IT.next().isDisabled())
		HMC.forEach(HMCC(MMC_IT))
		
		#Fails - first arg cannot be coerced into Consumer? Odd.
		# history_media_controls.forEach(lambda button: button.setDisabled( main_media_controls.forEach(lambda button: button.isDisabled()) ) )

		#Play
		#Won't work -- read only property does not inherit Property, seperate API.
		# Bindings.bindBidirectional(history_media_controls.get(0).disabledProperty(), main_media_controls[0].disabledProperty() )
		#Stop
		# Bindings.bindBidirectional(history_media_controls.get(1).disabledProperty(), main_media_controls[1].disabledProperty() )
		#Previous
		# Bindings.bindBidirectional(history_media_controls.get(2).disabledProperty(), main_media_controls[2].disabledProperty() )
		#Next
		# Bindings.bindBidirectional(history_media_controls.get(3).disabledProperty(), main_media_controls[3].disabledProperty() )

		#Shortcut Keys Allowed for History (CTRL + D, CTRL + Q, CTRL + T)
		scene.addEventFilter(KeyEvent.KEY_PRESSED, lambda event: self.handleHistoryShortcuts(event, self.BS, controller.getToggleTheme(), controller.getClearHistory() ) )
	
	
		#Python needs to fix lambdas so we don't have to resort to wrapping inner classes in collections. Yuck.
		class HistoryClosed:
			@staticmethod
			def printClosed():
				print("Log: Quit Action: History just closed.")

		#Switch back to the main stage
		self.stage.setOnCloseRequest(lambda event: [ self.app.getMainStage().toFront(), self.stage.close(), HistoryClosed.printClosed() ] )

		#Log
		print ('Log: History Notification: History data displayed @ ' + str(LocalDateTime.now()))

	def handleHistoryShortcuts(self, keysPressed, *eventArgs):
		'''
			Designate various shortcut key and combo-shortcut key combinations
			[0]BrowserSession, [1]ToggleTheme(CheckMenuItem), [2]CM_CLHIST
		'''

		##Shortcuts come FIRST##
		
		#Grab CTRL + Q
		if ComboShortcutKeys.QUIT.getCombo().match(keysPressed):
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: Quit action triggered by CTRL + Q')
			BrowserSession.closeHistoryWriter(eventArgs[0])
			self.app.closeStages(self.app.getStageList()) #Not a static call...
			Platform.exit()
		#Grab CTRL + T
		elif ComboShortcutKeys.THEME_TOGGLE.getCombo().match(keysPressed):
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: Theme-Switch action triggered by CTRL + T')
			eventArgs[1].fire()
			#Breaks when scene changes.
		#Grab CTRL + D
		elif ComboShortcutKeys.CLEAR_HIST.getCombo().match(keysPressed):
			eventArgs[2].fire()
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: History Cleared triggered by CTRL + D')
		else:
			pass

	def getStage(self):
		return self.stage