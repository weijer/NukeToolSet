#! /Applications/Nuke8.0v2/Nuke8.0v2.app/Contents/MacOS/libnuke-8.0.v2.dylib -nx
version 8.0 v2
Group {
 name TX_Fog
 inputs 0
 help "TX_Fog\nby Tomas Lefebvre\n\n/// v2.0"
 tile_color 0xccccccff
 addUserKnob {20 Settings}
 addUserKnob {26 noiseSetupDiv l "<b>noise basic settings</b>"}
 addUserKnob {20 noiseTabBegin l "" +STARTLINE n -2}
 addUserKnob {20 Noise}
 addUserKnob {41 size l x/ysize T Noise0.size}
 addUserKnob {41 zoffset l z T Noise0.zoffset}
 addUserKnob {41 octaves T Noise0.octaves}
 addUserKnob {41 nyquist l "clip at Nyquist limit" -STARTLINE T Noise0.nyquist}
 addUserKnob {41 lacunarity T Noise0.lacunarity}
 addUserKnob {41 gain T Noise0.gain}
 addUserKnob {41 gamma T Noise0.gamma}
 addUserKnob {20 "" l Transform}
 addUserKnob {41 transform T Noise0.transform}
 addUserKnob {41 translate T Noise0.translate}
 addUserKnob {41 rotate T Noise0.rotate}
 addUserKnob {41 scale T Noise0.scale}
 addUserKnob {41 skew +INVISIBLE T Noise0.skew}
 addUserKnob {41 center T Noise0.center}
 addUserKnob {41 xrotate T Noise0.xrotate}
 addUserKnob {41 yrotate T Noise0.yrotate}
 addUserKnob {20 "" l Color}
 addUserKnob {41 color T Noise0.color}
 addUserKnob {6 color_rampBT l ramp +STARTLINE}
 addUserKnob {12 color_p0 l p0}
 color_p0 {100 500}
 addUserKnob {18 color_color2 l color}
 color_color2 {1 0 0}
 addUserKnob {6 color_color2_panelDropped l "panel dropped state" -STARTLINE +HIDDEN}
 addUserKnob {12 color_p1 l p1}
 color_p1 {2000 1500}
 addUserKnob {20 noiseTabEnd l "" +STARTLINE n -3}
 addUserKnob {26 deadSpace1 l "" +STARTLINE T "  "}
 addUserKnob {3 subdivisions}
 subdivisions 10
 addUserKnob {22 update -STARTLINE T "from __future__ import with_statement\nthisNode = nuke.thisNode()\nsubdivs = int(thisNode\['subdivisions'].value())\nresolution = int(thisNode\['resolution'].value())\n\nwith thisNode :\n\n\tnAll = nuke.allNodes()\n\n\tfor n in nAll:\n    \t\tif n.name().split('_')\[0] == 'sub' :\n        \t\t\tnuke.delete(n)\n\tfor j in range(subdivs):\n    \t\ti = j + 1\n\n    \t\t##Noise\n    \t\tnoiseKnobs = \['octaves', 'nyquist', 'lacunarity', 'gain', 'gamma', 'translate', 'rotate', 'skew', 'center', 'ramp', 'color', 'xrotate', 'yrotate']\n    \t\tnoise = nuke.nodes.Noise(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                          \typos =nuke.toNode('Noise0').ypos())\n    \t\tnoise.setName('sub_' + str(i) + '_Noise')\n    \t\tnoise\['color'].setValue(\[0,0,0,0])\n    \t\tfor k in noiseKnobs :\n        \t\t\tnoise\[k].setExpression('parent.Noise0.' + str(k))\n    \t\tnoise\['size'].setValue(\[0,0])\n    \t\tnoise\['size'].setExpression('parent.Noise0.size.0',0)\n    \t\tnoise\['size'].setExpression('parent.Noise0.size.1',1)\n    \t\tnoise\['scale'].setValue(\[0,0])\n    \t\tnoise\['scale'].setExpression('parent.Noise0.scale.w',0)\n    \t\tnoise\['scale'].setExpression('parent.Noise0.scale.h',1)\n    \t\tnoise\['zoffset'].setExpression('parent.Noise0.zoffset+' + str(i) + '*parent.variancy')\n    \t\tnoise\['xrotate'].setExpression('parent.Noise0.xrotate')\n    \t\tnoise\['yrotate'].setExpression('parent.Noise0.yrotate')\n    \t\tnoise.setInput(0,nuke.toNode('Base'))\n\t\n    \t\t##Ramp\n    \t\tunpRamp = nuke.nodes.Unpremult(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                                         \typos =nuke.toNode('Unpremult0').ypos())\n    \t\tunpRamp.setName('sub_' + str(i) + '_Unpremult')\n    \t\tunpRamp\['disable'].setExpression('!parent.color_rampBT')\n    \t\tunpRamp.setInput(0,noise)\n\t\n    \t\tramp = nuke.nodes.Ramp(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                          \typos = nuke.toNode('Ramp0').ypos())\n    \t\tramp.setName('sub_' + str(i) + '_Ramp')\n    \t\tramp\['disable'].setExpression('!parent.color_rampBT')\n    \t\tramp\['p0'].setExpression('parent.color_p0')\n    \t\tramp\['output'].setValue('rgb')\n    \t\tramp\['color'].setValue(\[0,0,0,0])\n    \t\tramp\['color'].setExpression('parent.color_color2.r',0)\n    \t\tramp\['color'].setExpression('parent.color_color2.g',1)\n    \t\tramp\['color'].setExpression('parent.color_color2.b',2)\n    \t\tramp\['p1'].setExpression('parent.color_p1')\n    \t\tramp.setInput(0,unpRamp)\n\t\n\t    \tpreRamp = nuke.nodes.Premult(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                                        \typos =nuke.toNode('Premult0').ypos())\n    \t\tpreRamp.setName('sub_' + str(i) + '_premult')\n    \t\tpreRamp\['disable'].setExpression('!parent.color_rampBT')\n    \t\tpreRamp.setInput(0,ramp)\n\t\n\n    \t\t##Blur\n    \t\tblur = nuke.nodes.Blur(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                     \typos = nuke.toNode('Blur0').ypos())\n    \t\tblur.setName('sub_' + str(i) + '_Blur')\n    \t\tblur\['channel'].setValue('rgba')\n    \t\tblur\['size'].setValue(\[10,20])\n    \t\tblur\['size'].setExpression('parent.Blur0.size.w',0)\n    \t\tblur\['size'].setExpression('parent.Blur0.size.h',1)\n    \t\tblur.setInput(0,preRamp)\n\t\n\n    \t\t##Edge smooth\n    \t\tsmoothEdge = nuke.nodes.Multiply(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                  \t\t\t                      \typos =nuke.toNode('Multiply0').ypos())\n    \t\tsmoothEdge.setName('sub_' + str(i) + '_Multiply_SEdges')\n    \t\tsmoothEdge\['channel'].setValue('rgba')\n    \t\tsmoothEdge\['value'].setValue(0)\n    \t\tsmoothEdge\['invert_mask'].setValue(True)\n    \t\tsmoothEdge\['disable'].setExpression('!parent.softEdges')\n    \t\tsmoothEdge.setInput(0,blur)\n    \t\tsmoothEdge.setInput(1, nuke.toNode('GradeEdge'))\n    \t\n    \t\t##All the ramps\n    \t\tdecay_x = nuke.nodes.Ramp(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                               \typos =nuke.toNode('Ramp_X0').ypos())\n    \t\tdecay_x.setName('sub_' + str(i) + '_Ramp_x')\n    \t\tdecay_x\['type'].setValue('smooth')\n    \t\tdecay_x\['color'].setValue(0)\n    \t\tdecay_x\['disable'].setExpression('!parent.decay_XBT')\n    \t\tdecay_x\['p0'].setValue(\[100,100])\n    \t\tdecay_x\['p0'].setExpression('(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48',0)\n    \t\tdecay_x\['p1'].setValue(\[100,100])\n    \t\tdecay_x\['p1'].setExpression('(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48',0)\n    \t\tdecay_x.setInput(0,smoothEdge)\n\t\t\n    \t\tdecayx = nuke.nodes.Ramp(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                                        \t           \typos =nuke.toNode('RampX0').ypos())\n    \t\tdecayx.setName('sub_' + str(i) + '_Rampx')\n    \t\tdecayx\['type'].setValue('smooth')\n    \t\tdecayx\['color'].setValue(0)\n    \t\tdecayx\['disable'].setExpression('!parent.decayXBT')\n    \t\tdecayx\['p0'].setValue(\[100,100])\n    \t\tdecayx\['p0'].setExpression('2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48',0)\n    \t\tdecayx\['p1'].setValue(\[100,100])\n    \t\tdecayx\['p1'].setExpression('2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48',0)\n    \t\tdecayx.setInput(0,decay_x)\n\t\t\n    \t\tdecay_y = nuke.nodes.Ramp(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                    \t                               \typos =nuke.toNode('Ramp_Y0').ypos())\n    \t\tdecay_y.setName('sub_' + str(i) + '_Ramp_y')\n    \t\tdecay_y\['type'].setValue('smooth')\n    \t\tdecay_y\['color'].setValue(0)\n    \t\tdecay_y\['disable'].setExpression('!parent.decay_YBT')\n    \t\tdecay_y\['p0'].setExpression('(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48',1)\n    \t\tdecay_y\['p1'].setExpression('(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48',1)    \t\t\t\t\t\t\t\n\t\tdecay_y.setInput(0,decayx)\n\n\n\t    \tdecayy = nuke.nodes.Ramp(xpos = nuke.toNode('Noise0').xpos()+i*150,\n\t\t\t\typos =nuke.toNode('RampY0').ypos())\n\t    \tdecayy.setName('sub_' + str(i) + '_Rampy')\n\t    \tdecayy\['type'].setValue('smooth')\n\t    \tdecayy\['color'].setValue(0)\n\t    \tdecayy\['disable'].setExpression('!parent.decayYBT')\n\t    \tdecayy\['p0'].setExpression('2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48',1)\n\t    \tdecayy\['p1'].setExpression('2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48',1)\n\t    \tdecayy.setInput(0,decay_y)\n\t\n\t    \tdecay_z = nuke.nodes.Dissolve(xpos = nuke.toNode('Noise0').xpos()+i*150,\n\t                                                       \typos =nuke.toNode('Dissolve_Z0').ypos())\n\t    \tdecay_z.setName('sub_' + str(i) + '_Dissolve_z')\n\t    \tdecay_z\['channel'].setValue('rgba')\n\t    \tdecay_z\['disable'].setExpression('!parent.decay_ZBT')\n\t    \tdecay_z\['which'].setExpression('parent.decay_Zmin>='+str(i)+'*100/'+str(subdivs)+'?1:parent.decay_Zmax<='+str(i)+'*100/'+str(subdivs)+'?0:1-('+str(i)+'*100/'+str(subdivs)+'-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))')\n\t    \tdecay_z\['disable'].setExpression('!parent.decay_ZBT')\n    \t\tdecay_z.setInput(1,nuke.toNode('Base'))\n    \t\tdecay_z.setInput(0,decayy)\n\t\n\n\n \t   \t##Opacity\n    \t\tdissolve = nuke.nodes.Dissolve(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                                        \t               \typos =nuke.toNode('Dissolve0').ypos())\n    \t\tdissolve.setName('sub_' + str(i) + '_Dissolve')\n    \t\tdissolve\['channel'].setValue('rgba')\n    \t\tdissolve\['which'].setExpression('parent.Dissolve0.which')\n    \t\tdissolve.setInput(1,decay_z)\n    \t\tdissolve.setInput(0,nuke.toNode('Base'))\n\t\t\n\n\t    \t##Card\n\t    \tcard = nuke.nodes.Card2(xpos = nuke.toNode('Noise0').xpos()+i*150,\n\t                                              \typos =nuke.toNode('Card0').ypos())\n\t    \tcard.setName('sub_' + str(i) + '_Card')\n\t    \tcard\['rows'].setExpression('parent.resolution')\n\t    \tcard\['columns'].setExpression('parent.resolution')\n\t    \tcard\['translate'].setValue(\[0,0,0.5-i*1/subdivs])\n\t    \tcard.setInput(0,dissolve)\n\n\n\n    \t\t##ProcGeo\n\t    \tproc = nuke.nodes.ProcGeo(xpos = nuke.toNode('Noise0').xpos()+i*150,\n                     \t                         \typos =nuke.toNode('ProcGeo0').ypos())\n    \t\tproc.setName('sub_' + str(i) + '_ProcGeo')\n    \t\tproc\['x_size'].setExpression('parent.dNoiseX')\n    \t\tproc\['x_offset'].setExpression('parent.dNoiseXoffset+' + str(i) + '*parent.dNoiseVariancy')\n    \t\tproc\['y_size'].setExpression('parent.dNoiseY')\n    \t\tproc\['y_offset'].setExpression('parent.dNoiseYoffset+' + str(i) + '*parent.dNoiseVariancy')\n    \t\tproc\['Octaves'].setExpression('parent.dNoiseOctaves')\n    \t\tproc\['Lacunarity'].setExpression('parent.dNoiseLacunarity')\n    \t\tproc\['Gain'].setExpression('parent.dNoiseGain')\n    \t\tproc\['Speed'].setExpression('parent.dNoiseSpeed')\n    \t\tproc\['disable'].setExpression('!parent.dNoise')\n    \t\tproc.setInput(0,card)\n    \t\tnuke.toNode('Scene_layers').setInput(i,proc)\n\n\n\n\n"}
 addUserKnob {3 resolution l "   resolution" -STARTLINE}
 resolution 10
 addUserKnob {26 noiseAdvSetupDiv l "<b>noise advance settings</b>"}
 addUserKnob {14 blurSize l "blur size" R 0 100}
 addUserKnob {6 softEdges l "soft edges" +STARTLINE}
 softEdges true
 addUserKnob {7 softEdgesSize l "  size" -STARTLINE R 0 300}
 softEdgesSize 200
 addUserKnob {7 opacity}
 opacity 0.25
 addUserKnob {7 variancy R 0 200}
 variancy 100
 addUserKnob {20 decayGroup l decay n 1}
 decayGroup 0
 addUserKnob {6 decay_XBT l -x +STARTLINE}
 addUserKnob {7 decay_Xmin l "  min" -STARTLINE R 0 100}
 addUserKnob {7 decay_Xmax l "  max" -STARTLINE R 0 100}
 decay_Xmax 25
 addUserKnob {6 decayXBT l " x" +STARTLINE}
 addUserKnob {7 decayXmin l "  min" -STARTLINE R 0 100}
 addUserKnob {7 decayXmax l "  max" -STARTLINE R 0 100}
 decayXmax 25
 addUserKnob {6 decay_YBT l -y +STARTLINE}
 addUserKnob {7 decay_Ymin l "  min" -STARTLINE R 0 100}
 addUserKnob {7 decay_Ymax l "  max" -STARTLINE R 0 100}
 decay_Ymax 25
 addUserKnob {6 decayYBT l " y" +STARTLINE}
 addUserKnob {7 decayYmin l "  min" -STARTLINE R 0 100}
 addUserKnob {7 decayYmax l "  max" -STARTLINE R 0 100}
 decayYmax 25
 addUserKnob {6 decay_ZBT l -z +STARTLINE}
 addUserKnob {7 decay_Zmin l "  min" -STARTLINE R 0 100}
 addUserKnob {7 decay_Zmax l "  max" -STARTLINE R 0 100}
 decay_Zmax 25
 addUserKnob {6 decayZBT l INVISIBLE +INVISIBLE +STARTLINE}
 addUserKnob {20 endGroup l decayEndGroup n -1}
 addUserKnob {20 cage n 1}
 cage 0
 addUserKnob {41 cube l cage T Cube1.cube}
 addUserKnob {13 cage_position l translate}
 addUserKnob {13 cage_rotation l rotate}
 addUserKnob {7 cage_scale l scale R 0 50}
 cage_scale 1
 addUserKnob {20 endGroup_1 l endGroup n -1}
 addUserKnob {20 displace n 1}
 displace 0
 addUserKnob {6 bend +STARTLINE}
 addUserKnob {7 bendX l x R -1 1}
 addUserKnob {7 bendY l y R -1 1}
 addUserKnob {26 noisetxt l "" +STARTLINE T " "}
 addUserKnob {6 dNoise l noise +STARTLINE}
 addUserKnob {7 dNoiseX l "x size" R 0 20}
 dNoiseX 2
 addUserKnob {7 dNoiseXoffset l "x offset" R 0 100}
 addUserKnob {7 dNoiseY l "y size" R 0 20}
 dNoiseY 2
 addUserKnob {7 dNoiseYoffset l "y offset" R 0 100}
 addUserKnob {7 dNoiseVariancy l variancy R 0 10}
 dNoiseVariancy 1
 addUserKnob {3 dNoiseOctaves l octaves}
 dNoiseOctaves 5
 addUserKnob {7 dNoiseLacunarity l lacunarity R 0 5}
 dNoiseLacunarity 5
 addUserKnob {7 dNoiseGain l gain R -1 1}
 addUserKnob {7 dNoiseSpeed l speed R 0 10}
 addUserKnob {20 endGroup_2 l endGroup n -1}
 addUserKnob {26 dummy1 l " " T " "}
 addUserKnob {26 credit l "v2.1 -  Tomas Lefebvre"}
}
 Constant {
  inputs 0
  channels rgb
  color {0 0 0 0}
  format "2048 2048 0 0 2048 2048 1 square_2K"
  name Base
  xpos -371
  ypos -473
 }
