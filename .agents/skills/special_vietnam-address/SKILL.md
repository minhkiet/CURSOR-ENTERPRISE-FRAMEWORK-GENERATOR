---
description: Skill chuyên về xử lý địa chỉ Việt Nam - autocomplete, validation, phân tích địa chỉ, tích hợp với vietnamese-provinces-database. Kích hoạt khi cần làm việc với địa chỉ, tỉnh/thành phố, quận/huyện, phường/xã tại Việt Nam.
created: 2026-06-26
version: 1.0.0
tags: [vietnam, address, province, district, ward, autocomplete, validation, location, geocoding, form]
---

# Vietnamese Address Skill

## Tổng quan

Skill chuyên xử lý địa chỉ Việt Nam, tích hợp với [vietnamese-provinces-database](https://github.com/thanglequoc/vietnamese-provinces-database) - dataset 1.3k stars về đơn vị hành chính Việt Nam.

### Data Sources

| Format | Location | Use Case |
|--------|----------|----------|
| JSON | `json/` | Frontend, Node.js |
| PostgreSQL | `postgresql/` | Backend, Full-featured |
| MySQL | `mysql/` | Backend, Common |
| MongoDB | `mongodb/` | NoSQL projects |
| Redis | `redis/` | Caching layer |

### Tables Schema

```
administrative_regions (8 regions)
├── id, name, name_en, code_name, code_name_en
│
administrative_units (5 unit types)
├── id, full_name, full_name_en, short_name, short_name_en, code_name, code_name_en
│
provinces (34 provinces/cities)
├── code, name, name_en, full_name, full_name_en, code_name, administrative_unit_id
│
wards (~11,000 wards)
└── code, name, name_en, full_name, full_name_en, code_name, province_code, administrative_unit_id
```

## Kích hoạt khi

- Vietnamese address autocomplete/input
- Province/City selection (Tỉnh/Thành phố)
- District selection (Quận/Huyện)
- Ward/Commune selection (Phường/Xã)
- Address validation for Vietnam
- Shipping address form
- Location-based features
- Address parsing/extraction
- Vietnam geographic data
- Form với địa chỉ Việt Nam
- Dropdown tỉnh/thành phố → quận/huyện → phường/xã
- Validation địa chỉ cụ thể

## Pre-Review Gate

### V.1 Data Strategy

- [ ] Xác định data format phù hợp (JSON cho frontend, SQL cho backend)
- [ ] Load data từ vietnamese-provinces-database (hoặc API mock)
- [ ] Xác định search strategy (client-side search hay API call)

### V.2 Address Structure

- [ ] Xác định cấu trúc address cần thiết:
  - Full address (province → district → ward)
  - Province/City only
  - Province + District
  - With postal code
  - With geographic coordinates
- [ ] Xác định UI pattern:
  - Cascading dropdowns (3 levels)
  - Search autocomplete
  - Single field with auto-detect
  - Map picker

### V.3 Validation Rules

- [ ] Required fields identified
- [ ] Format validation rules defined
- [ ] Cross-field validation (ward belongs to district, district belongs to province)
- [ ] Real-time validation vs on-submit validation

## Implementation Guidelines

### Data Loading Strategy

```typescript
// Frontend - JSON import
import provincesData from './data/provinces.json';
import districtsData from './data/districts.json';
import wardsData from './data/wards.json';

// Backend - API endpoints
// GET /api/addresses/provinces
// GET /api/addresses/provinces/:code/districts
// GET /api/addresses/districts/:code/wards
// GET /api/addresses/search?q=keyword
```

### Cascading Dropdown Pattern

```typescript
// Province selection → filter Districts → filter Wards
const [selectedProvince, setSelectedProvince] = useState(null);
const [selectedDistrict, setSelectedDistrict] = useState(null);
const [selectedWard, setSelectedWard] = useState(null);

// Filtered data
const districts = districtsData.filter(d => d.province_code === selectedProvince?.code);
const wards = wardsData.filter(w => w.district_code === selectedDistrict?.code);
```

### Address Autocomplete Pattern

```typescript
// Search across all levels
function searchAddress(query: string) {
  const results = [
    ...provinces.filter(p => 
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.name_en.toLowerCase().includes(query.toLowerCase())
    ).map(p => ({ type: 'province', data: p })),
    
    ...districts.filter(d =>
      d.name.toLowerCase().includes(query.toLowerCase())
    ).map(d => ({ type: 'district', data: d })),
    
    ...wards.filter(w =>
      w.name.toLowerCase().includes(query.toLowerCase())
    ).map(w => ({ type: 'ward', data: w }))
  ];
  
  return results.slice(0, 10);
}
```

### Form Validation

```typescript
// Vietnamese address validation
const addressSchema = z.object({
  province: z.string().min(1, 'Vui lòng chọn tỉnh/thành phố'),
  district: z.string().min(1, 'Vui lòng chọn quận/huyện'),
  ward: z.string().min(1, 'Vui lòng chọn phường/xã'),
  street: z.string().min(5, 'Địa chỉ phải có ít nhất 5 ký tự'),
  postalCode: z.string().optional()
});

// Cross-field validation
function validateAddress(address: Address) {
  const district = districts.find(d => d.code === address.district);
  if (district && district.province_code !== address.province) {
    return { valid: false, error: 'Quận/huyện không thuộc tỉnh/thành phố đã chọn' };
  }
  return { valid: true };
}
```

## Post-Review Gate

### V.4 Data Integrity

- [ ] All provinces have correct codes (01-96)
- [ ] Districts properly linked to provinces
- [ ] Wards properly linked to districts
- [ ] English names available for all units
- [ ] Code names (slugs) correctly formatted

### V.5 UX Quality

- [ ] Cascading dropdowns work correctly (province → district → ward)
- [ ] Loading states shown during data fetch
- [ ] Empty states handled (no districts for selected province)
- [ ] Search/filter works for all fields
- [ ] Selected values display correctly

### V.6 Accessibility

- [ ] All selects have proper labels
- [ ] Keyboard navigation works
- [ ] Error messages announced to screen readers
- [ ] Focus management correct

### V.7 Performance

- [ ] Initial load optimized (lazy load districts/wards)
- [ ] Search debounced (300-500ms)
- [ ] Large datasets virtualized if needed

## Example Queries

### Get Full Address Path

```sql
-- PostgreSQL/MySQL
SELECT 
    p.name AS province,
    d.name AS district,
    w.name AS ward,
    CONCAT(w.name, ', ', d.name, ', ', p.name) AS full_address
FROM wards w
JOIN districts d ON w.district_code = d.code
JOIN provinces p ON d.province_code = p.code
WHERE w.code = '25920';
```

### Search by Keyword

```sql
-- Find all wards in "Ho Chi Minh" province
SELECT w.*
FROM wards w
JOIN districts d ON w.district_code = d.code
JOIN provinces p ON d.province_code = p.code
WHERE p.name LIKE '%Hồ Chí Minh%'
  AND w.name LIKE '%Tân%';
```

## Anti-Patterns

- [ ] Hardcode province/district/ward names in code
- [ ] Use outdated administrative divisions
- [ ] Skip validation of address hierarchy
- [ ] Load all data at once without lazy loading
- [ ] No loading states for async operations
- [ ] Inaccessible form controls

## Deliverables Checklist

```
[ ] Data layer (API/integration with vietnamese-provinces-database)
[ ] Province selector component
[ ] District selector component
[ ] Ward selector component
[ ] Cascading logic
[ ] Search/autocomplete (if applicable)
[ ] Form validation
[ ] Address display helper
[ ] Type definitions
[ ] Tests
```

---

**Data Source:** [thanglequoc/vietnamese-provinces-database](https://github.com/thanglequoc/vietnamese-provinces-database) (MIT License, v4.0.0)

**Last Updated:** 2026-06-26 (decree 30/2026/QH16 - Đồng Nai)
