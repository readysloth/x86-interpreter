"""
Thanks to http://www.gabrielececchetti.it/Teaching/CalcolatoriElettronici/Docs/i8086_instruction_set.pdf
"""
import typing as t

from enum import Enum, auto

import memory
from registers import Registers

def get_bits(integer: int):
    return '{:b}'.format(integer)

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


    def CALL(self, arguments: OpArgs):
        raise NotImplementedError('CALL is not implemented yet')


    def CBW(self):
        if self.registers.AL & 0b1000 != 0:
            self.registers.AH = 0xFF
            return self

        self.registers.AH = 0
        return self

    def CLC(self):
        self.registers.FLAGS.CF = 0
        return self


    def CLD(self):
        self.registers.FLAGS.DF = 0
        return self


    def CMC(self):
        self.registers.FLAGS.CF ^= 1
        return self


    def CMP(self, arguments: OpArgs):
        first_arg, second_arg = self._get_args(arguments)
        result_bits = get_bits(first_arg - second_arg)
        self.registers.FLAGS.CF = 1 if first_arg > second_arg else 0
        self.registers.FLAGS.OF = 1 if '{:b}'.format(first_arg)[0] != result_bits[0] else 0
        self.registers.FLAGS.SF = 1 if result_bits[0] == '1' else 0
        self.registers.FLAGS.ZF = 1 if first_arg - second_arg == 0 else 0
        self.registers.FLAGS.AF = 0 #TODO: AF = 1 if Carry in the low nibble of result
        self.registers.FLAGS.PF = 1 if result_bits[-8:].count('1') == result_bits[-8:].count('0') else 0
        return self


    def CMPSB(self, arguments: OpArgs):
        raise NotImplementedError('CMPSB is not implemented due to segment registers are not implemented yet')

    
    def CMPSW(self, arguments: OpArgs):
        raise NotImplementedError('CMPSW is not implemented due to segment registers are not implemented yet')


    def CWD(self):
        if get_bits(self.registers.AX)[0] == '1':
            self.registers.DX = 0xFFFF
        else:
            self.registers.DX = 0

        return self


    def DAA(self):
        if self.registers.AL & 0b1111 > 9 or self.registers.FLAGS.AF:
            self.registers.AL += 6
            self.registers.FLAGS.AF = 1
        if self.registers.AL > 0x9F or self.registers.FLAGS.CF:
            self.registers.AL += 0x60
            self.registers.FLAGS.CF = 1
        return self


    def DAS(self):
        if self.registers.AL & 0b1111 > 9 or self.registers.FLAGS.AF:
            self.registers.AL -= 6
            self.registers.FLAGS.AF = 1
        if self.registers.AL > 0x9F or self.registers.FLAGS.CF:
            self.registers.AL -= 0x60
            self.registers.FLAGS.CF = 1
        return self


    def DEC(self, arguments: OpArgs):
        first_arg, _ = self._get_args(arguments)
        if arguments.to_type == OpType.REG:
            setattr(self.registers,
                    arguments.to,
                    first_arg - 1)
        elif arguments.to_type == OpType.MEM:
            self.ram[arguments.to] -= 1
        
        return self


    def DIV(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def HLT(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def IDIV(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def IMUL(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def INC(self, arguments: OpArgs):
        first_arg, _ = self._get_args(arguments)
        if arguments.to_type == OpType.REG:
            setattr(self.registers,
                    arguments.to,
                    first_arg + 1)
        elif arguments.to_type == OpType.MEM:
            self.ram[arguments.to] += 1
        
        return self


    def INT(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def INTO(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')


    def IRET(self, arguments: OpArgs):
        raise NotImplementedError('Not implemented yet')
