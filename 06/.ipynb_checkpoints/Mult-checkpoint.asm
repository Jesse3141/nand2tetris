// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here.

// use a loop. execute R1 times. each step decrementing R1, with a jump to end when reaches 0. 

// first store 0 in R2. will update
	@R2
	M=0 
	// start conditions: if either of the inputs is 0, jump to end
	@R0
	D=M
	@END
	D;JEQ       // Jump if R0 is zero

	@R1
	D=M
	@END
	D;JEQ       // Jump if R1 is zero 
	// declare a counter i for the loop and set it to the value of R1
	@R1
	D=M // store value of R1 in D
	@i
	M=D // store value of R1 in i
	// declare start of loop
(LOOP)
	// jump to end if counter 0
	@i
	D=M
	@END
	D;JEQ
	// perform R2 + R0
	@R0
	D=M // store value 
	@R2
	M=M+D
	// decrement counter
	@i 
	M=M-1
	@LOOP
	0;JMP // jump to start of loop
(END)
