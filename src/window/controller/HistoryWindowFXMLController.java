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
import java.io.File;
import java.util.List;
import javafx.fxml.FXML;
import javafx.stage.Stage;
import javafx.scene.Scene;
import java.util.ArrayList;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.time.LocalDateTime;
import javafx.scene.image.Image;
import java.util.ResourceBundle;
import static java.lang.System.out;
import javafx.scene.control.Button;
import javafx.application.Platform;
import javafx.scene.image.ImageView;
import javafx.scene.control.MenuItem;
import javafx.scene.control.TextArea;
import javafx.scene.control.ComboBox;
import javafx.scene.control.MenuButton;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.CheckMenuItem;

public class HistoryWindowFXMLController {
	/*This class demonstrates the use of var with Java 10!*/

	/*EmeraldFX.py Resources*/
	//Quit
	private List<Stage> quit_ls; 
	private PrintWriter quit_pw;
	//Theme
	private Stage mainStage;
	private Stage histStage;
	private Scene scene;
	private static  String current_theme; 
	private TextArea textArea;
	private ImageView bottom_bar_dt;
	private ImageView bottom_bar_lt;
	private String dark_theme;
	//History
	private boolean isHistoryCleared;
	//Media Controls
	private List <Button> mediaControls;
	private List <Button> main_media_controls;


	/* Constructor */
	public HistoryWindowFXMLController() { 
		out.println("Log: FXML Action: HistoryTab FXML Controller successfully constructed."); 
	}


	/* FXML Resource Bundle, Location */	
	@FXML private ResourceBundle resources; //Do I misunderstand the purpose of this? We'll see later on.
	@FXML private URL location;

	/* FXML UI Elements: Variable name must match the corresponding fx:id for injection to be successful. */
	@FXML private Button home; 
	@FXML private ComboBox url;
	@FXML private Button enter;
	@FXML private Button cancel;
	@FXML private Button refresh;
	@FXML private Button backward;
	@FXML private Button forward;
	@FXML private Button history;
	@FXML private ProgressBar progress;
	@FXML private Button play;
	@FXML private Button stop;
	@FXML private Button previous;
	@FXML private Button next;
	@FXML private MenuButton menu;
	@FXML private CheckMenuItem toggleTheme;
	@FXML private MenuItem clearHistory;
	@FXML private MenuItem quit;


