#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Projection Cam
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
	i.knob('tile_color').setValue(4284809471)
	name = i.name()
	if name.startswith('Camera') or name.startswith('ShotCamera'):
		counter = 2
		name = 'ProjectionCamera1'
		while nuke.exists(name):
			name = 'ProjectionCamera%i'%counter
			counter += 1
		i.setName(name)
