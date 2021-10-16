import PySimpleGUI as sg

def get_window():
    
    sg.ChangeLookAndFeel('GreenTan')   
    column_buttons = [ 
        [sg.Button("Start Process")],
        [sg.Button("Test Inference Process")],
        [sg.Button("Kill Inference Process")],
         [sg.Button("Start Recording Speech")],
         [sg.Button("Stop Recording Speech")]
        ]
    
    terminal_text = sg.Multiline("Initialized Inferred Text.", size=(40, 40), font=('Arial', 12), background_color="#000000", text_color="#AAAAAA", 
                                 autoscroll=True, justification='left',
                                 key='terminal_text')
    #column_terminal_text = [[terminal_text]]
    
    inferred_text = sg.Multiline("Initialized Inferred Text.", size=(40, 40), font=('Arial', 12), background_color="#000000", text_color="#AAAAAA", 
                                 autoscroll=True, justification='left',
                                 key='inferred_text')
    #column_inferred_text = [[inferred_text]]
    
    
    def get_save_option(text, i):
        file_text = sg.Multiline(text, size=(50, 10), font=('Arial', 12), justification='left', key=f'file_text_{i:04d}')
        save_option = [file_text, sg.Column([[sg.Button("Play")], [sg.Button("Save")], [sg.Button("Delete")]])]
        return save_option
    
    
    so = []
    so.append(get_save_option("...",
              0))
    so.append(get_save_option("text text tuext",
              1))
    
    layout = [
    

            [
                sg.Column(column_buttons),
                sg.VSeperator(),
                terminal_text,
                sg.VSeperator(),
                inferred_text,
                sg.VSeperator(),
                sg.Column(so, size=(500,800), scrollable=True, vertical_scroll_only=True)
            ]
    ]
    
    window = sg.Window("Voice Assistant", layout)
    
    return window, layout

def add_save_option(VD):
    print("ADD SAVE OPTION")
    window = VD['window']
    text = VD['fixed_text']
    layout = VD['layout']
    file_text = sg.Multiline(text, size=(50, 10), font=('Arial', 12), justification='left', key='file_text')
    save_option = [file_text, sg.Column([[sg.Button("Play")], [sg.Button("Save")], [sg.Button("Delete")]])]
    layout[0][-1].add_row(save_option)
    #layout[0][-1] = sg.Column([save_option], size=(500,800), scrollable=True, vertical_scroll_only=True)
    
    
    
    window.Layout(layout)