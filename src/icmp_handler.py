# def send_icmp_packet(target_ip):
#     pass

# def receive_icmp_packet():
#     pass


import socket
import struct
import select
import time

# handling ipv4 and ipv6 
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMPV6_ECHO_REQUEST = 128
ICMPV6_ECHO_REPLY = 129

# error checking by using checkSum
def checksum(source_string):
    sum = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count += 2

    if count_to < len(source_string):
        sum += source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    answer = ~sum & 0xffff
    answer = (answer >> 8) | ((answer << 8) & 0xff00) #swapping for icmp
    return answer

#creating icmp packet 
def create_icmp_packet(packet_id, seq, ip_version=4):  #default values are taken accordingly if not provided
    if ip_version == 4:
        icmp_type = ICMP_ECHO_REQUEST
        icmp_code = 0
        header_format = 'bbHHh'  # Signed byte for ICMPv4
    else:
        icmp_type = ICMPV6_ECHO_REQUEST
        icmp_code = 0
        header_format = 'BBHHH'  # Unsigned byte for ICMPv6

    header = struct.pack(header_format, icmp_type, icmp_code, 0, packet_id, seq)
    data = b'abcdefghijklmnopqrstuvwxyzabcdefghi'  # 56 bytes payload

    my_checksum = checksum(header + data)
    header = struct.pack(header_format, icmp_type, icmp_code, socket.htons(my_checksum), packet_id, seq)
    return header + data


# sending the icmp packet which we created
def send_icmp_packet(target_ip, packet_id, seq, ttl=64, interface=None, ip_version=4):
    print(f"Creating socket for {target_ip}...",flush=True)
    
    #creating info n for raw socket
    sock_family = socket.AF_INET6 if ip_version == 6 else socket.AF_INET     
    sock_proto = socket.IPPROTO_ICMPV6 if ip_version == 6 else socket.IPPROTO_ICMP

    try:
        sock = socket.socket(sock_family, socket.SOCK_RAW, sock_proto)
    except PermissionError:
        raise PermissionError("Root privileges are required to create raw sockets")

    print(f"Socket created: {sock}",flush=True)

    sock.settimeout(2) #timeout so that program do not wait for reply for too long
    
    
    #if in option interface is given
    if interface:
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, interface.encode())
        except AttributeError:
            pass  # Not supported on this platform

    
    if ip_version == 4:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    else:
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, ttl)

    packet = create_icmp_packet(packet_id, seq, ip_version)
    start_time = time.time()

    print(f"Sending packet to {target_ip}...",flush=True)
    try:
        sock.sendto(packet, (target_ip, 0))
    except socket.error as e:
        print(f"Error sending packet: {e}",flush=True)
        return None, None

    print("Packet sent successfully.",flush=True)
    return sock, start_time

def receive_icmp_packet(sock, packet_id, ip_version=4, timeout=2):
    print("Waiting for reply...",flush=True)
    time_remaining = timeout
    while True:
        start_time = time.time()
        ready = select.select([sock], [], [], time_remaining) #waiting to gather all info but for 2 sec only
        if not ready[0]:
            print("Timeout waiting for reply.",flush=True)
            return None  # Timeout

        try:
            recv_packet, addr = sock.recvfrom(1024) #recieving packet giving size of 1024
        except socket.error:
            print("Error receiving packet.",flush=True)
            return None

        received_time = time.time()
        

        # Extract the ICMP header based on the IP version
        if ip_version == 4:
            # header starts after the 20-byte 
            icmp_header = recv_packet[20:28]
            
            icmp_type, code, checksum, p_id, seq = struct.unpack('bbHHh', icmp_header)
        
        else:#FOR v6
            # header starts at the beginning of the packet
            icmp_header = recv_packet[0:8]
            
            icmp_type, code, checksum, p_id, seq = struct.unpack('BBHHH', icmp_header)

        if (ip_version == 4 and icmp_type == ICMP_ECHO_REPLY) or (ip_version == 6 and icmp_type == ICMPV6_ECHO_REPLY):
            if p_id == packet_id:
                print(f"Received reply from {addr[0]}",flush=True)
                return received_time

        time_remaining -= (received_time - start_time)
        if time_remaining <= 0:
            print("Timeout waiting for reply.",flush=True)
            return None