import os
import eyed3
import click
from collections import defaultdict

# Function to scan the directory for audio files
def scan_directory(directory):
    audio_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp3', '.wav', '.flac')):
                audio_files.append(os.path.join(root, file))
    return audio_files

# Function to extract genre from the metadata of a song
def get_genre(file_path):
    try:
        audio_file = eyed3.load(file_path)
        genre = audio_file.tag.genre
        return genre.name if genre else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# Function to categorize songs by genre
def categorize_songs(audio_files):
    categorized = defaultdict(list)
    
    for file in audio_files:
        genre = get_genre(file)
        if genre:
            categorized[genre].append(file)
        else:
            categorized["Unknown"].append(file)
    
    return categorized

# Function to create a playlist (e.g., save as .m3u)
def create_playlist(genre, categorized_songs, playlist_name="playlist.m3u"):
    if genre in categorized_songs:
        with open(playlist_name, 'w') as playlist:
            for song in categorized_songs[genre]:
                playlist.write(f"{song}\n")
        print(f"Playlist '{playlist_name}' created with {len(categorized_songs[genre])} songs.")
    else:
        print(f"No songs found for genre '{genre}'.")

# CLI commands using click
@click.group()
def cli():
    """CLI tool for song categorization and playlist creation."""
    pass

@cli.command()
@click.argument('directory')
def scan(directory):
    """Scan a directory for audio files."""
    audio_files = scan_directory(directory)
    categorized = categorize_songs(audio_files)
    for genre, songs in categorized.items():
        print(f"{genre}: {len(songs)} songs found.")
    
@cli.command()
@click.argument('directory')
@click.argument('genre')
@click.option('--playlist-name', default="playlist.m3u", help="Name of the playlist file.")
def create_playlist_command(directory, genre, playlist_name):
    """Create a playlist based on a genre."""
    audio_files = scan_directory(directory)
    categorized = categorize_songs(audio_files)
    create_playlist(genre, categorized, playlist_name)

if __name__ == '__main__':
    cli()
