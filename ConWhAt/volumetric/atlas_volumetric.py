
from utils import read_igzip_slice,get_intersection,get_bounding_box_inds,get_image_and_compare,compute_roi_bbox_overlaps

from ..base import Atlas,compare_images,ROIStats

import os
import nibabel as nib
import numpy as np
import pandas as pd

import ConWhAt

from joblib import Parallel,delayed

from matplotlib import pyplot as plt
import seaborn as sns

from nilearn.plotting import plot_stat_map
from nilearn.image import index_img

import yaml

import networkx as nx

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

  def compute_hit_stats(self,roi_file,idxs,readwith='indexgzip',n_jobs=1):
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
    bbox_isol,bbox_propol = compute_roi_bbox_overlaps(self.bboxes,roi_file) #est_file)
    bbox_isol_idx = np.nonzero(bbox_isol)[0]
    idxs = [idx for idx in idxs if idx in bbox_isol_idx]

    """
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
    """



    """     
    def get_image_and_compare(idx,file_mappings,roi_img):

      _name,_nii_file,_nii_file_id,_4dvolind = file_mappings.ix[idx]

      cnxn_dat = np.squeeze(read_igzip_slice(_nii_file,int(_4dvolind)))

      comp = compare_images(roi_img,cnxn_dat)
  
      comparisons = [_name,_nii_file,_4dvolind,comp]

      return comparisons

    """

    res = Parallel(n_jobs=n_jobs)(delayed(get_image_and_compare)(idx,self.image_file_mappings,roi_img) for idx in idxs)

    df = pd.concat({r[0]: pd.DataFrame(r[3].values(),index=r[3].keys(),
                                       columns=['val']) for r in res})
    df.index.names = ['name', 'metric']
    df = df.unstack('metric')['val'] 
 
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



  def plot_image(self,name=None,idx=None,ax=None,plotargs={'cmap': 'coolwarm'}):

    if name: 
      m = self.image_file_mappings.set_index('name').ix[name]
    elif idx: 
      m = self.image_file_mappings.ix[idx]

    nf = m['nii_file']
    vi = m['4dvolind']

    if not ax:  fig, ax = plt.subplots()
  
    plot_stat_map(index_img(nf,vi),axes=ax,**plotargs)

    return ax



class VolTractAtlas(VolAtlas):
  def __init__(self, atlas_name):
    VolAtlas.__init__(self, atlas_name)



class VolConnAtlas(VolAtlas):

  def __init__(self, atlas_name, conn_name = 'weights'):
    VolAtlas.__init__(self, atlas_name)

    self.load_connectivity(conn_name)
    self.make_nx_graph()


  def load_connectivity(self,conn_name):


    weights_file = '%s/%s.txt' %(self.atlas_dir,conn_name)
    tract_lengths_file = '%s/tract_lengths.txt' % self.atlas_dir
    region_labels_file = '%s/region_labels.txt' % self.atlas_dir
    region_xyzs_file = '%s/region_xyzs.txt'  %self.atlas_dir
    region_nii_file = '%s/region_masks.nii.gz' %self.atlas_dir
    hemis_file = '%s/hemispheres.txt' % self.atlas_dir
    ctx_file = '%s/cortex.txt' %self.atlas_dir

    regmap_fsav_lh_file = '%s/region_mapping_fsav_lh.txt' % self.atlas_dir
    regmap_fsav_rh_file = '%s/region_mapping_fsav_rh.txt' % self.atlas_dir  
   
 
    if os.path.isfile(weights_file): 
      self.weights = np.loadtxt(weights_file)
      self.weights_file = weights_file

    if os.path.isfile(tract_lengths_file): 
      self.tract_lengths = np.loadtxt(tract_lengths_file)
      self.tract_lengths_file = tract_lengths_file


    if os.path.isfile(region_labels_file):
      self.region_labels_file = region_labels_file
      self.region_labels = [l[:-1] for l in open(region_labels_file, 'r').readlines()]


    if os.path.isfile(region_xyzs_file):
      self.region_xyzs = np.loadtxt(region_xyzs_file)
      self.region_xyzs_file = region_xyzs_file

    if os.path.isfile(region_nii_file): 
      self.region_nii_file = region_nii_file


    if os.path.isfile(hemis_file): 
      self.hemis_file = hemis_file
      self.hemispheres = np.loadtxt(hemis_file)
 
    if os.path.isfile(ctx_file): 
      self.cortex = np.loadtxt(ctx_file)


    if os.path.isfile(regmap_fsav_lh_file) and os.path.isfile(regmap_fsav_rh_file):

      self.fsaverage_region_mapping = True

      self.region_mapping_lh_file = regmap_fsav_lh_file
      self.region_mapping_rh_file = regmap_fsav_rh_file

      # (should we load these on initialization?)
      self.region_mapping_lh = np.loadtxt(regmap_fsav_lh_file)
      self.region_mapping_rh = np.loadtxt(regmap_fsav_rh_file)
     
      cfg_file = '../../config.yaml'
      rl = open(cfg_file, 'r').readlines()
      cfg = yaml.load(rl[1])
      fs_subjects_dir = cfg['fs_subjects_dir']
      
      self.surf_lh_file = '%s/fsaverage/surf/lh.white' %fs_subjects_dir
      self.surf_rh_file = '%s/fsaverage/surf/rh.white' %fs_subjects_dir



  def make_nx_graph(self):

    G = nx.DiGraph()
    ifms = self.image_file_mappings
    bbs = self.bboxes

    # add edge info
    for idx in ifms.index:
      ifm = ifms.ix[idx]
      roi1,roi2 = ifm['name'].split('_to_')
      roi1 = int(roi1); roi2 = int(roi2)
      ad = ifm.to_dict()
      ad.update(bbs.ix[idx])
      ad['idx'] = idx
      ad['weight'] = self.weights[roi1,roi2]
      G.add_edge(roi1,roi2,attr_dict=ad)
    

    # add node info
    for node_it,node in enumerate(self.region_labels):
    
      rl = self.region_labels[node_it]
      hemi = self.hemispheres[node_it]
      ctx = self.cortex[node_it]
    
      G.node[node_it].update({'region_label': rl,
                              'hemisphere': hemi,
                              'cortex': ctx})


    self.Gnx = G




            





