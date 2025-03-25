# def main():
#     print("Custom Ping Utility")

# if __name__ == "__main__":
#     main()
import argparse
import time
import math
import os
import socket
import sys
from icmp_handler import send_icmp_packet, receive_icmp_packet

#sudo configuration checking(for debugging purpose)
if os.geteuid() != 0:
    print("Error: This program must be run as root (use sudo)",flush=True)
    exit(1)

# ip format checking
def validate_ip_address(ip, is_ipv6):
    """
    Validate the IP address format.
    """
    try:
        if is_ipv6:
            socket.inet_pton(socket.AF_INET6, ip)
        else:
            socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

# parser used to get values enter by user in terminal
def main():
    parser = argparse.ArgumentParser(description='Custom Ping Utility')
    parser.add_argument('target', help='Target IP address')
    parser.add_argument('-c', '--count', type=int, default=4, help='Number of packets to send')
    parser.add_argument('-t', '--ttl', type=int, default=64, help='Time-To-Live value')
    parser.add_argument('-I', '--interface', help='Network interface to use')
    parser.add_argument('-6', '--ipv6', action='store_true', help='Use IPv6')
    args = parser.parse_args()

    # Validate IP address
    if not validate_ip_address(args.target, args.ipv6):
        print(f"Error: Invalid {'IPv6' if args.ipv6 else 'IPv4'} address: {args.target}", flush=True)
        sys.exit(1)
    
      # debugging purpose
    # print(f"Target IP: {args.target}", flush=True)
    # print(f"Packet count: {args.count}", flush=True)
    # print(f"TTL: {args.ttl}", flush=True)
    # print(f"Interface: {args.interface}", flush=True)
    # print(f"IPv6: {args.ipv6}", flush=True)
    
    
    
    
    
    
    
    
    
    packet_id = os.getpid() & 0xFFFF #getting a unique id for packet and ensuring it is of 16 bits
    ip_version = 6 if args.ipv6 else 4
    seq = 1
    rtt_list = []

    print(f"PING {args.target} using Python with {args.count} packets...",flush=True)

    

    for _ in range(args.count):

        #sending the ICMP packet
        sock, start_time = send_icmp_packet(
            args.target, packet_id, seq, args.ttl, args.interface, ip_version
        )
        if not sock:
            print("Failed to send packet.",flush=True)
            rtt_list.append(None)
            seq += 1
            continue
         

        
        reply_time = receive_icmp_packet(sock, packet_id, ip_version)
        sock.close()

        if reply_time is not None:
            rtt = (reply_time - start_time) * 1000
            print(f"Reply from {args.target}: time={rtt:.2f}ms",flush=True)
            rtt_list.append(rtt)
        else:
            print("Request timed out.",flush=True)
            rtt_list.append(None)
        seq += 1

    # Calculate statistics
    successful_rtt = [rtt for rtt in rtt_list if rtt is not None]
    packet_sent = args.count
    packet_received = len(successful_rtt)
    packet_loss = (1 - (packet_received / packet_sent)) * 100 if packet_sent else 0

    print("\n--- Statistics ---",flush=True)
    print(f"{packet_sent} packets transmitted, {packet_received} received, {packet_loss:.2f}% packet loss",flush=True)
    

    #stats for successful rtts
    if successful_rtt:
        min_rtt = min(successful_rtt)
        max_rtt = max(successful_rtt)
        avg_rtt = sum(successful_rtt) / len(successful_rtt)
        std_dev = math.sqrt(sum((x - avg_rtt) ** 2 for x in successful_rtt) / len(successful_rtt))

        print(f"Minimum RTT: {min_rtt:.2f}ms",flush=True)
        print(f"Maximum RTT: {max_rtt:.2f}ms",flush=True)
        print(f"Average RTT: {avg_rtt:.2f}ms",flush=True)
        print(f"Standard Deviation: {std_dev:.2f}ms",flush=True)
    else:
        print("No responses received.",flush=True)

if __name__ == "__main__":
    main()