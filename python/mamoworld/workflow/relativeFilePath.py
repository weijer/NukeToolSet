
import nuke
import posixpath
from Qt import QtWidgets as QtGui
from Qt import QtCore as QtCore
from platform import system

def showReplaceFilePathDialog():
    dialog = ReplaceFilePathDialog()
    dialog.exec_()

    
class ReplaceFilePathDialog(QtGui.QDialog):
    
    def __init__(self):
        super(ReplaceFilePathDialog, self).__init__()
        
        self.supportedNodeTypes = [{'label':'Read','types':['Read']},
                                   {'label':'ReadGeo','types':['ReadGeo','ReadGeo2']},
                                   {'label':'Camera','types':['Camera2']}
                                   ]
        self.supportedKnobTypes =[{'label':'File','types':['file']},
                                   {'label':'Proxy','types':['proxy']}
                                 ]
        self.aboutText = "<h3>What does it do?</h3><p>Tired of footage files breaking when you move your project to a different folder or open it on another machine? Relative File Path makes all paths of footage in your NUKE script relative to the location of the NUKE script itself. Now you can copy the folder containing you project wherever you want and the footage will always be found.</p><h3>Tutorial</h3><p>Watch the video tutorial about RelativeFilePath for more infos: http://mamoworld.com/tutorials/relative-file-path-nuke</p>"
        
        self.initUI()
        
    def initUI(self):      
       
        aboutBox =  QtGui.QVBoxLayout()
        aboutText = QtGui.QTextEdit(self.aboutText, self)
        aboutText.setReadOnly(True)
        aboutBox.addWidget(aboutText)
        
        
        buttonsBox =  QtGui.QHBoxLayout()
        self.nodeSelectionChoice = QtGui.QComboBox(self)
        self.nodeSelectionChoice.insertItem(0,"for all nodes")
        self.nodeSelectionChoice.insertItem(1,"for selected nodes")
        buttonsLabel = QtGui.QLabel("replace",self)
        self.commandTypeChoice = QtGui.QComboBox(self)
        self.commandTypeChoice.insertItem(0,"absolute file path by relative one")
        self.commandTypeChoice.insertItem(1,"relative file path by absolute one")
        self.doItButton = QtGui.QPushButton("do it", self)
        buttonsBox.addWidget(self.nodeSelectionChoice)
        buttonsBox.addWidget(buttonsLabel)
        buttonsBox.addWidget(self.commandTypeChoice)
        buttonsBox.addWidget(self.doItButton)
        buttonsBox.addStretch(1)
        
        nodeTypesBox = QtGui.QVBoxLayout()
        nodeTypesLabel = QtGui.QLabel("process the following node types",self)
        nodeTypesBox.addWidget(nodeTypesLabel)
        for t in self.supportedNodeTypes:
            t['checkbox']=QtGui.QCheckBox(t['label'],self)
            t['checkbox'].setCheckState(QtCore.Qt.Checked)
            nodeTypesBox.addWidget(t['checkbox'])
        
        knobTypesBox = QtGui.QVBoxLayout()
        knobTypesLabel = QtGui.QLabel("process the following knob types",self)
        knobTypesBox.addWidget(knobTypesLabel)
        for t in self.supportedKnobTypes:
            t['checkbox']=QtGui.QCheckBox(t['label'],self)
            t['checkbox'].setCheckState(QtCore.Qt.Checked)
            knobTypesBox.addWidget(t['checkbox'])
        
        resultsTextBox =  QtGui.QVBoxLayout()
        resultsLabel = QtGui.QLabel("Results",self)
        self.resultsText = QtGui.QTextEdit(self)
        self.resultsText.setReadOnly(True)
        resultsTextBox.addWidget(resultsLabel)
        resultsTextBox.addWidget(self.resultsText)
        
        warningsTextBox =  QtGui.QVBoxLayout()
        warningsLabel = QtGui.QLabel("Warnings",self)
        self.warningsText = QtGui.QTextEdit(self)
        self.warningsText.setReadOnly(True)
        warningsTextBox.addWidget(warningsLabel)
        warningsTextBox.addWidget(self.warningsText)
        
        closeButtonBox = QtGui.QHBoxLayout()
        closeButton = QtGui.QPushButton("Close", self)
        closeButton.setDefault(True)
        closeButtonBox.addStretch(0.5)
        closeButtonBox.addWidget(closeButton)
        closeButtonBox.addStretch(0.5)
        
        mainBox = QtGui.QVBoxLayout()
        mainBox.addLayout(aboutBox)
        mainBox.addLayout(buttonsBox)
        mainBox.addLayout(nodeTypesBox)
        mainBox.addLayout(knobTypesBox)
        mainBox.addLayout(resultsTextBox)
        mainBox.addLayout(warningsTextBox)
        mainBox.addLayout(closeButtonBox)
        
        closeButton.clicked.connect(self.accept)
        self.doItButton.clicked.connect(self.doIt)
        
        self.setGeometry(300, 300, 1000, 800)
        self.setLayout(mainBox)
        
        self.setWindowTitle("Relative File Path")
    
    

    def doIt(self):
        nodesToProcess = nuke.selectedNodes() if self.nodeSelectionChoice.currentIndex() == 1 else nuke.allNodes()
        processFunction = makeNodesAbsolute if self.commandTypeChoice.currentIndex() == 1 else makeNodesRelative

        filteredNodes = self.filterByNodeType(nodesToProcess)
        
        choosenKnobTypes = self.collectChoosenTypes(self.supportedKnobTypes)
        
        result = processFunction(filteredNodes,choosenKnobTypes)

        self.warningsText.setText("\n\n".join(result['warnings']))
        self.resultsText.setText("\n".join(result['replacements']))
        
    def filterByNodeType(self, nodes):
        wantedNodeTypes = self.collectChoosenTypes(self.supportedNodeTypes)
        
        filteredNodes = []
        for node in nodes:
            if nodeHasOneOfTheNodeClasses(node,wantedNodeTypes):
                filteredNodes.append(node)
        return filteredNodes
    
    def collectChoosenTypes(self, typeData):
        result = []
        for type in typeData:
            if type['checkbox'].isChecked():
                result += type['types']
        return result
        
                
