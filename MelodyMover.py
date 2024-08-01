import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, Pango
import os
import shutil
import mutagen
import subprocess
import threading
import time
import re

SUPPORTED_FORMATS = ('.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma', '.opus')

class MelodyMoverApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="MelodyMover")
        self.set_default_size(600, 500)
        self.set_border_width(10)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_box)

        # Manual search button
        self.manual_search_button = Gtk.Button(label="Manual Folder Search")
        self.manual_search_button.connect("clicked", self.on_manual_search_clicked)
        self.main_box.pack_start(self.manual_search_button, False, False, 0)

        # Drag and Drop area
        self.drop_area = Gtk.Label(label="Drag and drop album folders here")
        self.drop_area.set_size_request(-1, 80)
        self.main_box.pack_start(self.drop_area, False, False, 0)

        # Enable drag and drop
        self.drop_area.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.drop_area.connect("drag-data-received", self.on_drag_data_received)
        self.drop_area.drag_dest_add_uri_targets()

        # Scrolled window for the list of folders
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.main_box.pack_start(scrolled_window, True, True, 0)

        # List store and view for dragged folders
        self.list_store = Gtk.ListStore(str, str, str)  # Folder path, Status, New Name
        self.tree_view = Gtk.TreeView(model=self.list_store)
        scrolled_window.add(self.tree_view)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Folder", renderer, text=0)
        self.tree_view.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Status", renderer, text=1)
        self.tree_view.append_column(column)

        renderer = Gtk.CellRendererText(editable=True)
        renderer.connect("edited", self.on_folder_name_edited)
        column = Gtk.TreeViewColumn("New Name", renderer, text=2)
        self.tree_view.append_column(column)

        # Right-click menu for deleting folders
        self.tree_view.connect("button-press-event", self.on_button_press)
        self.tree_view.connect("key-press-event", self.on_key_press)

        # Delete button
        delete_button = Gtk.Button(label="Delete Selected")
        delete_button.connect("clicked", self.on_delete_clicked)
        self.main_box.pack_start(delete_button, False, False, 0)

        # Destination folder chooser
        self.dest_folder_button = Gtk.Button(label="Choose Destination Folder")
        self.dest_folder_button.connect("clicked", self.on_folder_clicked)
        self.main_box.pack_start(self.dest_folder_button, False, False, 0)

        # Metadata editing
        metadata_frame = Gtk.Frame(label="Metadata")
        self.main_box.pack_start(metadata_frame, False, False, 0)
        metadata_grid = Gtk.Grid()
        metadata_frame.add(metadata_grid)

        self.metadata_fields = {}
        for i, field in enumerate(['artist', 'album', 'year', 'genre']):
            label = Gtk.Label(label=field.capitalize())
            entry = Gtk.Entry()
            metadata_grid.attach(label, 0, i, 1, 1)
            metadata_grid.attach(entry, 1, i, 1, 1)
            self.metadata_fields[field] = entry

        # Transcode options
        transcode_frame = Gtk.Frame(label="Transcode Options")
        self.main_box.pack_start(transcode_frame, False, False, 0)
        transcode_grid = Gtk.Grid()
        transcode_frame.add(transcode_grid)

        self.transcode_check = Gtk.CheckButton(label="Transcode files")
        transcode_grid.attach(self.transcode_check, 0, 0, 2, 1)

        formats = ["mp3", "wav", "ogg", "flac", "aac", "opus"]
        self.format_combo = Gtk.ComboBoxText()
        for fmt in formats:
            self.format_combo.append_text(fmt)
        self.format_combo.set_active(0)
        transcode_grid.attach(Gtk.Label(label="Format:"), 0, 1, 1, 1)
        transcode_grid.attach(self.format_combo, 1, 1, 1, 1)

        bitrates = ["128", "192", "256", "320"]
        self.bitrate_combo = Gtk.ComboBoxText()
        for rate in bitrates:
            self.bitrate_combo.append_text(rate)
        self.bitrate_combo.set_active(3)  # Default to 320
        transcode_grid.attach(Gtk.Label(label="Bitrate (kbps):"), 0, 2, 1, 1)
        transcode_grid.attach(self.bitrate_combo, 1, 2, 1, 1)

        sample_rates = ["44100", "48000", "96000"]
        self.sample_rate_combo = Gtk.ComboBoxText()
        for rate in sample_rates:
            self.sample_rate_combo.append_text(rate)
        self.sample_rate_combo.set_active(0)  # Default to 44100
        transcode_grid.attach(Gtk.Label(label="Sample Rate (Hz):"), 0, 3, 1, 1)
        transcode_grid.attach(self.sample_rate_combo, 1, 3, 1, 1)

        self.threads_spin = Gtk.SpinButton()
        self.threads_spin.set_range(1, os.cpu_count())
        self.threads_spin.set_value(max(1, os.cpu_count() - 1))
        transcode_grid.attach(Gtk.Label(label="Threads:"), 0, 4, 1, 1)
        transcode_grid.attach(self.threads_spin, 1, 4, 1, 1)

        threads_help = Gtk.Label(label="(?)")
        threads_help.set_tooltip_text("Number of CPU threads to use for transcoding. Higher values may speed up the process but use more system resources. Default is number of CPU cores minus one.")
        transcode_grid.attach(threads_help, 2, 4, 1, 1)

        # Process button
        self.process_button = Gtk.Button(label="Process")
        self.process_button.connect("clicked", self.on_process_clicked)
        self.main_box.pack_start(self.process_button, False, False, 0)

        # Overall progress bar
        self.overall_progress = Gtk.ProgressBar()
        self.main_box.pack_start(self.overall_progress, False, False, 0)

        # Current file progress bar
        self.file_progress = Gtk.ProgressBar()
        self.main_box.pack_start(self.file_progress, False, False, 0)

        self.dest_folder = None
        self.album_folders = []

    def on_manual_search_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder to organize",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folder_path = dialog.get_filename()
            if folder_path not in [row[0] for row in self.list_store]:
                self.list_store.append([folder_path, "Pending", os.path.basename(folder_path)])
            self.update_drop_area_text()
        dialog.destroy()

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        uris = data.get_uris()
        for uri in uris:
            path = GLib.filename_from_uri(uri)[0]
            if os.path.isdir(path) and path not in [row[0] for row in self.list_store]:
                self.list_store.append([path, "Pending", os.path.basename(path)])
        self.update_drop_area_text()

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a destination folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.dest_folder = dialog.get_filename()
            self.dest_folder_button.set_label(f"Destination: {self.dest_folder}")
        dialog.destroy()

    def on_folder_name_edited(self, widget, path, text):
        self.list_store[path][2] = text

    def on_button_press(self, treeview, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            path = treeview.get_path_at_pos(int(event.x), int(event.y))
            if path is not None:
                treeview.set_cursor(path[0])
                self.show_context_menu(event)
            return True

    def on_key_press(self, treeview, event):
        if Gdk.keyval_name(event.keyval) == 'Delete':
            self.delete_selected_folder()
            return True

    def on_delete_clicked(self, button):
        self.delete_selected_folder()

    def show_context_menu(self, event):
        menu = Gtk.Menu()
        delete_item = Gtk.MenuItem(label="Delete")
        delete_item.connect("activate", self.on_delete_menu_item)
        menu.append(delete_item)
        menu.show_all()
        menu.popup(None, None, None, None, event.button, event.time)

    def on_delete_menu_item(self, widget):
        self.delete_selected_folder()

    def delete_selected_folder(self):
        selection = self.tree_view.get_selection()
        model, iter = selection.get_selected()
        if iter:
            model.remove(iter)
            self.update_drop_area_text()

    def on_process_clicked(self, widget):
        if not self.dest_folder or len(self.list_store) == 0:
            self.show_error_dialog("Please select a destination folder and add album folders.")
            return

        # Validate year input
        year = self.metadata_fields['year'].get_text()
        if year and not re.match(r'^\d{4}$', year):
            self.show_error_dialog("Invalid year format. Please enter a 4-digit year or leave it blank.")
            return

        self.process_button.set_sensitive(False)
        threading.Thread(target=self.process_albums, daemon=True).start()

    def process_albums(self):
        total_albums = len(self.list_store)
        for i, row in enumerate(self.list_store):
            album_folder, _, new_name = row
            GLib.idle_add(self.update_status, album_folder, "Processing")
            try:
                self.process_album(album_folder, new_name)
                GLib.idle_add(self.update_status, album_folder, "Completed")
            except Exception as e:
                GLib.idle_add(self.update_status, album_folder, f"Error: {str(e)}")
            GLib.idle_add(self.overall_progress.set_fraction, (i + 1) / total_albums)

        GLib.idle_add(self.process_complete)

    def process_album(self, album_folder, new_name):
        dest_album_folder = os.path.join(self.dest_folder, new_name)
        os.makedirs(dest_album_folder, exist_ok=True)

        for root, _, files in os.walk(album_folder):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, album_folder)
                dest_path = os.path.join(dest_album_folder, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                if file.lower().endswith(SUPPORTED_FORMATS):
                    if self.transcode_check.get_active():
                        dest_format = self.format_combo.get_active_text()
                        dest_path = os.path.splitext(dest_path)[0] + '.' + dest_format
                        self.transcode_file(src_path, dest_path)
                    else:
                        shutil.copy2(src_path, dest_path)
                    self.update_metadata(dest_path)
                else:
                    shutil.copy2(src_path, dest_path)

        if album_folder != self.dest_folder:
            shutil.rmtree(album_folder)

    def transcode_file(self, src_path, dest_path):
        format = self.format_combo.get_active_text()
        bitrate = self.bitrate_combo.get_active_text()
        sample_rate = self.sample_rate_combo.get_active_text()
        threads = self.threads_spin.get_value_as_int()

        command = [
            'ffmpeg', '-i', src_path,
            '-acodec', self.get_codec(format),
            '-ar', sample_rate,
            '-b:a', f'{bitrate}k',
            '-threads', str(threads),
            dest_path
        ]
        subprocess.run(command, check=True)

    def get_codec(self, format):
        codecs = {
            'mp3': 'libmp3lame',
            'wav': 'pcm_s16le',
            'ogg': 'libvorbis',
            'flac': 'flac',
            'aac': 'aac',
            'opus': 'libopus'
        }
        return codecs.get(format, 'copy')

    def update_metadata(self, file_path):
        audio = mutagen.File(file_path, easy=True)
        if audio:
            for field, entry in self.metadata_fields.items():
                value = entry.get_text()
                if value:
                    audio[field] = value
            audio.save()

    def update_drop_area_text(self):
        count = len(self.list_store)
        self.drop_area.set_text(f"{count} album folder{'s' if count != 1 else ''} selected")

    def update_status(self, album_folder, status):
        for row in self.list_store:
            if row[0] == album_folder:
                row[1] = status
                break

    def process_complete(self):
        self.process_button.set_sensitive(True)
        self.show_info_dialog("Processing complete!")
        self.overall_progress.set_fraction(0)
        self.file_progress.set_fraction(0)

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

    def show_info_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

win = MelodyMoverApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()



###################################################
### last touches or future updates:
##  please make it so both Transcode and Metadata fields appear next to each other; also some responsiveness to window tiling managers so u can still see all the buttons and info, make an option to get read of certain files like .nfo .cue .m3u, option to clean the list, if its possible to make the whole area of the app as possible drop spot then we can reduce the message area to just one line 
