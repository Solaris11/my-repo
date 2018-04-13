#!/usr/local/bin/python3

import socket
import subprocess
import re

host_file = "domains.txt"
ns1 = "192.168.20.2"
ns2 = "ns-170.awsdns-21.com"

def is_valid_ip(ip):
    if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', ip):
        return True
    else:
        return False

def get_ip(domain, name_server):
    completed = subprocess.run(
        ['dig', '+noall', '+answer', '+short', domain, name_server],
        stdout=subprocess.PIPE,
    )

    my_ips = list()
    if (completed.stdout.decode('utf-8') == ""):
        return my_ips

    result = completed.stdout.decode("utf-8").split()

    for ip_addr in result:
        if is_valid_ip(ip_addr):
            my_ips.append(ip_addr)
    my_ips.sort()
    return my_ips

num_domain = 1
num_failed = 0;

for domain in open(host_file):
    domain = domain.strip()
    if (domain == ""):
        continue;
    #print(str(num_domain), domain);
    num_domain = num_domain + 1

    ip_ns1 = get_ip(domain, "@" + ns1)
    ip_ns2 = get_ip(domain, "@" + ns2)

    print("")
    print(domain, "is resolved to ip addresses:\n")

    if not ip_ns1:
        print("NOT resolved by nameserver", ns1)
    else:
        first_ip = True
        for my_ip in ip_ns1:
            if not first_ip:
                print(", ", end="")
            print(my_ip, end="")
            first_ip = False
        print(" by nameserver", ns1)
    print("")

    if not ip_ns2:
        print("NOT resolved by nameserver", ns2)
    else:
        first_ip = True
        for my_ip in ip_ns2:
            if not first_ip:
                print(", ", end="")
            print(my_ip, end="")
            first_ip = False
        print(" by nameserver", ns2)
    print("")

    if (ip_ns1 != ip_ns2):
        print("WARNING: Inconsistent DNS resolution for", domain, "Please check it for any error.")
        num_failed = num_failed + 1

    print("-----------------------------------------------")


if num_failed > 0:
    print("")
    print("Hosts failed = ", num_failed)
    print("")
