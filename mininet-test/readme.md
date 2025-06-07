# ⚖️ Load Balancer SDN sử dụng Mininet, OpenFlow và Ryu

## 🎯 Mục tiêu

Xây dựng một hệ thống **Load Balancer** trong mô hình **Software Defined Networking (SDN)** sử dụng:

- **Mininet** để mô phỏng mạng  
- **Open vSwitch (OVS)** để quản lý switch ảo  
- **Ryu Controller** để điều khiển mạng và cân bằng tải  

---

## ⚙️ Cài đặt

- **Mininet** chạy bằng Python 2  
- **Ryu Controller** chạy bằng Python 3  

**Yêu cầu cài đặt:**
```bash
# Cài Mininet (Python 2)
sudo apt install mininet

# Cài Ryu Controller (Python 3)
sudo pip3 install ryu
```

---

## 🧩 Thiết kế mạng

Hệ thống mạng mô phỏng bao gồm:

- 🧠 **1 SDN Controller**: Ryu  
- 🔁 **1 Switch ảo**: Open vSwitch (s1)  
- 🖥️ **3 Server Web**: h1, h2, h3  
- 🧑‍💻 **1 Client**: h4 (gửi request đến Load Balancer)  

---

## 🛠️ Thực hiện

### 1. Tạo Topology mạng

Tạo file `load_balancer_topo.py` để định nghĩa topology gồm switch và 4 host (3 server + 1 client).

```bash
sudo python2 load_balancer_topo.py
```

### 2. Viết Load Balancer Controller

Tạo file `load_balancer.py` để xử lý logic OpenFlow, định tuyến dựa trên Virtual IP (VIP) `10.0.0.10` và phân phối yêu cầu đến các backend server (`h1`, `h2`, `h3`).

Chạy Ryu Controller với module load balancer:

```bash
ryu-manager load_balancer.py
```

---

## 🔎 Kiểm tra hệ thống

1. **Gửi request từ client (h4)**:

```bash
h4 curl 10.0.0.10
```

Mỗi request sẽ được Load Balancer chuyển ngẫu nhiên đến một trong các server: `10.0.0.1`, `10.0.0.2`, `10.0.0.3`

2. **Xem cấu hình Open vSwitch** trong Mininet:

```bash
sh sudo ovs-vsctl show
```

3. **Xem các flow hiện tại** trong switch:

```bash
sudo ovs-ofctl dump-flows s1
```

4. **Thêm một rule mặc định** để xử lý các gói không khớp rule:

```bash
sudo ovs-ofctl -O OpenFlow13 add-flow s1 priority=1,actions=normal
```

---

## 🧠 Chi tiết hoạt động của Load Balancer

- **Địa chỉ IP ảo (VIP)**: `10.0.0.10` được định nghĩa bằng biến `self.virtual_ip` trong `load_balancer.py`
- Khi phát hiện gói tin có **IPv4 destination là VIP**, controller:
  1. **Chọn ngẫu nhiên** một IP backend từ `self.server_ips`
  2. **Ghi flow rule**:
     - Chuyển đổi `ipv4_dst` từ `10.0.0.10` sang IP của server thực
     - Sử dụng hành động `OFPP_NORMAL` để chuyển tiếp bình thường
     - Rule này được ghi vào bảng flow để xử lý các gói tiếp theo hiệu quả hơn

---

## ✅ Kết quả

- Client (`h4`) chỉ cần gửi request đến `10.0.0.10` mà không biết backend server cụ thể.
- Load Balancer (Ryu Controller) sẽ:
  - **Phân phối tải** đều đến các server (h1, h2, h3)
  - **Ẩn thông tin server thật** khỏi client

---

## 📂 File dự án

```
.
├── load_balancer_topo.py     # Mô phỏng mạng bằng Mininet
└── load_balancer.py          # Ryu Controller thực hiện Load Balancing
```

---

## 📘 Tham khảo

- [Mininet Documentation](http://mininet.org/)
- [Ryu SDN Framework](https://osrg.github.io/ryu/)
- [OpenFlow Spec](https://www.opennetworking.org/software-defined-standards/specifications/)
```
