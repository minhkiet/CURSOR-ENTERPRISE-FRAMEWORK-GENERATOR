# Task Views & Views Layout Library

Progressive layouts for task management views across all devices. Reference cho thiết kế task apps.

## 1. CALENDAR VIEW (3 styles)

### 1.1 Calendar Bar View (Default)

```tsx
// ✅ TIMETABLE CALENDAR
const CalendarBarView = ({ events, onEventClick }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
        <div className="flex items-center gap-4">
          <h2 className="text-xl font-bold text-gray-900">Plan Schedule</h2>
          <span className="text-sm text-gray-500">Schedule for current month</span>
        </div>
        <button className="w-10 h-10 rounded-full bg-violet-500 text-white flex items-center justify-center hover:bg-violet-600 transition-colors">
          <Plus className="w-5 h-5" />
        </button>
      </div>
      
      {/* Toolbar */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-gray-100">
        <DatePicker value="October 2026" />
        <div className="flex items-center gap-3">
          <AvatarGroup members={members} />
          <button className="w-8 h-8 rounded-full border-2 border-dashed border-gray-300 flex items-center justify-center hover:border-gray-400">
            <Plus className="w-4 h-4 text-gray-400" />
          </button>
          <SortSelector />
          <ViewToggle />
        </div>
      </div>
      
      {/* Calendar Grid */}
      <div className="overflow-x-auto">
        <div className="min-w-[800px]">
          {/* Days header */}
          <div className="grid grid-cols-[80px_repeat(7,1fr)] border-b border-gray-100">
            <div></div>
            {['Mon 30', 'Tue 31', 'Wed 1', 'Thu 2', 'Fri 10', 'Sat 10'].map((day, i) => (
              <div key={i} className="px-4 py-3 text-center text-sm font-medium text-gray-700">
                {day}
              </div>
            ))}
          </div>
          
          {/* Time rows */}
          {times.map(time => (
            <div key={time} className="grid grid-cols-[80px_repeat(7,1fr)] border-b border-gray-50 min-h-[60px]">
              <div className="px-4 py-2 text-xs text-gray-500">{time}</div>
              {days.map(day => (
                <div key={day} className="border-l border-gray-50 relative">
                  {/* Event bars */}
                  {events.filter(e => e.day === day && e.time === time).map(event => (
                    <EventBar key={event.id} event={event} />
                  ))}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// Event Bar
const EventBar = ({ event }) => (
  <div className={`absolute left-2 right-6 ${event.color} rounded-xl p-3 cursor-pointer hover:shadow-lg transition-shadow`}>
    <div className="flex items-center gap-3">
      <img src={event.user.avatar} className="w-8 h-8 rounded-full" />
      <div className="flex-1">
        <p className="text-xs text-gray-700">{event.user.name}</p>
        <p className="text-sm font-semibold text-gray-900">{event.title}</p>
      </div>
      <div className="text-right">
        <p className="text-xs text-gray-600">Tasks</p>
        <p className="text-sm font-bold">{event.tasks}</p>
      </div>
      <div className="text-right">
        <p className="text-xs text-gray-600">Hours</p>
        <p className="text-sm font-bold">{event.hours}</p>
      </div>
    </div>
  </div>
)
```

### 1.2 Calendar Month View

```tsx
// ✅ MONTH GRID VIEW
const CalendarMonthView = ({ events }) => {
  return (
    <div className="grid grid-cols-7 border-l border-t border-gray-200">
      {/* Day headers */}
      {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
        <div key={day} className="border-r border-b border-gray-200 p-3 bg-gray-50 text-center text-sm font-medium text-gray-700">
          {day}
        </div>
      ))}
      
      {/* Days */}
      {days.map((day, i) => (
        <div key={i} className="min-h-[120px] border-r border-b border-gray-200 p-2 hover:bg-gray-50 cursor-pointer">
          <div className="flex items-center justify-between mb-2">
            <span className={`text-sm ${day.isToday ? 'font-bold text-violet-600' : 'text-gray-700'}`}>
              {day.number}
            </span>
            {day.hasEvents && (
              <span className="w-2 h-2 rounded-full bg-violet-500" />
            )}
          </div>
          
          {/* Events */}
          <div className="space-y-1">
            {day.events.slice(0, 3).map(event => (
              <div key={event.id} className={`text-xs px-2 py-1 rounded ${event.color} truncate`}>
                {event.title}
              </div>
            ))}
            {day.events.length > 3 && (
              <p className="text-xs text-gray-500">+{day.events.length - 3} more</p>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}
```

