# URL Regression Protocol

**Purpose:** URL clone work must prove fidelity through browser evidence, not memory, taste, or a single screenshot.

---

## 0. Required Outputs

Every URL implementation run must leave an evidence folder:

```
qa/compare/
  index.html                 # side-by-side viewer
  compare-report.json        # viewport, scrollY, selector hits, rects
  original_*.png             # fresh-profile original frames
  local_*.png               # clone frames
```

---

## 1. Fresh Opening Capture

Opening loaders often run once. Always capture original opening with:
- New browser profile / empty user-data-dir
- Cache disabled
- Cache-busting query param
- No reused page session
- Same viewport as clone

**Minimum frames:**
```
t0080, t2600, t3600, t5200, t5600, t6000, t6400, t7000
```

---

## 2. Same-Viewport Source Anchors

Compare by **source anchors** not scroll percentages:
```
hero:       scrollY = 0 after stable opening
intro:      first content section
projects:   project list header
model:      model/process section
cta:        final CTA
footer:     footer headline
```

For each anchor, capture screenshot + JSON with viewport, scrollY, rects, computed styles.

---

## 3. CSS / Framework Audit

Before blaming layout math, inspect computed boxes:

```js
// Audit these:
- root/body font, letter-spacing
- global box-sizing
- container width and max-width
- section overflow, min-height
- grid/flex columns, gap
- image object-fit and object-position
- sticky/fixed transforms
- z-index of overlays
```

**Tailwind trap:**
- `.container` has built-in breakpoint `max-width` — override or use custom class.

---

## 4. Data Cardinality

Extract real data before implementing:
- Number of project cards / partners / slides
- Source image/video/font URLs
- Placeholder vs real data

**Failure signals:**
- Repeated modules not in source
- Placeholder cards where source has real images
- Wrong number of visible items

---

## 5. Breakpoint Discipline

Record viewport and state for every conclusion:
- Different widths may have different layouts
- Record CSS viewport, DPR, scroll position

---

## 6. Overlay Discipline

Classify overlay-like layers:
```
foreground scenery/matte   # image-shaped, allowed only if source shows it
terminal black field      # black fill below foreground
readability overlay     # forbidden unless source proves it
opening-only overlay     # only at matching timestamps
```

---

## 7. Scroll & Interaction Sampling

**Minimum desktop states:**
```
opening frames
stable hero
mouse-left (x ≈ 20%)
mouse-center (x ≈ 50%)
mouse-right (x ≈ 80%)
scroll first transition
```

---

## 8. Pass/Fail Rule

**Pass only when:**
- Build succeeds
- `qa/compare/index.html` and `compare-report.json` exist
- Original and clone captured at same viewport/DPR
- Opening, scroll, hover states sampled
- No hard failures: missing loader, wrong tone, broken scroll, placeholder data

---

## Quick Checklist

- [ ] Fresh browser profile for opening capture
- [ ] Same viewport/DPR for all comparisons
- [ ] Source anchors instead of scroll percentages
- [ ] CSS/framework defaults audited
- [ ] Real data cardinality preserved
- [ ] No synthetic overlays added
- [ ] Compare canvas count, custom elements, fontVariationSettings
