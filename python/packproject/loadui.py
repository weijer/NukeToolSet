# coing=utf8
import PySide.QtCore as QtCore
import PySide.QtUiTools as QtUiTools


def load_ui(ui_path):
    loader = QtUiTools.QUiLoader()
    f = QtCore.QFile(ui_path)
    f.open(QtCore.QFile.ReadOnly)
    widget = loader.load(f)
    f.close()
    return widget
