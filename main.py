'''
import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil

# Function to save uploaded files
def save_uploadedfile(uploadedfile, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_path = os.path.join(dir, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path

st.title("Wav2Lip Lip-Sync App")

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Upload video file
uploaded_video = st.file_uploader("Upload a video file", type=["mp4"])
video_path = None
if uploaded_video is not None:
    video_path = save_uploadedfile(uploaded_video, 'uploads')
    st.video(video_path)

# Input text
text_input = st.text_area("Enter text to convert to speech")

if st.button("Generate Lip-Synced Video"):
    if uploaded_video is not None and text_input:
        # Convert text to speech
        tts_output = gTTS(text_input)
        tts_output.save(temp_audio_path)

        # Run Wav2Lip inference
        command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {video_path} --audio {temp_audio_path} --outfile {output_video_path}'
        subprocess.run(command, shell=True, check=True)

        # Display the result video
        st.video(output_video_path)

        # Cleanup temporary files
        os.remove(temp_audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(output_video_path):
            shutil.move(output_video_path, 'output_result.mp4')
            st.video('output_result.mp4')

    else:
        st.error("Please upload a video and enter text to proceed.")
,
import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil

# Function to save uploaded files
def save_uploadedfile(uploadedfile, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_path = os.path.join(dir, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path

st.title("Wav2Lip Lip-Sync App")

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Upload video file
uploaded_video = st.file_uploader("Upload a video file", type=["mp4"])
video_path = None
if uploaded_video is not None:
    video_path = save_uploadedfile(uploaded_video, 'uploads')
    st.video(video_path)

# Input text
text_input = st.text_area("Enter text to convert to speech")

if st.button("Generate Lip-Synced Video"):
    if uploaded_video is not None and text_input:
        # Convert text to speech
        tts_output = gTTS(text_input)
        tts_output.save(temp_audio_path)
        st.write("Text to speech conversion done.")

        # Run Wav2Lip inference
        command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {video_path} --audio {temp_audio_path} --outfile {output_video_path}'
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
            if os.path.exists(video_path):
                os.remove(video_path)
            # Move result video to a different location if necessary
            shutil.move(output_video_path, 'output_result.mp4')
            st.video('output_result.mp4')
        else:
            st.error("Failed to generate the lip-synced video. Please check the logs above for more details.")
    else:
        st.error("Please upload a video and enter text to proceed.")
'''

import streamlit as st
from gtts import gTTS
import subprocess
import os
import shutil

# Function to save uploaded files
def save_uploadedfile(uploadedfile, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_path = os.path.join(dir, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path

st.title("Wav2Lip Lip-Sync App")

# Path settings
wav2lip_path = '/teamspace/studios/this_studio/Wav2Lip'
checkpoint_path = os.path.join(wav2lip_path, 'checkpoints/wav2lip_gan.pth')
output_dir = os.path.join(wav2lip_path, 'results')
temp_audio_path = 'simple_gtts.wav'
output_video_path = os.path.join(output_dir, 'result.mp4')

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Upload video file
uploaded_video = st.file_uploader("Upload a video file", type=["mp4"])
video_path = None
if uploaded_video is not None:
    video_path = save_uploadedfile(uploaded_video, 'uploads')
    st.video(video_path)

# Input text
text_input = st.text_area("Enter text to convert to speech")

if st.button("Generate Lip-Synced Video"):
    if uploaded_video is not None and text_input:
        # Convert text to speech
        tts_output = gTTS(text_input)
        tts_output.save(temp_audio_path)
        st.write("Text to speech conversion done.")

        # Run Wav2Lip inference
        command = f'python {os.path.join(wav2lip_path, "inference.py")} --checkpoint_path {checkpoint_path} --face {video_path} --audio {temp_audio_path} --outfile {output_video_path}'
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
            if os.path.exists(video_path):
                os.remove(video_path)
            # Move result video to a different location if necessary
            shutil.move(output_video_path, 'output_result.mp4')
            st.video('output_result.mp4')
        else:
            st.error("Failed to generate the lip-synced video. Please check the logs above for more details.")
    else:
        st.error("Please upload a video and enter text to proceed.")
