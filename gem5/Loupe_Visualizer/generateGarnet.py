from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class GuiGenerateGarnet(QtGui.QMainWindow):
    def __init__(self):
        super(GuiGenerateGarnet, self).__init__()
        self.setObjectName(_fromUtf8("self"))
        self.resize(513, 500)
        self.setMaximumSize(QtCore.QSize(1000, 500))
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("GuiWindowInternal"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_topology_options = QtGui.QLabel(self.centralwidget)
        self.label_topology_options.setAlignment(QtCore.Qt.AlignCenter)
        self.label_topology_options.setObjectName(_fromUtf8("label_topology_options"))
        self.verticalLayout.addWidget(self.label_topology_options)
        self.combo_topology = QtGui.QComboBox(self.centralwidget)
        self.combo_topology.setObjectName(_fromUtf8("combo_topology"))
        self.combo_topology.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.combo_topology)
        self.sld_numcpus = QtGui.QSlider(self.centralwidget)
        self.sld_numcpus.setMaximum(64)
        self.sld_numcpus.setSliderPosition(16)
        self.sld_numcpus.setOrientation(QtCore.Qt.Horizontal)
        self.sld_numcpus.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_numcpus.setTickInterval(2)
        self.sld_numcpus.setObjectName(_fromUtf8("sld_numcpus"))
        self.verticalLayout.addWidget(self.sld_numcpus)
        self.sld_numrows = QtGui.QSlider(self.centralwidget)
        self.sld_numrows.setMaximum(8)
        self.sld_numrows.setProperty("value", 4)
        self.sld_numrows.setOrientation(QtCore.Qt.Horizontal)
        self.sld_numrows.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_numrows.setTickInterval(1)
        self.sld_numrows.setObjectName(_fromUtf8("sld_numrows"))
        self.verticalLayout.addWidget(self.sld_numrows)
        self.sld_vcspervnet = QtGui.QSlider(self.centralwidget)
        self.sld_vcspervnet.setMaximum(8)
        self.sld_vcspervnet.setSliderPosition(8)
        self.sld_vcspervnet.setOrientation(QtCore.Qt.Horizontal)
        self.sld_vcspervnet.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_vcspervnet.setTickInterval(1)
        self.sld_vcspervnet.setObjectName(_fromUtf8("sld_vcspervnet"))
        self.verticalLayout.addWidget(self.sld_vcspervnet)
        self.label_simulation_options = QtGui.QLabel(self.centralwidget)
        self.label_simulation_options.setAlignment(QtCore.Qt.AlignCenter)
        self.label_simulation_options.setObjectName(_fromUtf8("label_simulation_options"))
        self.verticalLayout.addWidget(self.label_simulation_options)
        self.sld_simcycles = QtGui.QSlider(self.centralwidget)
        self.sld_simcycles.setMaximum(5000)
        self.sld_simcycles.setSingleStep(500)
        self.sld_simcycles.setSliderPosition(2500)
        self.sld_simcycles.setOrientation(QtCore.Qt.Horizontal)
        self.sld_simcycles.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_simcycles.setTickInterval(500)
        self.sld_simcycles.setObjectName(_fromUtf8("sld_simcycles"))
        self.verticalLayout.addWidget(self.sld_simcycles)
        self.sld_injectionrate = QtGui.QSlider(self.centralwidget)
        self.sld_injectionrate.setMaximum(100)
        self.sld_injectionrate.setSingleStep(2)
        self.sld_injectionrate.setProperty("value", 24)
        self.sld_injectionrate.setOrientation(QtCore.Qt.Horizontal)
        self.sld_injectionrate.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_injectionrate.setTickInterval(10)
        self.sld_injectionrate.setObjectName(_fromUtf8("sld_injectionrate"))
        self.verticalLayout.addWidget(self.sld_injectionrate)
        self.combo_traffic = QtGui.QComboBox(self.centralwidget)
        self.combo_traffic.setObjectName(_fromUtf8("combo_traffic"))
        self.combo_traffic.addItem(_fromUtf8(""))
        self.combo_traffic.addItem(_fromUtf8(""))
        self.combo_traffic.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.combo_traffic)
        self.combo_algorithm = QtGui.QComboBox(self.centralwidget)
        self.combo_algorithm.setObjectName(_fromUtf8("combo_algorithm"))
        self.combo_algorithm.addItem(_fromUtf8(""))
        self.combo_algorithm.addItem(_fromUtf8(""))
        self.combo_algorithm.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.combo_algorithm)

        self.pb_createRunCommand = QtGui.QPushButton(self.centralwidget)
        self.pb_createRunCommand.setObjectName(_fromUtf8("pb_createRunCommand"))
        self.pb_createRunCommand.clicked.connect(self.show_garnet_cmd)
        self.verticalLayout.addWidget(self.pb_createRunCommand)

        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 513, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Generate Garnet Network", None))
        self.label_topology_options.setText(_translate("self", "Topology Options", None))
        self.combo_topology.setItemText(0, _translate("self", "Mesh", None))
        self.label_simulation_options.setText(_translate("self", "Simulation Options", None))
        self.combo_traffic.setItemText(0, _translate("self", "Uniform Random Traffic", None))
        self.combo_traffic.setItemText(1, _translate("self", "Tornado Traffic", None))
        self.combo_traffic.setItemText(2, _translate("self", "Bit Complement Traffic", None))
        self.combo_algorithm.setItemText(0, _translate("self", "XY Routing", None))
        self.combo_algorithm.setItemText(1, _translate("self", "George Routing", None))
        self.combo_algorithm.setItemText(2, _translate("self", "Escape VC Routing", None))
        self.pb_createRunCommand.setText(_translate("self", "Create Run Command", None))

    def show_garnet_cmd(self):
        garnet_dialog = QtGui.QMessageBox()
        run_cmd = self.generate_run_cmd()
        garnet_dialog.setWindowTitle("Generated Garnet Command")
        garnet_dialog.setText("Here is the generated Garnet Command:")
        garnet_dialog.setDetailedText(run_cmd)
        garnet_dialog.exec_()

    def generate_run_cmd(self):
        run_command = "./build/ALPHA_Network_test/gem5.debug configs/example/ruby_network_test.py \\"
        run_command += " --network=garnet2.0 \\"
        run_command += " --num-cpus=" + str(self.sld_numcpus.value()) + " \\"
        run_command += " --num-dirs=" + str(self.sld_numcpus.value()) + " \\"
        run_command += " --topology=" + str(self.combo_topology.currentText()) + " \\"
        run_command += " --num-rows=" + str(self.sld_numrows.value()) + " \\"
        run_command += " --sim-cycles=" + str(self.sld_simcycles.value()) + " \\"
        run_command += " --injectionrate=" + str(self.sld_injectionrate.value() / 100) + " \\"
        if self.combo_traffic.currentText() == "Uniform Random Traffic":
            run_command += " --synthetic=" + str(0) + " \\"
        elif self.combo_traffic.currentText() == "Tornado Traffic":
            run_command += " --synthetic=" + str(1) + " \\"
        elif self.combo_traffic.currentText() == "Bit Complement Traffic":
            run_command += " --synthetic=" + str(2) + " \\"
        else:
            print("Invalid traffic type")
        run_command += " --vcs-per-vnet=" + str(self.sld_vcspervnet.value()) + " \\"
        if self.combo_algorithm.currentText() == "XY Routing":
            run_command += " --routing-algorithm=" + str(0) + " \\"
        elif self.combo_algorithm.currentText() == "George Routing":
            run_command += " --routing-algorithm=" + str(1) + " \\"
        elif self.combo_algorithm.currentText() == "Escape VC Routing":
            run_command += " --routing-algorithm=" + str(2) + " \\"
        else:
            print("Invalid algorithm")
        print(run_command)
        return run_command
