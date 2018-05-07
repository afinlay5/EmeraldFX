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

from java.lang import NullPointerException #java.lang.NullPointerException
from javafx.util import Duration #import javafx.util.Duration
from javafx.scene import Scene #javafx.scene.Scene
from javafx.stage import StageStyle #javafx.stage.StageStyle
from javafx.geometry import Pos #javafx.geometry.Pos;
from javafx.animation import FadeTransition #import javafx.animation.FadeTransition
from javafx.scene.paint import Color #javafx.scene.paint.Color
from javafx.scene.effect import DropShadow, Lighting #javafx.scene.effect.DropShadow, Lighting
from javafx.scene.layout import VBox #javafx.scene.layout.VBox
from javafx.scene.effect.Light import Distant #javafx.scene.effect.Light.Distant



class SplashScreen():
	def __init__(self, browser, stage, splash,icons, CURRENT_TRACK, MUSIC_AUTO_PLAY):
		self.browser = browser
		self.stage = stage
		self.SPLASH_IMAGE_VIEW = splash
		self.ICONS = icons
		self.CURRENT_TRACK = CURRENT_TRACK
		self.MUSIC_AUTO_PLAY = MUSIC_AUTO_PLAY

		#Jython needs this here...
		from javafx.scene.control import ProgressBar #javafx.scene.control.ProgressBar
		self.progress_splash = ProgressBar()

		#Splash Fade
		self.splash_fade = FadeTransition(Duration.seconds(4))
	
	def render(self):		
		
		#Log
		print ("Log: Loading Flash Screen.....")

		#Add Splash to Collection of Stages
		self.browser.addStageToList(self.stage)

		#Consider Future Animation/Visual Effects, ie. Glow, Blur

		#Brighten Effect			
		lighting = Lighting()

		light = Distant()
		light.setAzimuth(-135.0)

		lighting.setLight(light)
		lighting.setSurfaceScale(5.0)
				
		#Splash Stage Configuration
		self.stage.initStyle(StageStyle.UNDECORATED)
		self.stage.setAlwaysOnTop(True)
		self.stage.setResizable(False)
		self.stage.setTitle("Splash - EmeraldFX")
		
		#Splash Screen Root Pane
		SPLASH_ROOTP = VBox()
		SPLASH_SCENE_WIDTH = 633
		SPLASH_SCENE_LENGTH = 240
		SPLASH_ROOTP.setAlignment(Pos.CENTER)

		#Splash Screen's Scene
		SPLASH_SCENE = Scene(SPLASH_ROOTP, SPLASH_SCENE_WIDTH, SPLASH_SCENE_LENGTH)
		SPLASH_SCENE.setFill(Color.BLACK)
		self.stage.setScene(SPLASH_SCENE)
		
		### Splash Screen's UI Elements ###

		#Set Effect on Splash Screen Image View	
		self.SPLASH_IMAGE_VIEW.setEffect(lighting)
		
		#DropShadow
		shadow = DropShadow()
		shadow.setColor(Color.BLACK.saturate())
		SPLASH_ROOTP.setEffect(shadow)
		
		#Fancy progress bar ;)
		self.progress_splash.setPrefWidth(SPLASH_SCENE_WIDTH-10)
				
		#Add UI Elements to Splash's Screen Root Pane
		SPLASH_ROOTP.getChildren().addAll(self.SPLASH_IMAGE_VIEW, self.progress_splash)
		
		#Splash Screen's Icon
		try:
			self.stage.getIcons().addAll(self.ICONS.get(0),self.ICONS.get(1),self.ICONS.get(2),self.ICONS.get(3),self.ICONS.get(4))
		except NullPointerException:
			print("Log: The application's icon file could not be found.")	
		
		#Fade Transition Configuration
		self.splash_fade.setNode(SPLASH_ROOTP)
		self.splash_fade.setFromValue(1.0)
		self.splash_fade.setToValue(0.2)	

		#As soon as the stage pops up, play
		# splash.setOnShown(self.__CURRENT_TRACK.play() if self.__MUSIC_AUTO_PLAY else None)
		self.stage.setOnShown(lambda event: (self.CURRENT_TRACK.setAutoPlay(True) if self.MUSIC_AUTO_PLAY else None) )
	def getProgressSplash(self):
		'''Progress Splash'''
		return self.progress_splash
	def getSplashFade(self):
		'''Splash Fade'''
		return self.splash_fade