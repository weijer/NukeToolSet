#----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
version = '1.9'
releaseDate = 'March 28 2021'

#----------------------------------------------------------------------------------------------------------
#LICENSE
#----------------------------------------------------------------------------------------------------------

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

#----------------------------------------------------------------------------------------------------------
#modules
#----------------------------------------------------------------------------------------------------------

import nuke

#Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
elif nuke.NUKE_VERSION_MAJOR < 16:
    from PySide2 import QtGui, QtCore, QtWidgets
else:
    from PySide6 import QtGui, QtCore, QtWidgets

import os
import subprocess
import platform

import traceback
import colorsys

from . import W_hotboxManager

preferencesNode = nuke.toNode('preferences')
operatingSystem = platform.system()

#----------------------------------------------------------------------------------------------------------

class Hotbox(QtWidgets.QWidget):
    '''
    The main class for the hotbox
    '''

    def __init__(self, subMenuMode = False, path = '', name = '', position = ''):
        super(Hotbox, self).__init__()

        self.active = True
        self.activeButton = None

        self.triggerMode = preferencesNode.knob('hotboxTriggerDropdown').getValue()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        #enable transparency on Linux
        if operatingSystem not in ['Darwin','Windows'] and nuke.NUKE_VERSION_MAJOR < 11:
            self.setAttribute(QtCore.Qt.WA_PaintOnScreen)

        masterLayout = QtWidgets.QVBoxLayout()
        self.setLayout(masterLayout)

        #--------------------------------------------------------------------------------------------------
        #context
        #--------------------------------------------------------------------------------------------------
   
        self.selection = nuke.selectedNodes()   

        #check whether selection in group
        self.groupRoot = 'root'

        if self.selection:
            nodeRoot = self.selection[0].fullName()
            if nodeRoot.count('.'):
                self.groupRoot = '.'.join([self.groupRoot] + nodeRoot.split('.')[:-1])

        #--------------------------------------------------------------------------------------------------
        #main hotbox
        #--------------------------------------------------------------------------------------------------

        if not subMenuMode:

            self.mode = 'Single'

            if len(self.selection) > 1:
                if len(list(set([node.Class() for node in nuke.selectedNodes()]))) > 1:
                    self.mode = 'Multiple'

            #Layouts
            centerLayout = QtWidgets.QHBoxLayout()
            centerLayout.addStretch()
            centerLayout.addWidget(HotboxButton('Reveal in %s'%getFileBrowser(),'revealInBrowser()'))
            centerLayout.addSpacing(25)
            centerLayout.addWidget(HotboxCenter())
            centerLayout.addSpacing(25)
            centerLayout.addWidget(HotboxButton('Hotbox Manager','showHotboxManager()'))
            centerLayout.addStretch()

            self.topLayout = NodeButtons()
            self.bottomLayout = NodeButtons('bottom')

            spacing = 12

        #--------------------------------------------------------------------------------------------------
        #submenu mode
        #--------------------------------------------------------------------------------------------------

        else:

            allItems = [path + '/' + i for i in sorted(os.listdir(path)) if i[0] not in ['.','_']]

            centerItems = allItems[:2]

            lists = [[],[]]
            for index, item in enumerate(allItems[2:]):

                if int((index%4)//2):
                    lists[index%2].append(item)
                else:
                    lists[index%2].insert(0,item)

            #Stretch layout
            centerLayout = QtWidgets.QHBoxLayout()

            centerLayout.addStretch()
            for index, item in enumerate(centerItems):
                centerLayout.addWidget(HotboxButton(item))
                if index == 0:
                    centerLayout.addWidget(HotboxCenter(False,path))

            if len(centerItems) == 1:
                centerLayout.addSpacing(105)

            centerLayout.addStretch()

            self.topLayout = NodeButtons('SubMenuTop',lists[0])
            self.bottomLayout = NodeButtons('SubMenuBottom',lists[1])

            spacing = 0

        #--------------------------------------------------------------------------------------------------
        #Equalize layouts to make sure the center layout is the center of the hotbox
        #--------------------------------------------------------------------------------------------------

        difference = self.topLayout.count() - self.bottomLayout.count()

        if difference != 0:

            extraLayout = QtWidgets.QVBoxLayout()

            for i in range(abs(difference)):
                extraLayout.addSpacing(35)

            if difference > 0:
                self.bottomLayout.addLayout(extraLayout)
            else:
                self.topLayout.insertLayout(0,extraLayout)

        #--------------------------------------------------------------------------------------------------

        masterLayout.addLayout(self.topLayout)
        masterLayout.addSpacing(spacing)
        masterLayout.addLayout(centerLayout)
        masterLayout.addSpacing(spacing)
        masterLayout.addLayout(self.bottomLayout)

        #position
        self.adjustSize()

        self.spwanPosition = QtGui.QCursor().pos() - QtCore.QPoint((self.width()//2),(self.height()//2))

        #set last position if a fresh instance of the hotbox is launched
        if position == '' and not subMenuMode:
            global lastPosition
            lastPosition = self.spwanPosition

        if subMenuMode:
            self.move(self.spwanPosition)

        else:
            self.move(lastPosition)

        #make sure the widgets closes when it loses focus
        self.installEventFilter(self)

    def closeHotbox(self, hotkey = False):

        #if the execute on close function is turned on, the hotbox will execute the selected button upon close

        
        
        if hotkey:
            if preferencesNode.knob('hotboxExecuteOnClose').value():
                if self.activeButton != None:
                    self.activeButton.invokeButton()
                    self.activeButton = None

        self.active = False
        self.close()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return False
        if event.text() == shortcut:
            global lastPosition
            lastPosition = ''

            # if set to single tap, leave the hotbox open after launching, else close it.
            if not self.triggerMode:
                self.closeHotbox(hotkey = True)

            return True

    def keyPressEvent(self, event):
        if event.text() == shortcut:
            if event.isAutoRepeat():
                return False

            #if launch mode is set to 'Single Tap' close the hotbox.
            if self.triggerMode:
                self.closeHotbox(hotkey = True)
        else:
            return False

    def eventFilter(self, object, event):
        if event.type() in [QtCore.QEvent.WindowDeactivate,QtCore.QEvent.FocusOut]:
            self.closeHotbox()
            return True
        return False

#----------------------------------------------------------------------------------------------------------
#Button field
#----------------------------------------------------------------------------------------------------------

class NodeButtons(QtWidgets.QVBoxLayout):
    '''
    Create QLayout filled with buttons
    '''

    def __init__(self, mode = '', allItems = ''):
        super(NodeButtons, self).__init__()

        selectedNodes = nuke.selectedNodes()

        #--------------------------------------------------------------------------------------------------
        #submenu
        #--------------------------------------------------------------------------------------------------

        if 'submenu' in mode.lower():

            self.rowMaxAmount = 3
            mirrored = ('top' not in mode.lower())

        #--------------------------------------------------------------------------------------------------
        #main hotbox
        #--------------------------------------------------------------------------------------------------

        else:

            mirrored = True

            mode = (mode == 'bottom')

            if preferencesNode.knob('hotboxMirroredLayout').value():
                mode = 1 - mode
                mirrored = 1 - mirrored

            self.path = preferencesNode.knob('hotboxLocation').value().replace('\\','/')
            if self.path[-1] != '/':
                self.path = self.path + '/'

            self.allRepositories = list(set([self.path]+[i[1] for i in extraRepositories]))

            self.rowMaxAmount = int(preferencesNode.knob('hotboxRowAmountAll').value())

            self.folderList = []
            
            #----------------------------------------------------------------------------------------------
            #noncontextual
            #----------------------------------------------------------------------------------------------

            if mode:

                self.folderList += [repository + 'All' for repository in self.allRepositories]

            #----------------------------------------------------------------------------------------------
            #contextual
            #----------------------------------------------------------------------------------------------
            
            else:

                mirrored = 1 - mirrored

                self.rowMaxAmount = int(preferencesNode.knob('hotboxRowAmountSelection').value())

                #------------------------------------------------------------------------------------------
                #rules
                #------------------------------------------------------------------------------------------

                #collect all folders storing buttons for applicable rules

                ignoreClasses = False
                tag = '# IGNORE CLASSES: '

                allRulePaths = []

                for repository in self.allRepositories:
                    
                    rulesFolder = repository + 'Rules'
                    if not os.path.exists(rulesFolder):
                        continue

                    rules = ['/'.join([rulesFolder,rule]) for rule in os.listdir(rulesFolder) if rule[0] not in ['_','.'] and rule[-1] != '_']

                    #validate rules
                    for rule in rules:

                        ruleFile = rule + '/_rule.py'

                        if os.path.exists(ruleFile):

                            if self.validateRule(ruleFile):
                                allRulePaths.append(rule)

                                #read ruleFile to check if ignoreClasses was enabled.
                                if not ignoreClasses:
                            
                                    for line in open(ruleFile).readlines():
                                        #no point in checking boyond the header
                                        if not line.startswith('#'):
                                            break
                                        #if proper tag is found, check its value
                                        if line.startswith(tag):
                                            ignoreClasses = bool(int(line.split(tag)[-1].replace('\n','')))
                                            break

                #------------------------------------------------------------------------------------------
                #classes
                #------------------------------------------------------------------------------------------

                #collect all folders storing buttons for applicable classes
                
                if not ignoreClasses:

                    allClassPaths = []

                    nodeClasses = list(set([node.Class() for node in selectedNodes]))

                    #if nothing selected
                    if len(nodeClasses) == 0:
                        nodeClasses = ['No Selection']

                    #if selection
                    else:
                        #check if group, if so take the name of the group, as well as the class
                        groupNodes = []
                        if 'Group' in nodeClasses:
                            for node in selectedNodes:
                                if node.Class() == 'Group':
                                    groupName = node.name()
                                    while groupName[-1] in [str(i) for i in range(10)]:
                                        groupName = groupName[:-1]
                                    if groupName not in groupNodes and groupName != 'Group':
                                        groupNodes.append(groupName)

                        if len(groupNodes) > 0:
                            groupNodes = [nodeClass for nodeClass in nodeClasses if nodeClass != 'Group'] + groupNodes

                        if len(nodeClasses) > 1:
                            nodeClasses = [nodeClasses]
                        if len(groupNodes) > 1:
                            groupNodes = [groupNodes]

                        nodeClasses = nodeClasses + groupNodes

                    #Check which defined class combinations on disk are applicable to the current selection.
                    for repository in self.allRepositories:
                        for nodeClass in nodeClasses:

                            if isinstance(nodeClass, list):
                                for managerNodeClasses in [i for i in os.listdir(repository + 'Multiple') if i[0] not in ['_','.']]:
                                    managerNodeClassesList = managerNodeClasses.split('-')
                                    match = list(set(nodeClass).intersection(managerNodeClassesList))

                                    if len(match) >= len(nodeClass):
                                        allClassPaths.append(repository + 'Multiple/' + managerNodeClasses)
                            else:
                                allClassPaths.append(repository + 'Single/' + nodeClass)

                    allClassPaths = list(set(allClassPaths))
                    allClassPaths = [path for path in allClassPaths if os.path.exists(path)]

                #------------------------------------------------------------------------------------------
                #combine classes and rules
                #------------------------------------------------------------------------------------------
                
                if ignoreClasses:
                    self.folderList = allRulePaths

                else:
                    self.folderList =  allClassPaths + allRulePaths

                    if preferencesNode.knob('hotboxRuleClassOrder').getValue():
                        self.folderList.reverse()

            #----------------------------------------------------------------------------------------------
            #files on disk representing items
            #----------------------------------------------------------------------------------------------

            allItems = []

            for folder in self.folderList:
                for file in sorted(os.listdir(folder)):
                    if file[0] not in ['.','_'] and len(file) in [3,6]:
                        allItems.append('/'.join([folder, file]))

        #--------------------------------------------------------------------------------------------------
        #devide in rows based on the row maximum
        #--------------------------------------------------------------------------------------------------
        
        allRows = []
        row = []

        for item in allItems:
            if preferencesNode.knob('hotboxButtonSpawnMode').value():
                if len(row) %2:
                    row.append(item)
                else:
                    row.insert(0,item)
            else:
                row.append(item)

            #when a row reaches its full capacity, add the row to the allRows list
            #and start a new one. Increase rowcapacity to get a triangular shape
            if len(row) == self.rowMaxAmount:
                allRows.append(row)
                row = []
                self.rowMaxAmount += preferencesNode.knob('hotboxRowStepSize').value()

        #if the last row is not completely full, add it to the allRows list anyway
        if len(row) != 0:
            allRows.append(row)

        if not mirrored:
            allRows.reverse()

        #nodeHotboxLayout
        for row in allRows:
            self.rowLayout = QtWidgets.QHBoxLayout()

            self.rowLayout.addStretch()

            for button in row:
                buttonObject = HotboxButton(button)
                self.rowLayout.addWidget(buttonObject)
            self.rowLayout.addStretch()

            self.addLayout(self.rowLayout)

        self.rowAmount = len(allRows)

    def validateRule(self, ruleFile):
        '''
        Run the rule, return True or False.
        '''

        error = False

        #read from file
        ruleString = open(ruleFile).read()

        #quick sanity check
        if not 'ret=' in ruleString.replace(' ',''):
            error = "RuleError: rule must contain variable named 'ret'"

        else:

            #prepend the rulestring with a nuke import statement and make it return False by default
            prefix = 'import nuke\nret = False\n'
            ruleString = prefix + ruleString

            #run rule
            try:
                scope = {}
                exec(ruleString, scope, scope)

                if 'ret' in scope.keys():
                    result = bool(scope['ret'])

            except:
                error = traceback.format_exc()

        #run error
        if error:
            printError(error, buttonName = os.path.basename(os.path.dirname(ruleFile)), rule = True)
            result = False

        #return the result of the rule
        return result

#----------------------------------------------------------------------------------------------------------

class HotboxCenter(QtWidgets.QLabel):
    '''
    Center button of the hotbox.
    If the 'color nodes' is set to True in the preferences panel, the button will take over the color and
    name of the current selection. If not, the button will be the same color as the other buttons will
    be in their selected state. The text will be read from the _name.json file in the folder.
    '''

    def __init__(self, node = True, name = ''):
        super(HotboxCenter, self).__init__()

        self.node = node

        nodeColor = '#525252'
        textColor = '#eeeeee'

        selectedNodes = nuke.selectedNodes()

        if node:
            #if no node selected
            if len(selectedNodes) == 0:
                name = 'W_hotbox'
                nodeColorRGB = interface2rgb(640034559)

            #if node(s) selected
            else:
                name = nuke.selectedNode().name()
                nodeColorRGB = interface2rgb(getTileColor())

            if preferencesNode.knob('hotboxColorCenter').value():
                nodeColor = rgb2hex(nodeColorRGB)

                nodeColorHSV = colorsys.rgb_to_hsv(nodeColorRGB[0],nodeColorRGB[1],nodeColorRGB[2])

                if nodeColorHSV[2] > 0.7 and nodeColorHSV[1] < 0.4:
                    textColor = '#262626'

            width = 115
            height = 60


            if (len(set([i.Class() for i in selectedNodes]))) > 1:
                name = 'Selection'

        else:

            name = open(name + '/_name.json').read()
            nodeColor = getSelectionColor()

            width = 105
            height = 35

        self.setText(name)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        #resize font based on length of name
        fontSize = int(max(5,(13-(max(0,(len(name) - 11))/2))))
        font = QtGui.QFont(preferencesNode.knob('UIFont').value(), fontSize)
        self.setFont(font)

        self.setStyleSheet("""
                border: 1px solid black;
                color:%s;
                background:%s""" %(textColor, nodeColor))

        self.setSelectionStatus(True)

    def setSelectionStatus(self, selected = False):
        '''
        Define the style of the button for different states
        '''
        if not self.node:
            self.selected = selected

    def enterEvent(self, event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        if not self.node:
            self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        if not self.node:
            self.setSelectionStatus()
        return True

    def mouseReleaseEvent(self,event):
        '''

        '''
        if not self.node:
            showHotbox(True, resetPosition = False)
        return True

#----------------------------------------------------------------------------------------------------------
#Buttons
#----------------------------------------------------------------------------------------------------------

class HotboxButton(QtWidgets.QLabel):
    '''
    Button class
    '''

    def __init__(self, name, function = None):

        super(HotboxButton, self).__init__()

        self.menuButton = False
        self.filePath = name
        self.bgColor = '#525252'

        self.borderColor = '#000000'

        #set the border color to grey for buttons from an additional repository
        for index,i in enumerate(extraRepositories):
            if name.startswith(i[1]):
                self.borderColor = '#959595'
                break

        if function != None:
            self.function = function

        else:

            #----------------------------------------------------------------------------------------------
            #Button linked to folder
            #----------------------------------------------------------------------------------------------

            if os.path.isdir(self.filePath):
                self.menuButton = True
                name = open(self.filePath+'/_name.json').read()
                self.function = 'showHotboxSubMenu("%s","%s")'%(self.filePath,name)
                self.bgColor = '#333333'

            #----------------------------------------------------------------------------------------------
            #Button linked to file
            #----------------------------------------------------------------------------------------------

            else:

                self.openFile = open(name).readlines()

                header = []
                for index, line in enumerate(self.openFile):

                    if not line.startswith('#'):
                        self.function = ''.join(self.openFile[index:])
                        break

                    header.append(line)

                tags = ['# %s: '%tag for tag in ['NAME','TEXTCOLOR','COLOR']]

                tagResults = []

                for tag in tags:
                    tagResult = None
                    for line in header:

                        if line.startswith(tag):

                            tagResult = line.split(tag)[-1].replace('\n','')
                            break

                    tagResults.append(tagResult)

                name, textColor, color = tagResults

                if textColor and name:
                    name = '<font color = "%s">%s</font>'%(textColor,name)

                if color:
                    self.bgColor = color

            #----------------------------------------------------------------------------------------------

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMouseTracking(True)
        self.setFixedWidth(105)
        self.setFixedHeight(35)

        fontSize = preferencesNode.knob('hotboxFontSize').value()
        font = QtGui.QFont(preferencesNode.knob('UIFont').value(), fontSize, QtGui.QFont.Bold)

        self.setFont(font)
        self.setWordWrap(True)
        self.setTextFormat(QtCore.Qt.RichText)

        self.setText(name)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.selected = False
        self.setSelectionStatus()

    def invokeButton(self):
        '''
        Execute script attached to button
        '''

        with nuke.toNode(hotboxInstance.groupRoot):

            try:
                scope = globals().copy()
                exec(self.function, scope, scope)

            except:
                printError(traceback.format_exc(), self.filePath, self.text())

        #if 'close on click' is ticked, close the hotbox
        if not self.menuButton:
            if preferencesNode.knob('hotboxCloseOnClick').value() and preferencesNode.knob('hotboxTriggerDropdown').getValue():
                hotboxInstance.closeHotbox()

    def setSelectionStatus(self, selected = False):
        '''
        Define the style of the button for different states
        '''

        #if button becomes selected
        if selected:
            self.setStyleSheet("""
                                border: 1px solid black;
                                background:%s;
                                color:#eeeeee;
                                """%getSelectionColor())

        #if button becomes unselected
        else:
            self.setStyleSheet("""
                                border: 1px solid %s;
                                background:%s;
                                color:#eeeeee;
                                """%(self.borderColor, self.bgColor))


        if preferencesNode.knob('hotboxExecuteOnClose').value():

            global hotboxInstance
            if hotboxInstance != None:

                hotboxInstance.activeButton = None

                #if launch mode set to Press and Hold and the button is a menu button,
                #dont open a submenu upon shortcut release

                if not self.menuButton and not preferencesNode.knob('hotboxTriggerDropdown').getValue():
                    if selected:
                        hotboxInstance.activeButton = self

        self.selected = selected

    def enterEvent(self, event):
        '''
        Change color of the button when the mouse starts hovering over it
        '''
        self.setSelectionStatus(True)
        return True

    def leaveEvent(self,event):
        '''
        Change color of the button when the mouse stops hovering over it
        '''
        self.setSelectionStatus()
        return True

    def mouseReleaseEvent(self,event):
        '''
        Execute the buttons' self.function (str)
        '''
        if self.selected:

            nuke.Undo().name(self.text())
            nuke.Undo().begin()

            self.invokeButton()
            
            nuke.Undo().end()

        return True

#----------------------------------------------------------------------------------------------------------
# Preferences
#----------------------------------------------------------------------------------------------------------

def addToPreferences(knobObject, tooltip = None):
    '''
    Add a knob to the preference panel.
    Save current preferences to the prefencesfile in the .nuke folder.
    '''

    if knobObject.name() not in preferencesNode.knobs().keys():

        if tooltip != None:
            knobObject.setTooltip(tooltip)

        preferencesNode.addKnob(knobObject)
        savePreferencesToFile()
        return preferencesNode.knob(knobObject.name())

def savePreferencesToFile():
    '''
    Save current preferences to the prefencesfile in the .nuke folder.
    Pythonic alternative to the 'ok' button of the preferences panel.
    '''

    nukeFolder = os.path.expanduser('~') + '/.nuke/'
    preferencesFile = nukeFolder + 'preferences{}.{}.nk'.format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)

    preferencesNode = nuke.toNode('preferences')

    customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
    customPrefences = customPrefences.replace('\n','\n  ')

    preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences

    # write to file
    openPreferencesFile = open( preferencesFile , 'w' )
    openPreferencesFile.write( preferencesCode )
    openPreferencesFile.close()

def deletePreferences():
    '''
    Delete all the W_hotbox related items in the properties panel.
    '''

    firstLaunch = True
    for i in preferencesNode.knobs().keys():
        if 'hotbox' in i:
            preferencesNode.removeKnob(preferencesNode.knob(i))
            firstLaunch = False

    #remove TabKnob
    try:
        preferencesNode.removeKnob(preferencesNode.knob('hotboxLabel'))
    except:
        pass

    if not firstLaunch:
        savePreferencesToFile()

def addPreferences():
    '''
    Add knobs to the preferences needed for this module to work properly.
    '''
    
    addToPreferences(nuke.Tab_Knob('hotboxLabel','W_hotbox'))
    addToPreferences(nuke.Text_Knob('hotboxGeneralLabel','<b>General</b>'))

    #version knob to check whether the hotbox was updated
    knob = nuke.String_Knob('hotboxVersion','version')
    knob.setValue(version)
    addToPreferences(knob)
    preferencesNode.knob('hotboxVersion').setVisible(False)

    #location knob
    knob = nuke.File_Knob('hotboxLocation','Hotbox location')

    tooltip = "The folder on disk the Hotbox uses to store the Hotbox buttons. Make sure this path links to the folder containing the 'All','Single' and 'Multiple' folders."

    locationKnobAdded = addToPreferences(knob, tooltip)

    #icons knob
    knob = nuke.File_Knob('hotboxIconLocation','Icons location')
    knob.setValue(homeFolder +'/icons/W_hotbox')

    tooltip = "The folder on disk the where the Hotbox related icons are stored. Make sure this path links to the folder containing the PNG files."
    addToPreferences(knob, tooltip)

    #open manager button
    knob = nuke.PyScript_Knob('hotboxOpenManager','open hotbox manager','W_hotboxManager.showHotboxManager()')
    knob.setFlag(nuke.STARTLINE)

    tooltip = "Open the Hotbox Manager."

    addToPreferences(knob, tooltip)

    #open in file system button knob
    knob = nuke.PyScript_Knob('hotboxOpenFolder','open hotbox folder','W_hotbox.revealInBrowser(True)')

    tooltip = "Open the folder containing the files that store the Hotbox buttons. It's advised not to mess around in this folder unless you understand what you're doing."

    addToPreferences(knob, tooltip)

    #delete preferences button knob
    knob = nuke.PyScript_Knob('hotboxDeletePreferences','delete preferences','W_hotbox.deletePreferences()')

    tooltip = "Delete all the Hotbox related knobs from the Preferences Panel. After clicking this button the Preferences Panel should be closed by clicking the 'cancel' button."

    addToPreferences(knob, tooltip)

    #Launch Label knob
    addToPreferences(nuke.Text_Knob('hotboxLaunchLabel','<b>Launch</b>'))

    #shortcut knob
    knob = nuke.String_Knob('hotboxShortcut','Shortcut')
    knob.setValue('`')

    tooltip = ("The key that triggers the Hotbox. Should be set to a single key without any modifier keys. "
                "Spacebar can be defined as 'space'. Nuke needs be restarted in order for the changes to take effect.")

    addToPreferences(knob, tooltip)
    global shortcut
    shortcut = preferencesNode.knob('hotboxShortcut').value()

    #reset shortcut knob
    knob = nuke.PyScript_Knob('hotboxResetShortcut','set', 'W_hotbox.resetMenuItems()')
    knob.clearFlag(nuke.STARTLINE)
    tooltip = "Apply new shortcut."

    addToPreferences(knob, tooltip)

    #trigger mode knob
    knob = nuke.Enumeration_Knob('hotboxTriggerDropdown', 'Launch mode',['Press and Hold','Single Tap'])

    tooltip = ("The way the hotbox is launched. When set to 'Press and Hold' the Hotbox will appear whenever the shortcut is pressed and disappear as soon as the user releases the key. "
                "When set to 'Single Tap' the shortcut will toggle the Hotbox on and off.")

    addToPreferences(knob, tooltip)

    #close on click
    knob = nuke.Boolean_Knob('hotboxCloseOnClick','Close on button click')
    knob.setValue(False)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Close the Hotbox whenever a button is clicked (excluding submenus obviously). This option will only take effect when the launch mode is set to 'Single Tap'."

    addToPreferences(knob, tooltip)

    #execute on close
    knob = nuke.Boolean_Knob('hotboxExecuteOnClose','Execute button without click')
    knob.setValue(False)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Execute the button underneath the cursor whenever the Hotbox is closed."

    addToPreferences(knob, tooltip)

    #Rule/Class order
    knob = nuke.Enumeration_Knob('hotboxRuleClassOrder', 'Order',['Class - Rule', 'Rule - Class'])
    tooltip = "The order in which the buttons will be loaded."

    addToPreferences(knob, tooltip)

    #Manager startup default
    knob = nuke.Enumeration_Knob('hotboxOpenManagerOptions', 'Manager startup default',['Contextual','All','Rules', 'Contextual/All', 'Contextual/Rules'])
    knob.clearFlag(nuke.STARTLINE)

    tooltip = ("The section of the Manager that will be opened on startup.\n"
                "\n<b>Contextual</b> Open the 'Single' or 'Multiple' section, depending on selection."
                "\n<b>All</b> Open the 'All' section."
                "\n<b>Rules</b> Open the 'Rules' section."
                "\n<b>Contextual/All</b> Contextual if the selection matches a button in the 'Single' or 'Multiple' section, otherwise the 'All' section will be opened."
                "\n<b>Contextual/Rules</b> Contextual if the selection matches a button in the 'Single' or 'Multiple' section, otherwise the 'Rules' section will be opened.")

    addToPreferences(knob, tooltip)

    #Appearence knob
    addToPreferences(nuke.Text_Knob('hotboxAppearanceLabel','<b>Appearance</b>'))

    #color dropdown knob
    knob = nuke.Boolean_Knob('hotboxMirroredLayout', 'Mirrored')

    tooltip = ("By default the contextual buttons will appear at the top of the hotbox and the non contextual buttons at the bottom.")

    addToPreferences(knob, tooltip)

    #color dropdown knob
    knob = nuke.Enumeration_Knob('hotboxColorDropdown', 'Color scheme',['Maya','Nuke','Custom'])

    tooltip = ("The color of the buttons when selected.\n"
                "\n<b>Maya</b> Autodesk Maya's muted blue."
                "\n<b>Nuke</b> Nuke's bright orange."
                "\n<b>Custom</b> which lets the user pick a color.")

    addToPreferences(knob, tooltip)

    #custom color knob
    knob = nuke.ColorChip_Knob('hotboxColorCustom','')
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "The color of the buttons when selected, when the color dropdown is set to 'Custom'."

    addToPreferences(knob, tooltip)

    #hotbox center knob
    knob = nuke.Boolean_Knob('hotboxColorCenter','Colorize hotbox center')
    knob.setValue(True)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Color the center button of the hotbox depending on the current selection. When unticked the center button will be colored a lighter tone of grey."

    addToPreferences(knob, tooltip)

    #auto color text
    knob = nuke.Boolean_Knob('hotboxAutoTextColor','Auto adjust text color')
    knob.setValue(True)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Automatically adjust the color of a button's text to its background color in order to keep enough of a difference to remain readable."

    addToPreferences(knob, tooltip)

    #fontsize knob
    knob = nuke.Int_Knob('hotboxFontSize','Font size')
    knob.setValue(8)

    tooltip = "The font size of the text that appears in the hotbox buttons, unless defined differently on a per-button level."

    addToPreferences(knob, tooltip)

    #fontsize manager's script editor knob
    knob = nuke.Int_Knob('hotboxScriptEditorFontSize','Font size script editor')
    knob.setValue(11)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "The font size of the text that appears in the hotbox manager's script editor."

    addToPreferences(knob, tooltip)

    addToPreferences(nuke.Text_Knob('hotboxItemsLabel','<b>Items per Row</b>'))

    #row amount selection knob
    knob = nuke.Int_Knob('hotboxRowAmountSelection', 'Selection specific')
    knob.setValue(3)

    tooltip = ("The maximum amount of buttons a row in the upper half of the Hotbox can contain. "
                "When the row's maximum capacity is reached a new row will be started. This new row's maximum capacity will be incremented by the step size.")

    addToPreferences(knob, tooltip)

    #row amount all knob
    knob = nuke.Int_Knob('hotboxRowAmountAll','All')
    knob.setValue(3)

    tooltip = ("The maximum amount of buttons a row in the lower half of the Hotbox can contain. "
                "When the row's maximum capacity is reached a new row will be started.This new row's maximum capacity will be incremented by the step size.")

    addToPreferences(knob, tooltip)

    #stepsize knob
    knob = nuke.Int_Knob('hotboxRowStepSize','Step size')
    knob.setValue(1)

    tooltip = ("The amount a buttons every new row's maximum capacity will be increased by. "
                "Having a number unequal to zero will result in a triangular shape when having multiple rows of buttons.")

    addToPreferences(knob, tooltip)

    #spawnmode knob
    knob = nuke.Boolean_Knob('hotboxButtonSpawnMode','Add new buttons to the sides')
    knob.setValue(True)
    knob.setFlag(nuke.STARTLINE)

    tooltip = "Add new buttons left and right of the row alternately, instead of to the right, in order to preserve muscle memory."

    addToPreferences(knob, tooltip)

    #hide the iconLocation knob if environment varible called 'W_HOTBOX_HIDE_ICON_LOC' is set to 'true' or '1'
    preferencesNode.knob('hotboxIconLocation').setVisible(True)
    if 'W_HOTBOX_HIDE_ICON_LOC' in os.environ.keys():
        if os.environ['W_HOTBOX_HIDE_ICON_LOC'].lower() in ['true','1']:
            preferencesNode.knob('hotboxIconLocation').setVisible(False)

    savePreferencesToFile()

def updatePreferences():
    '''
    Check whether the hotbox was updated since the last launch. If so refresh the preferences.
    '''

    allKnobs = preferencesNode.knobs().keys()

    #Older versions of the hotbox had a knob called 'iconLocation'.
    #This was a mistake and the knob was supposed to be called
    #'hotboxIconLocation', similar to the rest of the knobs.

    forceUpdate = False

    if 'iconLocation' in allKnobs and 'hotboxIconLocation' not in allKnobs:

        currentSetting = preferencesNode.knob('iconLocation').value()

        #delete 'iconLocation'
        preferencesNode.removeKnob(preferencesNode.knob('iconLocation'))

        #re-add 'hotboxIconLocation'
        iconLocationKnob = nuke.File_Knob('hotboxIconLocation','Icons location')
        iconLocationKnob.setValue(currentSetting)
        addToPreferences(iconLocationKnob)

        forceUpdate = True

    allKnobs = preferencesNode.knobs().keys()
    proceedUpdate = True

    if 'hotboxVersion' in allKnobs or forceUpdate:

        if not forceUpdate:
            try:
                if float(version) == float(preferencesNode.knob('hotboxVersion').value()):
                    proceedUpdate = False
            except:
                proceedUpdate = True

        if proceedUpdate:
            currentSettings = {knob:preferencesNode.knob(knob).value() for knob in allKnobs if knob.startswith('hotbox') and knob != 'hotboxVersion'}

            #delete all the preferences
            deletePreferences()

            #re-add all the knobs
            addPreferences()

            #restore
            for knob in currentSettings.keys():
                try:
                    preferencesNode.knob(knob).setValue(currentSettings[knob])
                except:
                    pass

            #save to file
            savePreferencesToFile()

    # nuke 12.2v4 and 13 bug. The last tab wont be shown. Workaround is to add an extra tab
    customTabs = [k.name() for k in preferencesNode.knobs().values() if isinstance(k, nuke.Tab_Knob)]
    if customTabs and customTabs[-1] == 'hotboxLabel':

        # make new tab and hide it
        dummyTab = nuke.Tab_Knob('hotboxDummyTab', 'Dummy')
        dummyTab.setFlag(0x00040000)

        addToPreferences(dummyTab)


#----------------------------------------------------------------------------------------------------------
#Color
#----------------------------------------------------------------------------------------------------------

def interface2rgb(hexValue, normalize = True):
    '''
    Convert a color stored as a 32 bit value as used by nuke for interface colors to normalized rgb values.

    '''
    return [(0xFF & hexValue >>  i) / 255.0 for i in [24,16,8]]


def rgb2hex(rgbaValues):
    '''
    Convert a color stored as normalized rgb values to a hex.
    '''

    rgbaValues = [int(i * 255) for i in rgbaValues]

    if len(rgbaValues) < 3:
        return

    return '#%02x%02x%02x' % (rgbaValues[0],rgbaValues[1],rgbaValues[2])

def hex2rgb(hexColor):
    '''
    Convert a color stored as hex to rgb values.
    '''

    hexColor = hexColor.lstrip('#')
    return tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))

def rgb2interface(rgb):
    '''
    Convert a color stored as rgb values to a 32 bit value as used by nuke for interface colors.
    '''
    if len(rgb) == 3:
        rgb = rgb + (255,)

    return int('%02x%02x%02x%02x'%rgb,16)

def getTileColor(node = None):
    '''
    If a node has it's color set automatically, the 'tile_color' knob will return 0.
    If so, this function will scan through the preferences to find the correct color value.
    '''

    if not node:
        node = nuke.selectedNode()

    interfaceColor = node.knob('tile_color').value()

    if interfaceColor == 0:
        interfaceColor = nuke.defaultNodeColor(node.Class())

    return interfaceColor

def getSelectionColor():
    '''
    Return color to be used for the selected items of the hotbox.
    '''

    customColor = rgb2hex(interface2rgb(preferencesNode.knob('hotboxColorCustom').value()))
    colorMode = int(preferencesNode.knob('hotboxColorDropdown').getValue())
    
    return['#5285a6','#f7931e',customColor][colorMode]

#----------------------------------------------------------------------------------------------------------

def revealInBrowser(startFolder = False):
    '''
    Reveal the hotbox folder in a filebrowser
    '''
    if startFolder:
        path = preferencesNode.knob('hotboxLocation').value()

    else:
        try:
            path =  hotboxInstance.topLayout.folderList[0]
        except:
            path = hotboxInstance.topLayout.path + hotboxInstance.mode

    if not os.path.exists(path):
        path = os.path.dirname(path)

    if operatingSystem == "Windows":
        os.startfile(path)
    elif operatingSystem == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def getFileBrowser():
    '''
    Determine the name of the file browser on the current system.
    '''

    if operatingSystem == "Windows":
        fileBrowser = 'Explorer'
    elif operatingSystem == "Darwin":
        fileBrowser = 'Finder'
    else:
        fileBrowser = 'file browser'

    return fileBrowser

#----------------------------------------------------------------------------------------------------------
#error catching
#----------------------------------------------------------------------------------------------------------


def printError(error, path = '', buttonName = '', rule = False):
    '''
    Format error message and print it to the scripteditor and shell.
    '''

    fullError = error.splitlines()

    buttonName = [buttonName]

    #line number
    lineNumber = ''
    for index, line in enumerate(reversed(fullError)):

        if line.startswith('  File "<'):
            for i in line.split(','):
                if i.startswith(' line '):
                    lineNumber = i

            index = len(fullError)-index
            break

    lineNumber = (' -' + lineNumber) * bool(lineNumber)

    fullError = fullError[index:]
    errorDescription = '\n'.join(fullError)

    #button
    if not rule:

        scriptFolder = os.path.dirname(path)
        scriptFolderName = os.path.basename(scriptFolder)

        while len(scriptFolderName) == 3 and scriptFolderName.isdigit():

            name = open(scriptFolder + '/_name.json').read()
            buttonName.insert(0, name)
            scriptFolder = os.path.dirname(scriptFolder)
            scriptFolderName = os.path.basename(scriptFolder)

        for i in range(2):
            buttonName.insert(0, os.path.basename(scriptFolder))
            scriptFolder = os.path.dirname(scriptFolder)

    #buttonName = [buttonName]

    hotboxError = '\nW_HOTBOX %sERROR: %s%s:\n%s'%('RULE '*int(bool(rule)), '/'.join(buttonName), lineNumber, errorDescription)

    #print error
    print(hotboxError)
    nuke.tprint(hotboxError)

#----------------------------------------------------------------------------------------------------------
#launch hotbox
#----------------------------------------------------------------------------------------------------------

def showHotbox(force = False, resetPosition = True):

    global hotboxInstance

    #is launch mode is set to single tap, close the hotbox if it's open
    if preferencesNode.knob('hotboxTriggerDropdown').getValue() and not force:
        if hotboxInstance != None and hotboxInstance.active:
            hotboxInstance.closeHotbox(hotkey = True)
            return

    if force:
        hotboxInstance.active = False
        hotboxInstance.close()

    if resetPosition:
        global lastPosition
        lastPosition = ''

    if hotboxInstance == None or not hotboxInstance.active:
        hotboxInstance = Hotbox(position = lastPosition)
        hotboxInstance.show()

def showHotboxSubMenu(path, name):
    global hotboxInstance
    hotboxInstance.active = False
    if hotboxInstance == None or not hotboxInstance.active:
        hotboxInstance = Hotbox(True, path, name)
        hotboxInstance.show()

def showHotboxManager():
    '''
    Open the hotbox manager from the hotbox
    '''
    hotboxInstance.closeHotbox()
    W_hotboxManager.showHotboxManager()

#----------------------------------------------------------------------------------------------------------
#menu items
#----------------------------------------------------------------------------------------------------------

def addMenuItems():
    '''
    Add items to the Nuke menu
    '''

    editMenu.addCommand('W_hotbox/Open W_hotbox', showHotbox, shortcut)
    editMenu.addCommand('W_hotbox/-', '', '')
    editMenu.addCommand('W_hotbox/Open Hotbox Manager', 'W_hotboxManager.showHotboxManager()')
    editMenu.addCommand('W_hotbox/Open in %s'%getFileBrowser(), revealInBrowser)
    editMenu.addCommand('W_hotbox/-', '', '')
    editMenu.addCommand('W_hotbox/Repair', 'W_hotboxManager.repairHotbox()')
    editMenu.addCommand('W_hotbox/Clear/Clear Everything', 'W_hotboxManager.clearHotboxManager()')
    editMenu.addCommand('W_hotbox/Clear/Clear Section/Single', 'W_hotboxManager.clearHotboxManager(["Single"])')
    editMenu.addCommand('W_hotbox/Clear/Clear Section/Multiple', 'W_hotboxManager.clearHotboxManager(["Multiple"])')
    editMenu.addCommand('W_hotbox/Clear/Clear Section/All', 'W_hotboxManager.clearHotboxManager(["All"])')
    editMenu.addCommand('W_hotbox/Clear/Clear Section/-', '', '')
    editMenu.addCommand('W_hotbox/Clear/Clear Section/Templates', 'W_hotboxManager.clearHotboxManager(["Templates"])')

def resetMenuItems():
    '''
    Remove and readd all items to the Nuke menu. Used to change the shotcut
    '''

    global shortcut 
    shortcut = preferencesNode.knob('hotboxShortcut').value()

    if editMenu.findItem('W_hotbox'):
        editMenu.removeItem('W_hotbox')

    addMenuItems()

#----------------------------------------------------------------------------------------------------------

#add knobs to preferences
preferencesNode = nuke.toNode('preferences')
homeFolder = os.getenv('HOME').replace('\\','/') + '/.nuke'

updatePreferences()
addPreferences()

#----------------------------------------------------------------------------------------------------------

#make sure the archive folders are present, if not, create them
hotboxLocationPathKnob = preferencesNode.knob('hotboxLocation')
hotboxLocationPath = hotboxLocationPathKnob.value().replace('\\','/')

if not hotboxLocationPath:
    hotboxLocationPath = homeFolder + '/W_hotbox'
    hotboxLocationPathKnob.setValue(hotboxLocationPath)

if hotboxLocationPath[-1] != '/':
    hotboxLocationPath += '/'

for subFolder in ['', 'Single', 'Multiple', 'All', 'Rules', 'Single/No Selection', 'Templates']:
    subFolderPath = hotboxLocationPath + subFolder
    if not os.path.isdir(subFolderPath):
        try:
            os.mkdir(subFolderPath)
        except:
            pass

#----------------------------------------------------------------------------------------------------------

#menu items
editMenu = nuke.menu('Nuke').findItem('Edit')
editMenu.addCommand('-', '', '')
addMenuItems()

#----------------------------------------------------------------------------------------------------------
# EXTRA REPOSTITORIES
#----------------------------------------------------------------------------------------------------------
'''
Add them like this:

W_HOTBOX_REPO_PATHS=/path1:/path2:/path3
W_HOTBOX_REPO_NAMES=name1:name2:name3

'''

extraRepositories = []

if 'W_HOTBOX_REPO_PATHS' in os.environ and 'W_HOTBOX_REPO_NAMES' in os.environ.keys():

    extraRepositoriesPaths = os.environ['W_HOTBOX_REPO_PATHS'].split(os.pathsep)
    extraRepositoriesNames = os.environ['W_HOTBOX_REPO_NAMES'].split(os.pathsep)

    for index, i in enumerate(range(min(len(extraRepositoriesPaths),len(extraRepositoriesNames)))):
        path = extraRepositoriesPaths[index].replace('\\','/')

        #make sure last character is a '/'
        if path[-1] != '/':
            path += '/'

        name = extraRepositoriesNames[index]
        if name not in [i[0] for i in extraRepositories] and path not in [i[1] for i in extraRepositories]:
            extraRepositories.append([name,path])



    if len(extraRepositories) > 0:
        editMenu.addCommand('W_hotbox/-', '', '')
        for repo in extraRepositories:
            editMenu.addCommand('W_hotbox/Special/Open Hotbox Manager - {}'.format(repo[0]), 'W_hotboxManager.showHotboxManager(path="{}")'.format(repo[1]))

#----------------------------------------------------------------------------------------------------------

hotboxInstance = None
lastPosition = ''

#----------------------------------------------------------------------------------------------------------

nuke.tprint('W_hotbox v{}, built {}.\nCopyright (c) 2016-{} Wouter Gilsing. All Rights Reserved.'.format(version, releaseDate, releaseDate.split()[-1]))
