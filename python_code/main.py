# mkdir older_versions/vXXX && mcp \*.py older_versions/vXXX/\#1.py && mcp \*.py older_versions/vXXX/\#1.txt

import PySimpleGUI as sg
import sys
import gui
import util
import actions

event = terminal_output = ""

window, layout = gui.get_window()

CD = dict()
VD = dict()
util.reset_constants_dict(CD)
util.reset_variables_dict(VD, window=window, layout=layout, inference_process=None)

try:
    
    event, values = window.read(timeout=10)
    #actions.start_inference_process(VD, CD)
    
    while True:
        
        event, values = window.read(timeout=10)
        
        if event == sg.WIN_CLOSED or VD['exit'] == True:
            print("Exiting.")
            break
        elif event == "Stop Recording Speech":
            actions.stop_recording(VD)
        elif VD['record_and_infer']:
            actions.record_and_infer(VD, CD)
        elif event == "Start Process":
            actions.start_inference_process(VD, CD)
        elif event == "Test Inference Process":
            actions.test_inference(VD, CD)
        elif event == "Kill Inference Process":
            actions.kill_inference_process(VD)
        elif event == "Start Recording Speech":
            actions.start_recording(VD, CD)
        elif event == "Stop Recording Speech":
            VD['terminal_output'] += "Not currently recording.\n"
        
        window['terminal_text'].update(VD['terminal_output'])
    
    # Kill the inference process
    actions.kill_inference_process(VD)
    window.close()
    
except:
    print("\nCatching error ...")
    actions.kill_inference_process(VD)
    
    window.close()
    print("Closed window.")
    
    print("\nUnexpected error:", sys.exc_info()[0])
    raise