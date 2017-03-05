import os,numpy as np,sys,glob
import pandas as pd
import yaml
import indexed_gzip as igzip
import nibabel as nib




def get_vol_atlas_info(atlas_name):

  returndict = {'atlas_name':atlas_name}

  if atlas_name == 'JHU':

    cfg_file = os.path.abspath('../../config.yaml')
    rl = open(cfg_file, 'r').readlines()
    cfg = yaml.load(rl[0])
    fsl_data_dir = cfg['fsl_data_dir']


    xml_file = fsl_data_dir + '/atlases/JHU-tracts.xml'
    nii_file = fsl_data_dir + '/atlases/JHU/JHU-ICBM-tracts-prob-2mm.nii.gz'

    rls = open(xml_file, 'r').readlines()
    names = [r.split('>')[1].split('<')[0] for r in rls[15:-3]]
    
    returndict['names'] = [names]
    returndict['files'] = [nii_file]

    mappings = []
    for _vol,_name in enumerate(names):

      mappings.append([_name,nii_file,_vol])

    returndict['mappings'] = mappings


  elif atlas_name == 'dipy_dsi_sd4_l2k8_sc33':

    returndict['names'] = []
    returndict['files'] = []
 
    at_dir  = os.path.abspath('../atlases/volumetric/dipy_dsi_sd4_l2k8_sc33')
    
    """
    at_fstr = at_dir + '/vismap_grp_cat_rois_v2_%s_norm.nii.gz'

    mappings = []
    nrois = 83

    for roi1 in range(nrois):
      nii_file = at_fstr %roi1
      for roi2 in range(nrois):
        _name = '%s_to_%s' %(roi1,roi2)
        _vol = roi2
        mappings.append([_name,nii_file,_vol])

    """

    #mappings = np.loadtxt(at_dir + '/mappings.txt')

    mappings = pd.read_csv(at_dir + '/mappings.txt', sep=',')

    returndict['mappings'] = mappings

  else: 

    print 'atlas name not recognized' 

  return returndict







def read_niigzip_vol(fname,volnum):
  # Here we are usin 4MB spacing between
  # seek points, and using a larger read
  # buffer (than the default size of 16KB).
  fobj = igzip.IndexedGzipFile(
    filename=fname,
    spacing=4194304,
    readbuf_size=131072)

  # Create a nibabel image using 
  # the existing file handle.
  fmap = nib.Nifti1Image.make_file_map()
  fmap['image'].fileobj = fobj
  image = nib.Nifti1Image.from_file_map(fmap)

  # Use the image ArrayProxy to access the 
  # data - the index will automatically be
  # built as data is accessed.
  dat = np.squeeze(image.dataobj[:, :, :, volnum])

  return dat





