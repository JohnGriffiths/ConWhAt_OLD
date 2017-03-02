
import sys
sys.path.append('/u1/work/hpc3230/ConWhAt')

from ConWhAt.volumetric import VolTractAtlas

va = VolTractAtlas('JHU')

idxs = [0]

res = va.compute_hit_stats('lesion_test_file_from_jhu.nii.gz',idxs)




