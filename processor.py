"""
Thanks to http://www.gabrielececchetti.it/Teaching/CalcolatoriElettronici/Docs/i8086_instruction_set.pdf
"""
import typing as t

from enum import Enum, auto

import memory
from registers import Registers

class OpType(Enum):
    REG = auto()
    MEM = auto()
    IMM = auto()

class OpArgs:
    def __init__(self,
                 to: t.Union[int, str],
                 arg: t.Union[int, str],
                 to_type: OpType,
                 arg_type: OpType):
        self.to = to
        self.arg = arg
        self.to_type = to_type
        self.arg_type = arg_type

    def op_type(self):
        return (self.to_type, self.arg_type)


class CPU:
    def __init__(self,
                 ram: t.List[int],
                 registers: Registers):
        self.ram = ram
        self.registers = registers

    def __str__(self):
        return str(self.registers)

    def _get_args(self, arguments: OpArgs):
        first_arg = getattr(self.registers, arguments.to)

        if arguments.arg_type == OpType.REG:
            second_arg = getattr(self.registers, arguments.arg)
        elif arguments.arg_type == OpType.MEM:
            second_arg = self.ram[arguments.arg]
        elif arguments.arg_type == OpType.IMM:
            second_arg = arguments.arg

        return first_arg, second_arg


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

    def ADC(self, arguments: OpArgs):
        cpu = self.ADD(arguments)
        if arguments.to_type == OpType.REG:
            reg_val = getattr(self.registers, arguments.to)
            setattr(cpu.registers,
                    arguments.to,
                    reg_val + cpu.registers.FLAGS.CF)
            return cpu

        cpu.ram[arguments.to] += cpu.registers.FLAGS.CF

        return cpu


    def ADD(self, arguments: OpArgs):
        first_arg, second_arg = self._get_args(arguments)
        if arguments.to_type == OpType.REG:
            setattr(self.registers,
                    arguments.to,
                    first_arg + second_arg)
            return self

        self.ram[arguments.to] += second_arg

        return self


    def AND(self, arguments: OpArgs):
        first_arg, second_arg = self._get_args(arguments)
        if arguments.to_type == OpType.REG:
            setattr(self.registers,
                    arguments.to,
                    first_arg & second_arg)
            return self

        self.ram[arguments.to] &= second_arg

        return self

