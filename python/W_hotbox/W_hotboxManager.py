# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
version = '1.9'
releaseDate = 'March 28 2021'

# ----------------------------------------------------------------------------------------------------------
# LICENSE
# ----------------------------------------------------------------------------------------------------------

'''
Copyright (c) 2016-2021, Wouter Gilsing
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Redistribution of this software in source or binary forms shall be free
      of all charges or fees to the recipient of this software.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

# ----------------------------------------------------------------------------------------------------------
# modules
# ----------------------------------------------------------------------------------------------------------

import nuke

# Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
elif nuke.NUKE_VERSION_MAJOR < 16:
    from PySide2 import QtGui, QtCore, QtWidgets
else:
    from PySide6 import QtGui, QtCore, QtWidgets

import os
import shutil

import re
import string
import colorsys
import tempfile
import tarfile
import base64

from datetime import datetime as dt
from webbrowser import open as openURL

from . import W_hotbox

preferencesNode = nuke.toNode('preferences')


# ----------------------------------------------------------------------------------------------------------

class HotboxManager(QtWidgets.QWidget):
    def __init__(self, path=''):
        super(HotboxManager, self).__init__()

        # --------------------------------------------------------------------------------------------------
        # main widget
        # --------------------------------------------------------------------------------------------------

        # parent to main nuke interface
        self.setParent(QtWidgets.QApplication.instance().activeWindow())
        self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowTitle('W_hotbox Manager - %s' % path)

        self.setMinimumWidth(1000)
        self.setMinimumHeight(400)

        # --------------------------------------------------------------------------------------------------
        # colors
        # --------------------------------------------------------------------------------------------------

        self.activeColor = '#3a3a3a'
        self.lockedColor = '#262626'

        # --------------------------------------------------------------------------------------------------

        self.rootLocation = path.replace('\\', '/')

        # --------------------------------------------------------------------------------------------------
        # create folders
        # --------------------------------------------------------------------------------------------------

        # If the manager is launched for the default repository, make sure the current archive exists.

        preferencesLocation = preferencesNode.knob('hotboxLocation').value()
        if preferencesLocation[-1] != '/':
            preferencesLocation += '/'

        if self.rootLocation == preferencesLocation:
            for subFolder in ['', 'Single', 'Multiple', 'All', 'Single/No Selection', 'Rules', 'Templates']:
                subFolderPath = self.rootLocation + subFolder
                if not os.path.isdir(subFolderPath):
                    try:
                        os.mkdir(subFolderPath)
                    except:
                        pass

        self.templateLocation = self.rootLocation + 'Templates/'

        # --------------------------------------------------------------------------------------------------
        # left column - classes list
        # --------------------------------------------------------------------------------------------------

        self.classesListLayout = QtWidgets.QVBoxLayout()

        # scope dropdown
        self.scopeComboBox = QtWidgets.QComboBox()
        self.scopeComboBoxItems = ['Single', 'Multiple', 'All', 'Rules']
        self.scopeComboBox.addItems(self.scopeComboBoxItems)
        self.scopeComboBox.insertSeparator(3)

        self.scopeComboBox.currentIndexChanged.connect(self.buildClassesList)

        # list column
        self.classesList = QListWidgetCustom(self)
        self.classesList.setFixedWidth(150)

        self.classesListLayout.addWidget(self.scopeComboBox)
        self.classesListLayout.addWidget(self.classesList)

        # buttons
        self.classesListButtonsLayout = QtWidgets.QVBoxLayout()

        self.classesListAddButton = QLabelButton('add', self.classesList)
        self.classesListRemoveButton = QLabelButton('remove', self.classesList)
        self.classesListRenameButton = QLabelButton('rename', self.classesList)

        # connect
        self.classesListAddButton.clicked.connect(self.addClass)
        self.classesListRemoveButton.clicked.connect(self.removeClass)
        self.classesListRenameButton.clicked.connect(self.renameClass)

        # assemble layout
        self.classesListButtonsLayout.addStretch()
        self.classesListButtonsLayout.addWidget(self.classesListAddButton)
        self.classesListButtonsLayout.addWidget(self.classesListRemoveButton)
        self.classesListButtonsLayout.addWidget(self.classesListRenameButton)
        self.classesListButtonsLayout.addStretch()

        # --------------------------------------------------------------------------------------------------
        # right column - hotbox items tree
        # --------------------------------------------------------------------------------------------------

        self.hotboxItemsTree = QTreeViewCustom(self)
        self.hotboxItemsTree.setFixedWidth(150)
        self.rootPath = nuke.toNode('preferences').knob('hotboxLocation').value()

        self.classesList.itemSelectionChanged.connect(self.hotboxItemsTree.populateTree)

        # actions
        self.hotboxItemsTreeButtonsLayout = QtWidgets.QVBoxLayout()

        self.hotboxItemsTreeAddButton = QLabelButton('add', self.hotboxItemsTree)
        self.hotboxItemsTreeAddFolderButton = QLabelButton('addFolder', self.hotboxItemsTree)
        self.hotboxItemsTreeRemoveButton = QLabelButton('remove', self.hotboxItemsTree)
        self.hotboxItemsTreeDuplicateButton = QLabelButton('duplicate', self.hotboxItemsTree)
        self.hotboxItemsTreeCopyButton = QLabelButton('copy', self.hotboxItemsTree)
        self.hotboxItemsTreePasteButton = QLabelButton('paste', self.hotboxItemsTree)

        self.hotboxItemsTreeMoveUp = QLabelButton('moveUp', self.hotboxItemsTree)
        self.hotboxItemsTreeMoveDown = QLabelButton('moveDown', self.hotboxItemsTree)
        self.hotboxItemsTreeMoveUpLevel = QLabelButton('moveUpLevel', self.hotboxItemsTree)

        # connect
        self.hotboxItemsTreeAddButton.clicked.connect(self.hotboxItemsTree.addItem)
        self.hotboxItemsTreeAddFolderButton.clicked.connect(lambda: self.hotboxItemsTree.addItem(True))
        self.hotboxItemsTreeRemoveButton.clicked.connect(self.hotboxItemsTree.removeItem)
        self.hotboxItemsTreeDuplicateButton.clicked.connect(self.hotboxItemsTree.duplicateItem)
        self.hotboxItemsTreeCopyButton.clicked.connect(self.hotboxItemsTree.copyItem)
        self.hotboxItemsTreePasteButton.clicked.connect(self.hotboxItemsTree.pasteItem)

        self.hotboxItemsTreeMoveUp.clicked.connect(lambda: self.hotboxItemsTree.moveItem(0))
        self.hotboxItemsTreeMoveDown.clicked.connect(lambda: self.hotboxItemsTree.moveItem(1))
        self.hotboxItemsTreeMoveUpLevel.clicked.connect(lambda: self.hotboxItemsTree.moveItem(2))

        # assemble layout
        self.hotboxItemsTreeButtonsLayout.addStretch()
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeAddButton)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeAddFolderButton)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeRemoveButton)

        self.hotboxItemsTreeButtonsLayout.addSpacing(25)

        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeMoveUp)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeMoveDown)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeMoveUpLevel)

        self.hotboxItemsTreeButtonsLayout.addSpacing(25)

        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeCopyButton)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreePasteButton)
        self.hotboxItemsTreeButtonsLayout.addWidget(self.hotboxItemsTreeDuplicateButton)

        self.hotboxItemsTreeButtonsLayout.addStretch()

        # --------------------------------------------------------------------------------------------------
        # import/export
        # --------------------------------------------------------------------------------------------------

        # create buttons
        self.clipboardArchive = QtWidgets.QCheckBox('Clipboard')
        self.importArchiveButton = QtWidgets.QPushButton('Import Archive')
        self.exportArchiveButton = QtWidgets.QPushButton('Export Archive')

        self.importArchiveButton.setMaximumWidth(100)
        self.exportArchiveButton.setMaximumWidth(100)

        # tooltips
        tooltip = 'Make use of the clipboard to import/export an archive, rather than saving a file to disk.'
        self.clipboardArchive.setToolTip(tooltip)
        tooltip = 'Import a button archive. This will append the current set of buttons and overwrite any buttons with the same name.'
        self.importArchiveButton.setToolTip(tooltip)
        tooltip = 'Export the current set of buttons as an archive.'
        self.exportArchiveButton.setToolTip(tooltip)

        # wire up
        self.importArchiveButton.clicked.connect(self.importHotboxArchive)
        self.exportArchiveButton.clicked.connect(self.exportHotboxArchive)

        # assemble
        self.archiveButtonsLayout = QtWidgets.QHBoxLayout()
        self.archiveButtonsLayout.addStretch()
        self.archiveButtonsLayout.addWidget(self.clipboardArchive)
        self.archiveButtonsLayout.addWidget(self.importArchiveButton)
        self.archiveButtonsLayout.addWidget(self.exportArchiveButton)

        # --------------------------------------------------------------------------------------------------
        # scriptEditor
        # --------------------------------------------------------------------------------------------------

        self.ignoreSave = False
        self.loadedScript = None
        self.scriptEditorLayout = QtWidgets.QVBoxLayout()

        # buttons
        self.scriptEditorButtonsLayout = QtWidgets.QHBoxLayout()

        self.scriptEditorTemplateButton = QtWidgets.QToolButton()
        self.scriptEditorTemplateButton.setText('Templates  ')
        self.scriptEditorTemplateButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.exitTemplateModeButton = QtWidgets.QPushButton('Exit template mode')
        self.exitTemplateModeButton.setStyleSheet('color: #f7931e')
        self.exitTemplateModeButton.setVisible(False)

        self.scriptEditorImportButton = QtWidgets.QPushButton('Import')
        self.scriptEditorImportButton.clicked.connect(self.importScriptEditor)

        self.scriptEditorTemplateMenu = ScriptEditorTemplateMenu(self)
        self.scriptEditorTemplateButton.setMenu(self.scriptEditorTemplateMenu)
        self.exitTemplateModeButton.clicked.connect(self.toggleTemplateMode)

        self.scriptEditorTemplateButtons = [self.exitTemplateModeButton, self.scriptEditorTemplateButton]

        self.scriptEditorButtonsLayout.addStretch()
        for button in self.scriptEditorTemplateButtons + [self.scriptEditorImportButton]:
            self.scriptEditorButtonsLayout.addWidget(button)
        self.scriptEditorButtonsLayout.addStretch()

        # name
        self.scriptEditorNameLayout = QtWidgets.QHBoxLayout()

        self.scriptEditorNameLabel = QtWidgets.QLabel('Name')
        self.scriptEditorName = ScriptEditorNameWidget()
        self.scriptEditorName.setAlignment(QtCore.Qt.AlignLeft)

        self.scriptEditorName.editingFinished.connect(self.saveScriptEditor)

        # color swatches
        self.colorSwatchButtonLabel = QtWidgets.QLabel('Button')
        self.colorSwatchButton = ColorSwatch('#525252')

        self.colorSwatchTextLabel = QtWidgets.QLabel('Text')
        self.colorSwatchText = ColorSwatch('#eeeeee')

        self.colorSwatchButton.setChild(self.colorSwatchText)

        # wire up color swatches
        self.colorSwatchButton.save.connect(self.saveScriptEditor)
        self.colorSwatchText.save.connect(self.saveScriptEditor)

        self.scriptEditorNameWidgets = [self.scriptEditorNameLabel, self.scriptEditorName, self.colorSwatchButtonLabel,
                                        self.colorSwatchButton, self.colorSwatchTextLabel, self.colorSwatchText]

        # rules
        self.rulesFlagCheckbox = QtWidgets.QCheckBox('Ignore classes')
        self.rulesFlagCheckbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.rulesFlagCheckbox.stateChanged.connect(lambda: self.saveScriptEditor())

        # label to make sure the checkbox is aligned to the right
        self.rulesFlagLabel = QtWidgets.QLabel('')
        self.rulesFlagWidgets = [self.rulesFlagCheckbox, self.rulesFlagLabel]

        for widget in self.rulesFlagWidgets:
            widget.setVisible(False)

        # assemble layout
        for widget in self.rulesFlagWidgets + self.scriptEditorNameWidgets:
            self.scriptEditorNameLayout.addWidget(widget)

        # script
        self.scriptEditorScript = ScriptEditorWidget()
        self.scriptEditorScript.setMinimumHeight(200)
        self.scriptEditorScript.setMinimumWidth(500)

        self.scriptEditorScript.save.connect(self.saveScriptEditor)

        ScriptEditorHighlighter(self.scriptEditorScript.document())

        scriptEditorFont = QtGui.QFont()
        scriptEditorFont.setFamily('Courier')
        scriptEditorFont.setStyleHint(QtGui.QFont.Monospace)
        scriptEditorFont.setFixedPitch(True)
        scriptEditorFont.setPointSize(preferencesNode.knob('hotboxScriptEditorFontSize').value())

        self.scriptEditorScript.setFont(scriptEditorFont)
        self.scriptEditorScript.setTabStopWidth(4 * QtGui.QFontMetrics(scriptEditorFont).width(' '))

        # assemble
        self.scriptEditorLayout.addLayout(self.archiveButtonsLayout)
        self.scriptEditorLayout.addLayout(self.scriptEditorNameLayout)
        self.scriptEditorLayout.addWidget(self.scriptEditorScript)
        self.scriptEditorLayout.addLayout(self.scriptEditorButtonsLayout)

        # --------------------------------------------------------------------------------------------------
        # main buttons
        # --------------------------------------------------------------------------------------------------

        self.mainButtonLayout = QtWidgets.QHBoxLayout()

        self.aboutButton = QtWidgets.QPushButton('?')
        self.aboutButton.clicked.connect(self.openAboutDialog)
        self.aboutButton.setMaximumWidth(20)

        self.mainCloseButton = QtWidgets.QPushButton('Close')
        self.mainCloseButton.clicked.connect(self.closeManager)

        self.mainButtonLayout.addWidget(self.aboutButton)
        self.mainButtonLayout.addStretch()
        self.mainButtonLayout.addWidget(self.mainCloseButton)

        # --------------------------------------------------------------------------------------------------
        # main layout
        # --------------------------------------------------------------------------------------------------

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.classesListButtonsLayout)
        self.mainLayout.addLayout(self.classesListLayout)
        self.mainLayout.addLayout(self.hotboxItemsTreeButtonsLayout)
        self.mainLayout.addWidget(self.hotboxItemsTree)
        self.mainLayout.addLayout(self.scriptEditorLayout)

        # --------------------------------------------------------------------------------------------------
        # layouts
        # --------------------------------------------------------------------------------------------------

        self.masterLayout = QtWidgets.QVBoxLayout()

        self.masterLayout.addLayout(self.mainLayout)
        self.masterLayout.addLayout(self.mainButtonLayout)

        self.setLayout(self.masterLayout)

        # --------------------------------------------------------------------------------------------------
        # move to center of the screen
        # --------------------------------------------------------------------------------------------------

        self.adjustSize()

        screenRes = QtWidgets.QDesktopWidget().screenGeometry()
        self.move(QtCore.QPoint(screenRes.width() // 2, screenRes.height() // 2) - QtCore.QPoint((self.width() // 2),
                                                                                                 (self.height() // 2)))

        # --------------------------------------------------------------------------------------------------
        # set values
        # --------------------------------------------------------------------------------------------------

        self.enableScriptEditor(False, False)

        self.scopeComboBox.setCurrentIndex(1)
        self.scopeComboBox.setCurrentIndex(0)
        self.scopeComboBoxLastIndex = 0

        # --------------------------------------------------------------------------------------------------
        # set hotbox to current selection
        # --------------------------------------------------------------------------------------------------

        launchMode = preferencesNode.knob('hotboxOpenManagerOptions').value()
        launchMode = launchMode.replace('Contextual', 'Single/Multiple')
        launchMode = launchMode.split('/')

        found = False

        # contextual
        if len(launchMode) > 1:

            selection = nuke.selectedNodes()

            classes = sorted(set([node.Class() for node in selection]))

            # single/multiple
            self.scopeComboBox.setCurrentIndex(len(classes) > 1)

            for index in range(self.classesList.count()):
                itemClasses = self.classesList.item(index).text().split('-')
                if all([nodeClass in itemClasses for nodeClass in classes]):
                    self.classesList.setCurrentRow(index)
                    found = True
                    break

            if len(launchMode) == 2:
                found = True

            else:
                found *= bool(selection)

        # all or rules (2 or 4)
        if not found:
            item = launchMode[-1]
            index = (int(item == 'Rules') * 2) + 2
            self.scopeComboBox.setCurrentIndex(index)

    # --------------------------------------------------------------------------------------------------
    # classes list
    # --------------------------------------------------------------------------------------------------

    def buildClassesList(self, selectItem=None):
        '''
        Populate classes list with items.
        '''

        # if restore based on index, save current index before clearing the widget.
        if isinstance(selectItem, bool) and selectItem:
            itemIndex = self.classesList.currentRow()

        self.mode = self.scopeComboBox.currentText()

        self.contextual = self.mode not in ['All', 'Templates']

        # turn this variable on, to prevent the itemChanged signal from emitting
        self.classesList.buildClassesList = True

        # clear selection
        self.classesList.clearSelection()

        # clear items tree
        self.hotboxItemsTree.clearTree()

        # clear list
        self.classesList.clear()

        # disable scripteditor
        self.enableScriptEditor(False, False)

        self.path = self.rootLocation + self.mode

        # color
        color = self.activeColor

        # disable if templates or all mode
        if self.contextual:
            self.classesList.setEnabled()
        else:
            self.classesList.setEnabled(False)

        if self.contextual:
            # sort items found on disk
            allItems = sorted(os.listdir(self.path), key=lambda s: s.lower())
            allItems = [folder for folder in allItems if
                        os.path.isdir(self.path + '/' + folder) and folder[0] not in ['.', '_']]

            # add items
            self.classesList.addItems(allItems)

        # add checkbox to item if in rule mode
        if self.mode == 'Rules':

            checkedStates = [QtCore.Qt.Unchecked, QtCore.Qt.Checked]
            for index in range(self.classesList.count()):

                item = self.classesList.item(index)
                itemText = item.text()

                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)

                # check if supposed to be enabled according to name
                checkedState = itemText[-1] != '_'
                item.setCheckState(checkedStates[checkedState])
                if not checkedState:
                    item.setText(itemText[:-1])

        self.toggleRulesMode(False)

        # populate buttons tree
        self.hotboxItemsTree.populateTree()

        # restore selection
        if selectItem:

            # select based on string
            if isinstance(selectItem, str):
                foundItems = self.classesList.findItems(selectItem, QtCore.Qt.MatchExactly)
                if foundItems:
                    self.classesList.setCurrentItem(foundItems[0])

            # select based on index
            if isinstance(selectItem, bool):
                allItems = self.classesList.count() - 1
                itemIndex = min(allItems, itemIndex)

                self.classesList.setCurrentRow(itemIndex)

        # turn this variable back off
        self.classesList.buildClassesList = False

    def addClass(self):
        '''
        Add a new nodeclass
        '''
        defaultName = 'NewClass'

        if self.mode == 'Rules':
            defaultName = 'NewRule'

        name = defaultName

        # in case name allready exists
        counter = 1
        while os.path.isdir(self.path + '/' + name):
            name = defaultName + str(counter)
            counter += 1

        # create folder on disk
        folderPath = '/'.join([self.path, name])
        os.mkdir(folderPath)

        # create rule file
        if self.mode == 'Rules':
            ruleFile = open(folderPath + '/_rule.py', 'w')
            ruleFile.write(FileHeader('0', rule=True).getHeader())
            ruleFile.close()

        self.buildClassesList(name)
        self.renameClass(True)

    def removeClass(self, className=None):
        '''
        Remove the selected nodeclass
        '''

        if className:
            selectedClass = className

        else:
            selectedClass = self.getSelectedClass()
            if not selectedClass:
                return

                # move to old folder
        oldFolder = '/'.join([self.path, '_old'])
        if not os.path.isdir(oldFolder):
            os.mkdir(oldFolder)

        shutil.move(self.path + '/' + selectedClass,
                    self.path + '/_old/' + selectedClass + '_' + dt.now().strftime('%Y%m%d%H%M%S'))

        self.buildClassesList(True)

    def renameClass(self, new=False):
        '''
        Rename the selected nodeclass
        '''

        selectedClass = self.getSelectedClass()
        if not selectedClass:
            return

            # kill any existing instances
        global renameDialogInstance
        if renameDialogInstance != None:
            renameDialogInstance.closeRenameDialog()

        # spawn new
        renameDialogInstance = RenameDialog(selectedClass, new)
        renameDialogInstance.show()

    def getSelectedClass(self):
        '''
        Return the name of the selected class
        '''

        if not self.classesList.itemSelected():
            return None

        selectedItem = self.classesList.currentItem()
        selectedClass = selectedItem.text()

        # if rule, check if item enabled
        if self.mode == 'Rules':
            selectedClass += '_' * (1 - bool(selectedItem.checkState()))

        return selectedClass

    # --------------------------------------------------------------------------------------------------
    # scriptEditor
    # --------------------------------------------------------------------------------------------------

    def loadScriptEditor(self, rule=False):
        '''
        Fill the fields of the the script editor with the information read from the currently selected
        file.
        '''

        self.scriptEditorScript.savedText = ''

        # check if items selected
        itemsSelected = True
        if not rule:
            itemsSelected = bool(self.hotboxItemsTree.selectedItems)

        if itemsSelected:

            if not rule:
                self.selectedItem = self.hotboxItemsTree.selectedItems[0]
                self.loadedScript = self.selectedItem.path

            # if rule mode
            else:
                item = self.classesList.currentItem()
                itemState = 1 - bool(item.checkState())
                self.loadedScript = '/'.join([self.path, item.text() + '_' * itemState, '_rule.py'])

            # if item (not submenu)
            if self.loadedScript.endswith('.py'):

                self.enableScriptEditor()

                if not rule:

                    # set attributes
                    name = getAttributeFromFile(self.loadedScript)
                    self.scriptEditorName.setText(name)

                    # make sure the colorswatches will remain disabled in template mode
                    if not self.exitTemplateModeButton.isVisible():
                        textColor = getAttributeFromFile(self.loadedScript, 'textColor')
                        self.colorSwatchText.setColor(textColor, adjustChild=False, indirect=True)

                        color = getAttributeFromFile(self.loadedScript, 'color')
                        self.colorSwatchButton.setColor(color, adjustChild=False, indirect=True)

                # rule
                else:

                    ignoreClasses = int(getAttributeFromFile(self.loadedScript, 'ignore classes'))

                    self.ignoreSave = True
                    self.rulesFlagCheckbox.setChecked(ignoreClasses)
                    self.ignoreSave = False

                # set script
                text = getScriptFromFile(self.loadedScript)
                self.scriptEditorScript.setPlainText(text)
                self.scriptEditorScript.updateSavedText()

            # if submenu
            else:

                # set name
                self.scriptEditorName.setText(open(self.loadedScript + '/_name.json').read())
                self.enableScriptEditor(False, True)

        else:

            self.loadedScript = None
            self.enableScriptEditor(False, False)

    def enableScriptEditor(self, editor=True, name=True):
        '''
        Enable/Disable widgets based on selection.
        '''

        colors = [self.activeColor, self.lockedColor]

        # script
        self.scriptEditorScript.setReadOnly(1 - editor)
        self.scriptEditorImportButton.setEnabled(editor)
        self.scriptEditorScript.setStyleSheet('background:%s' % colors[1 - editor])
        if not editor:
            self.scriptEditorScript.clear()

        # make sure the buttons are colorswatches are always disabled in template mode
        editor = editor * (1 - self.exitTemplateModeButton.isVisible())

        for colorSwatch in [self.colorSwatchButton, self.colorSwatchText, self.colorSwatchButtonLabel,
                            self.colorSwatchTextLabel]:
            colorSwatch.setEnabled(editor)

        # name
        self.scriptEditorName.setReadOnly(1 - name)
        self.scriptEditorNameLabel.setEnabled(name)
        self.scriptEditorName.setStyleSheet('background:%s' % colors[1 - name])

        if not name:
            self.scriptEditorName.clear()

        # template button
        self.scriptEditorTemplateMenu.enableMenuItems()

    def importScriptEditor(self):
        '''
        Set the current content of the script editor by importing an existing file. 
        '''

        if self.scriptEditorImportButton.isEnabled():
            importFile = nuke.getFilename('select file to  import', '*.py *.json')
            # replace tabs with spaces
            text = open(importFile).read().replace('\t', ' ' * 4)
            self.scriptEditorScript.setPlainText(text)
            self.scriptEditorScript.setFocus()

    def saveScriptEditor(self, template=False):
        '''
        Save the current content of the script editor 
        '''

        # dont save whenever this function is triggered while ignoreSave is on.
        if self.ignoreSave:
            return

        rule = self.rulesFlagCheckbox.isVisible()

        if not self.scriptEditorName.isReadOnly():

            name = self.scriptEditorName.text()

            if template:
                path = getFirstAvailableFilePath(self.templateLocation)
                path += '.py'

            else:
                path = self.loadedScript

            # file
            if path.endswith('.py'):

                text = self.scriptEditorScript.toPlainText()

                if not rule:

                    # header
                    color = self.colorSwatchButton.isNonDefault(True)
                    textColor = self.colorSwatchText.isNonDefault(True)

                    newFileContent = FileHeader(name, color, textColor).getHeader() + text

                else:
                    newFileContent = FileHeader(int(self.rulesFlagCheckbox.isChecked()), rule=True).getHeader() + text

                # save to disk
                currentFile = open(path, 'w')
                currentFile.write(newFileContent)
                currentFile.close()

                # change save status
                self.scriptEditorScript.updateSavedText()

            # menu
            else:
                # save to disk
                currentFile = open(self.loadedScript + '/_name.json', 'w')
                currentFile.write(name)
                currentFile.close()

            if not rule:
                self.selectedItem.setText(name)

            if template:
                # update template menu
                if path.startswith(self.templateLocation):
                    self.scriptEditorTemplateMenu.initMenu()

    # --------------------------------------------------------------------------------------------------
    # Rules mode
    # --------------------------------------------------------------------------------------------------

    def toggleRulesMode(self, mode=True):
        '''
        Toggle rule mode on and off.
        '''

        # if triggered by item selection
        if mode:
            if self.mode != 'Rules':
                return

        # apply change
        for index, widgetList in enumerate([self.rulesFlagWidgets, self.scriptEditorNameWidgets][::mode * 2 - 1]):
            for widget in widgetList:
                widget.setVisible(1 - index)

        if mode:
            self.loadScriptEditor(rule=True)

    # --------------------------------------------------------------------------------------------------
    # Template mode
    # --------------------------------------------------------------------------------------------------

    def toggleTemplateMode(self):
        '''
        Toggle template mode on and off.
        '''

        # check whether entering or leaving template mode.
        enter = True
        if self.exitTemplateModeButton.isVisible():
            enter = False

        # switch between template dropdown and 'Exit template mode' buttons.
        self.scriptEditorTemplateButton.setVisible(1 - enter)
        self.exitTemplateModeButton.setVisible(enter)

        # store current selection
        if enter:

            # scope
            self.lastSelectedScopeIndex = self.scopeComboBox.currentIndex()

            # class
            selectedClassItem = self.classesList.currentItem()
            if selectedClassItem:
                self.lastSelectedClassIndex = self.classesList.indexFromItem(selectedClassItem)
            else:
                self.lastSelectedClassIndex = None

            # item
            selectedItemIndexes = self.hotboxItemsTree.selectedIndexes()
            if selectedItemIndexes:
                self.lastSelectedItemIndex = selectedItemIndexes[0]
            else:
                self.lastSelectedItemIndex = None

        for index in range(self.scopeComboBox.count())[::-1]:
            self.scopeComboBox.removeItem(index)

        # refill scopeComboBox
        if enter:
            # change items of scopeCombobox to 'Templates'
            self.scopeComboBox.addItems(['Templates'])
            self.scopeComboBox.setCurrentIndex(0)
            self.scopeComboBox.setEditable(False)

        else:
            # update template menu
            self.scriptEditorTemplateMenu.initMenu()

            # change items of scopeCombobox to 'Single/Multiple/All'
            self.scopeComboBox.addItems(self.scopeComboBoxItems)

            # disable menu

            # restore last selection
            # scope
            self.scopeComboBox.setCurrentIndex(self.lastSelectedScopeIndex)

            # class
            if self.lastSelectedClassIndex:
                lastSelectedClassItem = self.classesList.itemFromIndex(self.lastSelectedClassIndex)
                self.classesList.setCurrentItem(lastSelectedClassItem)

            # item
            if self.lastSelectedItemIndex:
                self.hotboxItemsTree.setCurrentIndex(self.lastSelectedItemIndex)

            # make sure the template menu is properly enabled/disabled
            # this should would automatically, but fails when nothing is selected.
            self.scriptEditorTemplateMenu.enableMenuItems()

    # --------------------------------------------------------------------------------------------------
    # import/export functions
    # --------------------------------------------------------------------------------------------------

    # export
    def exportHotboxArchive(self):
        '''
        A method to export a set of buttons to an external archive.
        '''

        archiveLocation = tempfile.mkstemp()[1]

        # write to zip
        with tarfile.open(archiveLocation, "w:gz") as tar:
            tar.add(self.rootLocation, arcname=os.path.basename(self.rootLocation))

        # ----------------------------------------------------------------------------------------------
        # file
        # ----------------------------------------------------------------------------------------------

        if not self.clipboardArchive.isChecked():

            # save to file
            exportFileLocation = nuke.getFilename('Export Archive', '*.hotbox')

            if exportFileLocation == None:
                return

            if not exportFileLocation.endswith('.hotbox'):
                exportFileLocation += '.hotbox'

            shutil.copy(archiveLocation, exportFileLocation)

            nuke.message('Successfully exported archive to \n{}'.format(exportFileLocation))

        # ----------------------------------------------------------------------------------------------
        # clipboard
        # ----------------------------------------------------------------------------------------------

        else:

            # nuke 13
            if nuke.NUKE_VERSION_MAJOR > 12:

                # read from file
                with open(archiveLocation, 'rb') as tar:
                    archiveContent = tar.read()

                # convert bytes to text
                encodedArchive = str(base64.b64encode(archiveContent))
                encodedArchive = encodedArchive[2:-1]

            # nuke 12 and older
            else:
                # read from file
                with open(archiveLocation) as tar:
                    archiveContent = tar.read()

                encodedArchive = base64.b64encode(archiveContent)

            # save to clipboard
            QtWidgets.QApplication.clipboard().setText(encodedArchive)

    def indexArchive(self, location, dict=False):

        if dict:
            fileList = {}
        else:
            fileList = []

        for root, b, files in os.walk(location):
            root = root.replace('\\', '/')
            level = root.replace(location, '')

            if '/_' not in level and '/.' not in level:

                newLevel = level

                if '_name.json' in files:
                    readName = open(root + '/_name.json').read()
                    if '/' in readName:
                        readName = newLevel.replace('/', '**BACKSLASH**')

                    newLevel = '/'.join(level.split('/')[:-1]) + '/' + readName

                for file in files:
                    if not file.startswith('.'):
                        newFile = file
                        if len(file) == 6:
                            openFile = open(root + '/' + file).readlines()

                            nameTag = '# NAME: '

                            for line in (openFile):

                                if line.startswith(nameTag):

                                    newFile = line.split(nameTag)[-1].replace('\n', '')

                                    if '/' in newFile:
                                        newFile = newFile.replace('/', '**BACKSLASH**')

                        if dict:
                            fileList[newLevel + '/' + newFile] = level + '/' + file
                        else:
                            fileList.append([level + '/' + file, newLevel + '/' + newFile])
        return fileList

    # import
    def importHotboxArchive(self):
        '''
        A method to import a set of buttons to append the current archive with.
        If you're actually reading this, I apologise in advance for what's coming.
        I had trouble getting the code to work on Windows and it turned out it had to do with
        (back)slashes. I ended up trowing in a lot of ".replace('\\','/')". I works, but it
        turned kinda messy...
        '''

        nukeFolder = os.getenv('HOME').replace('\\', '/') + '/.nuke/'
        currentDate = dt.now().strftime('%Y%m%d%H%M')

        archiveLocation = tempfile.mkstemp()[1]

        # ----------------------------------------------------------------------------------------------
        # file
        # ----------------------------------------------------------------------------------------------

        if not self.clipboardArchive.isChecked():

            importFileLocation = nuke.getFilename('select to import', '*.hotbox')

            # if canceled
            if not importFileLocation:
                return

            shutil.copy(importFileLocation, archiveLocation)

        # ----------------------------------------------------------------------------------------------
        # clipboard
        # ----------------------------------------------------------------------------------------------

        else:

            encodedArchive = QtWidgets.QApplication.clipboard().text()
            decodedArchive = base64.b64decode(encodedArchive)

            with open(archiveLocation, 'wb') as archive:
                archive.write(decodedArchive)

        # ----------------------------------------------------------------------------------------------
        # extract archive
        # ----------------------------------------------------------------------------------------------

        importedArchiveLocation = tempfile.mkdtemp()

        # nuke 13
        if nuke.NUKE_VERSION_MAJOR > 12:
            # nuke 13 crashes when extracting a tar file...
            # therefore we need to run it through a subprocess

            command = []
            command.append('import tarfile')

            command.append('with tarfile.open("{}") as archive:'.format(archiveLocation))
            command.append('    archive.extractall("{}")'.format(importedArchiveLocation))

            command = '\n'.join(command)

            # write to temp file
            module = tempfile.mkstemp()[1]
            with open(module, 'w') as moduleFile:
                moduleFile.write(command)

            # execute temp file
            import subprocess
            process = subprocess.Popen('python {}'.format(module), shell=True)
            process.wait()

        # nuke 12 and odler
        else:

            with tarfile.open(archiveLocation) as archive:
                archive.extractall(importedArchiveLocation)

        # ----------------------------------------------------------------------------------------------

        importedArchiveLocation += '/'
        importedArchiveLocation = importedArchiveLocation.replace('\\', '/')

        # Make sure the current archive is healthy
        for i in ['Single', 'Multiple', 'All']:
            RepairHotbox(self.rootLocation + i, message=False)

        # Copy stuff from extracted archive to current hotbox location
        importedArchive = self.indexArchive(importedArchiveLocation)
        currentArchive = self.indexArchive(self.rootLocation, dict=True)

        newItems = []
        for i in importedArchive:
            if i[1] in currentArchive.keys():
                # if a file with the same name was found in the same folder, replace it with the new one
                shutil.copy(importedArchiveLocation + i[0], self.rootLocation + currentArchive[i[1]])
            else:
                # if no such file was found, store it in a list to be added later
                if not i[0].endswith('/_name.json'):
                    newItems.append(i)
        newItems = [[i[0].replace('\\', '/'), i[1].replace('\\', '/')] for i in newItems]

        # gather information about which folders are already present on disk, and which should be created
        allFoldersNeeded = {os.path.dirname(i[1]).replace('\\', '/'): os.path.dirname(i[0]).replace('\\', '/') for i in
                            newItems}
        allFoldersNeededInverted = {allFoldersNeeded[i]: i for i in allFoldersNeeded.keys()}

        for i in allFoldersNeeded.keys():
            if os.path.dirname(i) in allFoldersNeeded.values():
                dirname1 = os.path.dirname(i).replace('\\', '/')
                dirname2 = allFoldersNeededInverted[os.path.dirname(i).replace('\\', '/')]
                if dirname1 != dirname2:
                    newItems = [[i[0], i[1].replace(dirname1, dirname2)] for i in newItems]

        # properly sort the list
        newItemsDict = {i[0]: i[1] for i in newItems}
        newItemsSorted = sorted([i[0] for i in newItems])
        newItems = [[i, newItemsDict[i]] for i in newItemsSorted]

        # move the rest of the files and create new folders when needed
        for i in newItems:
            i = [i[0].replace('\\', '/'), i[1].replace('\\', '/')]
            if i[0].startswith('All'):
                prefixFolders = 1
            else:
                prefixFolders = 2

            splitFilePath = i[1].split('/')

            classFolders = '/'.join(splitFilePath[:(prefixFolders)])
            baseFolder = self.rootLocation + classFolders
            baseFolder = baseFolder.replace('\\', '/')

            if not os.path.isdir(baseFolder):
                os.mkdir(baseFolder)

            missingFolders = splitFilePath[prefixFolders:-1]
            for folderName in splitFilePath[prefixFolders:-1]:

                # check folders inside existing folder
                for folder in [dir for dir in os.listdir(baseFolder) if len(dir) == 3 and dir[0] not in ['.', '_']]:
                    nameFile = baseFolder + '/' + folder + '/_name.json'

                    if not os.path.exists(nameFile):
                        continue

                    if open(nameFile).read() == folderName:
                        baseFolder = baseFolder + '/' + folder
                        missingFolders = missingFolders[1:]
                        break

                # is the first folder wasn't found, don't bother lookign for its subfolder
                if missingFolders == splitFilePath[prefixFolders:-1]:
                    break

            # create the missing folders and put _name files in them
            for folder in missingFolders:
                currentFiles = [file[:3] for file in os.listdir(baseFolder) if file[0] not in ['.', '_']]
                baseFolder += '/' + str((len(currentFiles) + 1)).zfill(3)
                os.mkdir(baseFolder)
                shutil.copy(importedArchiveLocation + os.path.dirname(i[0]).replace('\\', '/') + '/_name.json',
                            baseFolder + '/_name.json')

            currentFiles = [file[:3] for file in os.listdir(baseFolder) if file[0] not in ['.', '_']]
            fileName = str((len(currentFiles) + 1)).zfill(3) + '.py'
            shutil.copy(importedArchiveLocation + '/' + i[0], baseFolder + '/' + fileName)

        # reinitiate
        self.buildClassesList()

    # --------------------------------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------------------------------

    def closeManager(self):
        self.close()
        global hotboxManagerInstance
        hotboxManagerInstance = None

    # --------------------------------------------------------------------------------------------------
    # open about widget
    # --------------------------------------------------------------------------------------------------

    def openAboutDialog(self):
        global aboutDialogInstance
        if aboutDialogInstance != None:
            aboutDialogInstance.close()
        aboutDialogInstance = AboutDialog()
        aboutDialogInstance.show()


# ------------------------------------------------------------------------------------------------------
# Classes List
# ------------------------------------------------------------------------------------------------------

class QListWidgetCustom(QtWidgets.QListWidget):

    def __init__(self, hotboxManager):
        super(QListWidgetCustom, self).__init__()

        self.enabled = False
        self.hotboxManager = hotboxManager

        self.buildClassesList = False
        self.itemChanged.connect(self.catchCheckboxChange)

    def setEnabled(self, mode=True):

        # only proceed if the mode will be changed
        if self.enabled == mode:
            return

        self.enabled = mode

        # change color
        color = [self.hotboxManager.lockedColor, self.hotboxManager.activeColor][int(mode)]
        self.setStyleSheet('background-color : %s' % color)

    def itemSelected(self):

        return bool(self.currentItem())

    def allItemNames(self):
        '''
        Return a list of all the items (text)
        '''
        return [self.item(index).text() for index in range(self.count())]

    def catchCheckboxChange(self):
        '''
        Function that get executed whenever an item is changed.
        '''

        # Only un when in Rules mode and when not building the list (so just when I user ticks the checkbox.)
        if self.hotboxManager.mode != 'Rules' or self.buildClassesList:
            return

        for index in range(self.count()):

            item = self.item(index)
            fileName = item.text()

            checkState = int(item.checkState())

            newRulePath, origRulePath = [self.hotboxManager.path + '/' + fileName + ('_' * index) for index in
                                         range(2)][::(checkState - 1)]

            if not os.path.exists(newRulePath):
                os.rename(origRulePath, newRulePath)
                break

    def focusInEvent(self, event):
        '''
        Actions executed when widget gains focus.
        '''

        # inherit default behaviour
        QtWidgets.QListWidget.focusOutEvent(self, event)

        if self.hotboxManager.mode == 'Rules' and not self.hotboxManager.rulesFlagCheckbox.isVisible():
            self.clearSelection()

        return True


# ------------------------------------------------------------------------------------------------------
# Color Swatch
# ------------------------------------------------------------------------------------------------------

class ColorSwatch(QtWidgets.QLabel):
    # signals
    save = QtCore.Signal()

    def __init__(self, defaultColor):
        super(ColorSwatch, self).__init__()

        self.color = None

        self.enabled = False
        self.active = False

        self.child = None
        self.parent = None

        self.size = 12
        self.setFixedHeight(self.size)
        self.setFixedWidth(self.size)

        self.painter = QtGui.QPainter()

        # set line color to black
        self.lineColor = '#000000'

        # painter
        self.paintPen = QtGui.QPen()
        self.paintPen.setColor(QtGui.QColor(0, 0, 0))
        self.paintPen.setWidthF(1.5)

        self.defaultColor = defaultColor
        self.defaultColorInverted = self.invertColor(self.defaultColor)
        self.lockedColor = '#262626'

        self.setColor(adjustChild=False, indirect=True)

        # Tooltip
        self.assignToolTip()

    def assignToolTip(self, child=False):
        '''
        Set the
        '''
        childSpecificToolTip = ['', '', '']

        if child:
            childSpecificToolTip = ['text ',
                                    " When set to default this color will adjust upon altering the button's color in order to remain readable."
                                    " This behaviour can be turned off by disabling 'Auto adjust text color' in the preferences",
                                    " Invert default color."]

        self.toolTipText = ("<p>Change the button's %scolor.</p>"
                            "<p>/ indicates the color is set to default.%s</p>"
                            "<ul>"
                            "<li><b>LMB</b> Open color picker to set a custom color.</li>"
                            "<li><b>RMB</b> Revert to default color.%s</li>"
                            "<li><b>CTRL + LMB</b>  Paste color from clipboard.</li>"
                            "<li><b>CTRL + RMB</b> Copy color to clipboard.</li>"
                            "<li><b>SHIFT + LMB</b> Set to color of selected node.</li>"
                            "<li><b>SHIFT + RMB</b> Copy color to clipboard, formatted as a 32bit integer.</li>"
                            "</ul>" % (childSpecificToolTip[0], childSpecificToolTip[1], childSpecificToolTip[2])
                            )

        self.setToolTip(self.toolTipText)

    # --------------------------------------------------------------------------------------------------
    # Events
    # --------------------------------------------------------------------------------------------------

    def saveEvent(self):
        '''
        Emit save signal that can be picked up by parent class
        '''
        self.save.emit()

    def enterEvent(self, event):
        '''
        Set Active to true when the mouse starts hovering over it
        '''
        if not self.enabled:
            return False

        self.active = True
        return True

    def leaveEvent(self, event):
        '''
        Set Active to false when the mouse stops hovering over it
        '''
        if self.enabled:
            self.active = False
        return False

    def mouseReleaseEvent(self, event):
        '''
        Set the color of the button
        '''
        if self.enabled and self.active:

            # Control key pressed
            if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ShiftModifier:

                # left click
                if event.button() == QtCore.Qt.LeftButton:
                    self.colorFromSelection()

                # right click
                else:
                    self.copyColorInterface()

            # Control key pressed
            elif QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:

                # left click
                if event.button() == QtCore.Qt.LeftButton:
                    # paste color form clipboard
                    self.pasteColorHex()

                # right click
                else:
                    # copy color to clipboard
                    self.copyColorHex()

            # Control key not pressed
            else:
                # left click
                if event.button() == QtCore.Qt.LeftButton:
                    # set custom color
                    self.getColor()

                # right click
                else:
                    # set to default
                    color = None

                    # if already set to default, toggle between inverted and regular
                    if self.parent:
                        if self.color == self.defaultColor:
                            color = self.defaultColorInverted

                    self.setColor(color)

            return True

        return False

    def dragEnterEvent(self, e):

        # check if color
        if e.mimeData().hasFormat('application/x-color') and self.enabled:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):

        # find color
        node = nuke.toNode(nuke.tcl('stack 0'))

        if not node:
            node = nuke.selectedNode()

        if not node:
            return

        interfaceColor = node.knob('tile_color').value()

        if interfaceColor == 0:
            interfaceColor = nuke.defaultNodeColor(node.Class())

        rgbColor = W_hotbox.interface2rgb(interfaceColor)
        color = W_hotbox.rgb2hex(rgbColor)

        self.setColor(color)

    # --------------------------------------------------------------------------------------------------
    # Color
    # --------------------------------------------------------------------------------------------------
    def setEnabled(self, mode):
        '''
        lock/unlock the colorswatch.
        '''

        self.enabled = mode
        self.setAcceptDrops(mode)
        self.setColor(adjustChild=False, indirect=True)

    def getColor(self):
        '''
        Open color dialog to let the user pick a color
        '''

        # convert current color to Nuke notation
        rgbColor = W_hotbox.hex2rgb(self.color)
        interfaceColor = W_hotbox.rgb2interface(rgbColor)

        color = nuke.getColor(interfaceColor)

        # if changed, proceed
        # ideally, you would register whenever the user cancels the color picker
        # usually cancel would return False. However...
        # when setting an initial color, pressing cancel wont return False no more...
        if not color == interfaceColor:
            rgbColor = W_hotbox.interface2rgb(color)
            hexColor = W_hotbox.rgb2hex(rgbColor)

            self.setColor(hexColor)

    def setColor(self, color=None, adjustChild=True, indirect=False):
        '''
        Set color of the swatch.
        'Indirect' parameter reflects whether the method was called directly by the user, or as a side effect.
        '''

        colorChanged = False

        # if swatch not enabled, set to locked color
        if not self.enabled:
            color = self.lockedColor

        else:
            # if no color specified, set to default color
            if not color:
                color = self.defaultColor

            # if new color is the same as the current color
            if color != self.color:
                colorChanged = True

        # set color
        self.color = color
        self.setStyleSheet('QLabel {border: 1px solid %s; background-color : %s}' % (self.lineColor, self.color))

        # set child color. If the color of the child was changed, make sure the colorChanged variable is forced to True
        if adjustChild:
            colorChanged = bool(colorChanged + self.setChildColor())

        # save changes to file if conditions are met.
        if self.enabled and colorChanged and not indirect:
            self.saveEvent()

    def setChildColor(self):
        '''
        Change the color of another colorswatch whenever this swatch changes color
        '''

        # check if its relevant to compare colors
        if not self.child or not preferencesNode.knob('hotboxAutoTextColor').value():
            return False

        if not self.isNonDefault(True) and self.child.isNonDefault():
            return False

        # if self is default, and child is default
        if not self.isNonDefault(True) and not self.child.isNonDefault():
            self.child.setColor(indirect=True)
            return True

        # parent color
        rgbParentColor = W_hotbox.hex2rgb(self.color)
        hsvParentColor = colorsys.rgb_to_hsv(rgbParentColor[0], rgbParentColor[1], rgbParentColor[2])

        # child color
        childColor = self.child.color
        rgbChildColor = W_hotbox.hex2rgb(childColor)
        hsvChildColor = list(colorsys.rgb_to_hsv(rgbChildColor[0], rgbChildColor[1], rgbChildColor[2]))

        # check if diffenence is significant enough to be readable
        threshold = 255 / 2

        if abs(hsvParentColor[2] - hsvChildColor[2]) < threshold:
            color = [self.child.defaultColorInverted, self.child.defaultColor][int(bool(self.child.isNonDefault(True)))]

            # set child color
            self.child.setColor(color, indirect=True)

            return True

        return False

    def isNonDefault(self, ignoreInverted=False):
        '''
        Return the current color. If that's similar to the default color, return None.
        '''

        if not ignoreInverted:
            # if set to inverted default
            if self.parent:
                if self.color == self.defaultColorInverted:
                    return None

        # if default
        if self.color == self.defaultColor:
            return None

        # else, return the current color
        else:
            return self.color

    def setChild(self, child):
        '''

        '''
        if isinstance(child, ColorSwatch):
            self.child = child
            self.child.parent = self
            self.child.assignToolTip(True)

    # --------------------------------------------------------------------------------------------------
    # Copy/Paste
    # --------------------------------------------------------------------------------------------------

    def copyColorHex(self):
        '''
        Copy current color to clipboard
        '''

        QtWidgets.QApplication.clipboard().setText(self.color)

    def copyColorInterface(self):
        '''
        Copy current color to clipboard, formatted as a 32 bit value as used by nuke for interface colors.
        '''

        # convert hex to interface
        rgbColor = W_hotbox.hex2rgb(self.color)
        color = str(W_hotbox.rgb2interface(rgbColor))

        QtWidgets.QApplication.clipboard().setText(color)

    def pasteColorHex(self):
        '''
        Paste color from clipboard
        '''

        color = QtWidgets.QApplication.clipboard().text()

        # check if clipboard content is a color formatted as a 32 bit value as used by nuke for interface colors.
        # if so, convert to hex
        if color.isdigit():
            rgbColor = W_hotbox.interface2rgb(int(color))
            color = W_hotbox.rgb2hex(rgbColor)

        # check if clipboard content is a valid hex color
        if re.search('^#(?:[0-9a-fA-F]{2}){3}$', color):
            self.setColor(color)

    def colorFromSelection(self):
        '''
        Set color to color of selected node
        '''

        selection = nuke.selectedNodes
        if not selection:
            return

        interfaceColor = W_hotbox.getTileColor()
        rgbColor = W_hotbox.interface2rgb(interfaceColor)
        color = W_hotbox.rgb2hex(rgbColor)

        self.setColor(color)

    # --------------------------------------------------------------------------------------------------
    # Line
    # --------------------------------------------------------------------------------------------------

    def invertColor(self, color):
        '''
        Retrun color with inverted brightness.
        '''

        rgbColor = W_hotbox.hex2rgb(color)
        hsvColor = list(colorsys.rgb_to_hsv(rgbColor[0], rgbColor[1], rgbColor[2]))

        hsvColor[2] = 255 - hsvColor[2]

        # convert back to hex
        # the rgb2hex function in the W_hotbox module expects normalized rgb values

        rgbColor = [float(value) / 255 for value in colorsys.hsv_to_rgb(hsvColor[0], hsvColor[1], hsvColor[2])]

        return W_hotbox.rgb2hex(rgbColor)

    def paintEvent(self, event):
        '''
        Draw diagonal line on top of colorswatch in case the swatch is set to it's default color.
        '''
        if self.enabled:
            # if default color paint diagonal line
            if not self.isNonDefault():
                self.painter.begin(self)
                self.painter.setPen(self.paintPen)
                self.painter.drawLine(self.size - 1, 1, 1, self.size - 1)
                self.painter.end()


# ------------------------------------------------------------------------------------------------------
# File Name
# ------------------------------------------------------------------------------------------------------

class ScriptEditorNameWidget(QtWidgets.QLineEdit):
    '''
    Subclassed QLineEdit.
    Added some functionality to check whether the text was changed and to save.
    '''

    # signals
    save = QtCore.Signal()

    def __init__(self):
        super(ScriptEditorNameWidget, self).__init__()

        self.savedText = ''
        self.editingFinished.connect(self.saveEvent)

    # --------------------------------------------------------------------------------------------------
    # Subclassed methods/events
    # --------------------------------------------------------------------------------------------------

    def saveEvent(self):
        '''
        Emit save signal that can be picked up by parent class.
        Make sure text is actually changed and valid before emitting a signal.
        '''

        # check if changed
        if self.text() != self.savedText:

            # if new name is valid, save to disk
            textFormatted = self.text().strip()
            if textFormatted:
                self.setText(textFormatted)
                self.save.emit()

            # if not valid, revert back to saved
            else:
                self.setText(self.savedText)

    def setText(self, text):
        '''
        Set text
        '''

        self.savedText = text
        # keep default behaviour
        QtWidgets.QLineEdit.setText(self, text)


# ------------------------------------------------------------------------------------------------------
# Script Editor
# ------------------------------------------------------------------------------------------------------

class ScriptEditorWidget(QtWidgets.QPlainTextEdit):
    '''
    Script editor widget.
    '''

    # signals
    save = QtCore.Signal()

    def __init__(self):
        super(ScriptEditorWidget, self).__init__()

        self.savedText = ''
        self.savedName = ''

        # Setup line numbers
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth()

        # highlight line
        self.textChanged.connect(self.highlightCurrentLine)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth()

    # --------------------------------------------------------------------------------------------------
    # events
    # --------------------------------------------------------------------------------------------------

    def focusOutEvent(self, event):
        '''
        Actions executed when widget loses focus.
        '''

        # inherit default behaviour
        QtWidgets.QPlainTextEdit.focusOutEvent(self, event)

        self.highlightCurrentLine()

        # save to file
        if not self.isReadOnly():
            if self.isChanged():
                self.save.emit()

        return True

    # indents

    def keyPressEvent(self, event):
        '''
        Custom actions for specific keystrokes
        '''

        # if Tab convert to Space
        if event.key() == 16777217:
            self.indentation('indent')

        # if Shift+Tab remove indent
        elif event.key() == 16777218:
            self.indentation('unindent')

        # if BackSpace try to snap to previous indent level
        elif event.key() == 16777219:
            if not self.unindentBackspace():
                QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

        # if shift+/ comment out current line(s) (toggle)
        elif event.key() == 47 and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            # QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
            self.toggleComment()

        # if enter or return, match indent level
        elif event.key() in [16777220, 16777221]:
            # QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
            self.indentNewLine()

        else:
            QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

    # --------------------------------------------------------------------------------------------------

    def isChanged(self):
        '''
        Check whether current text is the same as the text saved to disk.
        '''

        currentText = self.toPlainText()

        if currentText == self.savedText:
            return False

        return True

    def updateSavedText(self):
        '''
        Update the variable that holds the text as it is saved to disk.
        '''

        self.savedText = self.toPlainText()

    # --------------------------------------------------------------------------------------------------
    # Line Numbers

    # While researching the implementation of line numbers, I had a look at Nuke's Blinkscript interface.
    # This node has an excellent C++ editor, built with Qt.
    # The source code for that editor can be found here (or in Nuke's installation folder):
    # thefoundry.co.uk/products/nuke/developers/100/pythonreference/nukescripts.blinkscripteditor-pysrc.html
    # I stripped and modified the useful bits of the line number related parts of the code
    # and implemented it in the Hotbox Manager. Credits to theFoundry for writing the blinkscripteditor,
    # best example code I could have wished for.
    # --------------------------------------------------------------------------------------------------

    def lineNumberAreaWidth(self):
        digits = 1
        maxNum = max(1, self.blockCount())
        while (maxNum >= 10):
            maxNum //= 10
            digits += 1

        space = 7 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):

        if (dy):
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        QtWidgets.QPlainTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):

        if self.isReadOnly():
            return

        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QtGui.QColor(38, 38, 38))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        currentLine = self.document().findBlock(self.textCursor().position()).blockNumber()

        painter.setPen(self.palette().color(QtGui.QPalette.Text))

        while (block.isValid() and top <= event.rect().bottom()):

            # default grey
            textColor = QtGui.QColor(155, 155, 155)

            if blockNumber == currentLine and self.hasFocus():
                # current line
                textColor = QtGui.QColor(255, 170, 0, 255)

            painter.setPen(textColor)

            number = "%s " % str(blockNumber + 1)
            painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(), QtCore.Qt.AlignRight,
                             number)

            # Move to the next block
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    # --------------------------------------------------------------------------------------------------

    def getCursorInfo(self):

        self.cursor = self.textCursor()

        self.firstChar = self.cursor.selectionStart()
        self.lastChar = self.cursor.selectionEnd()

        self.noSelection = False
        if self.firstChar == self.lastChar:
            self.noSelection = True

        self.originalPosition = self.cursor.position()
        self.cursorBlockPos = self.cursor.positionInBlock()

    # --------------------------------------------------------------------------------------------------

    def unindentBackspace(self):
        '''
        snap to previous indent level
        '''

        self.getCursorInfo()

        if not self.noSelection or self.cursorBlockPos == 0:
            return False

        # check text in front of cursor
        textInFront = self.document().findBlock(self.firstChar).text()[:self.cursorBlockPos]

        # check whether solely spaces
        if textInFront != ' ' * self.cursorBlockPos:
            return False

        # snap to previous indent level
        spaces = len(textInFront)
        for space in range(spaces - ((spaces - 1) // 4) * 4 - 1):
            self.cursor.deletePreviousChar()

    def indentNewLine(self):
        '''
        Auto indent a new line
        '''

        # in case selection covers multiple line, make it one line first
        self.insertPlainText('')

        self.getCursorInfo()

        # check how many spaces after cursor
        text = self.document().findBlock(self.firstChar).text()

        textInFront = text[:self.cursorBlockPos]

        if len(textInFront) == 0:
            self.insertPlainText('\n')
            return

        indentLevel = 0
        for i in textInFront:
            if i == ' ':
                indentLevel += 1
            else:
                break

        indentLevel //= 4

        # find out whether textInFront's last character was a ':'
        # if that's the case add another indent.
        # ignore any spaces at the end, however also
        # make sure textInFront is not just an indent
        if textInFront.count(' ') != len(textInFront):
            while textInFront[-1] == ' ':
                textInFront = textInFront[:-1]

        if textInFront[-1] == ':':
            indentLevel += 1

        # new line
        self.insertPlainText('\n')
        # match indent
        self.insertPlainText(' ' * (4 * int(indentLevel)))

    def indentation(self, mode):
        '''
        Indent selected
        '''

        self.getCursorInfo()

        # if nothing is selected and mode is set to indent, simply insert as many
        # space as needed to reach the next indentation level.

        if self.noSelection and mode == 'indent':
            remainingSpaces = 4 - (self.cursorBlockPos % 4)
            self.insertPlainText(' ' * remainingSpaces)
            return

        selectedBlocks = self.findBlocks(self.firstChar, self.lastChar)
        beforeBlocks = self.findBlocks(last=self.firstChar - 1, exclude=selectedBlocks)
        afterBlocks = self.findBlocks(first=self.lastChar + 1, exclude=selectedBlocks)

        beforeBlocksText = self.blocks2list(beforeBlocks)
        selectedBlocksText = self.blocks2list(selectedBlocks, mode)
        afterBlocksText = self.blocks2list(afterBlocks)

        combinedText = '\n'.join(beforeBlocksText + selectedBlocksText + afterBlocksText)

        # make sure the line count stays the same
        originalBlockCount = len(self.toPlainText().split('\n'))
        combinedText = '\n'.join(combinedText.split('\n')[:originalBlockCount])

        self.clear()
        self.setPlainText(combinedText)

        self.restoreSelection()

    def toggleComment(self):
        '''
        Disable a line by putting  a # in front of it.
        '''

        self.getCursorInfo()

        selectedBlocks = self.findBlocks(self.firstChar, self.lastChar)
        beforeBlocks = self.findBlocks(last=self.firstChar - 1, exclude=selectedBlocks)
        afterBlocks = self.findBlocks(first=self.lastChar + 1, exclude=selectedBlocks)

        beforeBlocksText = self.blocks2list(beforeBlocks)
        selectedBlocksText = self.blocks2list(selectedBlocks, 'comment')
        afterBlocksText = self.blocks2list(afterBlocks)

        combinedText = '\n'.join(beforeBlocksText + selectedBlocksText + afterBlocksText)

        # make sure the line count stays the same
        originalBlockCount = len(self.toPlainText().split('\n'))
        combinedText = '\n'.join(combinedText.split('\n')[:originalBlockCount])

        self.clear()
        self.setPlainText(combinedText)

        self.restoreSelection()

    def restoreSelection(self):
        '''
        Restore the original selection and cursor posiftion modifing the text.
        '''

        if self.noSelection:
            self.cursor.setPosition(self.lastChar)

        # check whether the the original selection was from top to bottom or vice versa
        else:
            if self.originalPosition == self.firstChar:
                first = self.lastChar
                last = self.firstChar
                firstBlockSnap = QtGui.QTextCursor.EndOfBlock
                lastBlockSnap = QtGui.QTextCursor.StartOfBlock
            else:
                first = self.firstChar
                last = self.lastChar
                firstBlockSnap = QtGui.QTextCursor.StartOfBlock
                lastBlockSnap = QtGui.QTextCursor.EndOfBlock

            self.cursor.setPosition(first)
            self.cursor.movePosition(firstBlockSnap, QtGui.QTextCursor.MoveAnchor)
            self.cursor.setPosition(last, QtGui.QTextCursor.KeepAnchor)
            self.cursor.movePosition(lastBlockSnap, QtGui.QTextCursor.KeepAnchor)

        self.setTextCursor(self.cursor)
        # --------------------------------------------------------------------------------------------------

    def findBlocks(self, first=0, last=None, exclude=[]):
        '''
        Divide text in blocks
        '''

        blocks = []
        if last == None:
            last = self.document().characterCount()
        for pos in range(first, last + 1):
            block = self.document().findBlock(pos)
            if block not in blocks and block not in exclude:
                blocks.append(block)
        return blocks

    def blocks2list(self, blocks, mode=None):
        '''
        Convert a block to a string.
        If a mode is specified, preform custom modification to the text.
        '''

        text = []

        toggle = None

        for block in blocks:

            blockText = block.text()

            # ------------------------------------------------------------------------------------------

            if mode == 'unindent':

                if blockText.startswith(' ' * 4):
                    blockText = blockText[4:]
                    self.lastChar -= 4

                elif blockText.startswith('\t'):
                    blockText = blockText[1:]
                    self.lastChar -= 1

            # ------------------------------------------------------------------------------------------

            elif mode == 'indent':
                blockText = ' ' * 4 + blockText
                self.lastChar += 4

            # ------------------------------------------------------------------------------------------

            elif mode == 'comment':

                unindentedBlockText = blockText.lstrip()
                indents = len(blockText) - len(unindentedBlockText)

                if toggle is None:
                    toggle = not unindentedBlockText.startswith('#')

                # kill comment
                if unindentedBlockText.startswith('# '):
                    unindentedBlockText = unindentedBlockText[2:]

                elif unindentedBlockText.startswith('#'):
                    unindentedBlockText = unindentedBlockText[1:]

                # combine
                blockText = (' ' * indents) + ('# ' * int(toggle)) + unindentedBlockText

            # ------------------------------------------------------------------------------------------

            text.append(blockText)

        return text

    # --------------------------------------------------------------------------------------------------
    # current line hightlighting
    # --------------------------------------------------------------------------------------------------

    def highlightCurrentLine(self):
        '''
        Highlight currently selected line
        '''

        extraSelections = []

        selection = QtWidgets.QTextEdit.ExtraSelection()

        lineColor = QtGui.QColor(88, 88, 88, 255)

        if not self.hasFocus() or self.isReadOnly():
            lineColor.setAlpha(0)

        selection.format.setBackground(lineColor)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extraSelections.append(selection)

        self.setExtraSelections(extraSelections)


class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, scriptEditor):
        super(LineNumberArea, self).__init__(scriptEditor)

        self.scriptEditor = scriptEditor
        self.setStyleSheet("text-align: center;")

    def paintEvent(self, event):
        self.scriptEditor.lineNumberAreaPaintEvent(event)
        return


class ScriptEditorHighlighter(QtGui.QSyntaxHighlighter):
    '''
    Modified, simplified version of some code found I found when researching:
    wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
    They did an awesome job, so credits to them. I only needed to make some
    modifications to make it fit my needs.
    '''

    def __init__(self, document):

        super(ScriptEditorHighlighter, self).__init__(document)

        self.styles = {
            'keyword': self.format([238, 117, 181], 'bold'),
            'string': self.format([242, 136, 135]),
            'comment': self.format([143, 221, 144]),
            'numbers': self.format([174, 129, 255]),
            'placeholders': self.format([255, 190, 0]),
        }

        self.keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'with', 'yield'
        ]

        self.operatorKeywords = [
            '=', '==', '!=', '<', '<=', '>', '>=',
            '\+', '-', '\*', '/', '//', '\%', '\*\*',
            '\+=', '-=', '\*=', '/=', '\%=',
            '\^', '\|', '\&', '\~', '>>', '<<'
        ]

        self.numbers = ['True', 'False', 'None']

        self.tri_single = (QtCore.QRegExp("'''"), 1, self.styles['comment'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, self.styles['comment'])

        self.placeholders = [
            'KNOBNAME', 'NODECLASS', 'NODENAME', 'VALUE', 'EXPRESSION'
        ]

        # rules
        rules = []

        rules += [(r'\b%s\b' % i, 0, self.styles['keyword']) for i in self.keywords]
        rules += [(r'\b%s\b' % i, 0, self.styles['placeholders']) for i in self.placeholders]
        rules += [(i, 0, self.styles['keyword']) for i in self.operatorKeywords]
        rules += [(r'\b%s\b' % i, 0, self.styles['numbers']) for i in self.numbers]

        rules += [

            # integers
            (r'\b[0-9]+\b', 0, self.styles['numbers']),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['string']),
            # From '#' until a newline
            (r'#[^\n]*', 0, self.styles['comment']),
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QtCore.QRegExp(pat), index, fmt) for (pat, index, fmt) in rules]

    def format(self, rgb, style=''):
        '''
        Return a QtGui.QTextCharFormat with the given attributes.
        '''

        color = QtGui.QColor(*rgb)
        textFormat = QtGui.QTextCharFormat()
        textFormat.setForeground(color)

        if 'bold' in style:
            textFormat.setFontWeight(QtGui.QFont.Bold)
        if 'italic' in style:
            textFormat.setFontItalic(True)

        return textFormat

    def highlightBlock(self, text):
        '''
        Apply syntax highlighting to the given block of text.
        '''
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.matchMultiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.matchMultiline(text, *self.tri_double)

    def matchMultiline(self, text, delimiter, in_state, style):
        '''
        Check whether highlighting requires multiple lines.
        '''
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(text)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False Otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False


