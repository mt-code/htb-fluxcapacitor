# HTB FluxCapacitor

## About
Python script that automates a back-connect shell on the HackTheBox machine **FluxCapacitor**.

Exploits a command injection vulnerability, that involves simple WAF bypass techniques.

## Requirements
Requires netcat to be installed on your system and installed to your $PATH as **nc**

## Usage
Specify the host and port you wish to listen on:

`htb-fluxcapacitor.py {LHOST} {LPORT}`