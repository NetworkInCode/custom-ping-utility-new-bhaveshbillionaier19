[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/waUhK5p8)
# Custom Ping Utility

## **Objective**
The goal of this assignment is to develop a custom **ping utility** that replicates the basic functionality of the standard `ping` tool. This tool will allow users to test network reachability and measure round-trip time (RTT) for packets sent to a target IP address.

---

## **Problem Statement**
Your task is to build a **custom ping utility** that performs the following functions:

- **Send ICMP echo requests** to a target IP address.
- **Receive and process ICMP echo replies** from the target.
- **Calculate and display round-trip time (RTT)** for each ICMP echo request-reply cycle.
- **[Bonus] Provide statistics** on:
  - Packet loss
  - Minimum RTT
  - Maximum RTT
  - Average RTT
  - Standard deviation of RTT
- **[Bonus] Provide options** to configure the utility:
  - Choose the network interface for sending packets.
  - Set the Time-To-Live (TTL) value.
  - Support both **IPv4 and IPv6**.

---

## **Repository Setup**
1. **Clone the repository:**
   ```sh
   git clone <repo-link>
   cd custom-ping-utility
   ```
2. **Modify and extend the provided template** according to the requirements.

---

## **Implementation Guidelines**
- Implement socket programming to handle **ICMP (Internet Control Message Protocol) packets**.
- Ensure compatibility with both **Linux and macOS systems**.
- Use appropriate **error handling** to deal with network timeouts, unreachable hosts, and permission issues.
- Structure your code to allow easy extension for bonus features.

---

## **Documentation Requirements**
Your submission must include:
- A **README.md** file with:
  - Clear **setup and installation instructions**.
  - **Usage examples** with command-line arguments.
  - **Required dependencies** and supported versions.
- **Well-documented code** with meaningful comments.
- A **script (`scripts/test.sh`)** to test the functionality of your custom ping utility.

---

## **Example Repository Structure**
```
/ (Root)
│── README.md          # Detailed assignment instructions
│── Makefile           # Build and run commands (if applicable)
│── src/
│   │── main.py        # Main Python script for the ping utility
│   │── icmp_handler.py # ICMP packet handling logic
│── scripts/
│   │── test.sh        # Script to test the program
```

---

## **Resources**
- [What are Ping and Traceroute Really?](https://blog.apnic.net/2021/06/21/what-are-ping-and-traceroute-really/)
- [Socket Programming Guide](https://www.cs.rpi.edu/~moorthy/Courses/os98/Pgms/socket.html)
- [Understanding ICMP and Ping](https://avocado89.medium.com/ping-icmp-32e9eba81623)
- **Socket Programming in Python** (for implementation reference)

---

## **Submission Instructions**
1. Complete your implementation and ensure it meets the assignment requirements.
2. Update the `README.md` with detailed instructions on how to build and run your solution.
3. **Make a pull request (PR)** to submit your final code.
4. Your PR should include:
   - A description of your implementation.
   - Any limitations or known issues.
   - Example test cases demonstrating the tool's functionality.

**Happy coding! 🚀**

