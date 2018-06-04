#!/usr/bin/env python3
#encoding: UTF-8

import random

names = set()

ORIGIN = "cs430.luther.edu." # Important: trailing dot
TYPES = ["A", "AAAA"]
TTL = ['', '1s', '1m', '1h', '1d', '1w', '1y']
CLASS = "IN"
FILE_IN = "students.txt"
FILE_OUT = "hosts.txt"

def read_names(filename):
    with open(filename) as f:
        for name in f:
            full_name = name.strip().lower().split()
            names.add(full_name[0])

def write_zone(FILE_OUT):
    with open(FILE_OUT, 'w') as f:
        f.write("$ORIGIN %s\n" % ORIGIN)
        f.write("$TTL %s\n" % random.choice(TTL))
        for n in names:
            # Adding IPv4 record
            dom_name = n
            dom_type = "A"
            dom_ttl = random.choice(TTL)
            dom_clss = CLASS
            dom_addr = ""
            for _ in range(4):
                dom_addr = dom_addr + str(random.randint(0, 255)) + '.'
            dom_addr = dom_addr.rstrip('.')
            record = format("%-15s%-5s%-5s%-10s%s\n" % (dom_name, dom_ttl, dom_clss, dom_type, dom_addr))
            f.write(record)
            # Adding another IPv4 record. Maybe
            if random.randint(1, 10) > 7:
                dom_name = ""
                dom_ttl = random.choice(TTL)
                dom_clss = CLASS
                dom_addr = ""
                for _ in range(4):
                    dom_addr = dom_addr + str(random.randint(0, 255)) + '.'
                dom_addr = dom_addr.rstrip('.')
                record = format("%-15s%-5s%-5s%-10s%s\n" % (dom_name, dom_ttl, dom_clss, dom_type, dom_addr))
                f.write(record)
            # Adding AAAA record
            dom_name = ""
            dom_type = "AAAA"
            dom_addr = ""
            for _ in range(8):
                dom_addr = dom_addr + str(hex(random.randint(0, 255)))
                dom_addr = dom_addr + str(hex(random.randint(0, 255))) + ':'
            dom_addr = dom_addr.replace('0x', '').rstrip(':')
            record = format("%-15s%-5s%-5s%-10s%s\n" % (dom_name, dom_ttl, dom_clss, dom_type, dom_addr))
            f.write(record)

def main():
    read_names(FILE_IN)
    write_zone(FILE_OUT)

if __name__ == "__main__":
    main()