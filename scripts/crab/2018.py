from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import sys

# this will use CRAB client API
from CRABAPI.RawCommand import crabCommand

# talk to DBS to get list of files in this dataset
#from dbs.apis.dbsClient import DbsApi
#dbs = DbsApi('https://cmsweb.cern.ch/dbs/prod/global/DBSReader')

#dataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM'
#fileDictList=dbs.listFiles(dataset=dataset)

#print ("dataset %s has %d files" % (dataset, len(fileDictList)))

# DBS client returns a list of dictionaries, but we want a list of Logical File Names
#lfnList = [ dic['logical_file_name'] for dic in fileDictList ]

# this now standard CRAB configuration

from WMCore.Configuration import Configuration

config = config()

submitVersion ="2018"
doEleTree = 'doEleID=True'
doPhoTree = 'doPhoID=False'
doHLTTree = 'doTrigger=True'
calibEn   = 'calibEn=False'
#ERROR
#from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights
#ImportError: No module named regressionWeights_cfi

mainOutputDir = '/store/user/hyseo/EgammaTnP/%s' % submitVersion

config.General.transferLogs = False

config.JobType.pluginName  = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName  = 'python/TnPTreeProducer_cfg.py'
config.JobType.sendExternalFolder     = True

config.Data.inputDBS = 'global'
config.Data.publication = False
#config.Data.allowNonValidInputDataset = False
config.Data.allowNonValidInputDataset = True
#config.Data.publishDataName = 

config.Site.storageSite = 'T2_KR_KNU'


 
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
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=102X_upgrade2018_realistic_v19','isAOD=False']
    config.Data.splitting = 'FileBased'
    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8'
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.unitsPerJob = 4
    #submit(config)

    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'mc')
    config.JobType.pyCfgParams  = ['isMC=True',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=102X_upgrade2018_realistic_v19','isAOD=False']
    config.Data.splitting = 'FileBased'
    config.General.requestName  = 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8'
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v1/MINIAODSIM'
    config.Data.unitsPerJob = 4
    submit(config)

    ##### now submit DATA
    config.Data.outLFNDirBase = '%s/%s/' % (mainOutputDir,'data')
    config.Data.splitting     = 'LumiBased'
    config.Data.lumiMask      = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
    config.Data.unitsPerJob   = 100
    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=102X_dataRun2_v11','isAOD=False']
    config.Data.userInputFiles = []
 
    config.General.requestName  = 'Run2018A'
    config.Data.inputDataset    = '/EGamma/Run2018A-17Sep2018-v2/MINIAOD'
    #submit(config)    

    config.General.requestName  = 'Run2018B'
    config.Data.inputDataset    = '/EGamma/Run2018B-17Sep2018-v1/MINIAOD'
    #submit(config)    

    config.General.requestName  = 'Run2018C'
    config.Data.inputDataset    = '/EGamma/Run2018C-17Sep2018-v1/MINIAOD'
    #submit(config)    

    config.JobType.pyCfgParams  = ['isMC=False',doEleTree,doPhoTree,doHLTTree,calibEn,'GT=102X_dataRun2_Prompt_v14','isAOD=False']
    config.General.requestName  = 'Run2018D'
    config.Data.inputDataset    = '/EGamma/Run2018D-22Jan2019-v2/MINIAOD'
    #submit(config)    

