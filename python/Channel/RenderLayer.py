import nuke

def RenderLayer():
    RenderLayernode = nuke.nodes.NoOp(name='RenderLayer')
    knob_tk = nuke.Tab_Knob('User', 'RenderLayer')
    RenderLayernode.addKnob(knob_tk)

    knob_fk = nuke.File_Knob('filename', 'FileName')
    RenderLayernode.addKnob(knob_fk)

    knob_pk = nuke.Pulldown_Knob('choosefiletype', 'chooseFileType')

    knob_ek1 = nuke.Enumeration_Knob('filetype', 'FileType', ['tiff', 'targa', 'jpeg', 'png'])

    RenderLayernode.addKnob(knob_pk)
    RenderLayernode.addKnob(knob_ek1)

    # tiff
    knob_ek_tiff1 = nuke.Enumeration_Knob('datatypetiff', 'DataType', ['8 bit', '16 bit', '32 bit float'])
    knob_ek_tiff2 = nuke.Enumeration_Knob('compressiontiff', 'Compression', ['none', 'PackBits', 'LZW', 'Deflate'])
    RenderLayernode.addKnob(knob_ek_tiff1)
    RenderLayernode.addKnob(knob_ek_tiff2)
    knob_ek_tiff1.setVisible(False)
    knob_ek_tiff2.setVisible(False)
    # tga
    knob_ek_tga = nuke.Enumeration_Knob('compressiontga', 'Compression', ['none', 'RLE'])
    RenderLayernode.addKnob(knob_ek_tga)
    knob_ek_tga.setVisible(False)
    # jpeg
    knob_dk_jpeg1 = nuke.Double_Knob('jpeg_quality', 'quality')
    knob_dk_jpeg1.setValue(1)
    knob_ek_jpeg2 = nuke.Enumeration_Knob('jpeg_sub_sampling', 'sub-sampling', ['4:1:1', '4:2:2', '4:4:4'])
    RenderLayernode.addKnob(knob_dk_jpeg1)
    RenderLayernode.addKnob(knob_ek_jpeg2)
    knob_dk_jpeg1.setVisible(False)
    knob_ek_jpeg2.setVisible(False)
    # png
    knob_ek_png = nuke.Enumeration_Knob('datatypepng', 'DataType', ['8 bit', '16 bit'])
    RenderLayernode.addKnob(knob_ek_png)
    knob_ek_png.setVisible(False)

    knob_pk.setValues({
                          'chosefiletype/tiff': 'nuke.thisNode().knob("filetype").setValue("tiff");nuke.thisNode().knob("datatypetiff").setVisible(True);nuke.thisNode().knob("compressiontiff").setVisible(True);nuke.thisNode().knob("compressiontga").setVisible(False);nuke.thisNode().knob("jpeg_quality").setVisible(False);nuke.thisNode().knob("jpeg_sub_sampling").setVisible(False);nuke.thisNode().knob("datatypepng").setVisible(False)',

                          'targa': 'nuke.thisNode().knob("filetype").setValue("targa");nuke.thisNode().knob("datatypetiff").setVisible(False);nuke.thisNode().knob("compressiontiff").setVisible(False);nuke.thisNode().knob("compressiontga").setVisible(True);nuke.thisNode().knob("jpeg_quality").setVisible(False);nuke.thisNode().knob("jpeg_sub_sampling").setVisible(False);nuke.thisNode().knob("datatypepng").setVisible(False)',

                          'jpeg': 'nuke.thisNode().knob("filetype").setValue("jpeg");nuke.thisNode().knob("datatypetiff").setVisible(False);nuke.thisNode().knob("compressiontiff").setVisible(False);nuke.thisNode().knob("compressiontga").setVisible(False);nuke.thisNode().knob("jpeg_quality").setVisible(True);nuke.thisNode().knob("jpeg_sub_sampling").setVisible(True);nuke.thisNode().knob("datatypepng").setVisible(False) ',

                          'png': 'nuke.thisNode().knob("filetype").setValue("png");nuke.thisNode().knob("datatypetiff").setVisible(False);nuke.thisNode().knob("compressiontiff").setVisible(False);nuke.thisNode().knob("compressiontga").setVisible(False);nuke.thisNode().knob("jpeg_quality").setVisible(False);nuke.thisNode().knob("jpeg_sub_sampling").setVisible(False);nuke.thisNode().knob("datatypepng").setVisible(True)'})

    knob_line = nuke.Text_Knob('')
    RenderLayernode.addKnob(knob_line)

    knob_py = nuke.PyScript_Knob('createwrite', 'CreateWrite')
    RenderLayernode.addKnob(knob_py)

    knob_py.setCommand("""
                        layerlist = nuke.layers(nuke.thisNode())
                        print layerlist
                        for i in layerlist:
                            if i == 'rgb':
                                print i
                                pass
                            else:
                                node = nuke.nodes.Shuffle()
                                node.setInput(0,nuke.thisNode())
                                node.knob('in').setValue(i)
                                node.knob('name').setValue(i)
                                node.knob('postage_stamp').setValue(1)
                                node.knob('note_font_size').setValue(16)
                                filename = nuke.thisNode().knob('filename').value() + i + '.####.' + nuke.thisNode().knob('filetype').value()
                                write = nuke.nodes.Write()
                                write.setInput(0,node)
                                write.knob('file').setValue(filename)
                                write.knob('file_type').setValue(nuke.thisNode().knob('filetype').value())
                                if nuke.thisNode().knob('filetype').value() == 'tiff':
                                    write.knob('datatype').setValue(nuke.thisNode().knob('datatypetiff').value())
                                    write.knob('compression').setValue(nuke.thisNode().knob('compressiontiff').value())
                                elif nuke.thisNode().knob('filetype').value() == 'targa':
                                    write.knob('compression').setValue(nuke.thisNode().knob('compressiontga').value())
                                elif nuke.thisNode().knob('filetype').value() == 'jpeg':
                                    write.knob('_jpeg_quality').setValue(nuke.thisNode().knob('jpeg_quality').value())
                                    write.knob('_jpeg_sub_sampling').setValue(nuke.thisNode().knob('jpeg_sub_sampling').value())
                                else:
                                    write.knob('datatype').setValue(nuke.thisNode().knob('datatypepng').value())
                                write.knob('beforeRender').setValue('''
                        if os.path.exists(os.path.dirname(nuke.thisNode().knob('file').value()))==True:
                            print nuke.thisNode().knob('file').value()
                        else:
                            os.makedirs(os.path.dirname(nuke.thisNode().knob('file').value()))''')
                                write.knob('afterRender').setValue('''

                        inputx = nuke.thisNode()['xpos'].value()
                        inputy = nuke.thisNode()['ypos'].value()
                        filelist = nuke.getFileNameList(os.path.dirname(nuke.thisNode().knob('file').value()))
                        writename = os.path.basename(nuke.thisNode().knob('file').value())

                        for file in filelist:
                            #print file
                            if file.find('.db') < 0:
                                if file.find(' ') > 0 and file.find('-') > 0:
                                    filename = file.split(' ')[0]
                                    if filename.find('#') > 0:
                                        number = filename.count('#')
                                        place = filename.find('#')
                                        oldstr = filename[place:place + number]
                                        filename = filename.replace(oldstr,'%0'+ str(number) + 'd')
                                        print filename
                                    if filename == writename:
                                        firstframe=file.split(' ')[-1].split("-")[0]
                                        lastframe=file.split(' ')[-1].split("-")[1]
                                        newnode = nuke.nodes.Read(file=os.path.dirname(nuke.thisNode().knob('file').value()) + '/' + writename,first=firstframe,last=lastframe,)
                                        newnode.setXYpos(int(inputx),int(inputy)+50)
                                    else:
                                        pass
                                else:
                                    filename = file
                                    if filename == writename:
                                        firstframe=filename.split('.')[-2]
                                        lastframe=filename.split('.')[-2]
                                        newnode = nuke.nodes.Read(file=os.path.dirname(nuke.thisNode().knob('file').value()) + '/' + writename,first=firstframe,last=lastframe,)
                                        newnode.setXYpos(int(inputx),int(inputy)+50)
                            else:
                                pass


                        ''')
                        """
                       )

    knob_doc = nuke.PyScript_Knob('document', 'HelpDocument')
    RenderLayernode.addKnob(knob_doc)

    knob_doc.setCommand("""nuke.message('''USE STEP
                            1.connect this node to Read node
                            2.set  up your render path at the FileName
                            3.choose render file Type
                            4.choose the  sub setting
                            5.click createwrite button
                            ''')
                            """
                        )
