#!/usr/bin/env python

import scapy.all as scapy
import argparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # you put [0] for only capture the answered list element (there was unanswered list too remember!!)
    # print(answered_list.summary())
    # element[1].show()
    clients_list = []
    for element in answered_list:
        clients_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(clients_dict)
        # print(element[1].psrc + "\t\t" + element[1].hwsrc)
        print("-----------------------------------------")
    return clients_list


def print_result(results_list):
    print("IP\t\t\t MAC Address\n-----------------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])


def get_ip_range():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip_range", help= "IP range for scanning")
    options = parser.parse_args()
    if options.ip_range:
        return options
    else:
        parser.error("Please specify IP range. Type --help for more info")


target = get_ip_range()

scan_result = scan(target.ip_range)
print_result(scan_result)
