# Sử dụng image Node.js chính thức
FROM node:18

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy file package.json và cài đặt dependencies
COPY package.json ./
RUN npm install

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 8080
EXPOSE 8080

# Chạy ứng dụng
CMD ["npm", "start"]
