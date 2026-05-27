import { type NextRequest, NextResponse } from "next/server"
import { execFile } from "node:child_process"
import path from "node:path"
import { promisify } from "node:util"

export const runtime = "nodejs"

const execFileAsync = promisify(execFile)

function getAnalyzerErrorMessage(error: unknown) {
  const execError = error as Error & { code?: string; stderr?: string; killed?: boolean }
  const stderr = execError?.stderr ?? ""

  if (execError?.code === "ENOENT") {
    return "Python 3 is not available on this server. Install Python and ensure python3 is on PATH."
  }

  if (stderr.includes("No module named")) {
    return "Python dependencies are missing. Install them with: python3 -m pip install -r backend/requirements.txt"
  }

  if (execError?.killed) {
    return "Stock analysis timed out. Please try again."
  }

  return "Failed to analyze stock using local Python analyzer."
}

function normalizeAnalyzerResponse(payload: Record<string, unknown>) {
  const finalScoreRaw = typeof payload.final_score === "string" ? payload.final_score : ""
  const scoreMatch = finalScoreRaw.match(/Score:\s*(\d+)/i)
  const parsedScore = scoreMatch ? Number.parseInt(scoreMatch[1], 10) : undefined

  if (typeof payload.fetch_data === "string" && payload.fetch_data.toLowerCase().includes("invalid")) {
    return {
      error: payload.fetch_data,
    }
  }

  return {
    company_name: payload.company_name,
    percent_change: "Historical performance",
    percent_change_2y: payload["2y_change"] !== undefined ? `${payload["2y_change"]}%` : undefined,
    percent_change_6mo: payload["6mo_change"] !== undefined ? `${payload["6mo_change"]}%` : undefined,
    pe_ratio: "Valuation metrics",
    trailing_pe_ratio: payload.trailing_pe,
    bull_flag_detection: "Pattern check",
    flagpole_change: payload.flagpole_change,
    flag_change: payload.flag_change,
    bull_flag_status: payload.bull_flag_detector,
    volume: "Volume check",
    current_volume: payload.volume,
    average_volume: payload.avg_volume,
    volume_change: payload.volume_difference,
    volume_analysis: payload.volume_check,
    score: Number.isFinite(parsedScore) ? parsedScore : undefined,
    warning: payload.warning,
  }
}

export async function POST(request: NextRequest) {
  try {
    const { ticker } = await request.json()
    const cleanTicker = typeof ticker === "string" ? ticker.trim().toUpperCase() : ""

    if (!cleanTicker) {
      return NextResponse.json({ error: "Ticker symbol is required" }, { status: 400 })
    }

    const scriptPath = path.join(process.cwd(), "backend", "Stock_Analyzer.py")
    const { stdout, stderr } = await execFileAsync("python3", [scriptPath, cleanTicker], {
      timeout: 60_000,
      maxBuffer: 1024 * 1024,
    })

    if (stderr?.trim()) {
      console.warn("Stock analyzer stderr:", stderr)
    }

    const parsed = JSON.parse(stdout) as Record<string, unknown>
    return NextResponse.json(normalizeAnalyzerResponse(parsed))
  } catch (error) {
    console.error("Error running backend/Stock_Analyzer.py:", error)
    return NextResponse.json({ error: getAnalyzerErrorMessage(error) }, { status: 500 })
  }
}