set N1daaef30 [stack 0]
push $N1daaef30
 Shuffle {
  alpha white
  name ShuffleEdge
  label "\[value in]"
  xpos -23
  ypos -456
 }
 Crop {
  box {0 0 2048 2048}
  softness {{parent.BlurEdge.size i}}
  reformat true
  crop false
  name CropEdge
  xpos -23
  ypos -374
 }
 Blur {
  channels alpha
  size {{parent.softEdgesSize i}}
  name BlurEdge
  label "\[value size]"
  xpos -23
  ypos -348
 }
 Grade {
  channels alpha
  blackpoint 0.15
  white_clamp true
  mix {{parent.BlurEdge.size/100 i}}
  name GradeEdge
  xpos -23
  ypos -290
 }
set N1da76ee0 [stack 0]
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+10*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_10_Noise
  xpos 236
  ypos -20
 }
 Unpremult {
  name sub_10_Unpremult
  xpos 236
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_10_Ramp
  xpos 236
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_10_premult
  xpos 236
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_10_Blur
  xpos 236
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_10_Multiply_SEdges
  xpos 236
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_10_Ramp_x
  xpos 236
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_10_Rampx
  xpos 236
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_10_Ramp_y
  xpos 236
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_10_Rampy
  xpos 236
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=10*100/10?1:parent.decay_Zmax<=10*100/10?0:1-(10*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_10_Dissolve_z
  xpos 236
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_10_Dissolve
  xpos 236
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 -0.5}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_10_Card
  xpos 236
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+10*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+10*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_10_ProcGeo
  xpos 236
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+9*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_9_Noise
  xpos 86
  ypos -20
 }
 Unpremult {
  name sub_9_Unpremult
  xpos 86
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_9_Ramp
  xpos 86
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_9_premult
  xpos 86
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_9_Blur
  xpos 86
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_9_Multiply_SEdges
  xpos 86
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_9_Ramp_x
  xpos 86
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_9_Rampx
  xpos 86
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_9_Ramp_y
  xpos 86
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_9_Rampy
  xpos 86
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=9*100/10?1:parent.decay_Zmax<=9*100/10?0:1-(9*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_9_Dissolve_z
  xpos 86
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_9_Dissolve
  xpos 86
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 -0.4}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_9_Card
  xpos 86
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+9*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+9*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_9_ProcGeo
  xpos 86
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+8*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_8_Noise
  xpos -64
  ypos -20
 }
 Unpremult {
  name sub_8_Unpremult
  xpos -64
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_8_Ramp
  xpos -64
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_8_premult
  xpos -64
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_8_Blur
  xpos -64
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_8_Multiply_SEdges
  xpos -64
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_8_Ramp_x
  xpos -64
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_8_Rampx
  xpos -64
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_8_Ramp_y
  xpos -64
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_8_Rampy
  xpos -64
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=8*100/10?1:parent.decay_Zmax<=8*100/10?0:1-(8*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_8_Dissolve_z
  xpos -64
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_8_Dissolve
  xpos -64
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 -0.3}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_8_Card
  xpos -64
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+8*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+8*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_8_ProcGeo
  xpos -64
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+7*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_7_Noise
  xpos -214
  ypos -20
 }
 Unpremult {
  name sub_7_Unpremult
  xpos -214
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_7_Ramp
  xpos -214
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_7_premult
  xpos -214
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_7_Blur
  xpos -214
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_7_Multiply_SEdges
  xpos -214
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_7_Ramp_x
  xpos -214
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_7_Rampx
  xpos -214
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_7_Ramp_y
  xpos -214
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_7_Rampy
  xpos -214
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=7*100/10?1:parent.decay_Zmax<=7*100/10?0:1-(7*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_7_Dissolve_z
  xpos -214
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_7_Dissolve
  xpos -214
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 -0.2}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_7_Card
  xpos -214
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+7*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+7*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_7_ProcGeo
  xpos -214
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+6*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_6_Noise
  xpos -364
  ypos -20
 }
 Unpremult {
  name sub_6_Unpremult
  xpos -364
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_6_Ramp
  xpos -364
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_6_premult
  xpos -364
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_6_Blur
  xpos -364
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_6_Multiply_SEdges
  xpos -364
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_6_Ramp_x
  xpos -364
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_6_Rampx
  xpos -364
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_6_Ramp_y
  xpos -364
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_6_Rampy
  xpos -364
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=6*100/10?1:parent.decay_Zmax<=6*100/10?0:1-(6*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_6_Dissolve_z
  xpos -364
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_6_Dissolve
  xpos -364
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 -0.1}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_6_Card
  xpos -364
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+6*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+6*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_6_ProcGeo
  xpos -364
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+5*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_5_Noise
  xpos -514
  ypos -20
 }
 Unpremult {
  name sub_5_Unpremult
  xpos -514
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_5_Ramp
  xpos -514
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_5_premult
  xpos -514
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_5_Blur
  xpos -514
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_5_Multiply_SEdges
  xpos -514
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_5_Ramp_x
  xpos -514
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_5_Rampx
  xpos -514
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_5_Ramp_y
  xpos -514
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_5_Rampy
  xpos -514
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=5*100/10?1:parent.decay_Zmax<=5*100/10?0:1-(5*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_5_Dissolve_z
  xpos -514
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_5_Dissolve
  xpos -514
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_5_Card
  xpos -514
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+5*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+5*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_5_ProcGeo
  xpos -514
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+4*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_4_Noise
  xpos -664
  ypos -20
 }
 Unpremult {
  name sub_4_Unpremult
  xpos -664
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_4_Ramp
  xpos -664
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_4_premult
  xpos -664
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_4_Blur
  xpos -664
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_4_Multiply_SEdges
  xpos -664
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_4_Ramp_x
  xpos -664
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_4_Rampx
  xpos -664
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_4_Ramp_y
  xpos -664
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_4_Rampy
  xpos -664
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=4*100/10?1:parent.decay_Zmax<=4*100/10?0:1-(4*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_4_Dissolve_z
  xpos -664
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_4_Dissolve
  xpos -664
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 0.1}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_4_Card
  xpos -664
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+4*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+4*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_4_ProcGeo
  xpos -664
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+3*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_3_Noise
  xpos -814
  ypos -20
 }
 Unpremult {
  name sub_3_Unpremult
  xpos -814
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_3_Ramp
  xpos -814
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_3_premult
  xpos -814
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_3_Blur
  xpos -814
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_3_Multiply_SEdges
  xpos -814
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_3_Ramp_x
  xpos -814
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_3_Rampx
  xpos -814
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_3_Ramp_y
  xpos -814
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_3_Rampy
  xpos -814
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=3*100/10?1:parent.decay_Zmax<=3*100/10?0:1-(3*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_3_Dissolve_z
  xpos -814
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_3_Dissolve
  xpos -814
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 0.2}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_3_Card
  xpos -814
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+3*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+3*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_3_ProcGeo
  xpos -814
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+2*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_2_Noise
  xpos -964
  ypos -20
 }
 Unpremult {
  name sub_2_Unpremult
  xpos -964
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_2_Ramp
  xpos -964
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_2_premult
  xpos -964
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_2_Blur
  xpos -964
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_2_Multiply_SEdges
  xpos -964
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_2_Ramp_x
  xpos -964
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_2_Rampx
  xpos -964
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_2_Ramp_y
  xpos -964
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_2_Rampy
  xpos -964
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=2*100/10?1:parent.decay_Zmax<=2*100/10?0:1-(2*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_2_Dissolve_z
  xpos -964
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_2_Dissolve
  xpos -964
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 0.3}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_2_Card
  xpos -964
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+2*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+2*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_2_ProcGeo
  xpos -964
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size {{parent.Noise0.size.0} {parent.Noise0.size.1}}
  zoffset {{parent.Noise0.zoffset+1*parent.variancy}}
  octaves {{parent.Noise0.octaves}}
  nyquist {{parent.Noise0.nyquist}}
  lacunarity {{parent.Noise0.lacunarity}}
  gain {{parent.Noise0.gain}}
  gamma {{parent.Noise0.gamma}}
  translate {{parent.Noise0.translate} {parent.Noise0.translate}}
  rotate {{parent.Noise0.rotate}}
  scale {{parent.Noise0.scale.w} {parent.Noise0.scale.h}}
  center {{parent.Noise0.center} {parent.Noise0.center}}
  xrotate {{parent.Noise0.xrotate}}
  yrotate {{parent.Noise0.yrotate}}
  ramp {{parent.Noise0.ramp}}
  color {{parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color} {parent.Noise0.color}}
  name sub_1_Noise
  xpos -1114
  ypos -20
 }
 Unpremult {
  name sub_1_Unpremult
  xpos -1114
  ypos 6
  disable {{!parent.color_rampBT}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0} {parent.color_p0}}
  p1 {{parent.color_p1} {parent.color_p1}}
  color {{parent.color_color2.r} {parent.color_color2.g} {parent.color_color2.b} 0}
  name sub_1_Ramp
  xpos -1114
  ypos 32
  disable {{!parent.color_rampBT}}
 }
 Premult {
  name sub_1_premult
  xpos -1114
  ypos 58
  disable {{!parent.color_rampBT}}
 }
 Blur {
  channels rgba
  size {{parent.Blur0.size.w} {parent.Blur0.size.h}}
  name sub_1_Blur
  xpos -1114
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name sub_1_Multiply_SEdges
  xpos -1114
  ypos 210
  disable {{!parent.softEdges}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48} 100}
  type smooth
  color 0
  name sub_1_Ramp_x
  xpos -1114
  ypos 271
  disable {{!parent.decay_XBT}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48} 100}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48} 100}
  type smooth
  color 0
  name sub_1_Rampx
  xpos -1114
  ypos 297
  disable {{!parent.decayXBT}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48}}
  type smooth
  color 0
  name sub_1_Ramp_y
  xpos -1114
  ypos 327
  disable {{!parent.decay_YBT}}
 }
 Ramp {
  p0 {100 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48}}
  p1 {100 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48}}
  type smooth
  color 0
  name sub_1_Rampy
  xpos -1114
  ypos 353
  disable {{!parent.decayYBT}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.decay_Zmin>=1*100/10?1:parent.decay_Zmax<=1*100/10?0:1-(1*100/10-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))/(parent.decay_Zmax-(parent.decay_Zmin>=parent.decay_Zmax?parent.decay_Zmax-0.01:parent.decay_Zmin))}}
  name sub_1_Dissolve_z
  xpos -1114
  ypos 407
  disable {{!parent.decay_ZBT}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.Dissolve0.which}}
  name sub_1_Dissolve
  xpos -1114
  ypos 580
 }
 Card2 {
  rows {{parent.resolution}}
  columns {{parent.resolution}}
  translate {0 0 0.4}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0 0 0} 
