// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.

// init var for screen end and initial index to color
@SCREEN
D=A
@8192
D=D+A
@screen_end_p1
M=M+D // 16834 + 8192 = 24576

@SCREEN
D=A
@index 
M=D // holds value of current index

// inifinite loop:  
(loop)
// in each cycle, check if key being pressed: is the value at 24576 0 or not
	@KBD
	D=M 	// load value
	@no_key
	D;JEQ 	// jump of not pressed
	// key pressed
	@color_vlaue
	M=-1 // in hack, pixel -1 represent black
	@update_screen
	0;JMP
	
(no_key)
	@color_vlaue
	M=0
	//continue regulary, no need to jump

(update_screen)
	@color_vlaue
	D=M
	@index
	A=M // take address from index and store in A
	M=D // color the chosen pixel
	
	// increment
	@index
	M=M+1

	// if index beyond screen boundary jump to reset index 
	@screen_end_p1
	D=M
	@index 
	D=D-M
	@reset_index
	D;JEQ
	//return to loop
	@loop
	0;JMP
(reset_index)
	@SCREEN
	D=A
	@index
	M=D
	@loop
	0;JMP
	


