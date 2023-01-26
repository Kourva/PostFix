#!/usr/bin/env python3


# Simple app to convert Infix yo Postfix
# GitHub: htpps://github.com/Kourva/PostFix


# Imports
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious


# KV config
with open("main.kv", "r") as kv:
    Builder.load_string(kv.read())


# Class to convert the expression
class Conversion:

    # Constructor to initialize the class variables
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity

        # This array is used a stack
        self.array = []

        # Precedence setting
        self.output = []
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

    # check if the stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # A utility function to check is the given character
    # is operand
    def isOperand(self, ch):
        return ch.isalpha()

    # Check if the precedence of operator is strictly
    # less than top of stack or not
    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a <= b else False
        except KeyError:
            return False

    # The main function that
    # converts given infix expression
    # to postfix expression
    def infixToPostfix(self, exp):

        # Iterate over the expression for conversion
        for i in exp:
            # If the character is an operand,
            # add it to output
            if self.isOperand(i):
                self.output.append(i)

            # If the character is an '(', push it to stack
            elif i == "(":
                self.push(i)

            # If the scanned character is an ')', pop and
            # output from the stack until and '(' is found
            elif i == ")":
                while (not self.isEmpty()) and self.peek() != "(":
                    a = self.pop()
                    self.output.append(a)
                if not self.isEmpty() and self.peek() != "(":
                    return -1
                else:
                    self.pop()

            # An operator is encountered
            else:
                while not self.isEmpty() and self.notGreater(i):
                    self.output.append(self.pop())
                self.push(i)

        # pop all the operator from the stack
        while not self.isEmpty():
            self.output.append(self.pop())

        return "".join(self.output)


# StartMenu screen
class StartMenuScreen(Screen):
    # Path to fonts
    KremlinMenshevik = "KremlinMenshevikBold.ttf"
    SourceCodePro = "SourceCodeProBold.ttf"

    # Path to assets
    background = "background.jpg"

    # Encryption method
    def convert(self, textinput, output):

        exp = textinput.text
        obj = Conversion(len(exp))
        result = obj.infixToPostfix(exp)

        output.text = f"[b][font=SourceCodeProBold.ttf]{result}[/font][/b]"


# Main class
class PostFix(App):

    # Build method
    def build(self):

        # Root screen
        root = ScreenManager()

        # Main menu screen
        self.StartMenuScreen = StartMenuScreen(name="StartMenu")
        root.add_widget(self.StartMenuScreen)

        # Set current screen to main menu and return root
        root.current = "StartMenu"
        return root


# Run App
PostFix().run()

# End of file