	/* Called for theme.onAction()  - Some bugs remain*/
	@FXML private void toggleTheme() {

		/*Switching Themes is broken: NullPointerException*/

		//Always Selected
		toggleTheme.setSelected(true);
		
		//Light Theme
		if (HistoryWindowFXMLController.current_theme.equals("Dark")) {

			//Set Current Theme
			toggleTheme.setText(HistoryWindowFXMLController.current_theme + " Theme\t  (Ctrl + T)");

			//Flip Switch
			HistoryWindowFXMLController.current_theme = "Light";

			//Set up Root Node for Light Scene
			var rootNode = new javafx.scene.layout.VBox();
			
			//Set up top bar
			var fxmlLoader = new javafx.fxml.FXMLLoader();
			javafx.scene.layout.HBox top_bar = null;
			try {
				fxmlLoader.setLocation(new File("../resources/fxml/history_url_tab_light.fxml").toURI().toURL());
				top_bar = fxmlLoader.load();
			}
			catch (java.net.MalformedURLException|javafx.fxml.LoadException fe){
				if (fe instanceof java.net.MalformedURLException) {
					out.println("Log: Exception: MalformedURL, no such FXML file exists.\n" + fe);
				}
				else
					out.println("Log: Exception: FXML Load Exception occured, FXML likely needs linting.\n" + fe.getCause());
			}
			catch (java.io.IOException ioe) {
				out.println("Log: Exception: FXML Loading Failed." + ioe);
			}
			finally {
				if (top_bar == null) { Platform.exit(); System.exit(0); }
			}

			//Add elements to Root Node
			rootNode.getChildren().addAll(top_bar, textArea, bottom_bar_lt);
			
			//Configure Light Scene
			var scene = new Scene(rootNode, 1350, 625);

			//Position History Stage
			histStage.setX(mainStage.getX());
			histStage.setY(mainStage.getX()+67);
			
			//Set new Stage
			histStage.setScene(scene);
			
			//Log
			out.println("Log: Theme Action: Changed to " + HistoryWindowFXMLController.current_theme + " theme.");
		}
		//Dark Theme
		else if (HistoryWindowFXMLController.current_theme.equals("Light")) {

			//Set Current Theme
			toggleTheme.setText(HistoryWindowFXMLController.current_theme + " Theme\t  (Ctrl + T)");

			//Flip Switch
			HistoryWindowFXMLController.current_theme = "Dark";
			
			//Set up Root Node for Dark Sene
			var rootNode = new javafx.scene.layout.VBox();
			
			//Set up top bar
			var fxmlLoader = new javafx.fxml.FXMLLoader();
			javafx.scene.layout.HBox top_bar = null;
			try {
				fxmlLoader.setLocation(new File("../resources/fxml/history_url_tab_dark.fxml").toURI().toURL());
				top_bar = fxmlLoader.load();
			}
			catch (java.net.MalformedURLException|javafx.fxml.LoadException fe){
				if (fe instanceof java.net.MalformedURLException) {
					out.println("Log: Exception: MalformedURL, no such FXML file exists.\n" + fe);
				}
				else
					out.println("Log: Exception: FXML Load Exception occured, FXML likely needs linting.\n" + fe);
			}
			catch (java.io.IOException ioe) {
				out.println("Log: Exception: FXML Loading Failed.\n" + ioe);
			}
			finally {
				if (top_bar == null) { Platform.exit(); System.exit(0); }
			}
			//Add Elements to Root Node
			rootNode.getChildren().addAll(top_bar, textArea, bottom_bar_dt);

			//Configure Dark Scene
			var dark_scene = new Scene(rootNode, 1350, 625);
			dark_scene.getStylesheets().add(dark_theme);

			//Position History Stage
			histStage.setX(mainStage.getX());
			histStage.setY(mainStage.getX()+67);

			//Set new Stage
			histStage.setScene (dark_scene);

			//Log
			out.println("Log: Theme Action: Changed to " + current_theme + " theme.");
		}
		//For later themes
		else {

		}
	}
	/* Called for history.onAction() - Some bugs remain */
	@FXML private void clearHistory() {
		//Set Up Alert Dialog
		var alert = new javafx.scene.control.Alert(javafx.scene.control.Alert.AlertType.INFORMATION);
		//Set Alert properties
		try{
			alert.setGraphic( new ImageView( new Image( new File("../resources/icons/alert.png").toURI().toString(), true) ) );
		}
		catch(NullPointerException npe) {
			out.println("Log: Exception: The alert icon could not be found.:\n-----" + npe);
		}
		alert.setTitle("History Alert - EmeraldFX");

		//If History is already cleared.
		if (isHistoryCleared == true) {
			//Alert
			alert.setHeaderText("There is no history.");
			// alert.showAndWait().filter(response -> response == javafx.scene.control.ButtonType.OK).ifPresent(response -> formatSystem());
			return;
		}
		// clear History.
		else {

			/*IMPORTANT: This is fundamentally broken because we don't know how to interface with EmeraldFX.py elegantly*/

			//Wipe history
			// BS.clearHistory()

			//Log
			out.println("Log: BrowserSession History successfully reset @ " + LocalDateTime.now() );
			out.println("Log: BrowserSession(Default Page Info):  T:\"" + "None"+ "\" , U:\""+ "None" + "\"");

			//Delete Files
			if (new File("../resources/history/HISTORY.csv").exists()) {
				new File("../resources/history/HISTORY.csv").delete();
			}
			if (new File("../resources/history/HISTORY.txt").exists()) {
				new File("../resources/history/HISTORY.txt").delete(); 
			}
			
			//Log
			out.println("Log: BrowserSession History File successfully deleted @ " +  LocalDateTime.now() + '\n');

			//Alert
			alert.setHeaderText("History is now cleared.");
			// alert.showAndWait().filter(response -> response == javafx.scene.control.ButtonType.OK).ifPresent(response -> formatSystem());

			//Set Flag - Note that BrowserSession.py does not know that this is flipped. This is fundamentally broken.
			this.isHistoryCleared = true;
		}

		//Nudge GC
		System.gc();
	}
	/* Called for quit.onAction() */
	@FXML private void quit() {	

		/*Close History Writer Stream **/
		quit_pw.print("BROWSER CLOSED @ " + LocalDateTime.now());
		quit_pw.close();
		out.println("Log: History: History Writer successfully closed @ " +  LocalDateTime.now());

		/*Close all Stages*/
		for (javafx.stage.Stage stage : quit_ls) {
			if (stage.isShowing()) {	//See notes in EmeraldFX.closeStages() about how this is fundamentally broken for our needs.
				stage.close();
				out.println("Log: Quit Action: " + stage.getTitle() + " just closed.");
			}
		}

		/*Close Application*/
		out.println ("\n----------------------------------------------------");
		out.println("Log: Action Event: Application quit.");	
		out.println ("----------------------------------------------------");
		out.println ("Goodbye, closed from History tab.\n");
		
		Platform.exit(); 
		System.exit(0); //Somtimes Platform.exit() hangs in Jython
	}
	/* Called for play.onAction() */
	@FXML private void handlePlay() {
		main_media_controls.get(0).fire();
	}
	/* Called for stop.onAction() */
	@FXML private void handleStop() {
		main_media_controls.get(1).fire();
	}
	/* Called for previous.onAction() */
	@FXML private void handlePrevious() {
		main_media_controls.get(2).fire();
	}
	/* Called for next.onAction() */
	@FXML private void handleNext() {
		main_media_controls.get(3).fire();
	}


