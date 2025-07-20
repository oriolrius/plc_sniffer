import os
import socket
import json
import time
import threading
import signal
from datetime import datetime

from scapy.all import *
from scapy.layers.http import HTTPRequest

import logging
import gc

# Set up the logger
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=LOGLEVEL, format = FORMAT, handlers = [logging.StreamHandler()])
logger = logging.getLogger('plc_sniffer')
logger.debug(f'LOGLEVEL = {LOGLEVEL}')

# CONFIGURATION
iface = os.getenv('IFACE') or "br-lan"
filtre = os.getenv('FILTER') or "udp port 40000"
# send payload to destination using UDP
UDP_IP = os.getenv('UDP_IP') or "10.121.101.1"
UDP_PORT = os.getenv('UDP_PORT') or 40000
UDP_PORT = int(UDP_PORT)

# Maximum time in seconds before recreating the socket
SOCKET_REFRESH_INTERVAL = 60
# Maximum time in seconds to run sniffing before restarting it
SNIFF_RESTART_INTERVAL = 300

# Flags for controlling the script
running = True
last_packet_time = time.time()

def process_packet(packet):
    global sock
    try:
        if packet.haslayer(IP) and packet.haslayer(UDP) and packet.haslayer(Raw):
            # get source and destination info
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            port_src = packet[UDP].sport
            port_dst = packet[UDP].dport
            
            # get payload data
            payload = bytes(packet[Raw].load)
            
            logger.info(f"{ip_src}:{port_src} -> {ip_dst}:{port_dst} - {len(payload)} bytes")
            logger.debug(f"Payload: {payload}")
            
            # forward the payload to destination
            try:
                sock.sendto(payload, (UDP_IP, UDP_PORT))
                logger.debug(f"Forwarded to {UDP_IP}:{UDP_PORT}")
            except socket.error as e:
                logger.error(f"Socket error while forwarding: {e}")
                # Attempt to recreate socket if there was an error
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e:
        logger.error(f"Error processing packet: {e}")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    
    logger.info(f"Starting UDP sniffer on interface {iface}")
    logger.info(f"Filter: {filtre}")
    logger.info(f"Forwarding to {UDP_IP}:{UDP_PORT}")
    
    try:
        # Use a timeout to allow for graceful handling of Ctrl+C
        sniff(filter=filtre, prn=process_packet, iface=iface, store=False, timeout=None)
    except KeyboardInterrupt:
        logger.info("Stopping sniffer due to keyboard interrupt")
    except Exception as e:
        logger.error(f"Sniffer stopped due to error: {e}")
    finally:
        sock.close()
        logger.info("Socket closed, sniffer stopped")
