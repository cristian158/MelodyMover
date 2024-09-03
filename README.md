# MelodyMover
### music organizer (and transcoder)

Version: 1.0.0

## Description

MelodyMover is a powerful and user-friendly desktop application designed to simplify the process of organizing and managing music collections. It provides an intuitive interface for batch processing audio files, including folder reorganization, metadata editing, and audio transcoding.

## Features

- Drag-and-drop interface for adding music folders
- Batch metadata editing (artist, album, year, genre)
- Audio file transcoding with customizable settings (format, bitrate, sample rate)
- Option to remove unwanted file types (.nfo, .cue, .m3u, etc.)
- Progress tracking for batch operations
- Cross-platform compatibility (Linux, macOS, Windows)

## Purpose and Goals

The primary goals of MelodyMover are:

1. To streamline the organization of large music libraries
2. To provide an easy-to-use interface for batch metadata editing
3. To offer flexible audio transcoding options for various needs
4. To reduce the time and effort required in managing music collections

MelodyMover aims to be a comprehensive solution for both casual music listeners and audiophiles who need to maintain large, well-organized music libraries.

## Why Python?

We chose Python for developing MelodyMover due to several factors:

1. Rapid development: Python's simplicity and extensive library ecosystem allowed for quick prototyping and iteration.
2. Cross-platform compatibility: Python applications can run on various operating systems with minimal modifications.
3. Rich audio processing libraries: Libraries like mutagen provide robust support for handling audio metadata.
4. GTK bindings: PyGObject offers a straightforward way to create GTK-based graphical user interfaces.
5. Large community and support: Python's vast community ensures good documentation and support for various libraries and frameworks.

## Installation

### Prerequisites

- Python 3.6 or higher
- GTK 3.0
- FFmpeg (for audio transcoding)

### Steps

1. Clone the repository:
    $ git clone https://github.com/yourusername/melodymover.git cd melodymover 

2. Install the required Python packages:
    $ pip install -r requirements.txt

3. Run the application:
    $ python melodymover.py

## Usage

1. Launch MelodyMover.
2. Click "Choose Destination Folder" to select where your organized music will be stored.
3. Add music folders by dragging and dropping them into the application window or by using the "Manual Folder Search" button.
4. (Optional) Edit metadata fields if you want to apply changes to all processed files.
5. (Optional) Configure transcoding options if you want to convert your audio files.
6. (Optional) Select file types to remove during the process.
7. Click "Process" to start organizing and processing your music files.
8. Monitor the progress using the progress bars at the bottom of the window.

## Contributing

We welcome contributions to MelodyMover! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure your code adheres to the existing style and includes appropriate tests and documentation.

## License

MelodyMover is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- GTK and PyGObject teams for providing the GUI framework
- Mutagen developers for the audio metadata library
- FFmpeg project for audio transcoding capabilities

## Contact


This program is a test to learn how to work with AI. It comes from an original problem we wanted to solve years ago. Now we make
it happen with a little help of some friends.

The program is designed to drag and drop folders with music to change their names, metadata and, optionally, transcode the audio
files of each album. We included the option of getting rid of files that sometimes comes after buying a digital album that are not need.

If you have any questions, suggestions, or issues, please open an issue on the GitHub repository or contact the maintainers directly.

---

Thank you for using MelodyMover! We hope it helps you keep your music collection organized and enjoyable.

