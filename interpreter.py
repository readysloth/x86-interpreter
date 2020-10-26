
from processor import OpType, OpArgs, CPU
from registers import Flags, Registers
from memory import MEMORY


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
while True:
    instruction = input('Instruction$ ')
    try:
        getattr(cpu, instruction)()
    except Exception as e:
        print('Exception!' , e)
    print(cpu)



