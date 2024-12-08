"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os

TEMP_START = 5

SEGMENT_TO_ADDRESS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "constant": "SP",
    "temp": "5",

}
# map segements to hack RAM locations

class CodeWriter:
    """Translates VM commands into Hack assembly code.
    gets the processed command list from the parser, and writes the hack code"""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        # load the mapping of segments to RAM locations
        self.file = output_stream
        self.diff = 0  # For generating unique labels
        self.file_name = ""  # Will be set in set_file_name

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.
        saves the unique file name as a class variable

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.file_name = os.path.splitext(os.path.basename(filename))[0]



    def load_value_to_d(self, value):
        self.file.write(f"""
        @{value}
        D=A
        """)

    def pop_to_d_register(self):
        '''
        sp points to next open pos
        decrement sp and then assign to D
        '''
        self.file.write("""
        @SP
        AM=M-1
        D=M
        """)

    #pushing:
    def push_d_register(self):
        self.file.write("""
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """)

    def write_binary_operation(self, command):
        '''

        x is the top of the stack. we manipulate it in place
        and pop y from the stack
        '''
        # Pop y into D
        self.pop_to_d_register()
        # Set A to SP-1 to access x
        self.file.write("@SP\nA=M-1\n")
        if command == 'add':
            self.file.write("M=M+D\n")
        elif command == 'sub':
            self.file.write("M=M-D\n")
        elif command == 'and':
            self.file.write("M=M&D\n")
        elif command == 'or':
            self.file.write("M=M|D\n")

    def write_unary_operation(self, command):
        '''
        x is the top of the stack. we manipulate it in place
        '''
        self.file.write("@SP\nA=M-1\n")
        if command == 'neg':
            self.file.write("M=-M\n")
        elif command == 'not':
            self.file.write("M=!M\n")
        elif command == 'shiftleft':
            self.file.write("M=M<<\n")
        elif command == 'shiftright':
            self.file.write("M=M>>\n")

    def write_comparison(self, command):
        '''
        use jump and labels to push true or false.
        we load top of stack into d then subtract it from the next val and store in D
        then we jump to the true label if the condition is met
        otherwise assign to sp-1 0 and jump to end
        '''
        label_true = f"{command.upper()}_TRUE_{self.diff}"
        label_end = f"{command.upper()}_END_{self.diff}"
        self.diff += 1

        # Pop y into D
        self.pop_to_d_register()
        # access x in sp-1 and subtract y from it
        self.file.write("@SP\nA=M-1\nD=M-D\n")
        if command == 'eq':
            jump_command = 'JEQ'
        elif command == 'gt':
            jump_command = 'JGT'
        elif command == 'lt':
            jump_command = 'JLT'

        self.file.write(f"""
        @{label_true}
        D;{jump_command}
        @SP
        A=M-1
        M=0
        @{label_end}
        0;JMP
    ({label_true})
        @SP
        A=M-1
        M=-1
    ({label_end})
        """)


    def write_arithmetic(self, command):
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.
        return the lines needed to execute uniary and binary operations        example:
        push constant 12
        push constant 13
        add:
        @12, D=A, @SP,A=M,M=D,@SP,M=M+1,
        @13,D=A,@SP,A=M,M=D,@SP, M=M+1 // finished loading the two numbers
        @SP //
        M=M-1
        A=M // A=SP-1
        D=M // D=13
        @SP
        M=M-1
        A=M // A=SP-2
        M=M+D // M=12+13

        does this need to hanldle the pop and push of add?
        consider a write unbiary and write binary method to handle the push and pop

        Args:
            command (str): an arithmetic command.
        """
        if command in ('add', 'sub', 'and', 'or'):
            self.write_binary_operation(command)
        elif command in ('neg', 'not', 'shiftleft', 'shiftright'):
            self.write_unary_operation(command)
        elif command in ('eq', 'gt', 'lt'):
            self.write_comparison(command)


    def write_push(self, segment, index):
        '''
        get the value from the segment and index
        then assign the value to D
        then push D onto the stack
        '''
        if segment == 'constant':
            self.load_value_to_d(index)
        elif segment in ('local', 'argument', 'this', 'that'):
            base = SEGMENT_TO_ADDRESS[segment]
            self.file.write(f"""
            @{base}
            D=M
            @{index}
            A=D+A
            D=M
            """)
        elif segment == 'temp':
            address = TEMP_START + index
            self.file.write(f"""
            @{address}
            D=M
            """)
        elif segment == 'pointer':
            pointer = 'THIS' if index == 0 else 'THAT'
            self.file.write(f"""
            @{pointer}
            D=M
            """)
        elif segment == 'static':
            variable_name = f"{self.file_name}.{index}"
            self.file.write(f"""
            @{variable_name}
            D=M
            """)

        # Push D onto the stack
        self.push_d_register()

    def write_pop(self, segment, index):
        '''
        store target ram address in R13
        then pop top of stack to D
        then store D in R13
        '''
        if segment in ('local', 'argument', 'this', 'that'):
            base = SEGMENT_TO_ADDRESS[segment]
            self.file.write(f"""
            @{base}
            D=M
            @{index}
            D=D+A
            @R13
            M=D
            """)
        elif segment == 'temp':
            address = TEMP_START + index
            self.file.write(f"""
            @{address}
            D=A
            @R13
            M=D
            """)
        elif segment == 'pointer':
            pointer = 'THIS' if index == 0 else 'THAT'
            self.file.write(f"""
            @{pointer}
            D=A
            @R13
            M=D
            """)
        elif segment == 'static':
            variable_name = f"{self.file_name}.{index}"
            self.file.write(f"""
            @{variable_name}
            D=A
            @R13
            M=D
            """)

        # Pop value into D and store at address in R13
        self.pop_to_d_register()
        self.file.write("""
        @R13
        A=M
        M=D
        """)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.

        examples commands:
        push constant 12
        pop local 0
        pop static 3
        push argument 2 // use the mapping convention
        add a method to handle static by adding the file name to the variable name

        push constant 12
        @12, D=A, @SP,A=M,M=D,@SP,M=M+1,
        pop local 4:
        // get the value from head of stack:
        @4, D=A, @LCL, A=M+D, D=A, @R13, M=D, // R13 = LCL+4
        @SP, M=M-1, A=M, D=M, @R13, A=M, M=D // LCL[4] = SP.pop()
        ulitmately, get the correct base address for the segment, and add the index to it
        then push or pop the value to the stack


        """
        # get base ram, using the mapping for most, and changing symbol for static, and getting the value for constant

        #
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == 'C_PUSH':
            self.write_push(segment, index)
        elif command == 'C_POP':
            self.write_pop(segment, index)
        else:
            raise ValueError(f"Invalid command: {command}")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        pass

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        pass

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
