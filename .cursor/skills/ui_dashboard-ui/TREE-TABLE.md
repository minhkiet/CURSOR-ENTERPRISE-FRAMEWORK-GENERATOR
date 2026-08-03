# Tree Table Library

Hierarchical/Tree table designs với expand/collapse, multiple styles, và full data management.

## 1. TREE TABLE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│ TREE TABLE ANATOMY                                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. TREE HEADER          │ Title, count, toggle all             │
│ 2. TOOLBAR              │ Search, filters, actions             │
│ 3. TREE COLUMNS         │ Expand toggle, hierarchical data    │
│ 4. TREE ROWS            │ Nested rows, indent, icons          │
│ 5. TREE FOOTER         │ Pagination, summary                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ TREE STRUCTURE                                                  │
├─────────────────────────────────────────────────────────────────┤
│ 📁 Technology                                          [Expand]  │
│   📂 Frontend                                               [+][⋯]│
│     📄 React.js                                         [+][⋯] │
│     📄 Vue.js                                            [+][⋯] │
│   📂 Backend                                               [+][⋯]│
│     📄 Node.js                                           [+][⋯] │
│     📄 Python                                            [+][⋯] │
│ 📁 Marketing                                        [Expand]      │
│   📂 SEO                                                 [+][⋯] │
│   📂 Content                                            [+][⋯] │
└─────────────────────────────────────────────────────────────────┘
```

## 2. TREE TABLE - FILE BROWSER STYLE

```tsx
// ✅ FILE BROWSER TREE TABLE
const FileTreeTable = ({ data, onFileClick, onFolderToggle }) => {
  const [expandedIds, setExpandedIds] = useState(new Set())
  const [selectedId, setSelectedId] = useState(null)
  
  const toggleExpand = (id) => {
    const newExpanded = new Set(expandedIds)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpandedIds(newExpanded)
    onFolderToggle?.(id)
  }
  
  const renderRow = (item, level = 0) => {
    const isFolder = item.type === 'folder'
    const isExpanded = expandedIds.has(item.id)
    const isSelected = selectedId === item.id
    const hasChildren = item.children?.length > 0
    
    return (
      <>
        <tr 
          key={item.id}
          className={`hover:bg-gray-50 cursor-pointer transition-colors ${isSelected ? 'bg-violet-50' : ''}`}
          onClick={() => {
            setSelectedId(item.id)
            if (isFolder) toggleExpand(item.id)
            else onFileClick?.(item)
          }}
        >
          <td className="px-4 py-3">
            <div className="flex items-center" style={{ paddingLeft: `${level * 24}px` }}>
              {/* Expand/Collapse button */}
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  toggleExpand(item.id)
                }}
                className={`w-6 h-6 flex items-center justify-center rounded hover:bg-gray-200 transition-colors ${
                  isFolder ? 'text-gray-500' : 'invisible'
                }`}
              >
                <ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
              </button>
              
              {/* Icon */}
              <div className="w-8 h-8 rounded-lg flex items-center justify-center mr-3">
                {item.type === 'folder' ? (
                  isExpanded ? (
                    <FolderOpen className="w-5 h-5 text-yellow-500" />
                  ) : (
                    <Folder className="w-5 h-5 text-yellow-500" />
                  )
                ) : (
                  <FileText className="w-5 h-5 text-gray-400" />
                )}
              </div>
              
              {/* Name */}
              <span className="font-medium text-gray-900">{item.name}</span>
              
              {/* File count for folders */}
              {isFolder && item.count !== undefined && (
                <span className="ml-2 text-xs text-gray-400">({item.count})</span>
              )}
            </div>
          </td>
          <td className="px-4 py-3 text-sm text-gray-500">{item.modified}</td>
          <td className="px-4 py-3 text-sm text-gray-500">{item.size}</td>
          <td className="px-4 py-3">
            {isFolder && (
              <div className="flex items-center gap-1">
                <button className="p-1.5 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-600">
                  <FolderPlus className="w-4 h-4" />
                </button>
                <button className="p-1.5 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-600">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            )}
            {!isFolder && (
              <button className="p-1.5 rounded hover:bg-gray-100 text-gray-400 hover:text-gray-600">
                <MoreHorizontal className="w-4 h-4" />
              </button>
            )}
          </td>
        </tr>
        
        {/* Children */}
        {isExpanded && hasChildren && item.children.map(child => renderRow(child, level + 1))}
      </>
    )
  }
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <TableToolbar data={data} />
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                Name
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider w-40">
                Modified
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider w-24">
                Size
              </th>
              <th className="px-4 py-3 w-20"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {data.map(item => renderRow(item))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
```

## 3. TREE TABLE - ORGANIZATION CHART

```tsx
// ✅ ORG CHART TREE TABLE
const OrgChartTable = ({ employees }) => {
  const [expandedIds, setExpandedIds] = useState(new Set(['ceo']))
  
  const toggleExpand = (id) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  const renderRow = (employee, level = 0) => {
    const isExpanded = expandedIds.has(employee.id)
    const hasChildren = employee.children?.length > 0
    
    return (
      <>
        <tr key={employee.id} className="hover:bg-gray-50 transition-colors">
          <td className="px-4 py-4">
            <div 
              className="flex items-center gap-4"
              style={{ paddingLeft: `${level * 40}px` }}
            >
              {/* Connector line */}
              {level > 0 && (
                <div className="absolute left-0 w-6 border-l-2 border-gray-200" />
              )}
              
              {/* Expand button */}
              {hasChildren && (
                <button
                  onClick={() => toggleExpand(employee.id)}
                  className="w-6 h-6 flex items-center justify-center rounded hover:bg-gray-200 text-gray-500"
                >
                  <ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                </button>
              )}
              {!hasChildren && <div className="w-6" />}
              
              {/* Avatar */}
              <img 
                src={employee.avatar}
                alt={employee.name}
                className="w-10 h-10 rounded-full object-cover ring-2 ring-white shadow-sm"
              />
              
              {/* Info */}
              <div>
                <p className="font-medium text-gray-900">{employee.name}</p>
                <p className="text-sm text-gray-500">{employee.position}</p>
              </div>
            </div>
          </td>
          <td className="px-4 py-4">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              employee.department === 'Engineering' ? 'bg-blue-50 text-blue-700' :
              employee.department === 'Marketing' ? 'bg-green-50 text-green-700' :
              employee.department === 'Sales' ? 'bg-purple-50 text-purple-700' :
              'bg-gray-50 text-gray-700'
            }`}>
              {employee.department}
            </span>
          </td>
          <td className="px-4 py-4 text-sm text-gray-500">{employee.email}</td>
          <td className="px-4 py-4 text-sm text-gray-500">{employee.phone}</td>
          <td className="px-4 py-4">
            <div className="flex items-center gap-2">
              {hasChildren && (
                <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded-full">
                  {employee.children.length} reports
                </span>
              )}
              <RowActions employee={employee} />
            </div>
          </td>
        </tr>
        
        {/* Children */}
        {isExpanded && hasChildren && employee.children.map(child => renderRow(child, level + 1))}
      </>
    )
  }
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <TableToolbar data={employees} title="Organization" />
      
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Employee
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Department
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Email
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Phone
            </th>
            <th className="px-4 py-3 w-32"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {employees.map(emp => renderRow(emp))}
        </tbody>
      </table>
      
      <TableFooter total={countAllEmployees(employees)} />
    </div>
  )
}
```

## 4. TREE TABLE - PRODUCT CATEGORY

```tsx
// ✅ PRODUCT CATEGORY TREE TABLE
const CategoryTreeTable = ({ categories }) => {
  const [expandedIds, setExpandedIds] = useState(new Set())
  const [selectedIds, setSelectedIds] = useState(new Set())
  
  const toggleExpand = (id) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  const toggleSelect = (id) => {
    setSelectedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  const renderRow = (category, level = 0) => {
    const isExpanded = expandedIds.has(category.id)
    const isSelected = selectedIds.has(category.id)
    const hasChildren = category.children?.length > 0
    
    return (
      <>
        <tr 
          key={category.id}
          className={`hover:bg-gray-50 transition-colors ${isSelected ? 'bg-violet-50' : ''}`}
        >
          {/* Checkbox */}
          <td className="px-4 py-3">
            <div style={{ paddingLeft: `${level * 24}px` }} className="flex items-center">
              {hasChildren ? (
                <button
                  onClick={() => toggleExpand(category.id)}
                  className="w-6 h-6 flex items-center justify-center rounded hover:bg-gray-200 text-gray-500"
                >
                  <ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                </button>
              ) : (
                <div className="w-6" />
              )}
              <Checkbox 
                checked={isSelected}
                onChange={() => toggleSelect(category.id)}
              />
            </div>
          </td>
          
          {/* Category info */}
          <td className="px-4 py-3">
            <div className="flex items-center gap-3">
              <div 
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: category.color + '20' }}
              >
                <span className="text-lg">{category.icon}</span>
              </div>
              <div>
                <p className="font-medium text-gray-900">{category.name}</p>
                <p className="text-sm text-gray-500">ID: {category.id}</p>
              </div>
            </div>
          </td>
          
          {/* Slug */}
          <td className="px-4 py-3">
            <code className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
              {category.slug}
            </code>
          </td>
          
          {/* Products count */}
          <td className="px-4 py-3">
            <span className="inline-flex items-center gap-1.5 text-sm">
              <Package className="w-4 h-4 text-gray-400" />
              {category.productCount} products
            </span>
          </td>
          
          {/* Status */}
          <td className="px-4 py-3">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              category.active ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-500'
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${category.active ? 'bg-green-500' : 'bg-gray-400'}`} />
              {category.active ? 'Active' : 'Inactive'}
            </span>
          </td>
          
          {/* Actions */}
          <td className="px-4 py-3">
            <RowActions category={category} onEdit={() => {}} onDelete={() => {}} />
          </td>
        </tr>
        
        {/* Children */}
        {isExpanded && hasChildren && category.children.map(child => renderRow(child, level + 1))}
      </>
    )
  }
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Toolbar */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Categories</h3>
            <p className="text-sm text-gray-500">
              {selectedIds.size > 0 ? `${selectedIds.size} selected` : `${flattenCategories(categories).length} total`}
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search categories..."
                className="pl-9 pr-4 py-2 w-64 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
              />
            </div>
            
            <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">
              <Filter className="w-4 h-4" />
              Filters
            </button>
            
            <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800">
              <Plus className="w-4 h-4" />
              Add Category
            </button>
          </div>
        </div>
        
        {/* Bulk actions */}
        {selectedIds.size > 0 && (
          <div className="flex items-center gap-4 mt-4 p-3 bg-violet-50 rounded-xl">
            <span className="text-sm font-medium text-violet-700">{selectedIds.size} selected</span>
            <div className="h-4 w-px bg-violet-200" />
            <button className="text-sm text-violet-700 hover:text-violet-800">Edit</button>
            <button className="text-sm text-violet-700 hover:text-violet-800">Move</button>
            <button className="text-sm text-red-600 hover:text-red-700">Delete</button>
          </div>
        )}
      </div>
      
      {/* Table */}
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="w-12 px-4 py-3"></th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Category
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Slug
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Products
            </th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
              Status
            </th>
            <th className="px-4 py-3 w-20"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {categories.map(cat => renderRow(cat))}
        </tbody>
      </table>
      
      <TableFooter total={flattenCategories(categories).length} />
    </div>
  )
}
```

## 5. TREE TABLE - PROJECT MILESTONE

```tsx
// ✅ PROJECT MILESTONE TREE TABLE
const MilestoneTreeTable = ({ projects }) => {
  const [expandedIds, setExpandedIds] = useState(new Set())
  
  const renderRow = (item, level = 0) => {
    const isExpanded = expandedIds.has(item.id)
    const isProject = item.type === 'project'
    const isMilestone = item.type === 'milestone'
    const isTask = item.type === 'task'
    
    const progressColor = item.progress >= 75 ? 'bg-green-500' : 
                          item.progress >= 50 ? 'bg-blue-500' :
                          item.progress >= 25 ? 'bg-yellow-500' : 'bg-red-500'
    
    return (
      <>
        <tr className="hover:bg-gray-50 transition-colors">
          {/* Expand */}
          <td className="px-4 py-3">
            <div style={{ paddingLeft: `${level * 24}px` }} className="flex items-center">
              {item.children?.length > 0 && (
                <button
                  onClick={() => toggleExpand(item.id)}
                  className="w-6 h-6 flex items-center justify-center rounded hover:bg-gray-200 text-gray-500"
                >
                  <ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                </button>
              )}
              {!(item.children?.length > 0) && <div className="w-6" />}
            </div>
          </td>
          
          {/* Name with icon */}
          <td className="px-4 py-3">
            <div className="flex items-center gap-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                isProject ? 'bg-violet-100' :
                isMilestone ? 'bg-blue-100' : 'bg-gray-100'
              }`}>
                {isProject ? <FolderKanban className="w-4 h-4 text-violet-600" /> :
                 isMilestone ? <Flag className="w-4 h-4 text-blue-600" /> :
                 <CheckSquare className="w-4 h-4 text-gray-600" />}
              </div>
              <div>
                <p className={`font-medium ${isTask ? 'text-gray-700' : 'text-gray-900'}`}>
                  {item.name}
                </p>
                {item.description && (
                  <p className="text-sm text-gray-500 truncate max-w-xs">{item.description}</p>
                )}
              </div>
            </div>
          </td>
          
          {/* Progress */}
          <td className="px-4 py-3">
            <div className="flex items-center gap-3">
              <div className="w-24 h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  className={`h-full ${progressColor} rounded-full transition-all`}
                  style={{ width: `${item.progress}%` }}
                />
              </div>
              <span className="text-sm text-gray-600 w-10">{item.progress}%</span>
            </div>
          </td>
          
          {/* Assignees */}
          <td className="px-4 py-3">
            <div className="flex items-center">
              {item.assignees.slice(0, 3).map((a, i) => (
                <img 
                  key={i}
                  src={a.avatar}
                  alt={a.name}
                  className="w-8 h-8 rounded-full border-2 border-white -ml-2 first:ml-0"
                  title={a.name}
                />
              ))}
              {item.assignees.length > 3 && (
                <div className="w-8 h-8 rounded-full bg-gray-100 border-2 border-white -ml-2 flex items-center justify-center text-xs font-medium text-gray-600">
                  +{item.assignees.length - 3}
                </div>
              )}
            </div>
          </td>
          
          {/* Due date */}
          <td className="px-4 py-3">
            <span className={`text-sm ${isOverdue(item.dueDate) ? 'text-red-600' : 'text-gray-600'}`}>
              {formatDate(item.dueDate)}
            </span>
          </td>
          
          {/* Priority */}
          <td className="px-4 py-3">
            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-medium ${
              item.priority === 'high' ? 'bg-red-50 text-red-700' :
              item.priority === 'medium' ? 'bg-yellow-50 text-yellow-700' :
              'bg-green-50 text-green-700'
            }`}>
              {item.priority === 'high' && <ArrowUp className="w-3 h-3" />}
              {item.priority}
            </span>
          </td>
          
          {/* Status */}
          <td className="px-4 py-3">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              item.status === 'completed' ? 'bg-green-50 text-green-700' :
              item.status === 'in_progress' ? 'bg-blue-50 text-blue-700' :
              item.status === 'blocked' ? 'bg-red-50 text-red-700' :
              'bg-gray-50 text-gray-700'
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${
                item.status === 'completed' ? 'bg-green-500' :
                item.status === 'in_progress' ? 'bg-blue-500' :
                item.status === 'blocked' ? 'bg-red-500' :
                'bg-gray-400'
              }`} />
              {item.status.replace('_', ' ')}
            </span>
          </td>
          
          {/* Actions */}
          <td className="px-4 py-3">
            <RowActions item={item} />
          </td>
        </tr>
        
        {/* Children */}
        {isExpanded && item.children?.map(child => renderRow(child, level + 1))}
      </>
    )
  }
  
  const toggleExpand = (id) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <ProjectToolbar />
      
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="w-12 px-4 py-3"></th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Name</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase w-40">Progress</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Assignees</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Due Date</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Priority</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Status</th>
            <th className="px-4 py-3 w-20"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {projects.map(p => renderRow(p))}
        </tbody>
      </table>
      
      <TableFooter total={countAllItems(projects)} />
    </div>
  )
}
```

## 6. TREE TABLE - MENU/NAVIGATION

```tsx
// ✅ MENU TREE TABLE
const MenuTreeTable = ({ menus }) => {
  const [expandedIds, setExpandedIds] = useState(new Set())
  const [dragId, setDragId] = useState(null)
  
  const handleDragStart = (e, id) => {
    setDragId(id)
    e.dataTransfer.effectAllowed = 'move'
  }
  
  const handleDrop = (e, targetId) => {
    e.preventDefault()
    // Handle reorder logic
    setDragId(null)
  }
  
  const renderRow = (menu, level = 0) => {
    const isExpanded = expandedIds.has(menu.id)
    const hasChildren = menu.children?.length > 0
    
    return (
      <>
        <tr 
          draggable
          onDragStart={(e) => handleDragStart(e, menu.id)}
          onDrop={(e) => handleDrop(e, menu.id)}
          onDragOver={(e) => e.preventDefault()}
          className={`hover:bg-gray-50 cursor-move transition-colors ${dragId === menu.id ? 'opacity-50' : ''}`}
        >
          {/* Drag handle */}
          <td className="px-4 py-3">
            <div style={{ paddingLeft: `${level * 24}px` }} className="flex items-center">
              <GripVertical className="w-5 h-5 text-gray-300 cursor-grab" />
              {hasChildren && (
                <button
                  onClick={() => toggleExpand(menu.id)}
                  className="w-6 h-6 flex items-center justify-center rounded hover:bg-gray-200 text-gray-500"
                >
                  <ChevronRight className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                </button>
              )}
            </div>
          </td>
          
          {/* Menu info */}
          <td className="px-4 py-3">
            <div className="flex items-center gap-3">
              {menu.icon && (
                <div className="w-10 h-10 rounded-lg bg-gray-100 flex items-center justify-center">
                  <img src={menu.icon} alt="" className="w-5 h-5" />
                </div>
              )}
              <div>
                <p className="font-medium text-gray-900">{menu.label}</p>
                <p className="text-sm text-gray-500">{menu.path}</p>
              </div>
            </div>
          </td>
          
          {/* Path */}
          <td className="px-4 py-3">
            <code className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">
              {menu.path || '/'}
            </code>
          </td>
          
          {/* Order */}
          <td className="px-4 py-3">
            <span className="text-sm text-gray-500">{menu.order}</span>
          </td>
          
          {/* Target */}
          <td className="px-4 py-3">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              menu.target === '_blank' ? 'bg-blue-50 text-blue-700' : 'bg-gray-50 text-gray-700'
            }`}>
              {menu.target === '_blank' ? <ExternalLink className="w-3 h-3" /> : <Link className="w-3 h-3" />}
              {menu.target || '_self'}
            </span>
          </td>
          
          {/* Visibility */}
          <td className="px-4 py-3">
            <div className="flex items-center gap-2">
              {menu.showOnDesktop && (
                <Desktop className="w-4 h-4 text-gray-400" title="Desktop" />
              )}
              {menu.showOnTablet && (
                <Tablet className="w-4 h-4 text-gray-400" title="Tablet" />
              )}
              {menu.showOnMobile && (
                <Smartphone className="w-4 h-4 text-gray-400" title="Mobile" />
              )}
            </div>
          </td>
          
          {/* Status */}
          <td className="px-4 py-3">
            <ToggleSwitch checked={menu.active} />
          </td>
          
          {/* Actions */}
          <td className="px-4 py-3">
            <RowActions menu={menu} />
          </td>
        </tr>
        
        {isExpanded && hasChildren && menu.children.map(child => renderRow(child, level + 1))}
      </>
    )
  }
  
  const toggleExpand = (id) => {
    setExpandedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Navigation Menu</h3>
          <p className="text-sm text-gray-500">Drag to reorder items</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50">
            <Download className="w-4 h-4" />
            Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-medium hover:bg-violet-700">
            <Plus className="w-4 h-4" />
            Add Menu
          </button>
        </div>
      </div>
      
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="w-16 px-4 py-3"></th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Menu</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Path</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase w-20">Order</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Target</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Devices</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase w-24">Active</th>
            <th className="px-4 py-3 w-20"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {menus.map(menu => renderRow(menu))}
        </tbody>
      </table>
    </div>
  )
}
```

## 7. EXPAND/COLLAPSE ALL FEATURE

```tsx
// ✅ EXPAND/COLLAPSE ALL
const ExpandCollapseAll = ({ onExpandAll, onCollapseAll, isAllExpanded }) => {
  return (
    <div className="flex items-center gap-1">
      <button
        onClick={onExpandAll}
        className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded"
        title="Expand all"
      >
        <ChevronsDownUp className="w-4 h-4" />
      </button>
      <button
        onClick={onCollapseAll}
        className="px-2 py-1 text-xs text-gray-600 hover:bg-gray-100 rounded"
        title="Collapse all"
      >
        <ChevronsUpDown className="w-4 h-4" />
      </button>
    </div>
  )
}

