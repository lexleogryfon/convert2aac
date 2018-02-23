#!/usr/bin/env nix-shell
#!nix-shell -p python35 -i python3.5

'''
made in wingIde 6 pro
lex(c)
'''



from pathlib import Path
from types import MappingProxyType
import sys, subprocess, os, shutil


def scan(path_string, ext_dict_param={}):
    '''
    returns read-only dictionary where key is '.extension' and value a tuple(of path objectes)
    '''
    
    ext_dict = ext_dict_param
    p = Path(path_string)
    for child in p.iterdir():
       
        if child.is_dir():
            scan(child, ext_dict_param=ext_dict)
        else:
            extension = child.suffix.lower()
            if extension in ext_dict.keys():
                #print(type(ext_dict[extension]), ext_dict[extension], ext_dict)
                ext_dict[extension] +=  (child, )
            else:
                #print(type(child), child, dir(child))
                ext_dict[extension] = (child, )

    return MappingProxyType(ext_dict)


def convert_file(input_file, output_prefix_folder):
    '''
    accept pathlib.Path objects as parameters
    '''

    devnull = open('/dev/null', 'w')
    output_prefix_folder = './' / output_prefix_folder / str(input_file.parent)[1:]
    # print('new files will be saved in ', output_prefix_folder)
    
    output_prefix_folder.mkdir(exist_ok=True, parents=True)
    output_file_name = str(input_file.stem) + '.m4a'
    output_file_path = output_prefix_folder / output_file_name
    #spawn non blocking async background process
    p = subprocess.Popen(['/home/lex/.nix-profile/bin/ffmpeg', '-threads', '1', '-i', str(input_file), '-vn',   '-c:a', 'libfdk_aac', '-profile:a', 'aac_he_v2', '-b:a', '32k', '-y', str(output_file_path)], stdout=devnull, stderr=devnull)

    # blocking wait until completion, to get exit code
    #while p.poll() is None:
        #import time
        #time.sleep(0.1)
    #print(p.poll())
#    if p.returncode != 0: raise CalledProcessError(input_file, p, p.returncode )    


def copy_file(input_file, output_prefix_folder):
    '''
    accept pathlib.Path objects as parameters
    '''
    output_prefix_folder = './' / output_prefix_folder / str(input_file.parent)[1:]
    # print('new files will be saved in ', output_prefix_folder)
    
    output_prefix_folder.mkdir(exist_ok=True, parents=True)
    #copy_file
    shutil.copy2(src=str(input_file), dst=str(output_prefix_folder))



def main(argv):
    files = scan(argv[1])
    #print extensions sorted by number of files
    for ext, count in sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  files.items()], 
                              key=lambda tpl: tpl[1], 
                              reverse=True): 
        print('{count} {ext} files'.format(ext=ext, count=count))



    # single file conversion example
    #i_f = Path('/home/lex/Desktop/mystuff/pc/media/media/music/Dubstep/Bjork - Pagan Poetry (Ripperton rmx).mp3')
    #o_p_f = Path('./subfolder/')
    #convert_file(input_file=i_f, output_prefix_folder=o_p_f)

    ALLOWED_EXTENSIONS = ('.mp3',)
    o_p_f = Path('./subfolder/')
    
    for key,values in files.items():
        print('key: ', key)
        for item in values:
            print(item)
            if key in ALLOWED_EXTENSIONS:
                convert_file(input_file=item, output_prefix_folder=o_p_f)
            else:
                copy_file(input_file=item, output_prefix_folder=o_p_f)
    

    #DONE store list of filenames, paths in ext_dict, along with extension number occurence ; we may not really count number of extension occurence, but just count a length of file list with particular extension
    #DONE return immutable value in scan()
    #DONE convert singe file
    #DONE convert singe file and write it in relative path inside multiple directories

    #DONE implement blocking loop, and covert file after file
    #TODO add logging for python app itself, for ffmpeg & if ffmpeg exit code != 0
    #DONE allow conversion only by specific extension
    #DONE copy non convertable files
    #TODO convert multiple files at same time    
    #TODO add argparse CLI parameters





if __name__ == "__main__":
    main(sys.argv)

