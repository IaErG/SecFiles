from scapy.all import *

def manage_packet(packet):
    if packet.haslayer(TCP):
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dest_port = packet[TCP].dport

        print(f"TCP Connection: {src_ip}:{src_port} -> {dest_ip}:{dest_port}")


sniff(iface=conf.iface, prn=lambda pkt: manage_packet(pkt), store=0)