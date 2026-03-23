FROM node:22-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build-time env vars (NEXT_PUBLIC_* must be available during next build)
ARG NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSyCd0sodGFRkjblQ-Rhl8cg7tGcRHkOu1QY
ARG NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=ai-agents-go.firebaseapp.com
ARG NEXT_PUBLIC_FIREBASE_PROJECT_ID=ai-agents-go
ARG NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=ai-agents-go.firebasestorage.app
ARG NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=538978391890
ARG NEXT_PUBLIC_FIREBASE_APP_ID=1:538978391890:web:7caad0a5e8334679f0cc8b
ENV NEXT_PUBLIC_FIREBASE_API_KEY=$NEXT_PUBLIC_FIREBASE_API_KEY \
    NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=$NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN \
    NEXT_PUBLIC_FIREBASE_PROJECT_ID=$NEXT_PUBLIC_FIREBASE_PROJECT_ID \
    NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=$NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET \
    NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=$NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID \
    NEXT_PUBLIC_FIREBASE_APP_ID=$NEXT_PUBLIC_FIREBASE_APP_ID

RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8080
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 8080
CMD ["node", "server.js"]
