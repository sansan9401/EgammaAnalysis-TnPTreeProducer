from ROOT import TFile, TTree
from array import array
from os import listdir
from os.path import isfile, join
import sys
import math

fIn = TFile("%s" %(sys.argv[1]))
tree = fIn.Get("tnpEleTrig/fitter_tree")

v_el_et = array('f',[0])
v_el_sc_eta = array('f',[0])
v_run = array('i',[0])
v_pass = array('i',[0])

#Only activate the needed branches
tree.SetBranchStatus("*",0)
tree.SetBranchStatus("el_et",1)
tree.SetBranchStatus("el_sc_eta",1)
tree.SetBranchStatus("run",1)
tree.SetBranchStatus("passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match",1)
#Set branch address to the local variables
tree.SetBranchAddress("el_et",v_el_et)
tree.SetBranchAddress("el_sc_eta",v_el_sc_eta)
tree.SetBranchAddress("run",v_run)
tree.SetBranchAddress("passHltEle23Ele12CaloIdLTrackIdLIsoVLLeg1L1match",v_pass)

json_dir = "../crab/prescaleInformation/%s/HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL/" %(sys.argv[2])
onlyfiles = [f for f in listdir(json_dir) if (isfile(join(json_dir, f)) and f.endswith(".json"))]

print onlyfiles

def countBadEvents():

    totEvents = 0
    badEvents = 0
    badEventsBarrel = 0

    for entry in xrange(tree.GetEntriesFast()):
        tree.GetEntry(entry)

        if v_pass[0] == 0: continue
        ref_energy = -9999.
        totEvents += 1
        ref_energy_found = False
        for f in onlyfiles:
            with open(json_dir + f, 'r') as searchfile:
                for line in searchfile:
                    if str(v_run[0]) in line: 
                        ref_energy = f.split("_")[2]
                        if "LooseIso" in ref_energy: 
                            ref_energy = ref_energy.replace("LooseIso","")
                        ref_energy_found = True
                        break
            if ref_energy_found: break

        if float(ref_energy) < 0.:
            raise Exception ("The reference energy from json was not properly retrieved!")
        else:
            if v_el_et[0] < float(ref_energy):
                #print "Reco Et --" + str(v_el_et[0]) + "-- is smaller than the L1 leg1 threshold"  
                badEvents += 1
                if math.fabs(v_el_sc_eta[0]) < 2.:
                    badEventsBarrel += 1

    print "There are " + str(round(badEvents*100./totEvents,2)) + "% events with reco Et smaller than L1 leg1 threshold -- " + str(round(badEventsBarrel*100./badEvents,2)) + "% of which are in the barrel"
    print "totEvents: ", totEvents, "   badEvents: ", badEvents


def makeFractions():

    totEvents = 0.
    threshold_list = [t.split("_")[2] for t in onlyfiles]
    #print threshold_list
    threshold_events = dict()
    for t in threshold_list:
        threshold_events[t] = 0.
    print threshold_events

    for entry in xrange(tree.GetEntriesFast()):
        tree.GetEntry(entry)

        #if v_pass[0] == 0: continue
        ref_energy = "None"
        totEvents += 1
        ref_energy_found = False
        for f in onlyfiles:
            with open(json_dir + f, 'r') as searchfile:
                for line in searchfile:
                    if str(v_run[0]) in line: 
                        ref_energy = f.split("_")[2]
                        if "LooseIso" in ref_energy: 
                            ref_energy = ref_energy.replace("LooseIso","")                
                        ref_energy_found = True
                        break
            if ref_energy_found: break

        if ref_energy == "None":
            print "Run:",v_run[0] 
            raise Exception ("The reference energy from json was not properly retrieved!")
        else:        
            #print ref_energy
            threshold_events[ref_energy] += 1

    print
    print "totEvents:", totEvents
    print "Fraction of events per each leg1 threshold\n"
    for entry in threshold_events:
        print entry, ": ", round(threshold_events[entry]/totEvents,4)," -- there are", threshold_events[entry], " with this threshold\n"
        


if __name__=="__main__":
    #countBadEvents()
    makeFractions()
