from math import e, pi
from math import log10, ceil, floor
from math import log as ln

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

class Bt:
    def glaso(self, input_data, Rs_array, Bo_array, Pb):
        """
        Glaso for total FVF
        :return:
        """
        gas_SG = input_data['gas_SG']
        T_res = input_data['T_res']
        oil_API = input_data['oil_API']

        T_res += 460
        oil_SG = 141.5 / (131.5 + oil_API)

        P = Rs_array[0]
        Rs = Rs_array[1]
        Bo = Bo_array[1]

        Bt = []
        for i in range(len(P)):
            if P[i]<=Pb:
                C = 2.9*(10**(-0.00027*Rs[i]))
                A_star = ( ( Rs[i]*((T_res-460)**0.5)*(oil_SG**C) )/( gas_SG**0.3 ) )*(P[i]**-1.1089)
                Bt.append(10**(0.080135 + 0.47257*log10(A_star) + 0.17351*((log10(A_star))**2)))
            else:
                Bt.append(Bo[i])
        data = [P, Bt]
        return data

class Bo:
    def glaso(self, input_data, Rs_array, IC_array, Pb):
        """
        Oil Formation Volume Factor
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        T_res = input_data['T_res']

        T_res += 460
        oil_SG = 141.5/(131.5+oil_API)

        P = Rs_array[0]
        Rs = Rs_array[1]
        c_o = IC_array[1]

        Bo = []
        for i in range(len(P)):
            if P[i]<=Pb:
                Bob_star = Rs[i]*((gas_SG/oil_SG)**0.526) + 0.968*(T_res-460)
                A = -6.58511 + 2.91329*log10(Bob_star) - 0.27683*(log10(Bob_star))**2
                Bob = 1+(10**A)
                Bo.append(Bob)
            else:
                Bo.append(Bob*(e**(-c_o[i]*(P[i]-Pb))))
        data = [P, Bo]
        return data

    def marhoun(self, input_data, Rs_array, IC_array, Pb):
        """
        Oil Formation Volume Factor (Bo) dalam bbl/STB
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        T_res = input_data['T_res']

        T_res += 460
        oil_SG = 141.5 / (131.5 + oil_API)

        a = 0.742390
        b = 0.323294
        c = -1.202040

        P = Rs_array[0]
        Rs = Rs_array[1]
        c_o = IC_array[1]

        Bo = []
        for i in range(len(P)):
            if P[i]<=Pb:
                F = (Rs[i]**a)*(gas_SG**b)*(oil_SG**c)
                Bob = 0.497069 + 0.862963*(10**-3)*T_res + 0.182594*(10**-2)*F + 0.318099*(10**-5)*(F**2)
                Bo.append(Bob)
            else:
                Bo.append(Bob * (e ** (-c_o[i] * (P[i] - Pb))))
        data = [P, Bo]
        return data

    def petroky_fahrshad(self, input_data, Rs_array, IC_array, Pb):
        """
        Petroky-Fahrshad untuk oil formation volume factor
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        T_res = input_data['T_res']

        T_res += 460
        oil_SG = 141.5 / (131.5 + oil_API)

        P = Rs_array[0]
        Rs = Rs_array[1]
        c_o = IC_array[1]

        Bo = []
        for i in range(len(P)):
            if P[i]<=Pb:
                Bob = 1.0113 + 7.2046*(10**-5)*(((Rs[i]**0.3738)*((gas_SG**0.2914)/(oil_SG**0.6265))+0.24626*((T_res-460)**0.5371))**3.0936)
                Bo.append(Bob)
            else:
                Bo.append(Bob * (e ** (-c_o[i] * (P[i] - Pb))))
        data = [P, Bo]
        return data

class Pb:
    def vasquez_beggs(self, input_data):
        """
        Persamaan Vasquez-Beggs untuk bubble point pressure.
        Parameter input: Rs (scf/STB), gas_SG, T(degF), oil_API, T_sep (degF), dan P_sep (psia).
        Output Pb (psia)
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_sep = input_data['P_sep']

        T_res += 460  # Konversi Fahrenheit ke Rankine
        T_sep = T_sep + 460

        if oil_API <= 30:
            C1 = 27.624
            C2 = 0.914328
            C3 = 11.172
        else:
            C1 = 56.18
            C2 = 0.84246
            C3 = 10.393

        gs_SG = gas_SG * (1 + (5.912 * (10 ** -5) * oil_API * (T_sep - 460) * log10(P_sep / 114.7)))

        a = -C3 * oil_API / T_res
        Pb = ((C1 * Rsb / gs_SG) * (10 ** a)) ** C2

        return Pb

    def glaso(self, input_data):
        """
        Mencari nilai bubble point pressure dengan persamaan Glaso.
        Membutuhkan parameter Rsb (scf/STB), gas_SG, T (degF), oil_API (degAPI).
        Output Pb (psia)
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']

        a = 0.816
        b = 0.172
        c = -0.989

        Pb_star = ((Rsb / gas_SG) ** a) * (T_res ** b) * (oil_API ** c)
        Pb = 10 ** (1.7669 + 1.7447 * log10(Pb_star) - 0.30218 * (log10(Pb_star) ** 2))
        return Pb

    def marhoun(self, input_data):
        """
        Mencari nilai bubble point pressure dengan persamaan Marhoun.
        Membutuhkan parameter Rs (scf/STB), gas_SG, T (degF), oil_SG atau oil_API (tergantung kebutuhan).
        By default, Mahroun pakai oil_SG dan T dalam Rankine.
        Fungsi ini mengubah satuannya secara otomatis.
        Output Pb (psia)
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']

        oil_SG = 141.5 / (131.5 + oil_API)
        T_res += 460  # Konversi Fahrenheit ke Rankine
        a = 5.38088 * (10 ** (-3))
        b = 0.715082
        c = -1.87784
        d = 3.1437
        e = 1.32657
        Pb = a * (Rsb ** b) * (gas_SG ** c) * (oil_SG ** d) * (T_res ** e)
        return Pb

    def petroky_fahrshad(self, input_data):
        """
        Persamaan Petroky-Fahrshad untuk bubble point pressure.
        Parameter input: Rs (scf/STB), gas_SG, T(degF), oil_API.
        Output Pb (psia)
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']

        T_res += 460  # Konversi Fahrenheit ke Rankine
        x = (7.916 * (10 ** -4) * (oil_API ** 1.5410)) - (4.561 * (10 ** -5) * ((T_res - 460) ** 1.3911))
        Pb = ((112.727 * (Rsb ** 0.577421)) / ((gas_SG ** 0.8439) * (10 ** x))) - 1391.051
        return Pb

class Rs:

    def vasquez_beggs(self, input_data, Pb):
        """
        Menghitung gas solubility.
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_sep = input_data['P_sep']
        P_res = input_data['P_res']
        P_step = input_data['P_step']

        T_sep += 460
        T_res += 460

        if oil_API <= 30:
            C1 = 0.0362
            C2 = 1.0937
            C3 = 25.7240
        else:
            C1 = 0.0178
            C2 = 1.1870
            C3 = 23.931

        gs_SG = gas_SG * (1 + (5.912 * (10 ** -5) * oil_API * (T_sep - 460) * log10(P_sep / 114.7)))
        if P_res <= Pb:
            P_res = Pb + 3000

        P = array_P(P_atm=14.7, step=P_step, P_res=P_res, Pb=Pb)

        Rs = []
        for j in P:
            if j < Pb:
                Rs.append(C1 * gs_SG * (j ** C2) * e ** (C3 * oil_API / T_res))
            else:
                Rs.append(Rsb)

        data = [P, Rs]
        return data

    def glaso(self, input_data, Pb):
        """
        Menghitung gas solubility
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_res = input_data['P_res']
        P_step = input_data['P_step']
        T_sep += 460
        T_res += 460

        P = array_P(P_atm=14.7, P_res=P_res, step=P_step, Pb=Pb)
        Rs = []
        for i in P:
            if i<Pb:
                x = 2.8869 - (14.1811 - 3.3093*log10(i))**0.5
                Pb_star = 10**x
                Rs.append(gas_SG*(((oil_API**0.989)/((T_res-460)**0.172))*Pb_star)**1.2255)
            else:
                Rs.append(Rsb)
        data = [P, Rs]
        return data

    def petroky_fahrshad(self, input_data, Pb):
        """
        Gas solubility.
        :param input_data:
        :param Pb:
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_res = input_data['P_res']
        P_step = input_data['P_step']

        T_res += 460
        T_sep += 460

        P = array_P(P_atm=14.7, P_res=P_res, step=P_step, Pb=Pb)
        Rs = []
        x = 7.916*(10**(-4))*(oil_API**1.5410) - (4.561*(10**(-5))*(T_res-460)**1.3911)

        for i in P:
            if i<Pb:
                Rs.append((((i/112.727)+12.340)*(gas_SG**0.8439)*(10**x))**1.73184)
            else:
                Rs.append(Rsb)
        data = [P, Rs]
        return data

    def marhoun(self, input_data, Pb):
        """
        Gas solubility.
        :param input_data:
        :param Pb:
        :return:
        """
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_res = input_data['P_res']
        P_step = input_data['P_step']

        T_res += 460
        T_sep += 460
        oil_SG = 141.5/(131.5+oil_API)

        P = array_P(P_atm=14.7, P_res=P_res, step=P_step, Pb=Pb)
        Rs = []
        a = 185.843208
        b = 1.877840
        c = -3.1437
        d = -1.32657
        e_marh = 1.398441
        for i in P:
            if i<Pb:
                Rs.append((a*(gas_SG**b)*(oil_SG**c)*(T_res**d)*i)**e_marh)
            else:
                Rs.append(Rsb)
        data = [P, Rs]
        return data

