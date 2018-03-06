#!/usr/bin/env nix-shell
#!nix-shell -p python35 python35Packages.psutil -i python3.5

'''
made in wingIde 6 pro
lex(c)
'''



from pathlib import Path
from types import MappingProxyType
import sys, subprocess, os, shutil, argparse, time, logging, re, copy
import psutil
#from threading  import Thread






class My_Event_loop_queue:

    def __init__(self):
        self.pool = []
        self.wlog = logging.getLogger('warning_logger')
        self.dlog = logging.getLogger('debug_logger')

    def append(self, job):
        '''
        appends task to pool & give up control to main program
        doesn't block until 6 tasks in pool
        block if 6 tasks running in pool, wait until at least 1 completed, then remove it from pool and give back control to main program (e.g. for copy files and other stuff)
        '''
        if len(self.pool) < 9:
            self.pool.append(job)
        self.run_loop(until=8)
                    
    def run_until_completion(self):
        self.run_loop(until=1)
       

    def run_loop(self, until):
        
        while len(self.pool) >= until:
            for task in self.pool:
                if task.poll() is None:
                    time.sleep(0.1)
                    #work around ffmpeg bug, when ffmpeg process hang out
                    #check for [mp3 @ 0x14aaa20] overread, skip -4 enddists: -1 -1
                    if os.getloadavg()[0] < 3:
                        #print(os.getloadavg()[0])
                        #outs, errs = task.communicate() #BUG sets exitcode to 0, blocking
                        pattern = re.compile(r"^.*mp3.*overread.*skip.*enddists.*$",  re.MULTILINE)
                        # print(type(errs), type(outs))
                        while True:
                            # outline = task.stdout.readline()
                            errline = task.stderr.readline()
                            #if not outline:
                                #break
                            if not errline:
                                break                             
                            #if re.search(pattern, outline) or re.search(pattern, errline):
                            if re.search(pattern, errline):
                                #task.poll()
                                #print("match")
                                task.kill()
                                task.poll()
                                #logging.debug(
                                    #msg='ffmpeg output found to contain "^.*mp3.*overread.*skip.*enddists.*$" errors, to prevent process from infinite loop we killing it {}'.format(
                                #str(task.returncode) + ' ' + str(task.pid) + ' '.join(task.args) + '\n'))
                                self.wlog.warning(
                                    msg="""ffmpeg output found to contain "mp3 overread" errors, to prevent process from infinite loop we killing it for file {} """.format(task.input_file))                                
                                break
                            #else:
                                #break
                            
                           

                                
                elif task.returncode is 0:
                    self.pool.remove(task)
                else:
                    #log exit code of task with task args                
                    outs, errs = task.communicate()
                    err = 'task: ' + ' '.join(task.args) + '\n returncode: ' + str(task.returncode) +  '\n stdout: ' + outs + '\n stderr: ' + errs
                    self.dlog.debug(msg=err)
                    
                    self.wlog.error(msg= 'ffmpeg failed to convert {} , file will be copied'.format(task.input_file))
                    
                    #copy file in case it can't be converted by ffmpeg
                    copy_file(input_file=task.input_file, output_prefix_folder=task.output_prefix_folder_original)
                    #shutil.copy2(src=str(task.input_file), dst=str(task.output_prefix_folder))
                    #remove invalid file
                    if task.output_file_path.exists(): os.remove(str(task.output_file_path))
                    #remove task from pool
                    self.pool.remove(task)




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
    output_prefix_folder_original = copy.deepcopy(output_prefix_folder)
    output_prefix_folder = './' / output_prefix_folder / str(input_file.parent)[1:]
    # print('new files will be saved in ', output_prefix_folder)
    
    output_prefix_folder.mkdir(exist_ok=True, parents=True)
    output_file_name = str(input_file.stem) + '.m4a'
    output_file_path = output_prefix_folder / output_file_name
    #spawn non blocking async background process
    p = subprocess.Popen(['/home/lex/.nix-profile/bin/ffmpeg', '-threads', '1', '-i', str(input_file), '-vn',   '-c:a', 'libfdk_aac', '-profile:a', 'aac_he_v2', '-b:a', '32k', '-y', '-nostdin', str(output_file_path)], universal_newlines=True, stdout=subprocess.PIPE , stderr=subprocess.PIPE)

    # blocking wait until completion, to get exit code
    #while p.poll() is None:
        #import time
        #time.sleep(0.1)
    #print(p.poll())
