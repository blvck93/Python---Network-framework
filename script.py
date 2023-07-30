#!/usr/bin/env python3

import functions

def main():
    device1 = functions.network("admin", "admin", "10.10.10.10", "cisco_asa")
#    device1.execute_command("show run config")
    device1.send_syslog("127.0.0.1", "test", 514)

if __name__ == "__main__":
    # Call the main function
    main()