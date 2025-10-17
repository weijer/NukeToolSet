#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Copy Class
#
#----------------------------------------------------------------------------------------------------------

from PySide import QtGui

nodeClasses = ' '.join(sorted([i.Class() for i in nuke.selectedNodes()]))

QtGui.QApplication.clipboard().setText(nodeClasses)

	