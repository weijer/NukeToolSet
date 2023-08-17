# to apply any of the help texts, copy and paste the respective code
# to the NUKE script editor, select the node and run the script
import nuke

# START STABILIZED GIZMO HELP

n = nuke.selectedNode()
print(n)
n['help'].setValue("""
<h1>Creates a stabilized view</h1>
<p>Transforms an input image such that only the region of the corner pin track is shown as stabilized view.</p>
<p>This node is normally used as part of a stabilized view rig. The rig uses the StartStabilized node to create a stabilized view on the region of the clip that you tracked. In this stabilized view you can do arbitrary modifications and then go back to the original perspective using an EndStabilized node.</p>

<h2>Inputs of StartStabilized</h2>

<p><strong>Src:</strong>The input clip that you tracked</p>

<p><strong>UndistMap</strong> (optional) a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'undistort'.</p>

<h2>Basic Usage of Stabilized View Rig</h2>
<ol>
<li>From the MochaImportPlus menu, create the stabilized view rig consisting of the StartStabilized node, the EndStabilized node, and the Stabilized View Backdrop.</li>
<li>Load your mocha tracking data in the StartStabilized node.
<li>Do arbitrary manipulations in the Stabilized View by inserting new nodes inside the backdrop. All changes you do there in a stabilized setting will also be visible in your original perspective after the EndStabilized node.</li>
</ol>

<h2>Lens Distortion</h2>
<p>If you've used the mocha Lens module to analyze the lens distortion of your clip, you need to do the following things to get an undistorted stabilized view and reapply the lens distortion to the final result:
<ul>
<li>make sure the mocha corner pin data you load into the StartStabilized node is exported from mocha Pro with the option 'Remove lens distortion'</li>
<li>as UndistMap input of the StartStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'undistort'.</li>
<li>as DistMap input of the EndStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</li>
</ul>""".replace('\n', '').replace('\r', ''))

# END STABILIZED GIZMO HELP

n = nuke.selectedNode()
print(n)
n['help'].setValue("""
<h1>Go back from a stabilized view to the original perspective</h1>
<p>Undoes the stabilization of a stabilized view by reintroducing the movement of the original perspective.</p> 
<p>This node is normally used as part of a stabilized view rig. The rig uses a StartStabilized node to create a stabilized view on the region of the clip that you tracked. In this stabilized view you can do arbitrary modifications and then go back to the original perspective using the EndStabilized node.</p>

<h2>Inputs of EndStabilized</h2>

<p><strong>Stabilized:</strong>The stabilized view including all your manipulations</p>
<strong>Stabilized Plate:</strong>The orignal stabilized view as created by the StartStabilized node and without any modifications
<p><strong>DistMap</strong> (optional) a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</p>

<h2>Basic Usage of Stabilized View Rig</h2>
<ol>
<li>From the MochaImportPlus menu, create the stabilized view rig consisting of the StartStabilized node, the EndStabilized node, and the Stabilized View Backdrop.</li>
<li>Load your mocha tracking data in the StartStabilized node.
<li>Do arbitrary manipulations in the Stabilized View by inserting new nodes inside teh backdrop. All changes you do there in a stabilized setting will also be visible in your original perspective after the EndStabilized node.</li>
</ol>

<h2>Lens Distortion</h2>
<p>If you've used the mocha Lens module to analyze the lens distortion of your clip, you need to do the following things to get an undistorted stabilized view and reapply the lens distortion to the final result:
<ul>
<li>make sure the mocha corner pin data you load into the StartStabilized node is exported from mocha Pro with the option 'Remove lens distortion'</li>
<li>as UndistMap input of the StartStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'undistort'.</li>
<li>as DistMap input of the EndStabilized node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</li>
</ul>""".replace('\n', '').replace('\r', ''))

# CORNER PIN W LENS DIST HELP

n = nuke.selectedNode()
print(n)
n['help'].setValue("""
<h1>Corner Pin With Lens Distortion</h1>
<p>Creates a corner pin based on mocha tracking data and optionally also mocha lens data</p> 
<h2>Inputs</h2>

<p><strong>Src:</strong>The image that you want to corner pin</p>
<strong>Bg:</strong>The background (usually the clip that you tracked). It is required for two things: (1) The node has an option to merge the background behind the corner pin (2) The background is required to correctly interpret the size of the DistMap input
<p><strong>DistMap</strong> (optional) a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</p>

<h2>Basic Usage</h2>
<ol>
<li>Create the node.</li>
<li>connect the Src and Bg inputs</li>
<li>Load your mocha tracking data from the clipboard or from file. The format you need to export from mocha is Nuke corner pin (*.nk)</li>
</ol>

<h2>Lens Distortion</h2>
<p>If you've used the mocha Lens module to analyze the lens distortion of your clip, you need to do the following things to apply both the corner pin and the lens distortion to your image:
<ul>
<li>Make sure to provide the Background (Bg) input, even if you don't want the option to merge in the background. The background is needed to correctly interpret the size of the distortion map.</li>
<li>Make sure the mocha corner pin data you load into the node is exported from mocha Pro with the option 'Remove lens distortion'.</li>
<li>as DistMap input of the node use a Distortion Map Clip (ST Map) exported with the mocha Pro lens module with option 'distort'.</li>
</ul>""".replace('\n', '').replace('\r', ''))
