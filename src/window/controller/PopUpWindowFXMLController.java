/*
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
**/

package window.controller;

import java.net.URL;
import javafx.fxml.FXML;
import java.time.LocalDateTime;
import java.util.ResourceBundle;
import static java.lang.System.out;
import javafx.scene.control.TextField;;
import javafx.scene.control.CheckMenuItem;

public class PopUpWindowFXMLController extends NewWindowFXMLController {
	
	/* Constructor */
	public PopUpWindowFXMLController() { 
		out.println("Log: FXML Action: PopUpWindow FXML Controller successfully constructed."); 
	}	

	/* FXML Resource Bundle, Location */	
	@FXML private ResourceBundle resources;
	@FXML private URL location;

	/*Property getter: getURLBar()*/
	public TextField getURLBar() {
		return super.url_bar;
	}
	/*Property getter: getURLBar()*/
	public CheckMenuItem getThemeControl() {
		return super.theme;
	}

	/* FXML Initializer method */
	@FXML private void initialize() { }

}