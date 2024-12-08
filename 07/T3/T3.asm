// push constant 32767

        @32767
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // neg
@SP
A=M-1
M=-M
// push constant 1

        @1
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // sub

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M-D
// push constant 32767

        @32767
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // lt

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @LT_TRUE_0
        D;JLT
        @SP
        A=M-1
        M=0
        @LT_END_0
        0;JMP
    (LT_TRUE_0)
        @SP
        A=M-1
        M=-1
    (LT_END_0)
        // push constant 32767

        @32767
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 32767

        @32767
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // neg
@SP
A=M-1
M=-M
// push constant 1

        @1
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // sub

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M-D
// gt

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @GT_TRUE_1
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_1
        0;JMP
    (GT_TRUE_1)
        @SP
        A=M-1
        M=-1
    (GT_END_1)
        // push constant 20000

        @20000
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // neg
@SP
A=M-1
M=-M
// push constant 1

        @1
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // sub

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M-D
// push constant 30000

        @30000
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // gt

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @GT_TRUE_2
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_2
        0;JMP
    (GT_TRUE_2)
        @SP
        A=M-1
        M=-1
    (GT_END_2)
        // push constant 20000

        @20000
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 30000

        @30000
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // neg
@SP
A=M-1
M=-M
// push constant 1

        @1
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // sub

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M-D
// gt

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @GT_TRUE_3
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_3
        0;JMP
    (GT_TRUE_3)
        @SP
        A=M-1
        M=-1
    (GT_END_3)
        