"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Github, Linkedin, Box } from "lucide-react"

interface AnalysisResult {
  company_name?: string
  percent_change?: string
  percent_change_2y?: string
  percent_change_6mo?: string
  pe_ratio?: string
  trailing_pe_ratio?: string
  bull_flag_detection?: string
  flagpole_change?: string
  flag_change?: string
  bull_flag_status?: string
  volume?: string
  current_volume?: string
  average_volume?: string
  volume_change?: string
  volume_analysis?: string
  score?: number
  error?: string
}

export default function StockAnalysisPage() {
  const [ticker, setTicker] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)

  const handleAnalyze = async () => {
    if (!ticker.trim()) return

    setIsAnalyzing(true)
    setResult(null)

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ticker: ticker.toUpperCase() }),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data?.error || "Stock analysis failed")
      }
      setResult(data)
    } catch (error) {
      console.error("Error analyzing stock:", error)
      setResult({ error: "Failed to analyze stock. Verify Python is installed and backend dependencies are set up." })
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleAnalyze()
    }
  }

  return (
    <div className="min-h-screen text-white">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-block border-2 border-white rounded-lg px-8 py-4 mb-6">
            <h1 className="text-4xl font-bold tracking-wider text-white">STOCK ANALYSIS</h1>
          </div>
          <p className="text-lg text-gray-200 max-w-2xl mx-auto leading-relaxed">
            Get a scored <em className="text-gray-200">evaluation</em> of any stock, bond, ETF, or mutual fund. Analysis
            will vary based on investment vehicle.
          </p>
        </div>

        {/* Input Section */}
        <div className="max-w-md mx-auto mb-8">
          <div className="flex flex-col gap-4">
            <Input
              type="text"
              placeholder="Enter Ticker... (ex. RBLX)"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              onKeyDown={handleKeyPress}
              className="bg-white/10 border-white/20 text-white placeholder:text-gray-300 text-center py-3 text-lg"
              disabled={isAnalyzing}
            />
            <Button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !ticker.trim()}
              className="bg-transparent border-2 border-white text-white hover:bg-white hover:text-slate-900 py-3 text-lg font-semibold tracking-wider transition-all duration-200"
            >
              {isAnalyzing ? "ANALYZING..." : "ANALYZE"}
            </Button>
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="max-w-2xl mx-auto mb-8">
            <Card className="bg-gray-200 text-black p-6">
              {result.error ? (
                <div className="text-red-600 text-center">
                  <p className="font-semibold">Error:</p>
                  <p>{result.error}</p>
                </div>
              ) : (
                <div className="space-y-2 font-mono text-sm">
                  <p>Data for ${ticker.toUpperCase()} received.</p>
                  {result.company_name && <p>Company Name: {result.company_name}</p>}
                  <p>--------------------------------</p>

                  {result.percent_change && (
                    <>
                      <p>Percent Change: {result.percent_change}</p>
                      {result.percent_change_2y && <p>Percent Change over 2y: {result.percent_change_2y}</p>}
                      {result.percent_change_6mo && <p>Percent Change over 6mo: {result.percent_change_6mo}</p>}
                      <p>--------------------------------</p>
                    </>
                  )}

                  {result.pe_ratio && (
                    <>
                      <p>P/E Ratio: {result.pe_ratio}</p>
                      {result.trailing_pe_ratio && <p>Trailing PE Ratio: {result.trailing_pe_ratio}</p>}
                      <p>--------------------------------</p>
                    </>
                  )}

                  {result.bull_flag_detection && (
                    <>
                      <p>Bull Flag Detection:</p>
                      {result.flagpole_change && <p>Flagpole change: {result.flagpole_change}</p>}
                      {result.flag_change && <p>Flag change: {result.flag_change}</p>}
                      {result.bull_flag_status && <p>{result.bull_flag_status}</p>}
                      <p>--------------------------------</p>
                    </>
                  )}

                  {result.volume && (
                    <>
                      <p>Volume:</p>
                      {result.current_volume && result.average_volume && (
                        <p>
                          Current Stock Volume: {result.current_volume}. Average Volume: {result.average_volume}
                        </p>
                      )}
                      {result.volume_change && (
                        <p>
                          ${ticker.toUpperCase()} volume change is {result.volume_change}.
                        </p>
                      )}
                      {result.volume_analysis && <p>{result.volume_analysis}</p>}
                    </>
                  )}
                </div>
              )}
            </Card>

            {result.score !== undefined && !result.error && (
              <div className="text-center mt-6">
                <div className="inline-block bg-gray-300 text-black px-6 py-3 rounded-lg">
                  <span className="text-2xl font-bold">Score: {result.score}/100</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="flex flex-col items-center gap-6 mt-16">
          <div className="flex justify-between items-end w-full max-w-md">
            {/* Ro's buttons group */}
            <div className="flex items-end gap-3">
              <a
                href="https://github.com/ro-the-creator"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity"
              >
                <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center">
                  <Github className="w-6 h-6 text-white" />
                </div>
                <span className="text-sm text-white">Ro's GitHub</span>
              </a>

              <a
                href="https://www.linkedin.com/in/romaro/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity"
              >
                <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center">
                  <Linkedin className="w-6 h-6 text-white" />
                </div>
                <span className="text-sm text-white">Ro's LinkedIn</span>
              </a>
            </div>

            {/* Slinky's buttons group */}
            <div className="flex items-end gap-3">
              <a
                href="https://www.linkedin.com/in/nicole-blanchette/"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity"
              >
                <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center">
                  <Linkedin className="w-6 h-6 text-white" />
                </div>
                <span className="text-sm text-white">Slinky's LinkedIn</span>
              </a>

              <a
                href="https://github.com/nicoleblanchette"
                target="_blank"
                rel="noopener noreferrer"
                className="flex flex-col items-center gap-2 hover:opacity-80 transition-opacity"
              >
                <div className="w-12 h-12 bg-white/10 rounded-full flex items-center justify-center">
                  <Github className="w-6 h-6 text-white" />
                </div>
                <span className="text-sm text-white">Slinky's GitHub</span>
              </a>
            </div>
          </div>

          <a
            href="https://github.com/ro-the-creator/Stocks-Analysis-Project"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:opacity-80 transition-opacity"
          >
            <div className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center">
              <Box className="w-4 h-4 text-white" />
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}
