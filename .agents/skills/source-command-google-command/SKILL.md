# Google API Integration Skill

> **Version:** 1.0.0  
> **Platform:** Google Cloud APIs  
> **Use case:** Gmail, Drive, Sheets, Calendar, Maps, Firebase

## Overview

Google APIs cung cấp access đến hàng trăm dịch vụ của Google. Skill này tập trung vào các API phổ biến nhất cho người dùng Việt Nam: Gmail, Google Sheets, Google Calendar, Google Drive, Google Maps, và Firebase.

## API Capabilities

### 1. Google Sheets API

| Feature | Method | Description |
|---------|--------|-------------|
| Read Data | `spreadsheets.values.get` | Đọc dữ liệu từ sheet |
| Write Data | `spreadsheets.values.update` | Ghi dữ liệu vào sheet |
| Append Data | `spreadsheets.values.append` | Thêm dòng mới |
| Create Sheet | `spreadsheets.create` | Tạo spreadsheet mới |
| Format Cells | `spreadsheets.batchUpdate` | Định dạng, merge cells |

### 2. Gmail API

| Feature | Method | Description |
|---------|--------|-------------|
| List Emails | `users.messages.list` | Lấy danh sách emails |
| Read Email | `users.messages.get` | Đọc nội dung email |
| Send Email | `users.messages.send` | Gửi email |
| Create Draft | `users.drafts.create` | Tạo nháp |
| Modify Labels | `users.messages.modify` | Thêm/bớt labels |

### 3. Google Calendar API

| Feature | Method | Description |
|---------|--------|-------------|
| List Events | `events.list` | Lấy danh sách sự kiện |
| Create Event | `events.insert` | Tạo sự kiện mới |
| Update Event | `events.update` | Cập nhật sự kiện |
| Delete Event | `events.delete` | Xóa sự kiện |
| Quick Add | `events.quickAdd` | Tạo từ text |

### 4. Google Drive API

| Feature | Method | Description |
|---------|--------|-------------|
| List Files | `files.list` | Lấy danh sách files |
| Get File | `files.get` | Lấy metadata file |
| Upload File | `files.create` | Upload file lên Drive |
| Share File | `permissions.create` | Chia sẻ file |
| Download | `files.get` | Download file content |

### 5. Google Maps Platform

| Feature | API | Description |
|---------|-----|-------------|
| Geocoding | Maps Geocoding API | Địa chỉ → Lat/Lng |
| Directions | Maps Directions API | Tính route |
| Places | Places API | Tìm kiếm địa điểm |
| Distance Matrix | Distance Matrix API | Ma trận khoảng cách |
| Elevation | Elevation API | Độ cao terrain |

## Quick Start

### 1. Setup Google Cloud Project

```bash
# 1. Create project in Google Cloud Console
# https://console.cloud.google.com

# 2. Enable required APIs:
# - Google Sheets API
# - Gmail API
# - Google Calendar API
# - Drive API
# - (other APIs as needed)

# 3. Create OAuth 2.0 credentials
# - Application type: Desktop app (for local)
# - Or: Web application (for server)

# 4. Download credentials.json
```

### 2. Python Integration

```python
from tools.api_integrations.google_integration import (
    GoogleSheetsClient,
    GmailClient,
    CalendarClient,
    DriveClient
)

# Google Sheets
sheets = GoogleSheetsClient(credentials_path="credentials.json")
spreadsheet = sheets.create(title="My Report")
sheets.update_values(
    spreadsheet_id=spreadsheet["spreadsheetId"],
    range="Sheet1!A1",
    values=[["Name", "Value"], ["Item 1", 100]]
)

# Gmail
gmail = GmailClient(credentials_path="credentials.json")
gmail.send_message(
    to="recipient@example.com",
    subject="Hello",
    body="This is a test email"
)

# Calendar
calendar = CalendarClient(credentials_path="credentials.json")
event = calendar.create_event(
    summary="Meeting",
    start="2024-01-15T10:00:00+07:00",
    end="2024-01-15T11:00:00+07:00",
    attendees=["alice@example.com", "bob@example.com"]
)

# Drive
drive = DriveClient(credentials_path="credentials.json")
files = drive.list_files(folder_id="ROOT_FOLDER_ID")
```

## Google Sheets Advanced

### 1. Read & Write Operations

