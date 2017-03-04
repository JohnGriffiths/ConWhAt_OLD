
from utils import get_vol_atlas_info
from ..base import Atlas,compare_images,ROIStats

import nibabel as nib
import numpy as np
import pandas as pd

class VolAtlas(Atlas):
  """
  
  Volumetric atlas base class
  
  tract-based atlas uses this class directly
  connectivity-based atlas subtypes from this
  
  connectivity-based atlas mostly just adds in loops and things related to matrices
  ...not much of core functionality
  (modifications can also be done for tract-based atlas)
  
  
  """

  import nibabel as nib
  import numpy as np
  from nilearn.image import index_img

  def __init__(self,atlas_name):
    
    atlas_info = get_vol_atlas_info(atlas_name)
    # get_atlas_info  will return a dict, which includes connectivity stuff if it's that kind of atlas
    
    self.atlas_info = atlas_info

  def compute_hit_stats(self,roi_file,idxs):

    """
    idxs correspond to the entries in the 'mappings' 
    attribute of the atlas_info

    'mappings' is a three element list of 
    [name,file,volume] for each atlas structure
    
    if idx=='all', all structures are analyzed

 
    """

    import nibabel as nib
    import numpy as np
    from nilearn.image import index_img

    print 'computing hit stats for roi %s' % roi_file

    roi_img = nib.load(roi_file)


    res = []

    if idxs == 'all': 
      idxs = range(len(self.atlas_info['mappings']))

    for idx in idxs:
      
      #_name,_file,_vol = self.atlas_info['mappings'][idx]

      _name,_nii_file,_nii_file_id,_4dvolind = self.atlas_info['mappings'].ix[idx]

      _file = self.at_dir + '/' + _nii_file
      _vol = _4dvolind

      cnxn_img = index_img(_file,_vol)

      comp = compare_images(roi_img,cnxn_img)
  
      res.append([_name,_file,_vol,comp])


    df = pd.concat({r[0]: pd.DataFrame(r[3].values(),index=r[3].keys(),
                                       columns=['val']) for r in res})
    df.index.names = ['structure', 'metric']
    
    return res,df



  def compute_hit_stats_test(self,roi_file,idxs):
    """
    idxs correspond to the entries in the 'mappings' 
    attribute of the atlas_info

    'mappings' is a three element list of 
    [name,file,volume] for each atlas structure
    
    if idx=='all', all structures are analyzed

 
    """

    import nibabel as nib
    import numpy as np
    from nilearn.image import index_img

    print 'computing hit stats for roi %s' % roi_file

    roi_img = nib.load(roi_file)


    res = []

    if idxs == 'all': 
      idxs = range(len(self.atlas_info['mappings']))

    mappings = self.atlas_info['mappings']

    # group together the nifti files for each index

    # - get all unique file ids for the supplied indices
    file_ids = np.unique(mappings.ix[idxs]['nii_file_id'])

    # - run through each file, load in, and grab the volume indices
    for file_id in file_ids:
      
      # - pick out elements in idxs that correspond to this file
      idxsforthisfile = np.nonzero(mappings['nii_file_id'] == file_id)[0]
      idxstouse = [i for i in idxsforthisfile if i in idxs]


      # - load the image
      nii_f = self.at_dir + '/' + mappings.ix[idxstouse[0]]['nii_file']
      nii_img = nib.load(nii_f)
      nii_dat = nii_img.get_data()


      namesforthisfile = list(mappings.ix[idxstouse]['name'].values)
      volsforthisfile = list(mappings.ix[idxstouse]['4dvolind'].values)
    
   
      for v,n in zip(volsforthisfile,namesforthisfile):

        this_dat = np.squeeze(nii_dat[:,:,:,v])
        #this_img = nib.Nifti1Image(nii_dat[:,:,:,v]index_img(nii_img,v)

        comp = compare_images(roi_img,this_dat)

        res.append([n,nii_f,v,comp])

    df = pd.concat({r[0]: pd.DataFrame(r[3].values(),index=r[3].keys(),
                                       columns=['val']) for r in res})
    df.index.names = ['structure', 'metric']
    
    return res,df




  def compute_roi_stats(self,fa_image,cnxn_ids):

    res = ROIStats()
    print 'blah'


class VolTractAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)



class VolConnAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)











  def compute_roi_stats(self,fa_image,cnxn_ids):

    res = ROIStats()
    print 'blah'


class VolTractAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)



class VolConnAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)


