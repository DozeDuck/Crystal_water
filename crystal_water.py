import subprocess
import os
import sys
import getopt


args=sys.argv[1:]
input_receptor =''
percentage = ''
cores = ''
input_ntrys = ''
input_Replicas = ''
cyclization = ''
reference = ''

# user input transfer chain: -i arg -> getopt -> "input_receptor = arg" -> "prepare = TOPOLfile(input_receptor)" -> "def __init__(self, pdbfilename)" -> "self.pdbfile = pdbfilename" -> "def prepare_input(self)"
try:
   opts, args = getopt.getopt(args,"h:i:",["help","input_receptor ="])
except getopt.GetoptError:
   print ('crystal_water.py -i <inputfile> -o <outputfile> # notice: the crystal water in pdb file must looks like this "O   HOH"')
   sys.exit(2)
 
for opt, arg in opts:
   if opt == '-h':
      print ('crystal_water.py -i <inputfile> -o <outputfile>')
      sys.exit()
   elif opt in ("-i", "--input_seq"):
      input_receptor = arg

class TOPOLfile:
    pdbfile = "none"
    
    def __init__(self, pdbfilename):
        self.pdbfile = pdbfilename
        
    def prepare_input(self):    
        # os.system(r'sed -i "s/O   HOH/OW  FWA/g" %s' % (input_receptor))
        a,b = subprocess.getstatusoutput(['sed -i "s/O   HOH/OW  FWA/g" ' + self.pdbfile])
        
        # a,b=subprocess.getstatusoutput(['cat topol.top'])
        # myoutput = open(path_to_output_file,'w+')
        # a=subprocess.Popen(['ls'],stdout=myoutput).communicate
        
        a,b = subprocess.getstatusoutput(['which gmx'])
        a = b.split('/')
        # print(a[1:-2])  # grab the PATH for gromacshome  ['home', 'dozeduck', 'workspace', 'gromacs', 'gmx20205']
        
        linker="/"
        GROMACSHOME=linker.join(a[1:-2])
        
        os.system('cp -r /' + GROMACSHOME+'/share/gromacs/top/amber99sb-ildn.ff ./amber99sb-ildn-crystalwater.ff')   # copy and paste amber99sb-ildn.ff to current folder
        
        
        aminoacids_rtp=['; crystal_water','[ FWA ]',' [ atoms ]','    OW   OW           -0.834    0','   HW1   HW            0.417    0','   HW2   HW            0.417    0',' [ bonds ]','    OW   HW1','    OW   HW2']
        with open('amber99sb-ildn-crystalwater.ff/aminoacids.rtp', mode = 'a') as rtp:
             for i in range(len(aminoacids_rtp)):
                     rtp.write(aminoacids_rtp[i])
                     rtp.write('\n')
        
        aminoacid_hdb = ['FWA     1', '2       7       HW      OW']
        with open('amber99sb-ildn-crystalwater.ff/aminoacids.hdb', mode = 'a') as hdb:
            for i in range(len(aminoacid_hdb)): 
                hdb.write(aminoacid_hdb[i])
                hdb.write('\n')
             
        residue_type = ['FWA     Ion']
        a,last_line_of_residuetype = subprocess.getstatusoutput(['tail -1 /' + GROMACSHOME + '/share/gromacs/top/residuetypes.dat'])
        # print(last_line_of_residuetype)
        if(last_line_of_residuetype.split()[0] != "FWA"):
            # print(last_line_of_residuetype.split()[0])
            with open('/'+GROMACSHOME+'/share/gromacs/top/residuetypes.dat', mode = 'a') as restype:
                restype.write(residue_type[0])
                restype.write('\n')
        os.system('printf "1\n 1\n" | gmx pdb2gmx -f ' + self.pdbfile + ' -o rec.gro -ignh -merge all')
            
        


prepare = TOPOLfile(input_receptor)
prepare.prepare_input()
