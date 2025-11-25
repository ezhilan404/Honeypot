# Honeypot System

A Python-based honeypot that listens for incoming connections, logs intrusion attempts and presents a fake banner to capture any usernames/passwords the attacker tries.

This project is focused on understanding how attackers probe exposed services, how tools like `nc` and `nmap` behave against open ports, and how basic deception can be used to gather intelligence.

---

## 🔍 Overview

The honeypot exposes a configurable TCP service (fake shell / login prompt).  
Whenever a client connects:

- The honeypot logs the connection (IP, port, timestamp).
- Sends a fake banner / login prompt to the client.
- Captures whatever the attacker types as “username” and “password”.
- Writes all captured data into a log file for later analysis.

> ⚠️ This is for **educational and ethical** use only. Do not deploy against systems or networks you do not own or have explicit permission to monitor.

---

## 🧠 Features

- TCP listener on a configurable host and port
- Fake login banner / prompt for the attacker
- Logs:
  - Source IP and port
  - Timestamp of connection
  - Any attempted credentials (username/password)
- Simple console output + log file for offline analysis

---

## 🧱 Tech Stack

- **Language:** Python
- **Concepts:** TCP sockets, basic intrusion detection, deception, logging
- **Tools used for testing:** `nc` (netcat), `nmap`

---

## 📦 Requirements

- Python 3.x
- (Optional) Virtual environment

If your project uses external Python packages, list them in `requirements.txt` and mention them here.

---

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/ezhilan404/<your-honeypot-repo-name>.git
cd <your-honeypot-repo-name>
