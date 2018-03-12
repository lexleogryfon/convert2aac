# convert2aac

## What?
CLI audio converter to 32kbps HE v2 AAC, that relies on nixpkgs, ffmpeg, lib_fdk-aac.
+ utilizes multiple CPU cores
+ records error and debug log
+ accepts as input a folder, attempts to convert each file if format supported, otherwise (or if conversion failed for specific file) it will be copied to output directory with respected folder structure (e.g. album,jpg, lyrics.txt)
+ known supported input formats '.mp3', '.wav', '.ogg', '.wma', '.flac', '.ape'


## How?

    Installation:
    Software have self-contained pure nix expression to install correct versions of python, ffmpeg with aac support, dependecies.
    You must have nix-shell in your system in order to evaluate it. 
    
    case 1) you use NixOs 17.09 (tested)
    case 2) you use nix package manager in another distro (untested, but should work in theory)
    
    >git clone https://github.com/lexleogryfon/convert2aac
    
    usage: program.py [-h] [-s SCAN] [-i INPUT] [-o OUTPUT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SCAN, --scan SCAN  show extensions sorted by number of files
      -i INPUT, --input INPUT input folder
      -o OUTPUT, --output OUTPUT
      
      e.g. ./program.py -s "/path/to/folder"
      will output format\extension statistics for folder
      
      ./program.py -i "/home/albums" -o "/home/albums.converted"
      will convert albums to new directory /home/albums.converted with aac content
       



## Why?
- compress music in order to save disk space
- there were no available aac converters in NixOS as of FEB-2018
- current raw ffmpeg (v3.3.4) doesn't ship this way of workflow \ conversion (e.g. with folder copy and retry attempt)
- python > shell script
- HEv2AAC 32kpbs provides acceptable quality for Lo-Fi home\general use in combination with awesome compression rate


> Written with [StackEdit](https://stackedit.io/).
