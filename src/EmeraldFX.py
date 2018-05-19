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

#Application Packages - Jython, Python
from MusicPlayer import MusicPlayer
from BrowserSession import BrowserSession
from HistoryDataElement import HistoryDataElement
from util import MediaPlayerUtil
from LicensePrompt import LicensePrompt
from window import History
from SplashScreen import SplashScreen

#Application Packages - Java
import ShortcutKeys #Shortcut Keys
import ComboShortcutKeys #Shortcut Key Combos
import URLBarArrowConstants
# from util import MediaPlayerUtil


#Python Standard Library Pakckages
import json, sys
from ast import literal_eval
from array import array

#Jython Standard Library Packages
# from jarray import array

#Java Standard Library Packages, JavaFX Packages
from java import lang #import java.lang (For Explicit access to java.lang.Exception) (Conflicts with Py2's "Exception")
from java.io import File #java.io.File
from java.net import URL #java.net.URL
from java.time import LocalDateTime #java.time.LocalDateTime
from java.util import UUID, ArrayList #java.util.UUID, java.util.ArrayList
from java.lang import System, Override, NullPointerException #java.lang.Override,System,NullPointerException
from java.lang import Thread, Runnable, String, StringBuilder #java.lang.Thread, java.lang.String, java.lang.StringBuilder
from javafx.fxml import FXMLLoader #javafx.fxml.FXMLLoader
from javafx.fxml import LoadException #javafx.fxml.LoadException
from javafx.util import Duration #import javafx.util.Duration
from javafx.event import EventHandler #javafx.event.EventHandler
from javafx.scene import Scene, ImageCursor #javafx.scene.Scene,ImageCursor
from javafx.stage import Stage #javafx.scene.Stage
from javafx.stage import StageStyle #javafx.stage.StageStyle
from java.nio.file import Files #java.nio.file.Files
from javafx.geometry import Pos, Insets #javafx.geometry.Pos;
from javafx.scene.web import WebView  #javafx.scene.web.WebView
from javafx.scene.paint import Color #javafx.scene.paint.Color
from java.util.function import Predicate, Function, Consumer
from javafx.scene.input import KeyEvent #javafx.scene.input.KeyEvent
from javafx.application import Application #javafx.application.Application
from javafx.beans.value import ChangeListener #javafx.beans.value.ChangeListener
from javafx.scene.input import KeyCode #javafx.scene.input.KeyCode
from javafx.scene.image import Image, ImageView #javafx.scene.image.Image, javafx.scene.image.ImageView
from javafx.application import Platform #javafx.application.Platform
from javafx.scene.input import MouseButton #javafx.scene.input.MouseButton
from javafx.scene.input import Clipboard #javafx.scene.input.Clipboard
from javafx.beans.value import ChangeListener #javafx.beans.value.ChangeListener
from javafx.scene.layout import VBox, HBox #javafx.scene.layout.VBox, HBox
from javafx.scene.control import Alert, ButtonType#javafx.scene.control.ButtonType, #javafx.scene.control.Alert
from javafx.beans.binding import DoubleBinding#import javafx.beans.binding.DoubleBinding
from javafx.beans.property import SimpleDoubleProperty#import javafx.beans.property.SimpleDoubleProperty
from javafx.concurrent.Worker import State #javafx.concurrent.Worker.State
from javafx.scene.control.Alert import AlertType#javafx.scene.control.Alert.AlertType


#Access to Override -- Broken
#from jynx.jannotations import annotation
#Override = annotation.extract(Override)

#Swing/AWT Dependencies
# - from java.awt.MouseInfo
# - from javax.swing.text.html.HTMLDocument, HTMLEditorKit
#The shade of blue we use is - 84B1D1


### --- EmeraldFX --- A JythonFX Web Browser ###
class EmeraldFX (Application):

	#Lifecycle Method #1
#	@Override
	def init (self):
		print ("----------------------------------------------------")
		print ("Log: This is the first lifecycle method -- init().")
		print ("----------------------------------------------------")
		print ("Hello, init().\n")
		
		#GPLv2License
		print("EmeraldFX v.1.0, Copyright (C) 2018 Adrian D. Finlay.")
		print("EmeraldFX comes with ABSOLUTELY NO WARRANTY; for details type.")
		print("This is free software, and you are welcome to redistribute it")
		print("under certain conditions. For all related details, see ~/license.\n")

		try:	
			self.__ERROR_404  = File("../resources/html/ERROR_404.html").toURI().toString()
			self.__NO_CONNECTION_PAGE  = File("../resources/html/NO_CONNECTION.html").toURI().toString()

	    	#Load Configuration Defaults
			with open('../resources/config/properties.json', 'r') as prop:
				self.__config = json.load(prop)	
			
			#Check if the client accepted license already
			self.license_check_stage_json = str(self.__config ['license']['value'])
			if self.license_check_stage_json != "YES":
				self.__LICENSE = File("../license/EMERALDFX_MIT_LICENSE.txt").toURI().toString()

			#Cursors
			self.__HELP_CURSOR = Image( String(File('../resources/icons/help-cursor.png').toURI().toString()), True)
			self.__SELECT_CURSOR = Image( String(File('../resources/icons/select-cursor.png').toURI().toString()), True)
			self.__TEXT_CURSOR = Image( String(File('../resources/icons/text-cursor.png').toURI().toString()), True)
			self.__BUSY_CURSOR = Image( String(File('../resources/icons/busy-cursor.png').toURI().toString()), True)


			#Set Application Default Variables
			self.__CURRENT_URL = str(self.__config['info']['URL'])
			self.__CURRENT_SEARCH_ENGINE = str(self.__config['info']['SEARCH_ENGINE'])
			self.__HOME = str(self.__config['info']['URL'])
			self.__THEME_CHOICE = str(self.__config['style']['theme'])
			self.__IS_SE_QUERY_FLAG = bool()	
			self.__CONNECTION_FLAG = True #Temporary assumption to circumvent getTitleByURL()
			self.__CURRENT_THEME = str(self.__config['style']['theme'])
			self.__CURRENT_TITLE = self.getTitleByURL(self.__CURRENT_URL)
			self.__CONNECTION_FLAG = bool()
			self.__LICENSE_ACCEPTANCE = str()
			
			try:
				self.__HISTORY_ENABLED = literal_eval(self.__config['optionals']['HISTORY_ENABLED'])
				self.__SPLASH_SCREEN_ENABLED = 	literal_eval(self.__config['optionals']['SPLASH_SCREEN_ENABLED'])
				self.__POPUPS_ALLOWED = literal_eval(self.__config['optionals']['POP_UP_BLOCKER'])
				self.__IS_FULL_SCREEN = literal_eval(self.__config['optionals']['FULL_SCREEN_ENABLED'])
				self.__MUSIC_AUTO_PLAY = literal_eval(self.__config['optionals']['MUSIC_AUTO_PLAY'])
			except ValueError:
				print('Log: Initialization Error: Failed to evaluate a property\'s boolean literal. Must be "True" or "False". ')
				sys.exit()

			if self.__SPLASH_SCREEN_ENABLED:
				self.__SPLASH_IMAGE_VIEW = ImageView(Image( String(File('../resources/icons/splash.png').toURI().toString()), True))

			'''
				Unfortunately the implementation of the icon chooser in JavaFX 8 does not always choose the best icon size 
				for the application from the list of available icons. 
				https://stackoverflow.com/questions/29356066/low-quality-icon-in-taskbar-of-a-stage-javafx
			'''
			self.__ICONS = ArrayList()

			#self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-16x12.jpg').toURI().toString())))
			self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-32x24.jpg').toURI().toString())))
			self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-48x36.jpg').toURI().toString())))
			self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-64x48.jpg').toURI().toString())))
			self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-128x96.jpg').toURI().toString())))
			self.__ICONS.add(Image(String(File('../resources/icons/EmeraldFX-256x192.jpg').toURI().toString())))

		except NullPointerException:
			print("Log: The application's icon files could not be found.")

		#Filter bad values
		if self.__CURRENT_THEME != "Light" and self.__CURRENT_THEME != "Dark":
			print("Log: Initialization Error: Failed to evaluate Theme property's value. Must be \"Light\" or \"Dark\". ")
			sys.exit()

		#Collection for holding Stages
		self.__ALL_STAGES = ArrayList()

		#Music Player - WAV, MP3, AAC only - drop files in /root/resources/music
		self.__INIT_NO_MUSIC = MusicPlayer.isFolderEmpty()
		if not self.__INIT_NO_MUSIC:
			self.__MUSIC_PLAYER = MusicPlayer()
			self.__NUM_SONGS = self.__MUSIC_PLAYER.getMediaPlayer().getValue().size()
			self.__MP_IT= self.__MUSIC_PLAYER.getMediaPlayer().getKey()
			self.__CURRENT_TRACK = self.__MP_IT.next()
		else:
			self.__MUSIC_AUTO_PLAY = False
			self.__CURRENT_TRACK = None

		# self.__APPLICATION_CLIPBOARD = Clipboard.getSystemClipboard()

	#Lifecycle Method #2
