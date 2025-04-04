# YouTube Subtitle Manager

A Python application that allows you to download subtitles from YouTube videos and playlists, and combine them into a single file.

## Features

- Download subtitles from single YouTube videos
- Download subtitles from entire YouTube playlists
- Create folders named after the video/playlist titles
- Combine multiple subtitle files into a single file
- Generate multiple-choice tests from manuscript content
- User-friendly menu interface
- No API key required
- Supports various YouTube URL formats (youtube.com, youtu.be)

## Installation

1. Make sure you have Python 3.6+ installed
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Main Application

Run the main application:
```bash
python subtitle_manager.py
```

This will display a menu with the following options:
1. Download subtitles from YouTube videos/playlists
2. Combine existing subtitle files
3. Generate test from manuscript
4. Exit

### Downloading Subtitles

1. Select option 1 from the main menu
2. When prompted, paste a YouTube URL. It can be:
   - A single video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
   - A playlist URL (e.g., https://www.youtube.com/playlist?list=PLAYLIST_ID)
   - A video URL from within a playlist

3. The script will:
   - Create a `youtube_subtitles` directory
   - For single videos: Create a folder named after the video title
   - For playlists: Create a folder named after the playlist title
   - Download subtitles for all videos
   - Save each subtitle file as `VIDEO_ID.txt` in the appropriate folder

### Combining Subtitles

1. Select option 2 from the main menu
2. The script will display a list of all available subtitle files
3. Enter the numbers of the subtitles you want to combine (comma-separated, e.g., '1,3,5')
4. Enter an output filename (or press Enter for default: combined_subtitles.txt)
5. The script will:
   - Create a `test_manuscripts` directory if it doesn't exist
   - Save the combined file in the `test_manuscripts` directory
   - Include headers for each video with its ID and source folder

### Generating Tests

1. Select option 3 from the main menu
2. The script will display a list of all available manuscript files in the `test_manuscripts` directory
3. Enter the number of the manuscript you want to use
4. Enter the number of questions you want (1-10)
5. Select the difficulty level (Easy, Medium, Hard)
6. The script will:
   - Generate a multiple-choice test based on the manuscript content
   - Create a `generated_tests` directory if it doesn't exist
   - Save the test in the `generated_tests` directory with a filename that includes the manuscript name, number of questions, and difficulty level

## Notes

- Subtitles are downloaded in the video's default language
- Videos without subtitles are skipped
- Folder names are sanitized to remove invalid characters
- Each subtitle file contains the full transcript in text format
- The combined file includes headers for each video with its ID and source folder
- Test generation uses a free AI model and may take a minute to complete 