
import os
import numpy as np
import pandas as pd
import yaml

cfg_file = '../../../../config.yaml'
rl = open(cfg_file, 'r').readlines()
cfg = yaml.load(rl[0])
fsl_data_dir = cfg['fsl_data_dir']

xml_file = fsl_data_dir + '/atlases/JHU-tracts.xml'
nii_file = fsl_data_dir + '/atlases/JHU/JHU-ICBM-tracts-prob-2mm.nii.gz'

rls = open(xml_file, 'r').readlines()
names = [r.split('>')[1].split('<')[0] for r in rls[15:-3]]

mappings = [['name', 'nii_file','nii_file_id','4dvolind']]

for tract_id,tract_name in enumerate(names):

  mappings.append([tract_name,nii_file,0,tract_id])

df_mappings = pd.DataFrame(mappings)
df_mappings = df_mappings.T.set_index([0]).T

df_mappings.to_csv('mappings.txt', sep=',',index=False)