#	@Override
	def start (self, splash):

		###  Setup Main Stage (The default stage was used for the splash screen) ####
		main = Stage(StageStyle.DECORATED) 

		#Log: Enter start()
		print ("----------------------------------------------------")
		print ("Log: This is the second lifecycle method -- start().")
		print ("----------------------------------------------------")
		print ("Hello, EmeraldFX:\n")

		#Jython needs these here as opposed to up top.
		from javafx.animation import PauseTransition #import javafx.animation.PauseTransition
		from javafx.scene.control import ComboBox #javafx.scene.control.ComboBox
		from javafx.scene.control import Button #javafx.scene.control.Button
		from javafx.scene.control import ProgressBar #javafx.scene.control.ProgressBar
		from javafx.scene.control import MenuItem, CheckMenuItem, MenuButton #javafx.scene.control.MenuItem,MenuButton,CheckMenuItem
		from javafx.scene.control import SeparatorMenuItem #javafx.scene.control.SeparatorMenuItem
		from javafx.scene.control import ContextMenu #javafx.scene.control.ContextMenu
		from javafx.scene.control import ListCell #javafx.scene.control.ListCell
		

		#Load/Skip Splash Screen
		if self.__SPLASH_SCREEN_ENABLED is True:
			ss = SplashScreen(self, splash, self.__SPLASH_IMAGE_VIEW, self.__ICONS, self.__CURRENT_TRACK, self.__MUSIC_AUTO_PLAY)
			ss.render()

		###  Configure Main Stage ####
		
		#Add main to Collection of Stages
		self.addStageToList(main)
		
		#Set Stage Title
		main.setTitle("EmeraldFX")	

		#Pause Transition
		delay = PauseTransition(Duration.seconds(2.5))

		#Supply an icon
		try:
			main.getIcons().addAll(self.__ICONS.get(0),self.__ICONS.get(1),self.__ICONS.get(2),self.__ICONS.get(3),self.__ICONS.get(4))
		except NullPointerException:
			print("Log: The application's icon file could not be found.")
		
		#Root Node
		rootNode = VBox()
		
		#Top Bar
		bar = HBox(5)
		
		#UI Elements
		url_bar = ComboBox()
		home = Button()
		refresh = Button()
		cancel = Button()
		enter = Button()
		forward = Button()
		backward = Button()
		history = Button()
		play = Button()
		media = HBox()
		stop = Button()
		next = Button()
		previous = Button()
		progress = ProgressBar()

		# Insantiate ContextMenuItems, Set Menu Graphics, Labels
		try: 
			CM_REFRESH = MenuItem("Refresh\t \t(F5)", ImageView( Image(String(File('../resources/icons/refresh.png').toURI().toString()), True)))
			CM_HOME = MenuItem("Home\t \t(Ctrl + `)", ImageView( Image(String(File('../resources/icons/home.png').toURI().toString()), True)))
			CM_BACK = MenuItem("Back", ImageView( Image(String(File('../resources/icons/backward.png').toURI().toString()), True)))
			CM_FWD = MenuItem("Forward", ImageView( Image(String(File('../resources/icons/forward.png').toURI().toString()), True)))
			CM_CP = MenuItem("Copy\t\t \t(Ctrl + C)", ImageView( Image(String(File('../resources/icons/copy.png').toURI().toString()), True)))
			CM_CT = MenuItem("Cut\t\t \t(Ctrl + X)", ImageView( Image(String(File('../resources/icons/cut.png').toURI().toString()), True)))
			CM_P = MenuItem("Paste\t \t(Ctrl + V)", ImageView( Image(String(File('../resources/icons/paste.png').toURI().toString()), True)))
			CM_CLHIST = MenuItem("Clear History\t \t(Ctrl + D)", ImageView( Image(String(File('../resources/icons/trash.png').toURI().toString()), True)))
			CM_NEW_WINDOW = MenuItem("Open in New Window", ImageView( Image(String(File('../resources/icons/new_window.png').toURI().toString()), True)))
			CM_QUIT = MenuItem("Quit\t\t \t(Ctrl + Q)", ImageView( Image(String(File('../resources/icons/quit.png').toURI().toString()), True)))
			CM_HIST = MenuItem("History\t \t(Ctrl + H)", ImageView( Image(String(File('../resources/icons/history.png').toURI().toString()), True)))
			CM_PRINT = MenuItem("Print\t\t \t(Ctrl + P)", ImageView( Image(String(File('../resources/icons/print.png').toURI().toString()), True)))
			self.CM_FULL1 = CheckMenuItem("Fullscreen\t(F11)", ImageView( Image(String(File('../resources/icons/full_screen.png').toURI().toString()), True)))
			self.CM_FULL2 = CheckMenuItem("Fullscreen\t (F11)", ImageView( Image(String(File('../resources/icons/full_screen.png').toURI().toString()), True)))
			CM = ContextMenu()
			themeToggle = CheckMenuItem(self.__CURRENT_THEME + " Theme\t (Ctrl + T)", ImageView( Image(String(File('../resources/icons/theme.png').toURI().toString()), True))) 
			quit = MenuItem("Quit\t\t\t (Ctrl + Q)", ImageView( Image(String(File('../resources/icons/quit.png').toURI().toString()), True)))
		except NullPointerException as npe:
			print("Log: Exception: One or more Application resouces could not be found.:\n-----" + str(npe))

		
		#Set UI Element Graphics
		try:
			#Make copies of UI Elements for going between themes
			self.bottom_bar_dt = ImageView( Image(String(File('../resources/icons/bottom_bar_dt.png').toURI().toString()), True))
		
			#Dark Theme CSS
			self.dark_theme = File('../resources/themes/dark_theme.css').toURI().toString()
			
			home.setGraphic( ImageView( Image(String(File('../resources/icons/home.png').toURI().toString()), True)) )
			enter.setGraphic( ImageView( Image(String(File('../resources/icons/enter.png').toURI().toString()), True))  )
			cancel.setGraphic( ImageView( Image(String(File('../resources/icons/cancel.png').toURI().toString()), True)) )
			refresh.setGraphic( ImageView( Image(String(File('../resources/icons/refresh.png').toURI().toString()), True)) )
			forward.setGraphic( ImageView( Image(String(File('../resources/icons/forward.png').toURI().toString()), True)) )
			backward.setGraphic( ImageView( Image(String(File('../resources/icons/backward.png').toURI().toString()), True)) )
			history.setGraphic( ImageView( Image(String(File('../resources/icons/history.png').toURI().toString()), True)) )
			play.setGraphic( ImageView( Image(String(File('../resources/icons/play.png').toURI().toString()), True)) )
			stop.setGraphic( ImageView( Image(String(File('../resources/icons/stop.png').toURI().toString()), True)) )
			next.setGraphic( ImageView( Image(String(File('../resources/icons/next.png').toURI().toString()), True)) )
			previous.setGraphic( ImageView( Image(String(File('../resources/icons/previous.png').toURI().toString()), True)) )
			menubutton = MenuButton("", ImageView(Image(String(File('../resources/icons/HBGR_MENU_ICON.png').toURI().toString()), True)))
			
		except NullPointerException as npe:
			print("Log: Exception: One or more Application resouces could not be found.:\n-----" + str(npe))

		#Set UI Element IDs
		home.setId("home")
		refresh.setId("refresh")
		cancel.setId("cancel")
		enter.setId("enter")
		forward.setId("forward")
		backward.setId("backward")
		history.setId("history")
		bar.setId("bar")
		progress.setId("progress")
		menubutton.setId("menu")
		play.setId("play")
		stop.setId("stop")
		next.setId("next")
		previous.setId("previous")
		themeToggle.setId("themeToggle")
		CM.setId("contextmenu")
		CM_REFRESH.setId("refresh")
		CM_HOME.setId("home")
		CM_HIST.setId("history")
		CM_BACK.setId("back")
		CM_FWD.setId("forward")
		CM_CP.setId("copy")
		CM_CT.setId("cut")
		CM_P.setId("paste")
		CM_CLHIST.setId("clearhistory")
		CM_NEW_WINDOW.setId("newwindow")
		CM_PRINT.setId("print")
		CM_QUIT.setId("quit")
		self.CM_FULL1.setId("fullscreen1")
		self.CM_FULL2.setId("fullscreen1")

		
		#Miscellaneous UI Configuration		
		url_bar.setEditable(True)
		progress.setPrefWidth(210)
		url_bar.setPrefWidth(640) 
		url_bar.setPrefHeight(25)
		bar.setAlignment(Pos.CENTER)

 		menubutton.getItems().addAll( [themeToggle, SeparatorMenuItem(),self.CM_FULL1, SeparatorMenuItem(),CM_CLHIST,SeparatorMenuItem(),quit] )
	 	CM.getItems().addAll(CM_REFRESH, CM_HOME, CM_HIST, SeparatorMenuItem(), CM_BACK, CM_FWD, 
	 		SeparatorMenuItem(), CM_CP, CM_CT, CM_P, SeparatorMenuItem(), CM_NEW_WINDOW,SeparatorMenuItem(), self.CM_FULL2, SeparatorMenuItem(), 
	 		CM_PRINT, SeparatorMenuItem(),CM_QUIT)
	 	CM_NEW_WINDOW.setDisable(True) #Notice it is not setDisable() like other API
	 	media.setSpacing(5)

	 	#Configure FullScreen CheckMenuItem
	 	if self.__IS_FULL_SCREEN is True:
	 		self.CM_FULL1.setSelected(True)
	 		self.CM_FULL2.setSelected(True)

	 	#Application Clipboard (Jython needs this here)
	 	self.__APPLICATION_CLIPBOARD = Clipboard.getSystemClipboard()

		#Set up URL BAR
		media.getChildren().addAll(stop, previous, next)
		bar.getChildren().addAll(home, url_bar, enter, cancel, refresh, backward, forward, history, progress, play, media, menubutton)
		
		#Instantiate WebView, WebEngine
		webView = WebView()
		webEng = webView.getEngine()
		#Get a Load Worker so we can bind to various things: loading progress and track title/url changes of unexpected redirects, etc
		webEngLoadWorker= webEng.getLoadWorker()
		
		#Bind Browser's Progress Bar's progress to WebView's loading
		progress.progressProperty().bind(webEngLoadWorker.workDoneProperty().divide(100))
		#Bind Titles- Webpage -- Application -- Illegal
		# main.titleProperty().bind(webEngLoadWorker.titleProperty().concat(" - EmeraldFX"))

		#Python List of media controls
		self.MEDIA_CONTROLS = ArrayList([play, stop, previous, next])
		
		#Test Connectivity
		if EmeraldFX.testConnection() is False:
			print('Log: ' + "Network Error: " + "You likely do not have an active internet connection." + " @ " + str(LocalDateTime.now()))
			webEng.load(self.__NO_CONNECTION_PAGE) #Load the Error Page for No Connection
		
			#Load Unsuccessful, flip switch
			self.__CONNECTION_FLAG = False

			if self.__SPLASH_SCREEN_ENABLED is True:
				#Indeterminate should be display the bouncing back and forth animation? Broken somehow.
				ss.getProgressSplash().setProgress(1.0)

			#Set Current URL
			self.__CURRENT_URL = self.formatURL(self.__CURRENT_URL, self.__CURRENT_SEARCH_ENGINE)
			#Set Current Title
			self.__CURRENT_TITLE = "No Connection"
		else:
			#Set Current URL
			self.__CURRENT_URL = self.formatURL(self.__CURRENT_URL, self.__CURRENT_SEARCH_ENGINE)	

			if self.__SPLASH_SCREEN_ENABLED is True: 
				#Bind Splash Screen's Progress Bar's progress to WebView's loading
				ss.getProgressSplash().progressProperty().bind(webEngLoadWorker.workDoneProperty().divide(100))

			#Load as normal
			webEng.load(self.__CURRENT_URL)		
		
			#Load Successful, Flip switch
			self.__CONNECTION_FLAG = True
		
		#Set Defaul URL for URL Bar
		url_bar.setValue(self.__CURRENT_URL)
		
		#Load Home Page
		print('Log: ' + "Loading: " + self.__CURRENT_URL + " @ " + str(LocalDateTime.now()))
		
		#Instantiate HistoryDataElement Instance - UUID, URL, Title, LocalDateTime 
		HDE = HistoryDataElement( UUID.randomUUID(), self.__CURRENT_URL, self.__CURRENT_TITLE, LocalDateTime.now() )
		
		#Instantiate BrowserSession Instance
		self.BS = BrowserSession(HDE)
		#Write Default History Entry
		self.BS.writeHistoryToFile(HDE.getDateTime(), HDE.getUUID(), HDE.getURL(), HDE.getTitle())
		
		#Grab Theme
	  	try:
	  		#Light Theme
			if self.__THEME_CHOICE == "Light":
				bottom_bar = ImageView( Image(String(File('../resources/icons/bottom_bar_lt.png').toURI().toString()), True))
			#Dark Theme
			elif self.__THEME_CHOICE == "Dark":
				bottom_bar = ImageView( Image(String(File('../resources/icons/bottom_bar_dt.png').toURI().toString()), True))
			#Future Themes
			else:
				pass
			#Always Selected
			themeToggle.setSelected(True)
		except NullPointerException as npe:
			print("Log: One or more GUI element's icon file(s) is/are missing:\n-----" + str(npe))
		
		#Add the UI Components to the Root Node.
		rootNode.getChildren().addAll(bar,webView, bottom_bar)

		#Main Scene
		self.scene = Scene(rootNode, 1350, 675)
		
		#Set Custom Combo Box Arrow
		self.setCustomURLBarArrow(url_bar, self.scene, URLBarArrowConstants.NOCSS_AND_NO_SHAPE)
		
		#Configure the Dark Theme if we have selected it.
		#Dark Theme
		if self.__THEME_CHOICE == "Dark":
			self.scene.getStylesheets().add(self.dark_theme)

		#Add Tooltip Stylesheet
		self.scene.getStylesheets().add(File("../resources/themes/tooltip.css").toURI().toString())
		#Add Custom Text Cursor StyleSheet
		self.scene.getStylesheets().add(File("../resources/themes/text-cursor.css").toURI().toString())
		
		#Disable Navigational Buttons & Default Context menu
		backward.setDisable(True)
		forward.setDisable(True)
		webView.setContextMenuEnabled(False)

		#We will leave play on, in case a user decides to add files to the folder during program execution
	 	if 	self.__INIT_NO_MUSIC:
	 		media.setDisable(True)
		
 		#Configure Next
 		if not self.__INIT_NO_MUSIC:
 			if not self.__MP_IT.hasNext():
 				next.setDisable(True)

 		#Configure Previous
 		if self.__MUSIC_AUTO_PLAY:
			#Rationale: At this point if auto play isn't on then nothing has played, yet.
			#For future consideration - what if auto play fails?
			previous.setDisable(True)
		#If auto play disabled
		else:
			stop.setDisable(True)
			previous.setDisable(True)

		#Create ArryaList so we can check all as a collection
		nav_buttons = ArrayList()
		nav_buttons.add(backward)
		nav_buttons.add(forward)
		nav_buttons.add(history)
		

		#If the user specified full screen, reflect that.
		if self.__IS_FULL_SCREEN is True:
			main.setFullScreen(True)
			self.CM_FULL1.setSelected(True)
			self.CM_FULL2.setSelected(True)
		
		
		#21 EVENT HANDLERS, 2 ANONYMOUS INNER CLASSES
		#Update SessionHistory when page changes by user clicks
		class AnonInner_CL_LOC(ChangeListener):
			def __init__(self, outerclass, main, url_bar, nav_buttons, searchEngine, webEng, netTestFlag, CM_BACK):
				self.outerclass = outerclass
				self.BS = outerclass.getBS()
				self.main = main
				self.url_bar = url_bar
				self.nav_buttons = nav_buttons
				self.webEng = webEng
				self.searchEngine = searchEngine
				self.netTestFlag = netTestFlag
				self.CM_BACK = CM_BACK
			#@override
			def changed(self, observable, oldURL, newURL):
				if (self.main.getTitle() == "about:blank - EmeraldFX"):
					return
				elif String(self.main.getTitle()).startsWith("HTTP"):
					TITLE = main.getTitle()
				else:
					# if webEng.getTitle() is not None:
					# 		TITLE = webEng.getTitle() #Why does this give the previous title?
					TITLE = self.outerclass.getTitleByURL(newURL)
				self.outerclass.locationChange(url_bar, nav_buttons, self.searchEngine, webEng, newURL, TITLE, self.CM_BACK)
				
				#Enable Back Button
				if nav_buttons.get(0).isDisabled():
					nav_buttons.get(0).setDisable(False)
				#Flip the Connection Switch if connection has gone bad, inefficient!
				if not self.outerclass.testConnection():
					self.netTestFlag = False 

		#Set Cursor to busy while page is loading.
		# class AnonInner_CL_WEB(ChangeListener):
			# def __init__(self,scene, busy):
				# self.scene = scene 
				# self.BUSY_CURSOR = busy
			# def changed(self, observable, oldState, newState):
				# if oldState == State.SCHEDULED:
				# if newState == State.RUNNING:
					# self.scene.setCursor(ImageCursor(self.BUSY_CURSOR))

		#Toggle between themes
		class AnonInner_CL_THEME(EventHandler):
			def __init__(self, outerclass, scene, webView, top_bar, themeToggle, CM_CLHIST, HISTORY, home):
				'''
					"dark_theme.css" taken from James_D on S/O
					https://stackoverflow.com/a/49159612
				'''
				self.mainStage = outerclass.getMainStage()
				self.mainScene = scene
				self.webView = webView
				self.top_bar = bar
				self.bottom_bar_dt = outerclass.bottom_bar_dt
				self.dark_theme = outerclass.dark_theme
				self.outer = outerclass
				self.BS = outerclass.getBS()
				self.themeToggle = themeToggle
				self.CM_CLHIST = CM_CLHIST
				self.HISTORY = HISTORY
				self.home = home

			#@override
			def handle(self, event):
				###Toggle between themes###

				#Switch to Dark
				if self.outer._EmeraldFX__CURRENT_THEME == "Light":
					rootNode = VBox()
					rootNode.getChildren().addAll(self.top_bar, self.webView, self.bottom_bar_dt)
					DarkScene = Scene(rootNode, 1350, 675)
					DarkScene.getStylesheets().add(self.dark_theme)
					DarkScene.addEventFilter(KeyEvent.KEY_PRESSED, lambda event: self.outer.handleShortcutKeys(event, self.webView.getEngine(),
						self.BS, self.themeToggle, self.top_bar, self.webView, self.home, self.CM_CLHIST, self.HISTORY ))
					self.mainStage.setScene(DarkScene)
					self.outer._EmeraldFX__CURRENT_THEME = "Dark"
					self.themeToggle.setText("Dark Theme\t (Ctrl + T)")
					#Nudge GC
					System.gc();
				#Light
				elif self.outer._EmeraldFX__CURRENT_THEME == "Dark":
					bottom_bar_lt = ImageView( Image(String(File('../resources/icons/bottom_bar_lt.png').toURI().toString()), True))
					rootNode = VBox()
					rootNode.getChildren().addAll(self.top_bar, self.webView, bottom_bar_lt)
					scene = Scene(rootNode, 1350, 675)
					scene.addEventFilter(KeyEvent.KEY_PRESSED, lambda event: self.outer.handleShortcutKeys(event, self.webView.getEngine(),
						self.BS, self.themeToggle, self.top_bar, self.webView, self.home, self.CM_CLHIST, self.HISTORY ))
					self.mainStage.setScene(scene)
					self.outer._EmeraldFX__CURRENT_THEME = "Light"
					self.themeToggle.setText("Light Theme\t (Ctrl + T)")
					#Nudge GC
					System.gc();
				else:
					pass
				#Always Selected
				self.themeToggle.setSelected(True)
				print ("Log: Theme Action: Changed to " + self.outer._EmeraldFX__CURRENT_THEME + " theme.")
		

		#Handle Various Shortcut Keys - Start with F5 for Refresh, and CTRL + C for Copy
		self.CURRENT_MODIFIER = str()
		self.scene.addEventFilter(KeyEvent.KEY_PRESSED, lambda event: self.handleShortcutKeys(event, webEng, themeToggle, url_bar, webView, home, CM_CLHIST, history ))

		#Let's set the scene on the Stage!
		main.setScene(self.scene)

		#Restrict Resizing Browser
		#Cannot toggle resizable on Linux :/
		#https://stackoverflow.com/questions/17816682/why-disabling-of-stage-resizable-dont-work-in-javafx
		# main.setResizable(False)
		
		#Ascertain whether or not to grey out play()
		class PlayRunnable(Runnable):
			def __init__(self, play, stop):
				self.play = play
				self.stop = stop
			#@Override
			def run(self):
				self.play.setDisable(True)
				self.stop.setDisable(False)
		
		if self.__CURRENT_TRACK is not None:
			self.__CURRENT_TRACK.setOnPlaying(PlayRunnable(play,stop))
			self.__CURRENT_TRACK.setOnEndOfMedia(self.autoPlayNext(self,play,stop,previous,next))			
		
		webEng.locationProperty().addListener(AnonInner_CL_LOC(self, main,url_bar,nav_buttons,self.__CURRENT_SEARCH_ENGINE, webEng, self.__CONNECTION_FLAG, CM_BACK))

		#Broken, somehow.
		themeToggle.setOnAction( AnonInner_CL_THEME (self, self.scene, webView, bar, themeToggle, CM_CLHIST, history, home))
				
		delay.setOnFinished( lambda event: [splash.close(), main.show(), (self.licensePrompt(self.__ICONS) if self.license_check_stage_json != "YES" else None) ]	)
		home.setOnAction(lambda event: self.goHome(webEng, main, url_bar, nav_buttons, CM_BACK) )
		url_bar.setOnKeyPressed(lambda event: (self.seek(main,webEng, url_bar, nav_buttons, self.__CURRENT_SEARCH_ENGINE, CM_BACK)) if event.getCode() == KeyCode.ENTER else None)
		enter.setOnAction(lambda event: self.seek(main, webEng, url_bar, nav_buttons, self.__CURRENT_SEARCH_ENGINE, CM_BACK) )
		refresh.setOnAction(lambda event: self.handleRefresh(webEng) )
		cancel.setOnAction(lambda event: self.handleCancel(webEng,url_bar) ) #We need this button only visible when atempting to load.
		
		#THESE HAVE BUGS THAT NEED URGENT FIX
		backward.setOnAction(lambda event: self.navigateBackward(main, webEng, backward, url_bar, forward, CM_FWD, CM_BACK) ) # Future consideration - webEngine.executeScript("history.back()")
		forward.setOnAction(lambda event: self.navigateForward(main, webEng, forward, url_bar, backward, CM_BACK, CM_FWD) )
		#THESE HAVE BUGS THAT NEED URGENT FIX
		
		history.setOnAction(lambda event: self.displayHistory()) 
		quit.setOnAction(lambda event: Platform.exit())
		webView.setOnMouseClicked(lambda event: (self.setUpContextMenu(webView, CM, event)) if (event.getButton() == MouseButton.SECONDARY) else CM.hide())
		webView.setOnKeyPressed(lambda event: CM.hide())
		CM_REFRESH.setOnAction(lambda event: self.handleRefresh(webEng) )
		CM_HOME.setOnAction(lambda event: self.goHome(webEng, main, url_bar, nav_buttons, CM_BACK)  )
		CM_BACK.setOnAction(lambda event: self.navigateBackward(main, webEng, backward, url_bar, forward, CM_FWD, CM_BACK))
		CM_FWD.setOnAction(lambda event: self.navigateForward(main, webEng, forward, url_bar, backward, CM_BACK, CM_FWD) )
		CM_CP.setOnAction(lambda event: self.copyText(webView) )
		CM_CT.setOnAction(lambda event: self.cutText(webView))
		CM_CLHIST.setOnAction(lambda event: self.clearHistory())
		CM_QUIT.setOnAction(lambda event: Platform.exit())
		CM_HIST.setOnAction(lambda event: self.displayHistory()) 
		CM_P.setOnAction(lambda event: self.pasteText(webView))
		self.CM_FULL1.setOnAction(lambda event: self.toggleFullScreen())
		self.CM_FULL2.setOnAction(lambda event: self.toggleFullScreen())	
		CM_NEW_WINDOW.setOnAction(lambda event: self.openInNewWindow(webEng) )		

		webEng.setCreatePopupHandler(lambda event: self.handlePopUps(history) )
	
		#This is likely an expensive operation, maybe do this on another thread?

		# webEngLoadWorker.stateProperty().addListener(AnonInner_CL_WEB(self.scene, self.__BUSY_CURSOR))
		# progress.progressProperty().addListener(lambda prog: (self.scene.setCursor(ImageCursor(self.__BUSY_CURSOR))) if prog.getValue() < 1 else None )
		class RUNNABLE_BUSY(Runnable):
			def __init__(self, scene, prog, busy_cursor):
				self.scene = scene
				self.prog = prog
				self.busy_cursor = busy_cursor
			#Override
			def run(self):
				(self.scene.setCursor(ImageCursor(self.busy_cursor))) if self.prog.getValue() < 1 else None
		progress.progressProperty().addListener(lambda prog: Platform.runLater(RUNNABLE_BUSY (self.scene, prog, self.__BUSY_CURSOR) ))

		stop.setOnAction(lambda event: [self.__CURRENT_TRACK.stop(), MediaPlayerUtil.disableAllStop(self.getActiveStages()), MediaPlayerUtil.enableAllPlay(self.getActiveStages()) ] )
		play.setOnAction(lambda event: [self.__CURRENT_TRACK.play(), MediaPlayerUtil.enableAllStop(self.getActiveStages()), MediaPlayerUtil.disableAllPlay(self.getActiveStages())] if not self.__INIT_NO_MUSIC else None)
		next.setOnAction(lambda event: self.setNextTrack(play,stop,previous,next) )
		previous.setOnAction(lambda event: self.setPreviousTrack(play,stop,previous,next) )
		
		#OnMouseMoved Event Handlers for Tooltips
		home.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not home.isDisabled() else None), self.showToolTip(main,home)] )
		enter.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not enter.isDisabled() else None), self.showToolTip(main,enter)] )
		cancel.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not cancel.isDisabled() else None), self.showToolTip(main,cancel)] )
		refresh.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not refresh.isDisabled() else None), self.showToolTip(main,refresh)] )
		backward.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not backward.isDisabled() else None), self.showToolTip(main,backward)] )
		forward.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not forward.isDisabled() else None), self.showToolTip(main,forward)] )
		history.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not history.isDisabled() else None), self.showToolTip(main,history)] )
		progress.setOnMouseEntered(lambda event: self.showToolTip(main,progress) )
		play.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not play.isDisabled() else None), self.showToolTip(main,play)] )
		stop.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not stop.isDisabled() else None), self.showToolTip(main,stop)] )
		previous.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not previous.isDisabled() else None), self.showToolTip(main,previous)] )
		next.setOnMouseEntered(lambda event: [(self.scene.setCursor(ImageCursor(self.__SELECT_CURSOR)) if not menubutton.isDisabled() else None), self.showToolTip(main,next)] )
		menubutton.setOnMouseEntered(lambda event: menubutton.fire() )
		
		ub_arrow = url_bar.lookup(".arrow-button")
		ub_arrow.setOnMouseEntered(lambda event: self.showToolTip(main , ub_arrow)  )

		#Get Main's Title Label Node
		try:
			stage_title = main.getScene().getRoot().lookup("#lblTitle")
			stage_title.setOnMouseEntered(lambda event: self.showToolTip (main, stage_title))
		except Exception as e:
			print("Log: Exception: Could not find Main Title's Label Node")
									
		#Close the history writer when we exit
		main.setOnCloseRequest(lambda event: [BrowserSession.closeHistoryWriter(self.BS), EmeraldFX.closeStages(self.__ALL_STAGES)])

		#As soon as the stage pops up, play
		if self.__SPLASH_SCREEN_ENABLED is False:
			# main.setOnShown(lambda event: (self.__CURRENT_TRACK.play() if self.__MUSIC_AUTO_PLAY else None) if not self.__SPLASH_SCREEN_ENABLED else None )
			main.setOnShown(lambda event: (self.__CURRENT_TRACK.setAutoPlay(True) if self.__MUSIC_AUTO_PLAY else None) if not self.__SPLASH_SCREEN_ENABLED else None )

		if self.__SPLASH_SCREEN_ENABLED is True:
			#Play splash screen's stage
			splash.show()

			#Play splash's fade transition
			ss.getSplashFade().play()

		#Play the delay
		delay.play()		

	#Lifecycle Method #3
