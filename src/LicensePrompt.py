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

import json
from array import array

from BrowserSession import BrowserSession

from java.io import File
from java.lang import Thread, String, NullPointerException
from javafx.scene import Scene
from javafx.stage import Modality 
from javafx.event import EventHandler
from javafx.geometry import Pos,Insets
from javafx.scene.web import WebView
from javafx.application import Platform
from javafx.scene.image import Image, ImageView 
from javafx.scene.layout import VBox, HBox, Background, BackgroundSize, BackgroundImage, BackgroundPosition, BackgroundRepeat, BackgroundFill

class LicensePrompt:
	def __init__(self, EmeraldFX, BS, license_stage, main_stage, icons):
		self.app = EmeraldFX
		self.BS = BS
		self.license_check_stage = license_stage
		self.main_stage = main_stage
		self.icons = icons

	def show(self):
		from javafx.scene.control import CheckBox, Button
		
		#Make Stage always on top
		self.license_check_stage.setAlwaysOnTop(True)
		#Set Max Height/Width
		self.license_check_stage.setMaxWidth(900)
		self.license_check_stage.setMaxHeight(500)
		#Disallow resizing
		self.license_check_stage.setResizable(False)
		#Center on screen
		self.license_check_stage.centerOnScreen()
		#Get input focus
		self.license_check_stage.requestFocus()

		#Block Main Stage from recieving events!
		self.license_check_stage.initModality(Modality.APPLICATION_MODAL) #Why is this not in setter bean notation? Hmm.

		#License Check
		self.license_check_stage.setTitle("License Terms & Conditions  -  EmeraldFX")
		#License Answer Placeholder
		license_answer = str()

		#Buttons
		yes = CheckBox()
		no = CheckBox()
		enter = Button()

		#Grab, icon, graphics, button graphics
		try:
			self.license_check_stage.getIcons().addAll(self.icons.get(0), self.icons.get(1), self.icons.get(2), self.icons.get(3), self.icons.get(4))
			license_graphic = ImageView( Image(String(File('../resources/icons/license.png').toURI().toString()), True) ) 
			yes.setGraphic(ImageView( Image(String(File('../resources/icons/YES.png').toURI().toString()), True) ) )
			no.setGraphic(ImageView( Image(String(File('../resources/icons/NO.png').toURI().toString()), True) ) )
			enter.setGraphic(ImageView( Image(String(File('../resources/icons/GO.png').toURI().toString()), True) ) )
		except NullPointerException:
			print("Log: One or more Application resouce files could not be found.")

		#Disallow Indeterminate
		yes.setAllowIndeterminate(False)
		no.setAllowIndeterminate(False)
		
		
		#Header
		if self.app.getCurrentTheme() == "Dark":
			top = ImageView(Image(File('../resources/icons/top_bar_license_dt.png').toURI().toString()))
		elif self.app.getCurrentTheme() == "Light":
			top = ImageView(Image(File('../resources/icons/top_bar_license_lt.png').toURI().toString()))
		
		#Middle
		middle = HBox(15)
		#Set up WebEngine
		license_webView = WebView()
		webEng = license_webView.getEngine()
		webEng.load(self.app._EmeraldFX__LICENSE)
		
		#License Image
		license_logo = VBox()
		license_logo.getChildren().add(ImageView( Image(String(File('../resources/icons/license.png').toURI().toString()), True) ))
		license_logo.setAlignment(Pos.CENTER)

		#Put it all together
		middle.getChildren().addAll(license_logo, license_webView)			
		middle.setPadding(Insets(0, 10, 0, 10))

		#CheckBox Grouping
		bottom = HBox()
		bottom.getChildren().addAll(yes,no,enter)
		bottom.setSpacing(50)
		bottom.setPadding(Insets(0, 0, 0, 200))

		#Set Theme Accordingly
		try:
			if self.app.getCurrentTheme() == "Dark":
				BKG= File('../resources/icons/bottom_bar_dt.png').toURI().toString()
			elif self.app.getCurrentTheme() == "Light":
				BKG= File('../resources/icons/bottom_bar_lt.png').toURI().toString()
			else:
				pass 
		except NullPointerException:
			print("Log: One or more Application resouce files could not be found.")
		
		#Footer
		background_bottom = Background(array(BackgroundImage, [BackgroundImage(Image(BKG), BackgroundRepeat.NO_REPEAT,BackgroundRepeat.NO_REPEAT,BackgroundPosition.DEFAULT, BackgroundSize.DEFAULT)] ))
		bottom.setBackground(background_bottom)
		bottom.setAlignment(Pos.CENTER)
		bottom.setPrefHeight(15)

		#Root Pane
		license_check_stage_root = VBox ()
		license_check_stage_root.getChildren().addAll(top, middle, bottom)
		
		#Scene
		license_check_scene = Scene (license_check_stage_root, 895,498)
		#Shortcuts not available for this scene. We will use defaults, for now.

		#Set Scene on Stage
		self.license_check_stage.setScene(license_check_scene)

		#Handle Selection		
		class AnonInnerCL_E(EventHandler):
			def __init__(self, outer, yes, no):
				self.outer = outer
				self.app = outer.app
				self.BS = outer.BS
				self.YES = yes
				self.NO = no
				self.license_check_stage_json = self.app._EmeraldFX__config
			#@Override
			def handle (self, action):
				if (yes.isSelected()) ^ (no.isSelected()):
					if self.app._EmeraldFX__LICENSE_ACCEPTANCE == "YES":
						#We're done here
						self.outer.license_check_stage.close()
						#Update properties.json
						self.license_check_stage_json['license']['value'] = "YES"
						#Write Data, close stream
						with open("../resources/config/properties.json", "w") as prop:
							json.dump(self.license_check_stage_json, prop)
					else:
						# checked == "NO":
						BrowserSession.closeHistoryWriter(self.BS)
						Thread.sleep(300)
						Platform.exit()
		class AnonInnerCL_Y(EventHandler):
			def __init__(self, YES, NO, ENTER, app):
				self.YES = YES
				self.NO = NO
				self.ENTER = ENTER
				self.app = app
			#@Override
			def handle (self, action):
				if self.YES.isSelected():
					self.NO.setSelected(False)
					self.ENTER.setDisabled(False) if self.ENTER.isDisabled() else None
					self.app._EmeraldFX__LICENSE_ACCEPTANCE = "YES"
				elif not self.YES.isSelected() and not self.NO.isSelected():
					self.ENTER.setDisabled(True)
		class AnonInnerCL_N(EventHandler):
			def __init__(self, NO, YES, ENTER, app):
				self.NO = NO
				self.YES = YES
				self.ENTER = ENTER
				self.app = app
			#@Override
			def handle (self, action):
				if self.NO.isSelected():
					self.YES.setSelected(False)
					self.ENTER.setDisabled(False) if self.ENTER.isDisabled() else None
					self.app._EmeraldFX__LICENSE_ACCEPTANCE = "NO"
				elif not self.NO.isSelected() and not self.YES.isSelected():
					self.ENTER.setDisabled(True)

		#Disable Enter by Default
		enter.setDisabled(True)
		
		#Enter hit
		enter.setOnAction(AnonInnerCL_E (self, yes, no) )
		#Yes Checked
		yes.setOnAction(AnonInnerCL_Y(yes, no, enter, self.app))
		#No Checked
		no.setOnAction(AnonInnerCL_N(no, yes, enter, self.app))

		#If they enter no selection, exit
		self.license_check_stage.setOnCloseRequest(lambda event: [BrowserSession.closeHistoryWriter(self.BS), Platform.exit()])

		#Display stage
		self.license_check_stage.show()

	def getStage(self):
		return self.license_check_stage
