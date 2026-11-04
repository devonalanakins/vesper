import { WINDOWS, chartGeometry, summarizeSeries } from "./logic.mjs";

// Static, synthetic example only. This program intentionally has no fetch,
// WebSocket, storage, credentials, account identifiers, broker or order APIs.
const content = document.getElementById("dynamic-content");
const heading = document.getElementById("view-heading");
const description = document.getElementById("view-description");
const crumb = document.getElementById("breadcrumb-view");
const nav = [...document.querySelectorAll("[data-view]")];
let period = "1M";

const screens = Object.freeze({
  overview: { heading: "See the signal.<br><em>Question everything.</em>", description: "A research environment where capital decisions are examined before they're made." },
  research: { heading: "Every hypothesis.<br><em>Under scrutiny.</em>", description: "A disciplined place to test ideas, reproduce outcomes and challenge assumptions." },
  risk: { heading: "Protect the downside.<br><em>Before anything else.</em>", description: "Independent constraints, explicit limits and a permanent separation from live execution." },
  evidence: { heading: "Nothing asserted.<br><em>Without a trail.</em>", description: "Provable data lineage, account isolation, missing-data detection and audit-ready explanations." }
});

function lineChart() {
  const series = WINDOWS[period];
  const chart = document.getElementById("equity-chart");
  if (!chart) return;
  const geometry = chartGeometry(series);
  document.getElementById("chart-line").setAttribute("d", geometry.line);
  document.getElementById("chart-fill").setAttribute("d", geometry.fill);
  const grid = document.getElementById("chart-grid");
  grid.replaceChildren();
  for (let i = 1; i <= 3; i++) {
    const node = document.createElementNS("http://www.w3.org/2000/svg", "line");
    const y = (i * 260 / 4).toFixed(2);
    node.setAttribute("x1", "0");
    node.setAttribute("x2", "800");
    node.setAttribute("y1", y);
    node.setAttribute("y2", y);
    node.setAttribute("stroke", "rgba(177,182,220,.16)");
    node.setAttribute("stroke-dasharray", "4 8");
    grid.append(node);
  }
  const result = summarizeSeries(series);
  const change = document.getElementById("period-return");
  change.textContent = result.sign + result.pct.toFixed(2) + "%";
  change.classList.toggle("negative", result.pct < 0);
  change.classList.toggle("positive", result.pct >= 0);
  document.getElementById("period-label").textContent = "Synthetic " + period + " window";
  document.getElementById("chart-range").textContent = "Illustrative sample: synthetic " + period + " series";
  for (const button of document.querySelectorAll("[data-period]")) {
    const active = button.dataset.period === period;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  }
}

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

const dataSections = {
  research: [
    ["01 / HYPOTHESIS", "Is the edge real?", "Separate exploratory fit from out-of-sample evidence. No experiments in this prototype have been independently validated.", "NOT EVALUATED"],
    ["02 / REPRODUCIBILITY", "Replay before belief.", "Require versioned datasets, stable time boundaries, realistic costs, slippage and explicit failure criteria.", "DESIGNED / NOT BUILT"],
    ["03 / PROMOTION", "Research is not execution.", "A hypothesis never receives trading permission merely because simulated returns were positive.", "GATE CLOSED"]
  ],
  risk: [
    ["01 / ACCOUNT SCOPE", "No mixed accounts.", "Financial data belongs to an explicitly authorized owner and account. Cross-account calculation must fail.", "OFFLINE CORE"],
    ["02 / POLICY ENFORCEMENT", "Hard limits, not suggestions.", "Live sizing, drawdown controls and independent kill switches require separate implementation and review.", "NOT IMPLEMENTED"],
    ["03 / EXECUTION", "No order pathway.", "This repository cannot place a trade, move money or authorize a banking operation.", "DISABLED"]
  ],
  evidence: [
    ["01 / PROVENANCE", "The source must be known.", "A value needs an owner, account, timestamp, evidence identifier and completeness state.", "DOMAIN CONTRACT"],
    ["02 / PERFORMANCE", "Contributions are not profit.", "Linked time-weighted return distinguishes external capital movements from investment change.", "OFFLINE MATH"],
    ["03 / VERIFICATION", "Missing means unavailable.", "No invented exact return when valuation evidence is incomplete or the account is unfunded.", "FAIL CLOSED"]
  ]
};

function renderScreen(view) {
  const config = screens[view];
  heading.innerHTML = config.heading; // fixed, local, code-owned display strings only
  description.textContent = config.description;
  crumb.textContent = view.toUpperCase();
  for (const item of nav) {
    const active = item.dataset.view === view;
    item.classList.toggle("is-selected", active);
    if (active) item.setAttribute("aria-current", "page");
    else item.removeAttribute("aria-current");
  }
  if (view === "overview") {
    content.hidden = false;
    document.getElementById("detail-content")?.remove();
    lineChart();
    return;
  }
  content.hidden = true;
  let detail = document.getElementById("detail-content");
  if (!detail) {
    detail = document.createElement("div");
    detail.id = "detail-content";
    content.after(detail);
  }
  detail.className = "detail-grid";
  detail.innerHTML = dataSections[view].map(([step, title, text, status]) =>
    '<article class="panel detail-card"><span class="overline">' + escapeHtml(step) +
    '</span><h2>' + escapeHtml(title) + '</h2><p>' + escapeHtml(text) +
    '</p><span class="detail-status">' + escapeHtml(status) + '</span></article>'
  ).join("") +
  '<div class="detail-note">ALL EXAMPLES ARE SYNTHETIC · NO LIVE DATA OR FINANCIAL ACTIONS</div>';
}

for (const item of nav) item.addEventListener("click", () => renderScreen(item.dataset.view));
for (const button of document.querySelectorAll("[data-period]")) {
  button.addEventListener("click", () => {
    period = button.dataset.period;
    lineChart();
  });
}
lineChart();
