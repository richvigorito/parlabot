# ---- Build stage ----
FROM node:18-alpine AS builder

WORKDIR /app

# Copy deps and install
COPY package*.json ./
RUN npm install

# Copy app
COPY . .

# Force NODE_ENV=production
ENV NODE_ENV=production

# Remove local env if it exists (safety)
RUN rm -f .env.local

# Copy the correct env file to `.env`
COPY .env.production .env

# Build React
RUN npm run build

# ---- Run stage ----
FROM node:18-alpine
RUN npm install -g serve

WORKDIR /app
COPY --from=builder /app/build ./build

EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]

