# ===========================
# Stage 1 — Build React App
# ===========================
FROM node:18-alpine AS builder

# Install CA certificates for SSL verification
RUN apk add --no-cache bash ca-certificates

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source code
COPY . .

# Build the React/Vite app
RUN npm run build

# ===========================
# Stage 2 — Serve via Nginx
# ===========================
FROM nginx:alpine

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose default HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
