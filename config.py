# coding=utf-8
# author=weijer
# http://www.cgspread.com

nuke_config = {
    "toolbar": {
        "cgspread": {
            "icon": "logo.png",
            "list": [
                #
                # Image
                #
                {
                    "name": "Image/CWSlate",
                    "command": "CWSlate",
                    "shortcut": "",
                    "icon": "AntsSlate.png",
                    "type": "gizmo"
                },
                {
                    "name": "Image/a_Text",
                    "command": "a_Text",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Image icon
                {
                    "name": "Image",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_image.png",
                    "type": "toolbar"
                },
                #
                # Channel
                # 1、AutoComper
                # 2、PreCompForArnold
                # 3、RenderLayer
                #
                {
                    "name": "Channel/AutoComper",
                    "command": "command.run_autoComper()",
                    "shortcut": "",
                    "icon": "autoComper.png",
                    "type": "python"
                },
                {
                    "name": "Channel/Cryptomatte/Cryptomatte",
                    "command": "command.run_cryptomatte_create()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/Cryptomatte/Decryptomatte All",
                    "command": "command.run_decryptomatte_all()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/Cryptomatte/Decryptomatte Selection",
                    "command": "command.run_decryptomatte_selected()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/Cryptomatte/Encryptomatte",
                    "command": "command.run_encryptomatte()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/PreCompForArnold",
                    "command": "command.run_preCompForArnold()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/RenderLayer",
                    "command": "command.run_RenderLayer()",
                    "shortcut": "",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "Channel/Multimatte",
                    "command": "Multimatte",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Channel/akromatism_stRub",
                    "command": "akromatism_stRub",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Channel/L_MultiplePasses",
                    "command": "L_MultiplePasses",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Channel/Aberration_Chromatique",
                    "command": "Aberration_Chromatique",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Channel/AutocomperArnold",
                    "command": "AutocomperArnold",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Channel icon
                {
                    "name": "Channel",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_channel.png",
                    "type": "toolbar"
                },
                {
                    "name": "Channel/Cryptomatte",
                    "command": "",
                    "shortcut": "",
                    "icon": "cryptomatte_logo.png",
                    "type": "toolbar"
                },
                #
                # Filter
                # 1、RealHeatDistortion
                # 2、iBlur
                # 3、vectorBlurGizmo
                # 4、zBlurGizmo
                # 5、CWDefocus
                # 6、Turbulate
                # 7、Mosaic
                # 8、DilateErodeFine
                # 9、Lightwarp
                # 10、Glow_hub
                #
                {
                    "name": "Filter/RealHeatDistortion",
                    "command": "RealHeatDist",
                    "shortcut": "",
                    "icon": "RealHeatDistortion.png",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/iBlur",
                    "command": "iBlur",
                    "shortcut": "",
                    "icon": "iBlur.png",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/vectorBlurGizmo",
                    "command": "vectorBlurGizmo",
                    "shortcut": "",
                    "icon": "VectorBlur.png",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/zBlurGizmo",
                    "command": "zBlurGizmo",
                    "shortcut": "",
                    "icon": "ZBlur.png",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/CWDefocus",
                    "command": "CWDefocus",
                    "shortcut": "",
                    "icon": "CWDefocus.png",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/Turbulate",
                    "command": "Turbulate",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/Mosaic",
                    "command": "mosaic",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/DilateErodeFine",
                    "command": "DilateErodeFine_CB",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/Lightwarp",
                    "command": "bm_Lightwrap",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Filter/Glow_hub",
                    "command": "glows_hub",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Filter icon
                {
                    "name": "Filter",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_filter.png",
                    "type": "toolbar"
                },
                #
                # Keyer
                # 1、AdditiveKeyer
                # 2、DespillMadness
                # 3、LumaDespill
                # 4、EdgeExtend
                # 5、EdgeExtend
                # 6、hairEasyKey
                # 7、KillOutline
                # 8、alpha_edge
                # 9、EdgeKey
                # 10、Spill_Tool
                # 11、RemoveSkyEdge
                #
                {
                    "name": "Keyer/AdditiveKeyer",
                    "command": "AdditiveKeyer",
                    "shortcut": "",
                    "icon": "KeyerLuminance.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/DespillMadness",
                    "command": "DespillMadness",
                    "shortcut": "",
                    "icon": "DespillMadness.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/LumaDespill",
                    "command": "LumaDespill",
                    "shortcut": "",
                    "icon": "LumaDespill.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/EdgeExtend",
                    "command": "EdgeExtend2",
                    "shortcut": "",
                    "icon": "EdgeDetect.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/hairEasyKey",
                    "command": "hairEasyKey",
                    "shortcut": "",
                    "icon": "Keyer.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/KillOutline",
                    "command": "KillOutline",
                    "shortcut": "",
                    "icon": "VolumeRays.png",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/alpha_edge",
                    "command": "alpha_edge",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/EdgeKey",
                    "command": "EdgeKey",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/Spill_Tool",
                    "command": "Spill_Tool",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/RemoveSkyEdge",
                    "command": "RemoveSkyEdge",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Keyer/a_IDKeyer",
                    "command": "a_IDKeyer",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Keyer icon
                {
                    "name": "Keyer",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_keyer.png",
                    "type": "toolbar"
                },
                #
                # 3D
                # 1、RealHeat CameraProjection
                # 2、EnvRelight
                # 3、ReLighting
                # 4、FallingLeaves
                # 5、RainMaker
                # 6、TX_Fog
                # 6、3D/Tangent_Space_Normals
                #
                {
                    "name": "3D/CameraProjection",
                    "command": "CameraProjection",
                    "shortcut": "",
                    "icon": "Camera.png",
                    "type": "gizmo"
                },
                {
                    "name": "3D/EnvRelight",
                    "command": "EnvRelight",
                    "shortcut": "",
                    "icon": "ReLighting.png",
                    "type": "gizmo"
                },
                {
                    "name": "3D/ReLighting",
                    "command": "ReLighting",
                    "shortcut": "",
                    "icon": "ReLighting.png",
                    "type": "gizmo"
                },
                 {
                    "name": "3D/CreatedPointCloud",
                    "command": "command.run_createdPointCloud()",
                    "shortcut": "",
                    "icon": "pointcloud.png",
                    "type": "python"
                },
                {
                    "name": "3D/FallingLeaves",
                    "command": "FallingLeaves",
                    "shortcut": "",
                    "icon": "FallingLeavesIcon.png",
                    "type": "gizmo"
                },
                {
                    "name": "3D/RainMaker",
                    "command": "RainMaker",
                    "shortcut": "",
                    "icon": "RainMakerIcon.png",
                    "type": "gizmo"
                },
                {
                    "name": "3D/TX_Fog",
                    "command": "TX_Fog",
                    "shortcut": "",
                    "icon": "TXFogIcon.png",
                    "type": "gizmo"
                },
                {
                    "name": "3D/a_RelightSimple",
                    "command": "a_RelightSimple",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/a_ReLighting",
                    "command": "a_ReLighting",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/a_ReLightingP",
                    "command": "a_ReLightingP",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/a_RimLight2D",
                    "command": "a_RimLight2D",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/L_RimLight2D",
                    "command": "L_RimLight2D",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Multi_Tangent_Space_Normals_Generator",
                    "command": "Multi_Tangent_Space_Normals_Generator",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Normalise_Tangent_Space_Normals",
                    "command": "Normalise_Tangent_Space_Normals",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Partial_Derivative_Blending",
                    "command": "Partial_Derivative_Blending",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Tangent_Space_Normals_Generator",
                    "command": "Tangent_Space_Normals_Generator",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Tangent_Space_Normals_Previewer",
                    "command": "Tangent_Space_Normals_Previewer",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "3D/Tangent_Space_Normals/Tangent_Space_Normals_to_Cavity",
                    "command": "Tangent_Space_Normals_to_Cavity",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Channel icon
                {
                    "name": "3D",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_3d.png",
                    "type": "toolbar"
                },
                {
                    "name": "3D/Tangent_Space_Normals",
                    "command": "",
                    "shortcut": "",
                    "icon": "Tangent_Space_Normals.png",
                    "type": "toolbar"
                },
                #
                # Lighting
                # 1、Mask3D_RS
                # 2、ReLight_RS
                # 3、RimLight_RS
                # 4、MT_Relight
                # 5、NormalLighting
                # 6、P_Matte
                # 7、P_Noise3D
                # 8、P_Ramp
                # 9、EnvRelight
                # 10、ReProject3D
                # 11、PP_Mask_hub
                # 12、DepthSlice
                #
                {
                    "name": "Lighting/Mask3D_RS",
                    "command": "Mask3D_RS",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/ReLight_RSS",
                    "command": "ReLight_RS",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/RimLight_RS",
                    "command": "RimLight_RS",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/MT_Relight",
                    "command": "MT_Relight",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/NormalLighting",
                    "command": "normalLighting",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/P_Matte",
                    "command": "P_Matte",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/P_Noise3D",
                    "command": "P_Noise3D",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/P_Ramp",
                    "command": "P_Ramp",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/EnvRelight",
                    "command": "EnvRelight",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/ReProject3D",
                    "command": "ReProject3D",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/PP Mask hub",
                    "command": "PP_Mask_hub",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/DepthSlice",
                    "command": "DepthSlice",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                {
                    "name": "Lighting/Final Flare",
                    "command": "final_flare_tool",
                    "shortcut": "",
                    "icon": "",
                    "type": "gizmo"
                },
                # Lighting icon
                {
                    "name": "Lighting",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_light.png",
                    "type": "toolbar"
                },
                #
                # ToolSet
                # 1、Preset Backdrop
                #
                {
                    "name": "ToolSet/PackProject",
                    "command": "command.run_pack()",
                    "shortcut": "",
                    "icon": "nuke2pack.png",
                    "type": "python"
                },
                {
                    "name": "ToolSet/PresetBackdrop",
                    "command": "command.run_presetBackdrop()",
                    "shortcut": "ctrl+alt+b",
                    "icon": "Backdrop.png",
                    "type": "python"
                },
                {
                    "name": "ToolSet/AutoCrop",
                    "command": "nukescripts.autocrop()",
                    "shortcut": "",
                    "icon": "AutoCrop.png",
                    "type": "python"
                },
                {
                    "name": "ToolSet/BrowseDir",
                    "command": "command.run_browseDir()",
                    "shortcut": "shift+b",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/Single To Sequence",
                    "command": "command.run_SingleToEquence()",
                    "shortcut": "alt+F2",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/Switch Shot",
                    "command": "command.run_switchShot()",
                    "shortcut": "alt+F3",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/Correct Error Read Node",
                    "command": "command.run_correctErrorReadNode()",
                    "shortcut": "alt+F4",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/List Shuffles",
                    "command": "command.run_ListShuffle()",
                    "shortcut": "alt+F5",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/Replace Read Node Path",
                    "command": "command.run_replaceReadNodePath()",
                    "shortcut": "alt+F6",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/toggle stamp",
                    "command": "command.run_toggleStamp()",
                    "shortcut": "alt+Q",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/toggle input",
                    "command": "command.run_toggleInput()",
                    "shortcut": "alt+shift+Q",
                    "icon": "",
                    "type": "python"
                },
                {
                    "name": "ToolSet/nukeFXSExporter",
                    "command": "command.run_nukeFXSExporter()",
                    "shortcut": "",
                    "icon": "NukeFXSExporter.png",
                    "type": "python"
                },
                 {
                    "name": "ToolSet/readFromWrite",
                    "command": "command.run_readFromWrite()",
                    "shortcut": "shift+r",
                    "icon": "",
                    "type": "python"
                },
                # ToolSet icon
                {
                    "name": "ToolSet",
                    "command": "",
                    "shortcut": "",
                    "icon": "icon_toolbar_toolsets.png",
                    "type": "toolbar"
                },
                #
                # Mamoworld
                #
                #
                #MochaImport+
                {
                    "name": "Mamoworld/MochaImport+/Stabilized View+",
                    "command": "command.run_createStabilizedView()",
                    "shortcut": "",
                    "icon": "MiStabilizedView.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/CornerPin+ w. Lens Dist.",
                    "command": "command.run_createCornerPin()",
                    "shortcut": "",
                    "icon": "MiCornerPin.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Tracker+",
                    "command": "command.run_createTracker4Node()",
                    "shortcut": "",
                    "icon": "MiTracker4.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Tracker+ (old)",
                    "command": "command.run_createTracker3Node()",
                    "shortcut": "",
                    "icon": "MiTracker3.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/RotoPaint+",
                    "command": "command.run_createRotoPaintNodeMI()",
                    "shortcut": "",
                    "icon": "MiRotoPaint.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Roto+",
                    "command": "command.run_createRotoNodeMI()",
                    "shortcut": "",
                    "icon": "MiRoto.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/GridWarp+",
                    "command": "command.run_createGridWarpNodeMI()",
                    "shortcut": "",
                    "icon": "MiGridWarp.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Transform+",
                    "command": "command.run_createTransformNodeMI()",
                    "shortcut": "",
                    "icon": "MiMove.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Camera and Geo+",
                    "command": "command.run_createCameraAndPointCloud()",
                    "shortcut": "",
                    "icon": "MiCameraAndGeo.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Full camera rig+",
                    "command": "command.run_createCameraRig()",
                    "shortcut": "",
                    "icon": "MiFullCameraRig.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/MochaImport+/Settings",
                    "command": "command.run_showSettings()",
                    "shortcut": "",
                    "icon": "MiSettings.png",
                    "type": "python"
                },
                #Workflow
                {
                    "name": "Mamoworld/Workflow/Relative file path",
                    "command": "command.run_relativeFilePath()",
                    "shortcut": "",
                    "icon": "MWRelativeFilePath.png",
                    "type": "python"
                },
                {
                    "name": "Mamoworld/Workflow/Collect files",
                    "command": "nuke.message('Not yet implemented')",
                    "shortcut": "",
                    "icon": "MWCollectFiles.png",
                    "type": "python"
                },
                # Mamoworld icon
                {
                    "name": "Mamoworld",
                    "command": "",
                    "shortcut": "",
                    "icon": "Mamoworld.png",
                    "type": "toolbar"
                },
                {
                    "name": "Mamoworld/MochaImport+",
                    "command": "",
                    "shortcut": "",
                    "icon": "MochaImport.png",
                    "type": "toolbar"
                },
                {
                    "name": "Mamoworld/Workflow",
                    "command": "",
                    "shortcut": "",
                    "icon": "MWWorkflow.png",
                    "type": "toolbar"
                },
                # Release Notes icon
                {
                    "name": "Release Notes",
                    "command": "command.run_releaseNotes()",
                    "shortcut": "",
                    "icon": "icon_toolbar_release.png",
                    "type": "python"
                }
            ]
        }
    },
    "toolMenu": {
        # Multi Script Editor
        "ScriptEditor": {
            "name": "Multi Script Editor",
            "command": "command.run_ScriptEditor()",
        }
    }
}
