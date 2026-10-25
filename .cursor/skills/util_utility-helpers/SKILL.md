---
description: Utility helpers skill covering common utilities, synchronization tools, code generators, and helper functions. Provides reusable components for common development tasks.
version: 1.0.0
created: 2026-08-03
tags: [utility, helpers, tools, sync, generator, common, reusable]
role: overlay
domains: [utility, tools, frontend, backend]
confidence:
  base: 0.60
  threshold: 0.50
  auto_select: false
triggers:
  - "utility"
  - "helper"
  - "tool"
  - "common"
  - "reusable"
  - "generator"
  - "sync"
  - "formatter"
  - "validator"
  - "converter"
  - "parser"
  - "util"
  - "tiện ích"
  - "công cụ"
---

# Utility Helpers Skill

## Overview

Collection of reusable utilities, tools, and helper functions for common development tasks.

## Categories

### 1. Data Utilities

**Validators**
```javascript
const isEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
const isUrl = (url) => try { new URL(url); return true; } catch { return false; };
const isUUID = (id) => /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id);
```

**Formatters**
```javascript
const formatCurrency = (amount, locale = 'en-US') => 
  new Intl.NumberFormat(locale, { style: 'currency', currency: 'USD' }).format(amount);

const formatDate = (date, format = 'short') => 
  new Intl.DateTimeFormat('en-US', { dateStyle: format }).format(new Date(date));
```

**Transformers**
```javascript
const groupBy = (array, key) => 
  array.reduce((acc, item) => ({ ...acc, [item[key]]: [...(acc[item[key]] || []), item] }), {});

const unique = (array) => [...new Set(array)];
const chunk = (array, size) => Array.from({ length: Math.ceil(array.length / size) }, 
  (_, i) => array.slice(i * size, (i + 1) * size));
```

### 2. Async Utilities

**Async Pool**
```javascript
class AsyncPool {
  constructor(concurrency = 5) {
    this.concurrency = concurrency;
    this.running = 0;
    this.queue = [];
  }
  
  async add(fn) {
    return new Promise((resolve, reject) => {
      this.queue.push({ fn, resolve, reject });
      this.process();
    });
  }
  
  async process() {
    while (this.running < this.concurrency && this.queue.length) {
      const { fn, resolve, reject } = this.queue.shift();
      this.running++;
      fn().then(resolve, reject).finally(() => {
        this.running--;
        this.process();
      });
    }
  }
}
```

**Debounce/Throttle**
```javascript
const debounce = (fn, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
};

const throttle = (fn, limit) => {
  let inThrottle;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
};
```

### 3. String Utilities

```javascript
const slugify = (str) => str.toLowerCase().trim()
  .replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, '');

const truncate = (str, max, suffix = '...') => 
  str.length > max ? str.slice(0, max - suffix.length) + suffix : str;

const camelToKebab = (str) => str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
```

### 4. Sync Tools

**File Sync**
```javascript
async function syncFiles(source, dest, options = {}) {
  const { dryRun = false, verbose = false } = options;
  const files = await glob(source);
  
  for (const file of files) {
    const destPath = file.replace(source, dest);
    if (dryRun) {
      console.log(`Would sync: ${file} -> ${destPath}`);
    } else {
      await fs.mkdir(path.dirname(destPath), { recursive: true });
      await fs.copyFile(file, destPath);
    }
  }
}
```

**Config Merge**
```javascript
const deepMerge = (target, ...sources) => {
  if (!sources.length) return target;
  const source = sources.shift();
  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        deepMerge(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }
  return deepMerge(target, ...sources);
};
```

## Quality Standards

### Pre-Implementation (§U.1)
- [ ] Utility follows single responsibility
- [ ] Type-safe with TypeScript
- [ ] Error handling included
- [ ] Tests written

### Post-Implementation (§U.2)
- [ ] Reusable in multiple contexts
- [ ] Documented with JSDoc
- [ ] No external dependencies
- [ ] Tree-shakeable

## Anti-Patterns to Reject

- Duplicate existing utilities
- Side effects
- Mutable global state
- Overly complex abstractions
- Missing error handling
- No TypeScript types
