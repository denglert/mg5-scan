#!/bin/bash

WORKDIR="/scratch/de3u14/2HDM-Zh/ParameterScans/results/Beta_mA_100-700_mHc_500_mH_560_Z7_0.6/mg-scan/test_folder"

module load gcc/6.1.0
source /home/de3u14/lib/build/envs/py27/bin/activate py27

cd ${WORKDIR}
python -V
python mg5-xsec-scan.py
