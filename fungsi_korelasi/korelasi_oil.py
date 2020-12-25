from math import e, pi
from math import log10
from math import log as ln

class Pb:
    def vasquez_beggs(self, Rsb, gas_SG, T_res, oil_API, T_sep, P_sep):
        """
        Persamaan Vasquez-Beggs untuk bubble point pressure.
        Parameter input: Rs (scf/STB), gas_SG, T(degF), oil_API, T_sep (degF), dan P_sep (psia).
        Output Pb (psia)
        """

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

    def glaso(self, Rsb, gas_SG, T_res, oil_API):
        """
        Mencari nilai bubble point pressure dengan persamaan Glaso.
        Membutuhkan parameter Rsb (scf/STB), gas_SG, T (degF), oil_API (degAPI).
        Output Pb (psia)
        """
        a = 0.816
        b = 0.172
        c = -0.989

        Pb_star = ((Rsb / gas_SG) ** a) * (T_res ** b) * (oil_API ** c)
        Pb = 10 ** (1.7669 + 1.7447 * log10(Pb_star) - 0.30218 * (log10(Pb_star) ** 2))
        return Pb

    def mahroun(self, Rsb, gas_SG, T_res, oil_API):
        """
        Mencari nilai bubble point pressure dengan persamaan Mahroun.
        Membutuhkan parameter Rs (scf/STB), gas_SG, T (degF), oil_SG atau oil_API (tergantung kebutuhan).
        By default, Mahroun pakai oil_SG dan T dalam Rankine.
        Fungsi ini mengubah satuannya secara otomatis.
        Output Pb (psia)
        """
        oil_SG = 141.5 / (131.5 + oil_API)
        T_res += 460  # Konversi Fahrenheit ke Rankine
        a = 5.38088 * (10 ** (-3))
        b = 0.715082
        c = -1.87784
        d = 3.1437
        e = 1.32657
        Pb = a * (Rsb ** b) * (gas_SG ** c) * (oil_SG ** d) * (T_res ** e)
        return Pb

    def petroky_fahrshad(self, Rsb, gas_SG, T_res, oil_API):
        """
        Persamaan Petroky-Fahrshad untuk bubble point pressure.
        Parameter input: Rs (scf/STB), gas_SG, T(degF), oil_API.
        Output Pb (psia)
        """
        T_res += 460  # Konversi Fahrenheit ke Rankine
        x = (7.916 * (10 ** -4) * (oil_API ** 1.5410)) - (4.561 * (10 ** -5) * ((T_res - 460) ** 1.3911))
        Pb = ((112.727 * (Rsb ** 0.577421)) / ((gas_SG ** 0.8439) * (10 ** x))) - 1391.051
        return Pb

class Rs:

    def vasquez_beggs(self, oil_API, T_sep, P_sep, gas_SG, P_res, Pb, T_res, Rsb):
        """
        Menghitung gas solubility.
        :return:
        """
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

        P = [14.7]
        for i in range(15, P_res):
            P.append(i)

        Rs = []
        for j in P:
            if j < Pb:
                Rs.append(C1 * gs_SG * (j ** C2) * e ** (C3 * oil_API / T_res))
            else:
                Rs.append(Rsb)

        data = [P, Rs]
        return data

    def glaso(self):
        pass

    def petroky_fahrshad_mahroun(self):
        pass

class viscosity():
    def vasquez_beggs_robinson(self, oil_API, T_res, Rs_array, Pb, P_res, Rsb):
        """
        Note. Fungsi ini mencari dead oil, saturated, dan undersaturated
        oil viscosity sekaligus. Untuk dead oil, fungsi ini menggunakan
        korelasi Beggs-Robinson. Untuk saturated, menggunakan Beggs-Robinson.
        Untuk undersaturated, menggunakan Vasquez-Beggs.
        :return:
        """
        T_res += 460
        def dead_oil(oil_API=oil_API, T_res=T_res):
            """
            Beggs-Robinson. At surface pressure (14.7 psia)
            :return:
            """
            Z = 3.0324-0.02023*oil_API
            Y = 10**Z
            X = Y*(T_res-460)**(-1.163)
            mu_od = (10**X)-1
            return mu_od

        def saturated_oil(Rs_at_P):
            """
            Beggs-Robinson. At Bubble Point. Need Rs information at custom P.
            Menghitung per P. Jadi nanti silakan ulangi sendiri.
            :return:
            """
            a = 10.715*(Rs_at_P + 100)**(-0.515)
            b = 5.44*(Rs_at_P + 150)**(-0.338)
            mu_ob = a*(dead_oil()**b)
            return mu_ob

        def undersaturated_oil(P, Pb=Pb, Rsb=Rsb):
            """
            Vasquez-Beggs. Above Bubble Point Pressure. At custom P
            :return:
            """
            a = -3.9*(10**(-5))*P - 5
            m = 2.6*(P**1.187)*(10**a)
            mu_o = saturated_oil(Rs_at_P=Rsb)*((P/Pb)**m)
            return mu_o

        # Saatnya gabungkan ketiganya.
        # Ketika P = 14.7, pakai dead oil
        # Ketika 14.7 < P <= Pb, pakai saturated oil
        # Ketika P > Pb, pakai undersaturated oil

        P = Rs_array[0]
        Rs = Rs_array[1]
        mu = []
        for i in range(len(P)):
            if P[i] == 14.7:
                mu.append(dead_oil())
            elif P[i] <= Pb:
                mu.append(saturated_oil(Rs[i]))
            else:
                mu.append(undersaturated_oil(P=P[i]))

        data = [P, mu]
        return data