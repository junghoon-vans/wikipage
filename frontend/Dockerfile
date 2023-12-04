FROM oven/bun:1.0.15-slim AS builder

WORKDIR /app

COPY . .

RUN bun i
RUN bun run build

FROM nginx:alpine3.18

COPY --from=builder /app/build /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
