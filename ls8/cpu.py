"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.fl = self.reg[4]
        self.running = True
        self.commands = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b10100111: self.cmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010100: self.jmp,
        }


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self,value, address):
        self.ram[address] = value

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(file) as f:
            lines = f.readlines()
            lines = [line for line in lines if line.startswith('0') or line.startswith('1')]
            program = [int(line[:8],2) for line in lines]

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
                

    def run(self):
        """Run the CPU."""


        while self.running:
            ir = self.ram[self.pc]

            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)

            try: 
                #out put is all of the values returned from the command functions.
                operation_output = self.commands[ir](operand_a,operand_b)
                self.running = operation_output[0]
                self.pc += operation_output[1]

            except Exception as e: #error catch
                print(e)
                print(f"command: {ir}")
                sys.exit()


    
    def ldi(self,operand_a,operand_b):
        self.reg[operand_a] = operand_b
        return(True, 3) #this is to check that it is still running [0] and how many pc spots to hop [1] in this case still runing is true and we hop 3 spots forward.

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return(True, 2)
    
    def hlt(self, operand_a, operand_b):
        return(False, 0)

    def mul(self, operand_a,operand_b):
        self.alu("MUL", operand_a, operand_b)
        return(True,3)


    def push (self, operand_a, operand_b):
        self.reg[7] -= 1
        sp = self.reg[7]
        value = self.reg[operand_a]
        self.ram[sp] = value
        return (True, 2)
    
    def pop(self,operand_a,operand_b):
        sp = self.reg[7]
        value = self.ram[sp]
        self.reg[operand_a] = value
        self.reg[7] += 1
        return (True, 2)

    def cmp(self, operand_a, operand_b):
        new_operand_a = self.reg[operand_a]
        new_operand_b = self.reg[operand_b]
        if new_operand_a > new_operand_b:
            value = 0b00000010
        elif new_operand_a== new_operand_b:
            value = 0b00000001
        else:
            value = 0b00000100
        self.fl = value
        return (True, 3)

    def jeq(self, operand_a, operand_b):
        if self.fl == 0b00000001:
            address = self.reg[operand_a]
            self.pc = address
            return (True, 0)
        else:
            return (True, 2)

    def jne(self, operand_a, operand_b):
        address = self.reg[operand_a]
        if self.fl == 0b00000100:
            self.pc = address
            return (True, 0)
        else:
            return (True, 2)

    def jmp(self, operand_a, operand_b):
        address = self.reg[operand_a]
        self.pc = address
        return (True, 0)

    def call(self, operand_a, operand_b):
        address = self.reg[operand_a]
        self.pc = address
        return(True,0)