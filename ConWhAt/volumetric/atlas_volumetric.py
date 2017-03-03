
from utils import get_vol_atlas_info
from ..base import Atlas,compare_images,ROIStats

import nibabel as nib
import numpy as np

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
      
      _name,_file,_vol = self.atlas_info['mappings'][idx]

      cnxn_img = index_img(_file,_vol)

      comp = compare_images(roi_img,cnxn_img)
  
      res.append([_name,_file,_vol,comp])
      
    return res


  def compute_roi_stats(self,fa_image,cnxn_ids):

    res = ROIStats()
    print 'blah'


class VolTractAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)



class VolConnAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)


