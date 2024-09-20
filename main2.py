'''
import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil
import cv2
from PIL import Image

# Function to create GIF from video
def create_gif(video_path, gif_path, duration=2):
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(fps * duration)
    success, frame = cap.read()
    count = 0

    while success and count < total_frames:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame_rgb))
        success, frame = cap.read()
        count += 1

    if frames:
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0)

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Pre-uploaded video files on the server
uploaded_videos = [
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-18 at 9.53.50 AM.mp4',
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-19 at 11.05.38 AM.mp4',
    '/teamspace/studios/this_studio/vids/SRKK.mp4'
]

# Create GIFs from the videos
gif_paths = []
for i, video_path in enumerate(uploaded_videos):
    gif_path = f'gif_{i}.gif'
    create_gif(video_path, gif_path)
    gif_paths.append(gif_path)

st.title("Wav2Lip Application")

st.header("Select a video by clicking on the GIF")
selected_video = None

# Display GIFs in a row and detect clicks
cols = st.columns(3)
for i, col in enumerate(cols):
    if col.button(f"Select Video {i+1}"):
        selected_video = uploaded_videos[i]
    col.image(gif_paths[i], use_column_width=True)

# Input text
text_input = st.text_area("Enter text to convert to speech")

if st.button("Generate Lip-Synced Video"):
    if selected_video and text_input:
        # Convert text to speech
        tts_output = gTTS(text_input)
        tts_output.save(temp_audio_path)
        st.write("Text to speech conversion done.")

        # Run Wav2Lip inference
        command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {selected_video} --audio {temp_audio_path} --outfile {output_video_path}'
        st.write("Running Wav2Lip inference...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Debugging information
        st.text("Command executed: " + command)
        st.text("STDOUT: " + result.stdout)
        st.text("STDERR: " + result.stderr)

        # Check for output file existence
        if os.path.exists(output_video_path):
            st.write("Inference completed successfully.")
            # Display the result video
            st.video(output_video_path)

            # Cleanup temporary files
            os.remove(temp_audio_path)
            # Move result video to a different location if necessary
            shutil.move(output_video_path, 'output_result.mp4')
            st.video('output_result.mp4')
        else:
            st.error("Failed to generate the lip-synced video. Please check the logs above for more details.")
    else:
        st.error("Please select a video and enter text to proceed.")
,
import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil
import cv2
from PIL import Image

# Function to create GIF from video
def create_gif(video_path, gif_path, duration=2):
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(fps * duration)
        success, frame = cap.read()
        count = 0

        while success and count < total_frames:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame_rgb))
            success, frame = cap.read()
            count += 1

        if frames:
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
            return gif_path
        else:
            raise ValueError(f"No frames extracted from {video_path}")

    except Exception as e:
        st.error(f"Error creating GIF from {video_path}: {e}")
        return None

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Pre-uploaded video files on the server
uploaded_videos = [
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-18 at 9.53.50 AM.mp4',
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-19 at 11.05.38 AM.mp4',
    '/teamspace/studios/this_studio/vids/SRKK.mp4'
]

# Create GIFs from the videos
gif_paths = []
for i, video_path in enumerate(uploaded_videos):
    gif_path = f'gif_{i}.gif'
    created_gif_path = create_gif(video_path, gif_path)
    if created_gif_path:
        gif_paths.append(created_gif_path)
    else:
        st.error(f"Failed to create GIF for video: {video_path}")

st.title("Wav2Lip Application")

st.header("Select a video by clicking on the GIF")

# Initialize session state
if "selected_video" not in st.session_state:
    st.session_state.selected_video = None

# Display GIFs in a row and detect clicks
if gif_paths:
    cols = st.columns(len(gif_paths))
    for i, col in enumerate(cols):
        if col.button(f"Select Video {i+1}"):
            st.session_state.selected_video = uploaded_videos[i]
        col.image(gif_paths[i], use_column_width=True)
else:
    st.error("No GIFs available to display.")

# Show text input area only if a video is selected
if st.session_state.selected_video:
    st.subheader("You selected: " + st.session_state.selected_video)
    text_input = st.text_area("Enter text to convert to speech")

    if st.button("Generate Lip-Synced Video"):
        if text_input:
            # Convert text to speech
            tts_output = gTTS(text_input)
            tts_output.save(temp_audio_path)
            st.write("Text to speech conversion done.")

            # Run Wav2Lip inference
            command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {st.session_state.selected_video} --audio {temp_audio_path} --outfile {output_video_path}'
            st.write("Running Wav2Lip inference...")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Debugging information
            st.text("Command executed: " + command)
            st.text("STDOUT: " + result.stdout)
            st.text("STDERR: " + result.stderr)

            # Check for output file existence
            if os.path.exists(output_video_path):
                st.write("Inference completed successfully.")
                # Display the result video
                st.video(output_video_path)

                # Cleanup temporary files
                os.remove(temp_audio_path)
                # Move result video to a different location if necessary
                shutil.move(output_video_path, 'output_result.mp4')
                st.video('output_result.mp4')
            else:
                st.error("Failed to generate the lip-synced video. Please check the logs above for more details.")
        else:
            st.error("Please enter text to proceed.")
'''