class viscosity():
    def vasquez_beggs_robinson(self, input_data, Rs_array, Pb):
        """
        Note. Fungsi ini mencari dead oil, saturated, dan undersaturated
        oil viscosity sekaligus. Untuk dead oil, fungsi ini menggunakan
        korelasi Beggs-Robinson. Untuk saturated, menggunakan Beggs-Robinson.
        Untuk undersaturated, menggunakan Vasquez-Beggs.
        :return:
        """
        oil_API = input_data['oil_API']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']

        T_res += 460
        def dead_oil(oil_API=oil_API, T_res=T_res):
            """
            Beggs-Robinson. At surface pressure (14.7 psia) and NO GAS IN SOLUTION
            If there is gas, then use before_saturated_oil
            :return:
            """
            Z = 3.0324-0.02023*oil_API
            Y = 10**Z
            X = Y*(T_res-460)**(-1.163)
            mu_od = (10**X)-1
            return mu_od

        def before_saturated_oil(Rs_at_P):
            """
            Beggs-Robinson. At Bubble Point. Need Rs information at custom P.
            Menghitung per P. Jadi nanti silakan ulangi sendiri.
            :return:
            """
            a = 10.715*(Rs_at_P + 100)**(-0.515)
            b = 5.44*(Rs_at_P + 150)**(-0.338)
            mu_ob = a*(dead_oil()**b)
            return mu_ob

        def at_saturated_oil(Rsb=Rsb):
            a = 10.715 * (Rsb + 100) ** (-0.515)
            b = 5.44 * (Rsb + 150) ** (-0.338)
            mu_ob = a * (dead_oil() ** b)
            return mu_ob

        def undersaturated_oil(P, Pb=Pb, Rsb=Rsb):
            """
            Vasquez-Beggs. Above Bubble Point Pressure. At custom P
            :return:
            """
            a = -3.9*(10**(-5))*P - 5
            m = 2.6*(P**1.187)*(10**a)
            mu_o = at_saturated_oil()*((P/Pb)**m)
            return mu_o

        # Saatnya gabungkan ketiganya.
        # Ketika P = 14.7, pakai dead oil
        # Ketika 14.7 < P <= Pb, pakai saturated oil
        # Ketika P > Pb, pakai undersaturated oil

        P = Rs_array[0]
        Rs = Rs_array[1]
        mu = []
        for i in range(len(P)):
            if P[i] < Pb:
                mu.append(before_saturated_oil(Rs[i]))
            elif P[i] == Pb:
                mu.append(at_saturated_oil())
            else:
                mu.append(undersaturated_oil(P=P[i]))

        data = [P, mu]
        return data

