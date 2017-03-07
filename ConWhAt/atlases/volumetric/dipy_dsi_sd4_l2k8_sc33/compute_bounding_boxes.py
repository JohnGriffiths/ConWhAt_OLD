
import numpy as np
import pandas as pd
from nilearn.image import index_img
import nibabel as nib


import sys
sys.path.append('/home/jgriffiths/Code/libraries_of_mine/github/ConWhAt')
import ConWhAt

from ConWhAt.volumetric.utils import get_bounding_box_inds,read_igzip_slice


fstr = 'vismap_grp_cat_rois_v2_%s_norm.nii.gz'

info = [['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax']]

nrois = 83

for roi1 in range(nrois):
  nii_file = fstr %roi1
  nii_img = nib.load(nii_file)
  
  for roi2 in range(nii_img.shape[3]):


    print 'reading data for roi %s to %s' %(roi1,roi2)
    dat = read_igzip_slice(nii_file,roi2)

    res = get_bounding_box_inds(dat)
    
    (xmin,xmax),(ymin,ymax),(zmin,zmax) = res # get_bounding_box_inds(dat)

    info.append([xmin,xmax,ymin,ymax,zmin,zmax])


df_info= pd.DataFrame(info)
df_info = df_info.T.set_index([0]).T

df_info.to_csv('bounding_boxes.txt', sep=',',index=False)

