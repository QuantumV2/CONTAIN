# CONTAIN
### An esolang all about boxes
## Overview
CONTAIN is an esolang about boxes that contain numbers.

## Usage
    python main.py "examples/helloworld.contain"
## Instructions
```

Programs end when all containers get deleted.

Boxes:
[number] - Create container at this character position with default number set.

[] - Init container to 0

"text" - Create sequential containers with Unicode values (used cleverly in some example programs to cut down on space, see programs with "_golf" postfixes)

Box Pointer Movement:

Box Pointer movement triggers all queued operations.

> - Move BP to next container (by creation order)

< - Move BP to previous container

$ - Save current BP position

& - Load saved BP position

Instruction Pointer (IP) Control:

( - Save current IP position

) - Load saved IP position

x - Skip next ) or & if current box = 0

Binary Operations (use current & next containers):

Next container in this case refers to the container that you end up on after BP movement (can be same as current!)

+ - Add

- - Subtract

* - Multiply

/ - Divide (deletes container if divide by zero)

= - Set current = next

@ - Swap current and next

Unary Operations:

! - Print current as number

? - Print current as ASCII

^ - Create new container: position = current+1, val=0

Input:

: - Input number to current container

; - Input ASCII to current container

Special:

# - comment everything after it out
Anything else - NOP
```