// Usage
const [expandedIds, setExpandedIds] = useState(new Set())

const expandAll = () => {
  setExpandedIds(new Set(getAllIds(data)))
}

const collapseAll = () => {
  setExpandedIds(new Set())
}
```

## 8. ADVANCED FEATURES

### 8.1 Lazy Loading Children

```tsx
// ✅ LAZY LOAD CHILDREN
const LazyTreeRow = ({ item, onLoadChildren }) => {
  const [expanded, setExpanded] = useState(false)
  const [loading, setLoading] = useState(false)
  const [children, setChildren] = useState([])
  
  const handleExpand = async () => {
    if (expanded) {
      setExpanded(false)
      return
    }
    
    if (!children.length) {
      setLoading(true)
      const data = await onLoadChildren(item.id)
      setChildren(data)
    }
    setExpanded(true)
    setLoading(false)
  }
  
  return (
    <>
      <tr>
        <td>
          <button onClick={handleExpand} disabled={loading}>
            {loading ? <Loader2 className="animate-spin" /> : 
              <ChevronRight className={`w-4 h-4 ${expanded ? 'rotate-90' : ''}`} />}
          </button>
        </td>
        {/* other cells */}
      </tr>
      {expanded && children.map(child => <ChildRow key={child.id} data={child} />)}
    </>
  )
}
```

### 8.2 Virtual Scrolling for Large Trees

```tsx
// ✅ VIRTUAL SCROLLING
import { useVirtualizer } from 'react-virtual'

