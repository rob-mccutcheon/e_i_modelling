import nibabel as nib
import sys
import os
import numpy as np
import pandas as pd
import subprocess
sys.path.append('/home/k1201869/glu_rs/src')
from glu_fuctions import conn_calc, plotting
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
import shutil
import bct


results_dir = '/home/k1201869/e_i_modelling/results/hcp_processed'
atlas = 'dk'
subject_list = os.listdir(results_dir)
subject_list.remove('collated')
subject_list.remove('hcp_ep_glasser.zip')
subject = '1002_01_MR'

path='/home/k1201869/e_i_modelling/data/processed/1001_01_MR/MNINonLinear/fsaverage_LR32k/1001_01_MR.aparc.32k_fs_LR.dlabel.nii'
a=nib.cifti2.load(f'/home/k1201869/e_i_modelling/data/processed/{subject}/MNINonLinear/fsaverage_LR32k/{subject}.aparc.32k_fs_LR.dlabel.nii')
np.max(a.get_data())
a.affine
header = a.header
print(header.get_data_shape())
path.get_data()
a.cifti2Label()
nib.cifti2.cifti2Label(path)
len(np.where(np.sum(tseries_df==0))[0])

# Load denoised surface time series
group_cm = []
identify = []
for subject in subject_list:
    tseries = nib.cifti2.load(f'{results_dir}/{subject}/{atlas}.ptseries.nii')
    tseries_df = pd.DataFrame(tseries.get_data())
    if atlas=='dk':
        tseries_df = tseries_df.drop([3, 38], axis=1)

    # Pearson correlation matrix
    cm = tseries_df.corr().values
    if len(np.where(np.sum(tseries_df==0))[0]) != 2:
        identify.append(subject)

    # Zeros for diagonal
    np.fill_diagonal(cm,0)

    # Save connectivity matrix
    np.savetxt(f"{results_dir}/{subject}/{subject}_{atlas}_pearson.csv", cm, delimiter=",")

    # adjust
    adjust_cm = (cm - np.mean(cm))/np.std(cm)
    group_cm.append(cm)

# Group mean
mean_cm = np.array(np.mean(group_cm,0))

# Gordon sorting
cm_sort = conn_calc.gordon_sort(mean_cm)


# Gordon plotting
plt.rcParams['figure.figsize'] = [10, 10]
plotting.rdbu_heatmap(cm_sort[0], vmax=1, vmin=-1, lines=cm_sort[1], center=0)

# Glasser plotting
com = bct.community_louvain(mean_cm, gamma=1.2, B='negative_sym')
order=[]
for network in np.unique(com[0]):
    order=order+np.where(com[0]==network)[0].tolist()
sns.heatmap(cm[order][:,order], cmap='RdBu_r', vmax=1, vmin=-1, center=0)

# Make zip
for subject in subject_list:
    src = f"{results_dir}/{subject}/{subject}_{atlas}_pearson.csv"
    dst = f"{results_dir}/collated/{subject}_{atlas}_pearson.csv"
    shutil.copy(src, dst)

# demo details
demo_df=pd.read_csv("/home/k1201869/e_i_modelling/results/hcp_processed/collated/ndar_subject01.txt", sep="\t")


ptsd = []
ptmn = []
consd = []
conmn = []
for subject in subject_list:
    diagnosis = demo_df[demo_df.src_subject_id==subject[:4]]['phenotype']
    if diagnosis.values[0] == 'Control':
        cm = pd.read_csv(f"{results_dir}/{subject}/{subject}_{atlas}_pearson.csv", header=None).values
        consd.append(np.std(cm))
        conmn.append(np.mean(cm))

    if diagnosis.values[0] == 'Patient':
        cm = pd.read_csv(f"{results_dir}/{subject}/{subject}_{atlas}_pearson.csv", header=None).values
        ptsd.append(np.std(cm))
        ptmn.append(np.mean(cm))
diag = len(ptsd)*['pt']+len(consd)*['con']
sns.scatterplot(diag, ptsd+consd)
plt.ylabel('SD')
sns.scatterplot(diag, ptmn+conmn)
np.mean(ptsd)
np.mean(consd)
np.std(np.array(con))

len(pt)

cm.shape