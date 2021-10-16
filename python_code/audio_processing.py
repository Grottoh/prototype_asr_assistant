import os

import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

from subprocess import Popen, PIPE
import subprocess

from pydub import AudioSegment

import soundfile as sf

import re

import sounddevice as sd


# =============================================================================
# Speech-to-Text Inference Functions
# =============================================================================

def interpret_text(text, VD, CD):
    
    """ Find commands in the given text. """
    
    def find_and_remove_command(commands, text):
        
        """ Look for a command in the text, if found remove it from the text. """
        
        def remove_command(command, text):
            match = re.search(f".+?(?={command})", text)
            if match:
                return match.group(0)
            return text
        
        for command in commands:
            if command in text:
                text = remove_command(command, text)
                return True, text
        return False, text
    
    # Look for commands in the text, if found remove it from the text
    for voice_commands, command in CD['command_list']:
        found_command, text = find_and_remove_command(voice_commands, text)
        if found_command:
            VD['command'] = command
            VD['reset_merge'] = True
            return text
    
    return text

def remove_log_text(text):
    
    """ Remove log information from the given string. """
    
    # The pattern basically searches for anything following ".cpp:[0-9]{1-4}] "
    pattern = "(?:(?<=\.cpp:[0-9]] )|(?<=\.cpp:[0-9][0-9]] )|(?<=\.cpp:[0-9][0-9][0-9]] )|(?<=\.cpp:[0-9][0-9][0-9][0-9]] )).+"
    match = re.search(pattern, text)
    return text if match == None else match.group(0)

def read_current_output(VD, CD):
    
    """ Handle the output of the given process. """
    
    while True:
        output = VD['inference_process'].stderr.readline()
        text = output.decode().strip()
        if not text == "":
            
            # Remove the log information from the text
            text = remove_log_text(text)
            #print(text)
            
            # If it concerns text inferred from speech ...
            if text[0:4] == ">>> ": 
                text = text[4:]
                
                text = interpret_text(text, VD, CD)
                VD['temp_text'] = text
                
                if VD['reset_merge']:
                    VD['fixed_text'] += text + " | "
                    VD['temp_text'] = ""
            
            # Else if looking for silence and it concerns tokens inferred from speech ...
            elif VD['look_for_silence'] and text[0:4] == "--> ": 
                text = text[4:]
                
                # If the silence if of sufficient length ...
                match = re.search("(#|\|)+$", text)
                if match != None:
                    pause_length = len(match.group(0))
                    CD['silence_threshold'] = 30
                    VD['reset_merge'] = pause_length >= CD['silence_threshold']
            
        if "Waiting the input in the format" in text:
            break

def create_process(VD, CD):
    
    """ Run an external process (such as a C++ script that infers text from speech) """
    
    process = Popen(CD['inference_cmd'],
                    stdin=PIPE, stdout=PIPE, stderr=PIPE,
                    shell=True, preexec_fn=os.setsid)
    VD['inference_process'] = process
    read_current_output(VD, CD)

def run_inference(audio_path, VD, CD):
    
    """ Infer text from speech given an audio file and an inference process. """
    
    VD['inference_process'].stdin.write("{}\n".format(audio_path).encode())
    VD['inference_process'].stdin.flush()
    read_current_output(VD, CD)

# =============================================================================
# Audio Recording and Merging Functions
# =============================================================================

def save_recording(recording, path_recordings, fnt_og_recording, fnt_recording, VD, fs=16000):
    
    """ Save the given recording and a version of it with a sample rate of 16000hz. """
    
    fn_og_recording = fnt_og_recording.format(VD['ith_rec'])
    fn_recording = fnt_recording.format(VD['ith_rec'])
    if fs == 16000: # If the original recording is was recorded at 16000hz ...
        sf.write(path_recordings+fn_recording, recording, fs)
    else: # Else create a copy with a sample rate of 16000hz ...
        sf.write(path_recordings+fn_og_recording, recording, fs)
        subprocess.call("find ./"+path_recordings+" -name \""+fn_og_recording+"\" -exec sox {} -r 16000 -b 16 -c 1 ./"+path_recordings+fn_recording+" \;", shell=True)

def merge_recordings(merged_recording, ith_rec, path_temp_recordings, fnt_recording, path_merged, recording_format="flac", n_merges=1):
    
    """ Merge N recordings into a single recording """
    
    for i in range(n_merges, 0, -1):
        rec_min_i = AudioSegment.from_file(path_temp_recordings+fnt_recording.format(ith_rec-i), format=recording_format)
        merged_recording = rec_min_i if merged_recording == None else merged_recording + rec_min_i
    merged_recording.export(path_merged, format=recording_format)
    
    return merged_recording

# =============================================================================
# Main Recording and Inference Function
# =============================================================================
import gui
def record_speech(VD, CD):
    
    """ The main function for the online recording and inference of speech. """

    def process_recording(rec, VD, CD):
        
        """ Save the given recording, check whether to look for silence or whether to merge, and do so if necessary. """
        
        save_recording(rec, CD['path_temp_recordings'], CD['fnt_og_recording'], CD['fnt_recording'], VD, CD['fs'])
        VD['ith_rec'] += 1
        
        # Merge recording 1
        VD['look_for_silence'] = (VD['ith_rec'] - VD['last_merge_reset']) % CD['max_n_merges'] > CD['min_n_merges']
        VD['reset_merge'] = (VD['ith_rec'] - VD['last_merge_reset']) % CD['max_n_merges'] == 0
        
        # Append the recording to the recordings merged so far
        VD['merged_recording'] = merge_recordings(VD['merged_recording'], VD['ith_rec'],
                         CD['path_temp_recordings'], CD['fnt_recording'], CD['path_merged'],
                         recording_format=CD['recording_format'])
        
        # Infer text from the speech in the merged recordings
        run_inference(CD['path_merged'], VD, CD)
        
        if VD['reset_merge']:
            #gui.add_save_option(VD)
            print("RESETTING")
            os.rename(CD['path_merged'], CD['path_merged'][:-5]+f"_{VD['ith_merge_reset']:02d}.flac")
            VD['ith_merge_reset'] += 1
            
            # Sometimes the end of an audiofile is mistakenly seen as a silence, so append the final bit (which is either silence, or speech to be included in next merge)
            merge_overlap = CD['merge_overlap'] if VD["command"] == "" else 0
            VD['merged_recording'] = VD['merged_recording'][len(VD['merged_recording'])-merge_overlap:]
            
            VD['last_merge_reset'] = VD['ith_rec']
            VD['reset_merge'] = VD['look_for_silence'] = False
    
    # Start recording 0
    VD['rec0'] = sd.rec(int(CD['fragment_duration'] * CD['fs']), samplerate=CD['fs'], channels=1)
    
    # If beyond first iteration: handle recording 1
    if VD['ith_rec'] > 0:
        process_recording(VD['rec1'], VD, CD)
        
        VD['window']['inferred_text'].update(VD['fixed_text'] + " " + VD['temp_text'])
    
    # Wait for recording 0 to finish
    sd.wait()
    
    # Start recording 1
    VD['rec1'] = sd.rec(int(CD['fragment_duration'] * CD['fs']), samplerate=CD['fs'], channels=1)
    
    # Handle recording 0
    process_recording(VD['rec0'], VD, CD)
    
    VD['window']['inferred_text'].update(VD['fixed_text'] + " " + VD['temp_text'])

    # Wait for recording 1 to finish
    sd.wait()