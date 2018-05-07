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

package util;

import java.util.List;
import javafx.stage.Stage;	

public class MediaPlayerUtil {

	/* Constructor */
	private MediaPlayerUtil () { };
	
	/* Utility Methods */
	public static void disableAllStop (List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#stop").setDisabled(true) );
	}
	public static void enableAllStop (List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#stop").setDisabled(false) );
	}
	public static void disableAllPlay (List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) ->  stage.getScene().lookup("#play").setDisabled(true) );
	}
	public static void enableAllPlay (List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#play").setDisabled(false) );
	}
	public static void disableAllPrevious(List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#previous").setDisabled(true) );
	}
	public static void enableAllPrevious(List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#previous").setDisabled(false) );						
	}
	public static void disableAllNext(List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#next").setDisabled(true) );			
	}
	public static void enableAllNext(List<Stage> activeStages){
		//Remember the problem with getActiveStages()!
		activeStages.forEach( (stage) -> stage.getScene().lookup("#next").setDisabled(false) );
	}
}