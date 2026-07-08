const API_BASE = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api").replace(/\/$/, "");

export async function fetchIssues() {
  const res = await fetch(`${API_BASE}/issues`);
  if (!res.ok) throw new Error("Failed to fetch issues");
  return res.json();
}

export async function createIssue(data: { exchange: string, symbol: string, scripcode?: string, name: string, status: string }) {
  const res = await fetch(`${API_BASE}/issues`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Failed to create issue");
  return res.json();
}

export async function deleteIssue(issueId: number) {
  const res = await fetch(`${API_BASE}/issues/${issueId}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error("Failed to delete issue");
  return res.json();
}

export async function fetchLadder(exchange: string, issue: string) {
  const res = await fetch(`${API_BASE}/ladder?exchange=${exchange}&issue=${issue}`);
  if (!res.ok) throw new Error("Failed to fetch ladder");
  return res.json();
}

export async function fetchCombinedLadder(issue: string, investorType: string = "NON_RETAIL") {
  const res = await fetch(`${API_BASE}/combined?issue=${issue}&investor_type=${investorType}`);
  if (!res.ok) throw new Error("Failed to fetch combined ladder");
  return res.json();
}

export async function fetchAnalytics(exchange: string, issue: string) {
  const res = await fetch(`${API_BASE}/analytics?exchange=${exchange}&issue=${issue}`);
  if (!res.ok) throw new Error("Failed to fetch analytics");
  return res.json();
}

export async function fetchTimeseries(exchange: string, issue: string) {
  const res = await fetch(`${API_BASE}/timeseries?exchange=${exchange}&issue=${issue}`);
  if (!res.ok) throw new Error("Failed to fetch timeseries");
  return res.json();
}
