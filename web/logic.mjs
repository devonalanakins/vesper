// All scenario data is created locally. No API access or source of real market data.
export const WINDOWS = Object.freeze({
  "1W": Object.freeze([100, 101.5, 100.8, 102.4, 101.9, 103.2, 104.1]),
  "1M": Object.freeze([100, 99.2, 100.6, 101.8, 101.1, 103.6, 102.9, 104.5, 103.8, 105.2, 104.4, 107, 106.3, 108.2, 107.7, 109.1, 108.8, 110.6, 109.9, 111.8]),
  "1Y": Object.freeze([100, 103, 102, 106, 104, 109, 112, 110, 114, 117, 116, 120, 118, 122, 125, 123, 127, 130, 128, 133, 132, 136, 139, 137])
});
export function summarizeSeries(series) {
  if (!Array.isArray(series) || series.length < 2 || series.some(x => !Number.isFinite(x) || x <= 0)) {
    throw new TypeError("synthetic series needs at least two positive finite observations");
  }
  const pct = (series.at(-1) / series[0] - 1) * 100;
  return { pct, sign: pct >= 0 ? "+" : "", first: series[0], last: series.at(-1) };
}
export function chartGeometry(series, width = 800, height = 260) {
  summarizeSeries(series);
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) {
    throw new TypeError("chart bounds must be positive");
  }
  const lower = Math.min(...series);
  const upper = Math.max(...series);
  const spread = Math.max(1, upper - lower);
  const min = lower - spread * .23;
  const max = upper + spread * .23;
  const points = series.map((v, i) => ({
    x: (i / (series.length - 1)) * width,
    y: (1 - (v - min) / (max - min)) * height
  }));
  const line = points.map((p, i) => (i === 0 ? "M" : "L") + p.x.toFixed(2) + " " + p.y.toFixed(2)).join(" ");
  const fill = line + " L" + width + " " + height + " L0 " + height + " Z";
  return { line, fill, points, lower, upper };
}
