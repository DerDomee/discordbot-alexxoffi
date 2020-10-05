import re
""" stavlex - A StringToArgumentVectorLexer

    @version 0.1.0
    @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    @maintainer Dominik "derdomee_" Riedig <me@dominikriedig.de>


    This module introduces a function 'get_argv' that takes a string
    and generates a full-fledged argument vector out of it.

    stavlex supports full escaping and generates POSIX-compliant argv.
    It is split into three parts:
    Lexer:     create_character_definition - creates a list of every character
               in the string and determines if it is escaped. The escape
               character itself gets deleted. The lexer also supports
               meta-escapes (Escaping the escape character works).
    Parser:    determine_split_points - From the character definition, create
               an array of split points. This array then defines where every
               argument starts and ends.
    Generator: generate_argv - From the split points, create the argument
               vector itself. This is really fast-forward.

"""


def create_character_definition(argstring):
    """ Creates an array of character definitions.
        A character definition is a dict containing the character itself and
        his escape-state.

        @arg argstring: String - The input string
        @return characters: Dict[] - Ordered list of character definitions

        @since 0.0.1
        @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    """
    characters = []
    skip_next = False
    for i in range(len(argstring)):
        if skip_next is True:
            skip_next = False
            continue

        if not characters:
            if argstring[i] == "\\":
                skip_next = True
                characters.append({
                    'character': argstring[i + 1],
                    'escaped': True})
            else:
                characters.append({
                    'character': argstring[i],
                    'escaped': False})
        else:
            lastchar = characters[-1]
            if argstring[i] == "\\" and lastchar['escaped'] is False:
                skip_next = True
                characters.append({
                    'character': argstring[i + 1],
                    'escaped': True})
            else:
                characters.append({
                    'character': argstring[i],
                    'escaped': False})
    return characters


def debug_character_definition(characters):
    """ Generates a string useful for debugging. Every normal character
        returns ANSI-default-colored and every escaped character returns
        ANSI-red-colored.

        @arg characters: Dict[] - Ordered list of character definitions
        @return charstr: String - ANSI-Colored String

        @since 0.0.1
        @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    """
    charstr = ""
    for c in characters:
        if c['escaped']:
            charstr = charstr + "\033[1;31m" + c['character'] + "\033[0;0m"
        else:
            charstr = charstr + c['character']
    return charstr


def determine_split_points(characters):
    """ Generates an ordered array of split points. Every odd element defines
        the character index of the start of an argument inside the string
        and the following even element defines it's end point.

        @arg characters: Dict - Ordered list of character definitions
        @return split_points: int[] - Ordered list of split-point indices

        @since 0.0.1
        @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    """
    WORDMODES = ['OUTSIDE', 'SINGLE', 'SQUOTE', 'DQUOTE']
    current_mode = WORDMODES[0]
    split_points = []

    for i in range(len(characters)):
        char = characters[i]['character']
        escaped = characters[i]['escaped']

        if current_mode == WORDMODES[0]:
            if char == "\'" and not escaped:
                current_mode = WORDMODES[2]
                split_points.append(i + 1)
            elif char == "\"" and not escaped:
                current_mode = WORDMODES[3]
                split_points.append(i + 1)
            elif re.search('[^\\s]', char):
                current_mode = WORDMODES[1]
                split_points.append(i)
        elif current_mode == WORDMODES[1]:
            if re.search('[\\s]', char) and not escaped:
                current_mode = WORDMODES[0]
                split_points.append(i)
        elif current_mode == WORDMODES[2]:
            if char == "\'" and not escaped:
                current_mode = WORDMODES[0]
                split_points.append(i)
        elif current_mode == WORDMODES[3]:
            if char == "\"" and not escaped:
                current_mode = WORDMODES[0]
                split_points.append(i)
    if len(split_points) % 2 != 0:
        split_points.append(len(characters))
    return split_points


def generate_argv(characters, start_end_points):
    """ Generates the argument vector out of lexed and parsed information

        @arg characters: Dict[] - Ordered list of character definitions
        @arg start_end_points: int[] - Ordered list of split-point indices
        @return argv: String[] - List of arguments in order of occurence

        @since 0.0.1
        @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    """
    argv = []
    for i in range(0, len(start_end_points) - 1, 2):
        argument = "".join(
            [c['character'] for c in characters[
                start_end_points[i]:start_end_points[i + 1]]])
        argv.append(argument)
    return argv


def get_argv(argstring):
    """ Creates an argument vector (argv) from a given string

        @arg argstring: String - The input string
        @return argv: String[] - List of arguments in order of occurence

        @since 0.0.1
        @author Dominik "derdomee_" Riedig <me@dominikriedig.de>
    """
    characters = create_character_definition(argstring)
    """print(debug_character_definition(characters))"""
    start_end_points = determine_split_points(characters)
    """print(start_end_points)"""
    argv = generate_argv(characters, start_end_points)
    return argv
