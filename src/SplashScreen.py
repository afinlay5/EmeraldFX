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