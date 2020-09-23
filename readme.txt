 Preproccessing

Imaging data downloaded using javaws

HCP pipelines downloaded to k1201869/hcp/code

Need to download MSM binaries https://github.com/ecr05/MSM_HOCR/releases

preprocessing instructions at:
https://github.com/Washington-University/HCPpipelines/wiki/Installation-and-Usage-Instructions

Need to copy subjects data from imagingcollection1 to fmriresults/unprocessed/3T

Need to amend SetUpHCPPipeline.sh:

export HCPPIPEDIR="${HOME}/hcp/code/HCPpipelines-4.2.0-rc.1"
## Set up other environment variables
export MSMBINDIR="${HOME}/hcp/code/HCPpipelines-4.2.0-rc.1/MSMBinaries"

Need to amend GenericfMRIVOlumeProcessigPipelineBatch.sh and GenericfMRISurfaceProcessigPipelineBatch.sh:
StudyFolder="${HOME}//home/k1201869/e_i_modelling/data/HCPEPRelease/imagingcollection01" #Location of Subject folders (named by subjectID)
# StudyFolder="${HOME}/projects/Pipelines_ExampleData" #Location of Subject folders (named by subjectID)

Subjlist="1001_01_MR" #Space delimited list of subject IDs
EnvironmentScript="${HOME}/hcp/code/HCPpipelines-4.2.0-rc.1/Examples/Scripts/SetUpHCPPipeline.sh"

Tasklist=""
Tasklist="${Tasklist} rfMRI_REST1_RL"
Tasklist="${Tasklist} rfMRI_REST1_LR"
Tasklist="${Tasklist} rfMRI_REST2_RL"
Tasklist="${Tasklist} rfMRI_REST2_LR"

Run volume then run surface
