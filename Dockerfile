FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y tor

# Configure Tor
COPY torrc /etc/tor/torrc

# Install Playwright and browsers
RUN pip install playwright
RUN playwright install firefox

# Copy application files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Start Tor and the script
CMD ["sh", "-c", "tor & python3 script.py"]
