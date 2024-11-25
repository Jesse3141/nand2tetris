// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.


// if min = max, no change

@R14 
D=M // get address of array start
@R7 //arr_start
M=D // save
@R9
M=D // prep index to go over array. example: 2050-2052 
@R15
D=D+M // arr start + arr length
D=D-1
@R8 //arr end
M=D


// init min,min_ind and max,max_ind and temp virtual registers R0 - R5
// R0 max, R1 min, R2 max_ind, R3 min_ind, R5 curr value, R9 index
@R7
A=M //load address
D=M // load first value
@R0 //max
M=D
@R7
A=M //load address
D=M // load first value
@R1 //min
M=D
//set indexes
@R7 
D=M 
@R2// max ind
M=D
@R3 //min ind
M=D

(loop)
// check if index beyond boundary: 
	@R9
	D=M
	@R8
	D=M-D
	@swap
	D;JLT // jump if index beyond end

// at each step, if curr value > max: update max and ind. ditto if value < min
	@R9
	A=M //get current value
	D=M
	@R5 //store curr
	M=D
	@R0 //check max
	D=D-M
	@update_max
	D;JGT // jump if curr > max
	@R5 //get current value
	D=M
	@R1 //check min
	D=M-D 
	@update_min
	D;JGT //jump if curr < min 
	@increment
	0;JMP


(increment)
// increment array index and jump
	@R9 
	M=M+1
	@loop
	0;JMP
// loop boundary

(update_max)
	//update max to current and max ind to index
	@R5 //get current
	D=M
	@R0
	M=D
	@R9 //get index
	D=M 
	@R2
	M=D
	@increment
	0;JMP

(update_min)
	//update min to current and min ind to index
	@R5 //get current
	D=M
	@R1
	M=D
	@R9 //get index
	D=M 
	@R3
	M=D
	@increment
	0;JMP
	
(swap)
	//check if min equals max
	@R0
	D=M
	@R1
	D=D-M
	@end
	D;JEQ
	//swap min and max: put the min value in the mem of max
	@R1
	D=M //store min
	@R2 // max ind
	A=M
	M=D
	@R0 
	D=M //max val
	@R3 //min ind
	A=M
	M=D
	@end
	0;JMP
	
// at end: check if min = max. if not, swap
(end)