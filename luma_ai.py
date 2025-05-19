import streamlit as st
import os
import requests
import time
from lumaai import LumaAI

# Set up LumaAI client
client = LumaAI(auth_token=os.getenv("LUMAAI_API_KEY"))

st.set_page_config(page_title="LumaAI Video Generator", layout="centered")
st.title("🎥 LumaAI Video Generator")
st.markdown("Enter a prompt to generate a video using LumaAI's `ray-2` model.")

# Prompt input
prompt = st.text_area("Enter your prompt", value="Create a positive, cheerful, and festive animated scene for New Year's greetings.", height=150)

# Submit button
if st.button("Generate Video"):
    with st.spinner("Generating video... please wait ⏳"):
        try:
            # Trigger generation
            generation = client.generations.create(
                prompt=prompt,
                model="ray-2"
            )

            # Polling until done
            while True:
                generation = client.generations.get(id=generation.id)
                if generation.state == "completed":
                    break
                elif generation.state == "failed":
                    st.error(f"Generation failed: {generation.failure_reason}")
                    st.stop()
                time.sleep(3)

            # Get video
            video_url = generation.assets.video
            video_response = requests.get(video_url)
            video_filename = f"{generation.id}.mp4"
            with open(video_filename, 'wb') as f:
                f.write(video_response.content)

            st.success("✅ Video generated successfully!")
            st.video(video_filename)

            with open(video_filename, "rb") as file:
                st.download_button("📥 Download Video", file, file_name=video_filename, mime="video/mp4")

        except Exception as e:
            st.error(f"An error occurred: {e}")
                                                                                                                                                                                                                        