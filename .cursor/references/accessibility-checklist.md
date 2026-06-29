# Accessibility Checklist Reference

> Based on [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) references

---

## WCAG 2.1 AA Compliance

### The Four Principles (POUR)

1. **Perceivable** - Information must be presentable
2. **Operable** - UI components must be operable
3. **Understandable** - Information and UI must be understandable
4. **Robust** - Content must be robust for assistive tech

---

## Perceivable

### Text Alternatives

- [ ] All images have alt text
- [ ] alt="" for decorative images
- [ ] alt text is descriptive for meaningful images
- [ ] Complex images have long descriptions
- [ ] Charts have data tables available
- [ ] Videos have captions
- [ ] Audio has transcripts

### Captions & Transcripts

| Content Type | Requirement |
|--------------|-------------|
| Pre-recorded video | Captions required |
| Live video | Captions required |
| Audio content | Transcript required |
| Interactive | Text alternatives |

### Adaptable

- [ ] Content structure with semantic HTML
- [ ] Information not relying on shape/color
- [ ] Instructions not relying on sensory characteristics
- [ ] Orientation not restricted (mobile)
- [ ] Reflow works at 400% zoom

### Distinguishable

- [ ] Color contrast 4.5:1 (text)
- [ ] Color contrast 3:1 (large text)
- [ ] Color contrast 3:1 (UI components)
- [ ] Text resizable to 200%
- [ ] No information by color alone
- [ ] Text spacing adjustable
- [ ] Images of text avoided

### Color Contrast Table

| Text Size | Minimum Ratio |
|-----------|---------------|
| < 18pt (or 14pt bold) | 4.5:1 |
| >= 18pt (or 14pt bold) | 3:1 |
| UI components | 3:1 |

---

## Operable

### Keyboard Accessible

- [ ] All functionality via keyboard
- [ ] No keyboard traps
- [ ] Focus order logical
- [ ] Focus visible
- [ ] Skip links present
- [ ] Shortcut keys don't conflict
- [ ] Focus not moved unexpectedly

### Focus Indicators

```css
/* ❌ BAD: No visible focus */
:focus {
  outline: none;
}

/* ✅ GOOD: Clear focus indicator */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

### Enough Time

- [ ] Content pauseable
- [ ] Auto-updating content deferrable
- [ ] No time limits (or extendable)
- [ ] Session timeout reasonable

### Seizures & Physical Reactions

- [ ] No flashing content (> 3 times/second)
- [ ] Animations respect reduced motion
- [ ] No auto-play that can't be controlled

### Navigable

- [ ] Focus order logical
- [ ] Focus targets large enough (44x44px)
- [ ] Link purpose clear
- [ ] Multiple ways to find content
- [ ] Headings and labels present
- [ ] Focus visible on interactive elements

### Modal/Dialog Access

- [ ] Focus trapped in modal
- [ ] Focus returns on close
- [ ] Escape key closes modal
- [ ] Click outside closes modal

---

## Understandable

### Readable

- [ ] Language declared
- [ ] Abbreviations explained on first use
- [ ] Reading level appropriate
- [ ] Unusual words explained
- [ ] Pronunciation available for ambiguous

### Predictable

- [ ] Navigation consistent
- [ ] Same functionality same way
- [ ] Identified consistently
- [ ] Components behave predictably

### Input Assistance

- [ ] Error identification
- [ ] Error suggestions
- [ ] Labels or instructions
- [ ] Error prevention (legal/financial)

### Form Errors

```html
<!-- ❌ BAD: No association -->
<span class="error">Email is required</span>
<input type="email" />

<!-- ✅ GOOD: Proper association -->
<label for="email">Email</label>
<input type="email" id="email" aria-describedby="email-error" />
<span id="email-error" class="error" role="alert">Email is required</span>
```

---

## Robust

### Compatible

- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Status messages announced
- [ ] Works with assistive tech

### ARIA Usage

| Pattern | ARIA |
|---------|------|
| Button | `<button>` (not div) |
| Link | `<a href>` |
| Checkbox | `<input type="checkbox">` + `<label>` |
| Radio | `<input type="radio">` + `<fieldset>` |
| Modal | `role="dialog"` + focus trap |
| Alert | `role="alert"` |
| Loading | `role="status"` or `aria-busy` |

### Status Messages

```html
<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true">
  <!-- Content updates announced -->
</div>

<!-- For important alerts -->
<div role="alert">
  Your session will expire in 5 minutes.
</div>
```

---

## Testing Tools

### Automated

| Tool | What It Catches |
|------|-----------------|
| axe DevTools | 30-50% of issues |
| WAVE | Contrast, structural |
| Lighthouse | Accessibility audit |
| Accessibility Insights | Comprehensive |

### Manual Testing

| Test | How |
|------|-----|
| Keyboard only | Tab through entire page |
| Screen reader | NVDA/VoiceOver |
| Zoom 400% | Reflow and overflow |
| Color blindness | Sim Daltonism |

### Keyboard Testing

1. Tab to page
2. Navigate all interactive elements
3. Trigger all actions
4. Close all modals/dropdowns
5. Verify logical order

### Screen Reader Testing

| Screen Reader | Platform |
|--------------|----------|
| NVDA | Windows |
| JAWS | Windows |
| VoiceOver | macOS/iOS |
| TalkBack | Android |

---

## Common Issues

### High Impact

| Issue | Fix |
|-------|-----|
| Missing alt text | Add descriptive alt |
| Low contrast | Increase color difference |
| Missing form labels | Add `<label for>` |
| Focus not visible | Add `:focus-visible` styles |
| No skip link | Add skip navigation |

### Medium Impact

| Issue | Fix |
|-------|-----|
| Missing headings | Add semantic h1-h6 |
| Redundant links | Remove or combine |
| Missing lang | Add `lang="en"` |
| Missing error IDs | Add unique IDs |

### Low Impact

| Issue | Fix |
|-------|-----|
| Empty button | Add text or aria-label |
| Decorative image alt | Use alt="" |
| Missing table headers | Add `<th>` |

---

## Checklist Summary

### Pre-Launch

- [ ] Automated audit passes
- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Color contrast meets requirements
- [ ] Focus indicators visible
- [ ] Forms have labels and errors
- [ ] Images have alt text
- [ ] Video has captions
- [ ] Reduced motion works
- [ ] Content reflows at 400%

---

## Links

- [agent-skills](https://github.com/addyosmani/agent-skills) - Source reference
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [[skill-registry]] - Accessibility triggers
