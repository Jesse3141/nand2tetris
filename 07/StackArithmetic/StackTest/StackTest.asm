// push constant 17

        @17
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 17

        @17
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // eq

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @EQ_TRUE_0
        D;JEQ
        @SP
        A=M-1
        M=0
        @EQ_END_0
        0;JMP
    (EQ_TRUE_0)
        @SP
        A=M-1
        M=-1
    (EQ_END_0)
        // push constant 17

        @17
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 16

        @16
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // eq

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @EQ_TRUE_1
        D;JEQ
        @SP
        A=M-1
        M=0
        @EQ_END_1
        0;JMP
    (EQ_TRUE_1)
        @SP
        A=M-1
        M=-1
    (EQ_END_1)
        // push constant 16

        @16
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 17

        @17
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // eq

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @EQ_TRUE_2
        D;JEQ
        @SP
        A=M-1
        M=0
        @EQ_END_2
        0;JMP
    (EQ_TRUE_2)
        @SP
        A=M-1
        M=-1
    (EQ_END_2)
        // push constant 892

        @892
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 891

        @891
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

        @LT_TRUE_3
        D;JLT
        @SP
        A=M-1
        M=0
        @LT_END_3
        0;JMP
    (LT_TRUE_3)
        @SP
        A=M-1
        M=-1
    (LT_END_3)
        // push constant 891

        @891
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 892

        @892
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

        @LT_TRUE_4
        D;JLT
        @SP
        A=M-1
        M=0
        @LT_END_4
        0;JMP
    (LT_TRUE_4)
        @SP
        A=M-1
        M=-1
    (LT_END_4)
        // push constant 891

        @891
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 891

        @891
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

        @LT_TRUE_5
        D;JLT
        @SP
        A=M-1
        M=0
        @LT_END_5
        0;JMP
    (LT_TRUE_5)
        @SP
        A=M-1
        M=-1
    (LT_END_5)
        // push constant 32767

        @32767
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 32766

        @32766
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

        @GT_TRUE_6
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_6
        0;JMP
    (GT_TRUE_6)
        @SP
        A=M-1
        M=-1
    (GT_END_6)
        // push constant 32766

        @32766
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
        // gt

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
D=M-D

        @GT_TRUE_7
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_7
        0;JMP
    (GT_TRUE_7)
        @SP
        A=M-1
        M=-1
    (GT_END_7)
        // push constant 32766

        @32766
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 32766

        @32766
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

        @GT_TRUE_8
        D;JGT
        @SP
        A=M-1
        M=0
        @GT_END_8
        0;JMP
    (GT_TRUE_8)
        @SP
        A=M-1
        M=-1
    (GT_END_8)
        // push constant 57

        @57
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 31

        @31
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // push constant 53

        @53
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // add

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M+D
// push constant 112

        @112
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
// neg
@SP
A=M-1
M=-M
// and

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M&D
// push constant 82

        @82
        D=A
        
        @SP
        A=M
        M=D
        @SP
        M=M+1
        // or

        @SP
        AM=M-1
        D=M
        @SP
A=M-1
M=M|D
// not
@SP
A=M-1
M=!M