	/*Add Quit Resources*/
	public void addQuitResources(ArrayList <Stage> quit_ls, PrintWriter quit_pw) {
		this.quit_pw =  quit_pw;
		this.quit_ls = 	quit_ls;
	}
	/*Add Theme Resources*/
	public void addThemeResources(Stage mainStage, Stage histStage, Scene scene, String theme, TextArea textArea) {
		this.mainStage = mainStage;
		this.histStage = histStage;
		this.scene = scene;
		HistoryWindowFXMLController.current_theme = theme;
		//Set Current Theme on Switch
		toggleTheme.setText(HistoryWindowFXMLController.current_theme + " Theme\t  (Ctrl + T)");
		this.textArea = textArea;
	}
	/*Add Clear History Resources*/
	public void addClearResources(boolean isHistoryCleared) {
		this.isHistoryCleared = isHistoryCleared;
	}
	/*Add Media Resources*/
	public void addMediaResources(List<Button> main_media_controls) {
		//Instantiate ArrayList of Media Controls
		mediaControls = new ArrayList <>(4);
		mediaControls.add(play);	
		mediaControls.add(stop);
		mediaControls.add(previous);
		mediaControls.add(next);

		this.main_media_controls = main_media_controls;
	}


	/*Property Getter(): clearHistory, Button*/
	public MenuItem getClearHistory() {
		return clearHistory;
	}
	/*Property Getter(): toggleTheme, CheckMenuItem*/
	public CheckMenuItem getToggleTheme() {
		return toggleTheme;
	}
	/*Property Getter(): mediaControls, ArrayList<>*/
	public List<Button> getMediaControls () {
		return mediaControls;
	}


	/* FXML Initializer method */
	@FXML private void initialize() { }
}