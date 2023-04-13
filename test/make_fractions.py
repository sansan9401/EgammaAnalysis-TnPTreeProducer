from ROOT import TFile
from os import listdir
from sys import argv

tName = "tnpEleTrig/fitter_tree"
#theDir = "/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016postVFP/data/SingleElectron/"
theDir = "/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016preVFP/data/SingleElectron/"
leg1List = [l for l in listdir(theDir)]
leg1Dict = dict()
threshDict = dict()

#listDir = ["/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016postVFP/data/SingleElectron/","/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016preVFP/data/SingleElectron/"]

for l in leg1List:
    print l
    leg1Dict[l] = 0.
    threshDict[l.split("_")[-1].replace("leg1Threshold","")] = 0.

    subDir = listdir(theDir + l)
    subSubDir = listdir(theDir + l + "/" + subDir[0])
    finalDir = theDir + l + "/" + subDir[0] + "/" + subSubDir[0] + "/"


    for t in listdir(finalDir):
        if t.endswith(".root"):
            fIn = TFile(finalDir+t)
            tIn = fIn.Get(tName)
            leg1Dict[l] += tIn.GetEntriesFast()


totEvts = 0.

for e in leg1Dict:    
    totEvts += leg1Dict[e]
    threshDict[e.split("_")[-1].replace("leg1Threshold","")] += leg1Dict[e]

print
with open("fractions_2016preVFP.txt","w") as fOut:
    for g in threshDict:
        fOut.write("totEvts: " + str(totEvts) + "\n")
        fOut.write("tot" + g + ": " + str(threshDict[g]) + "\n")
        threshDict[g] /= totEvts
        print g + ":", round(threshDict[g],4)
        print
        fOut.write(g + ": " + str(round(threshDict[g],4)) + "\n")

