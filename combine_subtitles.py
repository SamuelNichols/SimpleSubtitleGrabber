import os
import glob
from pathlib import Path

def get_subtitle_files():
    """Get all subtitle files from the youtube_subtitles directory."""
    base_dir = "youtube_subtitles"
    if not os.path.exists(base_dir):
        print("No subtitles directory found. Please run youtube_subtitle_downloader.py first.")
        return []
    
    # Get all .txt files from all subdirectories
    subtitle_files = []
    for txt_file in glob.glob(os.path.join(base_dir, "**", "*.txt"), recursive=True):
        # Get the parent directory name (video/playlist title)
        parent_dir = os.path.basename(os.path.dirname(txt_file))
        # Get the filename without extension
        filename = os.path.splitext(os.path.basename(txt_file))[0]
        
        # Try to convert filename to integer for sorting
        try:
            order = int(filename)
            is_playlist = True
        except ValueError:
            order = float('inf')  # Put non-numeric filenames at the end
            is_playlist = False
        
        subtitle_files.append({
            'path': txt_file,
            'folder': parent_dir,
            'filename': filename,
            'order': order,
            'is_playlist': is_playlist
        })
    
    # Sort files: first by folder name, then by order number
    subtitle_files.sort(key=lambda x: (x['folder'], x['order']))
    
    return subtitle_files

def display_subtitles(subtitle_files):
    """Display all available subtitles in a numbered list."""
    if not subtitle_files:
        print("No subtitle files found.")
        return
    
    print("\nAvailable subtitles:")
    print("-" * 80)
    current_folder = None
    for i, sub in enumerate(subtitle_files, 1):
        # Print folder name as a header when it changes
        if sub['folder'] != current_folder:
            current_folder = sub['folder']
            print(f"\n{current_folder}:")
        
        # For playlist videos, show the order number
        if sub['is_playlist']:
            print(f"{i}. Video {sub['filename']}")
        else:
            print(f"{i}. {sub['filename']}")
    print("-" * 80)

def read_subtitle_file(file_path):
    """Read and return the contents of a subtitle file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return ""

def combine_subtitles(selected_files, output_file):
    """Combine selected subtitle files into one file."""
    try:
        # Create test_manuscripts directory if it doesn't exist
        output_dir = "test_manuscripts"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create the full output path
        output_path = os.path.join(output_dir, output_file)
        
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for sub in selected_files:
                # Write a header for each video
                outfile.write(f"\n{'='*80}\n")
                if sub['is_playlist']:
                    outfile.write(f"Video {sub['filename']} from playlist: {sub['folder']}\n")
                else:
                    outfile.write(f"Video: {sub['filename']}\n")
                outfile.write(f"{'='*80}\n\n")
                
                # Write the subtitle content
                content = read_subtitle_file(sub['path'])
                outfile.write(content)
                outfile.write("\n")
        
        print(f"\nCombined subtitles saved to: {output_path}")
    except Exception as e:
        print(f"Error combining subtitles: {str(e)}")

def main():
    # Get all subtitle files
    subtitle_files = get_subtitle_files()
    
    # Display available subtitles
    display_subtitles(subtitle_files)
    
    if not subtitle_files:
        return
    
    # Get user selection
    while True:
        try:
            selection = input("\nEnter the numbers of the subtitles to combine (comma-separated, e.g., '1,3,5'): ")
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            
            # Validate selection
            if any(i < 0 or i >= len(subtitle_files) for i in indices):
                print("Invalid selection. Please enter numbers from the list above.")
                continue
            
            selected_files = [subtitle_files[i] for i in indices]
            break
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    
    # Get output filename
    output_file = input("\nEnter the output filename (default: combined_subtitles.txt): ").strip()
    if not output_file:
        output_file = "combined_subtitles.txt"
    if not output_file.endswith('.txt'):
        output_file += '.txt'
    
    # Combine selected subtitles
    combine_subtitles(selected_files, output_file)

if __name__ == "__main__":
    main() 