#	@Override
	def stop (self):
		print ("\n----------------------------------------------------")
		print ("Log: This is the last lifecycle method -- stop().")
		print ("----------------------------------------------------")
		print ("Goodbye, stop().\n")
		Platform.exit()
		sys.exit() #Sometimes it hangs....

	### Utility Methods ###

	#3/3 WORKING FULLY
	def setNextTrack(self, play, stop, previous, next):
		active_stages = self.getActiveStages()
		if not self.__MUSIC_AUTO_PLAY:
			self.__CURRENT_TRACK.play()
			MediaPlayerUtil.enableAllPrevious(active_stages)
			MediaPlayerUtil.disableAllPlay(active_stages)
			MediaPlayerUtil.enableAllStop(active_stages)
		elif self.__MP_IT.nextIndex() != (self.__NUM_SONGS+1):
			self.__CURRENT_TRACK.stop()	
			self.__CURRENT_TRACK = self.__MP_IT.next()
			self.__CURRENT_TRACK.play()
			MediaPlayerUtil.enableAllPrevious(active_stages)
		else:
			#If we have no next, do nothing but grey out next
			MediaPlayerUtil.disableAllNext(active_stages)
			return False
	def setPreviousTrack(self, play, stop, previous, next):
		active_stages = self.getActiveStages()
		if self.__MP_IT.previousIndex() != -1:
			self.__CURRENT_TRACK.stop()	
			self.__CURRENT_TRACK = self.__MP_IT.previous()
			self.__CURRENT_TRACK.play()
			MediaPlayerUtil.enableAllNext(active_stages) if next.isDisabled() else None
		else:
			#If we have no previous, do nothing but grey out next
			MediaPlayerUtil.disableAllPrevious(active_stages)
			return False
	def autoPlayNext (self, outer, play, stop, previous, next):
		class AutoNext(Runnable):
			def __init__(self,outer,play,stop,previous,next):
				self.outer = outer
				self.play = play
				self.stop = stop
				self.previous = previous
				self.next = next
			#@Override
			def run(self):
				if self.outer.setNextTrack(play,stop,previous,next) is False:
					self.stop.setDisable(True)
					self.play.setDisable(False)
		return AutoNext(outer,play,stop,previous,next)

	#5/5 WORKING FULLY
	def licensePrompt(self, icons):	
		'''Make sure they agree to license and conditions, else, exit.'''

		#Instantiate LicensePrompt
		licensePrompt = LicensePrompt(self, self.getBS(), (Stage()), self.getMainStage(), icons )		

		#Show LicensePrompt
		licensePrompt.show()
		
		#Add license_check_stage to list of Stages
		self.addStageToList(licensePrompt.getStage())
	def addStageToList(self, stage):
		'''Add a stage to master list'''
		self.__ALL_STAGES.add(stage)
	def getMainStage (self):
		'''Grab Main Stage'''
		return self.__ALL_STAGES.get(0)
	def getStageList(self):
		'''Return Master List of All Stages, open or closed'''
		return self.__ALL_STAGES
	def getActiveStages(self):
		activeStages = ArrayList()

		#Consumer class to filter stages
		class FilterInvalid(Consumer):
			def __init__(self, activeStages):
				self.activeStages = activeStages
			#@Override
			def accept (self, stage):
				filter = ("Splash - EmeraldFX", "License Terms & Conditions  -  EmeraldFX")
				(self.activeStages.add(stage)) if ( (stage is not None) and (str(stage.getTitle()) not in filter) and stage.isShowing() ) else False
		self.getStageList().forEach(FilterInvalid(activeStages))

		return activeStages		
	
	#3/4 WORKING FULLY
	def setCurrentTitle (self, title):
		self.__CURRENT_TITLE = str(title)
		#Nudge GC
		System.gc()
	def setCustomURLBarArrow(self, url_bar, scene, URLBarArrowConstant):
		from javafx.scene.paint import Paint
		from javafx.scene.shape import Shape, SVGPath, FillRule

		#Don't configure the ComboBox Arrow by CSS, instead, do it programmatically and change the Regions SVG Shape
		if URLBarArrowConstant == URLBarArrowConstants.NOCSS_AND_SHAPE:
				
			#SVG Object
			previous_url_bar = SVGPath()
			
			#SVG Path
			previous_url_bar.setContent("M244.75,0c-5.5,0-9.9,4.4-9.9,9.9V370l-73.9-73.9c-3.9-3.9-10.1-3.9-14,0s-3.9," +
				"10.1,0,14l90.8,90.8c1.9,1.9,4.5,2.9,7,2.9s5.1-1,7-2.9l90.8-90.8c3.9-3.9,3.9-10.1,0-14s-10.1-3.9-14," +
				"0l-73.9,73.9V9.9C254.65,4.4,250.25,0,244.75,0,M38.75,366.9c-5.5,0-9.9,4.4-9.9,9.9v102.8c0,5.5,4.4,9.9," +
				"9.9,9.9h412c5.5,0,9.9-4.4,9.9-9.9V376.8c0-5.5-4.4-9.9-9.9-9.9s-9.9,4.4-9.9,9.9v92.9H48.65v-92.9C48.65,371.3,44.25,366.9,38.75,366.9z")
			
			#SVG Fill Rule
			previous_url_bar.setFillRule(FillRule.NON_ZERO)
			
			#Set Fill -- Note that the API is limited.. how can we set two values on one SVG? We probably can't.
			previous_url_bar.setFill(Paint.valueOf(Color.web("2C2F33").toString()))
			previous_url_bar.setFill(Paint.valueOf(Color.web("3C92CA").toString()))
			
			#Apply CSS Sheet
			url_bar.applyCss()
			
			#Set Region's Shape
			arrow_region = url_bar.lookup(".arrow").setShape(previous_url_bar)

		#Configure the ComboBox Arrow by CSS and change the Regions SVG Shape
		elif URLBarArrowConstant == URLBarArrowConstants.BYCSS_AND_SHAPE:
			#Apply Stylesheet for URL Bar
			scene.getStylesheets().add(File("../resources/themes/combo-box_arrow_shape.css").toURI().toString())

		#Configure the ComboBox Arrow by CSS but instead, merely hide the arrow by setting the transparency/opacity values and set a background.
		elif URLBarArrowConstant == URLBarArrowConstants.BYCSS_AND_NO_SHAPE:
			#Apply Stylesheet for URL Bar
			scene.getStylesheets().add(File("../resources/themes/combo-box_arrow_no_shape.css").toURI().toString())

		#Don't configure the ComboBox Arrow by CSS, instead, do it programmatically and merely hide the arrow by setting the transparency/opacity values and set a background.
		elif URLBarArrowConstant == URLBarArrowConstants.NOCSS_AND_NO_SHAPE:
	
			from javafx.scene.paint import Paint
			from javafx.scene.layout import CornerRadii
			from javafx.scene.layout import Background, BackgroundSize, BackgroundImage, BackgroundPosition, BackgroundRepeat, BackgroundFill

			#Apply CSS Sheet
			url_bar.applyCss()

			#Grab Arrow(Region), ArrowButton(StackPane) ComboBox properties
			arrow_region = url_bar.lookup(".arrow")
			arrow_button = url_bar.lookup(".arrow-button")

			#Either Set Opacity to 0 or set background color to transparent.
			arrow_region.setOpacity(0.0)
			arrow_region.setBackground( Background( array(BackgroundFill, [BackgroundFill( Paint.valueOf(Color.TRANSPARENT.toString()), CornerRadii.EMPTY, Insets.EMPTY)]) ) )

			#Set a Background Image for the .arrow-button StackPane.
			arrow_button.setBackground(Background( array(BackgroundImage, [BackgroundImage( Image( String(File('../resources/icons/previous_url_bar.png').toURI().toString()), True) , BackgroundRepeat.NO_REPEAT, BackgroundRepeat.NO_REPEAT, BackgroundPosition.CENTER, BackgroundSize.DEFAULT)] ) ) )		
	def toggleFullScreen(self):
		'''Toggle Full Screen Mode'''
		stage = self.getMainStage()
		if self.__IS_FULL_SCREEN == False:
			# stage.setResizable(True)
			#Cannot toggle resizable on Linux :/
			#https://stackoverflow.com/questions/17816682/why-disabling-of-stage-resizable-dont-work-in-javafx
			stage.setFullScreen(True)
			self.__IS_FULL_SCREEN = True
			self.CM_FULL1.setSelected(True)
			self.CM_FULL2.setSelected(True)
			# stage.setResizable(False)
		elif self.__IS_FULL_SCREEN == True:
			# stage.setResizable(True)
			stage.setFullScreen(False)
			self.__IS_FULL_SCREEN = False
			self.CM_FULL1.setSelected(False)
			self.CM_FULL2.setSelected(False)
			# stage.setResizable(False)
		else:
			pass
		print('Log: Action: Fullscreen switch toggled')
		#This is known to break when screen theme is toggled.
	#99% there, we just need to grab the Main Stage's Title (Label)
	def showToolTip(self,stage, node):
		from javafx.scene.text import Font
		from javafx.scene.layout import StackPane
		from javafx.scene.control import Tooltip,ContentDisplay
		from java.awt import MouseInfo #Why does a class like this not exist in JavaFX? I do not want AWT dependencies/ having to rely on MouseEvents!

		#Wait for two seconds to pass.
 		from javafx.animation import Timeline,KeyFrame
 		timeline = Timeline( array(KeyFrame, [KeyFrame(Duration.seconds(1.0), (lambda event: stage.getScene().setCursor(ImageCursor(self.__HELP_CURSOR)) )  , None )] ) )
		
		#Avoid making several tool tips
		if type(node) is not StackPane and node.getTooltip() is not None:
			tt = node.getTooltip()
			#Show
	 		tt.show(stage, (MouseInfo.getPointerInfo().getLocation().getX()+10), (MouseInfo.getPointerInfo().getLocation().getY()+15)  )
	 		#On Showing
 			tt.setOnShowing(lambda event: timeline.play() )
 			#OnMouseExited
 			node.setOnMouseExited(lambda event: tt.hide())
			return
		elif type(node) is StackPane:
			for childnode in node.getChildren():
				if type(childnode) is Tooltip:
					tt = childnode.getTooltip()
					#Show
	 				tt.show(stage, (MouseInfo.getPointerInfo().getLocation().getX()+10), (MouseInfo.getPointerInfo().getLocation().getY()+15)  )
	 				#On Showing
 					tt.setOnShowing(lambda event: timeline.play() )
 					#OnMouseExited
 					node.setOnMouseExited(lambda event: tt.hide())
					return	
		#Fix
		main = False

		#For Main's Title 
		if main:
			nodeText = String(self.getCurrentURL())
		#For Combo Box URl Bar
		elif type(node) is StackPane:
			nodeText = String('Previous pages visited')
		else:
			nodeText = String(node.getId())
		#Very Annoying that static factory java.lang.String methods and Object.toString() gave a <'unicode'> as opposed to an actual String object!
 		tooltip = Tooltip(   String(StringBuilder(nodeText).replace(0, 1, String(String.valueOf(nodeText.charAt(0))).toUpperCase() ))     )
 		tooltip.setGraphic( ImageView(Image( String(File('../resources/icons/info.png').toURI().toString()), True)))
 		
 		#Set ContentDisplay
 		tooltip.setContentDisplay(ContentDisplay.LEFT)
 		#Set GraphicTextGapProperty
 		tooltip.setGraphicTextGap(6.0)
 		#Set Font
 		tooltip.setFont(Font("DejaVu Sans Oblique", 10))

 		#Set AutoFix
 		tooltip.setAutoFix(True)
 		#Set AutoHide
 		tooltip.setAutoHide(True)
 		#Set HideOnEscape
 		tooltip.setHideOnEscape(True)

 		#Set Style
 		tooltip.setStyle('background-color:powderblue')
 		#Set Skin
 		# tooltip.setSkin()

 		#Assign to Node
 		try:
 			node.setTooltip(tooltip)
 		# except NoSuchMethodException as e:
 		except AttributeError:
 			try:
 				Tooltip.install(node, tooltip);	
 			except TypeError:
 				print ('Log: Exception: This is not a valid node.')
		
 		#Show
 		tooltip.show(stage, (MouseInfo.getPointerInfo().getLocation().getX()+10), (MouseInfo.getPointerInfo().getLocation().getY()+15)  )
			
 		#On Showing
 		tooltip.setOnShowing(lambda event: timeline.play() )

 		#OnMouseExited
 		node.setOnMouseExited(lambda event: tooltip.hide())

	# 2/5 WORKING FULLY
	def seek(self, main, eng, url_bar, nav_buttons, searchEngine, CM_BACK):
		'''Seek URL'''

		#Grab BrowserSession instance
		BS = self.getBS()

		#Check if a connection is avilable. If not, leave the subroutine
		if EmeraldFX.testConnection() is False:
			return

		#Enable Backward Button
		nav_buttons.get(0).setDisable(False)
		CM_BACK.setDisable(False)

		#Check to see if we ran into a 404.
		if self.getTitleByURL(self.formatURL(url_bar.getValue(), str(searchEngine))) == "Error[404] - EmeraldFX":
			eng.load(self.__ERROR_404)
			URL = '://ERROR:404/'
			TITLE  = "Error[404] - EmeraldFX"
		elif self.getTitleByURL(self.formatURL(url_bar.getValue(), str(searchEngine))) == "RELOAD":
			eng.reload()
			URL = self.__CURRENT_URL
			TITLE = str(self.getTitleByURL(self.formatURL(url_bar.getValue(), str(searchEngine)))) + " - EmeraldFX"
		else:
			URL = (str(self.formatURL(url_bar.getValue(), str(searchEngine))))
			TITLE = str(self.getTitleByURL(URL)) + " - EmeraldFX"
			#Load Engine
			eng.load(URL)
			print("Log: Success: Loading. . . " + str(URL) + ' @ ' + str(LocalDateTime.now()))
		#Seek
		BS.addVisit( HistoryDataElement( (self.UUIDByIfURLVisited(url_bar.getValue())), 	#(1)UUID
			URL, TITLE, LocalDateTime.now()) )	 	#(2)URL , (3)Title , (4)LocalDateTime
		#Update Title, Current URL
		url_bar.setValue(URL)	
		#Set Main Title
		main.setTitle(TITLE)
		#Set Current Title
		self.setCurrentTitle(TITLE)

		#Set current URL
		self.__CURRENT_URL = URL
	def goHome(self, eng, main, url, nav_buttons, CM_BACK):
		#Check if a connection is avilable. If not, leave the subroutine
		if EmeraldFX.testConnection() is False:
			return

		'''Navigate to home diretory'''
		eng.load(self.__HOME)
		url.setValue(self.__HOME)
		TITLE = ("Home - " + str(self.getTitleByURL(self.__HOME))+ " - EmeraldFX")
		main.setTitle(TITLE)

		#Set current URL
		self.__CURRENT_URL = self.__HOME

		#Set Current Title
		self.setCurrentTitle(TITLE)

		#Enable Backward, History Buttons
		for button in nav_buttons:
			if button.getId() != "forward" and button.isDisabled() == True:
				button.setDisable(False)
		CM_BACK.setDisable(False)

		#Log
		print('Log: Action: Navigated home')

		#Nudge GC
		System.gc()
	
	##Fix Navigation Issues##
	def locationChange(self, url_bar, nav_buttons, searchEngine, webEng, newURL, newTitle, CM_BACK):
		'''Seek URL'''
		#How do we implement - CM_BACK.setDisable(False) if we click a Hyperlink
		#Everytime we hit back or forwards.. this will be called
		# previous = BS.getPreviousSessionHistoryEntry()
		# if previous is not None:
			# previous_URL_visited = previous.getValue().get(0)
				#This belies fundamental assumptions that may be wrong.
				#Can the user not navigate to the page before by clicking on a link in the current page?
				# if previous_URL_visited == newURL
					# return
		# print(self.__CONNECTION_FLAG)

		#Grab BrowserSession instance
		BS = self.getBS()

		#Main
		main = self.getMainStage()


		#Broken -- but suffice for now
		CM_BACK.setDisable(False)

		#Check if a connection is avilable. If not, leave the subroutine
		if EmeraldFX.testConnection() is False: #Not very efficient
			return
		if not self.__CONNECTION_FLAG == True :
			self.__CONNECTION_FLAG = True

		TIME = LocalDateTime.now()

		#Check to see if we ran into a 404.
		if self.getTitleByURL(self.formatURL(newURL, str(searchEngine))) == "Error[404] - EmeraldFX":
			URL = self.__CURRENT_URL
			TITLE  = "Error[404] - EmeraldFX"
			
		else:
			URL = str(newURL)
			if str(newTitle) != 'EmeraldFX':
				TITLE = str(newTitle) + " - EmeraldFX"
			else:
				TITLE = str(newTitle)
			print("Log: Success: Loaded " + str(URL) + ' @ ' + str(TIME))
			print("Log: Success: Navigated to " + TITLE + ' @ ' + str(TIME))

			#Set current URL
			self.__CURRENT_URL = URL

		#Seek - HistoryDataElement( (1)UUID, (2)URL, (3)Title, (4)LocalDateTime )
		BS.addVisit( HistoryDataElement( (self.UUIDByIfURLVisited(str(newURL))), URL, TITLE, TIME) 	)
		#Update Title, Current URL
		url_bar.setValue(URL)	
		
		#Don't set the Current Title for a cancel refresh
		if not self.getMainStage().getTitle() == "about:blank - EmeraldFX":
			#Set Current Title
			self.setCurrentTitle(TITLE)
			
		#Set Main Title
		main.setTitle(TITLE)
	def navigateForward(self, main, eng, forward, url_bar, backward, CM_BACK,CM_FWD):
		'''Navigate Forwards'''

		#Grab BrowserSession instance
		BS = self.getBS()
		
		#Check if a connection is avilable. If not, leave the subroutine
		if EmeraldFX.testConnection() is False:
			#Log
			print('Log: Action: Attempt to navigate forwards unsuccessful.')
			return

		elif BS.hasNext():
			URL = BS.navigateForward()
			TITLE = str(self.getTitleByURL(URL))

			#Load Engine: Discriminate between 404 and non-404
			if TITLE == "Error[404] - EmeraldFX":
				eng.LoadContent(URL)
			else:
				eng.load(URL)

			#Update Title, Current URL
			url_bar.setValue(URL)
			#Set Main Title
			main.setTitle(TITLE + "- EmeraldFX")
			#Set Current URL
			self.__CURRENT_URL = URL
			#Set Current Title
			self.setCurrentTitle(TITLE + "- EmeraldFX")

			#Log
			print('Log: Action: Successfully navigated forwards.')
		else:
			forward.setDisable(True)
			CM_FWD.setDisable(True)

			#Set Up Alert Dialog
			alert = Alert(AlertType.INFORMATION)
			#Set Alert properties
			try:
				alert.setGraphic( ImageView( Image(String(File('../resources/icons/alert.png').toURI().toString()), True) ) )
			except NullPointerException as npe:
				print("The alert icon could not be found.:\n-----" + str(npe))
			alert.setTitle("Navigation Alert")
			alert.setHeaderText("No subsequent page available.")
			#Broken - Error - TypeError: filter(): 1st arg can't be coerced to java.util.function.Predicate
			#How does this not satisfy java.util.function.Predicate.test()? Strange behavior. Jython type conversion issue?

			#Ridiculous that we should have to do this. Nevertheless, here goes.
			class AlertFilterPred(Predicate):
				#@Override
				def test (self, response):
					return respponse == ButtonType.OK
			class AlertConsumerPred(Consumer):
				#@Override
				def accept(self, object):
					object.formatSystem() #Where is formatSystem()?
					#Ref the API -
					#https://docs.oracle.com/javase/9/docs/api/javafx/scene/control/Alert.html

			#Log
			print('Log: Action: Attempt to navigate forwards unsuccessful.')

			#Show and Wait
			alert.showAndWait().filter(AlertFilterPred()).ifPresent(AlertConsumerPred())
	

		#If we go forward, we want to have backward enabled.
		if BS.hasPrevious():
			backward.setDisable(False)			#Navigation, Dialog Issue
			CM_BACK.setDisable(False)
	def navigateBackward(self, main, eng, backward, url_bar, forward, CM_FWD, CM_BACK):
		'''Navigate Backwards'''
		#Log
		print('Log: Action: Attempt to navigate backwards.')

		#Grab BrowserSession instance
		BS = self.getBS()

		#Check if a connection is avilable. If not, leave the subroutine
		if EmeraldFX.testConnection() is False:
			#Log
			print('Log: Action: Attempt to navigate backwards unsuccessful.')
			return

		elif BS.hasPrevious():
			URL = BS.navigateBackward()
			TITLE = str(self.getTitleByURL(URL))

			#Load Engine: Discriminate between 404 and non-404
			if TITLE == "Error[404] - EmeraldFX":
				eng.loadContent(URL)
			else:
				eng.load(URL)

			#Update Title, Current URL
			url_bar.setValue(URL)
			#Set Main Title
			main.setTitle(TITLE + "- EmeraldFX")
			#Set Current URL
			self.__CURRENT_URL = URL
			#Set Current Title
			self.setCurrentTitle(TITLE + "- EmeraldFX")
			#Activate forward
			forward.setDisable(False)
			CM_FWD.setDisable(False)

			#Log
			print('Log: Action: Successfully navigated backwards.')
		else:
			backward.setDisable(True)
			CM_BACK.setDisable(True)

			#Set Up Alert Dialog
			alert = Alert(AlertType.INFORMATION)
			#Set Alert properties
			try:
				alert.setGraphic( ImageView( Image(String(File('../resources/icons/alert.png').toURI().toString()), True) ) )
			except NullPointerException as npe:
				print("The alert icon could not be found.:\n-----" + str(npe))
			alert.setTitle("Navigation Alert")
			alert.setHeaderText("No previous page available.")
			#Broken - Error - TypeError: filter(): 1st arg can't be coerced to java.util.function.Predicate
			#How does this not satisfy java.util.function.Predicate.test()? Strange behavior. Jython type conversion issue?
			
			#Ridiculous that we should have to do this. Nevertheless, here goes.
			class AlertFilterPred(Predicate):
				#@Override
				def test (self, response):
					return respponse == ButtonType.OK
			class AlertConsumerPred(Consumer):
				#@Override
				def accept(self, object):
					object.formatSystem() #Where is formatSystem()?
					#Ref the API -
					#https://docs.oracle.com/javase/9/docs/api/javafx/scene/control/Alert.html

			#Log
			print('Log: Action: Attempt to navigate backwards unsuccessful.')

			#Show and Wait
			alert.showAndWait().filter(AlertFilterPred()).ifPresent(AlertConsumerPred())

		#If we go back, we want to have forward enabled.
		if BS.hasNext():
			CM_FWD.setDisable(False)
			forward.setDisable(False)			#Navigation, Dialog Issue
	##Fix Navigation Issues##

	# 5/7 WORKING FULLY
	def formatURL(self, url, searchEngine):
		'''
		For right now, we are only supporting HTTP/HTTPS.
		We could use Apache Commons' URL Validator or python's validator package.
		Return None if we should throw a 404.
		'''

		#Check if there's no connection
		if not self.__CONNECTION_FLAG:
			return url

		#Rid ourselves of any unicode types, we want java.lang.String
		url = String(url) 

		# Is it a perfect URL already? Save ourselves the work
		badURL = bool()
		if not url.startsWith(":"):
			from java.net import MalformedURLException
			try:
				URL(url).openConnection().connect() #Attempt Connection
			except MalformedURLException:
				#How do we suppress this in Jython?
				print("Log: Exception Ignored: MalformedURLException on ERROR 404 page.")
				badURL = True
			except:
				badURL = True
			
		#URL is already good to go!
		if not badURL:
			print('Log: Success: URL is good to go: \"' + str(url) + '\" @ ' + str(LocalDateTime.now()))
			#Let clients know
			self.__IS_SE_QUERY_FLAG = False
			return str(url)
		elif self.__CURRENT_TITLE == "Error[404] - EmeraldFX":	
			return str(url)
		#Probably not a URL, Forward to Search Engine
		elif not url.contains(".") or type(url.charAt( int((url.indexOf(".")) + 1))) is int :
			'''
				There are known limitations here, such as parsing '#'.
				This should work for most alphanumeric queries, however.
				This is not internationalized well and results may vary
				with characters outside of ISO Basic Latin Alphabet.
				This is one of the known knowns. There are very likely
				several known unknowns and unknown unknowns.

				We are also only accepting two protocol schemes (HTTP,HTTPS).
				Consequently, custom schemes and "ftp://", for E.G., will not be accepted.

				We should be able to interpret queries like "python2.7 docs" as a search query.

				This program is not intended to be exhaustive. 
				This feature may be extended in the future.
			'''

			#Let clients know
			self.__IS_SE_QUERY_FLAG = True

			#Search Engine Query
			full_query = StringBuilder()

			#Search Engine Options
			google = 'https://www.google.com/search?q='
			bing = 'https://www.bing.com/search?q='
			duckduckgo = 'https://duckduckgo.com/?q='

			#Choose a Search Engine
			if searchEngine == "google":
				full_query.append(google)
			elif searchEngine == "bing":
				full_query.append(bing)
			elif searchEngine == "duckduckgo":
				full_query.append(duckduckgo)

			#UTF-8 Suffix
			utf8_suffix = '&ie=utf-8&oe=utf-8'

			#Format Actual Search Query
			query_list = url.split(" ")
			for query in query_list:
					full_query.append(str(query) + '+')
			if String(full_query).endsWith("+"):
				full_query.deleteCharAt(full_query.length()-1)

			#Added UTF-8 Suffix
			full_query.append(utf8_suffix)
			#Finish URL Query Construction, ship as str
			full_query = (str)(full_query)

			#Log Search
			print('Log: Success: Performing '+ searchEngine + ' search @' + str(LocalDateTime.now()))

			return full_query		
		#If they forgot either http:// or .<tld>, OK, else they're outta luck(for now).
		elif url.startsWith('www.') and url.length() >4:
			#Let clients know
			self.__IS_SE_QUERY_FLAG = False

			#Let's assume they have .<tld> first
			try: 
				#Prefer TLS/SSL
				URL('https://' + str(url)).openConnection().connect()
				if url.contains('/'):
					return 'https://' + str(url)
				else:
					return 'https://' + str(url) + '/'
			except:
				#Try http://
				try:
					URL('http://' + str(url)).openConnection().connect()
					print ('Log: [WARNING]: Your connection to this host is unsecure!')
					if url.contains('/'):
						return 'http://' + str(url)
					else:
						return 'http://' + str(url) + '/'
				except:
					pass

			#No .<tld> specified, attempt to provide tld #http(s)://www.url + .com/ | .com only. Too bad!
			try: 
				#Prefer TLS/SSL
				URL('https://' + str(url) + '.com/').openConnection().connect()
				return 'https://' + str(url) + '.com/'
			except:
				#Try http://
				try:
					URL('http://' + str(url) + '.com/').openConnection().connect()
					print ('Log: [WARNING]: Your connection to this host is unsecure!')
					return 'http://' + str(url) +'.com/'
				except:
					print('Log: Error[404]: The Browser could not load the specified URL: \"' + str(url) + '\"')
					return None #Throw A 404
		#Obviously no "www"., we'll supply a .com or an "http://"
		elif url.startsWith('http://') or url.startsWith('https://'):
			#Let clients know
			self.__IS_SE_QUERY_FLAG = False

			#www isn't needed so attempt a load.
			try:
				URL(url).openConnection().connect()
				return str(url)
			except:
				#We'll try to give them a .com, but if you fail, you fail
				try:
					URL(str(url) + ".com/").openConnection().connect()
					return str(url) + ".com/"
				except:
					print('Log: Error[404]: The Browser could not load the specified URL: \"' + str(url) + '\"')
					return None #Throw a 404.		
		#No www, no http://, and no https:// ? They just have  .<tld>
		elif url.contains("."):
			#The most popular TLDs: https://w3techs.com/technologies/overview/top_level_domain/all

			#We will provide http://www. or https://www. by default. If they particularly want the root
			#It is on them to specify that, explicitly. Not for us to guess.

			#Let clients know
			self.__IS_SE_QUERY_FLAG = False

			#We are going to leave it up to the server to determine which subdomain (if any) it will redirect to

			#Go to ROOT domain, not www. - has ROOT directory
			if not url.endsWith('/'): #google.com, for example
				#Prefer TLS first, Attempt connection
				try:
					URL('https://' + str(url)).openConnection().connect()
					return 'https://' + str(url) +'/'
				#No SSL/TLS
				except:
					try:
						URL('http://' + str(url)).openConnection().connect()
						print ('Log: [WARNING]: Your connection to this host is unsecure!')
						return 'http://' + str(url) +'/'
					except:
						print('Log: Error[404]: The Browser could not load the specified URL: \"' + str(url) + '\"')
						return None	
			#Go to ROOT domain, not www. - go to the ROOT directory
			else:
				#Prefer TLS first, Attempt connection
				try:
					URL('https://' + str(url)).openConnection().connect()
					return 'https://' + str(url)
				#No SSL/TLS
				except:
					try:
						URL('http://' + str(url)).openConnection().connect()
						print ('Log: [WARNING]: Your connection to this host is unsecure!')
						return 'http://' + str(url)
					except:
						print('Log: Error[404]: The Browser could not load the specified URL: \"' + str(url) + '\"')
						return None			
		#You're on your own, pal.
		else:
			print('Log: Error[404]: The Browser could not load the specified URL: \"' + str(url) + '\"')
			#Let clients know
			self.__IS_SE_QUERY_FLAG = False
			return None #Throw a 404			
	def getTitleByURL(self, url):
		'''
			The caller must ensure that the supplied URL is formatted correctly.
			We could also use the java library jsoup or the python library beautiful soup.
			We could spawn a thread for this task.
		'''

		#Handle if we have no connection
		if not self.__CONNECTION_FLAG:
			return "No Active Internet Connection "

		#For now, by hand
		from java.io import InputStreamReader, BufferedReader #java.io.InputStreamReader, java.io.BufferedReader
		from java.net import  UnknownHostException, HttpURLConnection, SocketException #java.net.UnknownHostException, HttpURLConnection, SocketException
		from javax.net.ssl import SSLHandshakeException	#javax.net.ssl.SSLHandshakeException
			

		#Handle Existing 404
		if url == '://ERROR:404/':
			return "Error[404] - EmeraldFX"

		#Blank Input
		if url == None:
			return "Error[404] - EmeraldFX"

		#Always prefer SSL/TLS
		if url is not None:
			#URL
			_URL = URL(url)

			if not String(url).startsWith("https://"):
				HTTPS_URL = str((StringBuilder(url)).insert(4, 's'))
				#Attempt to see if there is HTTPS
				try:
					URL(HTTPS_URL).openStream()
					_URL = URL(HTTPS_URL)

				#We should not get a MalformedURLException at this point
				#Throw a 404
				except UnknownHostException:
					return None 
				#HTTPS not supported
				except SSLHandshakeException:
					try:
						URL(str(_URL)).openStream()
						print ('Log: [WARNING]: Your connection to this host is unsecure!')
					except:	
						return None #Throw an Error Message
				#Likely Connection Reset
				except SocketException:
					try:
						URL(str(_URL)).openStream()
						print ('Log: [WARNING]: Your connection to this host is unsecure!')
					except:	
						return None #Throw an Error Message

		#Establish a connection
		CON = _URL.openConnection()

		#Follow server redirects
		CON.setInstanceFollowRedirects(True)
		CON.setFollowRedirects(True)
		#Spoof Chrome 62.0
		CON.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36")
		#Stream
		URL_STREAM = BufferedReader( InputStreamReader( CON.getInputStream() ) )
		
		#Did we still get a 403?
		if CON.getResponseCode() == HttpURLConnection.HTTP_FORBIDDEN:
			print ("Log: Error[403]: The User-Agent spoof likely failed.")
			return "HTTP 403 - EmeraldFX"
		#Running into a 301 or 302 after redirect doesn't mean failure (www.nba.com for example)
		#We will have to return to this
		elif CON.getResponseCode() == HttpURLConnection.HTTP_MOVED_PERM:
			#nba.com will land here, for example, but it is valid.
			return "HTTP 301 - EmeraldFX"
		elif CON.getResponseCode() == HttpURLConnection.HTTP_MOVED_TEMP:
			return "HTTP 301 - EmeraldFX"
		else:
			pass

		#Walk through stream. BufferedReader should have a hasNextLine()!
		flag = bool()
		result = StringBuilder ()
		while flag is False:
			#Grab each line
			# print(type(URL_STREAM.readLine()))
			try:
				line = String(URL_STREAM.readLine())
			except NullPointerException: #This bug needs to be fixed
				print("Log: Exception: (1/1) Attempt to grab Title by URL failed.")
				print("Log: Exception: (2/2) The URL, however, is valid. Refresh for title.")
				return "Refresh for <Title>"
					
			#Title all on one line
			if line.contains("<title") == True and line.contains("</title>") == True:
				result.append(line)
				flag = True #Effectively Breaks
			#Title on multiple lines
			elif line.contains("<title") == True and line.contains("</title>") == False:
				result.append(line) #Grab The First Part
				if String(URL_STREAM.readLine()).contains("</title>") == True:
					result.append(line)
					flag=True

		#Slow, consider future optimization, maybe regex, jsoup
		result = String(result.delete(result.indexOf("</title>"), result.length()).delete(0, (result.indexOf("title>") +6))).replaceAll("\\P{Print}", "-")
		
		#Really do not want AWT/Swing API. If there is a JavaFX solution, I would love to hear it!
		#javafx.scene.web.HTMLEditor is a start

		#Code to convert HTML Characters and remove non-printable Unicode Characters
		#### Inspired by this solution -- https://stackoverflow.com/a/40953015 ###
		from javax.swing.text.html import HTMLDocument, HTMLEditorKit
		from java.io import StringReader
		doc = HTMLDocument()
		HTMLEditorKit().read(StringReader( "<html><body>" + result ), doc, 0 )
		result = str(doc.getText( 1, doc.getLength() )).strip(' \t\r\n')
		#### Inspired by this solution -- https://stackoverflow.com/a/40953015 ###

		return result
	def UUIDByIfURLVisited (self, url):
		#Grab BrowserSession instance
		BS = self.getBS()

		# Have we visited this site before?
		if BS.hasVisited(str(url)):
			return BS.getUUIDbyURL(url)
		#No prior visit to this page	
		else:
			return UUID.randomUUID()	
	def setUpContextMenu(self, webView, CM, event):
		'''Enable Context Menu'''	
		CM.show(webView , event.getScreenX(), event.getScreenY())
	def copyText(self, webView):
		from javafx.scene.input import ClipboardContent #javafx.scene.input.ClipboardContent
		##Taken from https://stackoverflow.com/a/12798438 ##
		selection = String(webView.getEngine().executeScript("window.getSelection().toString()"))
		##Taken from https://stackoverflow.com/a/12798438 ##
		content = ClipboardContent()
		content.putString(selection)
		self.__APPLICATION_CLIPBOARD.setContent(content)
		print ('Log: Action: Text copied to clipboard')
	#Works, just doesn't remove text
	def cutText(self, webView):
		from javafx.scene.input import ClipboardContent #javafx.scene.input.ClipboardContent
		
		webEng = webView.getEngine()
		selection = String(webEng.executeScript("window.getSelection().toString()"))
		#This is broken - despite following the docs. Possibly Browser Incompatability?
		#https://developer.mozilla.org/en-US/docs/Web/API/Selection/deleteFromDocument
		webEng.executeScript("window.getSelection().deleteFromDocument()")
		
		content = ClipboardContent()
		content.putString(selection)
		self.__APPLICATION_CLIPBOARD.setContent(content)
		print ('Log: Action: Text cut and copied to clipboard')		
	#Not Working
	def pasteText(self, webView):
		# from javafx.scene.input import ClipboardContent #javafx.scene.input.ClipboardContent
		#Get copied content
		# clipboard_content = ClipboardContent().getString()
		#Paste
		webView.getEngine().executeScript("document.execCommand('Paste')")
		print ('Log: Action: Text pasted from clipboard')

	#3/5 WORKING FULLY
	def handleCancel(self, webEng, url_bar):
		self.getMainStage().setTitle("about:blank - EmeraldFX")
		webEng.load("about:blank")
		url_bar.setValue("about:blank")
	def handleRefresh(self, webEng):

		#Grab BrowserSession instance
		BS = self.getBS()
		
		#Grab MainStage
		mainStage = self.getMainStage()

		#If we are a 404, do nothing, really.
		if mainStage.getTitle() == "Error[404] - EmeraldFX":
			webEng.reload()

		#Check if a connection pops up proced. If not, leave the subroutine
		if EmeraldFX.testConnection() is False:
			return
		
		#Reload site
		webEng.load( self.formatURL(self.__CURRENT_URL, self.__CURRENT_SEARCH_ENGINE))

		if mainStage.getTitle() == "about:blank - EmeraldFX":
			mainStage.setTitle(self.__CURRENT_TITLE)

		#Update Title when page refreshes
		class AnonInner_CL_T(ChangeListener):
			def __init__(self, mainStage, BS):
				pass
			#@override
			def changed(self, observable, oldTitle, newTitle):
				if newTitle != None:
					mainStage.setTitle(str(newTitle.encode("utf-8")) + " - EmeraldFX")				
				#newTitle == None
				else: #This might be an issue related to JavaFX. More likely than a site with a Null title.
					mainStage.setTitle("Refresh for <Title> - EmeraldFX")
		#Update WriteHistory only once, for final title
		class AnonInner_CL_S(ChangeListener):
			def __init__(self,mainStage, BS):
				self.mainStage = mainStage
				self.BS = BS
			#@override
			def changed(self, observable, oldState, newState):
				if (newState == State.SUCCEEDED):
					if not self.BS.isHistoryCleared():
						#Write refresh instances to history file but not to other history collections.
						self.BS.writeHistoryToFile(LocalDateTime.now(), self.BS.getCurrentUUID(), self.BS.getCurrentURL(), "REFRESH OF ^ " + self.mainStage.getTitle())	
					else:
						HDE = HistoryDataElement(UUID.randomUUID(),str(self.__CURRENT_URL), str(self.getTitleByURL(self.__CURRENT_URL)), LocalDateTime.now())
						self.BS.writeHistoryToFile(HDE.getDateTime(), HDE.getUUID(), HDE.getURL(), "REFRESH OF ^ " + HDE.getTitle())	

		webEng.titleProperty().addListener(AnonInner_CL_T(mainStage, BS))
		webEng.getLoadWorker().stateProperty().addListener(AnonInner_CL_S(mainStage, BS))

		#Log
		print('Log: Action: Refresh action:  ' + self.__CURRENT_URL)

		#Nudge GC
		System.gc()
	def handleShortcutKeys(self, keysPressed, *eventArgs):
		'''
			Designate various shortcut key and combo-shortcut key combinations
			[0]WebEngine, [1]ToggleTheme(CheckMenuItem), [2] URL Bar,
			[3]WebView, [4]Home Button, [5]CM_CLHIST , [6]History Button, [7]...
		'''

		##Shortcuts come FIRST##
		#Grab CTRL + C
		if ComboShortcutKeys.COPY.getCombo().match(keysPressed):
			keysPressed.consume()
			self.copyText(eventArgs[3])
			print ('Log: Shortcut Combo-Key Action: Copy action triggered by CTRL + C')
		#Grab CTRL + X
		if ComboShortcutKeys.CUT.getCombo().match(keysPressed):
			keysPressed.consume()
			self.cutText(eventArgs[3])
			print ('Log: Shortcut Combo-Key Action: Cut action triggered by CTRL + X')
		#Grab CTRL + V
		if ComboShortcutKeys.PASTE.getCombo().match(keysPressed):
			keysPressed.consume()
			self.pasteText(eventArgs[3])
			print ('Log: Shortcut Combo-Key Action: Paste action triggered by CTRL + V')
		#Grab CTRL + Q
		elif ComboShortcutKeys.QUIT.getCombo().match(keysPressed):
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: Quit action triggered by CTRL + Q')
			BrowserSession.closeHistoryWriter(self.getBS())
			EmeraldFX.closeStages(self.getStageList())
			Platform.exit()
		#Grab CTRL + T
		elif ComboShortcutKeys.THEME_TOGGLE.getCombo().match(keysPressed):
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: Theme-Switch action triggered by CTRL + T')
			eventArgs[1].fire()
			#Breaks when scene changes.
		#Grab CTRL + `
		elif ComboShortcutKeys.HOME.getCombo().match(keysPressed):
			eventArgs[4].fire()
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: Home navigation triggered by CTRL + `')
		#Grab CTRL + D
		elif ComboShortcutKeys.CLEAR_HIST.getCombo().match(keysPressed):
			eventArgs[5].fire()
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: History Cleared triggered by CTRL + D')
		
		#CTRL + M will seek on a page.

		#CTRL + H show history 
		elif ComboShortcutKeys.HISTORY.getCombo().match(keysPressed):
			eventArgs[6].fire()
			keysPressed.consume()
			print ('Log: Shortcut Combo-Key Action: History display triggered by CTRL + H')

		#CTRL + N new window

		#Handle F5 Pressed
		elif ShortcutKeys.REFRESH.getCode() == keysPressed.getCode():
			self.handleRefresh(eventArgs[0])
			print ('Log: Shortcut Key Action: Refresh triggered by F5.')
		#Handle ESC Pressed
		elif ShortcutKeys.CANCEL_LOAD.getCode() == keysPressed.getCode():
			self.handleCancel(eventArgs[0], eventArgs[2])
			print ('Log: Shortcut Key Action: Cancel load triggered by ESC.')
		#Handle F11 Pressed
		elif ShortcutKeys.FULL_SCREEN.getCode() == keysPressed.getCode():
			self.toggleFullScreen()
			print ('Log: Shortcut Key Action: FullScreen toggle triggered by F11.')
		
		#Unregistered Combinations
		elif keysPressed.isAltDown() or keysPressed.isControlDown() or  keysPressed.isMetaDown() or keysPressed.isShiftDown() or keysPressed.isShortcutDown():
			if str(keysPressed.getCode()) in ('ALT','ALT_GRAPH','CONTROL', 'SHIFT', 'META'):
				self.CURRENT_MODIFIER = str(keysPressed.getCode())
			elif keysPressed.getCode() != self.CURRENT_MODIFIER and str(keysPressed.getCode()) not in ('ALT','ALT_GRAPH','CONTROL', 'SHIFT', 'META'):
				print("Log: Shortcut Key Action: Unregistered key combination: " + self.CURRENT_MODIFIER + " + " + str(keysPressed.getCode()) )
		else:
			pass #We do not want to consume these. URL_BAR could need them.		

	##Fix Implementation##
	def handlePopUps(self, HISTORY):	
		'''
			From the API Docs: 
				To satisfy this request a handler may create a new WebEngine, 
				attach a visibility handler and optionally a resize handler, 
				and return the newly created engine. To block the popup, a handler should return null.
			S/N: History not going to be logged in this release for new windows, pop ups.
			To test popups - http://www.popuptest.com/popuptest4.html
		'''
		#Grab BrowserSession instance
		BS = self.getBS()

		#PopupStage
		popup_stage = Stage ()
		#Add new Popup Stage
		self.addStageToList(popup_stage)


		#Demonstrate Declarative/Injected UI - FXML
		fxmlLoader = FXMLLoader()
		if self.__CURRENT_THEME is "Light":
			fxmlLoader.setLocation(File("../resources/fxml/popup_window_light.fxml").toURI().toURL())
		elif self.__CURRENT_THEME is "Dark":
			fxmlLoader.setLocation(File("../resources/fxml/popup_window_dark.fxml").toURI().toURL())

		#Set up the Vbox( HBox(Home - URL Bar - Enter - Refresh - Backward - Forwards - History - Progress Bar - Menu), WebView)
		try:
			main = fxmlLoader.load()
		except LoadException as le:
			print("Log: Load Exception: " + str(le.getCause()) )
			return

		#Construct Controller
		# init_controller = NewWindowFXMLController()
		#Set Controller
		# fxmlLoader.setController(init_controller)
		#GetController instance
		controller = fxmlLoader.getController()

		#Popup Stage
		popup_stage.getIcons().addAll(self.__ICONS.get(0),self.__ICONS.get(1),self.__ICONS.get(2),self.__ICONS.get(3),self.__ICONS.get(4))
		popup_view = WebView()
		popup_engine = popup_view.getEngine()

		#Grab from http:// to .<tld>/
		SB_URL = StringBuilder(self.__CURRENT_URL)

		# url_chars = array ('c', _url.length())
		# _url.getChars(0, _url.length(), url_chars, 0)
		#Let's remove everything past the third "/"
		# for x in url_chars:

		#Previous solution no longer needed. Let's do substring ( 0, indexOf(str, fromIndex) after 8+1 instead.
		URL = str(SB_URL.substring( 0 , (SB_URL.indexOf("/", 8) +1) ) )

		#Set Title
		if popup_engine.getTitle() == None:
			popup_stage.setTitle("PopUp from \""+ URL + "\" - EmeraldFX")
		else:
			popup_stage.setTitle(str(popup_engine.getTitle()) + " - EmeraldFX")

		#Set Scene, show Stage
		scene = Scene(main)
		scene.addEventFilter(KeyEvent.KEY_PRESSED, lambda event: self.handleShortcutKeys(event, pop_engine(),
						controller.getThemeControl(), controller.getURLBar(), popup_view, HISTORY ))
		popup_stage.setScene(scene)#popup_view))
		popup_stage.show()

		#Return Web Engine for popups, or Null for blocking
		if self.__POPUPS_ALLOWED is True:
			return popup_engine
		else:
			return 					#FixAll
	def openInNewWindow(self, webEng): 
		
		#Demonstrate Declarative/Injected UI - FXML
		fxmlLoader = FXMLLoader()
		fxmlLoader.setLocation(File("../resources/fxml/new_window.fxml").toURI().toURL())		
	##Fix Implementation##

	#2/2 WORKING FULLY
	def displayHistory(self):
		'''Display History'''

		#Instantiate History Stage
		history = EmeraldFX_History(self, Stage(), self.getBS())

		#Show History
		history.show()
		
		#Add History Stage to list of Stages
		self.addStageToList(history.getStage())

		# print(Thread.activeCount())

		#Nudge GC
		System.gc()
	def clearHistory(self):

		#Grab BrowserSession instance
		BS = self.getBS()	

		#Set Up Alert Dialog
		alert = Alert(AlertType.INFORMATION)
		#Set Alert properties
		try:
			alert.setGraphic( ImageView( Image(String(File('../resources/icons/alert.png').toURI().toString()), True) ) )
		except NullPointerException as npe:
			print("The alert icon could not be found.:\n-----" + str(npe))
		alert.setTitle("History Alert - EmeraldFX")

		if BS.isHistoryCleared() == True:
			alert.setHeaderText("There is no history.")
			#Broken - Error - TypeError: filter(): 1st arg can't be coerced to java.util.function.Predicate
			#How does this not satisfy java.util.function.Predicate.test()? Strange behavior. Jython type conversion issue?
			
			#Ridiculous that we should have to do this. Nevertheless, here goes.
			class AlertFilterPred(Predicate):
				#@Override
				def test (self, response):
					return respponse == ButtonType.OK
			class AlertConsumerPred(Consumer):
				#@Override
				def accept(self, object):
					object.formatSystem() #Where is formatSystem()?
					#Ref the API -
					#https://docs.oracle.com/javase/9/docs/api/javafx/scene/control/Alert.html

			#Show and Wait
			alert.showAndWait().filter(AlterFilterPred()).ifPresent(AlertConsumerPred())
			return

		else:
			alert.setHeaderText("History is now cleared.")
			#Broken - Error - TypeError: filter(): 1st arg can't be coerced to java.util.function.Predicate
			#How does this not satisfy java.util.function.Predicate.test()? Strange behavior. Jython type conversion issue?
			
			#Ridiculous that we should have to do this. Nevertheless, here goes.
			class AlertFilterPred(Predicate):
				#@Override
				def test (self, response):
					return response == ButtonType.OK
			class AlertConsumerPred(Consumer):
				#@Override
				def accept(self, object):
					object.formatSystem() #Where is formatSystem()?
					#Ref the API -
					#https://docs.oracle.com/javase/9/docs/api/javafx/scene/control/Alert.html

			#Show and Wait
			alert.showAndWait().filter(AlertFilterPred()).ifPresent(AlertConsumerPred())

		'''Wipe history'''
		BS.clearHistory()

		#Nudge GC
		System.gc()

	#4/4 WORKING FULLY
	def getBS(self):
		'''Get Browser Session Instance'''
		return self.BS
	def getMediaControls(self):
		'''
			Property Getters for Media Controls
			Play - Stop - Forwards - Backwards
		'''
		return self.MEDIA_CONTROLS
	def getAllStages(self):
		'''Get all Stages'''
		return self.__ALL_STAGES
	def getCurrentTheme(self):
		'''Property Getter for Current Theme'''
		return self.__CURRENT_THEME
	
	#2/2 WORKING FULLY
	@staticmethod
	def testConnection():
		#Check if a connection is avilable. If not, leave the subroutine
		#For future reference, we want to spend no more than 3 seconds in here. See Duration()
		from java.net import UnknownHostException, SocketException #java.net.SocketException,java.net.UnknownHostException
		try:
			URL("http://www.google.com/").openConnection().connect()
		except SocketException as se:
			print("Log: Socket Exception " + str(se) + " @ " + str(LocalDateTime.now()) )
			return False
		except UnknownHostException as uhe:
			print("Log: Unknown Host Exception " + str(uhe) + " @ " + str(LocalDateTime.now()))
			return False
		return True
	@staticmethod
	def closeStages(stages):
		for stage in stages:
			#Note - this is fundamentally not what we want.
			#API lacks facilities for what we need.

			'''
				From the API -
					The Stage might be "showing", yet the user might 
					not be able to see it due to the Stage being rendered 
					behind another window or due to the Stage being positioned off the monitor
			'''
			if stage.getTitle() is not None:
				print ("Log: Quit Action: " + str(stage.getTitle()) + " just closed.")
			stage.close()

# Launch
if __name__ == "__main__":
    Application.launch(EmeraldFX().class, [])


#Fix Autoplay issue, Fix Theme switch issue
#Printer, Text cursor
#Implement a simple dialog for the user to change the application properties.
#Write Restart Script in actual python.
#Close Stage(Window) - Ctrl + W
#Add support for downloading, starting with "save link as".
#Add shebang to all jython files #! /usr/bin/env jython
#https://docs.oracle.com/javase/8/javafx/api/javafx/scene/control/TextInputControl.html#cut--