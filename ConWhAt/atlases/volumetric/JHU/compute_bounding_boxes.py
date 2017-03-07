
import numpy as np
import pandas as pd
from nilearn.image import index_img
import nibabel as nib


import sys
sys.path.append('/home/jgriffiths/Code/libraries_of_mine/github/ConWhAt')
import ConWhAt

from ConWhAt.volumetric.utils import get_bounding_box_inds,read_igzip_slice


info = [['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']]

df_mappings = pd.read_csv('mappings.txt')

for i in df_mappings.index:
  nii_file = df_mappings.ix[i]['nii_file']
  vol = df_mappings.ix[i]['4dvolind']
  name = df_mappings.ix[i]['name']

  print 'reading data for %s' % name
  
  dat = read_igzip_slice(nii_file,vol)

  res = get_bounding_box_inds(dat)
    
  (xmin,xmax),(ymin,ymax),(zmin,zmax) = res # get_bounding_box_inds(dat)

  info.append([xmin,xmax,ymin,ymax,zmin,zmax])


df_info= pd.DataFrame(info)
df_info = df_info.T.set_index([0]).T

df_info.to_csv('bounding_boxes.txt', sep=',',index=False)

