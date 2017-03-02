
import sys
sys.path.append('/u1/work/hpc3230/ConWhAt_brainhack')

from ConWhAt.volumetric import VolTractAtlas

va = VolTractAtlas('JHU')

import nibabel as nib

img = nib.load(va.atlas_info['files'][0])
dat = img.get_data()

from nilearn.image import index_img

img0 = index_img(img,0)
new_img = nib.Nifti1Image((img0.get_data() > 20).astype('float'),img0.affine)
new_img.to_filename('lesion_test_file_from_jhu.nii.gz')


