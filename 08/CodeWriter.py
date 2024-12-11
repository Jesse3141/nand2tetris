import typing

TEMP_START = 5
POINTER_START = 3

"""Translates VM commands into Hack assembly code."""
class CodeWriter:
    def __init__(self, output_stream: typing.TextIO, label_counter = None) -> None:
        """Initializes the CodeWriter.
        Args:
            output_stream (typing.TextIO): output stream.
            counter: a list of one elem:
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.label_counter = label_counter
        self.output_stream = output_stream
        self.input_filename = None
        self.l_num = 0
        self.comparison_commands = {"gt": "JGT", "lt": "JLT", "eq": "JEQ"}
        self.curr_function = ''

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.
        I'm adding a saving of the file name without the extension
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
        self.input_filename = filename


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        binary_commands = {"add": "D+M", "sub": "M-D", "and": "D&M", "or": "D|M"}
        unary_commands = {"neg": "-M", "not": "!M", "shiftleft": "M<<", "shiftright": "M>>"}
        comparison_commands = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}

        if command in binary_commands:
            # Binary operations: add, sub, and, or
            self.output_stream.write("@SP\n")
            self.output_stream.write("M=M-1\n")
            self.output_stream.write("A=M\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("A=A-1\n")
            self.output_stream.write("M=" + binary_commands[command] + "\n")

        elif command in unary_commands:
            # Unary operations: neg, not, shiftleft, shiftright
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("M=" + unary_commands[command] + "\n")

        elif command in comparison_commands:
            # Comparison operations: eq, lt, gt
            self.output_stream.write("@SP\n")
            self.output_stream.write("M=M-1\n")
            self.output_stream.write("A=M\n")
            self.output_stream.write("D=M\n")

            self.output_stream.write("@IS_POS" + str(self.l_num) + "\n")
            self.output_stream.write("D;JGT\n")
            self.output_stream.write("@IS_NEG" + str(self.l_num) + "\n")
            self.output_stream.write("0;JMP\n")

            self.output_stream.write("(IS_POS" + str(self.l_num) + ")\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("@SAME_SIGN" + str(self.l_num) + "\n")
            self.output_stream.write("D;JGT\n")
            self.output_stream.write("@RETURN_TRUE" + str(self.l_num) + "\n")
            self.output_stream.write("D;" + comparison_commands[command] + "\n")
            self.output_stream.write("@RETURN_FALSE" + str(self.l_num) + "\n")
            self.output_stream.write("0;JMP\n")

            self.output_stream.write("(IS_NEG" + str(self.l_num) + ")\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("@SAME_SIGN" + str(self.l_num) + "\n")
            self.output_stream.write("D;JLT\n")
            self.output_stream.write("@RETURN_TRUE" + str(self.l_num) + "\n")
            self.output_stream.write("D;" + comparison_commands[command] + "\n")
            self.output_stream.write("@RETURN_FALSE" + str(self.l_num) + "\n")
            self.output_stream.write("0;JMP\n")

            self.output_stream.write("(SAME_SIGN" + str(self.l_num) + ")\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("A=A-1\n")
            self.output_stream.write("D=M-D\n")
            self.output_stream.write("@RETURN_TRUE" + str(self.l_num) + "\n")
            self.output_stream.write("D;" + comparison_commands[command] + "\n")
            self.output_stream.write("@RETURN_FALSE" + str(self.l_num) + "\n")
            self.output_stream.write("0;JMP\n")

            self.output_stream.write("(RETURN_TRUE" + str(self.l_num) + ")\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("M=-1\n")
            self.output_stream.write("@END" + str(self.l_num) + "\n")
            self.output_stream.write("0;JMP\n")

            self.output_stream.write("(RETURN_FALSE" + str(self.l_num) + ")\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("M=0\n")

            self.output_stream.write("(END" + str(self.l_num) + ")\n")
            self.l_num += 1

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        segments_dict = {"constant": "constant", "local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        if command == "C_PUSH":
            if segment in ["local", "argument", "this", "that", "constant"]:
                self.output_stream.write("@" + str(index) + "\n")
                self.output_stream.write("D=A\n")
                if segment != "constant":
                    self.output_stream.write("@" + segments_dict[segment] + "\n")
                    self.output_stream.write("A= D+M\n")
                    self.output_stream.write("D=M\n")

            if segment == "static":
                self.output_stream.write("@" + self.input_filename + "." + str(index) + "\n")
                self.output_stream.write("D=M\n")
            if segment == "temp":
                self.output_stream.write("@R" + str(TEMP_START + index) + "\n")
                self.output_stream.write("D=M\n")
            if segment == "pointer":
                self.output_stream.write("@R" + str(POINTER_START + index) + "\n")
                self.output_stream.write("D=M\n")

            self.output_stream.write("@SP\n")
            self.output_stream.write("M=M+1\n")
            self.output_stream.write("A=M-1\n")
            self.output_stream.write("M=D\n")

        if command == "C_POP":
            if segment in ["local", "argument", "this", "that"]:
                self.output_stream.write("@" + str(index) + "\n")
                self.output_stream.write("D=A\n")
                self.output_stream.write("@" + segments_dict[segment] + "\n")
                self.output_stream.write("D=D+M\n")

                self.output_stream.write("@R13\n")
                self.output_stream.write("M=D\n")

                self.output_stream.write("@SP\n")
                self.output_stream.write("M=M-1\n")
                self.output_stream.write("A=M\n")
                self.output_stream.write("D=M\n")

                self.output_stream.write("@R13\n")
                self.output_stream.write("A=M\n")
                self.output_stream.write("M=D\n")

            elif segment == "static":
                self.output_stream.write("@SP\n")
                self.output_stream.write("M=M-1\n")
                self.output_stream.write("A=M\n")
                self.output_stream.write("D=M\n")
                self.output_stream.write("@" + self.input_filename + "." + str(index) + "\n")
                self.output_stream.write("M=D\n")

            elif segment in ["temp", "pointer"]:
                self.output_stream.write("@SP\n")
                self.output_stream.write("M=M-1\n")
                self.output_stream.write("A=M\n")
                self.output_stream.write("D=M\n")
                base = POINTER_START if segment == "pointer" else TEMP_START
                self.output_stream.write("@R" + str(base + index) + "\n")
                self.output_stream.write("M=D\n")

    def create_label(self, label: str) -> str:
        """Creates a label for the given label name.

        Args:           label (str): the label name.
        Returns:            str: the label.
        """
        full_label = f'{self.input_filename}.{self.curr_function}${label}.{self.label_counter[0]}'
        self.label_counter[0] += 1
        return full_label

    def write_label(self, label: str,formatted = False) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".
        eg, given the commnad
        label loop_start,
        writes the required assembly code: (label_name)
        therefore, if inside a function, need to save it's name to the writer
        but in this format: filename.function_name$label
        edge cases:
        a function that makes tow calls to the smae function.
        each return must be unqiue.
        Args:
            label (str): the label to write.
        """
        if not formatted:
            label = self.create_label(label)
        self.output_stream.write(f'({label})\n')




    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.
        execute the jump:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.
        push argument 0
        if-goto LOOP_START  // If counter != 0, goto LOOP_START
        process:
        load argument 0 into D,
        load loop address @label
        then jump if D is not 0, ie JNE
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

        note:
        add the asm code to initalise to 0 the local variables.
        this will be executed whenever the function is called.
        part of a larger api which assumes local vairables will be 0.
        assumption: the function name includes it's file name

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
        #update curr function
        self.curr_function = function_name
        # create the function name label: filename.function_name
        self.output_stream.write(f'({function_name})\n')
        #initialize the local variables to 0
        for _ in range(n_vars):
            self.write_push_pop("C_PUSH", "constant", 0)

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

        is assumes the last n items on the stack are the n args.
        the idea is that the function will place the result in arg 0
        and the code will continue from where it left off by jumping to the label of r

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
        #create return address label: filename.function_name$ret.i
        # but the write label adds filename.function_name and the count
        return_label = self.create_label(f'ret_from_{function_name}')
        # push the label onto the stack
        self.write_push_pop("C_PUSH", "constant", return_label)
        #push LCL, ARG, THIS, THAT
        self.write_push_pop("C_PUSH", "LCL", 0)
        self.write_push_pop("C_PUSH", "ARG", 0)
        self.write_push_pop("C_PUSH", "THIS", 0)
        self.write_push_pop("C_PUSH", "THAT", 0)
        #reposition ARG to SP-5-n_args
        self.output_stream.write("@SP\nD=M\n@5\nD=D-A\n@n_args\nD=D-A\n@ARG\nM=D\n")
        #reposition LCL to SP
        self.output_stream.write("@SP\nD=M\n@LCL\nM=D\n")
        #goto function_name
        self.write_goto(function_name)
        # write the label
        self.write_label(return_label, True)

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

        # i will use R13 to store the return address
        self.output_stream.write("@LCL\nD=M\n@R13\nM=D\n")
        #save return add to R14
        self.output_stream.write("@5\nA=D-A\nD=M\n@R14\nM=D\n")
        # pop to arg 0
        self.write_push_pop("C_POP", "argument", 0)
        # reposition SP
        self.output_stream.write("@ARG\nD=M+1\n@SP\nM=D\n")
        # restore THAT, THIS, ARG, LCL
        self.output_stream.write("@R13\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n")
        self.output_stream.write("@R13\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n")
        self.output_stream.write("@R13\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n")
        self.output_stream.write("@R13\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n")
        # goto return address
        self.output_stream.write("@R14\nA=M\n0;JMP\n")

    def write_init(self):
        '''
        set the stack pointer to 256 and call Sys.init
        '''
        self.output_stream.write("@256\n")
        self.output_stream.write("D=A\n")
        self.output_stream.write("@SP\n")
        self.output_stream.write("M=D\n")
        self.write_call("Sys.init", 0)
