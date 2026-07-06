# Accessibility Appendix

> Testable acceptance criteria for WCAG 2.2 AA conformance. Every rule in this appendix must be verifiable by automated test, manual test, or both.

---

## A. Perceivable

### A.1 Text alternatives

**A.1.1 Non-text content (Level A)**

| Criterion | Test |
|---|---|
| Every `<img>` has `alt` attribute | Automated: axe-core |
| Decorative images use `alt=""` | Manual review |
| Functional icons (button icons) have `aria-label` on parent button | Automated: axe-core |
| Complex graphics (charts, diagrams) have long description | Manual review |

**Pass criteria**: 0 axe-core violations on every page.

### A.1.2 Decorative-only elements

- Decorative SVGs use `aria-hidden="true"` and `focusable="false"`.
- Background images via CSS do not convey content.
- Icon-only buttons must have `aria-label` that includes the action verb ("Close", "Copy", not "Icon").

### A.2 Time-based media

- Not applicable (no audio/video on marketplace or docs surfaces).

### A.3 Adaptable

#### A.3.1 Info and relationships (Level A)

- Headings form a logical outline: one `<h1>` per page, no skipped levels.
- Lists use `<ul>`/`<ol>`, not styled `<div>`s.
- Form fields have associated `<label>`.
- Tables use `<th scope="col|row">`.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>` used semantically.

**Pass criteria**: axe-core landmark and heading checks pass; manual review of one page per component.

#### A.3.2 Meaningful sequence (Level A)

- DOM order matches visual order.
- Reading order is logical without CSS.

**Pass criteria**: disable CSS, read top-to-bottom, content makes sense.

#### A.3.3 Sensory characteristics (Level A)

- Instructions do not rely on color or shape alone ("Click the green button" → "Click 'Submit'").
- Status communicated via text or icon AND color, not color alone.

### A.4 Distinguishable

#### A.4.1 Color contrast (Level AA)

| Element | Foreground | Background | Required ratio | Test |
|---|---|---|---|---|
| Body text | `color.text.primary` | `color.surface.base` | 4.5:1 | Automated (axe), manual spot-check |
| Body text | `color.text.secondary` | `color.surface.base` | 4.5:1 | 7.86:1. PASS |
| Caption text ≥18px | `color.text.tertiary` | `color.surface.base` | 4.5:1 | 4.65:1. PASS (≥18px only) |
| Caption text <18px | `color.text.tertiary` | `color.surface.base` | 4.5:1 | FAIL. must not use for small text |
| Button primary | `color.surface.base` | `color.text.primary` | 4.5:1 | 21:1. PASS AAA |
| Button disabled | `color.text.tertiary` | `color.surface.strong` | 4.5:1 | FAIL. must add aria-describedby with reason |
| Focus ring | `color.border.strong` | `color.surface.base` | 3:1 (non-text) | 17.5:1. PASS |
| Border default | `color.border.default` | `color.surface.base` | 3:1 (UI) | 17.5:1. PASS |

**Mandatory rule**: `color.text.tertiary` is permitted only for text ≥18px regular, ≥14px bold, or non-essential (decorative captions, status counts). Lint rule must reject use for body copy <18px.

#### A.4.2 Audio control

- Not applicable.

#### A.4.3 Resize text (Level AA)

- Text remains readable at 200% zoom.
- No content is lost or requires horizontal scroll at 200%.
- Layout reflows gracefully.

**Pass criteria**: zoom to 200% in browser, verify no content lost, no horizontal scroll on body.

#### A.4.4 Images of text (Level AA)

- No images of text except for logos (which are exempt).
- Custom typography rendered as text, not images.

#### A.4.5 Reflow (Level AA, WCAG 2.1+)

- Content reflows at 320px width without horizontal scrolling (except for data tables, code blocks, maps).
- Mobile breakpoint (<768px) and small desktop both tested.

**Pass criteria**: resize viewport to 320×256, scroll vertically, verify no horizontal scroll.

#### A.4.10 Reflow (Level AA, WCAG 2.1+). duplicate, covered above

#### A.4.11 Non-text contrast (Level AA, WCAG 2.1+)

- UI components have 3:1 contrast against adjacent colors.
- Graphical objects (icons) have 3:1 contrast.

#### A.4.12 Text spacing (Level AA, WCAG 2.1+)

- No content lost when user overrides:
  - Line height to 1.5× font size
  - Paragraph spacing to 2× font size
  - Letter spacing to 0.12em
  - Word spacing to 0.16em

#### A.4.13 Content on hover or focus (Level AA, WCAG 2.1+)

- Hover content (tooltips, dropdowns) is dismissible, hoverable, and persistent.

---

## B. Operable

### B.1 Keyboard accessible

#### B.1.1 Keyboard (Level A)

- All functionality available via keyboard.
- No keyboard trap (focus can move away from any component using Tab/Shift+Tab or standard exit keys).

**Pass criteria**: keyboard-only walkthrough completes all primary user flows:
1. Browse marketplace, filter by category, view template, copy snippet.
2. Navigate to docs, find component, copy code.
3. Submit contact form, receive confirmation.

#### B.1.2 No keyboard trap (Level A)

- Modal/dialog: Escape closes, focus returns to trigger.
- Mobile menu: Escape closes, focus returns to hamburger.

### B.2 Enough time

- Not applicable (no time-limited interactions on marketplace or docs).

### B.3 Seizures and physical reactions

#### B.3.1 Three flashes (Level A)

- No content flashes more than 3 times per second.

### B.4 Navigable

#### B.4.1 Bypass blocks (Level A)

- Skip-to-content link is the first focusable element.
- Skip link target is `<main>`.
- Visible on focus, hidden when not focused.

#### B.4.2 Page titled (Level A)

- Each page has unique `<title>`.
- Format: "[Page]. ProofMatcher".
- Length ≤60 characters.

#### B.4.3 Focus order (Level A)

- Focus order matches visual order.
- No `tabindex` > 0.

#### B.4.4 Link purpose (Level A)

- Link text describes destination (no "click here", "read more" without context).
- Exception: when link text is part of a card title that itself describes the destination.

#### B.4.5 Multiple ways (Level AA)

- ≥2 ways to find a page: navigation, search, sitemap, related links.

#### B.4.6 Headings and labels (Level AA)

- Headings describe topic.
- Labels describe input purpose.

#### B.4.7 Focus visible (Level AA)

- Focus indicator visible on every focusable element.
- `:focus-visible` (not `:focus`) shows ring.
- Mouse click does not show ring.
- Keyboard Tab always shows ring.

**Mandatory CSS rule**:

```css
:focus { outline: none; }
:focus-visible {
  outline: 2px solid var(--color-border-strong);
  outline-offset: 2px;
}
```

#### B.4.11 Focus not obscured (Level AA, WCAG 2.2)

- Focus indicator not hidden by sticky header, footer, or other content.
- `scroll-padding-top` set to top nav height to ensure focus is visible after anchor scroll.

#### B.4.12 Focus appearance (Level AA, WCAG 2.2)

- Focus indicator has 3:1 contrast against adjacent colors.
- Focus area is at least 2px thick (CSS outline 2px meets this).
- Focus area is at least the size of a 1px perimeter of the element OR 4×4px, whichever is larger.

#### B.4.13 Reference sensors (Level AA, WCAG 2.2). placeholder, not in scope yet

### B.5 Input modalities

#### B.5.1 Pointer gestures (Level A, WCAG 2.1+)

- All functionality available via single pointer (no multi-finger or path-based gestures required).

#### B.5.2 Pointer cancellation (Level A, WCAG 2.1+)

- Click events fire on `mouseup`, not `mousedown`. Allows user to cancel by dragging away.

#### B.5.3 Label in name (Level A, WCAG 2.1+)

- Visible label text matches the accessible name.
- If icon button has visible "X" text, `aria-label` must include "Close" or similar, not just "X".

#### B.5.4 Motion actuation (Level A, WCAG 2.1+)

- Not applicable (no device motion required).

---

## C. Understandable

### C.1 Readable

#### C.1.1 Language (Level A)

- `<html lang="en">` set on every page.

#### C.1.2 Language of parts (Level AA)

- Non-English phrases have `lang` attribute (e.g. `<span lang="vi">Xin chào</span>`).

### C.2 Predictable

#### C.2.1 On focus (Level A)

- No context change on focus (modals don't open just by focusing a button).

#### C.2.2 On input (Level A)

- No context change on input (filter chips don't auto-submit; typing in search doesn't navigate).

#### C.2.3 Consistent navigation (Level AA)

- Navigation order consistent across pages.

#### C.2.4 Consistent identification (Level AA)

- Same icon/label for same function across pages.

### C.3 Input assistance

#### C.3.1 Error identification (Level A)

- Errors identified in text.
- `role="alert"` or `aria-live` for screen reader announcement.
- Error field has `aria-invalid="true"`.

#### C.3.2 Labels or instructions (Level A)

- Required fields marked with `*` and `aria-required="true"`.
- Input format guidance provided when constrained (e.g. password requirements).

#### C.3.3 Error suggestion (Level AA)

- Error messages suggest correction ("Email must include @" not "Invalid email").

#### C.3.4 Error prevention (legal, financial) (Level AA)

- Not applicable for marketplace browsing; applies to checkout (out of scope for design system).

---

## D. Robust

### D.1 Compatible

#### D.1.1 Parsing (Level A). obsolete in WCAG 2.2

- Marked obsolete; do not test.

#### D.1.2 Name, role, value (Level A)

- All UI components have:
  - Name: `aria-label`, `aria-labelledby`, or visible text.
  - Role: native HTML element or explicit ARIA role.
  - Value/state: ARIA state or native HTML state.

**Pass criteria**: NVDA/VoiceOver announces component name, role, and current state.

---

## E. Test method matrix

| Test | Tool | Frequency |
|---|---|---|
| Automated axe-core scan | `@axe-core/playwright` in CI | Every PR |
| Color contrast (text) | Stark, Polypane, manual | Per component change |
| Color contrast (UI) | Stark, manual | Per component change |
| Keyboard walkthrough | Manual | Per sprint, per major change |
| Screen reader (NVDA + Chrome) | Manual | Per sprint |
| Screen reader (VoiceOver + Safari) | Manual | Quarterly |
| Zoom 200% reflow | Manual + automated | Per PR |
| Reduced motion | Playwright with `prefers-reduced-motion: reduce` | Per PR |
| Touch targets ≥44×44px | DevTools + manual | Per component change |
| Mobile (iOS Safari) | BrowserStack | Per sprint |

---

## F. Acceptance criteria summary (machine-readable)

```yaml
wcag_aa_acceptance:
  perceivable:
    text_alternatives: pass
    adaptable: pass
    distinguishable:
      text_contrast_aa: pass
      non_text_contrast_aa: pass
      resize_200_percent: pass
      reflow_320px: pass
  operable:
    keyboard: pass
    no_keyboard_trap: pass
    bypass_blocks: pass
    page_titled: pass
    focus_order: pass
    link_purpose: pass
    multiple_ways: pass
    headings_labels: pass
    focus_visible: pass
    focus_not_obscured: pass
    focus_appearance: pass
  understandable:
    language: pass
    on_focus: pass
    on_input: pass
    consistent_navigation: pass
    error_identification: pass
    labels_instructions: pass
    error_suggestion: pass
  robust:
    name_role_value: pass
```

---

## G. Known limitations and future work

1. **WCAG 2.2 new criteria**: Focus appearance, focus not obscured, dragging movements, target size enhanced. all in scope for current system.
2. **Cognitive accessibility** (Level AAA): not required, but documented for future.
3. **Mobile app accessibility**: out of scope (web only).

---

## H. Open questions for accessibility review

1. **Touch target minimum**: do we hold to 44×44px or relax to 40×40px for compact components? Current rule: 44×44px.
2. **Focus ring offset**: 2px or 4px? Current rule: 2px. 4px would give stronger visual separation but might overlap adjacent components.
3. **Skip link**: include both "Skip to main content" and "Skip to navigation"? Current: only "Skip to main content".
4. **Cookie consent**: do we need a separate accessibility statement page? Recommend: yes, link in footer.