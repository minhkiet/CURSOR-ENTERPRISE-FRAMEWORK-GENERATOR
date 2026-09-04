---
name: "source-command-bazi"
description: "Bazi / 四柱 — tính tứ trụ deterministic bằng calculator vendored, đọc references theo câu hỏi, trả lời có trích dẫn và phản chứng"
---

# source-command-bazi

Use this skill when the user asks to run the migrated source command `bazi`.

## Command Template

# Command: /bazi

## Mục tiêu

Chạy phân tích **tứ trụ / 八字** thực chiến thông qua upstream
`bazi-analysis-skill`. Workflow: preflight → chạy calculator deterministic
→ đọc references theo câu hỏi → tổng hợp có trích dẫn + phản chứng.

## Trigger Keywords
- `bazi`, `八字体`, `八字`, `四柱`, `命盘`, `命理`, `算命`, `排盘`, `批命`
- `流年`, `大运`, `十年大运`, `流月`, `运势`, `调候`
- `十神`, `藏干`, `纳音`, `神煞`, `空亡`
- `Tứ trụ`, `tử vi trung hoa`, `four pillars`, `fortune telling`,
  `birth chart analysis`
- Trigger tiếng Việt: "phân tích bát tự", "xem tử vi theo ngày giờ sinh",
  "vận mệnh theo tứ trụ"

## Khi nào dùng

Dùng khi user cung cấp **ngày giờ sinh (và giới tính)** và hỏi về
vận mệnh / sự nghiệp / tài lộc / quan hệ / sức khỏe / năm cụ thể. KHÔNG
dùng cho:

- Tử vi lá số (紫微斗数) → skill khác
- Bói Tarot / Western astrology → skill khác
- Tư vấn tâm lý / cuộc sống đơn thuần → chế độ chat thường
- Review code / threat modeling → `/security` (sec_security-review)

## Quy trình (BẮT BUỘC theo thứ tự)

### 1. Thu thập thông tin tối thiểu

Theo nguyên tắc "minimum information" của upstream, chỉ hỏi những gì cần:

- **Bắt buộc**: ngày sinh (dương lịch hoặc âm lịch có ghi rõ tháng nhuận),
  giờ sinh (hoặc tên khắc), giới tính.
- **Hữu ích khi gần biên**: kinh độ nơi sinh (để hiệu chỉnh true-solar).
- **Không cần**: tên, tên cũ, đang sống / đã mất (trừ khi user chủ động).

Nếu user chỉ cho giờ chung chung ("sáng", "chiều") → liệt kê các khắc
có thể, phân tích điểm chung, **không** bịa ra một khắc duy nhất.

### 2. Preflight

```bash
python tools/bazi-plugin/scripts/bazi_status.py
```

Đọc `ok`:
- `true` → tiếp tục
- `false` → DỪNG. Hiển thị `actions[]` nguyên xi, không "thử LLM đoán".

### 3. Chạy calculator

```bash
# Mặc định: dương lịch, zi-next day-boundary
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 14:30 --gender female \
  --target-year 2026 --compact

# Âm lịch có tháng nhuận
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-04-21 --time 14:30 --calendar lunar --leap \
  --gender female --compact

# Sinh sau 23:00, muốn dùng civil midnight
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 23:30 --gender male \
  --day-boundary civil-midnight --compact

# Gần biên节气 / sinh ở miền tây, cần true-solar
python tools/bazi-plugin/scripts/calculate_bazi.py \
  --date 1990-05-15 --time 14:30 --gender female \
  --longitude 104.07 --utc-offset 8 --compact
```

Đọc JSON, **đối chiếu ngay**:
- `conventions` → echo lại đầu câu trả lời (year_boundary, day_boundary)
- `four_pillars.text` → bốn trụ dùng xuyên suốt
- `element_profile.warning` → paste nguyên xi, **không paraphrase**
- `luck_cycles.primary` vs `alternative` → nếu khác nhau, nêu rõ

### 4. Map câu hỏi → task mode

| Câu hỏi của user | Mode | Đọc references |
|---|---|---|
| "Phân tích tổng quan cho tôi" | **A. Full consultation** | calculation-conventions, reasoning-protocol, domain-rules, temporal-reasoning, consultation-output |
| "Có nên đổi việc 2026 không?" | **B. Focused + C. Year window** | temporal-reasoning + đoạn `career` của domain-rules |
| "Hôn nhân / con cái / gia đình" | **B. Focused** | `relationship`/`family`/`children` trong domain-rules |
| "Bài thi / câu hỏi trắc nghiệm" | **D. Benchmark** | benchmark-protocol (cô lập context) |
| "Mệnh tôi hợp màu gì / hướng nào" | **B. Focused, nông** | classical-texts + wuxing-tables |
| "Hai người có hợp nhau không" | **B. Focused** | reasoning-protocol + domain-rules `relationship` |

### 5. Phân tích (4 bước theo upstream reasoning-protocol)

```
1. 事实扫描 (chart facts)         → lấy từ calculator JSON
2. 格局/病药 (structural read)    → classical-texts + reasoning-protocol
3. 领域映射 (domain mapping)       → domain-rules theo mode đã chọn
4. 岁运触发 (year/luck trigger)   → temporal-reasoning
5. 反证校准 (counter-evidence)     → bắt buộc, tìm ít nhất 1 phản chứng mạnh nhất
```