### 1.3 Calendar Week View

```tsx
// ✅ DAY-BY-DAY WEEK VIEW
const CalendarWeekView = ({ events, week }) => {
  return (
    <div className="space-y-4">
      {/* Week header */}
      <div className="flex items-center gap-2">
        {week.map(day => (
          <div key={day.date} className="flex-1 text-center">
            <p className="text-xs text-gray-500">{day.dayName}</p>
            <p className={`text-2xl font-bold ${day.isToday ? 'text-violet-600' : 'text-gray-900'}`}>
              {day.dayNumber}
            </p>
          </div>
        ))}
      </div>
      
      {/* Day columns */}
      <div className="grid grid-cols-7 gap-2">
        {week.map(day => (
          <div key={day.date} className="space-y-2">
            {events.filter(e => e.date === day.date).map(event => (
              <div key={event.id} className={`p-3 rounded-xl ${event.color} text-white cursor-pointer hover:shadow-lg transition-all`}>
                <p className="text-xs opacity-80">{event.time}</p>
                <p className="text-sm font-semibold mt-1">{event.title}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
```

### 1.4 Calendar List View

```tsx
// ✅ AGENDA LIST VIEW
const CalendarListView = ({ events, groupedByDate }) => {
  return (
    <div className="space-y-6">
      {groupedByDate.map(group => (
        <div key={group.date}>
          <h3 className="text-sm font-medium text-gray-500 mb-3">
            {group.dateLabel} <span className="text-violet-600">({group.events.length})</span>
          </h3>
          
          <div className="space-y-2">
            {group.events.map(event => (
              <div key={event.id} className="flex items-center gap-4 p-4 bg-white rounded-xl border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all cursor-pointer">
                <div className="text-center min-w-[60px]">
                  <p className="text-2xl font-bold text-gray-900">{event.time}</p>
                  <p className="text-xs text-gray-500">{event.period}</p>
                </div>
                <div className={`w-1 h-12 rounded-full ${event.color}`} />
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">{event.title}</p>
                  <p className="text-sm text-gray-500">{event.subtitle}</p>
                </div>
                <AvatarGroup members={event.members} />
                <MoreButton />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 2. KANBAN BOARD VIEW

### 2.1 Standard Kanban

```tsx
// ✅ KANBAN BOARD
const KanbanView = ({ columns, onCardMove }) => {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4">
      {columns.map(column => (
        <div key={column.id} className="flex-shrink-0 w-80">
          {/* Column Header */}
          <div className="flex items-center justify-between mb-4 px-2">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${column.color}`} />
              <h3 className="font-semibold text-gray-900">{column.title}</h3>
              <span className="text-sm text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">
                {column.tasks.length}
              </span>
            </div>
            <button className="text-gray-400 hover:text-gray-600">
              <MoreHorizontal className="w-5 h-5" />
            </button>
          </div>
          
          {/* Cards */}
          <div className="space-y-3">
            {column.tasks.map(task => (
              <TaskCard key={task.id} task={task} />
            ))}
            <button className="w-full p-3 border-2 border-dashed border-gray-200 rounded-xl text-gray-500 hover:border-gray-300 hover:text-gray-700 transition-colors">
              <Plus className="w-4 h-4 inline mr-1" />
              Add task
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

const TaskCard = ({ task }) => (
  <div className="bg-white rounded-xl p-4 border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all cursor-pointer">
    {/* Tags */}
    {task.tags && (
      <div className="flex gap-2 mb-3">
        {task.tags.map(tag => (
          <span key={tag} className={`text-xs px-2 py-1 rounded-full ${tag.color}`}>
            {tag.label}
          </span>
        ))}
      </div>
    )}
    
    {/* Title */}
    <h4 className="font-medium text-gray-900 mb-2">{task.title}</h4>
    
    {/* Description */}
    {task.description && (
      <p className="text-sm text-gray-500 mb-3 line-clamp-2">{task.description}</p>
    )}
    
    {/* Progress */}
    {task.progress !== undefined && (
      <div className="mb-3">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Progress</span>
          <span>{task.progress}%</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-violet-500 transition-all" style={{ width: `${task.progress}%` }} />
        </div>
      </div>
    )}
    
    {/* Footer */}
    <div className="flex items-center justify-between mt-4">
      <div className="flex items-center gap-2">
        <AvatarGroup members={task.assignees} max={3} />
        {task.comments && (
          <span className="flex items-center gap-1 text-xs text-gray-500">
            <MessageCircle className="w-3.5 h-3.5" />
            {task.comments}
          </span>
        )}
        {task.attachments && (
          <span className="flex items-center gap-1 text-xs text-gray-500">
            <Paperclip className="w-3.5 h-3.5" />
            {task.attachments}
          </span>
        )}
      </div>
      <span className="text-xs text-gray-500">{task.dueDate}</span>
    </div>
  </div>
)
```

### 2.2 Kanban with Subtasks

```tsx
// ✅ KANBAN WITH SUBTASKS
const KanbanWithSubtasks = ({ task }) => (
  <div className="bg-white rounded-xl p-4 border border-gray-200">
    <div className="flex items-center justify-between mb-3">
      <span className="text-xs text-gray-500">{task.id}</span>
      <span className={`text-xs px-2 py-1 rounded-full ${task.priorityColor}`}>
        {task.priority}
      </span>
    </div>
    
    <h4 className="font-medium text-gray-900 mb-3">{task.title}</h4>
    
    {/* Subtasks list */}
    <div className="space-y-2 mb-3">
      {task.subtasks.map(sub => (
        <div key={sub.id} className="flex items-center gap-2 text-sm">
          <Checkbox checked={sub.completed} />
          <span className={sub.completed ? 'line-through text-gray-400' : 'text-gray-700'}>
            {sub.title}
          </span>
        </div>
      ))}
    </div>
    
    {/* Checklists */}
    <div className="text-xs text-gray-500 mb-3">
      {task.completedSubtasks}/{task.subtasks.length} completed
    </div>
  </div>
)
```

## 3. LIST VIEW

### 3.1 Simple List

```tsx
// ✅ SIMPLE LIST VIEW
const ListView = ({ tasks }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="grid grid-cols-[40px_1fr_120px_120px_60px_60px] gap-4 px-4 py-3 bg-gray-50 border-b border-gray-200 text-xs font-medium text-gray-500 uppercase">
        <div></div>
        <div>Task</div>
        <div>Assignee</div>
        <div>Due Date</div>
        <div>Priority</div>
        <div></div>
      </div>
      
      {/* Rows */}
      {tasks.map(task => (
        <div key={task.id} className="grid grid-cols-[40px_1fr_120px_120px_60px_60px] gap-4 px-4 py-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer">
          <Checkbox checked={task.completed} />
          <div>
            <p className="font-medium text-gray-900">{task.title}</p>
            <p className="text-sm text-gray-500">{task.project}</p>
          </div>
          <Avatar user={task.assignee} />
          <div className="text-sm text-gray-700">{task.dueDate}</div>
          <PriorityBadge priority={task.priority} />
          <MoreButton />
        </div>
      ))}
    </div>
  )
}
```

### 3.2 Grouped List

```tsx
// ✅ GROUPED LIST VIEW
const GroupedListView = ({ tasks, groupBy = 'status' }) => {
  const grouped = groupTasksBy(tasks, groupBy)
  
  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([group, items]) => (
        <div key={group}>
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold text-gray-900">
              {group} <span className="text-gray-400 font-normal">({items.length})</span>
            </h3>
            <button className="text-sm text-gray-500 hover:text-gray-700">
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>
          
          <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            {items.map((task, i) => (
              <ListRow key={task.id} task={task} isLast={i === items.length - 1} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 4. GRID/CARD VIEW

### 4.1 Card Grid

```tsx
// ✅ CARD GRID VIEW
const CardGridView = ({ tasks }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {tasks.map(task => (
        <div key={task.id} className="bg-white rounded-2xl border border-gray-200 p-5 hover:shadow-lg transition-all cursor-pointer">
          {/* Header */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex gap-2">
              {task.tags?.map(tag => (
                <span key={tag} className={`text-xs px-2 py-1 rounded-full ${tag.color}`}>
                  {tag.label}
                </span>
              ))}
            </div>
            <MoreButton />
          </div>
          
          {/* Cover image */}
          {task.cover && (
            <div className="aspect-video bg-gray-100 rounded-xl mb-3 overflow-hidden">
              <img src={task.cover} className="w-full h-full object-cover" />
            </div>
          )}
          
          {/* Title */}
          <h4 className="font-semibold text-gray-900 mb-2">{task.title}</h4>
          
          {/* Description */}
          <p className="text-sm text-gray-500 line-clamp-2 mb-4">{task.description}</p>
          
          {/* Progress */}
          {task.progress !== undefined && (
            <div className="mb-4">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Progress</span>
                <span>{task.progress}%</span>
              </div>
              <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-violet-500 rounded-full" style={{ width: `${task.progress}%` }} />
              </div>
            </div>
          )}
          
          {/* Footer */}
          <div className="flex items-center justify-between pt-4 border-t border-gray-100">
            <AvatarGroup members={task.assignees} max={3} />
            <div className="flex items-center gap-3 text-xs text-gray-500">
              {task.attachments && <span className="flex items-center gap-1"><Paperclip className="w-3.5 h-3.5" />{task.attachments}</span>}
              {task.comments && <span className="flex items-center gap-1"><MessageCircle className="w-3.5 h-3.5" />{task.comments}</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 5. TABLE VIEW

### 5.1 Spreadsheet Table

```tsx
// ✅ SPREADSHEET TABLE VIEW
const TableView = ({ tasks, columns }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="w-10 px-4 py-3"></th>
              {columns.map(col => (
                <th key={col.key} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  {col.label}
                </th>
              ))}
              <th className="w-10 px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            {tasks.map(task => (
              <tr key={task.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="px-4 py-3">
                  <Checkbox checked={task.completed} />
                </td>
                {columns.map(col => (
                  <td key={col.key} className="px-4 py-3">
                    {col.render(task)}
                  </td>
                ))}
                <td className="px-4 py-3">
                  <MoreButton />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
```

## 6. GANTT/TIMELINE VIEW

### 6.1 Gantt Chart

```tsx
// ✅ GANTT TIMELINE VIEW
const GanttView = ({ tasks, startDate, endDate }) => {
  const days = getDaysBetween(startDate, endDate)
  
  return (
    <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      {/* Header with dates */}
      <div className="grid grid-cols-[200px_repeat(30,1fr)] border-b border-gray-200">
        <div className="p-3 bg-gray-50 font-medium text-gray-700">Task</div>
        {days.map((day, i) => (
          <div key={i} className="p-3 bg-gray-50 text-center text-xs text-gray-500 border-l border-gray-100">
            {day.day}
          </div>
        ))}
      </div>
      
      {/* Task rows */}
      {tasks.map(task => (
        <div key={task.id} className="grid grid-cols-[200px_repeat(30,1fr)] border-b border-gray-100">
          <div className="p-3 flex items-center gap-2">
            <img src={task.assignee.avatar} className="w-6 h-6 rounded-full" />
            <span className="text-sm text-gray-900">{task.title}</span>
          </div>
          
          <div className="col-span-30 relative h-12 border-l border-gray-100">
            {/* Today line */}
            <div className="absolute top-0 bottom-0 w-0.5 bg-red-500" style={{ left: `${todayPercent}%` }} />
            
            {/* Task bar */}
            <div
              className={`absolute top-3 h-6 ${task.color} rounded-full cursor-pointer hover:opacity-80 transition-opacity`}
              style={{
                left: `${task.startPercent}%`,
                width: `${task.durationPercent}%`,
              }}
            >
              <div className="flex items-center h-full px-3 text-xs text-white font-medium">
                {task.title}
              </div>
            </div>
            
            {/* Progress */}
            <div
              className="absolute top-3 h-6 bg-gray-200 rounded-full"
              style={{
                left: `${task.startPercent + task.durationPercent}%`,
                width: '0',
              }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 7. CALENDAR/MAP VIEW

### 7.1 Heatmap View

```tsx
// ✅ HEATMAP VIEW
const HeatmapView = ({ data }) => {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-[repeat(53,1fr)] gap-1">
        {data.map((week, weekIdx) => (
          <div key={weekIdx} className="grid grid-rows-7 gap-1">
            {week.map((day, dayIdx) => (
              <div
                key={dayIdx}
                className={`w-3 h-3 rounded-sm ${getIntensityColor(day.intensity)} cursor-pointer hover:ring-2 hover:ring-gray-300`}
                title={`${day.count} tasks on ${day.date}`}
              />
            ))}
          </div>
        ))}
      </div>
      
      {/* Legend */}
      <div className="flex items-center gap-2 text-xs text-gray-500">
        <span>Less</span>
        {[0, 1, 2, 3, 4].map(i => (
          <div key={i} className={`w-3 h-3 rounded-sm ${getIntensityColor(i)}`} />
        ))}
        <span>More</span>
      </div>
    </div>
  )
}
```

## 8. MOBILE VIEW

### 8.1 Mobile List

```tsx
// ✅ MOBILE LIST VIEW
const MobileListView = ({ tasks }) => {
  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <div key={task.id} className="bg-white rounded-2xl p-4 border border-gray-200">
          <div className="flex items-start gap-3">
            <Checkbox checked={task.completed} />
            <div className="flex-1">
              <h4 className="font-medium text-gray-900 mb-1">{task.title}</h4>
              <div className="flex items-center gap-2 mb-3">
                {task.tags?.map(tag => (
                  <span key={tag} className={`text-xs px-2 py-0.5 rounded-full ${tag.color}`}>
                    {tag.label}
                  </span>
                ))}
              </div>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <Avatar user={task.assignee} size="sm" />
                <span>{task.dueDate}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

### 8.2 Mobile Cards

```tsx
// ✅ MOBILE CARD VIEW
const MobileCardView = ({ tasks }) => {
  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <div key={task.id} className="bg-white rounded-2xl overflow-hidden border border-gray-200">
          {/* Cover */}
          {task.cover && (
            <div className="aspect-[2/1] bg-gray-100">
              <img src={task.cover} className="w-full h-full object-cover" />
            </div>
          )}
          
          <div className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className={`text-xs px-2 py-1 rounded-full ${task.tagColor}`}>
                {task.tag}
              </span>
              <span className="text-xs text-gray-500">{task.date}</span>
            </div>
            
            <h4 className="font-semibold text-gray-900 mb-2">{task.title}</h4>
            <p className="text-sm text-gray-500 mb-4">{task.description}</p>
            
            {/* Progress */}
            <div className="mb-4">
              <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div className="h-full bg-violet-500" style={{ width: `${task.progress}%` }} />
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex -space-x-2">
                {task.assignees.map((a, i) => (
                  <img key={i} src={a.avatar} className="w-7 h-7 rounded-full border-2 border-white" />
                ))}
              </div>
              <button className="text-violet-600 text-sm font-medium">
                Details →
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

## 9. SWITCHER COMPONENT

```tsx
// ✅ VIEW SWITCHER
const ViewSwitcher = ({ value, onChange }) => {
  const views = [
    { id: 'calendar', icon: CalendarDays, label: 'Calendar' },
    { id: 'kanban', icon: Columns3, label: 'Kanban' },
    { id: 'list', icon: List, label: 'List' },
    { id: 'grid', icon: Grid3x3, label: 'Grid' },
    { id: 'table', icon: Table, label: 'Table' },
    { id: 'gantt', icon: GanttChart, label: 'Gantt' },
  ]
  
  return (
    <div className="inline-flex bg-gray-100 rounded-xl p-1">
      {views.map(view => (
        <button
          key={view.id}
          onClick={() => onChange(view.id)}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            value === view.id 
              ? 'bg-white text-gray-900 shadow-sm' 
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <view.icon className="w-4 h-4" />
          <span className="hidden md:inline">{view.label}</span>
        </button>
      ))}
    </div>
  )
}
```

## 10. FILTER BAR

```tsx
// ✅ FILTER BAR
const FilterBar = ({ filters, onChange }) => {
  return (
    <div className="flex items-center gap-3 flex-wrap">
      <SearchInput placeholder="Search tasks..." />
      <SelectFilter label="Status" options={['All', 'Active', 'Completed']} />
      <SelectFilter label="Assignee" options={['All', 'Me', 'Team']} />
      <SelectFilter label="Priority" options={['All', 'High', 'Medium', 'Low']} />
      <SelectFilter label="Due Date" options={['All', 'Today', 'This Week', 'This Month']} />
      <Button variant="outline" icon={<Filter />}>
        More Filters
      </Button>
      <Button variant="outline" icon={<ArrowUpDown />}>
        Sort
      </Button>
    </div>
  )
}
```

## View Comparison

| View | Best For | Strengths |
|------|----------|-----------|
| **Calendar Bar** | Schedule tracking | Time-based, overlap view |
| **Calendar Month** | Monthly overview | Big picture, density |
| **Calendar Week** | Weekly planning | Day-by-day detail |
| **Calendar List** | Agenda review | Sequential events |
| **Kanban** | Workflow tracking | Status visualization |
| **List** | Quick scanning | Compact, sortable |
| **Grid** | Visual tasks | Cover images, designing |
| **Table** | Bulk editing | Data-dense, sorting |
| **Gantt** | Project planning | Dependencies, timeline |
| **Heatmap** | Activity tracking | Patterns, streaks |
| **Mobile List** | Phone portrait | Vertical scroll |
| **Mobile Card** | Phone landscape | Visual, swipe-friendly |

## Responsive Strategy

| Device | Primary View | Secondary |
|--------|-------------|-----------|
| **Desktop** | Kanban, Grid, Table | All views |
| **Tablet** | Kanban, Calendar Bar | List, Grid |
| **Mobile** | List, Card | Calendar List |
| **Watch** | Today's tasks | Reminders |

## View Detection (Optional)

```tsx
// Auto-recommend view based on context
const useRecommendedView = (tasks, context) => {
  return useMemo(() => {
    if (context.hasDeadlines) return 'calendar'
    if (context.hasWorkflow) return 'kanban'
    if (context.hasTimeRange) return 'gantt'
    if (context.isMobile) return 'list'
    if (tasks.length > 100) return 'table'
    return 'grid'
  }, [tasks, context])
}
```

## Checklist - View Quality

- [ ] Multiple view options (8+ recommended)
- [ ] View switcher in toolbar
- [ ] Mobile-optimized views
- [ ] Filter/search bar
- [ ] Sort options
- [ ] Empty states
- [ ] Loading states
- [ ] Bulk actions
- [ ] Drag & drop (Kanban)
- [ ] Click to view details
- [ ] Keyboard shortcuts
- [ ] Save user preference
