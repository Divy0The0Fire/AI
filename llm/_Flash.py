import os
import time

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini("Recorded Audio June 11, 2024 - 11:01PM.ogg", mime_type="audio/ogg"),
  upload_to_gemini("image_animal3.jpeg", mime_type="image/jpeg"),
  upload_to_gemini("American Museum of Natural History Tour - 5 Min", mime_type="video/mp4"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "hello",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Hello! How can I help you today? \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[0],
        files[1],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[2],
      ],
    },
    {
      "role": "user",
      "parts": [
        "can you tell me whats going on ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "The video is showing a tour of a dinosaur exhibit at a museum. It shows dinosaur skeletons, fossils, and other exhibits, with information about the different dinosaurs and their history.  \n\nIf you have any more questions about the video, feel free to ask!  \n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)