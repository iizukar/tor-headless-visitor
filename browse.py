import os
import time
import requests
from multiprocessing import Pool
from stem import Signal
from stem.control import Controller

URL = "https://www.browserling.com/browse/win10/chrome127/http://testingimp.great-site.net"
TOR_PORTS = [9050, 9051, 9052, 9053, 9054]

def new_tor_identity(control_port):
    with Controller.from_port(port=control_port) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        time.sleep(5)

def browse_via_tor(proxy_port, control_port):
    proxies = {
        'http': f'socks5://127.0.0.1:{proxy_port}',
        'https': f'socks5://127.0.0.1:{proxy_port}'
    }
    
    try:
        new_tor_identity(control_port)
        response = requests.get(URL, proxies=proxies, timeout=180)
        print(f"Port {proxy_port} - Status: {response.status_code}")
        time.sleep(180)  # Wait 3 minutes
    except Exception as e:
        print(f"Error on port {proxy_port}: {str(e)}")

def main():
    with Pool(5) as pool:
        while True:
            # Map TOR_PORTS to control ports (usually +1)
            pool.starmap(browse_via_tor, [(port, port+1) for port in TOR_PORTS])
            print("Completed cycle. Restarting...")

if __name__ == "__main__":
    main()
