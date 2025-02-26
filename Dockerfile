FROM python:3.9-slim

# Install Tor and dependencies
RUN apt-get update && \
    apt-get install -y tor curl && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Configure multiple Tor instances
COPY torrc.template /etc/tor/torrc.template
COPY browse.py .

# Start script
CMD ["python", "browse.py"]
