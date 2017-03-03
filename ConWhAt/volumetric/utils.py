
import yaml

def get_vol_atlas_info(atlas_name):

  returndict = {'atlas_name':atlas_name}

  if atlas_name == 'JHU':

    rl = open('../../config.yaml', 'r').readlines()
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


  elif atlas_name == 'l2k8_sc33':

    returndict['names'] = []
    returndict['files'] = []


  else: 

    print 'atlas name not recognized' 

  return returndict


