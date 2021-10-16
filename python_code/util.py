import actions
    
def reset_constants_dict(constants_dict):
    
    inference_cmd = """../build/InferenceCTC \
          --am_path=../../inference_tutorial/am_transformer_ctc_stride3_letters_300Mparams.bin \
          --tokens_path=../../inference_tutorial/tokens.txt \
          --lexicon_path=../../inference_tutorial/lexicon.txt \
          --lm_path=../../inference_tutorial/lm_common_crawl_small_4gram_prun0-6-15_200kvocab.bin \
          --logtostderr=true \
          --sample_rate=16000 \
          --beam_size=50 \
          --beam_size_token=30 \
          --beam_threshold=100 \
          --lm_weight=1.5 \
          --word_score=0"""
    constants_dict["inference_cmd"] = inference_cmd
    
    fs = 16000
    constants_dict["fs"] = fs
    
    fragment_duration = 0.5
    constants_dict["fragment_duration"] = fragment_duration
        
    path_recordings = "../recordings/"
    constants_dict["path_recordings"] = path_recordings
    
    path_temp_recordings = path_recordings + "temp/"
    constants_dict["path_temp_recordings"] = path_temp_recordings
    
    fnt_og_recording = "recording_OG_{:04d}.flac"
    constants_dict["fnt_og_recording"] = fnt_og_recording
    
    fnt_recording = "recording_{:04d}.flac"
    constants_dict["fnt_recording"] = fnt_recording
    
    path_merged = path_temp_recordings+"merged_audio.flac"
    constants_dict["path_merged"] = path_merged
    
    recording_format = "flac";
    constants_dict["recording_format"] = recording_format
    
    min_n_merges = int(20/fragment_duration) # Minimal amount of merges after which it starts looking for a silence to reset the merge
    constants_dict["min_n_merges"] = min_n_merges
    
    max_n_merges = int(32/fragment_duration) # Maximal amount of merges, when reached it always resets the merge
    constants_dict["max_n_merges"] = max_n_merges
    
    silence_threshold = 30
    constants_dict['silence_threshold'] = silence_threshold
    
    path_sample_audio = "../sample_audio.flac"
    constants_dict['path_sample_audio'] = path_sample_audio
    
    merge_overlap = 700
    constants_dict['merge_overlap'] = merge_overlap
    
    command_list = [(['stop inference', 'sub inference'], "cmd_inference_stop"),
                    (['kill inference', 'gill inference'], "cmd_inference_kill"),
                    (['exit inference'], "cmd_inference_exit"), 
                    (['start spotify', 'starts spotify'], "cmd_spotify_start"),
                    (['exit spotify', 'exits spotify'], "cmd_spotify_exit"),
                    (['start system monitor', 'starts system monitor'], "cmd_system_monitor_start"),
                    (['exit system monitor', 'exits system monitor'], "cmd_system_monitor_exit"),
                    (['clear terminal'], "cmd_clear_terminal"),
                    (['clear all text', 'clear old text'], "cmd_clear_all_text"),
                    (['inference break', 'inference brake'], "cmd_inference_break")]
    constants_dict['command_list'] = command_list
    

def reset_variables_dict(variables_dict, window, layout, inference_process=None,
                         terminal_output="", fixed_text=""):
    
    variables_dict['window'] = window
    variables_dict['inference_process'] = inference_process
    variables_dict['terminal_output'] = terminal_output
    
    variables_dict['record_and_infer'] = False
    
    variables_dict['rec0'] = None
    variables_dict['rec1'] = None
    variables_dict['merged_recording'] = None
    variables_dict['ith_rec'] = 0
    variables_dict['last_merge_reset'] = 0
    variables_dict['ith_merge_reset'] = 0
    variables_dict['look_for_silence'] = False
    
    variables_dict['fixed_text'] = fixed_text
    variables_dict['temp_text'] = ""
    variables_dict['reset_merge'] = False
    variables_dict['command'] = ""
    
    variables_dict['exit'] = False
    
    # Should find another place for this dict I think
    variables_dict['command_dict'] = dict()
    variables_dict['command_dict']['cmd_spotify_start'] = (actions.start_program, ["spotify", "Spotify", variables_dict])
    variables_dict['command_dict']['cmd_spotify_exit']  = ( actions.exit_program, ["spotify", "Spotify", variables_dict])
    variables_dict['command_dict']['cmd_system_monitor_start'] = (actions.start_program, ["gnome-system-monitor", "System Monitor", variables_dict])
    variables_dict['command_dict']['cmd_system_monitor_exit']  = ( actions.exit_program, ["gnome-system-monitor", "System Monitor", variables_dict])
    
    variables_dict['layout'] = layout