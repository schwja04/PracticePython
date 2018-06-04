###(5 points) Create a server that binds to a localhost at port
# 43053 and responds to any valid DNS requests. The server
# should never stop, serving one request (query) at a time.
# The server should be compatible with a DNS client developed
# for the Week 4 project (see dns_client.py attached). Parse
# the query message to extract the domain name and the
# requested record type and format a valid response message
# that includes all relevant fields found in the hosts.txt.
# The response must be properly formatted, recognized by
# Wireshark, and other clients.

from socket import *
from random import randint

q_type_dict = {"A": 1, "AAAA": 28}
time_to_sec = {'1s':1, '1m':60, '1h':3600, '1d':86400, '1w': 604800, '1y':31449600}

class DNSServer:
    def __init__(self):
        self.msg_qry = bytearray()
        self.dict = {}

    def format_response(self):
        trans_id = self.dict['trans_id']
        if self.dict['qry_type'] != 1 or self.dict['qry_type'] !=28:
            flags = 0x8184
        else:
            flags = 0x8180
        questions = 1
        rr_ans = 0 # figure out in parse_answers
        rr_auth = 0
        rr_add = 0
        q_name = self.dict['domain'] # human-readable
        q_name_lst = q_name.split('.')
        try:
            q_type = self.dict['qry_type']
        except:
            raise Exception("Unknown query type")
        q_class = 1 # IN

        if q_type == 1:
            for record in known_domains[q_name]:
                if record[2] == 'A':
                    rr_ans += 1
        elif q_type == 28:
            for record in known_domains[q_name]:
                if record[2] == 'AAAA':
                    rr_ans += 1

        self.msg_qry.append((trans_id & 0xff00) >> 8)
        self.msg_qry.append(trans_id & 0x00ff)
        self.msg_qry.append((flags & 0xff00) >> 8)
        self.msg_qry.append(flags & 0x00ff)
        self.msg_qry.append((questions & 0xff00) >> 8)
        self.msg_qry.append(questions & 0x00ff)
        self.msg_qry.append((rr_ans & 0xff00) >> 8)
        self.msg_qry.append(rr_ans & 0x00ff)
        self.msg_qry.append((rr_auth & 0xff00) >> 8)
        self.msg_qry.append(rr_auth & 0x00ff)
        self.msg_qry.append((rr_add & 0xff00) >> 8)
        self.msg_qry.append(rr_add & 0x00ff)
        for d in q_name_lst:
            self.msg_qry.append(len(d))
            for c in d:
                self.msg_qry.append(ord(c))
        self.msg_qry.append(0)
        self.msg_qry.append((q_type & 0xff00) >> 8)
        self.msg_qry.append(q_type & 0x00ff)
        self.msg_qry.append((q_class & 0xff00) >> 8)
        self.msg_qry.append(q_class & 0x00ff)

        start_ans = 0xc00c
        Class = 0x0001

        #answer starts
        if q_type == 1:
            data_len = 4
            for response in range(rr_ans):
                self.msg_qry.append((start_ans & 0xff00) >> 8)
                self.msg_qry.append(start_ans & 0x00ff)
                self.msg_qry.append((q_type & 0xff00) >> 8)
                self.msg_qry.append(q_type & 0x00ff)
                self.msg_qry.append((Class & 0xff00) >> 8)
                self.msg_qry.append(Class & 0x00ff)

                if known_domains[q_name]:
                    ttl_bytelist = self.val_to_n_bytes(time_to_sec[known_domains[q_name][response][0]], 4)
                    for x in ttl_bytelist:
                        self.msg_qry.append(x)
                    self.msg_qry.append((data_len & 0xff00) >> 8)
                    self.msg_qry.append(data_len & 0x00ff)
                    addr = known_domains[q_name][response][-1].split('.')
                    for num in addr:
                        self.msg_qry.append(int(num))

        elif q_type == 28:
            data_len = 16
            self.msg_qry.append((start_ans & 0xff00) >> 8)
            self.msg_qry.append(start_ans & 0x00ff)
            self.msg_qry.append((q_type & 0xff00) >> 8)
            self.msg_qry.append(q_type & 0x00ff)
            self.msg_qry.append((Class & 0xff00) >> 8)
            self.msg_qry.append(Class & 0x00ff)

            if known_domains[q_name]:
                ttl_bytelist = self.val_to_n_bytes(time_to_sec[known_domains[q_name][-1][0]], 4)
                for x in ttl_bytelist:
                    self.msg_qry.append(x)

                self.msg_qry.append((data_len & 0xff00) >> 8)
                self.msg_qry.append(data_len & 0x00ff)

                addr = known_domains[q_name][-1][-1].split(':')
                for num in addr:
                    self.msg_qry.append((int(num, 16) & 0xff00) >> 8)
                    self.msg_qry.append(int(num, 16) & 0x00ff)

        print(self.msg_qry)

    def parse_response(self, msg_resp):
        i = 0 # transaction id
        trans_id = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        self.dict['trans_id'] = trans_id
        i = 2 # flags
        flags = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        if (flags >> 15) == 1:
            print("Response received")

        i = 4 # questions
        questions = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])

        i = 6 # answers
        rr_ans = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])

        i = 8 # authority rrs
        rr_auth = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])

        i = 10 # additional rr
        rr_add = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])

        i = 12 # start of the query
        domain = []
        while msg_resp[i] != 0:
            dom_len = msg_resp[i]
            domain.append(msg_resp[i+1:i+dom_len+1])
            i = i + dom_len + 1
        domain_str = ''
        for char in domain:
            domain_str = domain_str + char.decode()
        self.dict['domain'] = domain_str
        i = i + 1 # type
        qry_type = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        self.dict['qry_type'] = qry_type
        i = i + 2 # class
        qry_clss = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])

        if qry_clss != 1:
            raise Exception("Unknown class")
        answer_start = i + 2

    # extract IPv4 address
    def parse_address_a(self, addr_len, addr_bytes):
        resp_addr = []
        # put bytes into a list
        for i in range(addr_len):
            resp_addr.append(addr_bytes[i])
        resp_addr = '.'.join(str(x) for x in resp_addr)

        return resp_addr
    # extract IPv6 address
    def parse_address_aaaa(self, addr_len, addr_bytes):
        resp_addr = []
        # put bytes into a list
        for i in range(0, addr_len, 2):
            resp_addr.append((addr_bytes[i] << 8) + addr_bytes[i+1])
        resp_addr = ':'.join(str(hex(x)) for x in resp_addr)

        return resp_addr.replace('0x', '')

    # Split a value into 2 bytes
    def val_to_2_bytes(self, value):
        byte_1 = (value & 0xff00) >> 8
        byte_2 = value & 0x00ff

        return [byte_1, byte_2]
    # Split a value into 2 bytes
    def val_to_n_bytes(self, value, n_bytes):
        result = []
        for s in range(n_bytes):
            byte = (value & (0xff << (8 * s))) >> (8 * s)
            result.insert(0, byte)

        return result
    # Merge 2 bytes into a value
    def bytes_to_val(self, bytes_lst):
        value = 0
        for b in bytes_lst:
            value = (value << 8) + b

        return value
    # Extract first two bits of a two-byte sequence
    def get_2_bits(self, bytes):
        return bytes[0] >> 6
    # Extract size of the offset from a two-byte sequence
    def get_offset(self, bytes):
        return ((bytes[0] & 0x3f) << 8) + bytes[1]

