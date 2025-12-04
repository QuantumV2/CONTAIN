import math
import sys
sys.set_int_max_str_digits(0)
class Interpreter:
    def __init__(self):
        self.code = ""
        self.ip = 0
        self.bp = 0
        self.boxes = []
        self.is_running = False
        self.queued_ops = []
        self.saved_bp = 0
        self.saved_ip = 0
        self.debug = False
        self.skip_mode = False
        self.commands = {
            '[': self.do_box,
            '"': self.do_string,
            '<': self.do_bp_left,
            '>': self.do_bp_right,
            '$': self.do_save_bp,
            '&': self.do_load_bp,
            '(': self.do_save_ip,
            ')': self.do_load_ip,
            'x': self.do_skip_load,
            '+': self.do_2arg_op,
            '-': self.do_2arg_op,
            '*': self.do_2arg_op,
            '/': self.do_2arg_op,
            '=': self.do_2arg_op,
            '@': self.do_2arg_op,
            '!': self.do_print_num,
            '?': self.do_print_str,
            '^': self.do_create,
            ':': self.do_input_num,
            ';': self.do_input_str,
            '#': self.do_comment,
        }
    def do_comment(self):
        while self.ip < len(self.code)-1 and self.code[self.ip] != '\n':

            self.ip += 1
    def do_input_num(self):
        self.boxes[self.bp]['val'] = int(input())
    def do_input_str(self):
        self.boxes[self.bp]['val'] = ord(input()[0])
    def do_create(self):
        self.boxes.insert(self.bp+1,({'val':0,'cpos':self.boxes[self.bp]['cpos']+1}))
    def do_print_num(self):
        print(self.boxes[self.bp]['val'], end='')
    def do_print_str(self):
        print(chr(self.boxes[self.bp]['val']), end='')
    def do_save_bp(self):
        self.saved_bp = self.bp
    def do_load_bp(self):
        if self.skip_mode:
            self.skip_mode = False
            return
        
        prev = self.bp
        self.bp = self.saved_bp
        self.run_ops(prev)
    def do_save_ip(self):
        self.saved_ip = self.ip
    def do_load_ip(self):
        if self.skip_mode:
            self.skip_mode = False
            return
        self.ip = self.saved_ip
    def do_skip_load(self):
        if self.boxes[self.bp]['val'] == 0:
            self.skip_mode = True
    def do_string(self):
        while self.ip < len(self.code)-1 and self.code[self.ip+1] != '"':

            self.ip += 1
            self.boxes.append({"val":ord(self.code[self.ip]),"cpos":self.ip})
        self.ip +=1
    def do_2arg_op(self):
        self.queued_ops.append(self.code[self.ip])
    def run_ops(self,prev):
        for op in self.queued_ops:
            if op == "@":
                c = self.boxes[self.bp]['val']
                self.boxes[self.bp]['val'] = self.boxes[prev]['val']
                self.boxes[prev]['val'] = c
            elif op == "=":
                self.boxes[prev]['val'] = self.boxes[self.bp]['val']
            elif op == "+":
                self.boxes[prev]['val'] += self.boxes[self.bp]['val']
            elif op == "-":
                self.boxes[prev]['val'] -= self.boxes[self.bp]['val']
            elif op == "*":
                self.boxes[prev]['val'] *= self.boxes[self.bp]['val']
            elif op == "/":
                if self.boxes[self.bp]['val'] == 0:
                    self.boxes.remove(self.boxes[prev])
                    if len(self.boxes) == 0:
                        self.is_running = False
                        return
                    self.bp = max(0, min(self.bp, len(self.boxes)-1))
                else:
                    self.boxes[prev]['val'] //= self.boxes[self.bp]['val']
            elif op == "%":
                if self.boxes[self.bp]['val'] == 0:
                    self.boxes.remove(self.boxes[prev])
                    if len(self.boxes) == 0:
                        self.is_running = False
                        return
                    self.bp = max(0, min(self.bp, len(self.boxes)-1))
                else:
                    self.boxes[prev]['val'] %= self.boxes[self.bp]['val']
        self.queued_ops.clear()
    def do_bp_left(self):
        prev = self.bp
        self.bp = max(self.bp-1, 0)
        self.run_ops(prev)
    def do_bp_right(self):
        prev = self.bp
        self.bp = min(self.bp+1, len(self.boxes)-1)
        self.run_ops(prev)


    def do_box(self):
        numstr = ""
        cur_pos = self.ip
        while self.ip < len(self.code)-1 and self.code[self.ip+1] != "]":

            self.ip += 1
            numstr += self.code[self.ip]
        if numstr == "":
            numstr = "0"
        num = int(numstr)
        for b in self.boxes:
            if b['cpos'] == cur_pos:
                b['val'] = num
                return
        self.boxes.append({"val":num,"cpos":cur_pos})
    def run(self, code):
        self.code = code
        self.is_running = True
        while True:
            if self.is_running == False:
                break
            c = code[self.ip]
            if c in self.commands:
                self.commands[c]()
            if self.debug:
                print(c)
                for b in self.boxes:
                    print(b['val'],", ",end="")
                print("\n")
            self.ip += 1