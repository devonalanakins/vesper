import test from "node:test";
import assert from "node:assert/strict";
import { evidenceCards } from "./evidence-view.mjs";
import { SYNTHETIC_EVIDENCE } from "./data/synthetic-evidence.mjs";

test("generated synthetic fixture reports Python-derived return and net P&L", () => {
  const cards = evidenceCards();
  assert.equal(cards.length, 4);
  assert.equal(cards[1][1], "+10.25%");
  assert.equal(cards[2][1], "$1,150.00");
  assert.equal(cards[3][1], "$2,500.00");
  assert.ok(!JSON.stringify(cards).includes("synthetic-owner-never-display"));
});

test("incomplete evidence must never display numerical performance", () => {
  const cards = evidenceCards({ ...SYNTHETIC_EVIDENCE, status: "INCOMPLETE_EVIDENCE", return_pct: null, net_pnl: null, external_flows: null });
  assert.match(cards[0][1], /unavailable/);
  assert.ok(!JSON.stringify(cards).includes("$1,150"));
});

test("missing status and inconsistent metrics fail closed", () => {
  const bad = [
    { ...SYNTHETIC_EVIDENCE, source: "broker" },
    { ...SYNTHETIC_EVIDENCE, label: "LIVE" },
    { ...SYNTHETIC_EVIDENCE, actions_enabled: true },
    { ...SYNTHETIC_EVIDENCE, status: "CALCULATED", net_pnl: null },
    { ...SYNTHETIC_EVIDENCE, status: "INCOMPLETE_EVIDENCE" },
    { ...SYNTHETIC_EVIDENCE, return_pct: "NaN" },
    { ...SYNTHETIC_EVIDENCE, net_pnl: "Infinity" },
    null
  ];
  for (const report of bad) {
    const cards = evidenceCards(report);
    assert.equal(cards[0][1], "Unavailable");
    assert.equal(cards.length, 3);
  }
});

test("negative returns are not mislabeled as positive", () => {
  const cards = evidenceCards({ ...SYNTHETIC_EVIDENCE, return_pct: "-12.5" });
  assert.equal(cards[1][1], "-12.50%");
});
