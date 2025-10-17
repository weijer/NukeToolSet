#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localise
#
#----------------------------------------------------------------------------------------------------------

readKnobList = []
for i in nuke.selectedNodes():
	i.knob('cacheLocal').setValue('always')
	readKnobList.append(i.knob('file'))

nuke.localiseFiles(readKnobList)