####################
        
def nodeHasOneOfTheKnobTypes(node, knobNameList):
    for knobName in knobNameList:
        if nodeHasKnob(node,knobName):
            return True
    return False

def nodeHasKnob(node, knobName):
    result =  True if node.knob(knobName) else False
    return result


def nodeHasOneOfTheNodeClasses(node,classNameList):
    for className in classNameList:
        if nodeHasClass(node, className):
            return True
    return False

def nodeHasClass(node, className):
    return node.Class()==className

#####################

def makeNodesRelative(nodes, knobTypes):
    result = { 'warnings': [], 'replacements': [], 'projectFolder': None}
    projectfile = nuke.root()['name'].value() 
    if projectfile =="":
        result['warnings'].append('Please save the nuke script before running this function such that it has a valid path.')
        return result
    projectFolderAbsolute = posixpath.dirname(projectfile)
    result['projectFolder'] = projectFolderAbsolute
    projectFolderRelative = "[file dirname [value root.name]]"

    for n in nodes:
        for k in knobTypes:
            if n.knob(k):
                originalFilePath = n[k].value()
                if n[k].isAnimated():
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since the knob is animated')
                elif n[k].hasExpression():
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since the knob has an expression')
                elif originalFilePath.strip()=="":
                    #result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since it is empty')
                    pass
                elif originalFilePath.startswith(projectFolderRelative): 
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since it is already a relative path:\n'+ __removePrefix(originalFilePath,projectFolderRelative))
                else:
                    relativeFilePath =  posixpath.relpath(originalFilePath,projectFolderAbsolute)
                    n[k].setValue(projectFolderRelative + '/' +relativeFilePath)
                    result['replacements'].append(k+' of '+ n['name'].value()+':\n'+relativeFilePath)
                        
    return result



def makeNodesAbsolute(nodes, knobTypes):
    result = { 'warnings': [], 'replacements': [], 'projectFolder': None}
    projectfile = nuke.root()['name'].value() 
    if projectfile =="":
        result['warnings'].append('Please save the nuke script before running this function such that it has a valid path.')
        return result
    projectFolderAbsolute = posixpath.dirname(projectfile)
    result['projectFolder'] = projectFolderAbsolute
    projectFolderRelative = "[file dirname [value root.name]]"

    for n in nodes:
        for k in knobTypes:
            if n.knob(k):
                originalFilePath = n[k].value()
                if n[k].isAnimated():
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since the knob is animated')
                elif n[k].hasExpression():
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since the knob has an expression')
                elif originalFilePath.strip()=="":
                    #result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since it is empty')
                    pass
                elif originalFilePath.startswith(projectFolderRelative):
                    relativeFilePath = __removePrefix(originalFilePath,projectFolderRelative+'/')
                    absoluteFilePath = posixpath.join(projectFolderAbsolute, relativeFilePath)
                    absoluteNormalizedFilePath = posixpath.normpath(absoluteFilePath)
                    n[k].setValue(absoluteNormalizedFilePath)
                    result['replacements'].append(k+' of '+ n['name'].value()+':\n'+absoluteNormalizedFilePath)
                else:
                    result['warnings'].append("Didn't replace "+k+' of node '+n['name'].value()+' since it is no relative path.\nproject path:'+projectFolderAbsolute+'\nfile path: '+originalFilePath)
    
    return result

def printMakeRelativeResults(results):
    print("----------------------------")
    print("attempt to replace file paths by relative variant")
    if len(results['warnings']) > 0:
        print ("warnings:")
        print ("\n\n".join(results['warnings']))
        print("")
    if len(results['replacements']) > 0:
       print("made the following paths relative to the project folder "+ results['projectFolder']+':')
       print ("\n".join(results['replacements']))
       print("")
    print("----------------------------")

def printMakeAbsoluteResults(results):
    print("----------------------------")
    print("attempt to replace relative paths by absolute variant")
    if len(results['warnings']) > 0:
        print ("warnings:")
        print ("\n\n".join(results['warnings']))
        print("")
    if len(results['replacements']) > 0:
       print("made the following paths absolute:")
       print ("\n".join(results['replacements']))
       print("")
    print("----------------------------")

                                  
                                     
def __removePrefix(str,prefix):
    return str[len(prefix):]
    