```python
from tools.api_integrations.google_integration import GoogleSheetsClient

client = GoogleSheetsClient(credentials_path="credentials.json")

# Read range
data = client.get_values(
    spreadsheet_id="SPREADSHEET_ID",
    range="Sheet1!A1:C10"
)
print(data)  # [['Name', 'Age', 'City'], ['Alice', '25', 'Hanoi'], ...]

# Write values
client.update_values(
    spreadsheet_id="SPREADSHEET_ID",
    range="Sheet1!A5",
    values=[["Bob", "30", "Ho Chi Minh"]]
)

# Append row
client.append_values(
    spreadsheet_id="SPREADSHEET_ID",
    range="Sheet1!A:A",
    values=[["Charlie", "35", "Da Nang"]]
)
```

### 2. Formatting

```python
# Format header row
client.batch_update(
    spreadsheet_id="SPREADSHEET_ID",
    requests=[
        {
            "repeatCell": {
                "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.2, "green": 0.2, "blue": 0.4},
                        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
                    }
                },
                "fields": "userEnteredFormat"
            }
        },
        {
            "freeze": {"rowCount": 1}
        }
    ]
)
```

### 3. Vietnamese Invoice Template

```python
# Create invoice sheet
invoice = client.create(title=f"Invoice #{invoice_id}")

# Set headers
client.update_values("Sheet1!A1", [
    ["HÓA ĐƠN BÁN HÀNG"],
    ["Số: ", invoice_id, "", "Ngày: ", date],
    ["Khách hàng: ", customer_name],
    ["Địa chỉ: ", customer_address],
    ["", ""],
    ["STT", "Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"]
])

# Add items
for i, item in enumerate(items, start=2):
    row = [i, item['name'], item['qty'], item['price'], item['qty'] * item['price']]
    client.update_values(f"Sheet1!A{i}", [row])
```

## Gmail Advanced

### 1. Search & Filter

```python
# Search messages
results = gmail.search(
    query="from:boss@example.com is:unread subject:report",
    max_results=10
)

# Get message details
for msg in results['messages']:
    message = gmail.get_message(msg['id'])
    print(f"From: {message['from']}")
    print(f"Subject: {message['subject']}")
    print(f"Body: {message['body'][:200]}")
```

### 2. Send with Attachments

```python
import base64

# Read file and encode
with open("document.pdf", "rb") as f:
    file_data = base64.b64encode(f.read()).decode()

gmail.send_message(
    to="recipient@example.com",
    subject="Invoice",
    body="Please find the invoice attached.",
    attachments=[
        {
            "filename": "invoice.pdf",
            "mimeType": "application/pdf",
            "data": file_data
        }
    ]
)
```

### 3. Create & Manage Labels

```python
# Create label
label = gmail.create_label(name="Projects/Cursor")

# Apply to message
gmail.modify_message(
    message_id="MESSAGE_ID",
    add_labels=["INBOX", "UNREAD"]
)
```

## Google Calendar Advanced

### 1. Recurring Events

```python
calendar.create_event(
    summary="Weekly Standup",
    start="2024-01-15T09:00:00+07:00",
    end="2024-01-15T09:30:00+07:00",
    recurrence=[
        "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR",
        "EXDATE;TZID=Asia/Ho_Chi_Minh:20240122T090000"
    ],
    reminders=[
        {"method": "popup", "minutes": 15}
    ]
)
```

### 2. Conference & Meet

```python
calendar.create_event(
    summary="Team Meeting",
    start="2024-01-15T14:00:00+07:00",
    end="2024-01-15T15:00:00+07:00",
    conference_data={
        "createRequest": {
            "conferenceSolutionKey": {"type": "hangoutsMeet"},
            "requestId": "unique-request-id"
        }
    },
    attendees=[
        {"email": "alice@example.com", "responseStatus": "needsAction"},
        {"email": "bob@example.com", "responseStatus": "needsAction"}
    ]
)
```

### 3. Vietnamese Holiday Calendar

```python
# Add Vietnamese holidays
holidays = [
    {"date": "2024-01-01", "name": "Tết Dương lịch"},
    {"date": "2024-04-30", "name": "Ngày Giải phóng miền Nam"},
    {"date": "2024-05-01", "name": "Ngày Quốc tế Lao động"},
    {"date": "2024-09-02", "name": "Ngày Quốc khánh"},
]

for holiday in holidays:
    calendar.create_event(
        summary=holiday['name'],
        start=holiday['date'],
        end=holiday['date'],
        all_day=True
    )
```

