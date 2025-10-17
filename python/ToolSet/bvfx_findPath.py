# Boundary Visual Effects - findPathbvfx
# Version 1.15
#
# For greeting, bugs, and requests email me at mborgo[at]boundaryvfx.com
#
# If you like it and use it frequently, please consider a small donation to the author,
# via Paypal on the email mborgo[at]boundaryvfx.com

# ===============================================================================
# This script is an extension/inspired by the work of my friend Dubi, original at http://www.nukepedia.com/python/misc/findpath/
# ===============================================================================

# ===============================================================================
# Version Log
# v1.16 (2017/05/29)
# added a suggested path for further automation
# v1.15 (2015/07/20)
# added search inside Groups
# v1.14 (2014/04/01)
# fixing a font path issue that halts script on Nuke v8
# fix for multiple read nodes with same file reference
# v1.13 (2013/07/25)
# Reverted the check order to avoid asking for a directory to search if there was no error on nodes.
#
# v1.12 (2013/02/07)
# added vfield_file to search, should be better implemented later
# automatic fix for wrong font path on text nodes.
#
# v1 (2012/11/23)
# All Nodes that own a file propertie will be searched
# Single os.walk for faster searchs
# Changed the %0d to a more generic search
# Added task progress that can cancel the search
# Added loop breaks to speed script velocity
# ===============================================================================

# ===============================================================================
# TO DO LIST
# Options to make paths relative from script location
# change missing fonts to default path [python nuke.defaultFontPathname()]
# ===============================================================================


# Copyright (c) 2012, Magno Borgo
# All rights reserved.
#
# BSD-style license:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Magno Borgo or its contributors may be used to
#       endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import nuke
import fnmatch
import os
import time


def bvfx_findPath(write=True, suggestedPath=None):
    start_time = time.time()
    finalmessage = ""
    newfindname = ""
    cancel = False
    errors = [node for node in nuke.allNodes() if node.error() == True]

    nodes = []
    # ===========================================================================
    # fix font errors
    # ===========================================================================
    try:

        fonts = [node for node in errors for n in range(node.getNumKnobs()) if node.knob(n).name() == "font"]
        for node in fonts:
            node.knob("font").setValue("[python nuke.defaultFontPathname()]")

    except:
        pass

    nodes = [node for node in errors for n in range(node.getNumKnobs()) if
             node.knob(n).name() == "file" or node.knob(n).name() == "vfield_file"]

    # ===========================================================================
    # search for nodes inside groups
    # ===========================================================================#
    # ===========================================================================
    # insideGroupNodes = [node for node in errors if node.Class() == "Group"]
    # for group in insideGroupNodes:
    # 	for node in group.nodes():
    # 		print node.name()
    # 		if node.error() == True:
    # 			for n in range(node.getNumKnobs()):
    # 				if node.knob(n).name() == "file" or node.knob(n).name() == "vfield_file":
    # 					nodes.append(node)
    # ===========================================================================
    # ===========================================================================
    # write parameter will define if write nodes should be changed or not
    # ===========================================================================
    if not write:
        nodes = [node for node in nodes if node.Class() != "Write"]

    if len(nodes) == 0:
        finalmessage = "You don't have any nodes with read file errors!"
    else:
        if suggestedPath == None:  # no suggestion, so ask for it to the user
            basePath = nuke.getFilename('Select Directory to Search assets', " ", type='open')
        else:
            basePath = suggestedPath

        if basePath != None:
            path = os.path.join(basePath)
        else:
            return

        task = nuke.ProgressTask('Searching files in path\n' + str(path))
        nodecount = 0

        # =======================================================================
        # generate a list with masked search names
        # =======================================================================
        nodefilenames = []

        for node in nodes:
            findFile = ""
            try:
                oldpath = node['file'].value()
            except:
                oldpath = node['vfield_file'].value()

            oldfilename = os.path.basename(oldpath)
            # ===================================================================
            # changing this to fit extendsions with different sizes
            # fileExt = oldfilename[-3:]
            # fileName = oldfilename[:-4]
            # ===================================================================
            fileExt = oldfilename.split(".")[-1]
            fileName = oldfilename[:((-1 * len(fileExt)) - 1)]
            if fileName.find("%") != -1:
                fileName = fileName[:fileName.find("%") + 1]
                newfindname = fileName.replace("%", "*")
            else:
                newfindname = fileName
            findFile = newfindname + "." + fileExt
            nodefilenames.append([node, findFile])

        for r, d, f in os.walk(path):
            cancelwalk = False
            # ===============================================================
            # user can Cancel the task if its taking too long
            # ===============================================================
            if task.isCancelled():
                cancel = True
                break
            if cancel:
                break
            if len(nodefilenames) == 0:
                break

            # ===============================================================================
            # simple string formatting for progress window
            # ===============================================================================
            if len(r) > 20:
                rstring = r[:20] + "..." + r[-20:]
            else:
                rstring = r
            # ===============================================================================
            task.setMessage('Searching ' + rstring)
            subpath = r
            for file in os.listdir(subpath):
                # ===============================================================
                # user can Cancel the task if its taking too long
                # ===============================================================
                if task.isCancelled():
                    cancel = True
                    break
                if cancel:
                    break
                # ===============================================================
                collection = []
                for findFile in nodefilenames:
                    if fnmatch.fnmatch(file, findFile[1]):
                        collection.append(findFile)

                if len(collection) > 0:
                    for findFile in collection:
                        reformatPath = subpath.replace("\\", "/")
                        try:
                            oldpath = findFile[0]['file'].value()
                        except:
                            oldpath = findFile[0]['vfield_file'].value()

                        oldfilename = os.path.basename(oldpath)
                        try:
                            findFile[0]['file'].setValue(reformatPath + '/' + oldfilename)
                        except:
                            findFile[0]['vfield_file'].setValue(reformatPath + '/' + oldfilename)
                        finalmessage = findFile[0].name() + " - " + " Found Successfully!\n" + finalmessage
                        nodefilenames.remove(findFile)
                        nodecount += 1

            task.setProgress(int(float(nodecount) / len(nodes) * 100))

        if len(nodefilenames) > 0:
            for node in nodefilenames:
                finalmessage = node[0].name() + " - " + " Not Found!\n" + finalmessage

    print("Time elapsed:", time.time() - start_time, "seconds")
    nuke.message(finalmessage)


def main():
    bvfx_findPath(False)