1 {0 -0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {0.5 0 0} 
1 {0.5 -0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666865 0} 1 {0 0 0} 1 {1 0 0} 
1 {-0.5 0 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0 0.5 0} 
1 {0 0 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {0.5 0.5 0} 
1 {0.5 0 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0.1666666716 0} 1 {0 -0.1666666716 0} 1 {1 0.5 0} 
1 {-0.5 0.5 0} 1 {0.1666666865 0 0} 1 {0 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0 1 0} 
1 {0 0.5 0} 1 {0.1666666716 0 0} 1 {-0.1666666716 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {0.5 1 0} 
1 {0.5 0.5 0} 1 {0 0 0} 1 {-0.1666666865 0 0} 1 {0 0 0} 1 {0 -0.1666666865 0} 1 {1 1 0} }
  name sub_1_Card
  xpos -1114
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX}}
  x_offset {{parent.dNoiseXoffset+1*parent.dNoiseVariancy}}
  y_size {{parent.dNoiseY}}
  y_offset {{parent.dNoiseYoffset+1*parent.dNoiseVariancy}}
  Octaves {{parent.dNoiseOctaves}}
  Lacunarity {{parent.dNoiseLacunarity}}
  Gain {{parent.dNoiseGain}}
  Speed {{parent.dNoiseSpeed}}
  name sub_1_ProcGeo
  xpos -1114
  ypos 805
  disable {{!parent.dNoise}}
 }
