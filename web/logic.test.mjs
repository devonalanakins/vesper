import test from "node:test";
import assert from "node:assert/strict";
import { WINDOWS, summarizeSeries, chartGeometry } from "./logic.mjs";

test("each synthetic window has positive finite observations", () => {
  for (const series of Object.values(WINDOWS)) {
    const metrics = summarizeSeries(series);
    assert.ok(Number.isFinite(metrics.pct));
    assert.equal(chartGeometry(series).points.length, series.length);
  }
});
test("change percentage uses first and last observations", () => {
  assert.equal(summarizeSeries([100, 110]).pct, 10.000000000000009);
});
test("negative example is honestly negative", () => {
  assert.ok(summarizeSeries([100, 85]).pct < 0);
});
test("identical observations create usable flat chart", () => {
  const path = chartGeometry([100, 100, 100]);
  assert.match(path.line, /^M0.00/);
  assert.ok(!path.line.includes("NaN"));
});
test("invalid, unsafe and empty source values are rejected", () => {
  for (const bad of [[], [100], [100, NaN], [10, Infinity], [0, 100], ["2", "3"]]) {
    assert.throws(() => chartGeometry(bad));
  }
  assert.throws(() => chartGeometry([1, 2], 0, 260));
});
test("all chart coordinates remain inside the viewport", () => {
  const { points } = chartGeometry([1, 100, 2, 20]);
  assert.ok(points.every(p => p.x >= 0 && p.x <= 800 && p.y >= 0 && p.y <= 260));
});
