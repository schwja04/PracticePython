#!/usr/bin/env python3
#encoding: UTF-8

from socket import *

HOST = "localhost"
PORT = 43053
VERSION = "0.0.1"

time_to_sec = {'1s':1, '1m':60, '1h':3600, '1d':86400, '1w':604800, '1y':31449600}

class DNServer:
    
    def __init__(self, dictionary):
        self.mesg_resp = bytearray()
        self.RR = dictionary
        
    def ReturnBytes(self):
        return self.mesg_resp
        
    def parse_query(self, msg_resp):
        
        i = 0 # transaction id
        trans_id = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        
        i = 2 # flags
        flags = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        if (flags >> 15) == 1:
            print("Response received")
            
        i = 4 # questions
        questions = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        
        #i = 6 # answers
        #rr_ans = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        #print("Answers: %d" % rr_ans)
        #i = 8 # authority rrs
        #rr_auth = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        #i = 10 # additional rr
        #rr_add = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        
        i = 12 # start of the query
        domain = []
        while msg_resp[i] != 0:
            dom_len = msg_resp[i]
            domain.append(msg_resp[i+1:i+dom_len+1])
            i = i + dom_len + 1
        
        i = i + 1 # type
        qry_type = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        
        i = i + 2 # class
        qry_clss = self.bytes_to_val([msg_resp[i], msg_resp[i+1]])
        if qry_clss != 1:
            raise Exception("Unknown class")
        
        return self.build_response(trans_id, domain, qry_type)
    
    def build_response(self, trans_id, domain, qry_type):
        
        if qry_type != 1 or qry_type != 28: #If qry is not A or AAAA, Reply Code = 4
            flags = 0x8184 #Not implemented
        else:
            flags = 0x8180 
            
        questions = 1
        
        domain_string = domain[3].decode()
        
        domain_string_list = []
        for x in domain:
            domain_string_list.append(x.decode())
        
        rr_ans = 0
        
        if qry_type == 1:
            for x in self.RR[domain_string]:
                if x[2] == 'A':
                    rr_ans += 1
        
        elif qry_type == 28:
            for x in self.RR[domain_string]:
                if x[2] == 'AAAA':
                    rr_ans += 1
            
        rr_auth = 0
        rr_add = 0
        qry_class = 1

        
        self.mesg_resp.append((trans_id & 0xff00) >> 8)
        self.mesg_resp.append(trans_id & 0x00ff)
        self.mesg_resp.append((flags & 0xff00) >> 8)
        self.mesg_resp.append(flags & 0x00ff)
        self.mesg_resp.append((questions & 0xff00) >> 8)
        self.mesg_resp.append(questions & 0x00ff)
        self.mesg_resp.append((rr_ans & 0xff00) >> 8)
        self.mesg_resp.append(rr_ans & 0x00ff)
        self.mesg_resp.append((rr_auth & 0xff00) >> 8)
        self.mesg_resp.append(rr_auth & 0x00ff)
        self.mesg_resp.append((rr_add & 0xff00) >> 8)
        self.mesg_resp.append(rr_add & 0x00ff)
        
        for d in domain_string_list:
            self.mesg_resp.append(len(d))
            for c in d:
                self.mesg_resp.append(ord(c))
                
        self.mesg_resp.append(0)
        self.mesg_resp.append((qry_type & 0xff00) >> 8)
        self.mesg_resp.append(qry_type & 0x00ff)
        self.mesg_resp.append((qry_class & 0xff00) >> 8)
        self.mesg_resp.append(qry_class & 0x00ff)
        
        starting_name = 0xc00c        
        
        if qry_type == 1:
        
            for response in range(0,rr_ans):
            
                self.mesg_resp.append((starting_name & 0xff00) >> 8)
                self.mesg_resp.append(starting_name & 0x00ff)
                
                data_len = 4
                self.mesg_resp.append((qry_type & 0xff00) >> 8)
                self.mesg_resp.append(qry_type & 0x00ff)    
                self.mesg_resp.append((qry_class & 0xff00) >> 8)
                self.mesg_resp.append(qry_class & 0x00ff)
                
                TTL_bytelist = self.val_to_n_bytes(time_to_sec[self.RR[domain_string][response][0]], 4)
                for x in TTL_bytelist:
                    self.mesg_resp.append(x)
                    
                self.mesg_resp.append((data_len & 0xff00) >>8)
                self.mesg_resp.append(data_len & 0x00ff)
                
                IP_num_list = self.RR[domain_string][response][3].split('.')
                for item in IP_num_list:
                    IP_num = int(item)
                    self.mesg_resp.append(IP_num)

                
        elif qry_type == 28:
            
            for response in range(1, rr_ans+1):
                
                self.mesg_resp.append((starting_name & 0xff00) >> 8)
                self.mesg_resp.append(starting_name & 0x00ff)                
                
                AAAAresponse = response * -1
                
                data_len = 16
                self.mesg_resp.append((qry_type & 0xff00) >> 8)
                self.mesg_resp.append(qry_type & 0x00ff)    
                self.mesg_resp.append((qry_class & 0xff00) >> 8)
                self.mesg_resp.append(qry_class & 0x00ff)
                
                TTL_bytelist = self.val_to_n_bytes(time_to_sec[self.RR[domain_string][AAAAresponse][0]], 4)
                for x in TTL_bytelist:
                    self.mesg_resp.append(x)
                    
                self.mesg_resp.append((data_len & 0xff00) >>8)
                self.mesg_resp.append(data_len & 0x00ff)
                
                IP_num_list = self.RR[domain_string][response][3].split(':')
                 
                for item in IP_num_list:
                    IP_num = int(item, 16)
                    self.mesg_resp.append((IP_num & 0xff00) >> 8)   
                    self.mesg_resp.append(IP_num & 0x00ff)
                                
        print(self.mesg_resp)
        
    # Split a value into 2 bytes
    def val_to_2_bytes(self, value):
        byte_1 = (value & 0xff00) >> 8
        byte_2 = value & 0x00ff
        
        return [byte_1, byte_2]
    
    # Split a value into n bytes
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

