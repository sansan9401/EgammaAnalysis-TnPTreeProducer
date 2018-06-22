from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys
config = config()

submitVersion ="2017Data_FullJson"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=True'
#doHLTTree = 'doTrigger=False'
#calibEn   = 'useCalibEn=False'

mainOutputDir = '/store/group/phys_egamma/soffi/TnP/ntuples_06152018/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = '/afs/cern.ch/work/s/soffi/EGM-WORK/CMSSW-1011-2017DataTnP/src/EgammaAnalysis/TnPTreeProducer/python/TnPTreeProducer_cfg.py'
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
    config.Data.unitsPerJob   = 4
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,'GT=94X_mc2017_realistic_v13']

    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1/MINIAODSIM'
    submit(config)

    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8-ext1'
    config.Data.inputDataset    = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-ext1-v1/MINIAODSIM'
    submit(config)


    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,'GT=94X_dataRun2_v6']

    config.General.requestName  = '17Nov2017_RunB'
    config.Data.inputDataset    = '/SingleElectron/Run2017B-17Nov2017-v1/MINIAOD'
    submit(config)    
    config.General.requestName  = '17Nov2017_RunC'
    config.Data.inputDataset    = '/SingleElectron/Run2017C-17Nov2017-v1/MINIAOD'
    submit(config)    
    config.General.requestName  = '17Nov2017_RunD'
    config.Data.inputDataset    = '/SingleElectron/Run2017D-17Nov2017-v1/MINIAOD'
    submit(config)    
    config.General.requestName  = '17Nov2017_RunE'
    config.Data.inputDataset    = '/SingleElectron/Run2017E-17Nov2017-v1/MINIAOD'
    submit(config)    
    config.General.requestName  = '17Nov2017_RunF'
    config.Data.inputDataset    = '/SingleElectron/Run2017F-17Nov2017-v1/MINIAOD'
    submit(config)    

