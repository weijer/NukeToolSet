# -*- coding：utf-8 -*-
# __author__ = "heshuai"
# description="""  """


import nuke 
import os
import re


def get_frames(folder):
    all_frames = os.listdir(folder)
    if 'Thumb.db' in all_frames:
        all_frames.remove('Thumb.db')
    all_frames = [frame for frame in all_frames if os.path.isfile(os.path.join(folder, frame))]
    if len(all_frames) > 1:
        return all_frames


def get_frame_range(all_frames):
    pattern_frame = r'.*\.(\d{4})\.[a-z]+$'
    frame_numbers = [int(re.match(pattern_frame, frame).group(1))
                     for frame in all_frames
                     if re.match(pattern_frame, frame)]
    if frame_numbers:
        start_frame, end_frame = [min(frame_numbers), max(frame_numbers)]
        if end_frame > start_frame:
            return start_frame, end_frame
            
            
def rebuild_read_node(read_node, start_frame, end_frame):
    read_node['first'].setValue(start_frame)
    read_node['last'].setValue(end_frame)
    read_node['origfirst'].setValue(start_frame)
    read_node['origlast'].setValue(end_frame)
            

def main():
    for read_node in nuke.allNodes('Read'):
        file_name = read_node['file'].getValue().replace('\\', '/')
        folder = os.path.dirname(file_name)
        all_frames = get_frames(folder)
        if all_frames: 
            replaced_frame = re.sub(r'\.\d{4}', '.%04d', all_frames[0])
            frame_ext = os.path.join(folder, replaced_frame)
            frame_ext = frame_ext.replace('\\', '/')
            if file_name == frame_ext:
                continue
            read_node['file'].setValue(frame_ext)
            frames = get_frame_range(all_frames)
            if frames:
                start_frame, end_frame = frames
                rebuild_read_node(read_node, start_frame, end_frame)