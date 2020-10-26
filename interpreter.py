import re
import typing as t

from processor import OpType, OpArgs, CPU
from registers import Flags, Registers
from memory import MEMORY

INSTRUCTION_RE = '(?P<instruction>\S+)'
FIRST_ARG_RE = '(?P<first_arg>[^,\s]+)'
SECOND_ARG_RE = '(?P<second_arg>[^,\s]+)'
FULL_RE = '{instruction_re}\s*(?:{first_arg_re}(?:\s*,\s*{second_arg_re})?)?'.format(instruction_re=INSTRUCTION_RE,
                                                                                     first_arg_re=FIRST_ARG_RE,
                                                                                     second_arg_re=SECOND_ARG_RE)
COMMAND_PARSER = re.compile(FULL_RE)

def process_instruction(instruction: str) -> t.Tuple[str, OpArgs]:
    match = COMMAND_PARSER.search(instruction)

    instruction = match['instruction']
    first_arg = match['first_arg']
    second_arg = match['second_arg']

    args = OpArgs(first_arg,
                  second_arg,
                  OpType.REG,
                  OpType.IMM)

    if len(list(filter(lambda g: g, match.groups()))) == 1:
        return (instruction, None)
    return (instruction, args)


cpu = CPU(MEMORY, Registers(AH=0, AL=0,
                            BH=0, BL=0,
                            CH=0, CL=0,
                            DH=0, DL=0,
                            SI=0, DI=0,
                            SP=0, BP=0,
                            FLAGS=Flags(CF=0, PF=0, AF=0,
                                        ZF=0, SF=0, TF=0,
                                        IF=0, DF=0, OF=0)))

print('CPU is initialized')
print(cpu)

history = []
while True:
    instruction = input('Instruction$ ')
    if instruction == 'history':
        for i, entry in enumerate(history):
            print(i, entry)
        continue
    if instruction.isnumeric():
        instruction = history[int(instruction)]
    history.append(instruction)
    try:
        cmd, args = process_instruction(instruction.upper())
        if not args:
            getattr(cpu, cmd)()
        else:
            getattr(cpu, cmd)(args)
    except Exception as e:
        print('Exception:' , e)
    print(cpu)



