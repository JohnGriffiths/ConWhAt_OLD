
from utils import get_vol_atlas_info,read_igzip_slice,get_intersection,get_bounding_box_inds


from ..base import Atlas,compare_images,ROIStats

import os
import nibabel as nib
import numpy as np
import pandas as pd

import ConWhAt


class VolAtlas(Atlas):
  """
  
  Volumetric atlas base class directly
  connectivity-based atlas subtypes from this
  
  connectivity-based atlas mostly just adds in loops and things related to matrices
  ...not much of core functionality
  (modifications can also be done for tract-based atlas)
  
  
  """

  import nibabel as nib
  import numpy as np
  from nilearn.image import index_img

  def __init__(self,atlas_name):
    
    self.atlas_dir = os.path.split(ConWhAt.__file__)[0]  + '/atlases/volumetric/%s' %atlas_name
    
    self.image_file_mappings = pd.read_csv(self.atlas_dir + '/mappings.txt', sep=',')

    self.bboxes = pd.read_csv(self.atlas_dir + '/bounding_boxes.txt', sep=',')


  def compute_roi_bbox_overlaps(self,roi_file):

    roi_bbox = get_bounding_box_inds(roi_file) 

    bbox_isol,bbox_propol = [],[]
    
    for ix in self.bboxes.index:

      bbox = self.bboxes.ix[ix].values

      if True in np.isnan(bbox): SI = 0.
      else: 
        bbox = [[bbox[0],bbox[1]],[bbox[2],bbox[3]],[bbox[4],bbox[5]]]
        SI = get_intersection(roi_bbox,bbox)
      bbox_isol.append(SI!=0)
      bbox_propol.append(SI)

    return bbox_isol,bbox_propol



  def compute_hit_stats(self,roi_file,idxs,readwith='indexgzip'):

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
    roi_dat = roi_img.get_data()


    res = []

    if idxs == 'all': idxs = range(self.image_file_mappings.shape[0])

    # only read files with overlapping bounding boxes
    bbox_isol,bbox_propol = self.compute_roi_bbox_overlaps(roi_file) #est_file)
    bbox_isol_idx = np.nonzero(bbox_isol)[0]
    idxs = [idx for idx in idxs if idx in bbox_isol_idx]

    for idx in idxs:
      
      #_name,_file,_vol = self.atlas_info['mappings'][idx]

      _name,_nii_file,_nii_file_id,_4dvolind = self.image_file_mappings.ix[idx]

      if readwith=='index_img':
        cnxn_img = index_img(_nii_file,_4dvolind)
        cnxn_dat = cnxn_img.get_data()
      elif readwith == 'indexgzip':
        cnxn_dat = np.squeeze(read_igzip_slice(_nii_file,int(_4dvolind)))

      comp = compare_images(roi_img,cnxn_dat)
  
      res.append([_name,_nii_file,_4dvolind,comp])


    df = pd.concat({r[0]: pd.DataFrame(r[3].values(),index=r[3].keys(),
                                       columns=['val']) for r in res})
    df.index.names = ['structure', 'metric']
    
    return res,df



  def compute_hit_stats_test(self,roi_file,idxs,readwith='indexgzip'):

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

    if idxs == 'all': idxs = range(self.image_file_mappings.shape[0])

    # only read files with overlapping bounding boxes
    bbox_isol,bbox_propol = self.compute_roi_bbox_overlaps(roi_file) #est_file)
    bbox_isol_idx = np.nonzero(bbox_isol)[0]
    idxs = [idx for idx in idxs if idx in bbox_isol_idx]


    mappings = self.image_file_mappings

    # group together the nifti files for each index

    # - get all unique file ids for the supplied indices
    file_ids = np.unique(mappings['nii_file_id'])
    # - run through each file, load in, and grab the volume indices
    for file_id in file_ids:
      
      # - pick out elements in idxs that correspond to this file
      idxsforthisfile = np.nonzero(mappings['nii_file_id'] == file_id)[0]
      idxstouse = [i for i in idxsforthisfile if i in idxs]

      if len(idxstouse) >0:

        # - load the image
        nii_f = mappings.ix[idxstouse[0]]['nii_file']
        nii_img = nib.load(nii_f)
        nii_dat = nii_img.get_data()


        namesforthisfile = list(mappings.ix[idxstouse]['name'].values)
        volsforthisfile = list(mappings.ix[idxstouse]['4dvolind'].values)
    
   
        for v,n in zip(volsforthisfile,namesforthisfile):

          this_dat = np.squeeze(nii_dat[:,:,:,v])
          #this_img = nib.Nifti1Image(nii_dat[:,:,:,v]index_img(nii_img,v)

          comp = compare_images(roi_img,this_dat)

          res.append([n,nii_f,v,comp])

    if len(res)>0: 
      df = pd.concat({r[0]: pd.DataFrame(r[3].values(),index=r[3].keys(),
                                       columns=['val']) for r in res})
      df.index.names = ['structure', 'metric']
    else: 
      res,df = [],[]  

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



