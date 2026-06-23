# Prompt: Database Design - Thiết kế Database

```markdown
# Database Design Workflow

## 1. DESIGN SCOPE
- **Type**: [OLTP / OLAP / Hybrid]
- **Database**: [PostgreSQL / MySQL / SQL Server / SQLite]
- **Scale**: [Small / Medium / Large / Enterprise]

## 2. CONTEXT LOADING
```
Load knowledge:
- knowledge/[database-type]/*
- knowledge/ddd/*
Load rules: [database-type].mdc, database.mdc
```

## 3. DESIGN STEPS

### Conceptual Design
- [ ] Identify entities
- [ ] Define relationships
- [ ] Create ER diagram

### Logical Design
- [ ] Normalize to 3NF/BCNF
- [ ] Define primary keys
- [ ] Define foreign keys
- [ ] Define constraints

### Physical Design
- [ ] Data types selection
- [ ] Index strategy
- [ ] Partition strategy
- [ ] Storage parameters

## 4. OUTPUT

### Tables
```sql
CREATE TABLE ...;
```

### Indexes
```sql
CREATE INDEX ...;
```

## 5. LIÊN KẾT
- [[../rules/database]] - Database Rules
- [[../rules/postgres]] - PostgreSQL Rules
```
