# coding=utf-8
# author=weijer
from Qt import QtWidgets as QtGui
from Qt import QtCore as QtCore
from Qt import QtCompat as QtCompat
import sys
import os
# import loadui
import package

current_dir = os.path.dirname(__file__)
ui_path = os.path.join(current_dir, "static/pack.ui")


class PackageDialog(QtGui.QDialog):
    def __init__(self):
        super(PackageDialog, self).__init__()

        main_layout = QtGui.QVBoxLayout(self)
        self.mainWidget = QtCompat.load_ui(ui_path)
        self.setWindowTitle(self.mainWidget.windowTitle())
        main_layout.addWidget(self.mainWidget)

        self.mainWidget.FileButton.clicked.connect(self.on_FileButton_clicked)
        self.mainWidget.packButton.clicked.connect(self.on_packButton_clicked)
        self.mainWidget.cancelButton.clicked.connect(self.close)

    @QtCore.Slot()
    def on_FileButton_clicked(self):
        """
        choice pack file folder
        :return:
        """
        dir = QtGui.QFileDialog.getExistingDirectory(self, "")
        self.mainWidget.filelineEdit.setText(dir)

    @QtCore.Slot()
    def on_packButton_clicked(self):
        """
        pack nuke project ro target dir
        :return:
        """
        target_dir = self.mainWidget.filelineEdit.text()
        if target_dir:
            package.Package(target_dir, self, self.show_Progress()).packed_file()
        else:
            self.show_msgBox()

    def show_msgBox(self):
        """
        MessageBox tips
        :return:
        """
        msgBox = QtGui.QMessageBox()
        msgBox.warning(self, u"警告", u"必须选择文件夹!")

    def show_Progress(self):
        """
        progress Dialog
        :return:
        """
        progressDialog = QtGui.QProgressDialog()
        progressDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        progressDialog.setWindowTitle(u"请等待")
        progressDialog.setLabelText(u"拷贝中...")
        progressDialog.setCancelButtonText(u"取消")
        return progressDialog


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Package = PackageDialog()
    Package.show()
    sys.exit(app.exec_())
