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