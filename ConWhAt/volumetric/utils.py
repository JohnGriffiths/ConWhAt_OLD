import os,numpy as np,sys,glob
import pandas as pd
import yaml
import indexed_gzip as igzip
import nibabel as nib

from itertools import product,combinations

from matplotlib import pyplot

import nibabel as nib

from nilearn.plotting import plot_stat_map

from nilearn.image import index_img

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import numpy as np
from itertools import product,combinations



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



def read_igzip_slice(fname,volnum):
  
  # Here we are usin 4MB spacing between
  # seek points, and using a larger read
  # buffer (than the default size of 16KB).
  fobj = igzip.IndexedGzipFile(
      filename=fname,#'big_image.nii.gz',
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


def read_igzip_multislice(fname,volnums):
  
  # Here we are usin 4MB spacing between
  # seek points, and using a larger read
  # buffer (than the default size of 16KB).
  fobj = igzip.IndexedGzipFile(
      filename=fname,#'big_image.nii.gz',
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
  #dats = np.array([np.squeeze(image.dataobj[:, :, :, int(volnum)]) for volnum in volnums])
  
  res=np.array([(image.dataobj[:, :, :, int(volnum)]) for volnum in volnums])

  dims  = res.shape
  res = res.reshape([dims[1],dims[2],dims[3],dims[0]])
    
  return res





def get_bounding_box_inds(dat):
  
  if (dat>0).sum()  > 0:
 
    nzx,nzy,nzz = np.nonzero(dat>0)
    xmin,xmax = nzx.min(),nzx.max()
    ymin,ymax = nzy.min(),nzy.max()
    zmin,zmax = nzz.min(),nzz.max()
    
    minmaxarr = np.array([[xmin,xmax],[ymin,ymax],[zmin,xmax]])    
    
    return minmaxarr

  else: 

    print 'no nonzero voxels'
    #return np.nan
    return [(np.nan,np.nan),(np.nan,np.nan),(np.nan,np.nan)]


    
def plot_cube_from_bb(bb,ax=None,c='b'):

  corners = np.array(list(product(bb[0],
                                  bb[1],
                                  bb[2])))
    
  cornerpairs = list(combinations(corners,2))

  linestoplot = [(s,e) for (s,e) in cornerpairs if ((np.abs(s-e) == 0).sum() == 2)]
    

  if not ax:
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    
  for (s,e) in linestoplot: 
    ax.plot3D(*zip(s,e), color=c) 
        
    
    
  
def plot_vol_scatter(dat,ax=None, pointint = 50,c='b',alpha=0.2,s=20.,
                     xlim=[0,100],ylim=[0,100],zlim=[0,100],marker='o',figsize=(10,10),
                     linewidth=0.01):
    
  xs,ys,zs = np.nonzero(dat>0)    
  idx = np.arange(0,xs.shape[0],pointint)

  if not ax: 
    fig = plt.figure(figsize=figsize)
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')
    ax.set_xlim([xlim[0],xlim[1]])  
    ax.set_ylim([ylim[0],ylim[1]])
    ax.set_zlim([zlim[0],zlim[1]])

  ax.scatter3D(xs[idx],ys[idx],zs[idx],c=c,alpha=alpha,s=s, marker=marker,linewidths=linewidth)
    
    
def get_intersection(bba,bbb):
    
  (xa1,xa2),(ya1,ya2),(za1,za2) = bba
  (xb1,xb2),(yb1,yb2),(zb1,zb2) = bbb
    
  SI = max(0, min(xa2,xb2) - max(xa1,xb1)) \
     * max(0, min(ya2,yb2) - max(ya1,yb1)) \
     * max(0, min(za2,zb2) - max(za1,zb1))

  return SI




