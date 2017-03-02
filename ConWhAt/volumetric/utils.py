
def get_vol_atlas_info(atlas_name,fsl_data_dir = '/opt/fsl/5.0.9/fsl/data'):

  returndict = {'atlas_name':atlas_name}

  if atlas_name == 'JHU':

    xml_file = fsl_data_dir + '/atlases/JHU-tracts.xml'
    nii_file = fsl_data_dir + '/atlases/JHU/JHU-ICBM-tracts-prob-2mm.nii.gz'

    rls = open(xml_file, 'r').readlines()
    names = [r.split('>')[1].split('<')[0] for r in rls[15:-3]]
    
    returndict['names'] = [names]
    returndict['files'] = [nii_file]


  elif atlas_name == 'l2k8_sc33':

    returndict['names'] = []
    returndict['files'] = []


  else: 

    print 'atlas name not recognized' 

  return returndict


