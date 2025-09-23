FROM python:3.12-alpine AS build-font

WORKDIR /app

RUN pip install --no-cache-dir tox

COPY pyproject.toml .

COPY *.py .
COPY symbols.json .
COPY symbols symbols

RUN python -m tox -e build

FROM node:current-alpine AS build-website

WORKDIR /app

COPY website/package.json .
COPY website/pnpm-lock.yaml .

RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY website/static static
COPY website/src src
COPY website/svelte.config.js .
COPY website/tsconfig.json .
COPY website/vite.config.ts .

COPY symbols.json src/lib/

COPY --from=build-font /app/dist ./static/font

RUN pnpm run build

FROM caddy:alpine AS prod

COPY ./Caddyfile /etc/caddy/Caddyfile

COPY --from=build-website /app/build /usr/share/caddy