Mỗi kết luận phải gắn nhãn độ tin cậy: **高 / 中 / 低**.

### 6. Trả lời theo consultation-output

Theo `references/consultation-output.md`:

1. **排盘口径** — echo `conventions` + giả định gender/calendar
2. **命局骨架** — bốn trụ, ngày chủ, nguyên khí, xung hợp
3. **核心判断** — 2-4 bằng chứng phân biệt nhất
4. **主题解读** — chỉ miền user hỏi, phân biệt "khuynh hướng ổn định"
   vs "biểu hiện có điều kiện"
5. **岁运窗口** — khoảng thời gian + cơ chế kích hoạt + loại sự kiện
6. **回溯校验** — 2-3 cửa sổ quá khứ (nếu user cung cấp) để đối chiếu
7. **结论边界** — confidence + nguồn uncertainty lớn nhất + lời khuyên thực tế

### 7. Đóng gói output với guardrails

Theo upstream SKILL.md, **luôn**:

- Phân biệt facts (không tranh cãi được với calculator) / structural
  (có truy xuất) / inference có điều kiện / practical advice.
- **Không** bịa古籍引文, kinh nghiệm người dùng, hoặc tai họa chắc chắn.
- Dùng "có khuynh hướng", "trong điều kiện X", "dễ biểu hiện thành"
  thay vì "sẽ", "phải", "nhất định".
- Sức khỏe: chỉ nói hình tượng truyền thống, khuyên khám bác sĩ.
- Tài chính / nghề nghiệp: không khuyên all-in / đòn bẩy cao.
- Hôn nhân / con cái: không phán vô sinh, ngoại tình, ly hôn,
  xu hướng tính dục.

## Ví dụ

### User: "Tôi sinh 1990-05-15 14:30, nữ, hỏi 2026–2027 đổi việc"

1. Thu thập: đủ dữ liệu, **không** hỏi tên
2. Preflight: `bazi_status.py` → `ok: true`
3. Calculator: chạy `--target-year 2026` và `--target-year 2027`
   (chạy 2 lần, hoặc gọi Python helper 2 lần)
4. Mode: **B + C** → đọc `temporal-reasoning.md` + đoạn `career` của
   `domain-rules.md`
5. Reasoning: facts → check 2026/2027 trong `luck_cycles` (丁丑 step
   2023–2032) → đối chiếu với `target_year.interactions_with_natal_chart`
6. Phản chứng: ít nhất 1 trong (空亡, 冲, 自刑, 月令冲克) — nếu phản
   chứng phủ định kết luận → giảm confidence hoặc đổi kết luận
7. Trả lời: structure của consultation-output, đính kèm **高/中/低**
   confidence cho từng dòng + giới hạn thực tế

### User: "Câu hỏi trắc nghiệm: 四柱 庚午 辛巳 庚辰 癸未, nữ, 2026 婚姻?"

1. Thu thập: user cho sẵn tứ trụ, **không** cần calculator nếu không hỏi
   về dương lịch / giờ cụ thể
2. Mode: **D. Benchmark** → đọc `benchmark-protocol.md` trước
3. Nếu có cơ chế "switch certificate" / sub-agent sạch → dùng; nếu
   không → dùng single-context degraded protocol
4. **Không** tra cứu dataset, tag câu hỏi, hay đáp án cùng nhân vật
5. Output: chỉ `答案：X` + 1-3 câu biện minh (nếu yêu cầu); nếu chỉ
   yêu cầu chữ cái → chỉ in chữ cái

## Anti-patterns

- ❌ Tính nhẩm ngày trụ / đại vận / biên节气 → **luôn** chạy calculator
- ❌ Coi `element_profile.support_ratio` là 旺衰 chính thức → đó chỉ
  là heuristic sơ loại, phải đọc lại `element_profile.warning`
- ❌ Bịa古籍引文, sự kiện đời user, hoặc tai họa chắc chắn
- ❌ "Đổi năm / dùng lunar_python mới hơn sẽ chính xác hơn" → vendor
  pin 1.4.8, **không** thay
- ❌ Sửa trực tiếp `tools/bazi-plugin/scripts/calculate_bazi.py` hoặc
  `vendor/lunar_python/` → mở PR upstream + sync
- ❌ Tư vấn y tế / pháp lý / tài chính chắc chắn từ tứ trụ

## Verify sau khi trả lời

```bash
# 1. Calculator có chạy đúng?
python tools/bazi-plugin/scripts/bazi_status.py
# expect: "ok": true

# 2. Regression tests pass?
python -m unittest -v tools/bazi-plugin/scripts/test_calculate_bazi.py
# expect: Ran 5 tests ... OK
```

## Liên kết

- Upstream: <https://github.com/guojiahh/bazi-analysis-skill>
- Bridge skill: `.cursor/skills/bazi/SKILL.md`
- Calculator: `tools/bazi-plugin/scripts/calculate_bazi.py`
- Preflight: `tools/bazi-plugin/scripts/bazi_status.py`
- Tests: `tools/bazi-plugin/scripts/test_calculate_bazi.py`
- Upstream references: `tools/bazi-plugin/references/*.md`
- Prompt-time fallback: `.cursor/skills/special_bazi/SKILL.md`
- Sync protocol: `tools/bazi-plugin/SYNC.md`

> 本技能用于传统文化研究与娱乐参考。Benchmark 模式仍可选择最符合传统
> 命理规则的选项，但不得把该选择包装成科学事实。
