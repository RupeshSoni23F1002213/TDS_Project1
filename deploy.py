from dotenv import load_dotenv
import os
import ngrok
import time

load_dotenv()

listener = ngrok.forward(
  # The port your app is running on.
  8000,
  authtoken=os.getenv("NGROK_AUTHTOKEN"),
  # If you haven't reserved a domain, omit this
  # This could also be a path to a traffic policy file.
)

# Output ngrok url to console
print(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")