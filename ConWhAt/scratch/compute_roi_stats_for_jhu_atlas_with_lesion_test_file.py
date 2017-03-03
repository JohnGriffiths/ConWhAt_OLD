
import sys
sys.path.append('/u1/work/hpc3230/ConWhAt_brainhack')


from ConWhAt.volumetric import VolTractAtlas

va = VolTractAtlas('JHU')

idxs = [0,3,5]


les = 'lesion_test_file_from_jhu.nii.gz'
res = va.compute_hit_stats(les,idxs)




