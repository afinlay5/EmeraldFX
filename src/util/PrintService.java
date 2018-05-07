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

import javafx.scene.Node;
import javafx.stage.Stage;
import javafx.print.Printer;
import javafx.concurrent.Task;
import javafx.print.PrinterJob;
import javafx.concurrent.Service;
import static java.lang.System.out;
import javafx.collections.ObservableSet;


public class PrintService extends Service {

	private static int count;
	private final Thread thread;
	private final Stage stage;
	private final Node node;
	private Printer printer;
	private PrinterJob job;
	private boolean SUCCESS;
	private static final Printer defaultPrinter = Printer.getDefaultPrinter();
	private static final ObservableSet <Printer> allPrinters = Printer.getAllPrinters();

	/* Constructor */
	public PrintService (Thread thread, Stage stage, Node node) throws java.lang.InterruptedException { 
		//Pause the Application Thread
		thread.wait();
		//Grab thread reference
		this.thread = thread;
		//Stage Reference
		this.stage = stage;
		//Node to be printed
		this.node = node;

		out.println("Log: Concurrency: Printer Service Initialized.");
	};

	public void setPrinter (Printer p) {
		printer = p;
	}
	
	@Override
	protected Task createTask() {
		PrintService.count +=1;
		out.println("Log: Concurrency: Printer Service ran " + PrintService.count + " time(s).");

		return new Task<>() {
			protected Void call() throws Exception {
				// Run Later
				javafx.application.Platform.runLater(
					new Runnable() {

						@Override 
						public void run () {
							//If user does not specify a printer, use the default printer.
							if (printer == null) {
								job = PrinterJob.createPrinterJob(defaultPrinter);
							}
							else {
								job = PrinterJob.createPrinterJob(printer);
							}

							//Show Printing Dialog
							job.showPrintDialog(stage);

							/*Print Page*/
							if (job != null){ 
								SUCCESS = job.printPage(node); 
							}
							/*End the print job if it prints successfully */
							if (SUCCESS) {
								job.endJob();
								out.println("Log: Printer Service: Attempt to print succeeded.");
								out.println(job + " on: " + job.getPrinter());
							}
							else {
								out.println("Log: Printer Service: Attempt to print failed.");
							}
						}
					}
				);
				//Resume main thread
				thread.notify();

				return null;
			}
		};
	}
}