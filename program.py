#!/usr/bin/env nix-shell
#!nix-shell -p python35 -i python3.5

import sys, subprocess, os
from pathlib import Path
#from os import path as ospath
from types import MappingProxyType


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
    #call ffmpeg cli
#    os.chdir("/home/lex/Desktop/mystuff/pc/media/media/music/Dubstep")
    # output = subprocess.check_output('ffmpeg -i Bjork\ -\ Pagan\ Poetry\ \(Ripperton\ rmx\).mp3 -vn -c:a libfdk_aac -profile:a aac_he_v2 -b:a 32k -y output2.m4a', shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    # print(output)
    #subprocess.Popen(['pwd'])
    #subprocess.Popen(['ls', '-la'])
    devnull = open('/dev/null', 'w')
    print("BEFORE")
    print(output_prefix_folder)
    output_prefix_folder = './' / output_prefix_folder / str(input_file.parent)[1:]
    print(output_prefix_folder)
    
    output_prefix_folder.mkdir(exist_ok=True, parents=True)
    output_file_name = str(input_file.stem) + '.m4a'
    output_file_path = output_prefix_folder / output_file_name  
    p = subprocess.Popen(['/home/lex/.nix-profile/bin/ffmpeg', '-threads', '1', '-i', str(input_file), '-vn',   '-c:a', 'libfdk_aac', '-profile:a', 'aac_he_v2', '-b:a', '32k', '-y', str(output_file_path)], stdout=devnull, stderr=devnull)
    print(p, p.returncode, p.poll() )
    print("DO NEW TASK")
    while p.poll() is None:
        import time
        time.sleep(0.1)
    print(p.poll())

def main(argv):
    files = scan(argv[1])
    #v 1 print extensions sorted by number of files
    for ext, count in sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  files.items()], 
                              key=lambda tpl: tpl[1], 
                              reverse=True): 
        print('{count} {ext} files'.format(ext=ext, count=count))

    #v 2 through map #does't work and unnecessary
    #print([*map(lambda ext, count: (ext, count), sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  files.items()], 
                              #key=lambda tpl: tpl[1], 
                              #reverse=True))])
                              
    #v 3 through list comprehension
    #[print('{count} {ext} files'.format(ext=ext, count=count)) for ext, count in sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  files.items()], 
                              #key=lambda tpl: tpl[1], 
                              #reverse=True)]

    i_f = Path('/home/lex/Desktop/mystuff/pc/media/media/music/Dubstep/Bjork - Pagan Poetry (Ripperton rmx).mp3')
    print(i_f.exists())
    #create output folder
    o_p_f = Path('./subfolder/ыги')
    convert_file(input_file=i_f, output_prefix_folder=o_p_f)

    #DONE store list of filenames, paths in ext_dict, along with extension number occurence ; we may not really count number of extension occurence, but just count a length of file list with particular extension
    #DONE return immutable value in scan()
    #TODO add argparse CLI parameters
    #TODO convert singe file
    #TODO convert singe file and write it in relative path inside multiple directories
    #TODO implement blocking loop, and covert file after file
    #TODO allow conversion only by specific extension
    #TODO convert multiple files at same time




if __name__ == "__main__":
    main(sys.argv)

