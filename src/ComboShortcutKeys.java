/*
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
**/

import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyCombination;
import javafx.scene.input.KeyCodeCombination;

public enum ComboShortcutKeys {

	//Combination Constants
	HOME (new KeyCodeCombination(KeyCode.BACK_QUOTE, KeyCombination.CONTROL_DOWN)), 
	COPY (new KeyCodeCombination(KeyCode.C, KeyCombination.CONTROL_DOWN)),
	CUT (KeyCombination.valueOf("CTRL+X")),
	PASTE (new KeyCodeCombination(KeyCode.V, KeyCombination.CONTROL_DOWN)),
	QUIT (new KeyCodeCombination(KeyCode.Q, KeyCombination.CONTROL_DOWN)),
	CLEAR_HIST (new KeyCodeCombination(KeyCode.D, KeyCombination.CONTROL_DOWN)),
	HISTORY (new KeyCodeCombination(KeyCode.H, KeyCombination.CONTROL_DOWN)),
	THEME_TOGGLE(new KeyCodeCombination(KeyCode.T, KeyCombination.CONTROL_DOWN));
	

	//Combo Constant Value
	private final KeyCombination COMBO;

	//Get Constant Value
	public KeyCombination getCombo() { return COMBO; }

	//Constructor
	ComboShortcutKeys(KeyCombination combo) {
		this.COMBO = combo;
	}
}