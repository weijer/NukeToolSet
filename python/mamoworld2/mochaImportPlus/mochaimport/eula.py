# USAGE
#
# if eula.acceptEulaDialog():
#    print("accepted")
# else:
#    print("rejected")


try:
    from PySide import QtGui

    myQtModule = QtGui
except:
    from PySide2 import QtWidgets

    myQtModule = QtWidgets


def acceptEulaDialog():
    return EulaDialog().exec_()


class EulaDialog(myQtModule.QDialog):

    def __init__(self):
        super(EulaDialog, self).__init__()
        self.eulaText = """<strong>END USER LICENSE AGREEMENT</strong><br>TODO"""
        self.initUI()

    def initUI(self):
        licenseTextBox = myQtModule.QHBoxLayout()
        licenseInfoText = myQtModule.QTextEdit(self.eulaText, self)
        licenseInfoText.setReadOnly(True)
        licenseTextBox.addWidget(licenseInfoText)

        infoTextBox = myQtModule.QHBoxLayout()
        infoText = myQtModule.QLabel(
            "If you agree to the above terms press 'I Accept'. "
            "Otherwise press 'Cancel' to cancel installation of the license.")
        infoTextBox.addWidget(infoText)

        buttonsBox = myQtModule.QHBoxLayout()
        acceptButton = myQtModule.QPushButton("I Accept", self)
        acceptButton.setAutoDefault(False)
        cancelButton = myQtModule.QPushButton("Cancel", self)
        cancelButton.setAutoDefault(False)
        buttonsBox.addWidget(acceptButton)
        buttonsBox.addWidget(cancelButton)

        mainBox = myQtModule.QVBoxLayout()
        mainBox.addLayout(licenseTextBox)
        mainBox.addLayout(infoTextBox)
        mainBox.addStretch(1)
        mainBox.addLayout(buttonsBox)

        acceptButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)

        # self.setGeometry(300, 300, 250, 150)
        self.setLayout(mainBox)

        self.setWindowTitle("End User License Agreement (EULA)")
