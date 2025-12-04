import interpreter
import sys
import os

interp = interpreter.Interpreter()


content = ""

with open(sys.argv[1], "r", encoding='utf-8') as f:
    content = f.read()

interp.run(content)
