# 📈 Real-Time OFS Tracker

A high-performance full-stack application built to track live Offer for Sale (OFS) bids across both the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) in real-time.

This application actively polls the exchanges and combines the bid/ask ladder data into a unified, sorted, and beautiful dashboard, elegantly separating **Non-Retail (Day 1)** and **Retail (Day 2)** investor streams.

## ✨ Features
- **Real-Time Polling**: Natively queries deep-ladder exchange APIs every 15 seconds.
- **Unified Exchange Ladder**: Automatically combines and sorts NSE and BSE bid arrays into a single, cohesive table.
- **Categorization**: Dedicated tracking tabs for Non-Retail and Retail investor types.
- **Intelligent Graceful Fallbacks**: Smartly handles Day 1 empty Retail API states without crashing data collection streams.
- **Containerized Architecture**: 100% Dockerized for instant, zero-configuration local deployments.

## 🏗️ Tech Stack
- **Frontend**: Next.js, React, TailwindCSS, React Query
- **Backend**: FastAPI (Python), SQLAlchemy, APScheduler
- **Database**: SQLite (Local persistent storage)
- **Deployment**: Docker Compose

## 🚀 Running Locally

The entire stack is containerized. To run it on your machine, simply use Docker Compose:

```bash
git clone <your-repo-url>
cd ofs-tracker
docker-compose up --build
```

The frontend dashboard will be instantly available at `http://localhost:3000`.

## ☁️ Deploying to Railway.app

This application is designed to be easily deployed to PaaS providers like [Railway](https://railway.app) for on-demand OFS tracking.

1. Connect your GitHub repository to Railway to automatically deploy the Docker Compose stack.
2. **Crucial Step**: Because the application utilizes an internal SQLite database (`ofs_tracker.db`), you **must** attach a Persistent Volume to the Backend container to ensure data is not wiped when the server sleeps.
3. In Railway > Backend Settings > Volumes, add a volume and set the Mount Path to exactly: `/app`.

This guarantees your collected data remains perfectly safe across the entire 48-hour OFS cycle!