push $N1daaef30
push $N1da76ee0
push $N1daaef30
 Noise {
  size 300
  center {1099 567}
  xrotate 5
  yrotate 5
  p1 {204 926}
  color0 {1 0.1200000048 0.1200000048 0}
  p0 {494 52}
  name Noise0
  xpos -1264
  ypos -20
 }
 Unpremult {
  name Unpremult0
  xpos -1264
  ypos 6
  disable {{!parent.color_rampBT i}}
 }
 Ramp {
  output rgb
  p0 {{parent.color_p0 i} {parent.color_p0 i}}
  p1 {{parent.color_p1 i} {parent.color_p1 i}}
  color {{parent.color_color2 i} {parent.color_color2 i} {parent.color_color2 i} {parent.color_color2 i}}
  name Ramp0
  xpos -1264
  ypos 32
  disable {{!parent.color_rampBT i}}
 }
 Premult {
  name Premult0
  xpos -1264
  ypos 58
  disable {{!parent.color_rampBT i}}
 }
 Blur {
  channels rgba
  size {{parent.blurSize i} {parent.blurSize i}}
  name Blur0
  label "\[value size]"
  xpos -1264
  ypos 107
 }
 Multiply {
  inputs 1+1
  channels rgba
  value 0
  invert_mask true
  name Multiply0
  xpos -1264
  ypos 210
  disable {{!parent.softEdges i}}
 }
 Ramp {
  p0 {{(parent.decay_Xmax==0?1:parent.decay_Xmax)*20.48 i} 100}
  p1 {{(parent.decay_Xmin>=parent.decay_Xmax?parent.decay_Xmax-1:parent.decay_Xmin)*20.48 i} 100}
  type smooth
  color 0
  name Ramp_X0
  xpos -1264
  ypos 271
  disable {{!parent.decay_XBT i}}
 }
 Ramp {
  p0 {{2048-(parent.decayXmax==0?1:parent.decayXmax)*20.48 i} 200}
  p1 {{2048-(parent.decayXmin>=parent.decayXmax?parent.decayXmax-1:parent.decayXmin)*20.48 i} 200}
  type smooth
  color 0
  name RampX0
  xpos -1264
  ypos 297
  disable {{!parent.decayXBT i}}
 }
 Ramp {
  p0 {100 {(parent.decay_Ymax==0?1:parent.decay_Ymax)*20.48 i}}
  p1 {100 {(parent.decay_Ymin>=parent.decay_Ymax?parent.decay_Ymax-1:parent.decay_Ymin)*20.48 i}}
  type smooth
  color 0
  name Ramp_Y0
  xpos -1264
  ypos 327
  disable {{!parent.decay_YBT i}}
 }
 Ramp {
  p0 {200 {2048-(parent.decayYmax==0?1:parent.decayYmax)*20.48 i}}
  p1 {200 {2048-(parent.decayYmin>=parent.decayYmax?parent.decayYmax-1:parent.decayYmin)*20.48 i}}
  color 0
  name RampY0
  xpos -1264
  ypos 353
  disable {{!parent.decayYBT i}}
 }
 Dissolve {
  inputs 2
  channels rgba
  which 1
  name Dissolve_Z0
  xpos -1264
  ypos 407
  disable {{!parent.decay_ZBT i}}
 }
