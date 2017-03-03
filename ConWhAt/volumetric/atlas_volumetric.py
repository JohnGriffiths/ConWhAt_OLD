
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
    idxs is a list of lists of vol ids for each file id
    
    so something like


    [0, [0,1,2,3,4,5,6...]  # - default for something like JHU
    [0, [0,1,2,3,4,5,6,...],
     1, [0,1,2,3,4,5,6,...],
     2, [0,1,2,3,4,5,6,...]] # default for full connectome
    [0, [0,4,6],
     3, [2,7,9]]              # random selection 

    numbers on the left are the file number
    numbers on the right are the (4th dim) volume ids inside that file
 
    """

    import nibabel as nib
    import numpy as np
    from nilearn.image import index_img

    print 'computing hit stats for roi %s' % roi_file

    roi_img = nib.load(roi_file)


    file_res = []

    for (file_idx,vol_idxs) in idxs:

      cnxns_file = self.atlas_info['files'][file_idx]
      cnxns_img = nib.load(cnxns_file)

      vol_res = []
      for vol_idx in vol_idsx:

        name = self.atlas_info['names'][file_idx][vol_idx]

        cnxn_img = index_img(cnxns_img,vol_idx)
      
        comp = compare_images(roi_img,cnxn_img)
  
        vol_res.append(comp)
      
      file_res.append(vol_res)

    return file_res


  def compute_roi_stats(self,fa_image,cnxn_ids):

    res = ROIStats()
    print 'blah'


class VolTractAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)



class VolConnAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)


