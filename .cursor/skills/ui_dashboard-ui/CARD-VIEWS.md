# Card View Library

Beautiful card-based data display với multiple styles, grids, and full data management.

## 1. CARD VIEW OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│ CARD VIEW VARIATIONS                                             │
├─────────────────────────────────────────────────────────────────┤
│ 1. GRID VIEW           │ Masonry, uniform grid                │
│ 2. LIST VIEW           │ Cards in vertical list               │
│ 3. COMPACT VIEW        │ Small thumbnails                      │
│ 4. DETAIL VIEW         │ Large featured cards                 │
│ 5. KANBAN VIEW         │ Column-based cards                   │
│ 6. GALLERY VIEW        │ Image-focused cards                  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. CARD GRID VIEW - UNIFORM

```tsx
// ✅ CARD GRID VIEW (UNIFORM)
const CardGridView = ({ data, onCardClick, onAction }) => {
  const [selectedIds, setSelectedIds] = useState(new Set())
  const [searchTerm, setSearchTerm] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  const [filters, setFilters] = useState({})
  const itemsPerPage = 12
  
  // Filter & Search
  const filteredData = useMemo(() => {
    let result = data
    
    if (searchTerm) {
      result = result.filter(item => 
        item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.description?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        result = result.filter(item => item[key] === value)
      }
    })
    
    return result
  }, [data, searchTerm, filters])
  
  // Pagination
  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage
    return filteredData.slice(start, start + itemsPerPage)
  }, [filteredData, currentPage])
  
  const totalPages = Math.ceil(filteredData.length / itemsPerPage)
  
  const toggleSelect = (id) => {
    setSelectedIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }
  
  return (
    <div className="space-y-6">
      {/* Toolbar */}
      <CardToolbar
        total={filteredData.length}
        selected={selectedIds.size}
        searchTerm={searchTerm}
        onSearch={setSearchTerm}
        filters={filters}
        onFilterChange={setFilters}
        onExport={() => exportData(filteredData)}
        onImport={() => openImportModal()}
        onDelete={() => deleteSelected(selectedIds)}
      />
      
      {/* Bulk Actions */}
      {selectedIds.size > 0 && (
        <BulkActionsBar
          selected={selectedIds.size}
          onClear={() => setSelectedIds(new Set())}
          onDelete={() => deleteSelected(selectedIds)}
          onExport={() => exportSelected(selectedIds)}
        />
      )}
      
      {/* Card Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {paginatedData.map(item => (
          <CardItem
            key={item.id}
            item={item}
            isSelected={selectedIds.has(item.id)}
            onSelect={() => toggleSelect(item.id)}
            onClick={() => onCardClick?.(item)}
            onAction={onAction}
          />
        ))}
      </div>
      
      {/* Empty State */}
      {paginatedData.length === 0 && (
        <EmptyState
          title="No items found"
          description="Try adjusting your search or filters"
          icon={Search}
        />
      )}
      
      {/* Pagination */}
      <CardPagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
        total={filteredData.length}
        pageSize={itemsPerPage}
      />
    </div>
  )
}

// ✅ CARD ITEM
const CardItem = ({ item, isSelected, onSelect, onClick, onAction }) => {
  return (
    <div 
      className={`group bg-white rounded-2xl border-2 overflow-hidden transition-all duration-200 hover:shadow-lg hover:-translate-y-1 cursor-pointer ${
        isSelected ? 'border-violet-500 ring-2 ring-violet-200' : 'border-gray-100 hover:border-gray-200'
      }`}
      onClick={onClick}
    >
      {/* Cover Image */}
      {item.cover && (
        <div className="aspect-[16/10] overflow-hidden">
          <img 
            src={item.cover} 
            alt={item.title}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
      
      {/* Content */}
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            {/* Tags */}
            {item.tags?.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-2">
                {item.tags.slice(0, 3).map((tag, i) => (
                  <span 
                    key={i}
                    className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                    style={{ backgroundColor: tag.bgColor, color: tag.textColor }}
                  >
                    {tag.label}
                  </span>
                ))}
                {item.tags.length > 3 && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                    +{item.tags.length - 3}
                  </span>
                )}
              </div>
            )}
            
            {/* Title */}
            <h3 className="font-semibold text-gray-900 line-clamp-2 group-hover:text-violet-600 transition-colors">
              {item.title}
            </h3>
            
            {/* Description */}
            {item.description && (
              <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                {item.description}
              </p>
            )}
          </div>
          
          {/* Checkbox */}
          <button 
            onClick={(e) => { e.stopPropagation(); onSelect(); }}
            className={`w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all ${
              isSelected 
                ? 'bg-violet-600 border-violet-600' 
                : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            {isSelected && <Check className="w-4 h-4 text-white" />}
          </button>
        </div>
        
        {/* Meta */}
        <div className="space-y-3">
          {/* Status & Date */}
          <div className="flex items-center justify-between text-sm">
            <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              item.status === 'active' ? 'bg-green-50 text-green-700' :
              item.status === 'pending' ? 'bg-yellow-50 text-yellow-700' :
              'bg-gray-50 text-gray-700'
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${
                item.status === 'active' ? 'bg-green-500' :
                item.status === 'pending' ? 'bg-yellow-500' :
                'bg-gray-400'
              }`} />
              {item.status}
            </span>
            <span className="text-gray-400 flex items-center gap-1">
              <Calendar className="w-3.5 h-3.5" />
              {formatDate(item.createdAt)}
            </span>
          </div>
          
          {/* Progress */}
          {item.progress !== undefined && (
            <div>
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Progress</span>
                <span>{item.progress}%</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  className="h-full rounded-full transition-all duration-500"
                  style={{ 
                    width: `${item.progress}%`,
                    backgroundColor: item.progress === 100 ? '#22c55e' : '#8b5cf6'
                  }}
                />
              </div>
            </div>
          )}
          
          {/* Stats */}
          {item.stats && (
            <div className="flex items-center gap-4 pt-2 border-t border-gray-100">
              {item.stats.views && (
                <span className="flex items-center gap-1 text-xs text-gray-500">
                  <Eye className="w-3.5 h-3.5" />
                  {formatNumber(item.stats.views)}
                </span>
              )}
              {item.stats.likes && (
                <span className="flex items-center gap-1 text-xs text-gray-500">
                  <Heart className="w-3.5 h-3.5" />
                  {formatNumber(item.stats.likes)}
                </span>
              )}
              {item.stats.comments && (
                <span className="flex items-center gap-1 text-xs text-gray-500">
                  <MessageCircle className="w-3.5 h-3.5" />
                  {formatNumber(item.stats.comments)}
                </span>
              )}
            </div>
          )}
          
          {/* Assignees */}
          {item.assignees?.length > 0 && (
            <div className="flex items-center justify-between pt-2 border-t border-gray-100">
              <div className="flex items-center">
                {item.assignees.slice(0, 4).map((a, i) => (
                  <img 
                    key={i}
                    src={a.avatar}
                    alt={a.name}
                    className="w-7 h-7 rounded-full border-2 border-white -ml-2 first:ml-0"
                    title={a.name}
                  />
                ))}
                {item.assignees.length > 4 && (
                  <div className="w-7 h-7 rounded-full bg-gray-100 border-2 border-white -ml-2 flex items-center justify-center text-xs font-medium text-gray-600">
                    +{item.assignees.length - 4}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
      
      {/* Actions */}
      <CardActions item={item} onAction={onAction} />
    </div>
  )
}

// ✅ CARD ACTIONS (HOVER)
const CardActions = ({ item, onAction }) => {
  const [show, setShow] = useState(false)
  
  return (
    <div 
      className="absolute top-3 right-3 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
      onClick={(e) => e.stopPropagation()}
    >
      <button 
        onClick={() => onAction?.('edit', item)}
        className="w-8 h-8 bg-white rounded-lg shadow-md flex items-center justify-center text-gray-600 hover:text-violet-600 hover:scale-110 transition-all"
      >
        <Pencil className="w-4 h-4" />
      </button>
      <button 
        onClick={() => onAction?.('delete', item)}
        className="w-8 h-8 bg-white rounded-lg shadow-md flex items-center justify-center text-gray-600 hover:text-red-600 hover:scale-110 transition-all"
      >
        <Trash2 className="w-4 h-4" />
      </button>
    </div>
  )
}
```

## 3. CARD GRID VIEW - MASONRY

```tsx
// ✅ MASONRY CARD GRID
const MasonryGridView = ({ data }) => {
  return (
    <div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6 space-y-6">
      {data.map(item => (
        <div 
          key={item.id}
          className="break-inside-avoid bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
        >
          {/* Cover */}
          {item.cover && (
            <img src={item.cover} alt="" className="w-full" />
          )}
          
          <div className="p-5">
            {/* Tags */}
            {item.tags?.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mb-3">
                {item.tags.slice(0, 2).map((tag, i) => (
                  <span 
                    key={i}
                    className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
                    style={{ backgroundColor: tag.bgColor, color: tag.textColor }}
                  >
                    {tag.label}
                  </span>
                ))}
              </div>
            )}
            
            {/* Title */}
            <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
            
            {/* Description */}
            {item.description && (
              <p className="text-sm text-gray-500 line-clamp-3">{item.description}</p>
            )}
            
            {/* Footer */}
            <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
              <div className="flex items-center gap-2">
                <img src={item.author.avatar} className="w-6 h-6 rounded-full" />
                <span className="text-xs text-gray-500">{item.author.name}</span>
              </div>
              <span className="text-xs text-gray-400">{formatDate(item.createdAt)}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 4. FEATURED CARD VIEW

```tsx
// ✅ FEATURED CARD (LARGE)
const FeaturedCardView = ({ data }) => {
  const [selected, setSelected] = useState(data[0]?.id)
  
  const featured = data.find(d => d.id === selected)
  
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Featured */}
      <div className="lg:col-span-2">
        <div className="bg-white rounded-3xl border border-gray-100 overflow-hidden">
          {/* Large Cover */}
          {featured?.cover && (
            <div className="aspect-[2/1] overflow-hidden">
              <img 
                src={featured.cover} 
                alt={featured.title}
                className="w-full h-full object-cover"
              />
            </div>
          )}
          
          <div className="p-8">
            {/* Tags */}
            <div className="flex flex-wrap gap-2 mb-4">
              {featured?.tags?.map((tag, i) => (
                <span 
                  key={i}
                  className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium"
                  style={{ backgroundColor: tag.bgColor, color: tag.textColor }}
                >
                  {tag.icon && <tag.icon className="w-3 h-3 mr-1" />}
                  {tag.label}
                </span>
              ))}
            </div>
            
            {/* Title */}
            <h2 className="text-2xl font-bold text-gray-900 mb-4">{featured?.title}</h2>
            
            {/* Description */}
            <p className="text-gray-600 mb-6 leading-relaxed">
              {featured?.description}
            </p>
            
            {/* Stats */}
            <div className="flex items-center gap-8 py-6 border-t border-gray-100">
              <div>
                <p className="text-3xl font-bold text-violet-600">{featured?.stats?.value}</p>
                <p className="text-sm text-gray-500">{featured?.stats?.label}</p>
              </div>
              <div className="h-12 w-px bg-gray-200" />
              <div className="flex items-center gap-4">
                {featured?.assignees?.map((a, i) => (
                  <img 
                    key={i}
                    src={a.avatar}
                    alt={a.name}
                    className="w-10 h-10 rounded-full border-2 border-white shadow-sm"
                    title={a.name}
                  />
                ))}
              </div>
            </div>
            
            {/* Actions */}
            <div className="flex items-center gap-4">
              <button className="flex-1 px-6 py-3 bg-violet-600 text-white rounded-xl font-medium hover:bg-violet-700 transition-colors">
                View Details
              </button>
              <button className="w-12 h-12 border border-gray-200 rounded-xl flex items-center justify-center hover:bg-gray-50 transition-colors">
                <Bookmark className="w-5 h-5 text-gray-600" />
              </button>
              <button className="w-12 h-12 border border-gray-200 rounded-xl flex items-center justify-center hover:bg-gray-50 transition-colors">
                <Share2 className="w-5 h-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Side Cards */}
      <div className="space-y-4">
        {data.filter(d => d.id !== selected).slice(0, 4).map(item => (
          <div 
            key={item.id}
            onClick={() => setSelected(item.id)}
            className={`bg-white rounded-2xl border overflow-hidden cursor-pointer transition-all ${
              selected === item.id ? 'border-violet-500 shadow-lg' : 'border-gray-100 hover:border-gray-200 hover:shadow'
            }`}
          >
            <div className="flex gap-4 p-4">
              {item.thumbnail && (
                <img src={item.thumbnail} className="w-20 h-20 rounded-xl object-cover" />
              )}
              <div className="flex-1">
                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                  item.status === 'active' ? 'bg-green-50 text-green-700' : 'bg-gray-50 text-gray-700'
                }`}>
                  {item.status}
                </span>
                <h3 className="font-semibold text-gray-900 mt-2 line-clamp-2">{item.title}</h3>
                <p className="text-sm text-gray-500 mt-1">{formatDate(item.createdAt)}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## 5. COMPACT CARD VIEW

```tsx
// ✅ COMPACT CARD (SMALL)
const CompactCardView = ({ data }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-3">
      {data.map(item => (
        <div 
          key={item.id}
          className="group bg-white rounded-xl border border-gray-100 overflow-hidden hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer"
        >
          {/* Thumbnail */}
          <div className="aspect-square relative overflow-hidden">
            <img 
              src={item.thumbnail || item.cover} 
              alt={item.title}
              className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
            />
            
            {/* Status overlay */}
            <div className="absolute top-2 right-2">
              <span className={`w-2.5 h-2.5 rounded-full ${
                item.status === 'active' ? 'bg-green-500' : 'bg-gray-400'
              }`} />
            </div>
            
            {/* Hover overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2">
              <button className="w-full py-1.5 bg-white rounded-lg text-xs font-medium text-gray-900">
                View
              </button>
            </div>
          </div>
          
          {/* Info */}
          <div className="p-2">
            <p className="text-xs font-medium text-gray-900 truncate">{item.title}</p>
            <p className="text-xs text-gray-500 truncate">{item.category}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 6. LIST CARD VIEW

```tsx
// ✅ LIST CARD VIEW
const ListCardView = ({ data, onCardClick }) => {
  return (
    <div className="space-y-3">
      {data.map(item => (
        <div 
          key={item.id}
          onClick={() => onCardClick?.(item)}
          className="bg-white rounded-2xl border border-gray-100 p-4 hover:shadow-md hover:border-gray-200 transition-all cursor-pointer"
        >
          <div className="flex items-center gap-4">
            {/* Checkbox */}
            <button className="w-5 h-5 rounded-lg border-2 border-gray-200 flex items-center justify-center hover:border-violet-500 transition-colors">
              {/* unchecked */}
            </button>
            
            {/* Thumbnail */}
            {item.thumbnail && (
              <img 
                src={item.thumbnail}
                alt=""
                className="w-16 h-16 rounded-xl object-cover"
              />
            )}
            
            {/* Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {item.tags?.slice(0, 2).map((tag, i) => (
                  <span 
                    key={i}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                    style={{ backgroundColor: tag.bgColor, color: tag.textColor }}
                  >
                    {tag.label}
                  </span>
                ))}
              </div>
              <h3 className="font-medium text-gray-900 truncate">{item.title}</h3>
              <p className="text-sm text-gray-500 truncate">{item.description}</p>
            </div>
            
            {/* Status */}
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              item.status === 'active' ? 'bg-green-50 text-green-700' :
              item.status === 'pending' ? 'bg-yellow-50 text-yellow-700' :
              'bg-gray-50 text-gray-700'
            }`}>
              {item.status}
            </span>
            
            {/* Date */}
            <div className="text-right">
              <p className="text-sm text-gray-900">{formatDate(item.date)}</p>
              <p className="text-xs text-gray-500">Created</p>
            </div>
            
            {/* Assignees */}
            {item.assignees?.length > 0 && (
              <div className="flex -space-x-2">
                {item.assignees.slice(0, 3).map((a, i) => (
                  <img 
                    key={i}
                    src={a.avatar}
                    className="w-8 h-8 rounded-full border-2 border-white"
                  />
                ))}
              </div>
            )}
            
            {/* Actions */}
            <div className="flex items-center gap-1">
              <button className="p-2 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600">
                <Eye className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-lg hover:bg-gray-100 text-gray-400 hover:text-gray-600">
                <Pencil className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-lg hover:bg-red-50 text-gray-400 hover:text-red-600">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 7. STATS CARD VIEW

```tsx
// ✅ STATS CARD VIEW
const StatsCardView = ({ data }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {data.map(item => (
        <div 
          key={item.id}
          className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-lg hover:-translate-y-1 transition-all cursor-pointer"
        >
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
              item.color === 'violet' ? 'bg-violet-100 text-violet-600' :
              item.color === 'blue' ? 'bg-blue-100 text-blue-600' :
              item.color === 'green' ? 'bg-green-100 text-green-600' :
              'bg-orange-100 text-orange-600'
            }`}>
              {item.icon === 'users' && <Users className="w-6 h-6" />}
              {item.icon === 'dollar' && <DollarSign className="w-6 h-6" />}
              {item.icon === 'chart' && <TrendingUp className="w-6 h-6" />}
              {item.icon === 'package' && <Package className="w-6 h-6" />}
            </div>
            
            {item.trend && (
              <span className={`flex items-center gap-1 text-sm font-medium ${
                item.trend > 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {item.trend > 0 ? <ArrowUp className="w-4 h-4" /> : <ArrowDown className="w-4 h-4" />}
                {Math.abs(item.trend)}%
              </span>
            )}
          </div>
          
          {/* Value */}
          <h3 className="text-3xl font-bold text-gray-900 mb-1">
            {formatNumber(item.value)}
          </h3>
          <p className="text-sm text-gray-500">{item.label}</p>
          
          {/* Progress */}
          {item.progress !== undefined && (
            <div className="mt-4">
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div 
                  className={`h-full rounded-full ${
                    item.color === 'violet' ? 'bg-violet-500' :
                    item.color === 'blue' ? 'bg-blue-500' :
                    item.color === 'green' ? 'bg-green-500' :
                    'bg-orange-500'
                  }`}
                  style={{ width: `${item.progress}%` }}
                />
              </div>
            </div>
          )}
          
          {/* Footer */}
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
            <span className="text-xs text-gray-500">{item.period}</span>
            {item.avatar && (
              <img src={item.avatar} className="w-6 h-6 rounded-full" />
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 8. PRODUCT CARD VIEW

```tsx
// ✅ PRODUCT CARD
const ProductCardView = ({ data }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {data.map(product => (
        <div 
          key={product.id}
          className="group bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl hover:-translate-y-2 transition-all duration-300"
        >
          {/* Image */}
          <div className="aspect-square relative overflow-hidden bg-gray-100">
            <img 
              src={product.image}
              alt={product.name}
              className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            
            {/* Badges */}
            <div className="absolute top-3 left-3 flex flex-col gap-2">
              {product.isNew && (
                <span className="px-3 py-1 bg-violet-600 text-white text-xs font-bold rounded-full">
                  NEW
                </span>
              )}
              {product.discount && (
                <span className="px-3 py-1 bg-red-500 text-white text-xs font-bold rounded-full">
                  -{product.discount}%
                </span>
              )}
            </div>
            
            {/* Quick actions */}
            <div className="absolute top-3 right-3 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button className="w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-100 transition-colors">
                <Heart className="w-5 h-5 text-gray-600" />
              </button>
              <button className="w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-100 transition-colors">
                <Eye className="w-5 h-5 text-gray-600" />
              </button>
            </div>
            
            {/* Add to cart */}
            <button className="absolute bottom-0 left-0 right-0 py-4 bg-violet-600 text-white font-medium translate-y-full group-hover:translate-y-0 transition-transform duration-300">
              Add to Cart
            </button>
          </div>
          
          {/* Info */}
          <div className="p-5">
            {/* Category */}
            <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">
              {product.category}
            </p>
            
            {/* Name */}
            <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
              {product.name}
            </h3>
            
            {/* Rating */}
            <div className="flex items-center gap-2 mb-3">
              <div className="flex items-center">
                {[1, 2, 3, 4, 5].map(i => (
                  <Star 
                    key={i}
                    className={`w-4 h-4 ${i <= product.rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'}`}
                  />
                ))}
              </div>
              <span className="text-xs text-gray-500">({product.reviews})</span>
            </div>
            
            {/* Price */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold text-gray-900">
                  ${product.price.toFixed(2)}
                </span>
                {product.originalPrice && (
                  <span className="text-sm text-gray-400 line-through">
                    ${product.originalPrice.toFixed(2)}
                  </span>
                )}
              </div>
              
              {/* Stock */}
              <span className={`text-xs font-medium ${
                product.stock > 10 ? 'text-green-600' :
                product.stock > 0 ? 'text-orange-600' :
                'text-red-600'
              }`}>
                {product.stock > 10 ? 'In Stock' :
                 product.stock > 0 ? `Only ${product.stock} left` :
                 'Out of Stock'}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 9. USER CARD VIEW

```tsx
// ✅ USER CARD
const UserCardView = ({ data }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {data.map(user => (
        <div 
          key={user.id}
          className="bg-white rounded-2xl border border-gray-100 p-6 hover:shadow-lg transition-all cursor-pointer text-center group"
        >
          {/* Avatar */}
          <div className="relative inline-block mb-4">
            <img 
              src={user.avatar}
              alt={user.name}
              className="w-20 h-20 rounded-full object-cover ring-4 ring-gray-100 group-hover:ring-violet-100 transition-all"
            />
            
            {/* Status */}
            <span className={`absolute bottom-1 right-1 w-4 h-4 rounded-full border-2 border-white ${
              user.status === 'online' ? 'bg-green-500' :
              user.status === 'away' ? 'bg-yellow-500' :
              'bg-gray-300'
            }`} />
          </div>
          
          {/* Name */}
          <h3 className="font-semibold text-gray-900 mb-1">{user.name}</h3>
          <p className="text-sm text-gray-500 mb-3">{user.email}</p>
          
          {/* Role badge */}
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-gray-700 mb-4">
            <Shield className="w-3 h-3" />
            {user.role}
          </span>
          
          {/* Stats */}
          <div className="grid grid-cols-3 gap-2 py-4 border-t border-gray-100">
            <div>
              <p className="text-lg font-bold text-gray-900">{user.projects}</p>
              <p className="text-xs text-gray-500">Projects</p>
            </div>
            <div>
              <p className="text-lg font-bold text-gray-900">{user.tasks}</p>
              <p className="text-xs text-gray-500">Tasks</p>
            </div>
            <div>
              <p className="text-lg font-bold text-gray-900">{user.followers}k</p>
              <p className="text-xs text-gray-500">Followers</p>
            </div>
          </div>
          
          {/* Actions */}
          <div className="flex items-center justify-center gap-2">
            <button className="flex-1 px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors">
              Follow
            </button>
            <button className="w-10 h-10 border border-gray-200 rounded-lg flex items-center justify-center hover:bg-gray-50 transition-colors">
              <Mail className="w-4 h-4 text-gray-600" />
            </button>
            <button className="w-10 h-10 border border-gray-200 rounded-lg flex items-center justify-center hover:bg-gray-50 transition-colors">
              <MoreHorizontal className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 10. TOOLBAR & PAGINATION

```tsx
// ✅ CARD VIEW TOOLBAR
const CardToolbar = ({ 
  total, 
  selected,
  searchTerm,
  onSearch,
  filters,
  onFilterChange,
  onExport,
  onImport
}) => {
  const [showFilters, setShowFilters] = useState(false)
  
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        {/* Left */}
        <div className="flex items-center gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Items</h2>
            <p className="text-sm text-gray-500">
              {selected > 0 ? `${selected} selected` : `${total} total`}
            </p>
          </div>
        </div>
        
        {/* Right */}
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => onSearch(e.target.value)}
              className="pl-9 pr-4 py-2 w-64 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
            />
            {searchTerm && (
              <button 
                onClick={() => onSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          
          {/* Filters */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-2 border rounded-xl text-sm font-medium transition-colors ${
              showFilters 
                ? 'bg-violet-50 border-violet-200 text-violet-700' 
                : 'border-gray-200 text-gray-700 hover:bg-gray-50'
            }`}
          >
            <SlidersHorizontal className="w-4 h-4" />
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
              <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50">
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
                <Download className="w-4 h-4 mr-2" />
                Export Template
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          
          {/* Export */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-xl text-sm font-medium hover:bg-gray-800">
                <Download className="w-4 h-4" />
                Export
                <ChevronDown className="w-4 h-4" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem onClick={() => onExport('xlsx')}>
                <FileSpreadsheet className="w-4 h-4 mr-2" />
                Excel (.xlsx)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onExport('csv')}>
                <FileText className="w-4 h-4 mr-2" />
                CSV (.csv)
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => onExport('pdf')}>
                <FileText className="w-4 h-4 mr-2" />
                PDF (.pdf)
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          
          {/* Add New */}
          <button className="flex items-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-xl text-sm font-medium hover:bg-violet-700 transition-colors">
            <Plus className="w-4 h-4" />
            Add New
          </button>
        </div>
      </div>
      
      {/* Filter Row */}
      {showFilters && (
        <FilterRow filters={filters} onFilterChange={onFilterChange} />
      )}
    </div>
  )
}

// ✅ FILTER ROW
const FilterRow = ({ filters, onFilterChange }) => {
  return (
    <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-2xl">
      {/* Created Date */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Created:</label>
        <Select
          value={filters.createdRange}
          onChange={(v) => onFilterChange({ ...filters, createdRange: v })}
        >
          <SelectTrigger className="w-36">
            <SelectValue placeholder="All time" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All time</SelectItem>
            <SelectItem value="today">Today</SelectItem>
            <SelectItem value="7days">Last 7 days</SelectItem>
            <SelectItem value="30days">Last 30 days</SelectItem>
            <SelectItem value="90days">Last 90 days</SelectItem>
            <SelectItem value="thisYear">This year</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Status */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Status:</label>
        <Select
          value={filters.status}
          onChange={(v) => onFilterChange({ ...filters, status: v })}
        >
          <SelectTrigger className="w-32">
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All</SelectItem>
            <SelectItem value="active">Active</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="inactive">Inactive</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Category */}
      <div className="flex items-center gap-2">
        <label className="text-xs font-medium text-gray-600">Category:</label>
        <Select
          value={filters.category}
          onChange={(v) => onFilterChange({ ...filters, category: v })}
        >
          <SelectTrigger className="w-36">
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All</SelectItem>
            <SelectItem value="technology">Technology</SelectItem>
            <SelectItem value="marketing">Marketing</SelectItem>
            <SelectItem value="design">Design</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      {/* Clear */}
      <button 
        onClick={() => onFilterChange({})}
        className="ml-auto text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
      >
        <X className="w-3 h-3" />
        Clear all
      </button>
    </div>
  )
}

// ✅ BULK ACTIONS BAR
const BulkActionsBar = ({ selected, onClear, onDelete, onExport }) => {
  return (
    <div className="flex items-center gap-4 p-4 bg-violet-50 rounded-2xl">
      <span className="text-sm font-medium text-violet-700">{selected} selected</span>
      <div className="h-5 w-px bg-violet-200" />
      <button onClick={onExport} className="text-sm text-violet-700 hover:text-violet-800">Export</button>
      <button onClick={onDelete} className="text-sm text-red-600 hover:text-red-700 flex items-center gap-1">
        <Trash2 className="w-4 h-4" />
        Delete
      </button>
      <button onClick={onClear} className="ml-auto text-sm text-gray-500 hover:text-gray-700">
        Cancel
      </button>
    </div>
  )
}

// ✅ PAGINATION
const CardPagination = ({ currentPage, totalPages, onPageChange, total, pageSize }) => {
  return (
    <div className="flex items-center justify-between pt-6 border-t border-gray-100">
      <p className="text-sm text-gray-500">
        Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, total)} of {total} results
      </p>
      
      <div className="flex items-center gap-2">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="w-10 h-10 rounded-xl border border-gray-200 flex items-center justify-center disabled:opacity-50 hover:bg-gray-50"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        
        {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
          let page
          if (totalPages <= 5) page = i + 1
          else if (currentPage <= 3) page = i + 1
          else if (currentPage >= totalPages - 2) page = totalPages - 4 + i
          else page = currentPage - 2 + i
          
          return (
            <button
              key={page}
              onClick={() => onPageChange(page)}
              className={`w-10 h-10 rounded-xl text-sm font-medium ${
                currentPage === page
                  ? 'bg-violet-600 text-white'
                  : 'border border-gray-200 hover:bg-gray-50'
              }`}
            >
              {page}
            </button>
          )
        })}
        
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="w-10 h-10 rounded-xl border border-gray-200 flex items-center justify-center disabled:opacity-50 hover:bg-gray-50"
        >
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}
```

## 11. VIEW SWITCHER

```tsx
// ✅ VIEW SWITCHER (TABLE / GRID / LIST)
const ViewSwitcher = ({ view, onChange }) => {
  return (
    <div className="inline-flex bg-gray-100 rounded-xl p-1">
      <button
        onClick={() => onChange('table')}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
          view === 'table' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        <LayoutGrid className="w-4 h-4" />
      </button>
      <button
        onClick={() => onChange('grid')}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
          view === 'grid' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        <Grid3x3 className="w-4 h-4" />
      </button>
      <button
        onClick={() => onChange('list')}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
          view === 'list' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        <List className="w-4 h-4" />
      </button>
      <button
        onClick={() => onChange('masonry')}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
          view === 'masonry' ? 'bg-white shadow-sm text-gray-900' : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        <Columns3 className="w-4 h-4" />
      </button>
    </div>
  )
}
```

## 12. EMPTY STATE

```tsx
// ✅ EMPTY STATE
const EmptyState = ({ title, description, icon: Icon }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-6">
        <Icon className="w-10 h-10 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-500 mb-6 max-w-sm text-center">{description}</p>
      <button className="px-4 py-2 bg-violet-600 text-white rounded-lg text-sm font-medium hover:bg-violet-700">
        Create your first item
      </button>
    </div>
  )
}
```

## 13. ICONS

```tsx
import {
  // Navigation
  ChevronLeft, ChevronRight, ChevronDown, ChevronUp,
  
  // Actions
  Plus, Pencil, Trash2, Copy, MoreHorizontal, Eye, Edit,
  Search, Filter, SlidersHorizontal, Download, Upload,
  
  // Cards
  Grid3x3, LayoutGrid, List, Columns3, LayoutList,
  
  // Content
  Heart, MessageCircle, Star, Bookmark, Share2, Eye,
  Mail, Phone, MapPin, Calendar, Clock,
  
  // Status
  Check, CheckCircle, X, XCircle, AlertCircle, AlertTriangle,
  
  // Finance
  DollarSign, TrendingUp, TrendingDown, ArrowUp, ArrowDown,
  
  // Users
  Users, User, Shield, UserPlus,
  
  // Files
  FileText, FileSpreadsheet, File, Folder, Image,
  
  // Misc
  Package, Tag, Label, Link, ExternalLink, X as Close,
} from 'lucide-react'
```

## Card View Checklist

- [ ] Multiple card styles (grid, list, compact, featured, masonry)
- [ ] Search input with clear button
- [ ] Filter options (status, category, date)
- [ ] Bulk selection with checkbox
- [ ] Bulk actions bar
- [ ] Pagination
- [ ] Export buttons (Excel, CSV, PDF)
- [ ] Import modal with preview
- [ ] Template export
- [ ] Created date filter
- [ ] Card hover effects
- [ ] Card actions (edit, delete)
- [ ] Empty state
- [ ] Loading skeleton
- [ ] View switcher
- [ ] Responsive grid
- [ ] Image lazy loading
- [ ] Infinite scroll option