push $N1daaef30
 Dissolve {
  inputs 2
  channels rgba
  which {{parent.opacity i}}
  name Dissolve0
  xpos -1264
  ypos 580
 }
 Card2 {
  rows {{parent.resolution i}}
  columns {{parent.resolution i}}
  translate {0 0 0.5}
  control_points {3 3 3 6 

1 {-0.5 -0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0 0 0} 
1 {0 -0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {0.5 0 0} 
1 {0.5 -0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666865 0} 0 {0 0 0} 0 {1 0 0} 
1 {-0.5 0 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0 0.5 0} 
1 {0 0 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {0.5 0.5 0} 
1 {0.5 0 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0.1666666716 0} 0 {0 -0.1666666716 0} 0 {1 0.5 0} 
1 {-0.5 0.5 0} 0 {0.1666666865 0 0} 0 {0 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0 1 0} 
1 {0 0.5 0} 0 {0.1666666716 0 0} 0 {-0.1666666716 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {0.5 1 0} 
1 {0.5 0.5 0} 0 {0 0 0} 0 {-0.1666666865 0 0} 0 {0 0 0} 0 {0 -0.1666666865 0} 0 {1 1 0} }
  name Card0
  xpos -1264
  ypos 779
 }
 ProcGeo {
  x_size {{parent.dNoiseX i}}
  x_offset {{parent.dNoiseXoffset i}}
  y_size {{parent.dNoiseY i}}
  y_offset {{parent.dNoiseYoffset i}}
  Octaves {{parent.dNoiseOctaves i}}
  Lacunarity {{parent.dNoiseLacunarity i}}
  Gain {{parent.dNoiseGain i}}
  Speed {{parent.dNoiseSpeed i}}
  name ProcGeo0
  xpos -1264
  ypos 805
  disable {{!parent.dNoise i}}
 }
 Scene {
  inputs 11
  name Scene_layers
  xpos -206
  ypos 1173
 }
 CrosstalkGeo {
  crossover {x {}
    y {}
    z {}
    x->y {}
    x->z {(-pow2(x*2))*bendX C 0}
    y->x {}
    y->z {(-pow2(x*2))*bendY C 0}
    z->x {}
    z->y {}}
  name CrosstalkGeo_bend
  xpos -216
  ypos 1266
  disable {{!parent.bend i}}
 }
 TransformGeo {
  translate {{(parent.Cube1.cube.x+parent.Cube1.cube.r)/2 i} {(parent.Cube1.cube.y+parent.Cube1.cube.t)/2 i} {(parent.Cube1.cube.n+parent.Cube1.cube.f)/2 i}}
  scaling {{(parent.Cube1.cube.r-parent.Cube1.cube.x) i} {(parent.Cube1.cube.t-parent.Cube1.cube.y) i} {(parent.Cube1.cube.f-parent.Cube1.cube.n) i}}
  name TransformGeo_cage
  xpos -216
  ypos 1404
 }
 TransformGeo {
  translate {{parent.cage_position i} {parent.cage_position i} {parent.cage_position i}}
  rotate {{parent.cage_rotation i} {parent.cage_rotation i} {parent.cage_rotation i}}
  uniform_scale {{parent.cage_scale i}}
  name TransformGeo_transform
  xpos -216
  ypos 1467
 }
 Output {
  name Output1
  xpos -216
  ypos 1640
 }
 Cube {
  inputs 0
  display wireframe
  render_mode off
  rows 1
  columns 1
  translate {{parent.cage_position i x1001 1.745000005} {parent.cage_position i x1001 0} {parent.cage_position i x1001 0}}
  rotate {{parent.cage_rotation i} {parent.cage_rotation i} {parent.cage_rotation i}}
  uniform_scale {{parent.cage_scale i}}
  name Cube1
  xpos 48
  ypos 1402
 }
end_group