class isothermal_compressibility():
    """
    Menghitung isothermal compressibility
    di bawah Pb maupun di atas Pb
    """
    def vasquez_beggs(self, input_data, Pb, Rs_array):
        """
        Vasquez-Beggs untuk c_o
        :return:
        """
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        oil_API = input_data['oil_API']
        T_sep = input_data['T_sep']
        P_sep = input_data['P_sep']
        gas_SG = input_data['gas_SG']
        P_step = input_data['P_step']
        P_res = input_data['P_res']

        T_sep += 460
        T_res += 460

        gs_SG = gas_SG * (1 + (5.912 * (10 ** -5) * oil_API * (T_sep - 460) * log10(P_sep / 114.7)))

        P = array_P(P_atm=14.7, step=P_step, P_res=P_res, Pb=Pb)
        Rsp = Rs_array[1]

        c_o = []

        for i in range(len(P)):
            if P[i]<=Pb:
                # Ini dicomment karena ragu pakai yg ini atau yg setelahnya
                # Ini digunakan jika tahu Pb
                # Sedangkan tidak ada data lapangan untuk Pb (hanya korelasi)
                # A = -7.573 - 1.45*ln(P[i]) - 0.383*ln(Pb) + 1.402*ln(T_res) + 0.256*ln(oil_API) + 0.449*ln(Rsb)
                A = -7.633 - 1.497*ln(P[i]) + 1.115*ln(T_res) + 0.533*ln(oil_API) + 0.184*ln(Rsp[i])
                # Kalau yang atas ini jika tidak tahu nilai Pb (butuh nilai Rsp)
                c_o.append(e**(A))
            else:
                c_o.append((-1433 + 5*Rsb + 17.2*(T_res-460) - 1180*gs_SG + 12.61*oil_API)/((10**5)*P[i]))
        data = [P, c_o]
        return data

    def petroky_fahrshad(self, input_data, Pb, Rs_array):
        """
        Petroky-Fahrshad untuk c_o
        :return:
        """
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        oil_API = input_data['oil_API']
        T_sep = input_data['T_sep']
        P_sep = input_data['P_sep']
        gas_SG = input_data['gas_SG']
        P_step = input_data['P_step']
        P_res = input_data['P_res']

        T_sep += 460
        T_res += 460

        P = array_P(P_atm=14.7, step=P_step, P_res=P_res, Pb=Pb)
        Rsp = Rs_array[1]
        c_o = []

        for i in range(len(P)):
            if P[i]<=Pb:
                A = -7.633 - 1.497 * ln(P[i]) + 1.115 * ln(T_res) + 0.533 * ln(oil_API) + 0.184 * ln(Rsp[i])
                c_o.append(e**A)
            else:
                c_o.append(1.705*(10**-7)*(Rsb**0.69357)*(gas_SG**0.1885)*(oil_API**0.3272)*((T_res-460)**0.6729)*(P[i]**-0.5906))
        data = [P, c_o]

        return data