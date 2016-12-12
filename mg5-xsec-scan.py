#!/usr/bin/env python

import sys
import os
import shutil
import csv
import imp
import os, errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occured

ppf = imp.load_source('param_pts_format', '/home/de3u14/lib/projects/2HDM/2HDM_ParameterSpaceScan/gnuplot/param_pts_format.py')

#############
# - Input - #
#############

#input = "../../formatted_dat_mA_200.0_mH_560.0_mHc_500.0_formatted.dat"
input = "../../formatted_dat_mA_200.0_mH_560.0_mHc_500.0_formatted_allowed.dat"

#######################################

#######################################
### --- Import MadGraph modules --- ###
#######################################

# - We will load the following two modules:
#   madevent_interface: launches event generation (among other things)
#   madgraph.various.banner: editing run_card (among other things)

# - Paths to MadGraph - #
# Note: You need to edit this to correspond to the paths in your system!
MG5_rootDir = "/home/de3u14/lib/build/hep/MadGraph/MG5_aMC_v2_4_2"
workDir     = "/scratch/de3u14/2HDM-Zh/MadGraph/samples/2HDMtII/2HDMtII_NLO_gg_zh1_noborn_QCD_MG5_242"

try:
    os.remove( os.path.join(workDir,'RunWeb') ) # - Delete RunWeb
except OSError:
    pass
# - Import MadGraph modules - #
sys.path.append(os.path.join(workDir,'bin','internal'))
import madevent_interface  as ME

sys.path.append( MG5_rootDir )
import madgraph.various.banner as banner_mod      # run_card
import check_param_card as param_card_mod         # param_card
import logging, logging.config, coloring_logging

# - Logging - #
logging.config.fileConfig(os.path.join(workDir, 'bin', 'internal', 'me5_logging.conf'))
logging.root.setLevel(logging.ERROR)
logging.getLogger('madevent').setLevel(logging.ERROR)
#logging.getLogger('madgraph').setLevel(logging.ERROR)

#########################################

# - Output of this script - #
output = "xsec_scan.dat"

###################################################################################

# - Access to MadEvent prompt - #
launch = ME.MadEventCmd(me_dir=workDir)

# - Cards - #
run_card_path   = os.path.join(workDir,  "./Cards/run_card.dat")
param_card_path = os.path.join(workDir,  "./Cards/param_card.dat")
run_card   = banner_mod.RunCard(       run_card_path   ) 
param_card = param_card_mod.ParamCard( param_card_path ) 

# - Define empty lists for holding the results - #
param_pts_list = []
xsec_list      = []
xsec_unc_list  = []
result_list    = []

##################################
### --- Cross section scan --- ###
##################################

# - Start of the for loop for the scan - #
#for cba in numpy.linspace(cba_min, cba_max, cba_bins):
#for  tb in numpy.linspace(tb_min,   tb_max, tb_bins):


# - Turn pythia=OFF
# - Turn delphes=OFF

silentremove(os.path.join(workDir, 'Cards/pythia_card.dat') )
silentremove(os.path.join(workDir, 'Cards/delphes_card.dat'))

#for line in sys.stdin:
#print('sys.stdin:', sys.stdin)

# - Write data to file - #


with open(output, 'w') as f_out:
    with open( input ) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))
        for line in lines:
    #   for line in lines[:2]:
            col = line.split()

            cba     = float(col[ppf.cba_col-1])
            sba     = float(col[ppf.sba_col-1])
            tb      = float(col[ppf.tb_col-1])
            Z4      = float(col[ppf.Z4_col-1])
            Z5      = float(col[ppf.Z5_col-1])
            Z7      = float(col[ppf.Z7_col-1])
            m12     = float(col[ppf.m12_col-1])
            l1      = float(col[ppf.l1_col-1])
            l2      = float(col[ppf.l2_col-1])
            l3      = float(col[ppf.l3_col-1])
            l4      = float(col[ppf.l4_col-1])
            l5      = float(col[ppf.l5_col-1])
            l6      = float(col[ppf.l6_col-1])
            l7      = float(col[ppf.l7_col-1])
            mh      = float(col[ppf.mh_col-1])
            mH      = float(col[ppf.mH_col-1])
            mHc     = float(col[ppf.mHc_col-1])
            mA      = float(col[ppf.mA_col-1])
            Gammah  = float(col[ppf.Gammah_col-1])
            GammaH  = float(col[ppf.GammaH_col-1])
            GammaHc = float(col[ppf.GammaHc_col-1])
            GammaA  = float(col[ppf.GammaA_col-1])

            # - Setting parameters
            param_card['frblock'].param_dict[ (1,)  ].value = tb      # tanbeta
            param_card['frblock'].param_dict[ (2,)  ].value = sba     # sinbmba
            param_card['higgs'].  param_dict[ (1,)  ].value = l2      # l2
            param_card['higgs'].  param_dict[ (2,)  ].value = l3      # l3
            param_card['higgs'].  param_dict[ (3,)  ].value = l7      # lr7
            param_card['mass'].   param_dict[ (35,) ].value = mH      # mh2 = mH
            param_card['mass'].   param_dict[ (36,) ].value = mA      # mh3 = mA
            param_card['mass'].   param_dict[ (37,) ].value = mHc     # mhc = mHc
            param_card['decay'].  param_dict[ (35,) ].value = GammaH  # wh2 = GammaH
            param_card['decay'].  param_dict[ (36,) ].value = GammaA  # wh3 = GammaA
            param_card['decay'].  param_dict[ (37,) ].value = GammaHc # whc = GammaHc

            param_card.write( param_card_path )
        
            # - Start calculation
            launch.run_cmd('generate_events -f')
            print( "Event generation now should be finished." )
            print( "Run name: %s" % launch.run_name )
            
            # - Get results
            xsec     = launch.results.current['cross']
            xsec_unc = launch.results.current['error']
            
            # - Store results in the list
            f_out.write( "{:.3e} {:.3e} {:.3e} {:.3e}\n".format( cba, tb, xsec, xsec_unc) )
            f_out.flush()
       #    param_pts_list.append( (cba, tb) )
       #    xsec_list.     append( xsec     )
       #    xsec_unc_list. append( xsec_unc )

            print( "cba: {:.2f} tb: {:.2f} mA: {:.2f} mH: {:.2f} mHc: {:.2f} xsec: {:.2e} xsec_unc: {:.2e}".format( cba, tb, mA, mH, mHc, xsec, xsec_unc ) )


            ### --- WARNING! --- ###
            # - This command deletes and entire directory tree
            # - Be very cautious with this command
            shutil.rmtree(os.path.join(workDir, 'Events', 'run_01'), ignore_errors=True )
            # - End of for loop - #
 
#    writer.writerows( zip(param_pts_list, xsec_list, xsec_unc_list) )

## - Exit from MadEventCmd - #
launch.run_cmd('quit')