def CreateRR():
    #server_sckt = socket(AF_INET, SOCK_DGRAM)
    #server_sckt.bind((HOST, PORT))

    file = open('hosts.txt', 'r')
    fileline = file.readline()
    RRecord = fileline.split()
    print("Using Resource Record " + RRecord[1])
    
    fileline = file.readline()
    FindTTL = fileline.split()
    TTLWorld = FindTTL[1]
    
    #Create a dicitonary of lists
    domain_dic = {}
    #previous_key = None
    
    while fileline != "":
        linelist = fileline.split()
        if linelist[0][0] != '1' and linelist[0] != "IN":
            domain_name = linelist.pop(0)
            if len(linelist) == 3:
                linelist.insert(0,TTLWorld)
            domain_dic[domain_name] = [linelist]
            previous_domain = domain_name
        
        else:
            if linelist[0][0] == '1':
                domain_dic[previous_domain].append(linelist)
            
            elif len(linelist) == 3:
                linelist.insert(0, TTLWorld)
                domain_dic[previous_domain].append(linelist)
        
        fileline = file.readline()
    return domain_dic
        
    
        # receive data
        #(msg_req, client_addr) = server_sckt.recvfrom(2048)

    

def main():
    dictionary = CreateRR()
    server_sckt = socket(AF_INET, SOCK_DGRAM)
    server_sckt.bind((HOST, PORT))
    
    while True:
        (msg_req, client_addr) = server_sckt.recvfrom(2048)
        MyServer = DNServer(dictionary)
        MyServer.parse_query(msg_req)
        Message_Response = MyServer.ReturnBytes()
        print(Message_Response)
        server_sckt.sendto(Message_Response, client_addr)
    
    server_sckt.close()
 
if __name__ == "__main__":
    main() 