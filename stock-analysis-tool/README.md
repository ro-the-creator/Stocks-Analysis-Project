# Stock Analysis Tool

A Next.js web app that analyzes stock tickers using a local Python engine.

The frontend sends a request to `POST /api/analyze`, and the Next.js API route executes `backend/Stock_Analyzer.py` with `python3` to generate analysis results.

## Quick Start

Run these commands from the project root:

```bash
pnpm install
python3 -m pip install -r backend/requirements.txt
pnpm dev
```

Then open http://localhost:3000

If you use npm instead of pnpm:

```bash
npm install
python3 -m pip install -r backend/requirements.txt
npm run dev
```

## Prerequisites

Install these tools first:

- Node.js 18+ (Node 20 recommended)
- A JavaScript package manager: `pnpm` (recommended) or `npm`
- Python 3.10+
- `pip` for Python package installation

Check versions:

```bash
node -v
python3 --version
pip3 --version
```

## 1. Download the project

Option A: Clone with Git

```bash
git clone <YOUR_REPO_URL>
cd stock-analysis-tool
```

Option B: Download ZIP from GitHub, extract it, then open the extracted `stock-analysis-tool` folder in your terminal.

## 2. Install JavaScript dependencies

Use one package manager only.

With pnpm:

```bash
pnpm install
```

With npm:

```bash
npm install
```

## 3. Install Python dependencies

From the project root:

```bash
python3 -m pip install -r backend/requirements.txt
```

`backend/requirements.txt` includes:

- yfinance
- pandas
- numpy

## 4. Run the app

With pnpm:

```bash
pnpm dev
```

With npm:

```bash
npm run dev
```

Open the app at:

- http://localhost:3000

## 5. Use the app

- Enter a ticker symbol (for example: `AAPL`, `MSFT`, `RBLX`)
- Click **ANALYZE**
- The app will run `backend/Stock_Analyzer.py` through the Next.js API route and show results in the UI

## How it works

- Frontend page: `app/page.tsx`
- API route: `app/api/analyze/route.ts`
- Python analyzer: `backend/Stock_Analyzer.py`

Request flow:

1. Browser sends `POST /api/analyze` with `{ "ticker": "AAPL" }`
2. Next.js route runs `python3 backend/Stock_Analyzer.py AAPL`
3. Python prints JSON
4. Route normalizes response fields and returns JSON to frontend

## Troubleshooting

### `python3` not found

Install Python 3 and make sure `python3` is available on your PATH.

### Python packages missing

Re-run:

```bash
python3 -m pip install -r backend/requirements.txt
```

### Node package manager command not found

Install Node.js from https://nodejs.org, then reopen your terminal.

### Stock request fails in the app

- Confirm you started the Next.js dev server in the project root
- Confirm `backend/Stock_Analyzer.py` exists
- Confirm `python3 backend/Stock_Analyzer.py AAPL` runs successfully in your terminal

## Production build

With pnpm:

```bash
pnpm build
pnpm start
```

With npm:

```bash
npm run build
npm run start
```
