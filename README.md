# arp_checker

During the initial connection to cisco_ios device the script will create and update arp_table file.

To run the script type ./get_arp.py <ip_address>

Thereafter, the actual arp-table from the device will be compared with the one in arp_table file.
The difference between the data will be logged in arp_table_log file and notified via email.


Requirements:

python3.8,
netmiko 3.3.0,
python-dotenv 3.3.0,