# ------------------------------------------------------------------------------------------------------
# Template Button
# ------------------------------------------------------------------------------------------------------

class ScriptEditorTemplateMenu(QtWidgets.QMenu):

    def __init__(self, parentObject):

        super(ScriptEditorTemplateMenu, self).__init__()

        self.hotbox = parentObject

        # set default template folder
        folder = preferencesNode.knob('hotboxLocation').value()
        if folder[-1] != '/':
            folder += '/'
        self.templateFolder = folder + 'Templates'

        self.initMenu()

    def initMenu(self):

        self.clear()
        self.menuItems = []

        # add menu entries pointing to templates stored on disk
        self.addUserTemplates(folder=self.templateFolder)

        self.addSeparator()

        # add function to manage templates
        self.addQAction(self, 'Save current script as template', self.saveAsTemplate)
        self.addQAction(self, 'Manage templates', self.hotbox.toggleTemplateMode)

    def addUserTemplates(self, folder, parent=None):
        '''
        Scan template folder and add an item for every template.
        '''

        if not parent:
            parent = self

        for path in [folder + '/' + file for file in os.listdir(folder) if file[0] not in ['_', '.']]:

            name = getAttributeFromFile(path)

            # make sure name won't be longer than 'Save current script as template'
            maxNameLength = 31

            # file
            if os.path.isfile(path):

                # trim name if to long
                if len(name) > maxNameLength:
                    name = name[:maxNameLength - 3] + '...'

                self.addQAction(parent, name, path)

            # dir
            else:

                # trim name if to long
                maxNameLength -= 3
                if len(name) > maxNameLength:
                    name = name[:maxNameLength - 3] + '...'

                # create new QMenu
                menu = QtWidgets.QMenu()
                menu.setTitle(name)

                # add QMenu to parent
                parent.addMenu(menu)
                self.menuItems.append(menu)

                # Run this function again, with new Qmenu as menu
                self.addUserTemplates(parent=menu, folder=path)

    def addQAction(self, parent, name, function):
        '''
        Create new action and add to menu.
        '''

        # create new QAction
        action = QtWidgets.QAction(parent)
        action.setText(name)

        # bind function

        # if a script is passed instead of a function, turn it into a function
        if not callable(function):
            script = function
            function = lambda: self.insertTemplate(script)

        action.triggered.connect(function)

        # addToMenu
        parent.addAction(action)
        self.menuItems.append(action)

    def insertTemplate(self, path):
        '''
        Insert template script into script editor
        '''

        # get script
        template = getScriptFromFile(path)

        # add proper indentation
        template = self.adjustTemplate(template)

        self.hotbox.scriptEditorScript.insertPlainText(template)

    def saveAsTemplate(self):
        '''
        Save current script as a template
        '''

        self.hotbox.saveScriptEditor(True)

    def adjustTemplate(self, script):
        '''
        Modify template script based on current cursor position
        '''
        cursor = self.hotbox.scriptEditorScript.textCursor()
        cursorPosition = cursor.positionInBlock()

        textBeforeCursor = cursor.block().text()[:cursorPosition]
        textBeforeCursorNoIndent = textBeforeCursor.lstrip()

        # if cursor at beginning of block, return original script
        if textBeforeCursor == '':
            return script

        # find current indentation, rounded by 4
        indentLevel = ' ' * (4 * ((len(textBeforeCursor) - len(textBeforeCursorNoIndent)) // 4))

        if textBeforeCursorNoIndent != '':
            script = '\n' + script

        script = script.replace('\n', '\n' + indentLevel)

        return script

    def enableMenuItems(self):
        '''
        Enable items based on state of script editor.
        '''

        # check if script editor widget is accessible
        mode = 1 - self.hotbox.scriptEditorScript.isReadOnly()

        # skip last item (enter template mode)
        for menuItem in self.menuItems[:-1]:
            menuItem.setEnabled(mode)


# ------------------------------------------------------------------------------------------------------
# Tree View
# ------------------------------------------------------------------------------------------------------

class QTreeViewCustom(QtWidgets.QTreeView):
    def __init__(self, parentClass):

        super(QTreeViewCustom, self).__init__()

        self.enabled = False

        self.clipboard = []

        self.parentClass = parentClass

        self.header().hide()
        self.expandsOnDoubleClick = True

        self.dataModel = QtGui.QStandardItemModel()
        self.root = self.dataModel.invisibleRootItem()

        self.setModel(self.dataModel)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        # to check whether the tree was populated from scratch of updated
        self.scope = ''
        self.previousScope = ''

        # Unfortunatley Nuke 10 crashes on startup when using the following line:
        # self.selectionModel().selectionChanged.connect(self.setSelectedItems)
        # Therefore I had to do this weird construction where the setModel Method is subclassed.

    # --------------------------------------------------------------------------------------------------

    def setModel(self, model):
        super(QTreeViewCustom, self).setModel(model)
        self.connect(self.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
                     self.setSelectedItems)

    # --------------------------------------------------------------------------------------------------

    def setEnabled(self, mode=True):

        self.enabled = mode

        # change color
        color = [self.parentClass.lockedColor, self.parentClass.activeColor][int(mode)]
        self.setStyleSheet('background-color : %s' % color)

    def populateTree(self):
        '''
        Fill the QTreeView with items associated with the selected nodeclass
        '''

        # store current scope as previous scope
        self.previousScope = self.scope

        self.setEnabled(True)

        # find current scope
        if not self.parentClass.contextual:
            self.scope = self.parentClass.path + '/'

        else:

            classItems = self.parentClass.classesList.selectedItems()
            if len(classItems) == 0:
                self.setEnabled(False)
                return

            classItem = classItems[0]
            classItemText = classItem.text()

            if self.parentClass.mode == 'Rules':
                if not int(classItem.checkState()):
                    classItemText += '_'

            self.scope = self.parentClass.path + '/' + classItemText + '/'

        if self.previousScope == self.scope:
            self.update = True
        else:
            self.update = False

        if self.update:
            # find currently collapsed menus
            self.collapsedMenus = []

            for button in self.buttonsList.values():

                index = self.dataModel.indexFromItem(button)

                if not self.isExpanded(index):
                    self.collapsedMenus.append(button.path)

        # ----------------------------------------------------------------------------------------------

        # reset buttons list (all items will be replaced with new items when rebuilding anyway)
        self.buttonsList = {}
        self.clearTree()

        # Fill the buttonstree if there is an item selected in the classescolumn, or the mode is set to all.
        if not self.parentClass.contextual or self.parentClass.classesList.selectedItems() != 0:
            self.addChild(self.root, self.scope)

        # Expand/Collapse
        self.expandAll()

        # closeall the menus when updating
        if self.update:
            for path in self.collapsedMenus:
                if path in self.buttonsList.keys():
                    button = self.buttonsList[path]
                    index = self.dataModel.indexFromItem(button)
                    self.collapse(index)

        self.parentClass.toggleRulesMode()

    def clearTree(self):
        '''
        empty the tree
        self.dataModel.clear() unfortunately this  Nuke
        '''
        for row in range(self.dataModel.rowCount()):
            self.dataModel.takeRow(0)

    def addChild(self, parent, path):
        '''
        Loop through folder structure and add items on the fly
        '''

        for i in sorted(os.listdir(path)):
            if i[0] not in ['_', '.']:

                if path[-1] != '/':
                    path += '/'

                filePath = path + i

                name = getAttributeFromFile(filePath)

                if not name:
                    return

                child = QStandardItemChild(name, filePath)
                parent.appendRow(child)

                # store in the list for easy access
                self.buttonsList[filePath] = child

                if os.path.isdir(filePath):
                    self.addChild(child, filePath)

    def setSelectedItems(self):
        '''
        Run when items gets selected
        '''
        self.selectedItems = [index.model().itemFromIndex(index) for index in self.selectedIndexes()]
        self.selectedItemsPaths = set([i.path for i in self.selectedItems])
        self.parentClass.loadScriptEditor()
        self.parentClass.toggleRulesMode(False)

    def moveItem(self, direction):
        '''
        Change the order of buttons by clicking the up/down buttons
        '''

        # get currently selected index and item
        self.currentItem = self.selectedItems[0]
        self.currentIndex = self.currentItem.index()

        # get target index and item
        self.getNextIndex(direction, self.currentIndex)

        # if direction was set to three, the item is supposed to leave the subdir from the top.
        if direction == 2:
            direction = 0

        # if current item is the first or last (depending on direction) in list
        # abort the operation, as theres no point in trying to move
        if self.nextItem is None:
            return

        sourceFolder = os.path.dirname(self.currentItem.path)
        sourceFile = os.path.basename(self.currentItem.path)

        destinationFolder = os.path.dirname(self.nextItem.path)
        destinationFile = os.path.basename(self.nextItem.path)

        if sourceFolder == destinationFolder:
            # stay in same (sub)menu
            filesSourceFolder = []
            filesDestinationFolder = [destinationFile]

        else:
            filesSourceFolder = self.indexFolder(sourceFolder)
            filesDestinationFolder = self.indexFolder(destinationFolder)

            if sourceFolder == sorted([sourceFolder, destinationFolder])[0]:
                # enter submenu
                filesSourceFolder = filesSourceFolder[filesSourceFolder.index(sourceFile):]

                if not direction:
                    # if entering a subfolder from the bottom
                    filesDestinationFolder = []
                    # +1 to name of the file, so the source file will appear at the bottom of the submenu
                    # without overwriting the dest item
                    destinationFile = str(int(destinationFile[:3]) + 1).zfill(3) + destinationFile[3:]
            else:

                if direction:
                    # if exiting a subfolder at the bottom
                    filesSourceFolder = []
                else:
                    # exit submenu at top
                    filesDestinationFolder = filesDestinationFolder[filesDestinationFolder.index(destinationFile):]

        if sourceFile in filesSourceFolder:
            filesSourceFolder.remove(sourceFile)

        # make sure destination is same type (file/submenu) as the file being moved
        # if len = 6 (###.py) it's a file, otherwise it must be a submenu (###)
        sourceType = len(sourceFile) == 6
        destinationType = len(destinationFile) == 6

        if destinationType != sourceType:
            if sourceType:
                destinationFile = destinationFile + '.py'
            else:
                destinationFile = destinationFile[:3]

        tmpExtention = '_tmp'

        # temporarily rename affected files in affected folders

        tmpFiles = [[], []]

        files = [filesDestinationFolder, filesSourceFolder]

        folders = [destinationFolder, sourceFolder]

        for index in range(2):

            for file in files[index]:

                tmpFile = file + tmpExtention
                tmpFiles[index].append(tmpFile)

                folder = folders[index]
                origPath = folder + '/' + file
                tmpPath = folder + '/' + tmpFile

                # rename files and update lookupTable to keep track of files
                self.renameButton(origPath, tmpPath)

                # if removing a file from a menu by it's top, the submenu will have to be renamed (as the file will take
                # the menu's place). When renaming this menu, we have to update the paths of the source folder as well,
                # otherwise we will not be able to find the files anymore.

                if origPath == folders[1 - index]:
                    folders[1 - index] = tmpPath

        # rename mainfile

        origPath = folders[1] + '/' + sourceFile
        newPath = folders[0] + '/' + destinationFile

        self.renameButton(origPath, newPath)
        # save to restore selection later on
        targetItem = newPath

        # give all the tmp files proper names

        for index in range(2):

            folder = folders[index]

            currentFiles = [i[:3] for i in self.indexFolder(folder)]

            file = '001'

            for tmpFile in tmpFiles[index]:

                # submenu or button
                extension = ''
                if '.' in tmpFile:
                    extension = '.py'

                while file in currentFiles:
                    file = str(int(file) + 1).zfill(3)

                currentFiles.append(file)

                origPath = folder + '/' + tmpFile
                newPath = folder + '/' + file + extension

                # when moving a file from a submenu, make sure the source folder gets renamed after renaming the tmp'd
                # submene, otherwise the tmp'd files living inside that submenu cannot be found.
                if index == 0 and extension == '' and origPath == folders[1]:
                    folders[1] = newPath

                if origPath == folders[0]:
                    targetItem = newPath + '/' + destinationFile

                self.renameButton(origPath, newPath)

        self.populateTree()

        self.restoreSelection(targetItem)

    def renameButton(self, origPath, newPath):
        '''
        Rename files and update paths to keep track of buttons
        '''
        # rename actual file
        os.rename(origPath, newPath)

        # update path for button objects

        for path in [path for path in self.buttonsList.keys() if path.startswith(origPath)]:
            button = self.buttonsList[path]

            updatedPath = path.replace(origPath, newPath)
            button.path = updatedPath

            # add updated path to dict
            self.buttonsList[updatedPath] = button

            # delete outdated path from dict
            del self.buttonsList[path]

    def restoreSelection(self, path=''):

        if not path:
            return
        if not os.path.exists(path):
            return

        # restore selection
        self.setCurrentIndex(self.buttonsList[path].index())

    def indexFolder(self, folder):
        '''
        Return a list of files currently present in a given folder.
        Only properly named files will be returned.
        '''
        files = []
        for file in os.listdir(folder):
            if file[0] not in ['_', '.'] and len(file) in [3, 6]:
                files.append(file)

        return files

    def getNextIndex(self, direction, index):
        '''
        Get the index of the item next to the current item
        '''

        if direction == 2:
            self.nextItem = self.currentItem.parent()

        else:
            if direction:

                # if current item is the submenu and the move-down button is triggered
                forceExpanded = False
                if not os.path.isfile(self.currentItem.path):

                    item = self.dataModel.itemFromIndex(index)

                    if self.isExpanded(index) and item.hasChildren():
                        self.setExpanded(index, False)
                        forceExpanded = True

                self.nextIndex = self.indexBelow(index)

                if forceExpanded:
                    self.setExpanded(index, True)

            else:
                self.nextIndex = self.indexAbove(index)

            self.nextItem = self.dataModel.itemFromIndex(self.nextIndex)

            # if moving down and current item is last item in a subfolder with no item underneath it.
            if self.nextItem is None and direction:
                parentItem = self.currentItem.parent()
                if parentItem is not None:
                    newBaseName = str(int(os.path.basename(parentItem.path)) + 1).zfill(3)
                    parentItem.path = os.path.dirname(parentItem.path) + '/' + newBaseName
                    self.nextItem = parentItem

            # exit
            if self.nextItem is None:
                return

            # if submenu
            # skip item if expanded
            if os.path.dirname(self.nextItem.path) == os.path.dirname(self.currentItem.path):
                if not os.path.isfile(self.nextItem.path):
                    if not self.nextItem.hasChildren():
                        self.nextItem.path += '/001' + os.path.basename(self.currentItem.path)[3:]
                    else:
                        if direction:
                            if self.isExpanded(self.nextIndex) and self.nextItem.hasChildren():
                                self.getNextIndex(direction, self.nextIndex)

    # --------------------------------------------------------------------------------------------------
    # hotbox items tree actions
    # --------------------------------------------------------------------------------------------------

    def addItem(self, folder=False):
        '''
        Create new item for selected nodeclass
        '''

        folderPath = self.scope

        # if item selected, place the new underneath
        selectedIndexes = self.selectedIndexes()
        if len(selectedIndexes) != 0:
            selectedItem = self.dataModel.itemFromIndex(selectedIndexes[0])
            folderPath = os.path.dirname(selectedItem.path) + '/'

        # make sure all the files inside the folder are named correctly
        RepairHotbox(folder=folderPath, recursive=False, message=False)

        # loop over content of folder to find an appropriate name for the new item
        itemPath = getFirstAvailableFilePath(folderPath)

        if not folder:

            itemName = 'New Item'
            itemPath += '.py'

            newFileContent = FileHeader(itemName).getHeader()
            currentFile = open(itemPath, 'w')
            currentFile.write(newFileContent)
            currentFile.close()

        else:
            itemName = 'New Menu'

            os.mkdir(itemPath)
            currentFile = open(itemPath + '/_name.json', 'w')
            currentFile.write(itemName)
            currentFile.close()

        self.populateTree()

        self.restoreSelection(itemPath)

    def removeItem(self):
        '''
        Move selected item to the _old folder.
        '''

        selectedIndex = self.selectedIndexes()[0]
        currentItem = self.dataModel.itemFromIndex(selectedIndex)

        # find next item to be selected after current item is deleted
        nextItemPath = None

        nextItem = self.dataModel.itemFromIndex(self.indexBelow(selectedIndex))
        if nextItem is None:
            nextItem = self.dataModel.itemFromIndex(self.indexAbove(selectedIndex))

        if nextItem is not None:
            nextItemPath = nextItem.path

        # remove selected file
        oldFolder = self.scope + '_old/'

        if not os.path.isdir(oldFolder):
            os.mkdir(oldFolder)

        currentTime = dt.now().strftime('%Y%m%d%H%M%S')
        newFileName = currentTime

        counter = 1
        while newFileName in sorted(os.listdir(oldFolder)):
            newFileName = currentTime + '_%s' % str(counter).zfill(3)
            counter += 1

        shutil.move(currentItem.path, oldFolder + newFileName)

        # make sure all the files inside the folder are named correctly
        changedFolder = os.path.dirname(currentItem.path)
        RepairHotbox(folder=changedFolder, recursive=False, message=False)

        self.populateTree()

        self.restoreSelection(nextItemPath)

    def copyItem(self):
        '''
        Place the selected items in the class' clipboard
        '''
        try:
            self.clipboard = []

            for path in self.selectedItemsPaths:
                self.clipboard.append(path)
        except:
            pass

    def pasteItem(self):
        '''
        Copy the items stored in the class' clipboard to the current folder
        '''

        if len(self.clipboard) > 0:

            # make sure all the files inside the folder are named correctly
            RepairHotbox(folder=self.scope, recursive=False, message=False)

            for path in self.clipboard:

                fileList = sorted([i[:3] for i in os.listdir(os.path.dirname(path)) if i[0] not in ['.', '_']])

                newFileName = '001'

                counter = 1
                while newFileName in fileList:
                    counter += 1
                    newFileName = str(counter).zfill(3)

                newPath = self.scope + newFileName

                # if file
                if path.endswith('.py'):
                    newPath += '.py'
                    shutil.copy2(path, newPath)

                # if menu
                else:
                    shutil.copytree(path, newPath)

            self.populateTree()

            self.restoreSelection(newPath)

    def duplicateItem(self):
        '''
        Duplicate the currently selected items.
        '''
        tmpClipboard = self.clipboard
        self.copyItem()
        self.pasteItem()
        self.clipboard = tmpClipboard


class QStandardItemChild(QtGui.QStandardItem):
    def __init__(self, name, path):

        super(QStandardItemChild, self).__init__()

        # self.richTextName = name

        # convert rich text to plain text

        if '<' in name:

            richToPlain = re.compile('<[^>]*>').sub('', name)

            if len(richToPlain) > 0:
                name = richToPlain
            else:
                # if image tag was used
                if 'img ' in name:
                    richToPlain = name.replace(' ', '').replace('<imgsrc=', '').replace("'", '"')
                    richToPlain = richToPlain.split('">')[0]
                    richToPlain = os.path.basename(richToPlain)
                    if len(richToPlain) > 0:
                        name = richToPlain

        # if the name has a whitespace at the beginning due to the conversion to plain text, get rid of them.
        while name.startswith(' '):
            name = name[1:]

        self.setText(name)

        # path points to the place the file is currently stored
        # parent points to the place in the gui

        self.path = path

        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        # change color is submenu
        if os.path.isdir(self.path):
            self.setBackground(QtGui.QColor(45, 45, 45))

        parentObject = self.parent()
        if parentObject != None:
            self.currentGuiPath = parentObject.path


class QLabelButton(QtWidgets.QLabel):
    '''
    Custom class to make a Qlabel function as a button.
    '''

    # signals
    clicked = QtCore.Signal()

    def __init__(self, name, linkedWidget=None):
        super(QLabelButton, self).__init__()

        self.linkedWidget = linkedWidget

        iconFolder = preferencesNode.knob('hotboxIconLocation').value()

        while iconFolder[-1] == '/':
            iconFolder = iconFolder[:-1]

        self.imageFile = '%s/hotbox_%s' % (iconFolder, name)

        # check if icon is present. If not, display '?'
        if not os.path.isfile('%s_neutral.png' % self.imageFile):
            self.imageFile = None

            self.setText('<font size = "6">?</font>')
            self.setAlignment(QtCore.Qt.AlignCenter)
            self.setStyleSheet('color: #717171')

        # add image
        else:
            self.updateIcon()

        # format name
        if name != name.lower():

            newName = ''

            for character in name:
                if character in string.ascii_uppercase:
                    character = ' ' + character.lower()
                newName = newName + character

            name = newName

        # tooltip
        self.setToolTip(name)

    # --------------------------------------------------------------------------------------------------
    # Events
    # --------------------------------------------------------------------------------------------------

    def enterEvent(self, event):
        self.updateIcon('hover')

    def leaveEvent(self, event):
        self.updateIcon()

    def mousePressEvent(self, event):
        self.updateIcon('clicked')

    def mouseReleaseEvent(self, event):
        # emit signal

        self.updateIcon('hover')

        # if button has a linkedwidget set, check if that widget is enabled.
        # if not, dont emit clicked signal

        if self.linkedWidget:
            if not self.linkedWidget.enabled:
                return

        self.clicked.emit()

    # --------------------------------------------------------------------------------------------------

    def updateIcon(self, mode='neutral'):

        if self.imageFile:
            path = '%s_%s.png' % (self.imageFile, mode)
            self.setPixmap(QtGui.QPixmap(path))


# ------------------------------------------------------------------------------------------------------
# rename  dialog
# ------------------------------------------------------------------------------------------------------

class RenameDialog(QtWidgets.QDialog):
    '''
    Dialog that will pop up when the rename button in the manager is clicked.
    '''

    def __init__(self, currentName, new=False):

        super(RenameDialog, self).__init__()

        self.currentName = currentName

        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)

        self.new = new

        self.hotboxManager = hotboxManagerInstance

        # list of all items currently in list
        self.allItems = self.hotboxManager.classesList.allItemNames()
        if self.currentName in self.allItems:
            self.allItems.remove(self.currentName)

        enitity = 'Class'
        if self.hotboxManager.mode == 'Rules':
            enitity = 'Rule'

        # window title
        if self.new:
            renameButtonLabel = 'Create'
            self.setWindowTitle('New ' + enitity)

        else:
            renameButtonLabel = 'Rename'
            self.setWindowTitle('Rename ' + enitity)

        # layout
        masterLayout = QtWidgets.QVBoxLayout()
        buttonsLayout = QtWidgets.QHBoxLayout()

        self.newNameLineEdit = QtWidgets.QLineEdit()
        self.newNameLineEdit.setText(self.currentName)
        self.newNameLineEdit.selectAll()

        self.newNameLineEdit.textChanged.connect(self.validateName)

        self.renameButton = QtWidgets.QPushButton(renameButtonLabel)
        cancelButton = QtWidgets.QPushButton('Cancel')

        self.renameButton.clicked.connect(self.renameButtonClicked)
        cancelButton.clicked.connect(self.cancelRenameDialog)

        for button in [self.renameButton, cancelButton]:
            buttonsLayout.addWidget(button)

        masterLayout.addWidget(self.newNameLineEdit)
        masterLayout.addLayout(buttonsLayout)
        self.setLayout(masterLayout)

        # shortcuts
        self.enterAction = QtWidgets.QAction(self)
        self.enterAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return))
        self.enterAction.triggered.connect(self.renameButtonClicked)
        self.addAction(self.enterAction)

        # move to screen center
        self.adjustSize()
        screenRes = QtWidgets.QDesktopWidget().screenGeometry()
        self.move(QtCore.QPoint(screenRes.width() // 2, screenRes.height() // 2) - QtCore.QPoint((self.width() // 2),
                                                                                                 (self.height() // 2)))

    def validateName(self):
        '''
        Check the imput name and disable the 'Rename button' accordingly.
        '''
        text = self.newNameLineEdit.text()
        valid = True

        try:

            valid *= text not in self.allItems
            valid *= len(text) > 0
            valid *= text[-1] != '_'
            valid *= text[0] != '_'
        except:

            valid = False

        self.renameButton.setEnabled(valid)

    def renameButtonClicked(self):

        currentPath = self.hotboxManager.path + '/' + self.currentName
        newPath = self.hotboxManager.path + '/' + self.newNameLineEdit.text()

        if currentPath != newPath:
            counter = 1
            while os.path.isdir(newPath):

                splitPath = os.path.basename(newPath).split('_')
                if len(splitPath) > 1:
                    suffix = splitPath[-1]
                    if suffix.isdigit():
                        counter = int(suffix) + 1

                newPath = self.hotboxManager.path + '/' + self.newNameLineEdit.text() + '_%s' % counter
                counter += 1

            shutil.move(currentPath, newPath)

            self.hotboxManager.buildClassesList(os.path.basename(newPath))

        self.closeRenameDialog()

    def cancelRenameDialog(self):
        if self.new:
            self.hotboxManager.removeClass(self.currentName)

        self.closeRenameDialog()

    def closeRenameDialog(self):
        self.close()
        global renameDialogInstance
        renameDialogInstance = None
        return False


# ------------------------------------------------------------------------------------------------------
# Dialog with contact informaton
# ------------------------------------------------------------------------------------------------------

class AboutDialog(QtWidgets.QFrame):
    '''
    Dialog that will show some information about the current version of the Hotbox.
    '''

    def __init__(self):

        super(AboutDialog, self).__init__()

        self.setWindowFlags(QtCore.Qt.ToolTip)

        self.setFixedHeight(250)
        self.setFixedWidth(230)

        self.setFrameStyle(QtWidgets.QFrame.Plain | QtWidgets.QFrame.StyledPanel)

        # logo
        aboutHotbox = QtWidgets.QLabel()
        aboutIcon = preferencesNode.knob('hotboxIconLocation').value().replace('\\', '/') + '/icon.png'
        aboutIcon = aboutIcon.replace('//icon.png', '/icon.png')
        aboutHotbox.setPixmap(QtGui.QPixmap(aboutIcon))

        # version
        aboutVersion = QtWidgets.QLabel(version)
        aboutDate = QtWidgets.QLabel(releaseDate)

        # clickable links
        aboutDownload = QWebLink('Nukepedia', 'http://www.nukepedia.com/python/ui/w_hotbox/')
        aboutName = QtWidgets.QLabel('Wouter Gilsing')
        aboutMail = QWebLink('woutergilsing@hotmail.com', 'mailto:woutergilsing@hotmail.com?body=')
        aboutWeb = QWebLink('woutergilsing.com', 'http://www.woutergilsing.com')

        # set fonts
        fontSize = 0.3
        font = preferencesNode.knob('UIFont').value()
        mediumFont = QtGui.QFont(font, fontSize * 40)
        smallFont = QtGui.QFont(font, fontSize * 30)

        aboutDownload.setFont(mediumFont)

        for label in [aboutVersion, aboutDate, aboutName, aboutMail, aboutWeb]:
            label.setFont(smallFont)

        # assemble interface
        masterLayout = QtWidgets.QVBoxLayout()

        masterLayout.addWidget(aboutHotbox)

        masterLayout.addWidget(aboutVersion)
        masterLayout.addWidget(aboutDate)
        masterLayout.addSpacing(40)
        masterLayout.addLayout(self.wrapInLayout(aboutDownload))
        masterLayout.addSpacing(20)

        masterLayout.addWidget(aboutName)
        masterLayout.addLayout(self.wrapInLayout(aboutMail, True))
        masterLayout.addLayout(self.wrapInLayout(aboutWeb, True))

        self.setLayout(masterLayout)

        # move to screen center
        self.adjustSize()
        screenRes = QtWidgets.QDesktopWidget().screenGeometry()
        self.move(QtCore.QPoint(screenRes.width() // 2, screenRes.height() // 2) - QtCore.QPoint((self.width() // 2),
                                                                                                 (self.height() // 2)))

    def mouseReleaseEvent(self, event):
        '''
        Close window when clicked. Like a splashscreen.
        '''
        self.close()

    def wrapInLayout(self, weblink, alignment=None):
        '''
        Wrap label/Weblink in a layout, to make sure it will be aligned properly and only the actual text is clickable.
        '''

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(weblink)

        if alignment:
            weblink.setAlignment(QtCore.Qt.AlignRight)

        layout.insertStretch(bool(alignment))

        return layout


class QWebLink(QtWidgets.QLabel):
    def __init__(self, name, link):
        super(QWebLink, self).__init__()

        self.link = link
        if self.link.startswith('mailto:'):
            self.link = self.link + self.composeEmail()
        self.setToolTip(self.link)

        self.origText = name
        self.setText(self.origText)

        self.active = False

    def composeEmail(self):

        import platform
        operatingSystem = platform.system()

        hotboxVersion = 'W_hotbox v%s (%s)' % (version, releaseDate)
        nukeVersion = 'Nuke ' + nuke.NUKE_VERSION_STRING

        if operatingSystem == 'Windows':
            osName = 'Windows'
            osVersion = platform.win32_ver()[0]

        elif operatingSystem == 'Darwin':
            osName = 'OSX'
            osVersion = platform.mac_ver()[0]
        else:
            osName = platform.linux_distribution(full_distribution_name=0)[0]
            osVersion = platform.linux_distribution(full_distribution_name=0)[1]

        operatingSystem = ' '.join([osName, osVersion])

        return '\n'.join(["I'm running:\n", hotboxVersion, nukeVersion, operatingSystem])

    def activate(self):
        self.setText('<font color = #f7931e>%s</font>' % self.origText)

    def deactivate(self):
        self.setText('<font color = #c8c8c8>%s</font>' % self.origText)

    def enterEvent(self, event):
        self.activate()

    def leaveEvent(self, event):
        self.deactivate()

    def mouseReleaseEvent(self, event):
        openURL(self.link)


# ------------------------------------------------------------------------------------------------------
# Top portion of the files that will be generated
# ------------------------------------------------------------------------------------------------------

class FileHeader():
    def __init__(self, name, color=None, textColor=None, rule=False):

        dividerLine = '-' * 106

        text = ['#%s' % dividerLine,
                '#',
                '# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX',
                '#',
                '# NAME: %s' % name,
                '#',
                '#%s\n\n' % dividerLine]

        if rule:
            text[4] = text[4].replace('# NAME:', '# IGNORE CLASSES:')

        # add extra attributes if available
        if textColor:
            text.insert(5, '# TEXTCOLOR: %s' % textColor)
        if color:
            text.insert(5, '# COLOR: %s' % color)

        self.text = '\n'.join(text)

    def getHeader(self):
        return self.text


# ------------------------------------------------------------------------------------------------------
# Repair
# ------------------------------------------------------------------------------------------------------

class RepairHotbox():

    # --------------------------------------------------------------------------------------------------
    def __init__(self, folder=None, recursive=True, message=True):

        # set root folder
        if folder == None:
            self.root = preferencesNode.knob('hotboxLocation').value()
        else:
            self.root = folder

        # make sure the root ends with '/'
        while self.root[-1] != '/':
            self.root += '/'

        # compose list of folders
        if folder == None:
            self.dirList = ['%sAll/' % self.root]
        else:
            self.dirList = []

        if recursive:
            self.indexFolders(self.root, folder)
        else:
            self.dirList = [self.root]

        # append every filename with a 'tmp' so no files will be overwritten.
        for i in self.dirList:
            self.tempifyFolder(i)

        # reset dirlist
        if folder == None:
            self.dirList = ['%sAll/' % self.root]
        else:
            self.dirList = []

        if recursive:
            self.indexFolders(self.root, folder)
        else:
            self.dirList = [self.root]

        # give every file its proper name

        repairProgress = 100.0 / max(1.0, len(self.dirList))

        for index, i in enumerate(self.dirList):
            if message:
                repairProgressBar = nuke.ProgressTask('Repairing W_hotbox...')

                repairProgressBar.setProgress(int(index * repairProgress))
                repairProgressBar.setMessage(i)

            self.repairFolder(i)

        if message:
            nuke.message('Succesfully repaired')

    # --------------------------------------------------------------------------------------------------

    def indexFolders(self, path, folder):

        while path[-1] != '/':
            path += '/'

        level = len([i for i in path.replace(self.root, '').split('/') if len(i) > 0])

        for i in [path + i + '/' for i in os.listdir(path) if i[0] not in ['.', '_']]:

            if os.path.isdir(i):

                if level == 0 and folder == None:
                    pass
                else:
                    self.dirList.insert(0, i)
                self.indexFolders(i, folder)

    # --------------------------------------------------------------------------------------------------

    def tempifyFolder(self, folderPath):

        folderContent = [folderPath + i for i in os.listdir(folderPath) if i[0] not in [".", "_"]]
        for i in sorted(folderContent):
            os.rename(i, i + '.tmp')

    # --------------------------------------------------------------------------------------------------

    def repairFolder(self, folderPath):

        folderContent = [folderPath + i for i in os.listdir(folderPath) if i[0] not in [".", "_"]]

        for index, oldFile in enumerate(sorted(folderContent)):
            extension = ''

            if os.path.isfile(oldFile):
                extension = '.py'

            newFile = folderPath + str(index + 1).zfill(3) + extension

            os.rename(oldFile, newFile)


# --------------------------------------------------------------------------------------------------

def clearHotboxManager(sections=['Single', 'Multiple', 'All', 'Rules']):
    '''
    Clear the buttons of the section specified. By default all buttons will be erased.
    '''

    message = "This will erase all of the excisting buttons added to the hotbox. This action can't be undone.\n\nAre you sure?"
    if len(sections) == 1:
        message = "This will erase all of the buttons added to the '%s'-section of the hotbox. This can't be undone.\n\nAre you sure?" % \
                  sections[0]

    if not nuke.ask(message):
        return

    hotboxLocation = preferencesNode.knob('hotboxLocation').value()
    if hotboxLocation[-1] != '/':
        hotboxLocation += '/'

    clearProgressBar = nuke.ProgressTask('Clearing W_hotbox...')

    clearProgressIncrement = 100 / (len(sections) * 2)
    clearProgress = 0.0
    clearProgressBar.setProgress(int(clearProgress))

    # Empty folders
    for i in sections:
        clearProgress += clearProgressIncrement
        clearProgressBar.setProgress(int(clearProgress))
        clearProgressBar.setMessage('Clearing ' + i)

        try:
            shutil.rmtree(hotboxLocation + i)
        except:
            pass

    # Rebuild folders
    for i in sections:
        clearProgress += clearProgressIncrement
        clearProgressBar.setProgress(int(clearProgress))
        clearProgressBar.setMessage('Rebuilding ' + i)

        try:
            os.mkdir(hotboxLocation + i)
        except:
            pass


# --------------------------------------------------------------------------------------------------
# Commenly used functions
# --------------------------------------------------------------------------------------------------


def getAttributeFromFile(path, attribute='name'):
    '''
    Scan file for the appropriate attribute.
    By default attribute is name. If no attribute found, return None
    '''

    if os.path.isfile(path):
        tag = '# %s: ' % attribute.upper()
        for line in open(path).readlines():

            if not line.startswith('#'):
                break

            if line.startswith(tag):
                result = line.split(tag)[-1].replace('\n', '')
                return result

    else:
        if attribute == 'name':
            nameFile = path + '/_name.json'
            if os.path.isfile(nameFile):
                result = open(nameFile).read()
                return result

    return None


def getScriptFromFile(path):
    '''
    Extract the appropriate fucntion from the file. If no name found, return None
    '''
    if os.path.isfile(path):

        openFile = open(path).readlines()

        for index, line in enumerate(openFile):

            if not line.startswith('#'):
                script = ''.join(openFile[index + 1:]).replace('\t', ' ' * 4)

                return script

    return None


def getFirstAvailableFilePath(folder):
    '''
    loop over content of folder to find an appropriate name for the new item
    '''

    newFileName = '001'

    while newFileName in [i[:3] for i in sorted(os.listdir(folder)) if i[0] not in ['.', '_']]:
        newFileName = str(int(newFileName) + 1).zfill(3)

    return folder + newFileName


# --------------------------------------------------------------------------------------------------

hotboxManagerInstance = None
renameDialogInstance = None
aboutDialogInstance = None


def showHotboxManager(path=''):
    '''
    Launch an instance of the hotbox manager
    '''

    global hotboxManagerInstance

    # check if the manager is opened already, if so close that instance.
    if hotboxManagerInstance != None:
        hotboxManagerInstance.close()

    if path == '':
        path = preferencesNode.knob('hotboxLocation').value()

    if path[-1] != '/':
        path += '/'

    hotboxManagerInstance = HotboxManager(path)
    hotboxManagerInstance.show()
