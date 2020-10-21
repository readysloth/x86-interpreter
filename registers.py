import typing as t

class Registers:
    def __init__(self, AH, AL,
                       BH, BL,
                       CH, CL,
                       DH, DL,
                       SI, DI,
                       SP, BP):
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
