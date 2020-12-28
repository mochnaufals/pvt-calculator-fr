# Ngulang gara2 filenya overwrite
# Rule of Thumb Korelasi: PASTIKAN ADA BUBBLE POINT PRESSURE PADA ARRAY!

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
from guikorelasi import Ui_MainWindow
from gui_plot import Ui_PlotWindow
from gui_about import Ui_AboutUsDialog
import resgui_rc
import sys
import random
import xlsxwriter
from math import sin, e, pi, erf, ceil
from fungsi_korelasi import korelasi_oil
import os, json, hashlib

oil_Rs = korelasi_oil.Rs()
oil_Pb = korelasi_oil.Pb()
oil_visc = korelasi_oil.viscosity()
oil_Bo = korelasi_oil.Bo()
oil_IC = korelasi_oil.isothermal_compressibility()
oil_Bt = korelasi_oil.Bt()
oil_rho = korelasi_oil.density()

# Sepertinya butuh konvensi array atau dictionary agar mudah oper variabel
# Input data:
# 1. Measured GOR/Rsb (scf/STB)
# 2. Gas SG (Fraction)
# 3. Oil Gravity (API)
# 4. Reservoir Temperature (F)
# 5. Separator Temperature (F)
# 6. Separator Pressure (psig) jangan lupa ubah ke psia
# 7. Pressure step

def bulat_atas_ribuan(angka):
    hasil = int(ceil(angka/1000.0))*1000
    return hasil

def bulat_atas_ratusan(angka):
    hasil = int(ceil(angka/100.0))*100
    return hasil

def transpose(matrix):
    matrix_new = []
    for i in range(len(matrix[0])):
        matrix_new.append([])
        matrix_new[i].append(matrix[0][i])
        matrix_new[i].append(matrix[1][i])
    return matrix_new

class grafik():
    def density(self, input_data, windowed=False):
        global density_oil
        global rho_at_Pb

        data, rho_at_Pb = oil_rho.by_definition(input_data, bubble_P, Rs_array, Bo_array, IC_array)

        density_oil = data

        data_new = transpose(data)
        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Oil Density')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(min(data[1])-0.5, max(data[1])+0.5)
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(lb/cf)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Bt(self, input_data, korelasi='gla', windowed=False):
        if korelasi == 'gla':
            data = oil_Bt.glaso(input_data, Rs_array, Bo_array, bubble_P)
        else:
            data = oil_Bt.marhoun(input_data, Rs_array, Bo_array, bubble_P)

        # Untuk dimasukkan ke tabel
        global Bt_array
        Bt_array = data

        data_new = transpose(data)
        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Total Formation Volume Factor (Bt)')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(0, max(data[1]))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(bbl/STB)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview


    def IC(self, input_data, Pb, korelasi='vas', windowed=False):
        if korelasi == 'vas':
            data = oil_IC.vasquez_beggs(input_data, Pb, Rs_array=Rs_array)
        else:
            data = oil_IC.petroky_fahrshad(input_data, Pb, Rs_array=Rs_array)

        # Jadikan global IC agar bisa dipakai Bo
        global IC_array
        IC_array = data

        # Lanjutkan perhitungan biasa
        data_new = transpose(data)
        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Isothermal Compressibility')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(0, max(data[1])/10)
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(1/psi)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Bo(self, input_data, korelasi='gla', windowed='False'):
        global Bo_bubble_point

        if korelasi == 'gla':
            data, Bo_bubble_point = oil_Bo.glaso(input_data, Rs_array, IC_array, bubble_P)
        elif korelasi == 'mar':
            data, Bo_bubble_point = oil_Bo.marhoun(input_data, Rs_array, IC_array, bubble_P)
        else:
            data, Bo_bubble_point = oil_Bo.petroky_fahrshad(input_data, Rs_array, IC_array, bubble_P)

        global Bo_array
        Bo_array = data

        data_new = transpose(data)
        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Oil Formation Volume Factor (Bo)')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(min(data[1])-0.1, max(data[1])+0.1)
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(bbl/STB)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def viscosity(self, input_data, Pb, korelasi='vas', windowed=False):
        if korelasi == 'vas':
            data = oil_visc.vasquez_beggs_robinson(input_data, Rs_array, Pb)

        global visc_array
        visc_array = data

        data_new = transpose(data)

        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        # chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Viscosity')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(0, max(data[1]))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(cP)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Rs(self, input_data, Pb, windowed=False, korelasi='vas'):
        global Rs_array

        if korelasi == 'vas':
            data = oil_Rs.vasquez_beggs(input_data, Pb)
            Rs_array = data
        elif korelasi == 'gla':
            data = oil_Rs.glaso(input_data, Pb)
            Rs_array = data
        elif korelasi == 'pet':
            data = oil_Rs.petroky_fahrshad(input_data, Pb)
            Rs_array = data
        else:
            data = oil_Rs.marhoun(input_data, Pb)
            Rs_array = data

        data_new = transpose(data)

        series = QLineSeries()
        for i in data_new:
            series.append(i[0], i[1])

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #chart.setAnimationEasingCurve(qtc.QEasingCurve.InSine)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Gas Solubility (Rs)')
            title_font = qtg.QFont()
            title_font.setBold(True)
            title_font.setPixelSize(18)
            chart.setTitleFont(title_font)
            label_font.setPixelSize(14)
            label_font.setBold(False)
        else:
            label_font.setPixelSize(10)
            label_font.setBold(False)

        axis_X = QValueAxis()
        axis_X.setRange(0, bulat_atas_ribuan(max(data[0])))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Pressure (psia)')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(0, bulat_atas_ratusan(max(data[1])))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('(scf/STB)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

class SecondWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_PlotWindow()
        self.ui.setupUi(self)
        # Kode plot window
        #self.setWindowTitle('Fluid Properties Calculator - {}'.format(nama_window))
        #self.ui.LayGraph.addWidget(chart_widget)

class WarningWindow(qtw.QMessageBox):
    def __init__(self):
        super(WarningWindow, self).__init__()
        icon = qtg.QIcon()
        icon.addPixmap(qtg.QPixmap(":/icon/oil-barrel.svg"), qtg.QIcon.Normal, qtg.QIcon.Off)
        self.setWindowIcon(icon)
        self.setIcon(qtw.QMessageBox.Warning)
        self.setText('Input fields cannot be empty!')
        self.setWindowTitle('Warning Message')
        self.setStandardButtons(qtw.QMessageBox.Ok)

class AboutWindow(qtw.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.ui = Ui_AboutUsDialog()
        self.ui.setupUi(self)

class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code will go here
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Enable the first tab only
        self.ui.MainPage.setTabEnabled(0, True)
        self.ui.MainPage.setTabEnabled(1, False)
        self.ui.MainPage.setTabEnabled(2, False)
        self.ui.MainPage.setTabEnabled(3, False)

        # Set Validator for fluid data input (only numbers)
        self.ui.measuredGORScfSTBLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.gasSpecificGravityFractionLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.oilGravityAPILineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.reservoirTemperatureFLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.reservoirPressurePsiaLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.separatorTemperatureFLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.separatorPressurePsigLineEdit.setValidator(qtg.QDoubleValidator())
        self.ui.pressureStepLineEdit.setValidator(qtg.QIntValidator())

        # Make sure that the input changes will disable the plot and table tab
        self.detectAllInputChanges()

        # Make instance of new windows
        self.dialogAbout = AboutWindow()
        self.dialogBo = SecondWindow()
        self.dialogRs = SecondWindow()
        self.dialogVisc = SecondWindow()
        self.dialogIC = SecondWindow()
        self.dialogRho = SecondWindow()
        self.dialogWarning = WarningWindow()

        # New Navigation buttons on first page
        self.ui.ButtonNextInput.clicked.connect(self.toTabCorr)

        # Plot on new window
        self.ui.viewBoButton.clicked.connect(self.BoWindow)
        self.ui.viewRsButton.clicked.connect(self.RsWindow)
        self.ui.viewViscButton.clicked.connect(self.ViscWindow)
        self.ui.viewICButton.clicked.connect(self.ICWindow)
        self.ui.viewRhoButton.clicked.connect(self.RhoWindow)


        # Input user information
        self.inputInformasiUser()

        # Navigation on tab 2
        self.ui.buttonCalcNext.clicked.connect(self.inputFluidData)
        self.ui.buttonCalcNext.clicked.connect(self.inputPilihanKorelasi)
        self.ui.buttonCalcNext.clicked.connect(self.calculateAndViewAllPlot)
        self.ui.actionAbout_Us.triggered.connect(self.openAboutWindow)

        # Navigation to tab table
        self.ui.viewTableOutputButton.clicked.connect(self.bukaTabTable)

        # Highlight Pb Row at table
        self.ui.goToPbButton.clicked.connect(self.highlightRowPb)

        # Export table to excel
        self.ui.exportDataButton.clicked.connect(self.exportTableToExcel)

        # Save config file
        self.ui.actionSave_As.triggered.connect(self.saveConfigAs)
        self.ui.actionSave_Config.triggered.connect(self.saveConfig)

        # Open config file
        self.ui.actionOpen_Config.triggered.connect(self.openConfig)

        # Your code will end here
        self.showMaximized()


    def detectAllInputChanges(self):
        def lakukan(what):
            def matikan():
                self.ui.MainPage.setTabEnabled(2, False)
                self.ui.MainPage.setTabEnabled(3, False)
            what.textEdited.connect(matikan)

        su = self.ui
        lakukan(su.measuredGORScfSTBLineEdit)
        lakukan(su.gasSpecificGravityFractionLineEdit)
        lakukan(su.oilGravityAPILineEdit)
        lakukan(su.reservoirTemperatureFLineEdit)
        lakukan(su.reservoirPressurePsiaLineEdit)
        lakukan(su.separatorTemperatureFLineEdit)
        lakukan(su.separatorPressurePsigLineEdit)
        lakukan(su.pressureStepLineEdit)

        def bagianDua(masuk):
            def coba(what):
                try:
                    def anu():
                        self.ui.MainPage.setTabEnabled(2, False)
                        self.ui.MainPage.setTabEnabled(3, False)
                    what.pressed.connect(anu)
                except:
                    pass
            for i in masuk.children():
                coba(i)

        bagianDua(su.groupCorPb)
        bagianDua(su.groupCorBo)
        bagianDua(su.groupCorRs)
        bagianDua(su.groupCorIC)

    def toTabCorr(self):
        def cekPanjang(what, what2):
            panjang = 1
            for i in what.children():
                try:
                    panjang *= len(i.text())
                except:
                    pass
            for i in what2.children():
                try:
                    panjang *= len(i.text())
                except:
                    pass
            if panjang == 0:
                self.dialogWarning.show()
            else:
                self.ui.MainPage.setTabEnabled(1, True)
                self.ui.MainPage.setCurrentIndex(1)
        cekPanjang(self.ui.groupBoxInputData, self.ui.groupBoxUserData)

    def openAboutWindow(self):
        self.dialogAbout.show()

    def inputPilihanKorelasi(self):
        if self.ui.radioPbGlaso.isChecked() == True:
            Pb = 'gla'
        elif self.ui.radioPbMarhoun.isChecked() == True:
            Pb = 'mar'
        elif self.ui.radioPbPetroky.isChecked() == True:
            Pb = 'pet'
        else:
            Pb = 'vas'
        if self.ui.radioBoGlaso.isChecked() == True:
            Bo = 'gla'
        elif self.ui.radioBoMarhoun.isChecked() == True:
            Bo = 'mar'
        else:
            Bo = 'pet'
        if self.ui.radioRsGlaso.isChecked() == True:
            Rs = 'gla'
        elif self.ui.radioRsPetroky.isChecked() == True:
            Rs = 'pet'
        elif self.ui.radioRsMarhoun.isChecked() == True:
            Rs = 'mar'
        else:
            Rs = 'vas'
        if self.ui.radioViscVasquezBeggsRobinson.isChecked() == True:
            visc = 'vas'
        if self.ui.radioICVasquez.isChecked() == True:
            IC = 'vas'
        else:
            IC = 'pet'
        global input_pilihan_korelasi
        input_pilihan_korelasi = {
            'Pb': Pb,
            'Bo': Bo,
            'Rs': Rs,
            'visc': visc,
            'IC': IC
        }

    def calculateAndViewAllPlot(self):
        self.ui.MainPage.setTabEnabled(2, True)
        input_data = input_fluid_data
        oil_API = input_data['oil_API']
        gas_SG = input_data['gas_SG']
        Rsb = input_data['Rsb']
        T_res = input_data['T_res']
        T_sep = input_data['T_sep']
        P_sep = input_data['P_sep']
        P_res = input_data['P_res']
        P_step = input_data['P_step']

        corr = input_pilihan_korelasi

        # Penentuan Pb di sini
        if corr['Pb'] == 'vas':
            Pb = oil_Pb.vasquez_beggs(input_data)
        elif corr['Pb'] == 'gla':
            Pb = oil_Pb.glaso(input_data)
        elif corr['Pb'] == 'mar':
            Pb = oil_Pb.marhoun(input_data)
        else:
            Pb = oil_Pb.petroky_fahrshad(input_data)
        global bubble_P
        bubble_P = Pb
        self.ui.PbLineEdit.clear()
        self.ui.PbLineEdit.setText(str(bubble_P))

        # Kemudian penentuan parameter yang lain

        # Gas Solubility
        if self.ui.RsLayout.isEmpty() == True:
            self.ui.RsLayout.addWidget(grafik.Rs(self, input_data=input_data, Pb=Pb,
                                                 korelasi=corr['Rs'], windowed=False))
        else:
            for i in reversed(range(self.ui.RsLayout.count())):
                self.ui.RsLayout.itemAt(i).widget().setParent(None)
            self.ui.RsLayout.addWidget(grafik.Rs(self, input_data=input_data, Pb=Pb,
                                                 korelasi=corr['Rs'], windowed=False))

        # Viscosity
        if self.ui.ViscLayout.isEmpty() == True:
            self.ui.ViscLayout.addWidget(grafik.viscosity(self, input_data=input_data, Pb=Pb,
                                                          korelasi=corr['visc'], windowed=False))
        else:
            for i in reversed(range(self.ui.ViscLayout.count())):
                self.ui.ViscLayout.itemAt(i).widget().setParent(None)
            self.ui.ViscLayout.addWidget(grafik.viscosity(self, input_data=input_data, Pb=Pb,
                                                          korelasi=corr['visc'], windowed=False))

        # Isothermal Compressibility (c_o)
        # c_o harus dijalankan sebelum Bo, karena butuh informasi IC_array
        if self.ui.ICLayout.isEmpty() == True:
            self.ui.ICLayout.addWidget(grafik.IC(self, input_data, Pb, korelasi=corr['IC']))
        else:
            for i in reversed(range(self.ui.ICLayout.count())):
                self.ui.ICLayout.itemAt(i).widget().setParent(None)
            self.ui.ICLayout.addWidget(grafik.IC(self, input_data, Pb, korelasi=corr['IC']))

        # Oil Formation Volume Factor (Bo)
        if self.ui.BoLayout.isEmpty() == True:
            self.ui.BoLayout.addWidget(grafik.Bo(self, input_data, korelasi=corr['Bo']))
        else:
            for i in reversed(range(self.ui.BoLayout.count())):
                self.ui.BoLayout.itemAt(i).widget().setParent(None)
            self.ui.BoLayout.addWidget(grafik.Bo(self, input_data, korelasi=corr['Bo']))

        # Oil FVF at Pb (Bob)
        self.ui.BobLineEdit.clear()
        self.ui.BobLineEdit.setText(str(Bo_bubble_point))

        # Total Formation Volume Factor (Bt)
        #if self.ui.BtLayout.isEmpty() == True:
        #    self.ui.BtLayout.addWidget(grafik.Bt(self, input_data, korelasi=corr['Bt']))
        #else:
        #    for i in reversed(range(self.ui.BtLayout.count())):
        #        self.ui.BtLayout.itemAt(i).widget().setParent(None)
        #    self.ui.BtLayout.addWidget(grafik.Bt(self, input_data, korelasi=corr['Bt']))

        # Oil Density
        if self.ui.RhoLayout.isEmpty() == True:
            self.ui.RhoLayout.addWidget(grafik.density(self, input_data))
        else:
            for i in reversed(range(self.ui.RhoLayout.count())):
                self.ui.RhoLayout.itemAt(i).widget().setParent(None)
            self.ui.RhoLayout.addWidget(grafik.density(self, input_data))

        # Oil Density at Pb
        self.ui.RhoPbLineEdit.clear()
        self.ui.RhoPbLineEdit.setText(str(rho_at_Pb))

        # Output data to table
        self.outputDataToTable()

        # Open Plot Tab
        self.ui.MainPage.setCurrentIndex(2)

        # Enable Table Tab (uji coba)
        self.ui.MainPage.setTabEnabled(3, True)

    def inputFluidData(self):
        def convert_to_number(masuk):
            if ceil(float(masuk)) == float(masuk):
                hasil = ceil(float(masuk))
            else:
                hasil = float(masuk)
            return hasil
        Rsb = convert_to_number(self.ui.measuredGORScfSTBLineEdit.text())
        gas_SG = convert_to_number(self.ui.gasSpecificGravityFractionLineEdit.text())
        oil_API = convert_to_number(self.ui.oilGravityAPILineEdit.text())
        T_res = convert_to_number(self.ui.reservoirTemperatureFLineEdit.text())
        T_sep = convert_to_number(self.ui.separatorTemperatureFLineEdit.text())
        P_res = convert_to_number(self.ui.reservoirPressurePsiaLineEdit.text())
        P_sep = convert_to_number(self.ui.separatorPressurePsigLineEdit.text()) + 14.7
        P_step = convert_to_number(self.ui.pressureStepLineEdit.text())

        global input_fluid_data
        input_fluid_data = {
            'Rsb': Rsb,
            'gas_SG': gas_SG,
            'oil_API': oil_API,
            'T_res': T_res,
            'T_sep': T_sep,
            'P_res': P_res,
            'P_sep': P_sep,
            'P_step': P_step
        }

    def inputInformasiUser(self):
        def ubah():
            self.ui.labelUserName.setText(self.ui.userNameLineEdit.text())
            self.ui.labelCompany.setText(self.ui.companyLineEdit.text())
            self.ui.labelField.setText(self.ui.fieldLineEdit.text())
            self.ui.labelWell.setText(self.ui.wellLineEdit.text())
            self.ui.labelReservoir.setText(self.ui.reservoirLineEdit.text())
            self.ui.labelUserID.setText(self.ui.userIDLineEdit.text())
        self.ui.userNameLineEdit.textChanged.connect(ubah)
        self.ui.companyLineEdit.textChanged.connect(ubah)
        self.ui.fieldLineEdit.textChanged.connect(ubah)
        self.ui.wellLineEdit.textChanged.connect(ubah)
        self.ui.reservoirLineEdit.textChanged.connect(ubah)
        self.ui.userIDLineEdit.textChanged.connect(ubah)

    def cekNextPrevTab(self):
        '''
        Masih susah pakai ini, nanti aja dulu
        :return:
        '''
        index_cek = self.ui.MainPage.currentIndex()


        if index_cek == 0:
            self.ui.ButtonNext.setEnabled(True)
            self.ui.ButtonPrev.setDisabled(True)
        elif index_cek == 3:
            self.ui.ButtonNext.setDisabled(True)
            self.ui.ButtonNext.setDisabled(True)
        else:
            self.ui.ButtonNext.setDisabled(True)
            self.ui.ButtonPrev.setEnabled(True)

    def ViscWindow(self):
        if self.dialogVisc.ui.LayGraph.isEmpty() == True:
            self.dialogVisc.ui.LayGraph.addWidget(grafik.viscosity(self,
                                                                   input_data=input_fluid_data,
                                                                   Pb=bubble_P,
                                                                   korelasi=input_pilihan_korelasi['visc'],
                                                                   windowed=True))
        else:
            for i in reversed(range(self.dialogVisc.ui.LayGraph.count())):
                self.dialogVisc.ui.LayGraph.itemAt(i).widget().setParent(None)
            self.dialogVisc.ui.LayGraph.addWidget(grafik.viscosity(self,
                                                                   input_data=input_fluid_data,
                                                                   Pb=bubble_P,
                                                                   korelasi=input_pilihan_korelasi['visc'],
                                                                   windowed=True))

        self.dialogVisc.setWindowTitle('View Plot: Viscosity')
        self.dialogVisc.show()

    def RsWindow(self):
        if self.dialogRs.ui.LayGraph.isEmpty() == True:
            self.dialogRs.ui.LayGraph.addWidget(grafik.Rs(self,
                                                          input_data=input_fluid_data,
                                                          Pb=bubble_P,
                                                          korelasi=input_pilihan_korelasi['Rs'],
                                                          windowed=True))
        else:
            for i in reversed(range(self.dialogRs.ui.LayGraph.count())):
                self.dialogRs.ui.LayGraph.itemAt(i).widget().setParent(None)
            self.dialogRs.ui.LayGraph.addWidget(grafik.Rs(self,
                                                          input_data=input_fluid_data,
                                                          Pb=bubble_P,
                                                          korelasi=input_pilihan_korelasi['Rs'],
                                                          windowed=True))

        self.dialogRs.setWindowTitle('View Plot: Gas Solubility')
        self.dialogRs.show()

    def BoWindow(self):
        if self.dialogBo.ui.LayGraph.isEmpty() == True:
            self.dialogBo.ui.LayGraph.addWidget(grafik.Bo(self, input_fluid_data,
                                                          korelasi=input_pilihan_korelasi['Bo'], windowed=True))
        else:
            for i in reversed(range(self.dialogBo.ui.LayGraph.count())):
                self.dialogBo.ui.LayGraph.itemAt(i).widget().setParent(None)
            self.dialogBo.ui.LayGraph.addWidget(grafik.Bo(self, input_fluid_data,
                                                          korelasi=input_pilihan_korelasi['Bo'], windowed=True))
        self.dialogBo.setWindowTitle('View Plot: Oil Formation Volume Factor (Bo)')
        self.dialogBo.show()

    def ICWindow(self):
        if self.dialogIC.ui.LayGraph.isEmpty() == True:
            self.dialogIC.ui.LayGraph.addWidget(grafik.IC(self,
                                                          input_fluid_data,
                                                          bubble_P,
                                                          korelasi=input_pilihan_korelasi['IC'],
                                                          windowed=True))
        else:
            for i in reversed(range(self.dialogIC.ui.LayGraph.count())):
                self.dialogIC.ui.LayGraph.itemAt(i).widget().setParent(None)
            self.dialogIC.ui.LayGraph.addWidget(grafik.IC(self,
                                                          input_fluid_data,
                                                          bubble_P,
                                                          korelasi=input_pilihan_korelasi['IC'],
                                                          windowed=True))
        self.dialogIC.setWindowTitle('View Plot: Isothermal Compressibility')
        self.dialogIC.show()

    def RhoWindow(self):
        if self.dialogRho.ui.LayGraph.isEmpty() == True:
            self.dialogRho.ui.LayGraph.addWidget(grafik.density(self, input_fluid_data, windowed=True))
        else:
            for i in reversed(range(self.dialogRho.ui.LayGraph.count())):
                self.dialogRho.ui.LayGraph.itemAt(i).widget().setParent(None)
            self.dialogRho.ui.LayGraph.addWidget(grafik.density(self, input_fluid_data, windowed=True))
        self.dialogRho.setWindowTitle('View Plot: Oil Density')
        self.dialogRho.show()

    def bukaTabTable(self):
        self.ui.MainPage.setCurrentIndex(3)

    def exportTableToExcel(self):
        nama = self.ui.userNameLineEdit.text()
        company = self.ui.companyLineEdit.text()
        field = self.ui.fieldLineEdit.text()
        reservoir = self.ui.reservoirLineEdit.text()
        well = self.ui.wellLineEdit.text()
        file_dir, jenis = qtw.QFileDialog.getSaveFileName(self,
                                                          'Save PVT Output Data',
                                                          os.path.expanduser('~/PVT_{}_{}_F{}_R{}_W{}'.format(
                                                              nama, company, field, reservoir, well
                                                          )),
                                                          'Microsoft Excel Workbook (*.xlsx)',)
        try:
            workbook = xlsxwriter.Workbook(file_dir)
            worksheet1 = workbook.add_worksheet('PVT Data')

            data = [['P (psia)', 'Pb (psia)', 'Bo (bbl/STB)', 'Bob (bbl/STB)', 'Density (lb/cf)',
                    'Rho at Pb (lb/cf)', 'Rs (scf/STB)', 'Viscosity (cP)', 'Iso_Comp (1/psi)']]
            for i in range(len(Rs_array[0])):
                data.append([Rs_array[0][i], bubble_P, Bo_array[1][i], Bo_bubble_point,
                               density_oil[1][i], rho_at_Pb, Rs_array[1][i], visc_array[1][i], IC_array[1][i]])

            row = range(len(data))
            col = range(len(data[0]))

            for i in row:
                for j in col:
                    item = data[i][j]
                    worksheet1.write(i, j, item)
            workbook.close()
        except:
            pass

    def outputDataToTable(self):
        """
        Method untuk memasukkan data hasil ke tabel
        Mengumpulkan semua data ke dalam sebuah matriks
        Kemudian data dimasukkan dengan fillTableData
        :return:
        """
        # Cek dulu
        table = self.ui.tableHasil
        matrix_data = []

        self.ui.tableHasil.setRowCount(len(Rs_array[0]))
        for i in range(len(Rs_array[0])):
            matrix_data.append([Rs_array[0][i], bubble_P, Bo_array[1][i], Bo_bubble_point,
                           density_oil[1][i], rho_at_Pb, Rs_array[1][i], visc_array[1][i], IC_array[1][i]])

        global output_table_data
        output_table_data = matrix_data

        self.fillTableData(table, matrix_data)
        header = self.ui.tableHasil.horizontalHeader()
        for i in range(header.count()):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

    def highlightRowPb(self):
        self.ui.tableHasil.selectRow(row_Pb_position)

    def nextTab(self):
        indeks = self.ui.MainPage.currentIndex()
        self.ui.MainPage.setCurrentIndex(indeks+1)

    def prevTab(self):
        indeks = self.ui.MainPage.currentIndex()
        self.ui.MainPage.setCurrentIndex(indeks-1)

    def fillTableData(self, table, matrix_data):
        # THIS FUNCTION IS CONSIDERED AS FASTER THAN addTableRow
        # This function will fill the existing table
        # Please make sure that the empty rows are already been made
        # Including highlighting Pb row
        row = range(0,len(matrix_data), 1)
        col = range(0,len(matrix_data[0]), 1)
        global row_Pb_position
        for i in row:
            for j in col:
                item = matrix_data[i][j]
                cell = qtw.QTableWidgetItem(str(item))
                table.setItem(i, j, cell)
                if matrix_data[i][0] == bubble_P:
                    row_Pb_position = i
                self.ui.progressCalc.setValue(int(i/(len(matrix_data)-1)*100))

    def _saveConfigFile(self, direktori):
        data = {}
        data['user_info'] = {
            'name': self.ui.userNameLineEdit.text(),
            'id': self.ui.userIDLineEdit.text(),
            'company': self.ui.companyLineEdit.text(),
            'field': self.ui.fieldLineEdit.text(),
            'well': self.ui.wellLineEdit.text(),
            'reservoir': self.ui.reservoirLineEdit.text()
        }
        data['fluid_data'] = {
            'Rsb': self.ui.measuredGORScfSTBLineEdit.text(),
            'gas_SG': self.ui.gasSpecificGravityFractionLineEdit.text(),
            'oil_API': self.ui.oilGravityAPILineEdit.text(),
            'T_res': self.ui.reservoirTemperatureFLineEdit.text(),
            'P_res': self.ui.reservoirPressurePsiaLineEdit.text(),
            'T_sep': self.ui.separatorTemperatureFLineEdit.text(),
            'P_sep': self.ui.separatorPressurePsigLineEdit.text(),
            'P_step': self.ui.pressureStepLineEdit.text()
        }
        self.inputPilihanKorelasi()
        data['corr'] = input_pilihan_korelasi

        try:
            with open(direktori, 'w') as outfile:
                json.dump(data, outfile)
        except:
            pass

    def saveConfigAs(self):
        nama = self.ui.userNameLineEdit.text()
        company = self.ui.companyLineEdit.text()
        field = self.ui.fieldLineEdit.text()
        reservoir = self.ui.reservoirLineEdit.text()
        well = self.ui.wellLineEdit.text()
        global file_input_config_dir
        file_input_config_dir, jenis = qtw.QFileDialog.getSaveFileName(self,
                                                          'Save PVT Input Config',
                                                          os.path.expanduser('~/PVTConfig_{}_{}_F{}_R{}_W{}'.format(
                                                              nama, company, field, reservoir, well
                                                          )),
                                                          'PVT Config File (*.pvtc)', )
        self._saveConfigFile(file_input_config_dir)

    def saveConfig(self):
        try:
            self._saveConfigFile(file_input_config_dir)
        except:
            self.saveConfigAs()

    def openConfig(self):
        try:
            try:
                dir_awal = file_input_config_dir
            except:
                dir_awal = os.path.expanduser('~/')
            filedir, jenis = qtw.QFileDialog.getOpenFileName(self,
                                                             'Open PVT Input Config File',
                                                             dir_awal,
                                                             'PVT Config File (*.pvtc)')
            with open(filedir) as json_file:
                data = json.load(json_file)
            user = data['user_info']
            self.ui.userNameLineEdit.setText(user['name'])
            self.ui.userIDLineEdit.setText(user['id'])
            self.ui.companyLineEdit.setText(user['company'])
            self.ui.fieldLineEdit.setText(user['field'])
            self.ui.reservoirLineEdit.setText(user['reservoir'])
            self.ui.wellLineEdit.setText(user['well'])
            fluid = data['fluid_data']
            self.ui.measuredGORScfSTBLineEdit.setText(fluid['Rsb'])
            self.ui.gasSpecificGravityFractionLineEdit.setText(fluid['gas_SG'])
            self.ui.oilGravityAPILineEdit.setText(fluid['oil_API'])
            self.ui.reservoirTemperatureFLineEdit.setText(fluid['T_res'])
            self.ui.reservoirPressurePsiaLabel.setText(fluid['P_res'])
            self.ui.separatorTemperatureFLineEdit.setText(fluid['T_sep'])
            self.ui.separatorPressurePsigLineEdit.setText(fluid['P_sep'])
            self.ui.pressureStepLineEdit.setText(fluid['P_step'])
            corr = data['corr']
            Pb = corr['Pb']
            Bo = corr['Bo']
            Rs = corr['Rs']
            IC = corr['IC']
            visc = corr['visc']
            if Pb == 'vas':
                self.ui.radioPbVasquezBeggs.setChecked(True)
            elif Pb == 'gla':
                self.ui.radioPbGlaso.setChecked(True)
            elif Pb == 'mar':
                self.ui.radioPbMarhoun.setChecked(True)
            else:
                self.ui.radioPbPetroky.setChecked(True)
            if Bo == 'gla':
                self.ui.radioBoGlaso.setChecked(True)
            elif Bo == 'mar':
                self.ui.radioBoMarhoun.setChecked(True)
            else:
                self.ui.radioBoPetroky.setChecked(True)
            if Rs == 'vas':
                self.ui.radioRsVasquez.setChecked(True)
            elif Rs == 'gla':
                self.ui.radioRsGlaso.setChecked(True)
            elif Rs == 'mar':
                self.ui.radioRsMarhoun.setChecked(True)
            else:
                self.ui.radioRsPetroky.setChecked(True)
            if IC == 'vas':
                self.ui.radioICVasquez.setChecked(True)
            else:
                self.ui.radioICPetroky.setChecked(True)
            if visc == 'vas':
                self.ui.radioViscVasquezBeggsRobinson.setChecked(True)
        except:
            pass

class LoginDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        icon = qtg.QIcon()
        icon.addPixmap(qtg.QPixmap(":/icon/oil-barrel.svg"), qtg.QIcon.Normal, qtg.QIcon.Off)
        self.setFixedSize(300, 150)
        self.setWindowIcon(icon)
        self.setWindowTitle('Fluid Properties Calculator')
        self.label = qtw.QLabel(self)
        self.label.setText('Enter verification code:\n'
                           'Please ask the developer (Ferdiansyah Rahman)')
        self.password = qtw.QLineEdit(self)
        self.login = qtw.QPushButton('Login', self)
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.password)
        layout.addWidget(self.login)
        self.login.clicked.connect(self.handleLogin)

    def handleLogin(self):
        hash_pass = hashlib.sha256(self.password.text().encode('utf-8')).hexdigest()
        if hash_pass == 'f80eb7deefa60ea5800fa247b5ae4e2548ff6527c8bed4acf4f8bbe85f3e71f1':
            data = {'SHA 256 Hash Password UTF-8 Encoding': 'f80eb7deefa60ea5800fa247b5ae4e2548ff6527c8bed4acf4f8bbe85f3e71f1'}
            with open('secure.dll', 'w') as outfile:
                json.dump(data, outfile)
            self.accept()
        else:
            qtw.QMessageBox.warning(self, 'Error', 'Wrong verification code! \n'
                                                   'Please ask the developer for the code (Ferdiansyah Rahman)')

if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    try:
        with open('secure.dll') as json_file:
            data = json.load(json_file)
    except:
        data = 0

    if data == 0:
        login = LoginDialog()
        if login.exec_() == qtw.QDialog.Accepted:
            w = MainWindow()
            sys.exit(app.exec_())
    else:
        w = MainWindow()
        sys.exit(app.exec_())