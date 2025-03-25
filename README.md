
# Custom Ping Utility

## **Objective**
The goal of this assignment is to develop a custom **ping utility** that replicates the basic functionality of the standard `ping` tool. This tool will allow users to test network reachability and measure round-trip time (RTT) for packets sent to a target IP address.

## Setup & Installation

### Prerequisites
- **Python 3.6+** (tested on 3.8+)
- **Linux/macOS** (requires root privileges for raw sockets)
- `sudo` access

### Installation
1. Clone the repository :
   ```sh
   git clone https://github.com/yourusername/custom-ping-utility.git
   cd custom-ping-utility
   ```
 2. Run the test file through makefile (for linux and macOS)
    ```sh
    sudo make test
    ```

## Usages

### Basic usage
1.Ping an IPv4 Address (Default)
```sh
sudo python3 src/main.py 8.8.8.8
```
 Sends 4 ICMP echo requests (default count) to the IPv4 address 8.8.8.8.


2.Ping an IPv6 Address
```sh
sudo python3 src/main.py 2001:4860:4860::8888 -6
```
Sends 4 ICMPv6 echo requests to the IPv6 address 2001:4860:4860::8888.

### Custom Packet Count
Send 10 Packets
```sh
sudo python3 src/main.py 8.8.8.8 -c 10
```
Sends 10 ICMP echo requests to 8.8.8.8

### Custom TTL (Time-To-Live)
```sh
sudo python3 src/main.py 8.8.8.8 -t 128
```
Sends ICMP echo requests with a TTL of 128

### Specify Network Interface

```sh
sudo python3 src/main.py 127.0.0.1 -I lo
```
Sends ICMP echo requests to 127.0.0.1 using the lo (loopback) interface , 
or can use eth0 etc.

### Invalid IP Address
Test Error Handling
```sh
sudo python3 src/main.py invalid.ip.address
```

### Help Message
Displays the help message with all available command-line arguments

```sh
python3 src/main.py -h
```

## Versions and Dependencies required
1. Ensure Python 3.6+ is installed on your system. You can check the installed version using:
```sh
python3 --version
```
2. Ensure you have sudo access to run the utility:
```sh
sudo -v
```



   
