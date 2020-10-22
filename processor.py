"""
Thanks to http://www.gabrielececchetti.it/Teaching/CalcolatoriElettronici/Docs/i8086_instruction_set.pdf
"""
import typing as t

import memory
from registers import Registers

class CPU:
    def __init__(self,
                 ram: t.List[int],
                 registers: Registers):
        self.ram = ram
        self.registers = registers


    def AAA(self):
        if self.registers.AL & 0b1111 > 9 or self.registers.FLAGS.AF:
            self.registers.AL += 6
            self.registers.AH += 1
            self.registers.FLAGS.AF = 1
            self.registers.FLAGS.CF = 1
        else:
            self.registers.FLAGS.AF = 0
            self.registers.FLAGS.CF = 0
        return self


    def AAD(self):
        self.registers.AL += self.registers.AH * 10
        self.registers.AH = 0
        return self


    def AAM(self):
        self.registers.AH = self.registers.AL // 10
        self.registers.AL = self.registers.AL % 10
        return self


    def AAS(self):
        if self.registers.AL & 0b1111 > 9 or self.registers.FLAGS.AF:
            self.registers.AL -= 6
            self.registers.AH -= 1
            self.registers.FLAGS.AF = 1
            self.registers.FLAGS.CF = 1
        else:
            self.registers.FLAGS.AF = 0
            self.registers.FLAGS.CF = 0
        return self
