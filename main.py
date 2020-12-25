# Ngulang gara2 filenya overwrite

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QValueAxis
from guikorelasi import Ui_MainWindow
from gui_plot import Ui_PlotWindow
from gui_about import Ui_AboutUsDialog
import sys
import random
from math import sin, e, pi, erf, ceil
from fungsi_korelasi import korelasi_oil

oil_Rs = korelasi_oil.Rs()
oil_Pb = korelasi_oil.Pb()
oil_visc = korelasi_oil.viscosity()

def bulat_atas_ribuan(angka):
    hasil = int(ceil(angka/1000.0))*1000
    return hasil

def transpose(matrix):
    matrix_new = []
    for i in range(len(matrix[0])):
        matrix_new.append([])
        matrix_new[i].append(matrix[0][i])
        matrix_new[i].append(matrix[1][i])
    return matrix_new

class grafik():
    def viscosity(self, windowed=False):
        oil_API = 40
        gas_SG = 0.841
        Rsb = 1658
        T_res = 271.4
        T_sep = 120
        P_sep = 295 + 14.7
        Pb = oil_Pb.vasquez_beggs(oil_API=oil_API, T_sep=T_sep, T_res=T_res, P_sep=P_sep, gas_SG=gas_SG, Rsb=Rsb)
        Rs_array = oil_Rs.vasquez_beggs(oil_API=oil_API, T_res=T_res, T_sep=T_sep, P_res=7500, P_sep=P_sep, gas_SG=gas_SG, Pb=Pb, Rsb=Rsb)
        data = oil_visc.vasquez_beggs_robinson(oil_API=oil_API, T_res=T_res, Rs_array=Rs_array, Pb=Pb, P_res=7500, Rsb=Rsb)

        print(data)

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
        axis_Y.setRange(min(data[1]), max(data[1]))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('Viscosity (cP)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Rs(self, windowed=False, korelasi="vasquez_beggs"):
        oil_API = 40
        gas_SG = 0.841
        Rsb = 1658
        T_res = 271.4
        T_sep = 120
        P_sep = 295 + 14.7
        Pb = oil_Pb.vasquez_beggs(oil_API=oil_API, T_sep=T_sep, T_res=T_res, P_sep=P_sep, gas_SG=gas_SG, Rsb=Rsb)
        if korelasi == "vasquez_beggs":
            data = oil_Rs.vasquez_beggs(oil_API=oil_API, T_res=T_res, T_sep=T_sep, P_res=7500, P_sep=P_sep, gas_SG=gas_SG, Pb=Pb, Rsb=Rsb)


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
        axis_Y.setRange(min(data[1]), bulat_atas_ribuan(max(data[1])))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('Gas Solubilty (scf/STB)')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Bo(self, windowed=False):

        x = []
        y = []
        for i_x in range(-100,100,1):
            x.append(i_x/10)
            y.append(erf(i_x/10))

        data = [x,y]
        data_new = transpose(data)

        series = QLineSeries()
        for l in data_new:
            series.append(l[0], l[1])

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
            chart.setTitle('Formation Volume Factor (Bob)')
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
        axis_X.setRange(min(x), max(x))
        axis_X.setTickCount(6)
        axis_X.setTitleText('Sumbu X')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(min(y), max(y))
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('Sumbu Y')
        axis_Y.setTitleFont(label_font)
        chart.addAxis(axis_Y, qtc.Qt.AlignLeft)
        series.attachAxis(axis_Y)

        chartview = QChartView(chart)
        chartview.setRenderHint(qtg.QPainter.Antialiasing)
        return chartview

    def Bob(self, windowed=False):
        series = QLineSeries()
        for i in range(0, 10, 1):
            series.append(i, random.randint(1, 20))

        chart = QChart()
        chart.addSeries(series)
        chart.legend().hide()
        chart.layout().setContentsMargins(0, 0, 0, 0)
        chart.setBackgroundRoundness(0)

        # Tema harus ditaruh di atas, agar label_font bisa overwrite Font-nya
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #chart.setAnimationEasingCurve(qtc.QEasingCurve.Linear)

        label_font = qtg.QFont()
        if windowed == True:
            chart.setTitle('Formation Volume Factor (Bob)')
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
        axis_X.setRange(0, 10)
        axis_X.setTickCount(6)
        axis_X.setTitleText('Sumbu X')
        axis_X.setTitleFont(label_font)
        chart.addAxis(axis_X, qtc.Qt.AlignBottom)
        series.attachAxis(axis_X)

        axis_Y = QValueAxis()
        axis_Y.setRange(0, 20)
        axis_Y.setTickCount(5)
        axis_Y.setTitleText('Sumbu Y')
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

        self.dialogAbout = AboutWindow()
        self.dialogBob = SecondWindow()
        self.dialogBo = SecondWindow()
        self.dialogRs = SecondWindow()
        self.dialogVisc = SecondWindow()

        self.ui.ButtonTest.clicked.connect(self.cobaPakaiChart)

        self.ui.ButtonNext.clicked.connect(self.nextTab)
        self.ui.ButtonPrev.clicked.connect(self.prevTab)

        self.ui.viewBobButton.clicked.connect(self.BobWindow)
        self.ui.viewBoButton.clicked.connect(self.BoWindow)
        self.ui.viewRsButton.clicked.connect(self.RsWindow)
        self.ui.viewViscButton.clicked.connect(self.ViscWindow)

        self.inputInformasiUser()
        self.ui.actionAbout_Us.triggered.connect(self.openAboutWindow)

        # Your code will end here
        self.showMaximized()

    def openAboutWindow(self):
        self.dialogAbout.show()

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

    def cobaPakaiChart(self):
        if self.ui.BobLayout.isEmpty() == True:
            self.ui.BobLayout.addWidget(grafik.Bob(self))
        if self.ui.BoLayout.isEmpty() == True:
            self.ui.BoLayout.addWidget(grafik.Bo(self))
        if self.ui.RsLayout.isEmpty() == True:
            self.ui.RsLayout.addWidget(grafik.Rs(self))
        if self.ui.ViscLayout.isEmpty() == True:
            self.ui.ViscLayout.addWidget(grafik.viscosity(self))

    def ViscWindow(self):
        if self.dialogVisc.ui.LayGraph.isEmpty() == True:
            self.dialogVisc.ui.LayGraph.addWidget(grafik.viscosity(self, windowed=True))
        self.dialogVisc.setWindowTitle('Viscosity')
        self.dialogVisc.show()

    def RsWindow(self):
        if self.dialogRs.ui.LayGraph.isEmpty() == True:
            self.dialogRs.ui.LayGraph.addWidget(grafik.Rs(self, windowed=True))
        self.dialogRs.setWindowTitle('Gas Solubility')
        self.dialogRs.show()

    def BoWindow(self):
        if self.dialogBo.ui.LayGraph.isEmpty() == True:
            self.dialogBo.ui.LayGraph.addWidget(grafik.Bo(self, windowed=True))
        self.dialogBo.setWindowTitle('Tes')
        self.dialogBo.show()

    def BobWindow(self):
        if self.dialogBob.ui.LayGraph.isEmpty() == True:
            self.dialogBob.ui.LayGraph.addWidget(grafik.Bob(self, windowed=True))
        self.dialogBob.setWindowTitle('Tes')
        self.dialogBob.show()

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
        row = range(0,len(matrix_data), 1)
        col = range(0,len(matrix_data[0]), 1)
        for i in row:
            for j in col:
                item = matrix_data[i][j]
                cell = qtw.QTableWidgetItem(str(item))
                table.setItem(i, j, cell)
                self.ui.progressTable.setValue(int((i/(len(matrix_data)-1))*100))

if __name__=='__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())