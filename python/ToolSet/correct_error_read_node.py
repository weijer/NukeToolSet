import nuke
import os
import re


EXTS = ['.mov', '.jpg', '.tga', '.exr', '.jpeg', '.iff', '.tiff']


def get_sequence(folder):
    if os.path.isdir(folder):
        all_frames = [os.path.join(folder, frame).replace('\\', '/')
                     for frame in os.listdir(folder) 
                     if os.path.isfile(os.path.join(folder, frame))]
        try:
            all_frames.remove('Thumb.db')
        except:pass
        return all_frames
        
        
def get_frame_numbers(frame_list):
    frame_numbers = [int(re.findall('\.(\d{4})', frame)[0]) 
                    for frame in frame_list
                    if re.findall('\.(\d{4})', frame)]
    return frame_numbers
        

def set_read_node_frame(node, first, last):
    node['first'].setValue(first)
    node['last'].setValue(last)
    node['origfirst'].setValue(first)
    node['origlast'].setValue(last)


def main():
    for node in nuke.allNodes('Read'):
        file_name = node['file'].getValue()
        
        if os.path.isfile(file_name):
            if os.path.splitext(file_name)[-1] not in EXTS:
                nuke.delete(node)
                
        if '####' in file_name or '%04d' in file_name:
            folder = os.path.dirname(file_name)
            frames = get_sequence(folder)
            frame_numbers = list()
            if frames:
                if '####' in file_name:
                    pattern = re.sub('####', '(\d{4})', file_name)
                else:
                    pattern = re.sub('%04d', '(\d{4})', file_name)
                for frame in frames:
                    if re.match(pattern, frame):
                        frame_number = re.match(pattern, frame).group(1)
                        frame_numbers.append(frame_number)
            if frame_numbers:
                frame_numbers.sort()
                first_frame = int(frame_numbers[0])
                last_frame = int(frame_numbers[-1])
                set_read_node_frame(node, first_frame, last_frame)
            else:
                nuke.delete(node)
                
        if os.path.isdir(file_name):
            for root, dir, files in os.walk(file_name):
                if '.mayaSwatches' not in root:
                    if files:
                        frames = [os.path.join(root, file).replace('\\', '/')
                                  for file in files
                                  if os.path.splitext(file)[-1] in EXTS]
                        if frames:
                            read_node_file = re.sub('\.\d{4}', '.%04d', frames[0])
                            read_node = nuke.nodes.Read(file=read_node_file)
                            frame_numbers = get_frame_numbers(frames)
                            frame_numbers.sort()
                            if frame_numbers:
                                set_read_node_frame(read_node, frame_numbers[0], frame_numbers[1])
            nuke.delete(node)