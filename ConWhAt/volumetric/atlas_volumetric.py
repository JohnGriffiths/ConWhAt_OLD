

from utils import get_vol_atlas_info
from ..base import Atlas,HitStats,ROIStats




class VolAtlas(Atlas):
  """

  Volumetric atlas base class

  tract-based atlas uses this class directly
  connectivity-based atlas subtypes from this

  connectivity-based atlas mostly just adds in loops and things related to matrices
  ...not much of core functionality
  (modifications can also be done for tract-based atlas)


  """

  def __init__(self,atlas_name):

    atlas_info = get_vol_atlas_info(atlas_name)
    # get_atlas_info  will return a dict, which includes connectivity stuff if it's that kind of atlas

    self.atlas_info = atlas_info

  def compute_hit_stats(self,roi_file,cnxn_ids):

    print 'computing hit stats for roi %s' % roi_file

    roi_img = nib.load(roi_file)

    cnxn_file = va.atlas_info['files'][0]
    cnxns_img = nib.load(cnxn_img_file)

    res = []

    for idx in cnxn_ids:

      name = va.atlas_info['names'][idx]

      cnxn_img = index_img(cnxn_img,idx)
  
      res.append(HitStats(roi_img,cnxn_img)
      

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


