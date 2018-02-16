#!/usr/bin/env nix-shell
#!nix-shell -p python35 -i python3.5

import sys
from pathlib import Path
from os import path as ospath
from types import MappingProxyType

### variables
#exts = set()    
#ext_dict = {}
#input=''

def scan(path_string):
    p = Path(path_string)
    for child in p.iterdir():
       
        if child.is_dir():
            scan(child)
        else:
            
            # file = str(child)
            # extension = ospath.splitext(file)[-1].lower()
            extension = child.suffix.lower()
            # exts.add(extension)
            if extension in ext_dict.keys():
                ext_dict[extension] = ext_dict[extension] +1          
            else:
                ext_dict[extension] = 1


def scanv2(path_string, ext_dict_param={}):
    '''
    returns read-only dictionary where key is '.extension' and value a tuple(of path objectes)
    '''
    ext_dict = ext_dict_param
    p = Path(path_string)
    for child in p.iterdir():
       
        if child.is_dir():
            scanv2(child, ext_dict_param=ext_dict)
        else:
            
            # file = str(child)
            # extension = ospath.splitext(file)[-1].lower()
            extension = child.suffix.lower()
            # exts.add(extension)
            if extension in ext_dict.keys():
                #print(type(ext_dict[extension]), ext_dict[extension], ext_dict)
                ext_dict[extension] +=  (child, )
            else:
                #print(type(child), child, dir(child))
                ext_dict[extension] = (child, )

    return MappingProxyType(ext_dict)
    #return ext_dict


def main(argv):
    # scan(input)
    ext_dict = scanv2(argv[1])
   
    #block v1
    #print extensions sorted by number of files
    #var = []
    #for extension, tuple_of_files in ext_dict.items():
        #var.append((extension, len(tuple_of_files),))
    ##^equals var = [(extension, len(tuple_of_files)) for extension, tuple_of_files in  ext_dict.items()]
    #s = sorted(var, key=lambda tpl: tpl[1], reverse=True)
    #for ext, count in s:
        #print('{count} {ext} files'.format(ext=ext, count=count))
    
    #block v2
    #print extensions sorted by number of files
    for ext, count in sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  ext_dict.items()], 
                              key=lambda tpl: tpl[1], 
                              reverse=True): 
        print('{count} {ext} files'.format(ext=ext, count=count))
    
  
# old code 
#    s = [(key, ext_dict[key]) for key in sorted(ext_dict, key=ext_dict.get, reverse=True)]
#    for ext, count in s: print('{count} {ext} files'.format(ext=ext, count=count))

    #DONE store list of filenames, paths in ext_dict, along with extension number occurence ; we may not really count number of extension occurence, but just count a length of file list with particular extension
    #DONE return immutable value in scan()
    #TODO convert singe file
    #TODO convert singe file and write it in relative path inside multiple directories
    #TODO implement blocking loop, and covert file after file
    #TODO allow conversion only by specific extension
    #TODO convert multiple files at same time




if __name__ == "__main__":
    main(sys.argv)

