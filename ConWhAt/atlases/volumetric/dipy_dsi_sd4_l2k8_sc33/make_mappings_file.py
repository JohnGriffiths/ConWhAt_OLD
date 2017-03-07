
import numpy as np
import pandas as pd
from nilearn.image import index_img
import nibabel as nib


fstr = 'vismap_grp_cat_rois_v2_%s_norm.nii.gz'

mappings = [['name', 'nii_file','nii_file_id','4dvolind']]
nrois = 83

for roi1 in range(nrois):
  nii_file = fstr %roi1
  for roi2 in range(nrois):
    _name = '%s_to_%s' %(roi1,roi2)
    _vol = roi2
    
    mappings.append([_name,nii_file,roi1,_vol])

#mappings_arr = np.array(mappings).astype(str)
#np.savetxt('mappings.txt', mappings_arr)

df_mappings = pd.DataFrame(mappings)
df_mappings = df_mappings.T.set_index([0]).T

df_mappings.to_csv('mappings.txt', sep=',',index=False)



# Make nonzero mappings

nzmappings = []

for roi1 in range(nrois):
  nii_file = fstr %roi1
  img = nib.load(nii_file)
  dat = img.get_data()
  for roi2 in range(nrois):

   
    _name = '%s_to_%s' %(roi1,roi2)


    print 'running for %s' %_name
    _vol = roi2

    #img = index_img(img,_vol)
    #dat = img.get_data()
    nzdat = np.nonzero(np.squeeze(dat[:,:,:,roi2]).ravel()>0)[0]

    nzmappings.append(nzdat)







