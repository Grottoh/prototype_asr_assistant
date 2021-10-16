import audio_processing as ap
import util
import os
import signal
import subprocess

def start_inference_process(VD, CD):
    
    """ Start an inference process if none is currently active. """
    
    if VD['inference_process'] == None:
        VD['terminal_output'] += "\nCreating inference process...\n"
        VD['window']['terminal_text'].update(VD['terminal_output'])
        event, values = VD['window'].read(timeout=0)
        ap.create_process(VD, CD)
        
        VD['terminal_output'] += "Created inference process.\n"
    else:
        VD['terminal_output']  += "An inference process is already active."
        
def test_inference(VD, CD):
    
    """ Test whether inference performs as expected. """
    
    if VD['inference_process'] == None:
        VD['terminal_output'] += "There is no active inference process.\n"
    else:
        VD['terminal_output'] += "\nTesting the inference process.\nOutput should be: \"let's test again then\".\n"
        ap.run_inference(CD['path_sample_audio'], VD, CD)
        VD['window']['inferred_text'].update(VD['temp_text'])


def kill_process(process):
    
    """ Kill the given process. """
    
    if process == None:
        print("No process to kill.")
        pass
    else:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process = None
        print("Process killed.")
    return None

def kill_inference_process(VD):
    
    """ Kill the inference process if one is active. """
    
    if VD['inference_process'] == None:
        VD['terminal_output'] += "There is no active inference process.\n"
    else:
        VD['inference_process'] = kill_process(VD['inference_process'])
        VD['terminal_output'] += "\nKilled inference process.\n"


def create_folders(CD):
    
    """ Create or clear the folders required for audio recording and inference. """
    
    path_recordings = CD['path_recordings']
    path_temp_recordings = CD['path_temp_recordings']
    
    # Create the recordings folder if it does not already exist
    if not os.path.isdir(path_recordings):
        os.mkdir(path_recordings)
    
    # Create the temporary audio files folder or clear it if it already exists
    if not os.path.isdir(path_temp_recordings):
        os.mkdir(path_temp_recordings)
    else:
        for f in os.listdir(path_temp_recordings):
            os.remove(path_temp_recordings+f)

def start_recording(VD, CD):
    
    """ Start recording audio and inferring text from the speech it contains. """
    
    if VD['inference_process'] == None:
        VD['terminal_output'] += "Cannot record and infer, no inference process is active.\n"
    else:
        create_folders(CD)
        VD['record_and_infer'] = True # Indicates that recording and inference is active
        VD['terminal_output'] += "\nRecording speech and inferring text ...\n"

def stop_recording(VD):
    
    """ Stop recording and inferring, reset a portion of the variables dictionary. """
    
    if VD['record_and_infer']:
        terminal_output = VD['terminal_output'] + "Stopped recording.\n\n"
        fixed_text = VD['fixed_text'] + " " + VD['temp_text'] + "\n\n"
        util.reset_variables_dict(VD, window=VD['window'], layout=VD['layout'], inference_process=VD['inference_process'],
                                  terminal_output=terminal_output, fixed_text=fixed_text)
    else:
        VD['terminal_output'] += "Not currently recording.\n"

    
def is_running(program):
    
    """ Returns True if the given program is currently running. """
    
    #cmd = ["xdotool", "search", "--name", program]
    cmd = ["xdotool", "search", "--name", "--class", "--classname", program]
    try:
        subprocess.check_output(cmd)
        return True
    except:
        return False

def start_program(program, program_name, VD):
    
    """ Starts the program with the given name if it is not already running. """
    
    if not is_running(program):
        VD['terminal_output'] += f"> Starting {program_name}.\n"
        subprocess.Popen([program])
        #subprocess.call(["xdotool", "search", "--name", "spotify", "")
    else:
        VD['terminal_output'] += f"> {program_name} is already running.\n"

def exit_program(program, program_name, VD):
    
    if is_running(program):
        VD['terminal_output'] += f"> Exiting {program_name}.\n"
        cmd = ["xdotool", "search", "--name", "--class", "--classname", program, "windowkill"]
        subprocess.Popen(cmd)
    else:
        VD['terminal_output'] += f"> {program_name} is not currently running.\n"

def execute_command(VD):
    
    """ Execute a given command (would be better to (at least) not try to match literal strings). """
    
    command = VD['command']
    print(f"command = {command}")
    
    if command == "cmd_inference_exit":
        VD['exit'] = True
    elif command == "cmd_inference_stop":
        stop_recording(VD)
    elif command == "cmd_inference_kill":
        kill_inference_process(VD)
        stop_recording(VD)
    elif command in VD['command_dict']:
        function, params = VD['command_dict'][command]
        function(*params)
    elif command == "cmd_clear_terminal":
        VD['terminal_output'] = ""
    elif command == "cmd_clear_all_text":
        VD['fixed_text'] = ""
    elif command == "cmd_inference_break":
        pass
    else:
        VD['terminal_output'] += f"Command <{command}> is not known.\n"
    
    VD['command'] = ""

def record_and_infer(VD, CD):
    if VD['command'] != "":
        execute_command(VD)
    else:
        ap.record_speech(VD, CD)





