#!/bin/bash
# 🚀 Kanban Orchestrator - Development Server Startup
# Starts both backend (FastAPI) and frontend (SvelteKit) servers

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_PID=""
FRONTEND_PID=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [ -n "$BACKEND_PID" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
        echo -e "${GREEN}✓ Backend stopped${NC}"
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null || true
        echo -e "${GREEN}✓ Frontend stopped${NC}"
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "${GREEN}🚀 Starting Kanban Orchestrator${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start Backend
echo -e "${YELLOW}📦 Starting Backend (FastAPI)...${NC}"
cd "$SCRIPT_DIR/backend"
uv run uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 2

# Check if backend started
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend running on http://localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    exit 1
fi

# Start Frontend
echo -e "${YELLOW}🎨 Starting Frontend (SvelteKit)...${NC}"
cd "$SCRIPT_DIR/frontend"
bun dev &
FRONTEND_PID=$!
sleep 3

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ All servers running!${NC}"
echo -e "   Backend:  ${YELLOW}http://localhost:8000${NC}"
echo -e "   Frontend: ${YELLOW}http://localhost:5173${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "Press ${RED}Ctrl+C${NC} to stop all servers"
echo ""

# Wait for processes
wait
