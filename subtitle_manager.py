#!/usr/bin/env python3
import os
import sys
import subprocess

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("=" * 80)
    print("YouTube Subtitle Manager".center(80))
    print("=" * 80)
    print()

def print_menu():
    """Print the main menu options."""
    print("What would you like to do?")
    print("1. Download subtitles from YouTube videos/playlists")
    print("2. Combine existing subtitle files")
    print("3. Generate test from manuscript")
    print("4. Exit")
    print()

def run_subtitle_downloader():
    """Run the subtitle downloader script."""
    clear_screen()
    print_header()
    print("YouTube Subtitle Downloader".center(80))
    print("=" * 80)
    print()
    
    try:
        # Run the subtitle downloader script
        subprocess.run([sys.executable, "youtube_subtitle_downloader.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nError running the subtitle downloader script.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def run_subtitle_combiner():
    """Run the subtitle combiner script."""
    clear_screen()
    print_header()
    print("YouTube Subtitle Combiner".center(80))
    print("=" * 80)
    print()
    
    try:
        # Run the subtitle combiner script
        subprocess.run([sys.executable, "combine_subtitles.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nError running the subtitle combiner script.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def run_test_generator():
    """Run the test generator script."""
    clear_screen()
    print_header()
    print("Test Generator".center(80))
    print("=" * 80)
    print()
    
    try:
        # Run the test generator script
        subprocess.run([sys.executable, "generate_test.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nError running the test generator script.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    input("\nPress Enter to return to the main menu...")

def main():
    """Main function to run the subtitle manager."""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            run_subtitle_downloader()
        elif choice == '2':
            run_subtitle_combiner()
        elif choice == '3':
            run_test_generator()
        elif choice == '4':
            print("\nThank you for using YouTube Subtitle Manager. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 