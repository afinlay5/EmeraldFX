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