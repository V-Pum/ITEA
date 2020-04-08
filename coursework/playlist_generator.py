import PySimpleGUIQt as sg
from pg_tools import pg_actions
from pg_tools import pg_ui
import random


def main():
    settings, files_list, missing_files = pg_actions.load_state()
    path = settings["path"]
    pl1, pl2, pl3, pl4, pl5 = settings["pl1"], settings["pl2"], settings["pl3"], settings["pl4"], settings["pl5"]
    if len(missing_files) > 0:
        sg.popup(f"{len(missing_files)} file(s) were removed from disk since last run")
    pl1, pl2, pl3, pl4, pl5 = pg_actions.remove_from_pls(missing_files, pl1, pl2, pl3, pl4, pl5)
    pl_dur = pg_actions.calculate_playlist_duration(files_list, pl1, pl2, pl3, pl4, pl5)
    src_dur = 0
    for key in files_list:
        src_dur += files_list[key][0]
    file_names = sorted(list(files_list.keys()))

    menu_def = [['&Edit', ['Remove Item', 'Move &UP', 'Move &DOWN']], ['&Help', '&About...'], ]

    all_files_layout = [
        [sg.Listbox(file_names, enable_events=False, key='-LIST-', size=(40, 22), select_mode="multiple")],
        [sg.Text(f"Total files duration: {src_dur//60} min. {src_dur-(src_dur//60)*60} sec.",
                 key="td")]
    ]

    add_tooltip = "Click to add selected tracks from left panel"
    rm_tooltip = "Click to remove track from this section of playlist"
    up_tooltip = "Click to move track up"
    down_tooltip = "Click to move track down"
    shuffle_tooltip = "Click to shuffle this section of playlist"

    butt_lo1 = [
        [sg.Button(">>", key="add1", tooltip=add_tooltip)],
        [sg.Button("X", key="rm1", tooltip=rm_tooltip)],
        [sg.Button("∧", key="up1", tooltip=up_tooltip)],
        [sg.Button("∨", key="dn1", tooltip=down_tooltip)],
        [sg.Button("Shuffle", key="sh1", tooltip=shuffle_tooltip)]
    ]
    butt_lo2 = [
        [sg.Button(">>", key="add2", tooltip=add_tooltip)],
        [sg.Button("X", key="rm2", tooltip=rm_tooltip)],
        [sg.Button("∧", key="up2", tooltip=up_tooltip)],
        [sg.Button("∨", key="dn2", tooltip=down_tooltip)],
        [sg.Button("Shuffle", key="sh2", tooltip=shuffle_tooltip)]
    ]
    butt_lo3 = [
        [sg.Button(">>", key="add3", tooltip=add_tooltip)],
        [sg.Button("X", key="rm3", tooltip=rm_tooltip)],
        [sg.Button("∧", key="up3", tooltip=up_tooltip)],
        [sg.Button("∨", key="dn3", tooltip=down_tooltip)],
        [sg.Button("Shuffle", key="sh3", tooltip=shuffle_tooltip)]
    ]
    butt_lo4 = [
        [sg.Button(">>", key="add4", tooltip=add_tooltip)],
        [sg.Button("X", key="rm4", tooltip=rm_tooltip)],
        [sg.Button("∧", key="up4", tooltip=up_tooltip)],
        [sg.Button("∨", key="dn4", tooltip=down_tooltip)],
        [sg.Button("Shuffle", key="sh4", tooltip=shuffle_tooltip)]
    ]
    butt_lo5 = [
        [sg.Button(">>", key="add5", tooltip=add_tooltip)],
        [sg.Button("X", key="rm5", tooltip=rm_tooltip)],
        [sg.Button("∧", key="up5", tooltip=up_tooltip)],
        [sg.Button("∨", key="dn5", tooltip=down_tooltip)],
        [sg.Button("Shuffle", key="sh5", tooltip=shuffle_tooltip)]
    ]

    playlists_layout = [
        [sg.Column(butt_lo1), sg.Listbox(pl1, key='pl1', size=(40, 4.38), select_mode="single")],
        [sg.Column(butt_lo2), sg.Listbox(pl2, key='pl2', size=(40, 4.38), select_mode="multiple")],
        [sg.Column(butt_lo3), sg.Listbox(pl3, key='pl3', size=(40, 4.38), select_mode="multiple")],
        [sg.Column(butt_lo4), sg.Listbox(pl4, key='pl4', size=(40, 4.38), select_mode="multiple")],
        [sg.Column(butt_lo5), sg.Listbox(pl5, key='pl5', size=(40, 4.38), select_mode="multiple")],
        [sg.Text(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.",
                 key="pld")]
    ]
    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
        [sg.Frame('All files', all_files_layout, font='Any 12', title_color='yellow', visible=True),
         sg.Frame('Create Playlist', playlists_layout, font='Any 12', title_color='yellow')],
        [sg.Button("Add Folder"), sg.Button("Add File"), sg.VerticalSeparator(pad=None), sg.Button("Delete Files"),
         sg.Button("Clear Playlist"), sg.VerticalSeparator(pad=None), sg.Button("Generate Playlist"), sg.Button("Exit")]
    ]

    window = sg.Window('Playlist creator v0.1', layout)
    while True:
        event, values = window.read()
        if event is None:
            break
        elif event == "Add Folder":
            src = pg_ui.open_folder_dialog("Select source folder", path)
            if not src:
                sg.popup("Source path cannot be empty")
                continue
            path1 = pg_ui.open_folder_dialog("Select destination folder", path)
            if not path1:
                sg.popup("Destination path cannot be empty")
                continue
            path = path1
            files_list = pg_actions.load_files_from_dir(src, path)
            file_names = sorted(list(files_list.keys()))
            src_dur = 0
            for key in files_list:
                src_dur += files_list[key][0]
            window['-LIST-'].update(file_names)
            window['td'].update(f"Total files duration: {src_dur // 60} min. {src_dur - (src_dur // 60) * 60} sec.")
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
        elif event == "Generate Playlist":
            pg_actions.create_playlist(pl1+pl2+pl3+pl4+pl5, path)
            sg.popup(f"{len(pl1+pl2+pl3+pl4+pl5)} files added to playlist.m3u at {path}")
        elif event == "Exit":
            exit()

        # Remove items from playlist sections:

        elif event == "rm1":
            track = values["pl1"][0]
            if track:
                pl1.remove(track)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            pl_dur -= files_list[track][0]
            window['pl1'].update(pl1)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")

        # Remove items to playlist sections:

        elif event == "add1":
            tracks = values['-LIST-']
            for track in tracks:
                pl1.append(track)
                pl_dur += files_list[track][0]
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl1'].update(pl1)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")
        elif event == "add2":
            tracks = values['-LIST-']
            for track in tracks:
                pl2.append(track)
                pl_dur += files_list[track][0]
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl2'].update(pl2)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")
        elif event == "add3":
            tracks = values['-LIST-']
            for track in tracks:
                pl3.append(track)
                pl_dur += files_list[track][0]
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl3'].update(pl3)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")
        elif event == "add4":
            tracks = values['-LIST-']
            for track in tracks:
                pl4.append(track)
                pl_dur += files_list[track][0]
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl4'].update(pl4)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")
        elif event == "add5":
            tracks = values['-LIST-']
            for track in tracks:
                pl5.append(track)
                pl_dur += files_list[track][0]
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl5'].update(pl5)
            window['pld'].update(f"Playlist duration: {pl_dur//60} min. {pl_dur-(pl_dur//60)*60} sec.")

        # Shuffle items in playlist sections:

        elif event == "sh1":
            random.shuffle(pl1)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl1'].update(pl1)
        elif event == "sh2":
            random.shuffle(pl2)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl2'].update(pl2)
        elif event == "sh3":
            random.shuffle(pl3)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl3'].update(pl3)
        elif event == "sh4":
            random.shuffle(pl4)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl4'].update(pl4)
        elif event == "sh5":
            random.shuffle(pl5)
            settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
            pg_actions.save_state(files_list, settings)
            window['pl5'].update(pl5)

        # Remove items from source section, optionally delete files:

        elif event == "Delete Files":
            tracks = values['-LIST-']
            decision = sg.popup_yes_no(f"Remove {len(tracks)} files from working list?")
            if decision == "Yes":
                pl1, pl2, pl3, pl4, pl5 = pg_actions.remove_from_pls(tracks, pl1, pl2, pl3, pl4, pl5)
                window['pl1'].update(pl1)
                window['pl2'].update(pl2)
                window['pl3'].update(pl3)
                window['pl4'].update(pl4)
                window['pl5'].update(pl5)
                pl_dur = pg_actions.calculate_playlist_duration(files_list, pl1, pl2, pl3, pl4, pl5)
                window['pld'].update(f"Playlist duration: {pl_dur // 60} min. {pl_dur - (pl_dur // 60) * 60} sec.")
                decision = sg.popup_yes_no(f"Delete files from disk? This cannot be undone!")
                if decision == "Yes":
                    files_list = pg_actions.delete_files(files_list, tracks, path, delete_file=True)
                else:
                    files_list = pg_actions.delete_files(files_list, tracks, delete_file=False)
                src_dur = 0
                for key in files_list:
                    src_dur += files_list[key][0]
                file_names = sorted(list(files_list.keys()))
                settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
                pg_actions.save_state(files_list, settings)
                window['-LIST-'].update(file_names)
                window['td'].update(f"Total files duration: {src_dur//60} min. {src_dur-(src_dur//60)*60} sec.")
            else:
                continue

        # Clear all playlist sections:

        elif event == "Clear Playlist":
            decision = sg.popup_yes_no("Are you sure you want to clear playlist?\nFiles will not be deleted")
            if decision == "Yes":
                pl1, pl2, pl3, pl4, pl5 = [], [], [], [], []
                settings = {"path": path, "pl1": pl1, "pl2": pl2, "pl3": pl3, "pl4": pl4, "pl5": pl5}
                pg_actions.save_state(files_list, settings)
                window['pl1'].update(pl1)
                window['pl2'].update(pl2)
                window['pl3'].update(pl3)
                window['pl4'].update(pl4)
                window['pl5'].update(pl5)
                pl_dur = pg_actions.calculate_playlist_duration(files_list, pl1, pl2, pl3, pl4, pl5)
                window['pld'].update(f"Playlist duration: {pl_dur // 60} min. {pl_dur - (pl_dur // 60) * 60} sec.")
            else:
                continue
    window.close()


if __name__ == '__main__':
    main()