## Google Maps Integration

### 1. Geocoding (Address → Coordinates)

```python
from tools.api_integrations.google_integration import MapsClient

maps = MapsClient(api_key="YOUR_API_KEY")

# Vietnamese address
result = maps.geocode("123 Nguyễn Huệ, Quận 1, TP Hồ Chí Minh, Vietnam")
location = result[0]['geometry']['location']
print(f"Lat: {location['lat']}, Lng: {location['lng']}")
```

### 2. Directions

```python
# Direction with Vietnamese addresses
route = maps.directions(
    origin="Trường Đại học Bách Khoa, TP Hồ Chí Minh",
    destination="Sân bay Tân Sơn Nhất, TP Hồ Chí Minh",
    mode="driving",
    language="vi"
)

for leg in route[0]['legs']:
    print(f"Distance: {leg['distance']['text']}")
    print(f"Duration: {leg['duration']['text']}")
    for step in leg['steps']:
        print(f"  - {step['html_instructions']}")
```

### 3. Distance Matrix

```python
# Calculate delivery times
matrix = maps.distance_matrix(
    origins=["Store A, Hanoi", "Store B, Ho Chi Minh"],
    destinations=["Customer 1, Hanoi", "Customer 2, Ho Chi Minh"],
    mode="driving"
)

for row in matrix['rows']:
    for element in row['elements']:
        print(f"Distance: {element['distance']['text']}")
        print(f"Duration: {element['duration']['text']}")
```

## Best Practices

### 1. Credential Management

```python
import os

# ✅ Good: Use environment variable or path
client = GoogleSheetsClient(
    credentials_path=os.environ.get("GOOGLE_CREDENTIALS_PATH")
)

# ✅ Or use service account
client = GoogleSheetsClient(
    credentials_path="service-account.json"
)
```

### 2. Error Handling

```python
from googleapiclient.errors import HttpError

try:
    result = client.get_values("SPREADSHEET_ID", "Sheet1!A1")
except HttpError as e:
    if e.resp.status == 404:
        print("Spreadsheet not found")
    elif e.resp.status == 403:
        print("Permission denied - sharing needed")
    else:
        print(f"API Error: {e}")
```

### 3. Batch Operations

```python
# Batch read multiple ranges
data = client.batch_get_values(
    spreadsheet_id="ID",
    ranges=["Sheet1!A1:C10", "Sheet2!A1:B5"]
)

# Batch write
client.batch_update_values(
    spreadsheet_id="ID",
    data=[
        {"range": "Sheet1!A1", "values": [["Header 1", "Header 2"]]},
        {"range": "Sheet1!A2", "values": [["Data 1", "Data 2"]]}
    ]
)
```

## Integration with Cursor Framework

### Slash Commands

```
/sheets read "SPREADSHEET_ID" "Sheet1!A1:C10"
/sheets write "SPREADSHEET_ID" "Sheet1!A1" "Name,Value\nItem,100"
/gmail send "to@example.com" "Subject" "Body"
/calendar event "Meeting" "2024-01-15T10:00"
/maps geocode "123 Nguyen Hue, HCMC"
/maps directions "A" "B"
```

### Workflow Example

```yaml
# .cursor/workflows/daily-report.yaml
name: Daily Sales Report to Google Sheets
trigger:
  type: schedule
  cron: "0 18 * * *"  # 6 PM daily

steps:
  - name: Fetch sales data
    action: database.query
    query: "SELECT product, SUM(quantity) as qty FROM orders WHERE DATE(created_at) = CURDATE() GROUP BY product"

  - name: Update Google Sheet
    action: sheets.update_values
    params:
      spreadsheet_id: "{{ secrets.sales_sheet_id }}"
      range: "Daily!A2"
      values: "{{ sales_data }}"
```

## References

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Gmail API](https://developers.google.com/gmail/api)
- [Calendar API](https://developers.google.com/calendar/api)
- [Drive API](https://developers.google.com/drive/api)
- [Maps Platform](https://developers.google.com/maps/documentation)
- [Google Cloud Console](https://console.cloud.google.com)