file = open('hosts.txt', 'r')

known_domains = {}
source = file.readline().split()[1]
TTL = file.readline().split()[1]

line = file.readline()
previous_key = None
str_digit = ['0','1','2','3','4','5','6','7','8','9']

while line != "":
    linelist = line.split()
    if linelist[0][0] not in str_digit and linelist[0] != "IN":
        domain = linelist.pop(0)
        if len(linelist) == 3:
            linelist.insert(0, TTL)
        known_domains[domain] = [linelist]
        previous_key = domain

    else:
        if linelist[0][0] in str_digit:
            known_domains[previous_key].append(linelist)
        else:
            if len(linelist) == 3:
                linelist.insert(0, TTL)
            known_domains[previous_key].append(linelist)

    line = file.readline()


HOST = 'localhost'
PORT = 43053

if __name__ == "__main__":
    d = DNSServer()
    server_sckt = socket(AF_INET, SOCK_DGRAM)
    server_sckt.bind((HOST, PORT))
    print("%s " % (HOST) + "Listening on %s: %d" % (HOST, PORT))

    while True:
        d.msg_qry = bytearray()
        (msg, client_addr) = server_sckt.recvfrom(2048)
        d.parse_response(msg)
        d.format_response()

        # keylist = []
        # for key in d.dict:
        #     keylist.append(key)
        #
        # keylist.sort()
        # for key in keylist:
        #     print(key, d.dict[key])

        server_sckt.sendto(d.msg_qry, client_addr)


    server_sckt.close()
