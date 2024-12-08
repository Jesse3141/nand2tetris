"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
# dicts mapping vm commands to hack commands
C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP="C_POP"

COMMAND_TYPE_DICT = {"add": C_ARITHMETIC, "sub": C_ARITHMETIC,
                              "neg": C_ARITHMETIC, "eq": C_ARITHMETIC,
                              "gt": C_ARITHMETIC, "lt": C_ARITHMETIC,
                              "and": C_ARITHMETIC, "or": C_ARITHMETIC,
                              "not": C_ARITHMETIC,
                                "shiftleft": C_ARITHMETIC, "shiftright": C_ARITHMETIC,
                            "push": C_PUSH, "pop": C_POP,
                     }

class Parser:
    """
    # Parser

    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.
    notes: can parse line by line since no multi-line commands

    first pass: remove all whie space. currently no labels.
    then use the command class to find its type, and values


    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that,
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>

      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.input_lines = input_file.read().splitlines()
        # line counter
        self.current_line = 0
        self.empty_command = False
        self.raw = ""
        self.command = ""

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_line < len(self.input_lines)


    def advance(self) -> None:
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.

        going line by line, remove comment and all after it,
        then split by white space into a list of 1-3 elements
        if empty, set empty flag
        """
        # get line
        line = self.input_lines[self.current_line]
        # remove comment
        line = line.split("//")[0]
        # Remove leading and trailing whitespace
        line = line.strip()
        #return if empty
        if not line:
            self.empty_command = True
            self.current_line += 1
            return
        self.empty_command = False
        # assign to raw
        self.raw = line
        # split by white space
        self.command = line.split()
        self.current_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        #check if command in dict, else raise valuerror
        if self.command[0] not in COMMAND_TYPE_DICT:
            raise ValueError(f"Invalid command: {self.command[0]}")
        return COMMAND_TYPE_DICT[self.command[0]]

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        command_type = self.command_type()
        if command_type == 'C_RETURN':
            raise Exception("Should not call arg1() if the current command is 'C_RETURN'")
        elif command_type == 'C_ARITHMETIC':
            return self.command[0]
        else:
            return self.command[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP",
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        command_type = self.command_type()
        if command_type in ('C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'):
            return int(self.command[2])
        else:
            raise Exception(f"arg2() incorrectly called for '{command_type}'")
