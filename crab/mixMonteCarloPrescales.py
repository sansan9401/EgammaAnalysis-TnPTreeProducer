#!/usr/bin/env python

import ROOT, glob, os

#
# System command
#
import subprocess
def system(command):
  return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)


#
# Write mixed output tree based on dyDir, inputTreeDir and fractions
#
def mix(target, inputs, inputTreeDir, fractions):
  assert abs(sum(fractions.values())-1.) < 0.001, 'Fractions do not sum up to 1!'

  inputData = []
  for input in inputs:
    inputFile    = ROOT.TFile(input)
    inputTree    = inputFile.Get('%s/fitter_tree' % inputTreeDir)
    totalEntries = inputTree.GetEntries()
    threshold    = input.split('_leg1Threshold')[-1].split('.root')[0]
    inputData.append((totalEntries, threshold, fractions[threshold], inputTree, inputFile))

  inputData.sort(key=lambda x: x[2]) # Sort by increasing value of the fraction

  totalEntries = inputData[-1][0]
  print "inputData: ", inputData

  # The idea of the variable "events" is to check whether the event that is being added to the output tree for a given threshold was already there
  # (after selecting events for each threshold, they total number of events will have to be identical to that of any of the _leg1Threshold rootfiles).
  # Therefore, if the first threshold to be processed corresponds to a large fraction, the events in the file corresponding to the following threshold will have to be
  # checked for duplicates against a large number of events in the previous rootfile (these have been added to the variable "events). And so on for the following files/thresholds.
  # So, it makes sense to have the thresholds to be processed in increasing magnitude of fractions.
  events = set() 
  filesToMerge = ''
  k = 0
  for _,threshold,_,inputTree,_ in inputData:
    toCopy        = int(totalEntries*fractions[threshold])
    outFile       = ROOT.TFile(target.replace('.root', '_%s.root' % threshold), 'RECREATE')
    filesToMerge += target.replace('.root', '_%s.root' % threshold) + ' '
    outFileDir    = outFile.mkdir(inputTreeDir)
    outFile.cd()
    outFileDir.cd()

    print 'Saving %s entries from %s for threshold %s' % (toCopy, totalEntries, threshold)
    outTree = inputTree.CloneTree(0)
    i, j = 0, 0
    while j < toCopy and i < totalEntries:
      inputTree.GetEntry(i)
      i+=1
      if (inputTree.event, inputTree.el_pt) in events: 
        k += 1
        continue # Check if this event was not yet written (and also the pt because you have sometime two entries for one pair)

      events.add((inputTree.event, inputTree.el_pt))
      j+=1
      outTree.Fill()
      if j%100000==0:
        print 'Event %d written' % j
        #outTree.AutoSave()
    #outTree.AutoSave()
    outFile.Close()
    print "Duplicates found so far:", k

  print system('hadd -f %s %s;rm %s' % (target, filesToMerge, filesToMerge)) # merge and delete the temporary outfiles

#
# Main script
#
submitVersion='2021-02-10'
VFP = 'postVFP'
order = 'LO'
#allFilesPerThreshold = glob.glob('/eos/cms/store/group/phys_egamma/tnpTuples/*/%s/*/merged/DY*.root' % submitVersion)
#allFilesPerThreshold = glob.glob('/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/%s/UL2016%s/mc/DYJetsToLL_M-50_TuneCP5_13TeV-%s-pythia8/*/*/*/TnPTree_mc*.root' % (submitVersion, VFP, generator))
allFilesPerThreshold = glob.glob('/eos/cms/store/group/phys_egamma/tnpTuples/rsalvati/%s/UL2016%s/%s/merged/DY*.root' %(submitVersion, VFP, order))
allFilesBase         = set(f.split('_leg1Threshold')[0] for f in allFilesPerThreshold)

for base in allFilesBase:
  filesToMix = [f for f in allFilesPerThreshold if (base + '_leg1Threshold') in f]
  target     = base+'_L1matched.root'
  print 'Mixing for %s using\n  %s' % (target, '\n  '.join(filesToMix))

  if   '2016preVFP'  in base: fractions = {'15': 0.4695, '18': 0.4900, '23': 0.0405, '24': 0.0000}
  elif '2016postVFP' in base: fractions = {'15': 0.3820, '18': 0.2490, '23': 0.3591, '24': 0.0099}
  elif '2017' in base: fractions = {'18': 0.0018, '22': 0.7959, '24': 0.0870, '25': 0.1153}
  elif '2018' in base: fractions = {'22': 0.9119, '25': 0.0881}

  try:
    mix(target, filesToMix, 'tnpEleTrig', fractions) 
  except Exception as e:
    print(e)
