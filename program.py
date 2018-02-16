#!/usr/bin/env nix-shell
#!nix-shell -p python35 -i python3.5


from pathlib import Path
from os import path as ospath
import sys

### variables
exts = set()    
ext_dict = {}
input=''

def scan(path_string):
    p = Path(path_string)
    for child in p.iterdir():
       
        if child.is_dir():
            scan(child)
        else:
            
            # file = str(child)
            # extension = ospath.splitext(file)[-1].lower()
            extension = child.suffix.lower()


            
            exts.add(extension)
            if extension in ext_dict.keys():
                ext_dict[extension] = ext_dict[extension] +1          
            else:
                ext_dict[extension] = 1



            


def main(argv):
    # scan(input)
    scan(argv[1])
    #print(exts)
    #print(ext_dict)
    # for key,value in ext_dict.items(): print(value, key)
    #print(ext_dict.get('.sample'))
    #print(sorted(ext_dict, key=ext_dict.get, reverse=True))
    s = [(key, ext_dict[key]) for key in sorted(ext_dict, key=ext_dict.get, reverse=True)]
    for ext, count in s: print('{count} {ext} files'.format(ext=ext, count=count))

    #TODO store list of filenames, paths in ext_dict, along with extension number occurence ; we may not really count number of extension occurence, but just count a lenth of file list with particular extension
    #TODO convert singe file
    #TODO convert singe file and write it in relative path inside multiple directories
    #TODO implement blocking loop, and covert file after file
    #TODO allow conversion only by specific extension
    #TODO convert multiple files at same time




if __name__ == "__main__":
    main(sys.argv)

