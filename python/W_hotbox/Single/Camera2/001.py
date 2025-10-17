#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Shot Cam
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('tile_color').setValue(6619135)
	name = i.name()

	if name.startswith('Camera') or name.startswith('ProjectionCamera'):
		counter = 2
		name = 'ShotCamera1'
		while nuke.exists(name):
			name = 'ShotCamera%i'%counter
			counter += 1
		i.setName(name)
		