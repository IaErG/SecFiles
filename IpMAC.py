import scapy.all as scapy

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broad = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broad = broad / arp_req

    answered_list = scapy.srp(arp_req_broad, timeout=1, verbose=False)[0]

    results = []

    for elem in answered_list:
        result = {"ip" : elem[1].psrc, "mac" : elem[1].hwsrc}
        results.append(result)

    return results

def display_results(res):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for result in res:
        print(result["ip"] + "\t\t" + result["mac"])

target_ip = "192.168.2.40"
scan_results = scan(target_ip)
display_results(scan_results)