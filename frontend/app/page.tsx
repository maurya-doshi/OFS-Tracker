"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, useEffect, useMemo } from "react";
import { fetchCombinedLadder, fetchIssues, createIssue, deleteIssue } from "../lib/api";
import { ChevronDown, ChevronUp, Plus, Trash2, Activity } from "lucide-react";

export default function Dashboard() {
  const queryClient = useQueryClient();
  const [exchange, setExchange] = useState("NSE");
  const [issue, setIssue] = useState("");
  const [investorType, setInvestorType] = useState("NON_RETAIL");
  const [isAdding, setIsAdding] = useState(false);
  const [newIssue, setNewIssue] = useState({ exchange: "NSE", symbol: "", scripcode: "", name: "", status: "ACTIVE" });
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc');

  const { data: issues } = useQuery({
    queryKey: ["issues"],
    queryFn: fetchIssues,
  });

  useEffect(() => {
    if (issues && issues.length > 0 && !issue) {
      setIssue(issues[0].symbol);
      setExchange(issues[0].exchange);
    }
  }, [issues, issue]);

  const addIssueMutation = useMutation({
    mutationFn: createIssue,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["issues"] });
      setIsAdding(false);
      setNewIssue({ exchange: "NSE", symbol: "", scripcode: "", name: "", status: "ACTIVE" });
    }
  });

  const deleteIssueMutation = useMutation({
    mutationFn: deleteIssue,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["issues"] });
      setIssue("");
    }
  });

  const handleAddIssue = (e: React.FormEvent) => {
    e.preventDefault();
    addIssueMutation.mutate(newIssue);
  };

  const handleDeleteIssue = () => {
    const selectedIssue = issues?.find((i: any) => i.symbol === issue);
    if (selectedIssue && window.confirm(`Are you sure you want to stop tracking ${selectedIssue.symbol}?`)) {
      deleteIssueMutation.mutate(selectedIssue.id);
    }
  };

  const { data: ladder, dataUpdatedAt } = useQuery({
    queryKey: ["ladder", issue, investorType],
    queryFn: () => fetchCombinedLadder(issue, investorType),
    refetchInterval: 15000,
    enabled: !!issue,
  });

  const lastUpdatedText = useMemo(() => {
    if (!dataUpdatedAt) return "";
    const date = new Date(dataUpdatedAt);
    return `Last updated on ${date.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })} | ${date.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`;
  }, [dataUpdatedAt]);

  const displayLadder = useMemo(() => {
    if (!ladder) return [];
    return [...ladder].sort((a, b) => sortOrder === 'desc' ? b.price - a.price : a.price - b.price);
  }, [ladder, sortOrder]);

  return (
    <div className="min-h-screen p-8 max-w-7xl mx-auto space-y-8">
      <header className="flex justify-between items-center pb-6 border-b border-gray-800">
        <div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500">
            OFS Live Bid Tracker
          </h1>
          <p className="text-gray-400 mt-2">Real-time demand analysis across NSE and BSE</p>
        </div>
        <div className="flex items-center space-x-4">
          {issues && issues.length > 0 ? (
            <div className="flex items-center space-x-2">
              <select 
                value={issue} 
                onChange={(e) => {
                  const selected = issues.find((i: any) => i.symbol === e.target.value);
                  if (selected) {
                    setIssue(selected.symbol);
                    setExchange(selected.exchange);
                  }
                }}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none min-w-[150px]"
              >
                {issues.map((i: any) => (
                  <option key={i.id} value={i.symbol}>{i.symbol}</option>
                ))}
              </select>
              <button 
                onClick={handleDeleteIssue}
                className="p-2 bg-red-600/20 text-red-400 hover:bg-red-600 hover:text-white rounded-lg transition-colors"
                title="Delete Tracking"
                disabled={deleteIssueMutation.isPending}
              >
                <Trash2 size={18} />
              </button>
            </div>
          ) : (
            <span className="text-gray-500">No issues tracked</span>
          )}
          
          <button 
            onClick={() => setIsAdding(!isAdding)}
            className="flex items-center space-x-1 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg transition-colors"
          >
            <Plus size={18} /> <span>Track Issue</span>
          </button>
        </div>
      </header>

      {isAdding && (
        <form onSubmit={handleAddIssue} className="bg-gray-900/80 backdrop-blur-xl border border-gray-800 p-6 rounded-2xl flex items-end gap-4 animate-in fade-in slide-in-from-top-4">
          <div className="flex-1 space-y-1">
            <label className="text-sm text-gray-400">Symbol (NSE)</label>
            <input required type="text" placeholder="e.g. COCHINSHIP" value={newIssue.symbol} onChange={e => setNewIssue({...newIssue, symbol: e.target.value, name: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white" />
          </div>
          <div className="flex-1 space-y-1">
            <label className="text-sm text-gray-400">Scripcode (BSE)</label>
            <input required type="text" placeholder="e.g. 540678" value={newIssue.scripcode} onChange={e => setNewIssue({...newIssue, scripcode: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white" />
          </div>
          <button type="submit" className="bg-green-600 hover:bg-green-500 text-white px-6 py-2 rounded-lg font-medium transition-colors" disabled={addIssueMutation.isPending}>
            {addIssueMutation.isPending ? "Adding..." : "Add"}
          </button>
        </form>
      )}

      {/* Ladder Table (Full Width) */}
      <div className="w-full">
        <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl overflow-x-auto">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center space-x-6">
                  <h2 className="text-xl font-bold text-white">Live Combined Ladder</h2>
                  <div className="flex bg-gray-800 p-1 rounded-lg">
                    <button 
                      onClick={() => setInvestorType("NON_RETAIL")}
                      className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${investorType === "NON_RETAIL" ? "bg-blue-600 text-white shadow" : "text-gray-400 hover:text-white"}`}
                    >
                      Non-Retail
                    </button>
                    <button 
                      onClick={() => setInvestorType("RETAIL")}
                      className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${investorType === "RETAIL" ? "bg-blue-600 text-white shadow" : "text-gray-400 hover:text-white"}`}
                    >
                      Retail
                    </button>
                  </div>
                </div>
                {lastUpdatedText && (
                  <span className="text-sm text-gray-400">{lastUpdatedText}</span>
                )}
              </div>
              {displayLadder && displayLadder.length > 0 ? (
                <table className="w-full text-right text-sm">
                  <thead>
                    <tr>
                      <th 
                        className="py-3 px-4 bg-gray-800 text-gray-300 font-semibold border-b border-gray-700 rounded-tl-lg cursor-pointer hover:bg-gray-700 transition-colors" 
                        rowSpan={2}
                        onClick={() => setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc')}
                        title="Click to sort by price"
                      >
                        <div className="flex items-center justify-start space-x-2">
                          <span>Price Interval</span>
                          {sortOrder === 'desc' ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
                        </div>
                      </th>
                      <th className="py-2 px-4 bg-[#1a2347] text-white font-semibold border-b border-gray-700 text-center" colSpan={4}>QUANTITY</th>
                      <th className="py-2 px-4 bg-[#1a2347] text-white font-semibold border-b border-gray-700 rounded-tr-lg text-center" colSpan={3}>CUMULATIVE QUANTITY</th>
                    </tr>
                    <tr>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">No. of Bids</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Confirmed</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Yet to be confirmed</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Total</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Confirmed</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Yet to be confirmed</th>
                      <th className="py-2 px-4 bg-[#1e2a57] text-gray-300 font-medium border-b border-gray-700 text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {displayLadder.map((row: any, idx: number) => (
                      <tr key={idx} className="hover:bg-gray-800/50 transition-colors border-b border-gray-800/50">
                        <td className="py-3 px-4 text-blue-400 font-medium text-left">
                          {row.price === 0 ? "Cut-off" : row.price.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                        </td>
                        <td className="py-3 px-4 text-gray-300">{row.bids === 0 ? "-" : row.bids.toLocaleString()}</td>
                        <td className="py-3 px-4 text-gray-300">{row.confirmed_qty === 0 ? "-" : row.confirmed_qty.toLocaleString()}</td>
                        <td className="py-3 px-4 text-gray-300">{row.unconfirmed_qty === 0 ? "-" : row.unconfirmed_qty.toLocaleString()}</td>
                        <td className="py-3 px-4 text-white font-medium">{row.total_quantity === 0 ? "-" : row.total_quantity.toLocaleString()}</td>
                        <td className="py-3 px-4 text-gray-300">{row.cumulative_confirmed.toLocaleString()}</td>
                        <td className="py-3 px-4 text-gray-300">{row.cumulative_unconfirmed.toLocaleString()}</td>
                        <td className="py-3 px-4 text-white font-medium">{row.cumulative_total.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <Activity size={48} className="mx-auto mb-4 opacity-20" />
                  <p>No bids received yet for this issue.</p>
                </div>
              )}
            </div>
        </div>
      </div>
    </div>
  );
}
