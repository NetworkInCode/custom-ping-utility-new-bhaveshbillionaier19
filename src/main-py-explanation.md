# Custom Ping Utility Breakdown

## 1. Argument Parsing
```python
parser = argparse.ArgumentParser(description='Custom Ping Utility')
parser.add_argument('target', help='Target IP address')
parser.add_argument('-c', '--count', type=int, default=4, help='Number of packets to send') 
parser.add_argument('-t', '--ttl', type=int, default=64, help='Time-To-Live value')
parser.add_argument('-I', '--interface', help='Network interface to use')
parser.add_argument('-6', '--ipv6', action='store_true', help='Use IPv6')
args = parser.parse_args()
```
- This section sets up command-line argument parsing
- Allows users to specify:
  - Target IP address (required)
  - Number of packets to send (default 4)
  - Time-to-Live (TTL) value (default 64)
  - Specific network interface (optional)
  - IPv6 mode (optional)

## 2. Packet Preparation
```python
packet_id = os.getpid() & 0xFFFF
ip_version = 6 if args.ipv6 else 4
seq = 1
rtt_list = []
```
- Generates a unique packet ID using process ID
- Determines IP version based on user input
- Initializes sequence number and RTT (Round-Trip Time) list
- Bitwise AND with 0xFFFF ensures 16-bit packet ID

## 3. Packet Sending and Receiving Loop
```python
for _ in range(args.count):
    sock, start_time = send_icmp_packet(
        args.target, packet_id, seq, args.ttl, args.interface, ip_version
    )
    if not sock:
        print("Failed to send packet.")
        rtt_list.append(None)
        seq += 1
        continue

    reply_time = receive_icmp_packet(sock, packet_id, ip_version)
    sock.close()

    if reply_time is not None:
        rtt = (reply_time - start_time) * 1000
        print(f"Reply from {args.target}: time={rtt:.2f}ms")
        rtt_list.append(rtt)
    else:
        print("Request timed out.")
        rtt_list.append(None)
    seq += 1
```
### Uses two key functions from `icmp_handler.py`:
1. `send_icmp_packet()`:
   - Creates and sends ICMP packet
   - Returns socket and start time
   - Handles both IPv4 and IPv6
   - Allows setting TTL and network interface

2. `receive_icmp_packet()`:
   - Receives ICMP reply
   - Checks for matching packet ID
   - Returns receive time if successful
   - Returns None if no reply or timeout

### Loop Flow:
- Sends specified number of packets
- Calculates Round-Trip Time (RTT)
- Tracks successful and failed packet attempts
- Increments sequence number for each packet

## 4. Statistics Calculation
```python
successful_rtt = [rtt for rtt in rtt_list if rtt is not None]
packet_sent = args.count
packet_received = len(successful_rtt)
packet_loss = (1 - (packet_received / packet_sent)) * 100 if packet_sent else 0
```
- Filters out successful RTT measurements
- Calculates:
  - Total packets sent
  - Packets received
  - Packet loss percentage

## 5. Results Output
```python
print(f"{packet_sent} packets transmitted, {packet_received} received, {packet_loss:.2f}% packet loss")

if successful_rtt:
    min_rtt = min(successful_rtt)
    max_rtt = max(successful_rtt)
    avg_rtt = sum(successful_rtt) / len(successful_rtt)
    std_dev = math.sqrt(sum((x - avg_rtt) ** 2 for x in successful_rtt) / len(successful_rtt))

    print(f"Minimum RTT: {min_rtt:.2f}ms")
    print(f"Maximum RTT: {max_rtt:.2f}ms")
    print(f"Average RTT: {avg_rtt:.2f}ms")
    print(f"Standard Deviation: {std_dev:.2f}ms")
else:
    print("No responses received.")
```
- Displays comprehensive ping statistics
- Calculates:
  - Minimum RTT
  - Maximum RTT
  - Average RTT
  - Standard Deviation of RTT