#    if p.returncode != 0: raise CalledProcessError(input_file, p, p.returncode )
    p.input_file = input_file
    p.output_prefix_folder_original = output_prefix_folder_original
    p.output_prefix_folder = output_prefix_folder
    p.output_file_path = output_file_path
    return p

def copy_file(input_file, output_prefix_folder):
    '''
    accept pathlib.Path objects as parameters
    '''
    output_prefix_folder = './' / output_prefix_folder / str(input_file.parent)[1:]
    # print('new files will be saved in ', output_prefix_folder)
    
    output_prefix_folder.mkdir(exist_ok=True, parents=True)
    #copy_file
    shutil.copy2(src=str(input_file), dst=str(output_prefix_folder), follow_symlinks=False)






def setup_logger(name, log_file, formatter, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger



def main(argv):
    global pool
    
    if len(argv) is 1:
        argv.append("-h")   
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scan", help="show extensions sorted by number of files")
    parser.add_argument("-i", "--input", help="input folder")
    parser.add_argument("-o", "--output", help="output folder")
    arguments = parser.parse_args()
    
    #logging.basicConfig(filename='debug_convert.log', level=logging.DEBUG, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #logging.basicConfig(filename='minimal_convert.log', level=logging.WARNING, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    dlog = setup_logger('debug_logger', 'debug_convert.log', level=logging.DEBUG, formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # second file logger
    wlog = setup_logger('warning_logger', 'warning_convert.log', level=logging.WARNING, formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


    
    if arguments.scan:
        

        files = scan(arguments.scan)
        #print extensions sorted by number of files
        for ext, count in sorted( [(extension, len(tuple_of_files)) for extension, tuple_of_files in  files.items()], 
                              key=lambda tpl: tpl[1], 
                              reverse=True):
            print('{count} {ext} files'.format(ext=ext, count=count))



    # single file conversion example
    #i_f = Path('/home/lex/Desktop/mystuff/pc/media/media/music/Dubstep/Bjork - Pagan Poetry (Ripperton rmx).mp3')
    #o_p_f = Path('./subfolder/')
    #convert_file(input_file=i_f, output_prefix_folder=o_p_f)

    if arguments.input and arguments.output:
        
        
        ALLOWED_EXTENSIONS = ('.mp3','.wav','.ogg', '.wma','.flac')
        files = scan(arguments.input)
        o_p_f = Path(arguments.output)
        evloop = My_Event_loop_queue()
        dlog.info('conversion started')
        
    
        for key,values in files.items():
            #print('key: ', key)
            for item in values:
                # print(item)
                if key in ALLOWED_EXTENSIONS:
                    evloop.append( convert_file(input_file=item, output_prefix_folder=o_p_f) )
                else:
                    copy_file(input_file=item, output_prefix_folder=o_p_f)

        #wait until pool exhaust of tasks
        evloop.run_until_completion()
        print('conversion is done')
        dlog.info('conversion is done')
        

    #DONE store list of filenames, paths in ext_dict, along with extension number occurence ; we may not really count number of extension occurence, but just count a length of file list with particular extension
    #DONE return immutable value in scan()
    #DONE convert singe file
    #DONE convert singe file and write it in relative path inside multiple directories
    #DONE implement blocking loop, and covert file after file
    #DONE convert multiple files at same time    
    #DONE allow conversion only by specific extension
    #DONE copy non convertable files

    #DONE add argparse CLI parameters
    #DONE add logging for python app itself, for ffmpeg & if ffmpeg exit code != 0
    #DONE FIX copy symlinks, don't follow them
    #DONE ffmpeg non-interactive -nostdin
    #DONE better log output
    #catch all errors, log them and attempt to continue on next file
    
    #print verbose stats output in the end, like timing, number of errors, files copied, files converted, saved space 
    #implement pause and continue, save file? remember progress
    #use async subprocess, async pipes, | threads, multiprocessing
    #throw exceptions from ffmpeg class
    #reStructed text docstrings
    #readme.md
    #flymake check


if __name__ == "__main__":
    main(sys.argv)

