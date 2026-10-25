# Table Library - Comprehensive Guide

Professional table designs with pagination, filtering, sorting, and data management.

## 1. TABLE COMPONENTS OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│ TABLE ANATOMY                                                    │
├─────────────────────────────────────────────────────────────────┤
│ 1. TABLE HEADER           │ Title, count, view toggers         │
│ 2. TABLE TOOLBAR          │ Search, filters, actions           │
│ 3. COLUMN HEADERS          │ Sortable, resizable, selectable     │
│ 4. TABLE BODY             │ Rows with cells                     │
│ 5. TABLE FOOTER           │ Pagination, summary                 │
│ 6. BULK ACTIONS           │ Selected rows actions               │
└─────────────────────────────────────────────────────────────────┘
```

## 2. TABLE VARIATIONS

### 2.1 Data Table (Default)

```tsx
// ✅ DATA TABLE
const DataTable = ({ data, columns, onRowClick }) => {
  const [selectedRows, setSelectedRows] = useState([])
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' })
  const [filters, setFilters] = useState({})
  
  // Sort & Filter logic
  const processedData = useMemo(() => {
    let result = [...data]
    
    // Apply filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        result = result.filter(row => 
          String(row[key]).toLowerCase().includes(value.toLowerCase())
        )
      }
    })
    
    // Apply sort
    if (sortConfig.key) {
      result.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) 
          return sortConfig.direction === 'asc' ? -1 : 1
        if (a[sortConfig.key] > b[sortConfig.key]) 
          return sortConfig.direction === 'asc' ? 1 : -1
        return 0
      })
    }
    
    return result
  }, [data, filters, sortConfig])
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Toolbar */}
      <TableToolbar
        data={data}
        selectedRows={selectedRows}
        onExport={() => exportToExcel(data)}
        onImport={() => openImportModal()}
        filters={filters}
        onFilterChange={setFilters}
      />
      
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="w-10 px-4 py-3">
                <Checkbox 
                  checked={selectedRows.length === processedData.length}
                  onChange={(e) => setSelectedRows(e.target.checked ? processedData.map(r => r.id) : [])}
                />
              </th>
              {columns.map(col => (
                <th 
                  key={col.key}
                  className={`px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ${
                    col.sortable ? 'cursor-pointer hover:bg-gray-100 select-none' : ''
                  }`}
                  style={{ width: col.width }}
                  onClick={() => col.sortable && handleSort(col.key)}
                >
                  <div className="flex items-center gap-2">
                    {col.label}
                    {col.sortable && (
                      <div className="flex flex-col">
                        <ChevronUp 
                          className={`w-3 h-3 -mb-1 ${sortConfig.key === col.key && sortConfig.direction === 'asc' ? 'text-violet-600' : 'text-gray-300'}`} 
                        />
                        <ChevronDown 
                          className={`w-3 h-3 ${sortConfig.key === col.key && sortConfig.direction === 'desc' ? 'text-violet-600' : 'text-gray-300'}`} 
                        />
                      </div>
                    )}
                  </div>
                </th>
              ))}
              <th className="w-20 px-4 py-3"></th>
            </tr>
          </thead>
          
          <tbody className="divide-y divide-gray-100">
            {processedData.map(row => (
              <tr 
                key={row.id} 
                className="hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={() => onRowClick?.(row)}
              >
                <td className="px-4 py-4" onClick={(e) => e.stopPropagation()}>
                  <Checkbox 
                    checked={selectedRows.includes(row.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedRows([...selectedRows, row.id])
                      } else {
                        setSelectedRows(selectedRows.filter(id => id !== row.id))
                      }
                    }}
                  />
                </td>
                {columns.map(col => (
                  <td key={col.key} className="px-4 py-4">
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
                <td className="px-4 py-4" onClick={(e) => e.stopPropagation()}>
                  <RowActions row={row} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Footer */}
      <TableFooter
        total={processedData.length}
        selected={selectedRows.length}
        onPageChange={handlePageChange}
        currentPage={currentPage}
        pageSize={pageSize}
      />
    </div>
  )
}
```

### 2.2 Table with Avatar & Status

```tsx
// ✅ TABLE WITH AVATAR & STATUS
const columns = [
  {
    key: 'user',
    label: 'User',
    render: (row) => (
      <div className="flex items-center gap-3">
        <img 
          src={row.avatar} 
          alt={row.name}
          className="w-10 h-10 rounded-full object-cover"
        />
        <div>
          <p className="font-medium text-gray-900">{row.name}</p>
          <p className="text-sm text-gray-500">{row.email}</p>
        </div>
      </div>
    )
  },
  {
    key: 'role',
    label: 'Role',
    render: (row) => (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
        <Shield className="w-3 h-3" />
        {row.role}
      </span>
    )
  },
  {
    key: 'status',
    label: 'Status',
    render: (row) => {
      const statusConfig = {
        active: { bg: 'bg-green-50', text: 'text-green-700', dot: 'bg-green-500', label: 'Active' },
        inactive: { bg: 'bg-gray-50', text: 'text-gray-700', dot: 'bg-gray-500', label: 'Inactive' },
        pending: { bg: 'bg-yellow-50', text: 'text-yellow-700', dot: 'bg-yellow-500', label: 'Pending' },
        banned: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-500', label: 'Banned' },
      }
      const config = statusConfig[row.status] || statusConfig.inactive
      
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
          {config.label}
        </span>
      )
    }
  },
  {
    key: 'department',
    label: 'Department',
    render: (row) => (
      <span className="text-sm text-gray-700">{row.department}</span>
    )
  },
  {
    key: 'joined',
    label: 'Joined',
    render: (row) => (
      <span className="text-sm text-gray-500">{formatDate(row.joined)}</span>
    )
  },
]
```

### 2.3 Table with Tags

```tsx
// ✅ TABLE WITH TAGS
const columns = [
  {
    key: 'project',
    label: 'Project',
    render: (row) => (
      <div>
        <p className="font-medium text-gray-900">{row.name}</p>
        <p className="text-sm text-gray-500">{row.client}</p>
      </div>
    )
  },
  {
    key: 'tags',
    label: 'Tags',
    render: (row) => (
      <div className="flex flex-wrap gap-1.5">
        {row.tags.map((tag, i) => (
          <span 
            key={i}
            className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
            style={{ backgroundColor: tag.bgColor, color: tag.textColor }}
          >
            {tag.label}
          </span>
        ))}
        {row.tags.length > 3 && (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
            +{row.tags.length - 3}
          </span>
        )}
      </div>
    )
  },
  {
    key: 'priority',
    label: 'Priority',
    render: (row) => {
      const colors = {
        critical: 'bg-red-100 text-red-700',
        high: 'bg-orange-100 text-orange-700',
        medium: 'bg-yellow-100 text-yellow-700',
        low: 'bg-green-100 text-green-700',
      }
      return (
        <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium ${colors[row.priority]}`}>
          <Flag className="w-3 h-3" />
          {row.priority}
        </span>
      )
    }
  },
  {
    key: 'progress',
    label: 'Progress',
    render: (row) => (
      <div className="w-32">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>{row.progress}%</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div 
            className="h-full rounded-full transition-all"
            style={{ 
              width: `${row.progress}%`,
              backgroundColor: row.progress === 100 ? '#22c55e' : '#8b5cf6'
            }}
          />
        </div>
      </div>
    )
  },
]
```

### 2.4 Table with Image Gallery

```tsx
// ✅ TABLE WITH IMAGE COLUMNS
const columns = [
  {
    key: 'product',
    label: 'Product',
    render: (row) => (
      <div className="flex items-center gap-3">
        <img 
          src={row.image} 
          alt={row.name}
          className="w-14 h-14 rounded-xl object-cover"
        />
        <div>
          <p className="font-medium text-gray-900">{row.name}</p>
          <p className="text-sm text-gray-500">SKU: {row.sku}</p>
        </div>
      </div>
    )
  },
  {
    key: 'gallery',
    label: 'Gallery',
    render: (row) => (
      <div className="flex items-center gap-1">
        {row.images.slice(0, 3).map((img, i) => (
          <img 
            key={i}
            src={img}
            alt=""
            className="w-10 h-10 rounded-lg object-cover"
          />
        ))}
        {row.images.length > 3 && (
          <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center text-xs font-medium text-gray-600">
            +{row.images.length - 3}
          </div>
        )}
      </div>
    )
  },
  {
    key: 'category',
    label: 'Category',
    render: (row) => (
      <div className="flex items-center gap-2">
        <span 
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: row.categoryColor }}
        />
        <span className="text-sm text-gray-700">{row.category}</span>
      </div>
    )
  },
  {
    key: 'price',
    label: 'Price',
    render: (row) => (
      <div className="text-right">
        <p className="font-semibold text-gray-900">${row.price.toLocaleString()}</p>
        {row.originalPrice && (
          <p className="text-xs text-gray-400 line-through">${row.originalPrice.toLocaleString()}</p>
        )}
      </div>
    )
  },
  {
    key: 'stock',
    label: 'Stock',
    render: (row) => {
      const isLow = row.stock < 10
      return (
        <span className={`inline-flex items-center gap-1 ${isLow ? 'text-red-600' : 'text-gray-700'}`}>
          <Package className="w-4 h-4" />
          {row.stock} units
        </span>
      )
    }
  },
]
```

### 2.5 Table with Avatar Group & Metrics

```tsx
// ✅ TABLE WITH METRICS
const columns = [
  {
    key: 'campaign',
    label: 'Campaign',
    render: (row) => (
      <div>
        <p className="font-medium text-gray-900">{row.name}</p>
        <p className="text-sm text-gray-500">{row.channel}</p>
      </div>
    )
  },
  {
    key: 'team',
    label: 'Team',
    render: (row) => (
      <div className="flex items-center">
        {row.members.slice(0, 3).map((m, i) => (
          <img 
            key={i}
            src={m.avatar}
            alt={m.name}
            className="w-8 h-8 rounded-full border-2 border-white -ml-2 first:ml-0"
            title={m.name}
          />
        ))}
        {row.members.length > 3 && (
          <div className="w-8 h-8 rounded-full bg-gray-100 border-2 border-white -ml-2 flex items-center justify-center text-xs font-medium text-gray-600">
            +{row.members.length - 3}
          </div>
        )}
      </div>
    )
  },
  {
    key: 'metrics',
    label: 'Impressions',
    render: (row) => (
      <div className="text-right">
        <p className="font-semibold text-gray-900">{formatNumber(row.impressions)}</p>
        <p className={`text-xs ${row.impressionsChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {row.impressionsChange >= 0 ? '+' : ''}{row.impressionsChange}%
        </p>
      </div>
    )
  },
  {
    key: 'metrics',
    label: 'Clicks',
    render: (row) => (
      <div className="text-right">
        <p className="font-semibold text-gray-900">{formatNumber(row.clicks)}</p>
        <p className={`text-xs ${row.clicksChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {row.clicksChange >= 0 ? '+' : ''}{row.clicksChange}%
        </p>
      </div>
    )
  },
  {
    key: 'metrics',
    label: 'CTR',
    render: (row) => (
      <div className="text-right">
        <p className="font-semibold text-gray-900">{row.ctr}%</p>
        <p className={`text-xs ${row.ctrChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {row.ctrChange >= 0 ? '+' : ''}{row.ctrChange}%
        </p>
      </div>
    )
  },
  {
    key: 'metrics',
    label: 'Conversions',
    render: (row) => (
      <div className="text-right">
        <p className="font-semibold text-gray-900">{formatNumber(row.conversions)}</p>
        <p className={`text-xs ${row.conversionsChange >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {row.conversionsChange >= 0 ? '+' : ''}{row.conversionsChange}%
        </p>
      </div>
    )
  },
  {
    key: 'budget',
    label: 'Budget',
    render: (row) => (
      <div>
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>${formatNumber(row.spent)}</span>
          <span>${formatNumber(row.budget)}</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden w-24">
          <div 
            className={`h-full rounded-full ${row.spent > row.budget ? 'bg-red-500' : 'bg-blue-500'}`}
            style={{ width: `${Math.min((row.spent / row.budget) * 100, 100)}%` }}
          />
        </div>
      </div>
    )
  },
]
```

## 3. TABLE TOOLBAR

```tsx
// ✅ TABLE TOOLBAR
const TableToolbar = ({ 
  total, 
  selected, 
  onExport, 
  onImport,
  onDelete,
  filters,
  onFilterChange,
  onSearch,
}) => {
  const [showFilters, setShowFilters] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  
  return (
    <div className="px-6 py-4 border-b border-gray-200">
      {/* Top row */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Users</h3>
            <p className="text-sm text-gray-500">
              {selected > 0 ? `${selected} selected` : `${total} total`}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value)
                onSearch?.(e.target.value)
              }}
              className="pl-9 pr-4 py-2 w-64 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
          </div>
          
          {/* Filter button */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-2 border rounded-lg text-sm font-medium transition-colors ${
              showFilters 
                ? 'bg-violet-50 border-violet-200 text-violet-700' 
                : 'border-gray-200 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <Filter className="w-4 h-4" />
            Filters
            {Object.values(filters).some(v => v) && (
              <span className="w-5 h-5 rounded-full bg-violet-500 text-white text-xs flex items-center justify-center">
                {Object.values(filters).filter(Boolean).length}
              </span>
            )}
          </button>
          
          {/* Import */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">
                <Upload className="w-4 h-4" />
                Import
                <ChevronDown className="w-4 h-4" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={onImport}>
                <FileSpreadsheet className="w-4 h-4 mr-2" />
                Import Excel
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onImport}>
                <FileJson className="w-4 h-4 mr-2" />
                Import JSON
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={onExport}>
                <Download className="w-4 h-4 mr-2" />
                Export Template
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          
          {/* Export */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800">
                <Download className="w-4 h-4" />
                Export
                <ChevronDown className="w-4 h-4" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => onExport('xlsx')}>
                <FileSpreadsheet className="w-4 h-4 mr-2" />
                Export Excel (.xlsx)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onExport('csv')}>
                <FileText className="w-4 h-4 mr-2" />
                Export CSV (.csv)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onExport('pdf')}>
                <FileText className="w-4 h-4 mr-2" />
                Export PDF (.pdf)
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          
          {/* Add new */}
          <button className="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-medium hover:bg-violet-700">
            <Plus className="w-4 h-4" />
            Add New
          </button>
        </div>
      </div>
      
      {/* Filter row */}
      {showFilters && (
        <FilterRow filters={filters} onFilterChange={onFilterChange} />
      )}
      
      {/* Bulk actions */}
      {selected > 0 && (
        <BulkActions 
          selected={selected} 
          onDelete={onDelete}
          onClear={() => {}}
        />
      )}
    </div>
  )
}

// ✅ FILTER ROW
const FilterRow = ({ filters, onFilterChange }) => {
  return (
    <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-xl">
      {/* Date range */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Created:</label>
        <DateRangePicker
          startDate={filters.startDate}
          endDate={filters.endDate}
          onChange={(start, end) => onFilterChange({ ...filters, startDate: start, endDate: end })}
        />
      </div>
      
      {/* Status filter */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Status:</label>
        <Select
          value={filters.status}
          onChange={(value) => onFilterChange({ ...filters, status: value })}
        >
          <SelectTrigger className="w-32">
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Role filter */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Role:</label>
        <Select
          value={filters.role}
          onChange={(value) => onFilterChange({ ...filters, role: value })}
        >
          <SelectTrigger className="w-32">
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All</SelectItem>
            <SelectItem value="admin">Admin</SelectItem>
            <SelectItem value="editor">Editor</SelectItem>
            <SelectItem value="viewer">Viewer</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Clear filters */}
      <button 
        onClick={() => onFilterChange({})}
        className="text-xs text-gray-500 hover:text-gray-700"
      >
        Clear all
      </button>
    </div>
  )
}

// ✅ BULK ACTIONS BAR
const BulkActions = ({ selected, onDelete, onExport, onEdit }) => {
  return (
    <div className="flex items-center gap-4 p-3 bg-violet-50 rounded-xl mt-4">
      <span className="text-sm font-medium text-violet-700">
        {selected} selected
      </span>
      
      <div className="h-4 w-px bg-violet-200" />
      
      <button 
        onClick={onEdit}
        className="flex items-center gap-1.5 text-sm text-violet-700 hover:text-violet-800"
      >
        <Pencil className="w-4 h-4" />
        Edit
      </button>
      
      <button 
        onClick={onExport}
        className="flex items-center gap-1.5 text-sm text-violet-700 hover:text-violet-800"
      >
        <Download className="w-4 h-4" />
        Export
      </button>
      
      <button 
        onClick={onDelete}
        className="flex items-center gap-1.5 text-sm text-red-600 hover:text-red-700"
      >
        <Trash2 className="w-4 h-4" />
        Delete
      </button>
    </div>
  )
}
```

## 4. ROW ACTIONS

```tsx
// ✅ ROW ACTIONS DROPDOWN
const RowActions = ({ row, onEdit, onDelete, onDuplicate, onView }) => {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-500 transition-colors">
          <MoreHorizontal className="w-5 h-5" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuItem onClick={() => onView?.(row)}>
          <Eye className="w-4 h-4 mr-2" />
          View Details
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => onEdit?.(row)}>
          <Pencil className="w-4 h-4 mr-2" />
          Edit
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => onDuplicate?.(row)}>
          <Copy className="w-4 h-4 mr-2" />
          Duplicate
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => onDelete?.(row)} className="text-red-600">
          <Trash2 className="w-4 h-4 mr-2" />
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

// ✅ ROW ACTIONS INLINE
const InlineActions = ({ row }) => {
  return (
    <div className="flex items-center gap-1">
      <button 
        className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors"
        title="View"
      >
        <Eye className="w-4 h-4" />
      </button>
      <button 
        className="p-2 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors"
        title="Edit"
      >
        <Pencil className="w-4 h-4" />
      </button>
      <button 
        className="p-2 rounded-lg hover:bg-red-50 text-gray-500 hover:text-red-600 transition-colors"
        title="Delete"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  )
}

// ✅ ROW ACTIONS ICON BUTTONS
const IconButtonActions = ({ row }) => {
  return (
    <div className="flex items-center gap-1">
      <IconButton icon={<Eye />} tooltip="View" onClick={() => {}} />
      <IconButton icon={<Pencil />} tooltip="Edit" onClick={() => {}} />
      <IconButton icon={<Trash2 />} tooltip="Delete" variant="danger" onClick={() => {}} />
    </div>
  )
}
```

## 5. PAGINATION

```tsx
// ✅ TABLE PAGINATION
const TableFooter = ({ total, selected, currentPage, pageSize, onPageChange }) => {
  const totalPages = Math.ceil(total / pageSize)
  
  return (
    <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-500">
          Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, total)} of {total} results
        </span>
        
        <select
          value={pageSize}
          onChange={(e) => onPageChange(1, Number(e.target.value))}
          className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
        >
          <option value={10}>10 / page</option>
          <option value={25}>25 / page</option>
          <option value={50}>50 / page</option>
          <option value={100}>100 / page</option>
        </select>
      </div>
      
      <div className="flex items-center gap-1">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-5 h-5 text-gray-500" />
        </button>
        
        {/* Page numbers */}
        {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
          let page
          if (totalPages <= 5) {
            page = i + 1
          } else if (currentPage <= 3) {
            page = i + 1
          } else if (currentPage >= totalPages - 2) {
            page = totalPages - 4 + i
          } else {
            page = currentPage - 2 + i
          }
          
          return (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
                currentPage === page
                  ? 'bg-violet-600 text-white'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
            >
              {page}
            </button>
          )
        })}
        
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronRight className="w-5 h-5 text-gray-500" />
        </button>
      </div>
    </div>
  )
}

// ✅ SIMPLE PAGINATION
const SimplePagination = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="flex items-center justify-center gap-2">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm disabled:opacity-50"
      >
        Previous
      </button>
      
      <span className="px-3 py-1.5 text-sm text-gray-600">
        Page {currentPage} of {totalPages}
      </span>
      
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-1.5 rounded-lg border border-gray-200 text-sm disabled:opacity-50"
      >
        Next
      </button>
    </div>
  )
}
```

## 6. EXPORT/IMPORT

### 6.1 Export Functions

```tsx
// ✅ EXPORT TO EXCEL
const exportToExcel = async (data, filename = 'export') => {
  const XLSX = await import('xlsx')
  
  // Prepare data
  const exportData = data.map(row => ({
    'ID': row.id,
    'Name': row.name,
    'Email': row.email,
    'Status': row.status,
    'Role': row.role,
    'Created At': formatDate(row.createdAt),
    'Updated At': formatDate(row.updatedAt),
  }))
  
  // Create workbook
  const ws = XLSX.utils.json_to_sheet(exportData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Data')
  
  // Auto-width columns
  const colWidths = Object.keys(exportData[0]).map(key => ({
    wch: Math.max(key.length, ...exportData.map(row => String(row[key]).length)) + 2
  }))
  ws['!cols'] = colWidths
  
  // Download
  XLSX.writeFile(wb, `${filename}.xlsx`)
}

// ✅ EXPORT TO CSV
const exportToCSV = (data, filename = 'export') => {
  const headers = Object.keys(data[0]).join(',')
  const rows = data.map(row => Object.values(row).join(','))
  const csv = [headers, ...rows].join('\n')
  
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

// ✅ EXPORT TO PDF
const exportToPDF = async (data, columns, title = 'Report') => {
  const { jsPDF } = await import('jspdf')
  const doc = new jsPDF()
  
  // Title
  doc.setFontSize(20)
  doc.text(title, 20, 20)
  doc.setFontSize(10)
  doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 30)
  
  // Table
  const startY = 40
  const colWidth = 190 / columns.length
  
  // Headers
  doc.setFontSize(10)
  doc.setFont(undefined, 'bold')
  columns.forEach((col, i) => {
    doc.text(col.label, 20 + i * colWidth, startY)
  })
  
  // Rows
  doc.setFont(undefined, 'normal')
  data.forEach((row, rowIndex) => {
    const y = startY + 10 + rowIndex * 7
    columns.forEach((col, i) => {
      const value = col.render ? col.render(row) : row[col.key]
      doc.text(String(value).substring(0, 30), 20 + i * colWidth, y)
    })
  })
  
  doc.save(`${title.toLowerCase().replace(/\s/g, '-')}.pdf`)
}

// ✅ EXPORT TEMPLATE
const exportTemplate = async (columns) => {
  const template = columns.map(col => ({
    [col.label]: col.example || '',
    ...(col.required && { [`${col.label} (Required)`]: col.example || '' })
  }))
  
  const XLSX = await import('xlsx')
  const ws = XLSX.utils.json_to_sheet(template)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Template')
  XLSX.writeFile(wb, 'import-template.xlsx')
}
```

### 6.2 Import Modal

```tsx
// ✅ IMPORT MODAL
const ImportModal = ({ isOpen, onClose, onImport, columns }) => {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState([])
  const [errors, setErrors] = useState([])
  const [mapping, setMapping] = useState({})
  
  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    setFile(file)
    
    // Parse file
    const data = await parseFile(file)
    setPreview(data.slice(0, 5))
    
    // Auto-map columns
    const autoMapping = {}
    columns.forEach(col => {
      const match = data.columns.find(c => 
        c.toLowerCase().includes(col.key.toLowerCase()) ||
        col.label.toLowerCase().includes(c.toLowerCase())
      )
      if (match) autoMapping[col.key] = match
    })
    setMapping(autoMapping)
  }
  
  const handleImport = () => {
    // Validate & import
    const result = validateAndImport(file, mapping)
    if (result.errors.length > 0) {
      setErrors(result.errors)
    } else {
      onImport(result.data)
      onClose()
    }
  }
  
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Import Data</DialogTitle>
          <DialogDescription>
            Upload a file to import data. Supported formats: .xlsx, .csv, .json
          </DialogDescription>
        </DialogHeader>
        
        {/* Upload area */}
        <div className="border-2 border-dashed border-gray-200 rounded-xl p-8 text-center">
          <input
            type="file"
            accept=".xlsx,.csv,.json"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-sm text-gray-600">
              Drag & drop or <span className="text-violet-600">browse</span>
            </p>
            <p className="text-xs text-gray-400 mt-2">XLSX, CSV, JSON</p>
          </label>
        </div>
        
        {/* Preview */}
        {preview.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-2">Preview ({preview.length} rows)</h4>
            <div className="overflow-x-auto border border-gray-200 rounded-lg">
              <table className="w-full text-xs">
                <thead className="bg-gray-50">
                  <tr>
                    {preview.columns.map(col => (
                      <th key={col} className="px-3 py-2 text-left">{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {preview.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((val, j) => (
                        <td key={j} className="px-3 py-2 border-t">{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        
        {/* Column mapping */}
        {preview.length > 0 && (
          <div>
            <h4 className="text-sm font-medium mb-2">Map Columns</h4>
            <div className="grid grid-cols-2 gap-4">
              {columns.filter(c => c.required).map(col => (
                <div key={col.key}>
                  <label className="text-xs text-gray-600 mb-1 block">{col.label}</label>
                  <select
                    value={mapping[col.key] || ''}
                    onChange={(e) => setMapping({ ...mapping, [col.key]: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm"
                  >
                    <option value="">Select column</option>
                    {preview.columns.map(col => (
                      <option key={col} value={col}>{col}</option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {/* Errors */}
        {errors.length > 0 && (
          <div className="p-4 bg-red-50 rounded-lg">
            <p className="text-sm text-red-600 font-medium mb-2">Errors found:</p>
            <ul className="text-xs text-red-600 space-y-1">
              {errors.map((err, i) => <li key={i}>{err}</li>)}
            </ul>
          </div>
        )}
        
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleImport} disabled={!file}>
            Import {preview.length} Rows
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

## 7. DATE FILTER

```tsx
// ✅ DATE RANGE PICKER
const DateRangePicker = ({ startDate, endDate, onChange }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [preset, setPreset] = useState('')
  
  const presets = [
    { label: 'Today', value: 'today', start: today, end: today },
    { label: 'Yesterday', value: 'yesterday', start: yesterday, end: yesterday },
    { label: 'Last 7 days', value: '7days', start: subDays(today, 7), end: today },
    { label: 'Last 30 days', value: '30days', start: subDays(today, 30), end: today },
    { label: 'This week', value: 'week', start: startOfWeek(today), end: today },
    { label: 'This month', value: 'month', start: startOfMonth(today), end: today },
    { label: 'Last month', value: 'lastMonth', start: startOfLastMonth, end: endOfLastMonth },
    { label: 'This year', value: 'year', start: startOfYear(today), end: today },
    { label: 'Custom', value: 'custom', start: null, end: null },
  ]
  
  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <button className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
          <Calendar className="w-4 h-4 text-gray-400" />
          <span className={startDate && endDate ? 'text-gray-900' : 'text-gray-400'}>
            {startDate && endDate 
              ? `${formatDate(startDate)} - ${formatDate(endDate)}`
              : 'Select dates'
            }
          </span>
        </button>
      </PopoverTrigger>
      
      <PopoverContent className="w-auto p-4" align="start">
        <div className="space-y-4">
          {/* Presets */}
          <div className="grid grid-cols-3 gap-2">
            {presets.map(p => (
              <button
                key={p.value}
                onClick={() => {
                  setPreset(p.value)
                  if (p.start && p.end) {
                    onChange(p.start, p.end)
                    setIsOpen(false)
                  }
                }}
                className={`px-3 py-1.5 text-xs rounded-lg transition-colors ${
                  preset === p.value 
                    ? 'bg-violet-100 text-violet-700' 
                    : 'hover:bg-gray-100'
                }`}
              >
                {p.label}
              </button>
            ))}
          </div>
          
          {/* Custom range */}
          {preset === 'custom' && (
            <div className="flex items-center gap-2 pt-2 border-t">
              <div>
                <label className="text-xs text-gray-500">From</label>
                <input
                  type="date"
                  value={startDate || ''}
                  onChange={(e) => onChange(e.target.value, endDate)}
                  className="px-2 py-1 border border-gray-200 rounded text-sm"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500">To</label>
                <input
                  type="date"
                  value={endDate || ''}
                  onChange={(e) => onChange(startDate, e.target.value)}
                  className="px-2 py-1 border border-gray-200 rounded text-sm"
                />
              </div>
            </div>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}

// ✅ CREATED DATE FILTER
const CreatedDateFilter = ({ value, onChange }) => {
  const options = [
    { value: '', label: 'All time' },
    { value: 'today', label: 'Today' },
    { value: 'yesterday', label: 'Yesterday' },
    { value: '7days', label: 'Last 7 days' },
    { value: '30days', label: 'Last 30 days' },
    { value: '90days', label: 'Last 90 days' },
    { value: 'thisYear', label: 'This year' },
    { value: 'custom', label: 'Custom range' },
  ]
  
  return (
    <Select value={value} onChange={onChange}>
      <SelectTrigger className="w-40">
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {options.map(opt => (
          <SelectItem key={opt.value} value={opt.value}>
            {opt.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
```

## 8. ADVANCED TABLE FEATURES

### 8.1 Expandable Rows

```tsx
// ✅ EXPANDABLE ROW
const ExpandableRow = ({ row }) => {
  const [isExpanded, setIsExpanded] = useState(false)
  
  return (
    <>
      <tr onClick={() => setIsExpanded(!isExpanded)} className="cursor-pointer">
        <td><ChevronRight className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-90' : ''}`} /></td>
        {/* other cells */}
      </tr>
      {isExpanded && (
        <tr>
          <td colSpan={columns.length + 1} className="bg-gray-50 p-4">
            <div className="ml-12">
              {/* Expanded content */}
              <p className="text-sm text-gray-600 mb-2">Additional details...</p>
              <pre className="text-xs bg-white p-2 rounded">{JSON.stringify(row, null, 2)}</pre>
            </div>
          </td>
        </tr>
      )}
    </>
  )
}
```

### 8.2 Sticky Header & Columns

```tsx
// ✅ STICKY TABLE
const StickyTable = ({ data, columns }) => {
  return (
    <div className="overflow-auto max-h-[600px]">
      <table className="w-full">
        <thead className="sticky top-0 z-10 bg-white shadow-sm">
          <tr>
            {columns.map(col => (
              <th key={col.key}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map(row => (
            <tr key={row.id}>
              {columns.map(col => (
                <td key={col.key}>{col.render ? col.render(row) : row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

// ✅ STICKY FIRST COLUMN
<table className="w-full">
  <colgroup>
    <col className="sticky left-0 bg-white z-20" /> {/* Sticky column */}
    <col /> {/* Regular columns */}
  </colgroup>
</table>
```

### 8.3 Loading & Empty States

```tsx
// ✅ LOADING STATE
const TableSkeleton = ({ rows = 5, columns = 5 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          {Array.from({ length: columns }).map((_, j) => (
            <div 
              key={j} 
              className="h-10 bg-gray-100 rounded animate-pulse"
              style={{ width: `${20 + Math.random() * 30}%` }}
            />
          ))}
        </div>
      ))}
    </div>
  )
}

// ✅ EMPTY STATE
const EmptyState = ({ title, description, icon: Icon, action }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <Icon className="w-8 h-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-medium text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-500 mb-6">{description}</p>
      {action && <Button onClick={action.onClick}>{action.label}</Button>}
    </div>
  )
}

// Usage
{processedData.length === 0 ? (
  <EmptyState 
    title="No results found"
    description="Try adjusting your search or filters"
    icon={Search}
    action={{ label: 'Clear filters', onClick: () => {} }}
  />
) : (
  <TableBody />
)}
```

## 9. COLUMN TYPES

```tsx
// ✅ COLUMN DEFINITIONS
const columnTypes = {
  // Text
  text: {
    render: (row, key) => <span>{row[key]}</span>
  },
  
  // Number
  number: {
    render: (row, key) => <span className="font-mono">{row[key].toLocaleString()}</span>
  },
  
  // Currency
  currency: {
    render: (row, key) => <span>${row[key].toLocaleString()}</span>
  },
  
  // Percentage
  percentage: {
    render: (row, key) => (
      <div className="flex items-center gap-2">
        <span>{row[key]}%</span>
        <div className="w-16 h-1.5 bg-gray-100 rounded-full">
          <div className="h-full bg-violet-500 rounded-full" style={{ width: `${row[key]}%` }} />
        </div>
      </div>
    )
  },
  
  // Boolean
  boolean: {
    render: (row, key) => (
      row[key] 
        ? <Check className="w-5 h-5 text-green-500" />
        : <X className="w-5 h-5 text-gray-300" />
    )
  },
  
  // Avatar
  avatar: {
    render: (row, key) => (
      <img src={row[key]} className="w-10 h-10 rounded-full" />
    )
  },
  
  // Avatar + Name
  user: {
    render: (row) => (
      <div className="flex items-center gap-3">
        <img src={row.avatar} className="w-10 h-10 rounded-full" />
        <div>
          <p className="font-medium">{row.name}</p>
          <p className="text-sm text-gray-500">{row.email}</p>
        </div>
      </div>
    )
  },
  
  // Image
  image: {
    render: (row, key) => (
      <img src={row[key]} className="w-14 h-14 rounded-xl object-cover" />
    )
  },
  
  // Tag
  tag: {
    render: (row, key, config) => {
      const styles = config.styles || {}
      return (
        <span 
          className="inline-flex px-2 py-1 rounded-full text-xs font-medium"
          style={{ backgroundColor: styles.bg, color: styles.text }}
        >
          {row[key]}
        </span>
      )
    }
  },
  
  // Status
  status: {
    render: (row, key, config) => {
      const status = config.statuses[row[key]] || {}
      return (
        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${status.bg} ${status.text}`}>
          <span className={`w-1.5 h-1.5 rounded-full ${status.dot}`} />
          {status.label || row[key]}
        </span>
      )
    }
  },
  
  // Date
  date: {
    render: (row, key) => formatDate(row[key])
  },
  
  // DateTime
  datetime: {
    render: (row, key) => formatDateTime(row[key])
  },
  
  // Relative time
  relativeTime: {
    render: (row, key) => formatRelativeTime(row[key])
  },
  
  // Progress
  progress: {
    render: (row, key) => (
      <div className="w-32">
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-violet-500 rounded-full" style={{ width: `${row[key]}%` }} />
        </div>
        <span className="text-xs text-gray-500 mt-1">{row[key]}%</span>
      </div>
    )
  },
  
  // Actions
  actions: {
    render: (row, key, config) => (
      <RowActions 
        row={row} 
        actions={config.actions || ['view', 'edit', 'delete']}
      />
    )
  },
}
```

## 10. TABLE STYLES

### 10.1 Minimal Table

```tsx
// ✅ MINIMAL TABLE
const MinimalTable = ({ data, columns }) => (
  <table className="w-full">
    <thead>
      <tr>
        {columns.map(col => (
          <th key={col.key} className="pb-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            {col.label}
          </th>
        ))}
      </tr>
    </thead>
    <tbody className="divide-y divide-gray-100">
      {data.map(row => (
        <tr key={row.id}>
          {columns.map(col => (
            <td key={col.key} className="py-4 text-sm text-gray-900">
              {col.render ? col.render(row) : row[col.key]}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
)
```

### 10.2 Bordered Table

```tsx
// ✅ BORDERED TABLE
const BorderedTable = ({ data, columns }) => (
  <div className="border border-gray-200 rounded-xl overflow-hidden">
    <table className="w-full">
      <thead className="bg-gray-50">
        <tr>
          {columns.map(col => (
            <th key={col.key} className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200">
        {data.map(row => (
          <tr key={row.id} className="hover:bg-gray-50">
            {columns.map(col => (
              <td key={col.key} className="px-4 py-3 text-sm">
                {col.render ? col.render(row) : row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
)
```

### 10.3 Striped Table

```tsx
// ✅ STRIPED TABLE
const StripedTable = ({ data, columns }) => (
  <table className="w-full">
    <thead>
      <tr>
        {columns.map(col => (
          <th key={col.key} className="bg-gray-50 px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">
            {col.label}
          </th>
        ))}
      </tr>
    </thead>
    <tbody className="divide-y divide-gray-100">
      {data.map((row, i) => (
        <tr key={row.id} className={i % 2 === 1 ? 'bg-gray-50' : 'bg-white'}>
          {columns.map(col => (
            <td key={col.key} className="px-4 py-3 text-sm">
              {col.render ? col.render(row) : row[col.key]}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  </table>
)
```

### 10.4 Cards View (Mobile-friendly)

```tsx
// ✅ CARDS VIEW (MOBILE)
const CardsView = ({ data, columns }) => (
  <div className="grid gap-4 md:hidden">
    {data.map(row => (
      <div key={row.id} className="bg-white rounded-xl border border-gray-200 p-4">
        {/* Card header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            {columns.find(c => c.key === 'avatar' || c.key === 'image')?.render?.(row)}
            <div>
              {columns.find(c => c.key === 'name' || c.key === 'title')?.render?.(row)}
            </div>
          </div>
          {columns.find(c => c.key === 'status')?.render?.(row)}
        </div>
        
        {/* Card details */}
        <div className="space-y-2">
          {columns
            .filter(c => !['avatar', 'image', 'name', 'title', 'status', 'actions'].includes(c.key))
            .map(col => (
              <div key={col.key} className="flex justify-between text-sm">
                <span className="text-gray-500">{col.label}</span>
                <span className="text-gray-900">{col.render ? col.render(row) : row[col.key]}</span>
              </div>
            ))}
        </div>
        
        {/* Card actions */}
        <div className="mt-4 pt-4 border-t flex justify-end">
          {columns.find(c => c.key === 'actions')?.render?.(row)}
        </div>
      </div>
    ))}
  </div>
)
```

## Table Checklist

- [ ] Search input with clear button
- [ ] Multiple filter options (status, date, category)
- [ ] Sortable columns (asc/desc indicators)
- [ ] Row selection (checkbox)
- [ ] Bulk actions bar
- [ ] Pagination (with page size selector)
- [ ] Export buttons (Excel, CSV, PDF)
- [ ] Import modal with preview
- [ ] Template export
- [ ] Date range picker
- [ ] Row actions dropdown
- [ ] Loading skeleton
- [ ] Empty state
- [ ] Sticky header on scroll
- [ ] Responsive (cards on mobile)
- [ ] Hover states
- [ ] Keyboard navigation
