from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

#submitVersion = "Moriond18_V1"
submitVersion = "Legacy16_V1"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
#doHLTTree = 'doTrigger=False'
#calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/micheli/TnP/ntuples_20180412/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '/afs/cern.ch/work/m/micheli/test_tnp_20180412/CMSSW_9_4_5/src/EgammaAnalysis/TnPTreeProducer/python/TnPTreeProducer_cfg.py'
#config.Data.allowNonValidInputDataset = False
config.JobType.sendExternalFolder     = True

config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.allowNonValidInputDataset = True
#config.Data.publishDataName = 

config.Site.storageSite = 'T2_CH_CERN'



if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_%s' % submitVersion

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)


    ##### submit MC
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
    config.Data.splitting     = 'FileBased'
    config.Data.unitsPerJob   = 8
#    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=94X_mc2017_realistic_v10']
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=80X_dataRun2_2016LegacyRepro_v3']

    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'#FRA update this
    submit(config)
    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-ext1'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10_ext1-v1/MINIAODSIM'#FRA update this
    submit(config)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
#    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    config.Data.unitsPerJob   = 100
#    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,'GT=94X_dataRun2_ReReco17_forValidation']
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,'GT=80X_dataRun2_2016LegacyRepro_v3'] 

#    config.General.requestName  = '17Nov2017_RunB'
#    config.Data.inputDataset    = '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD'
#  #  submit(config)    
#    config.General.requestName  = '17Nov2017_RunC'
#    config.Data.inputDataset    = ''
#  #  submit(config)    
#    config.General.requestName  = '17Nov2017_RunD'
#    config.Data.inputDataset    = '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD'
#   # submit(config)    
#    config.General.requestName  = '17Nov2017_RunE'
#    config.Data.inputDataset    = '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD'
# #   submit(config)    
#    config.General.requestName  = '17Nov2017_RunF'
#    config.Data.inputDataset    = '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD'
#    #submit(config)    

    config.General.requestName  = '07Aug17_Run2016Bv1'
    config.Data.inputDataset    = '/SingleElectron/Run2016B-07Aug17_ver1-v1/MINIAOD' #FRA which one of the two?
    config.General.requestName  = '07Aug17_Run2016B'
    config.Data.inputDataset    = '/SingleElectron/Run2016B-07Aug17_ver2-v2/MINIAOD' #FRA which one of the two?
  #  submit(config)    
    config.General.requestName  = '07Aug17_Run2016C'
    config.Data.inputDataset    = '/SingleElectron/Run2016C-07Aug17-v1/MINIAOD'
  #  submit(config)    
    config.General.requestName  = '07Aug17_Run2016D'
    config.Data.inputDataset    = '/SingleElectron/Run2016D-07Aug17-v1/MINIAOD'
   # submit(config)    
    config.General.requestName  = '07Aug17_Run2016E'
    config.Data.inputDataset    = '/SingleElectron/Run2016E-07Aug17-v1/MINIAOD'
 #   submit(config)    
    config.General.requestName  = '07Aug17_Run2016F'
    config.Data.inputDataset    = '/SingleElectron/Run2016F-07Aug17-v1/MINIAOD'
    #submit(config)    
    config.General.requestName  = '07Aug17_Run2016G'
    config.Data.inputDataset    = '/SingleElectron/Run2016G-07Aug17-v1/MINIAOD'
    #submit(config)    
    config.General.requestName  = '07Aug17_Run2016H'
    config.Data.inputDataset    = '/SingleElectron/Run2016H-07Aug17-v1/MINIAOD'
    #submit(config)    





#/SingleElectron/Run2017A-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017A-PromptReco-v3/MINIAOD
#/SingleElectron/Run2017B-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017B-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v2/MINIAOD
#/SingleElectron/Run2017C-PromptReco-v3/MINIAOD
#/SingleElectron/Run2017D-PromptReco-v1/MINIAOD
#/SingleElectron/Run2017E-PromptReco-v1/MINIAOD



