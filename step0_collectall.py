from step1_webscrap import webScrap
from step2_update_raw import updateRaw
from step3a_matlab_batch import matlabBatch
from step3b_eviewsbatch import eviewsbatch
from step4a_matlab_result_update import matlabUpdateMain
from step4b_eviewssep import eViewMerge
from step5_resultmerge_update import resultMerger
from step6a_indexplotly import callPlotly
from step6b_rawplot import callInfoPlot
from step7_overwriting import overwriting
#from step8_gitpush import gitpush

def main():
    1/0
    webScrap()
    updateRaw()
    matlabBatch()
    eviewsbatch()
    matlabUpdateMain()
    eViewMerge()
    resultMerger()
    callPlotly()
    callInfoPlot()
    overwriting()
    #gitpush()

if __name__ == '__main__':
    main()