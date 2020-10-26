import typing as t
from collections import OrderedDict


class Flags:
    def __init__(self,
                 CF, PF, AF,
                 ZF, SF, TF,
                 IF, DF, OF):
        self.CF = CF
        self.PF = PF
        self.AF = AF
        self.ZF = ZF
        self.SF = SF
        self.TF = TF
        self.IF = IF
        self.DF = DF
        self.OF = OF

    def __str__(self) -> str:
        flags = OrderedDict(self.__dict__.items())
        return ' '.join(filter(lambda k: flags[k], flags))


class Registers:
    def __init__(self, AH, AL,
                       BH, BL,
                       CH, CL,
                       DH, DL,
                       SI, DI,
                       SP, BP,
                       FLAGS: Flags):
        self.AH = AH
        self.AL = AL

        self.BH = BH
        self.BL = BL

        self.CH = CH
        self.CL = CL

        self.DH = DH
        self.DL = DL

        self.SI = SI
        self.DI = DI
        self.SP = SP
        self.BP = BP
        self.FLAGS = FLAGS

    def __str__(self) -> str:
        output = """
                 AH | AL  |        BH | BL  |        CH | CL  |         DH | DL  |
        +-----------+-----+-----------+-----+-----------+-----+------------+-----+
        |AX   0x{:04x}'{:04x} | BX  0x{:04x}'{:04x} | CX  0x{:04x}'{:04x} | DX   0x{:04x}'{:04x} |
        +-------------------------------------------------------------------------

        +----------------------------------+ +-----------------------------------+
        |SI   0x{:08x}  | DI  0x{:08x} | |SP  0x{:08x}  | BP   0x{:08x}  |
        +----------------------------------+ +-----------------------------------+
        +========================================================================+
        |    FLAGS: {: <26}                                   |
        +========================================================================+
        """.format(self.AH, self.AL, self.BH, self.BL, self.CH, self.CL, self.DH, self.DL,
                   self.SI, self.DI, self.SP, self.BP,
                   str(self.FLAGS).replace('FLAGS(', '').replace(')', ''))
        return output

    @classmethod
    def _generic_part_names(cls, register_name: str) -> t.Tuple[str, str]:
        register_name_h_part = register_name[:1] + 'H'
        register_name_l_part = register_name[:1] + 'L'
        return (register_name_h_part, register_name_l_part)


    def _generic_getter(self, register_name: str) -> int:
        register_name_h_part, register_name_l_part = Registers._generic_part_names(register_name)

        register_h_part = getattr(self, register_name_h_part)
        register_l_part = getattr(self, register_name_l_part)

        register = str(register_h_part) + str(register_l_part)
        return int(register)


    def _generic_setter(self,
                        register_name: str,
                        value: t.Union[str, int]):
        register_name_h_part, register_name_l_part = Registers._generic_part_names(register_name)

        if type(value) == int and value < 0b11111111:
            setattr(self, register_name_h_part, 0)
            setattr(self, register_name_l_part, value)
            return
        value = str(value)

        setattr(self, register_name_h_part, int(value[:len(value)//2]))
        setattr(self, register_name_l_part, int(value[len(value)//2:]))


    @property
    def AX(self):
        pass

    @property
    def BX(self):
        pass
    @property
    def CX(self):
        pass
    @property
    def DX(self):
        pass
    

    @AX.getter
    def AX(self):
        return self._generic_getter('AX')

    @BX.getter
    def BX(self):
        return self._generic_getter('BX')

    @CX.getter
    def CX(self):
        return self._generic_getter('CX')

    @DX.getter
    def DX(self):
        return self._generic_getter('DX')


    @AX.setter
    def AX(self, value: t.Union[str, int]):
        self._generic_setter('AX', value)

    @BX.setter
    def BX(self, value: t.Union[str, int]):
        self._generic_setter('BX', value)

    @CX.setter
    def CX(self, value: t.Union[str, int]):
        self._generic_setter('CX', value)

    @DX.setter
    def DX(self, value: t.Union[str, int]):
        self._generic_setter('DX', value)
