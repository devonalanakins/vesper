import { SYNTHETIC_EVIDENCE } from "./data/synthetic-evidence.mjs";

// This renderer accepts only generated synthetic evidence. No network, accounts,
// orders, trading controls, or storage exist in the browser prototype.
function money(amount) {
  if (typeof amount !== "string" || !/^-?\d+(\.\d+)?$/.test(amount)) return "Unavailable";
  const numeric = Number(amount);
  if (!Number.isFinite(numeric) || !Number.isSafeInteger(Math.trunc(numeric))) return "Unavailable";
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(numeric);
}

function percentage(amount) {
  if (typeof amount !== "string" || !/^-?\d+(\.\d+)?$/.test(amount)) return "Unavailable";
  const numeric = Number(amount);
  if (!Number.isFinite(numeric) || Math.abs(numeric) > 1e8) return "Unavailable";
  return (numeric > 0 ? "+" : "") + numeric.toFixed(2) + "%";
}

export function evidenceCards(report = SYNTHETIC_EVIDENCE) {
  const fallback = [
    ["01 / EVIDENCE GATE", "Unavailable", "This report is withheld because source, status or metric consistency could not be established.", "NO NUMBERS DISPLAYED"],
    ["02 / DATA SAFETY", "No assumptions", "Missing or incompatible evidence must never become a manufactured account return.", "REVIEW REQUIRED"],
    ["03 / OPERATING MODE", "No execution", "No money movement, order placement or external connection exists in this prototype.", "DISABLED"]
  ];
  if (!report || report.source !== "synthetic" || report.label !== "SYNTHETIC / NOT LIVE" || report.actions_enabled !== false) {
    return fallback;
  }
  const statuses = new Set(["CALCULATED", "INCOMPLETE_EVIDENCE", "UNAVAILABLE_UNFUNDED"]);
  if (!statuses.has(report.status)) return fallback;
  const metricFields = [report.return_pct, report.net_pnl, report.external_flows];
  const allPresent = metricFields.every(value => value !== null && value !== undefined);
  const allAbsent = metricFields.every(value => value === null);
  if (!(report.status === "CALCULATED" ? allPresent : allAbsent)) return fallback;
  if (report.status !== "CALCULATED") {
    return [
      ["01 / EVIDENCE GATE", "Return unavailable", "The synthetic source does not meet the requirements for a calculated return. Missing capital and incomplete evidence are not treated as zero returns.", report.status],
      ["02 / PROVENANCE", "Not verified live", "A local synthetic fixture does not establish custody, brokerage pagination, or market-data provenance.", "OFFLINE EXAMPLE"],
      ["03 / OPERATING MODE", "Actions disabled", "All financial activity is permanently absent from this prototype.", "NO EXECUTION"]
    ];
  }
  const pct = percentage(report.return_pct);
  const pnl = money(report.net_pnl);
  const flows = money(report.external_flows);
  if ([pct, pnl, flows].includes("Unavailable")) return fallback;
  return [
    ["01 / EVIDENCE GATE", "Source: synthetic", "A deterministic example generated offline by the Python performance contract. Account and activity identifiers are deliberately excluded from this view.", "CALCULATED / SIMULATED"],
    ["02 / TWR PERFORMANCE", pct, "Linked time-weighted change across funded subperiods. Illustrative mathematical result only; not an observed or forecast investment return.", "HYPOTHETICAL RETURN"],
    ["03 / NET P&L", pnl, "Illustrative change in equity after subtracting external owner contributions or withdrawals. No costs or real brokerage valuations are asserted.", "NOT A REAL ACCOUNT"],
    ["04 / EXTERNAL CASH", flows, "The hypothetical contribution is tracked separately and excluded from the calculated percentage return.", "SYNTHETIC CASH FLOW"]
  ];
}
