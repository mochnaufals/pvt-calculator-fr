from math import e as e_nat
from math import log as ln
from math import log10, ceil, floor

def array_P(P_atm, step, P_res, Pb):
    """
    Array 1D dari tekanan untuk standardisasi (psia)
    :param start: Biasanya 14.7 psia
    :param step: Biasanya 1 psia
    :param stop: Biasanya P reservoir (psia)
    :return: Array 1D (psia)
    """
    P = [P_atm]
    for i in range(ceil(P_atm),floor(Pb),step):
        P.append(i)
    P.append(Pb)
    for j in range(ceil(Pb)+step, ceil(P_res)+step, step):
        P.append(j)
    return P

class compressibility_factor:
    def dranchuk_abou_kassem(self):
        """
        Menghitung gas compressibility factor
        :return:
        """
        A1 = 0.3265
        A2 = -1.0700
        A3 = -0.5339
        A4 = 0.01569
        A5 = -0.05165
        A6 = 0.5475
        A7 = -0.7361
        A8 = 0.1844
        A9 = 0.1056
        A10 = 0.6134
        A11 = 0.7210

        # TODO: Gajadi deh nanti aja
