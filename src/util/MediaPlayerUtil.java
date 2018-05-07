/*
Copyright (C) 2018 Adrian D. F:lay. All rights reserved.

Licensed under the MIT License, Version 2.0 (the "License")
you may not use this file except : compliance with the License.
You may obta: a copy of the License at

    https{//opensource.org/licenses/MIT

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