# 🚀 Cấu Hình Định Tuyến Tĩnh Giữa Ba Router

## 🎯 Mục tiêu

- Mô phỏng mô hình mạng 3 router kết nối với 3 LAN riêng biệt.
- Cấu hình định tuyến tĩnh sao cho các PC trong các LAN có thể **ping tới nhau**.

---

## 🗺️ Sơ đồ mạng

```
              +-----------+          +-----------+          +-----------+
              |  Router1  | -------- |  Router2  | -------- |  Router3  |
              +-----------+          +-----------+          +-----------+
              | 192.168.1.1          | 192.168.2.1          | 192.168.3.1
              | G0/0                G0/0                   G0/0
              |                     |                     |
         192.168.1.0/24       192.168.2.0/24         192.168.3.0/24
```

---

## ⚙️ Cấu hình chi tiết từng Router

> Lưu ý: Cấu hình trên CLI của Cisco Router trong Packet Tracer.

---

### 🔹 Router1 (R1)

```bash
enable
configure terminal
hostname R1

interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface Serial0/0/0
 ip address 10.0.0.1 255.255.255.252
 no shutdown

ip route 192.168.2.0 255.255.255.0 10.0.0.2
ip route 192.168.3.0 255.255.255.0 10.0.0.2
```

---

### 🔹 Router2 (R2)

```bash
enable
configure terminal
hostname R2

interface GigabitEthernet0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown

interface Serial0/0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown

interface Serial0/0/1
 ip address 10.0.0.5 255.255.255.252
 no shutdown

ip route 192.168.1.0 255.255.255.0 10.0.0.1
ip route 192.168.3.0 255.255.255.0 10.0.0.6
```

---

### 🔹 Router3 (R3)

```bash
enable
configure terminal
hostname R3

interface GigabitEthernet0/0
 ip address 192.168.3.1 255.255.255.0
 no shutdown

interface Serial0/0/1
 ip address 10.0.0.6 255.255.255.252
 no shutdown

ip route 192.168.1.0 255.255.255.0 10.0.0.5
ip route 192.168.2.0 255.255.255.0 10.0.0.5
```

---

## 💡 Kiểm tra kết nối

- Gắn mỗi LAN với **1 PC** (PC1, PC2, PC3).
- Cấu hình IP cho các PC:
  - PC1: `192.168.1.10/24`, Gateway: `192.168.1.1`
  - PC2: `192.168.2.10/24`, Gateway: `192.168.2.1`
  - PC3: `192.168.3.10/24`, Gateway: `192.168.3.1`
- Kiểm tra bằng lệnh **ping** từ các PC tới nhau:
  
```bash
ping 192.168.2.10
ping 192.168.3.10
```

✅ Nếu tất cả PC đều **ping được tới nhau** → cấu hình thành công.

---

## 📌 Ghi chú

- Đảm bảo các interface đều `no shutdown`.
- Đặt đúng subnet mask (255.255.255.252 cho serial link).
- Cấu hình định tuyến tĩnh đúng hướng đi gói tin.

---
