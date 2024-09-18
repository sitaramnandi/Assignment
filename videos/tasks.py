# import subprocess
# import os
# import logging
# from celery import shared_task
# from .models import Video, Subtitle

# logger = logging.getLogger(__name__)

# @shared_task
# def process_video(video_id):
#     try:
#         video = Video.objects.get(id=video_id)
#     except Video.DoesNotExist:
#         logger.error(f"Video with id {video_id} does not exist.")
#         return f"Video with id {video_id} does not exist."

#     video_path = video.video_file.path
#     mkv_video_path = f"{video_path.rsplit('.', 1)[0]}.mkv"
#     subtitle_file = f"{mkv_video_path}.srt"
#     ccextractor_path = r"C:\\Program Files (x86)\\CCExtractor\\ccextractorwinfull.exe"

#     # Convert .webm to .mkv
#     try:
#         subprocess.run(['ffmpeg', '-i', video_path, '-c', 'copy', mkv_video_path], check=True)
#         logger.info(f"Video successfully converted to MKV format at {mkv_video_path}")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error converting video: {e}")
#         return f"Error converting video: {e}"

#     # Extract subtitles using CCExtractor
#     try:
#         subprocess.run([ccextractor_path, mkv_video_path, '-o', subtitle_file], check=True)
#         logger.info(f"CCExtractor run completed successfully. Subtitle file created at {subtitle_file}")
#     except subprocess.CalledProcessError as e:
#         logger.error(f"Error while running CCExtractor: {e}")
#         return f"Error while running CCExtractor: {e}"

#     if not os.path.exists(subtitle_file):
#         logger.error(f"Subtitle file {subtitle_file} was not created.")
#         return f"Subtitle file {subtitle_file} was not created."

#     # Parse and store subtitles
#     try:
#         subtitles = parse_srt_file(subtitle_file)
#         for timestamp, content in subtitles:
#             Subtitle.objects.create(
#                 video=video,
#                 language='en',
#                 content=content,
#                 timestamp=timestamp
#             )
#         logger.info("Subtitles successfully saved to the database.")
#     except IOError as e:
#         logger.error(f"Error reading subtitle file: {e}")
#         return f"Error reading subtitle file: {e}"

#     logger.info("Processing complete.")
#     return "Processing complete."

# def parse_srt_file(file_path):
#     subtitles = []
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             while True:
#                 number = file.readline().strip()
#                 if not number:
#                     break
#                 timestamp_line = file.readline().strip()
#                 content_line = file.readline().strip()
#                 file.readline()  # Skip empty line
#                 if ' --> ' in timestamp_line:
#                     timestamp = timestamp_line.split(' --> ')[0]
#                     subtitles.append((timestamp, content_line))
#     except Exception as e:
#         logger.error(f"Error parsing SRT file: {e}")
#         raise
#     return subtitles

# import subprocess
# import os
# import logging
# from celery import shared_task
# from .models import Video, Subtitle

# logger = logging.getLogger('tasks')
# logger.debug("This is a debug message for tasks logger")
# @shared_task
# def process_video(video_id):
#     try:
#         video = Video.objects.get(id=video_id)
#     except Video.DoesNotExist:
#         return f"Video with id {video_id} does not exist."

#     video_path = video.video_file.path
#     mkv_video_path = f"{video_path.rsplit('.', 1)[0]}.mkv"
    
#     # Define the desired subtitle file (e.g., 'test1_eng.srt')
#     subtitle_file = f"{video_path.rsplit('.', 1)[0]}_eng.srt"
#     ccextractor_path = r"C:\\Program Files (x86)\\CCExtractor\\ccextractorwinfull.exe"

#     # Convert .webm to .mkv
#     try:
#         subprocess.run(['ffmpeg', '-i', video_path, '-c', 'copy', mkv_video_path], check=True)
#     except subprocess.CalledProcessError as e:
#         return f"Error converting video: {e}"

