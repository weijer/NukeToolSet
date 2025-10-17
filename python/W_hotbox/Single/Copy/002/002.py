#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: 04
#
#----------------------------------------------------------------------------------------------------------

number = 4
layerName = 'CustomMatte'+str(number).zfill(2)
channels =  ['red','green','blue']
rgbaChannels = ['rgba.%s'%i for i in channels]
matteChannels = ['%s.%s'%(layerName,i) for i in channels]
nuke.Layer(layerName, matteChannels)

for i in nuke.selectedNodes():
    for index in range(3):
        i.knob('from%d'%index).setValue(rgbaChannels[index])
        i.knob('to%d'%index).setValue(matteChannels[index])
		i.knob('tile_color').setValue(421934079)