import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil
import cv2
from PIL import Image

# Function to create GIF from video
def create_gif(video_path, gif_path, duration=2):
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(fps * duration)
        success, frame = cap.read()
        count = 0

        while success and count < total_frames:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(frame_rgb))
            success, frame = cap.read()
            count += 1

        if frames:
            frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
            return gif_path
        else:
            raise ValueError(f"No frames extracted from {video_path}")

    except Exception as e:
        st.error(f"Error creating GIF from {video_path}: {e}")
        return None

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Pre-uploaded video files on the server
uploaded_videos = [
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-18 at 9.53.50 AM.mp4',
    '/teamspace/studios/this_studio/vids/Screen Recording 2024-06-19 at 11.05.38 AM.mp4',
    '/teamspace/studios/this_studio/vids/SRKK.mp4'
]

# Create GIFs from the videos
gif_paths = []
for i, video_path in enumerate(uploaded_videos):
    gif_path = f'gif_{i}.gif'
    created_gif_path = create_gif(video_path, gif_path)
    if created_gif_path:
        gif_paths.append(created_gif_path)
    else:
        st.error(f"Failed to create GIF for video: {video_path}")

st.title("Wav2Lip Application")

st.header("Select a video by clicking on the GIF")

# Initialize session state
if "selected_video" not in st.session_state:
    st.session_state.selected_video = None

# Display GIFs in a row and detect clicks
if gif_paths:
    cols = st.columns(len(gif_paths))
    for i, col in enumerate(cols):
        if col.button(f"Select Video {i+1}"):
            st.session_state.selected_video = uploaded_videos[i]
        col.image(gif_paths[i], use_column_width=True)
else:
    st.error("No GIFs available to display.")

# Show text input area only if a video is selected
if st.session_state.selected_video:
    st.subheader("You selected: " + st.session_state.selected_video)
    text_input = st.text_area("Enter text to convert to speech")

    if st.button("Generate Lip-Synced Video"):
        if text_input:
            # Convert text to speech
            tts_output = gTTS(text_input)
            tts_output.save(temp_audio_path)
            st.write("Text to speech conversion done.")

            # Properly quote the file paths
            selected_video_quoted = f'"{st.session_state.selected_video}"'
            temp_audio_path_quoted = f'"{temp_audio_path}"'
            output_video_path_quoted = f'"{output_video_path}"'

            # Run Wav2Lip inference
            command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {selected_video_quoted} --audio {temp_audio_path_quoted} --outfile {output_video_path_quoted}'
            st.write("Running Wav2Lip inference...")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Debugging information
            st.text("Command executed: " + command)
            st.text("STDOUT: " + result.stdout)
            st.text("STDERR: " + result.stderr)

            # Check for output file existence
            if os.path.exists(output_video_path):
                st.write("Inference completed successfully.")
                # Display the result video
                st.video(output_video_path)

                # Cleanup temporary files
                os.remove(temp_audio_path)
                # Move result video to a different location if necessary
                shutil.move(output_video_path, 'output_result.mp4')
                st.video('output_result.mp4')
            else:
                st.error("Failed to generate the lip-synced video. Please check the logs above for more details.")
        else:
            st.error("Please enter text to proceed.")