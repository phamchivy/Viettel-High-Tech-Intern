from scapy.all import *

# Địa chỉ IP giả lập của mạng lõi 5G
dst_ip = "192.168.1.100"

# Tạo gói tin UDP (GTP-U traffic)
packet = IP(dst=dst_ip) / UDP(sport=2152, dport=2152) / Raw(load="Fake GTP-U Traffic")

# Gửi gói tin liên tục (10 gói)
send(packet, count=10, inter=0.1)
