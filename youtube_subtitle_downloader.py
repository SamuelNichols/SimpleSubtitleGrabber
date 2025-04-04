import os
import json
import hashlib
import time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
from pytube import Playlist, YouTube
import re

def extract_video_id(url):
    """Extract video ID from various forms of YouTube URLs."""
    # Handle different URL formats
    if 'youtu.be' in url:
        return url.split('/')[-1]
    
    query = parse_qs(urlparse(url).query)
    if 'v' in query:
        return query['v'][0]
    
    return None

def generate_hash(text):
    """Generate a unique hash for a given text."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:10]

def get_playlist_info(url):
    """Get playlist information including title and video IDs with order."""
    try:
        # Extract playlist ID from URL
        playlist_id = parse_qs(urlparse(url).query).get('list', [None])[0]
        if not playlist_id:
            return None, []
        
        # Create playlist URL
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        
        # Get playlist object
        playlist = Playlist(playlist_url)
        
        # Get playlist title
        playlist_title = playlist.title
        
        # Get all video URLs with their order
        video_urls = playlist.video_urls
        
        # Extract video IDs from URLs with their order
        video_ids = []
        for i, video_url in enumerate(video_urls, 1):
            video_id = extract_video_id(video_url)
            if video_id:
                video_ids.append({
                    'id': video_id,
                    'order': i
                })
        
        return playlist_title, video_ids
    except Exception as e:
        print(f"Error getting playlist info: {str(e)}")
        return None, []

def get_video_title(video_id, max_retries=3):
    """Get video title from video ID with retry mechanism."""
    for attempt in range(max_retries):
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(video_url) # TODO: figure out why YouTube object is failing to retrieve with error 400 bad request
            return yt.title
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retrying to get title for video {video_id} (attempt {attempt+1}/{max_retries})")
                time.sleep(1)  # Wait a second before retrying
            else:
                print(f"Could not get title for video {video_id}: {str(e)}")
                return f"Video {video_id}"  # Fallback to using video ID as title

def save_mapping_file(base_dir, folder_hash, title, is_playlist=False):
    """Save mapping information to a JSON file."""
    mapping_file = os.path.join(base_dir, "mapping.json")
    
    # Load existing mappings if file exists
    mappings = {}
    if os.path.exists(mapping_file):
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
    
    # Add new mapping
    mappings[folder_hash] = {
        "title": title,
        "type": "playlist" if is_playlist else "video"
    }
    
    # Save updated mappings
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mappings, f, indent=2, ensure_ascii=False)

def save_video_mapping_file(folder_path, video_mappings):
    """Save video mapping information to a JSON file inside the folder."""
    mapping_file = os.path.join(folder_path, "video_mapping.json")
    
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(video_mappings, f, indent=2, ensure_ascii=False)

def download_subtitles(video_id, output_dir, order=None, video_title=None):
    """Download subtitles for a single video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine filename based on whether it's from a playlist
        if order is not None:
            # For playlist videos, use the order number
            output_file = os.path.join(output_dir, f"{order}.txt")
        else:
            # For single videos, use the video ID
            output_file = os.path.join(output_dir, f"{video_id}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_transcript)
        print(f"Downloaded subtitles for video {video_id}")
        return True
    except Exception as e:
        print(f"Error downloading subtitles for video {video_id}: {str(e)}")
        return False

def main():
    # Get URL from user
    url = input("Enter YouTube video or playlist URL: ")
    
    # Create base output directory
    base_output_dir = "youtube_subtitles"
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Check if it's a playlist
    if 'list=' in url:
        print("Processing playlist...")
        playlist_title, playlist_videos = get_playlist_info(url)
        if playlist_videos and playlist_title:
            # Generate hash for playlist folder
            playlist_hash = generate_hash(playlist_title)
            output_dir = os.path.join(base_output_dir, playlist_hash)
            
            # Save playlist mapping
            save_mapping_file(base_output_dir, playlist_hash, playlist_title, is_playlist=True)
            
            print(f"Found {len(playlist_videos)} videos in playlist: {playlist_title}")
            
            # Create video mappings for playlist
            video_mappings = {}
            
            # Download subtitles for each video in order
            for video in playlist_videos:
                video_id = video['id']
                order = video['order']
                
                # Get video title with retry mechanism
                video_title = get_video_title(video_id)
                
                # Add to video mappings
                video_mappings[str(order)] = {
                    "id": video_id,
                    "title": video_title
                }
                
                # Download subtitles
                download_subtitles(video_id, output_dir, order, video_title)
                
                # Add a small delay between requests to avoid rate limiting
                time.sleep(0.5)
            
            # Save video mappings
            save_video_mapping_file(output_dir, video_mappings)
        else:
            print("No videos found in playlist or playlist is private/unavailable")
    else:
        # Handle single video
        video_id = extract_video_id(url)
        if video_id:
            # Get video title with retry mechanism
            video_title = get_video_title(video_id)
            
            # Generate hash for video folder
            video_hash = generate_hash(video_title)
            output_dir = os.path.join(base_output_dir, video_hash)
            
            # Save video mapping
            save_mapping_file(base_output_dir, video_hash, video_title, is_playlist=False)
            
            # Create video mappings for single video
            video_mappings = {
                "1": {
                    "id": video_id,
                    "title": video_title
                }
            }
            
            # Download subtitles
            download_subtitles(video_id, output_dir, None, video_title)
            
            # Save video mappings
            save_video_mapping_file(output_dir, video_mappings)
        else:
            print("Could not extract video ID from URL")

if __name__ == "__main__":
    main() 