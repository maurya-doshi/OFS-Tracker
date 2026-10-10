"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, useMemo } from "react";
import { fetchCombinedLadder, fetchIssues, createIssue, deleteIssue } from "../lib/api";
import { Activity, Clock, Trash2, ArrowDown, ArrowUp } from "lucide-react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Issue {
  id: number;
  exchange: string;
  symbol: string;
  scripcode?: string;
  name: string;
  status: string;
}

interface LadderEntry {
  price: number;
  bids: number;
  confirmed_qty: number;
  unconfirmed_qty: number;
  total_quantity: number;
  cumulative_confirmed: number;
  cumulative_unconfirmed: number;
  cumulative_total: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function toIST(utcStr: string | null | undefined): string | null {
  if (!utcStr) return null;
  const date = new Date(utcStr.endsWith("Z") ? utcStr : utcStr + "Z");
  const timeStr = date.toLocaleTimeString("en-IN", {
    timeZone: "Asia/Kolkata",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  });
  return timeStr;
}

function fmt(n: number | null | undefined): string {
  if (n == null || n === 0) return "—";
  return n.toLocaleString("en-IN");
}

function fmtPrice(p: number): string {
  if (p === 0) return "Cut-off";
  return p.toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

// ── Main Dashboard ───────────────────────────────────────────────────────────

export default function Dashboard() {
  const queryClient = useQueryClient();
  const [investorType, setInvestorType] = useState<"NON_RETAIL" | "RETAIL">("NON_RETAIL");
  const [sortOrder, setSortOrder] = useState<"desc" | "asc">("desc");
  const [newIssue, setNewIssue] = useState({
    exchange: "NSE",
    symbol: "",
    scripcode: "",
    name: "",
    status: "ACTIVE",
  });

  const { data: issues, isLoading: issuesLoading } = useQuery<Issue[]>({
    queryKey: ["issues"],
    queryFn: fetchIssues,
  });

  // Since there will be only one active OFS at a time, we just pick the first one.
  const activeIssue = issues?.[0] || null;

  const addIssueMutation = useMutation({
    mutationFn: createIssue,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["issues"] });
      setNewIssue({ exchange: "NSE", symbol: "", scripcode: "", name: "", status: "ACTIVE" });
    },
  });

  const deleteIssueMutation = useMutation({
    mutationFn: deleteIssue,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["issues"] });
    },
  });

  const handleAddIssue = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newIssue.symbol || !newIssue.scripcode) return;
    addIssueMutation.mutate(newIssue);
  };

  const { data: ladderData, isLoading: ladderLoading } = useQuery({
    queryKey: ["ladder", activeIssue?.symbol, investorType],
    queryFn: () => fetchCombinedLadder(activeIssue!.symbol, investorType),
    refetchInterval: 15000,
    enabled: !!activeIssue,
  });

  const nseUpdatedText = useMemo(() => toIST(ladderData?.nse_last_updated), [ladderData?.nse_last_updated]);
  const bseUpdatedText = useMemo(() => toIST(ladderData?.bse_last_updated), [ladderData?.bse_last_updated]);

  const displayLadder = useMemo<LadderEntry[]>(() => {
    if (!ladderData?.ladder) return [];
    return [...ladderData.ladder].sort((a: LadderEntry, b: LadderEntry) =>
      sortOrder === "desc" ? b.price - a.price : a.price - b.price
    );
  }, [ladderData, sortOrder]);

  return (
    <div className="min-h-[100dvh] bg-[#141312] text-[#e8e6e3] font-sans selection:bg-[#8ba888]/30 overflow-x-hidden">
      <div className="max-w-[1600px] mx-auto p-6 md:p-12 lg:p-16 flex flex-col lg:flex-row gap-12 lg:gap-20 items-start">
        
        {/* ── LEFT PANE: LADDER (Bigger) ──────────────────────────────────── */}
        <main className="flex-[2.5] w-full order-2 lg:order-1">
          <header className="mb-10 flex items-center justify-between">
            <h1 className="text-3xl md:text-4xl font-medium tracking-tight text-[#f2f1ef]">
              Live Order Book
            </h1>
          </header>

          {!activeIssue ? (
            <div className="py-20 text-[#888682] text-lg font-light">
              Awaiting instrument provision. Configure active OFS in the control panel.
            </div>
          ) : ladderLoading ? (
            <div className="animate-pulse space-y-4">
              {Array.from({ length: 10 }).map((_, i) => (
                <div key={i} className="h-10 bg-[#1c1c1a] rounded-sm w-full" style={{ opacity: 1 - i * 0.08 }} />
              ))}
            </div>
          ) : displayLadder.length > 0 ? (
            <div className="min-w-[900px] pb-10">
              {/* Header */}
              <div className="grid grid-cols-8 gap-6 mb-4 pb-4 border-b border-[#2a2a28] text-[#888682] text-[11px] font-medium uppercase tracking-widest sticky top-0 bg-[#141312] z-10">
                <div 
                  className="col-span-1 cursor-pointer flex items-center gap-2 hover:text-[#d4a373] transition-colors select-none"
                  onClick={() => setSortOrder(s => (s === "desc" ? "asc" : "desc"))}
                >
                  Price (₹) {sortOrder === "desc" ? <ArrowDown size={14} /> : <ArrowUp size={14} />}
                </div>
                <div className="col-span-1 text-right">Bids</div>
                <div className="col-span-1 text-right">Qty (Conf)</div>
                <div className="col-span-1 text-right opacity-60">Qty (Unconf)</div>
                <div className="col-span-1 text-right text-[#e8e6e3]">Total Qty</div>
                <div className="col-span-1 text-right">Cum (Conf)</div>
                <div className="col-span-1 text-right opacity-60">Cum (Unconf)</div>
                <div className="col-span-1 text-right text-[#e8e6e3]">Total Cum</div>
              </div>

              {/* Data Rows */}
              <div className="flex flex-col">
                {displayLadder.map((row, idx) => {
                  const isCutoff = row.price === 0;
                  const highlightCutoff = isCutoff && investorType === "RETAIL";

                  return (
                    <div
                      key={idx}
                      className={`grid grid-cols-8 gap-6 py-3.5 border-b border-[#1c1c1a] text-[15px] items-center transition-colors tabular-nums ${
                        highlightCutoff 
                          ? "bg-[#8ba888]/10 !border-[#8ba888]/30 rounded-sm -mx-2 px-2" 
                          : "hover:bg-[#1a1918] -mx-2 px-2 rounded-sm"
                      }`}
                    >
                      <div className={`col-span-1 font-mono font-medium ${highlightCutoff ? "text-[#a3c2a0]" : "text-[#cfa374]"}`}>
                        {fmtPrice(row.price)}
                      </div>
                      <div className={`col-span-1 text-right ${highlightCutoff ? "text-[#8ba888]" : "text-[#a09e9a]"}`}>
                        {fmt(row.bids)}
                      </div>
                      <div className={`col-span-1 text-right ${highlightCutoff ? "text-[#a3c2a0] font-medium" : "text-[#d0cec9]"}`}>
                        {fmt(row.confirmed_qty)}
                      </div>
                      <div className={`col-span-1 text-right ${highlightCutoff ? "text-[#8ba888]" : "text-[#7a7874]"}`}>
                        {fmt(row.unconfirmed_qty)}
                      </div>
                      <div className={`col-span-1 text-right font-medium ${highlightCutoff ? "text-[#bfe0bc]" : "text-[#f2f1ef]"}`}>
                        {fmt(row.total_quantity)}
                      </div>
                      <div className={`col-span-1 text-right ${highlightCutoff ? "text-[#a3c2a0] font-medium" : "text-[#d0cec9]"}`}>
                        {fmt(row.cumulative_confirmed)}
                      </div>
                      <div className={`col-span-1 text-right ${highlightCutoff ? "text-[#8ba888]" : "text-[#7a7874]"}`}>
                        {fmt(row.cumulative_unconfirmed)}
                      </div>
                      <div className={`col-span-1 text-right font-medium ${highlightCutoff ? "text-[#bfe0bc]" : "text-[#f2f1ef]"}`}>
                        {fmt(row.cumulative_total)}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="py-20 text-[#888682] text-lg font-light flex items-center gap-4">
              <Activity className="animate-pulse opacity-50" />
              Waiting for order book execution...
            </div>
          )}
        </main>

        {/* ── RIGHT PANE: ACTIVE OFS / CONTROLS (Smaller) ─────────────────── */}
        <aside className="flex-[1] w-full order-1 lg:order-2 lg:sticky lg:top-16 flex flex-col gap-10">
          
          {/* Active OFS Panel */}
          {issuesLoading ? (
            <div className="h-40 bg-[#1c1c1a] rounded-sm animate-pulse" />
          ) : activeIssue ? (
            <div className="flex flex-col gap-8">
              <div>
                <div className="flex items-start justify-between mb-2">
                  <h2 className="text-4xl md:text-5xl font-light tracking-tight text-[#f2f1ef]">
                    {activeIssue.symbol}
                  </h2>
                  <button
                    onClick={() => deleteIssueMutation.mutate(activeIssue.id)}
                    className="text-[#7a7874] hover:text-[#e87a7a] transition-colors p-2 -mr-2"
                    title="Remove active OFS"
                  >
                    <Trash2 size={20} strokeWidth={1.5} />
                  </button>
                </div>
                <div className="text-[#a09e9a] font-medium tracking-wide">
                  {activeIssue.scripcode || "N/A"}
                </div>
              </div>

              {/* Type Toggle */}
              <div className="flex bg-[#1c1c1a] p-1 rounded-sm shadow-inner">
                <button
                  onClick={() => setInvestorType("NON_RETAIL")}
                  className={`flex-1 py-2.5 text-sm font-medium tracking-wide transition-all ${
                    investorType === "NON_RETAIL"
                      ? "bg-[#2a2a28] text-[#f2f1ef] shadow-sm"
                      : "text-[#888682] hover:text-[#d0cec9]"
                  }`}
                >
                  Non-Retail
                </button>
                <button
                  onClick={() => setInvestorType("RETAIL")}
                  className={`flex-1 py-2.5 text-sm font-medium tracking-wide transition-all ${
                    investorType === "RETAIL"
                      ? "bg-[#2a2a28] text-[#f2f1ef] shadow-sm"
                      : "text-[#888682] hover:text-[#d0cec9]"
                  }`}
                >
                  Retail
                </button>
              </div>

              {/* Telemetry / Updates */}
              <div className="flex flex-col gap-3 pt-6 border-t border-[#2a2a28]">
                <h3 className="text-[11px] font-medium text-[#7a7874] uppercase tracking-widest mb-1">
                  Exchange Telemetry
                </h3>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[#888682] flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#8ba888]" /> NSE Sync
                  </span>
                  <span className="text-[#d0cec9] tabular-nums font-mono">
                    {nseUpdatedText || "—"}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[#888682] flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#cfa374]" /> BSE Sync
                  </span>
                  <span className="text-[#d0cec9] tabular-nums font-mono">
                    {bseUpdatedText || "—"}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            /* Add Issue Form */
            <div className="flex flex-col gap-6">
              <div>
                <h2 className="text-2xl font-light tracking-tight text-[#f2f1ef] mb-1">
                  Track OFS
                </h2>
                <p className="text-[#888682] text-sm">Deploy a new instrument to the dashboard.</p>
              </div>
              
              <form onSubmit={handleAddIssue} className="flex flex-col gap-4">
                <div className="space-y-2">
                  <label className="text-[11px] font-medium text-[#7a7874] uppercase tracking-widest">
                    NSE Symbol
                  </label>
                  <input
                    required
                    type="text"
                    value={newIssue.symbol}
                    onChange={(e) =>
                      setNewIssue({ ...newIssue, symbol: e.target.value.toUpperCase(), name: e.target.value.toUpperCase() })
                    }
                    className="w-full bg-[#1c1c1a] border border-[#2a2a28] rounded-sm px-4 py-3 text-[#f2f1ef] placeholder-[#5a5855] focus:border-[#d4a373] outline-none transition-colors"
                    placeholder="e.g. COCHINSHIP"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-[11px] font-medium text-[#7a7874] uppercase tracking-widest">
                    BSE Scripcode
                  </label>
                  <input
                    required
                    type="text"
                    value={newIssue.scripcode}
                    onChange={(e) => setNewIssue({ ...newIssue, scripcode: e.target.value })}
                    className="w-full bg-[#1c1c1a] border border-[#2a2a28] rounded-sm px-4 py-3 text-[#f2f1ef] placeholder-[#5a5855] focus:border-[#d4a373] outline-none transition-colors"
                    placeholder="e.g. 540678"
                  />
                </div>
                
                <button
                  type="submit"
                  disabled={addIssueMutation.isPending || !newIssue.symbol || !newIssue.scripcode}
                  className="mt-2 w-full bg-[#e8e6e3] hover:bg-white text-[#141312] py-3.5 rounded-sm font-medium transition-colors disabled:opacity-50"
                >
                  {addIssueMutation.isPending ? "Connecting..." : "Initialize Tracker"}
                </button>
              </form>
            </div>
          )}
        </aside>

      </div>
    </div>
  );
}
