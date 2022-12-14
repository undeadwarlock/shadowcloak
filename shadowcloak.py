# /undead_warlock
# GPL3.0-or-foward

from ctypes import *
import secrets
import optparse
import winreg
import os
import re

### READ THE READ.ME PLEASE

##############################################################################
def optparser():
   
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mtd", dest = "mtd", help = "True | False")
    parser.add_option("-r", "--registry", dest= "registry", help = "True | False" )
    parser.add_option("-e", "--extension", dest = "extension_list", help= " .txt ")
    parser.add_option("-d", "--directory", dest = "dir_list", default= None, help = " .txt or None")
    parser.add_option("-s", "--subdirs", dest = "recursive", help = "True | False ")
    parser.add_option("-l", "--loop", dest = "loop", help = "True | False ")
    parser.add_option("-w", "--whitelist", dest = "whitelist", default = None, help = " .txt or None")

    (inputs,args) = parser.parse_args()

    return (inputs.mtd, inputs.registry, inputs.extension_list, inputs.dir_list, inputs.recursive, inputs.loop, inputs.whitelist)
#############################################################################################
def tratamento_argumentos():

  def erro():
    print("Read the documentation or use -h to check available arguments")
    quit()
    return

  args_aceitos1 = ["false", "true"]

  (mtd, registry, extension_list, dir_list, recursive, loop, whitelist) = optparser()
  arg_bool  = [mtd] + [registry] + [recursive] + [loop]

  for arg in arg_bool:
    try: 
        index = arg_bool.index(arg)
        arg_bool[index] = arg_bool[index].lower()
        if arg_bool[index] not in args_aceitos1:
            print(arg)
            erro()
       
    except:
          erro()
     
   
  mtd,registry,recursive,loop = arg_bool
  
  if loop == "true":
    registry = "false"
      
  if registry == "true" and not windll.shell32.IsUserAnAdmin():
       print("[X] If you want to add the file associations to Registry, make sure to run this script with special privileges")
       quit()

  return (mtd, registry, extension_list, dir_list, recursive, loop, whitelist)

#############################################################################################
def confirmar():

    confirmar = windll.user32.MessageBoxA(0, b"Are you Sure ? ", b"Confirm", 4)
    if confirmar != 6:
        quit()

    return
#########################################################################################

def readFile(file, access, readmode):   #readmode 2 -> read()
                                                # 3 -> splitlines()
    if "r" in access:
        with open(file, access) as readfile:
            if readmode == 2:
                content = readfile.read()
            if readmode == 3:
                content = readfile.read().splitlines()

        return content 

    else: 
        return 0
#########################################################################

def extension_lister(extension_list, mtd, loop):

    extensions_old = []
    extensions_new = []
           
    if mtd == "true" and loop == "false":

        extensions_old = readFile(extension_list, "r", 3) 

   
    if mtd == "true" and loop == "true":
      dump = readFile(extension_list, "r", 2)

      extregex       = re.findall(r"((\.\w*):(\.\w*)\|)", dump)
      extensions_old = [ext[1] for ext in extregex]
      extensions_new = [exten[2] for exten in extregex]


    if mtd == "false":
        dump = readFile(extension_list, "r", 2)
        
        extregex       = re.findall(r"((\.\w*):(\.\w*)\|)", dump)
        extensions_old = [exten[2] for exten in extregex]
        extensions_new = [ext[1] for ext in extregex]

        
    return extensions_old, extensions_new
#########################################################
  
def dir_lister(recursive, extension_list, mtd, loop, dir_list=None, whitelist=None):

    extensions      = extension_lister(extension_list, mtd, loop)
    file_list       = []
    filtered_list   = []
    whitelist_files = []


    if dir_list == None:


        for (dirpath, dirnames, filenames) in os.walk("C:\\"):
            file_list += [os.path.join(dirpath, file) for file in filenames]

        for arquivo in file_list:
            for extensao in extensions:
                if extensao in arquivo:
                    filtered_list += [arquivo]

                
    else:
        
        directory_list = readFile(dir_list, "r", 3)
        
        if recursive == "false":
            for j in directory_list:
                for h in os.listdir(j):
                    if os.path.isfile(j + "\\" + h):
                        filtered_list += [j + "\\" + h]

        if recursive == "true":
            for dir in directory_list:
                for (dirpath, dirnames, filenames) in os.walk(dir):
                    file_list += [os.path.join(dirpath, file) for file in filenames]

            for arquivo in file_list:
                for extensao in extensions[0]:
                    if extensao in arquivo:
                        filtered_list += [arquivo]
                

    if whitelist:
        wlist = readFile(whitelist, "r", 3)
        
        for wstring in wlist:
            for filtered_file in filtered_list:
                if wstring in filtered_file:
                    index = filtered_list.index(filtered_file)
                    del filtered_list[index]
 

    return filtered_list

###############################################################################################

def randomFourLenGen():
 alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
 string = str()
 lista_random = []
 while len(lista_random) != 4:
    randomnum = secrets.randbelow(26)
    if randomnum not in lista_random:
      lista_random += [randomnum]
 for num in range(0,4):
    string += alfabeto[lista_random[num]]
 return string
     
#################################################################################################

class Extension:
    def __init__(self, oldexts, newexts = None):
        self.oldexts = oldexts
        self.newexts = list()
        if newexts:
         self.newexts += newexts
        

    def fileExtChanger(self, mtd, registry, loop, files, recursive, extension_list, dir_list, whitelist):
       loop_flag = 1

       while loop_flag:

          if mtd == "true" and loop == "false":
            while len(self.oldexts) != len(self.newexts):
                random_ext = randomFourLenGen()
                try:
                    winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, random_ext, reserved = 0, access = winreg.KEY_READ )
                    continue
                except:
                    random_ext = "." + random_ext
                    self.newexts += [random_ext]

            output_archive = open(randomFourLenGen(), "a")
            for item in self.oldexts:
                indice = self.oldexts.index(item)
                output_archive.write("%s:%s|" %(self.oldexts[indice], self.newexts[indice]) )
            output_archive.close()


          for fullpath_file in files:
             try:
                pre, afterdot = os.path.splitext(fullpath_file)
                oldext_index = self.oldexts.index(afterdot)
                os.rename(fullpath_file, pre + self.newexts[oldext_index] )
             except:
                continue


          if registry == "true":
            for itemlist in self.oldexts:
                oldext_index = self.oldexts.index(itemlist)
                oldext_key   = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, itemlist, reserved=0, access= winreg.KEY_READ)
                winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, self.newexts[oldext_index])
          
                try:
                        regvalue = winreg.EnumValue(oldext_key, 0)[1]
                        winreg.SetValue(winreg.HKEY_CLASSES_ROOT, self.newexts[oldext_index], winreg.REG_SZ, regvalue)
                except:
                    pass


          if loop == "false":
             loop_flag = 0
          else: 
            files = dir_lister(recursive, extension_list, mtd, loop, dir_list, whitelist)

                
#######################################################################

def main():
   (mtd, registry, extension_list, dir_list, recursive, loop, whitelist) = tratamento_argumentos()
   confirmar()

   oldexts, newexts = extension_lister(extension_list, mtd, loop)
   filelist = dir_lister (recursive, extension_list, mtd, loop, dir_list, whitelist)
   MTDExtension = Extension(oldexts, newexts )
   MTDExtension.fileExtChanger(mtd, registry, loop, filelist, recursive, extension_list, dir_list, whitelist)

   return

#######################################################################

if __name__ == "__main__":
   main()