#     # Extract subtitles using CCExtractor to the desired file (e.g., 'test1_eng.srt')
#     try:
#         subprocess.run([ccextractor_path, mkv_video_path, '-o', subtitle_file], check=True)
#     except subprocess.CalledProcessError as e:
#         return f"Error while running CCExtractor: {e}"

#     # Check if the desired subtitle file was created
#     if not os.path.exists(subtitle_file):
#         return f"Subtitle file {subtitle_file} was not created."

#     # Automatically delete the unwanted .mkv.srt file if it exists
#     unwanted_srt_file = f"{mkv_video_path}.srt"
#     if os.path.exists(unwanted_srt_file):
#         os.remove(unwanted_srt_file)

#     # Parse and store subtitles
#     try:
#         subtitles = parse_srt_file(subtitle_file)
#         for timestamp, content in subtitles:
#             # Save subtitles to the database
#             Subtitle.objects.get_or_create(
#                 video=video,
#                 language='en',
#                 content=content,
#                 timestamp=timestamp
#             )
#     except IOError as e:
#         return f"Error reading subtitle file: {e}"

#     return "Processing complete."


# def parse_srt_file(file_path):
#     subtitles = []
#     try:
#         logger.info(f"Parsing SRT file: {file_path}")
#         with open(file_path, 'r', encoding='utf-8') as file:
#             content = file.read()
#             blocks = content.split('\n\n')
#             for block in blocks:
#                 lines = block.split('\n')
#                 if len(lines) >= 3:
#                     number = lines[0].strip()
#                     timestamp_line = lines[1].strip()
#                     content_line = '\n'.join(lines[2:]).strip()
#                     if ' --> ' in timestamp_line:
#                         timestamp = timestamp_line.split(' --> ')[0].replace(',', '.')
#                         logger.debug(f"Parsed subtitle: {timestamp} - {content_line}")
#                         subtitles.append((timestamp, content_line))
#     except Exception as e:
#         logger.error(f"Error parsing SRT file: {e}")
#         raise
#     return subtitles


# ======================================



import subprocess
import os
from celery import shared_task
from .models import Video, Subtitle

@shared_task
def process_video(video_id):
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return f"Video with id {video_id} does not exist."

    video_path = video.video_file.path
    base_name = os.path.splitext(video_path)[0]
    mkv_video_path = f"{base_name}.mkv"
    subtitle_file = f"{base_name}_eng.srt"

    # Convert .webm to .mkv
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-c', 'copy', mkv_video_path], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error converting video: {e}"

    # Extract subtitles from the .mkv file
    try:
        subprocess.run(['ffmpeg', '-i', mkv_video_path, '-map', '0:s:0', subtitle_file], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error extracting subtitles: {e}"

    # Check if the desired subtitle file was created
    if not os.path.exists(subtitle_file):
        return f"Subtitle file {subtitle_file} was not created."

    # Remove the .mkv file after processing
    if os.path.exists(mkv_video_path):
        os.remove(mkv_video_path)

    # Parse and store subtitles
    try:
        subtitles = parse_srt_file(subtitle_file)
        for timestamp, content in subtitles:
            # Save subtitles to the database
            Subtitle.objects.get_or_create(
                video=video,
                language='en',
                content=content,
                timestamp=timestamp
            )
    except IOError as e:
        return f"Error reading subtitle file: {e}"

    # Optionally, remove the subtitle file after storing it to the database
    # os.remove(subtitle_file)

    return "Processing complete."

def parse_srt_file(file_path):
    subtitles = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            blocks = content.split('\n\n')
            for block in blocks:
                lines = block.split('\n')
                if len(lines) >= 3:
                    timestamp_line = lines[1].strip()
                    content_line = '\n'.join(lines[2:]).strip()
                    if ' --> ' in timestamp_line:
                        timestamp = timestamp_line.split(' --> ')[0].replace(',', '.')
                        subtitles.append((timestamp, content_line))
    except Exception as e:
        raise IOError(f"Error parsing SRT file: {e}")
    return subtitles