const VirtualizedTreeTable = ({ data }) => {
  const flatData = useMemo(() => flattenTree(data), [data])
  
  const virtualizer = useVirtualizer({
    count: flatData.length,
    getScrollElement: () => scrollRef.current,
    estimateSize: () => 56,
  })
  
  return (
    <div ref={scrollRef} className="overflow-auto h-[600px]">
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: virtualRow.start,
              width: '100%',
            }}
          >
            <TreeRow data={flatData[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

### 8.3 Checkbox with Children Selection

```tsx
// ✅ CHECKBOX WITH CHILDREN
const TreeCheckbox = ({ item, checked, onChange }) => {
  const isIndeterminate = item.children?.length > 0 && 
    item.children.some(c => !isAllSelected(c))
  
  return (
    <Checkbox
      checked={checked}
      indeterminate={isIndeterminate}
      onChange={() => onChange(item.id)}
    />
  )
}

const isAllSelected = (item) => {
  if (!item.children?.length) return selectedIds.has(item.id)
  return item.children.every(c => isAllSelected(c))
}

const selectAllChildren = (item) => {
  const ids = [item.id]
  if (item.children) {
    item.children.forEach(c => ids.push(...selectAllChildren(c)))
  }
  return ids
}
```

### 8.4 Search in Tree

```tsx
// ✅ TREE SEARCH
const TreeSearch = ({ data, onFilter }) => {
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedIds, setExpandedIds] = useState(new Set())
  
  const filteredData = useMemo(() => {
    if (!searchTerm) return data
    
    const matches = findMatches(data, searchTerm.toLowerCase())
    // Expand parents of matches
    const parentIds = getParentIds(matches)
    setExpandedIds(new Set(parentIds))
    
    return filterTree(data, searchTerm.toLowerCase())
  }, [data, searchTerm])
  
  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search..."
        className="..."
      />
      <TreeTable data={filteredData} expandedIds={expandedIds} />
    </div>
  )
}
```

## 9. ROW ACTIONS

```tsx
// ✅ ROW ACTIONS
const RowActions = ({ item, onEdit, onDelete, onAddChild, onDuplicate }) => {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-gray-100 text-gray-500">
          <MoreHorizontal className="w-5 h-5" />
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-48">
        <DropdownMenuItem onClick={() => onEdit?.(item)}>
          <Pencil className="w-4 h-4 mr-2" />
          Edit
        </DropdownMenuItem>
        {item.type === 'folder' && (
          <DropdownMenuItem onClick={() => onAddChild?.(item)}>
            <FolderPlus className="w-4 h-4 mr-2" />
            Add Sub-item
          </DropdownMenuItem>
        )}
        <DropdownMenuItem onClick={() => onDuplicate?.(item)}>
          <Copy className="w-4 h-4 mr-2" />
          Duplicate
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => onDelete?.(item)} className="text-red-600">
          <Trash2 className="w-4 h-4 mr-2" />
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

## 10. EXPORT/IMPORT

```tsx
// ✅ EXPORT TREE TABLE
const exportTreeTable = async (data) => {
  const flattened = flattenTreeWithLevel(data)
  
  const exportData = flattened.map(item => ({
    'Level': item.level,
    'Name': item.name,
    'Type': item.type,
    'Status': item.status,
    'Created': item.createdAt,
    'Updated': item.updatedAt,
  }))
  
  const ws = XLSX.utils.json_to_sheet(exportData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Tree Data')
  XLSX.writeFile(wb, 'tree-data.xlsx')
}

// ✅ EXPORT TEMPLATE
const exportTreeTemplate = () => {
  const template = [
    { Name: 'Parent Item 1', Parent: '', Type: 'folder', Status: 'active' },
    { Name: 'Child Item 1.1', Parent: 'Parent Item 1', Type: 'item', Status: 'active' },
    { Name: 'Child Item 1.2', Parent: 'Parent Item 1', Type: 'item', Status: 'inactive' },
  ]
  
  const ws = XLSX.utils.json_to_sheet(template)
  XLSX.writeFile(wb, 'tree-template.xlsx')
}

// ✅ IMPORT WITH PARENT MAPPING
const importTreeData = async (file) => {
  const data = await parseExcel(file)
  
  // Build tree from flat data
  const tree = buildTree(data, {
    idKey: 'id',
    parentKey: 'parent',
    labelKey: 'name',
  })
  
  return tree
}
```

## 11. TABLE VARIATIONS

### 11.1 Compact Tree Table

```tsx
// ✅ COMPACT STYLE
const CompactTreeTable = ({ data }) => (
  <table className="w-full text-sm">
    <tbody>
      {flattenTree(data).map(item => (
        <tr key={item.id} className="hover:bg-gray-50">
          <td className="py-1.5" style={{ paddingLeft: `${item.level * 16}px` }}>
            <span className={item.isFolder ? 'font-medium' : ''}>
              {item.icon} {item.name}
            </span>
          </td>
          <td className="py-1.5">{item.value}</td>
          <td className="py-1.5">{item.status}</td>
        </tr>
      ))}
    </tbody>
  </table>
)
```

### 11.2 Cards Tree View (Mobile)

```tsx
// ✅ CARDS TREE VIEW
const CardsTreeView = ({ data, level = 0 }) => (
  <div className="space-y-2">
    {data.map(item => (
      <div 
        key={item.id}
        className={`bg-white rounded-xl border p-4 ${level > 0 ? 'ml-4 border-l-4 border-l-violet-200' : ''}`}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            {item.icon}
            <span className="font-medium">{item.name}</span>
          </div>
          <span className={`px-2 py-0.5 rounded text-xs ${item.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
            {item.active ? 'Active' : 'Inactive'}
          </span>
        </div>
        {item.description && <p className="text-sm text-gray-500 mb-2">{item.description}</p>}
        {item.children?.length > 0 && (
          <CardsTreeView data={item.children} level={level + 1} />
        )}
      </div>
    ))}
  </div>
)
```

## Icons for Tree Table

```tsx
import {
  // Expand/Collapse
  ChevronRight, ChevronDown, ChevronsDownUp, ChevronsUpDown,
  
  // File/Folder
  Folder, FolderOpen, FolderPlus, File, FileText, FileSpreadsheet,
  
  // Status
  Check, CheckCircle, X, XCircle, AlertCircle,
  
  // Actions
  MoreHorizontal, Plus, Pencil, Trash2, Copy, Eye, Edit,
  ExternalLink, Link, GripVertical,
  
  // Categories
  Package, Flag, CheckSquare, Target, LayoutDashboard,
  
  // Devices
  Desktop, Tablet, Smartphone,
  
  // User
  User, Users, UserPlus,
  
  // Misc
  Search, Filter, Download, Upload, Calendar, Loader2,
} from 'lucide-react'
```

## Tree Table Checklist

- [ ] Expand/Collapse buttons
- [ ] Indentation for levels
- [ ] Connector lines (optional)
- [ ] Drag & drop reordering
- [ ] Checkbox selection with parent/child
- [ ] Expand/Collapse all
- [ ] Search with parent expansion
- [ ] Lazy loading children
- [ ] Virtual scrolling for large trees
- [ ] Multiple tree styles (file, org, category, menu)
- [ ] Row actions dropdown
- [ ] Inline add/edit
- [ ] Export to Excel
- [ ] Import with parent mapping
- [ ] Export template
- [ ] Date filters
- [ ] Status filters
- [ ] Pagination
- [ ] Mobile cards view
- [ ] Keyboard navigation
- [ ] Keyboard shortcuts
