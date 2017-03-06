
# (hit statistics for two vectors)

 

import nibabel as nib
import numpy as np

 

def get_stats(TP,TN,FP,FN):

  # Source: https://en.wikipedia.org/wiki/Confusion_matrix

  # Condition positive
  P = TP + FN
    
  # Condition negative
  N = TN + FP
    
  # sensitivity / recall / hit rate / true positive rate (TPR)
  TPR = TP / (TP + FN)

  # specificity / true negative rate (TNR)
  TNR = TN / (FP + TN)
  
  # precision / positive predictive value (PPV)
  PPV = TP / (TP + FP)

  # negative predictive value (NPV)
  NPV = TN / (TN + FN)

  # fall-out / false positive rate (FPV)
  FPR = FP / (FP + TN)

  # false discovery rate (FDR)
  FDR = FP / (FP + TP) 

  # miss rate / false negative rate (FNR)
  FNR = FN / (FN + TP)
    
  # accuracy
  ACC = (TP + TN) / (P + N)
    
  # F1 score
  F1 = (2*TP) / (2*TP + FP + FN)
    
  # Matthews correlation coefficient (MCC)
  MCC = (TP*TN - FP*FN) / (np.sqrt((TP + FP)*(TP+FN)*(TN+FP)*(TN+FN)))
                           
  # Informedness / Bookmaker Informedness (BM)
  BM = TPR + TNR - 1
  
  # Markedness (MK)
  MK = PPV + NPV - 1

  RD = {'TPR': TPR, 'TNR': TNR,'PPV': PPV, 'NPV': NPV, 'FPR': FPR, 'FDR': FDR, 
        'FNR': FNR, 'ACC': ACC, 'F1': F1, 'MCC': MCC, 'BM': BM, 'MK': MK,
        'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}
  
  return RD



def compare_images(f1,f2, thr1=0,thr2=0):
    
  # Image 1 is the reference image
  # Image 2 is the image being tested

  if type(f1) == np.ndarray:
    dat1 = f1
  elif type(f1) == str:    
    img1 = nib.load(f1)
    dat1 = img1.get_data()
  else: 
    img1 = f1
    dat1 = img1.get_data()

 
  if type(f2) == np.ndarray:
    dat2 = f2
  elif type(f2) == str:
    img2 = nib.load(f2)
    dat2 = img2.get_data()
  else:
    img2 = f2
    dat2 = img2.get_data()

 
  dat1_thr = dat1.copy()
  dat1_thr[dat1_thr<thr1] = 0
    
  dat2_thr = dat2.copy()
  dat2_thr[dat2_thr<thr2] = 0
    
  dat1_thrbin = dat1_thr.copy()
  dat1_thrbin[dat1_thrbin>0] = 1
    
  dat2_thrbin = dat2_thr.copy()
  dat2_thrbin[dat2_thrbin>0] = 1

    
  thrbin_mul = dat1_thrbin*dat2_thrbin
  thrbininv_mul = (dat1_thrbin==0)*(dat2_thrbin==0)
  
  
  TP = thrbin_mul.sum()
  TN = thrbininv_mul.sum()
  FP = dat2_thrbin.sum() - TP
  FN = thrbininv_mul.sum()-TN
    
  hit_stats = get_stats(TP,TN,FP,FN)
    
  res = hit_stats

  res['corr_nothr'] = np.corrcoef(dat1.ravel(),dat2.ravel())[0,1]
  res['corr_thr'] = np.corrcoef(dat1_thr.ravel(),dat2_thr.ravel())[0,1]
  res['corr_thrbin'] = np.corrcoef(dat1_thrbin.ravel(),dat2_thrbin.ravel())[0,1]
    
  return res


