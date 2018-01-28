#!/bin/env python
from pathlib import Path
from os import path as ospath

### variables
exts = set()    
ext_dict = {}
out='.'

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



            


def main():
    scan(out)
    #print(exts)
    #print(ext_dict)
    #for key,value in ext_dict.items(): print(value, key)
    s = [(key, ext_dict[key]) for key in sorted(ext_dict, ext_dict.get, reverse=True)]
    for ext, count in s: print('{count} {ext} files'.format(ext=ext, count=count))

    #TODO convert singe file
    #TODO convert singe file and write it in relative path inside multiple directories
    #TODO implement blocking loop, and covert file after file
    #TODO allow conversion only by specific extension
    #TODO convert multiple files at same time

main()


