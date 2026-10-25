# Flow to Image/Video Integration

Guide to generate visual assets from workflows and integrate into apps/websites.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ FLOW VISUALIZATION PIPELINE                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Google Flow / Diagram  ──▶  Export Image/Video  ──▶  Web/App   │
│                                                                   │
│         │                         │                    │          │
│         ▼                         ▼                    ▼          │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────┐   │
│  │ Draw.io     │         │ PNG/SVG     │         │ React   │   │
│  │ Lucidchart  │   ──▶   │ MP4/GIF     │   ──▶   │ Next.js │   │
│  │ Mermaid     │         │ WebP/AVIF   │         │ Native  │   │
│  │ Excalidraw  │         │             │         │         │   │
│  └─────────────┘         └─────────────┘         └─────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 1. FLOW EXPORT OPTIONS

### 1.1 Mermaid.js (Code-based)

```tsx
// ✅ Mermaid to Image
// Use mermaid.live or mermaid.cli to export

import mermaid from 'mermaid'

// Initialize
mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose',
})

// Generate SVG
const generateFlowchart = async (code: string): Promise<string> => {
  const { svg } = await mermaid.render('flowchart', code)
  return svg
}

// Example flow
const flowCode = `
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E((End))
    D --> E
`

// Convert to image
const svgString = await generateFlowchart(flowCode)
```

### 1.2 Export Functions

```tsx
// ✅ SVG to PNG/PDF
const svgToImage = async (svgString: string, format: 'png' | 'jpg' | 'pdf') => {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  const img = new Image()
  
  img.onload = () => {
    canvas.width = img.width * 2
    canvas.height = img.height * 2
    ctx.scale(2, 2)
    ctx.drawImage(img, 0, 0)
    
    return canvas.toDataURL(`image/${format}`)
  }
  
  img.src = `data:image/svg+xml;base64,${btoa(svgString)}`
}

// ✅ SVG to WebP/AVIF (better compression)
const svgToWebP = async (svgString: string): Promise<Blob> => {
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  const img = new Image()
  
  return new Promise((resolve) => {
    img.onload = () => {
      canvas.width = img.width
      canvas.height = img.height
      ctx.drawImage(img, 0, 0)
      canvas.toBlob(resolve, 'image/webp', 0.9)
    }
    img.src = `data:image/svg+xml;base64,${btoa(svgString)}`
  })
}
```

## 2. FLOW TO VIDEO

### 2.1 Animated Flow (CSS/JS)

```tsx
// ✅ ANIMATED FLOW COMPONENT
const AnimatedFlow = ({ steps }: { steps: FlowStep[] }) => {
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    if (currentStep < steps.length - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => prev + 1)
      }, 1500)
      return () => clearTimeout(timer)
    }
  }, [currentStep, steps.length])

  return (
    <div className="relative">
      {/* Flow nodes */}
      <div className="flex items-center gap-4">
        {steps.map((step, i) => (
          <div key={i} className="flex items-center">
            {/* Node */}
            <div
              className={`relative px-6 py-4 rounded-2xl border-2 transition-all duration-500 ${
                i <= currentStep 
                  ? 'bg-violet-600 text-white border-violet-600 scale-110' 
                  : 'bg-gray-100 text-gray-400 border-gray-200'
              }`}
              style={{ transitionDelay: `${i * 200}ms` }}
            >
              <step.icon className="w-6 h-6 mb-2" />
              <p className="text-sm font-medium">{step.label}</p>
              
              {/* Pulse animation for current */}
              {i === currentStep && (
                <span className="absolute inset-0 rounded-2xl animate-ping opacity-20 bg-white" />
              )}
            </div>
            
            {/* Connector */}
            {i < steps.length - 1 && (
              <div className={`w-12 h-0.5 mx-2 transition-colors duration-500 ${
                i < currentStep ? 'bg-violet-600' : 'bg-gray-200'
              }`}>
                <ChevronRight className={`w-4 h-4 text-inherit -ml-2 -mt-2 ${
                  i < currentStep ? 'text-violet-600' : 'text-gray-300'
                }`} />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

// ✅ USAGE
const steps = [
  { icon: FileSearch, label: 'Analyze' },
  { icon: Lightbulb, label: 'Design' },
  { icon: Code, label: 'Build' },
  { icon: TestTube, label: 'Test' },
  { icon: Rocket, label: 'Deploy' },
]

;<AnimatedFlow steps={steps} />
```

### 2.2 Recording Flow as Video

```tsx
// ✅ USE canvas API TO RECORD
const recordFlowAnimation = async (element: HTMLElement): Promise<Blob> => {
  const stream = element.captureStream(30) // 30 FPS
  const recorder = new MediaRecorder(stream, {
    mimeType: 'video/webm;codecs=vp9',
    videoBitsPerSecond: 2500000,
  })
  
  const chunks: BlobPart[] = []
  recorder.ondataavailable = (e) => chunks.push(e.data)
  
  return new Promise((resolve) => {
    recorder.onstop = () => {
      resolve(new Blob(chunks, { type: 'video/webm' }))
    }
    
    recorder.start()
    
    // Run animation
    animateFlow()
    
    setTimeout(() => recorder.stop(), 5000) // 5 seconds
  })
}
```

## 3. INTEGRATION PATTERNS

### 3.1 React Component

```tsx
// ✅ FLOW VISUALIZER COMPONENT
interface FlowVisualizerProps {
  type: 'linear' | 'branch' | 'cycle' | 'funnel'
  data: FlowData
  interactive?: boolean
  animated?: boolean
  exportable?: boolean
}

const FlowVisualizer = ({
  type = 'linear',
  data,
  interactive = true,
  animated = false,
  exportable = true
}: FlowVisualizerProps) => {
  const containerRef = useRef<HTMLDivElement>(null)

  // Export as image
  const exportAsPng = async () => {
    if (!containerRef.current) return
    
    const canvas = await html2canvas(containerRef.current, {
      scale: 2,
      backgroundColor: '#ffffff',
    })
    
    const link = document.createElement('a')
    link.download = 'flow-diagram.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
  }

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      {exportable && (
        <div className="flex items-center gap-2">
          <button onClick={exportAsPng} className="btn-secondary">
            <Download className="w-4 h-4" />
            Export PNG
          </button>
          <button className="btn-secondary">
            <FileVideo className="w-4 h-4" />
            Export GIF
          </button>
        </div>
      )}
      
      {/* Flow Container */}
      <div 
        ref={containerRef}
        className="bg-white p-8 rounded-2xl border border-gray-200"
      >
        {type === 'linear' && <LinearFlow data={data} animated={animated} />}
        {type === 'branch' && <BranchFlow data={data} animated={animated} />}
        {type === 'cycle' && <CycleFlow data={data} animated={animated} />}
        {type === 'funnel' && <FunnelFlow data={data} animated={animated} />}
      </div>
    </div>
  )
}
```

### 3.2 Linear Flow

```tsx
// ✅ LINEAR FLOW
const LinearFlow = ({ data, animated }: FlowVisualizerProps) => {
  return (
    <div className="flex items-center justify-center gap-0">
      {data.nodes.map((node, i) => (
        <React.Fragment key={node.id}>
          {/* Node */}
          <div className={`
            relative flex flex-col items-center justify-center
            w-32 h-32 rounded-2xl border-2 transition-all duration-500
            ${i % 2 === 0 ? 'bg-violet-50 border-violet-200' : 'bg-blue-50 border-blue-200'}
            ${animated ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'}
          `}>
            <node.icon className="w-8 h-8 text-violet-600 mb-2" />
            <span className="text-sm font-medium text-gray-700">{node.label}</span>
            <span className="text-xs text-gray-400">{node.value}</span>
          </div>
          
          {/* Arrow */}
          {i < data.nodes.length - 1 && (
            <div className="w-16 flex items-center justify-center">
              <div className="w-full h-0.5 bg-gradient-to-r from-violet-300 to-blue-300" />
              <ChevronRight className="w-5 h-5 text-gray-400 -ml-2" />
            </div>
          )}
        </React.Fragment>
      ))}
    </div>
  )
}
```

### 3.3 Branch Flow (Decision Tree)

```tsx
// ✅ BRANCH FLOW
const BranchFlow = ({ data }: FlowVisualizerProps) => {
  return (
    <div className="flex flex-col items-center">
      {/* Root */}
      <div className="w-40 h-16 bg-violet-600 text-white rounded-xl flex items-center justify-center font-medium mb-8">
        {data.root}
      </div>
      
      {/* Branches */}
      <div className="flex gap-16">
        {data.branches.map((branch, i) => (
          <div key={i} className="flex flex-col items-center">
            {/* Connector */}
            <div className="w-0.5 h-8 bg-gray-300" />
            <div className="w-4 h-4 border-2 border-gray-400 rounded-full bg-white" />
            <div className="w-0.5 h-8 bg-gray-300" />
            
            {/* Condition */}
            <div className="px-4 py-2 bg-gray-100 rounded-lg text-sm text-gray-600 mb-4">
              {branch.condition}
            </div>
            
            {/* Children */}
            {branch.nodes.map((node, j) => (
              <div key={j} className="w-32 h-12 bg-blue-500 text-white rounded-lg flex items-center justify-center text-sm">
                {node}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
```

### 3.4 Cycle Flow

```tsx
// ✅ CYCLE FLOW (CIRCULAR)
const CycleFlow = ({ data, animated }: FlowVisualizerProps) => {
  const total = data.nodes.length
  const radius = 120
  
  return (
    <div className="relative w-80 h-80 mx-auto">
      {/* SVG Circle */}
      <svg className="w-full h-full" viewBox="0 0 320 320">
        {/* Connection arcs */}
        {data.nodes.map((_, i) => {
          const startAngle = (i * 360) / total - 90
          const endAngle = ((i + 1) * 360) / total - 90
          
          return (
            <path
              key={i}
              d={describeArc(160, 160, radius, startAngle, endAngle)}
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="3"
              className={`transition-all duration-1000 ${
                animated ? 'stroke-dashoffset-100' : ''
              }`}
            />
          )
        })}
        
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
        </defs>
      </svg>
      
      {/* Center */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-20 h-20 bg-gradient-to-br from-violet-600 to-blue-600 rounded-full flex items-center justify-center text-white">
          <RotateCw className="w-8 h-8" />
        </div>
      </div>
      
      {/* Nodes */}
      {data.nodes.map((node, i) => {
        const angle = (i * 360) / total - 90
        const x = 160 + radius * Math.cos((angle * Math.PI) / 180)
        const y = 160 + radius * Math.sin((angle * Math.PI) / 180)
        
        return (
          <div
            key={i}
            className="absolute transform -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${x}px`, top: `${y}px` }}
          >
            <div className="w-16 h-16 bg-white rounded-xl shadow-lg border border-gray-100 flex flex-col items-center justify-center">
              <node.icon className="w-5 h-5 text-violet-600" />
              <span className="text-xs font-medium mt-1">{node.label}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}

// Helper for SVG arc
const describeArc = (x: number, y: number, radius: number, startAngle: number, endAngle: number) => {
  const start = polarToCartesian(x, y, radius, endAngle)
  const end = polarToCartesian(x, y, radius, startAngle)
  const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1
  
  return `M ${start.x} ${start.y} A ${radius} ${radius} 0 ${largeArcFlag} 0 ${end.x} ${end.y}`
}
```

### 3.5 Funnel Flow

```tsx
// ✅ FUNNEL FLOW
const FunnelFlow = ({ data, animated }: FlowVisualizerProps) => {
  return (
    <div className="space-y-2">
      {data.stages.map((stage, i) => {
        const width = 100 - i * 15 // Decreasing width
        
        return (
          <div key={i} className="flex items-center gap-4">
            {/* Stage */}
            <div 
              className="h-14 bg-gradient-to-r from-violet-500 to-violet-600 rounded-lg flex items-center justify-between px-6 text-white transition-all duration-500"
              style={{ width: `${width}%`, marginLeft: `${i * 5}%` }}
            >
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-sm font-bold">
                  {i + 1}
                </span>
                <span className="font-medium">{stage.name}</span>
              </div>
              <span className="text-lg font-bold">{stage.value.toLocaleString()}</span>
            </div>
            
            {/* Connector */}
            {i < data.stages.length - 1 && (
              <span className="text-sm text-gray-400">
                {Math.round((stage.value / data.stages[0].value) * 100)}%
              </span>
            )}
          </div>
        )
      })}
    </div>
  )
}
```

## 4. GOOGLE FLOW INTEGRATION

### 4.1 Google Drawings to Image

```tsx
// ✅ GOOGLE DRAWINGS EXPORT
// 1. In Google Drawings, go to File > Download > PNG/SVG
// 2. Or use Google Apps Script to auto-export

// apps-script.js
function exportDrawing() {
  const drawing = SlidesApp.getActivePresentation()
  const slides = drawing.getSlides()
  
  slides.forEach((slide, i) => {
    const shapes = slide.getShapes()
    shapes.forEach(shape => {
      // Export each shape as image
      const blob = shape.getAs('image/png')
      DriveApp.createFile(blob.setName(`shape_${i}.png`))
    })
  })
}
```

### 4.2 Google Slides Frame by Frame

```tsx
// ✅ SLIDES TO ANIMATED FRAMES
const slidesToFrames = async (presentationId: string) => {
  // Using Google Slides API
  const response = await gapi.client.slides.presentations.get({
    presentationId,
    pages: 'all'
  })
  
  const frames = response.result.slides.map((slide, i) => ({
    id: slide.objectId,
    index: i,
    elements: slide.pageElements,
    thumbnail: `https://slides.googleapis.com/v1/presentation/${presentationId}/pages/${slide.objectId}/thumbnail`
  }))
  
  return frames
}

// Render as animated carousel
const SlidesViewer = ({ frames }: { frames: Frame[] }) => {
  const [current, setCurrent] = useState(0)
  
  return (
    <div className="space-y-4">
      <img 
        src={frames[current].thumbnail}
        alt={`Frame ${current + 1}`}
        className="w-full rounded-2xl shadow-lg"
      />
      <div className="flex justify-center gap-2">
        {frames.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className={`w-2 h-2 rounded-full transition-all ${
              i === current ? 'bg-violet-600 w-6' : 'bg-gray-300'
            }`}
          />
        ))}
      </div>
    </div>
  )
}
```

### 4.3 Google Docs to Image

```tsx
// ✅ GOOGLE DOCS FLOWCHART TO IMAGE
const docToFlowchart = async (docId: string) => {
  // 1. Export doc as HTML
  const exportUrl = `https://docs.google.com/document/d/${docId}/export?format=html`
  
  // 2. Parse HTML and convert tables to flowchart
  const html = await fetch(exportUrl).then(r => r.text())
  const parser = new DOMParser()
  const doc = parser.parseFromString(html, 'text/html')
  
  // 3. Find table-based flowcharts
  const tables = doc.querySelectorAll('table')
  tables.forEach(table => {
    const rows = table.querySelectorAll('tr')
    const nodes = Array.from(rows).map(row => {
      const cells = row.querySelectorAll('td')
      return {
        text: cells[0]?.textContent,
        next: cells[1]?.textContent,
      }
    })
    // Convert to flow data
    return convertToFlowData(nodes)
  })
}
```

## 5. ANIMATION OPTIONS

### 5.1 Step-by-Step Reveal

```tsx
// ✅ STEP REVEAL ANIMATION
const StepRevealFlow = ({ nodes }: { nodes: FlowNode[] }) => {
  const [revealed, setRevealed] = useState(0)
  
  useEffect(() => {
    const timer = setInterval(() => {
      setRevealed(prev => prev < nodes.length - 1 ? prev + 1 : prev)
    }, 800)
    return () => clearInterval(timer)
  }, [])
  
  return (
    <div className="space-y-4">
      {nodes.map((node, i) => (
        <div
          key={i}
          className={`transition-all duration-500 ${
            i <= revealed 
              ? 'opacity-100 translate-x-0' 
              : 'opacity-0 -translate-x-8'
          }`}
        >
          <div className="flex items-center gap-4">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
              i < revealed ? 'bg-violet-600 text-white' : 'bg-gray-200 text-gray-400'
            }`}>
              {i < revealed ? <Check className="w-5 h-5" /> : <span>{i + 1}</span>}
            </div>
            <span className="font-medium">{node.label}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
```

### 5.2 SVG Path Animation

```tsx
// ✅ SVG PATH DRAWING
const AnimatedPath = ({ path }: { path: string }) => {
  return (
    <svg className="w-full h-full">
      <path
        d={path}
        fill="none"
        stroke="#8b5cf6"
        strokeWidth="3"
        strokeLinecap="round"
        className="path-animation"
      />
      <style>{`
        .path-animation {
          stroke-dasharray: 1000;
          stroke-dashoffset: 1000;
          animation: draw 3s ease-in-out forwards;
        }
        @keyframes draw {
          to { stroke-dashoffset: 0; }
        }
      `}</style>
    </svg>
  )
}
```

## 6. EXPORT OPTIONS

### 6.1 Download as Image

```tsx
// ✅ EXPORT COMPONENT AS IMAGE
const exportAsImage = async (elementRef: React.RefObject<HTMLElement>) => {
  const element = elementRef.current
  if (!element) return
  
  // Option 1: html2canvas
  const canvas = await html2canvas(element, {
    scale: 2, // Retina
    useCORS: true,
    backgroundColor: '#ffffff',
  })
  
  // Option 2: dom-to-image
  // const canvas = await domtoimage.toCanvas(element, {
  //   pixelRatio: 2,
  // })
  
  const link = document.createElement('a')
  link.download = `flow-${Date.now()}.png`
  link.href = canvas.toDataURL('image/png')
  link.click()
}

// Export as SVG
const exportAsSvg = async (elementRef: React.RefObject<HTMLElement>) => {
  const element = elementRef.current
  if (!element) return
  
  const svg = await domtoimage.toSvg(element)
  const link = document.createElement('a')
  link.download = `flow-${Date.now()}.svg`
  link.href = svg
  link.click()
}
```

### 6.2 Export as PDF

```tsx
// ✅ EXPORT AS PDF
const exportAsPdf = async (elementRef: React.RefObject<HTMLElement>) => {
  const element = elementRef.current
  if (!element) return
  
  const canvas = await html2canvas(element, { scale: 2 })
  
  const { jsPDF } = await import('jspdf')
  const pdf = new jsPDF({
    orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
    unit: 'px',
    format: [canvas.width, canvas.height],
  })
  
  pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, canvas.width, canvas.height)
  pdf.save(`flow-${Date.now()}.pdf`)
}
```

### 6.3 Export as GIF

```tsx
// ✅ EXPORT ANIMATED GIF
const exportAsGif = async (elementRef: React.RefObject<HTMLElement>) => {
  const element = elementRef.current
  if (!element) return
  
  const canvas = await html2canvas(element, { 
    scale: 1,
    backgroundColor: '#ffffff',
  })
  
  const gif = new GIF({
    workers: 2,
    quality: 10,
    width: canvas.width,
    height: canvas.height,
    workerScript: '/gif.worker.js',
  })
  
  // Capture 30 frames over 3 seconds
  for (let i = 0; i < 30; i++) {
    // Update animation state
    updateAnimationProgress(i / 30)
    
    const frame = await html2canvas(element)
    gif.addFrame(frame, { delay: 100 })
  }
  
  gif.on('finished', (blob) => {
    const link = document.createElement('a')
    link.download = `flow-${Date.now()}.gif`
    link.href = URL.createObjectURL(blob)
    link.click()
  })
  
  gif.render()
}
```

## 7. ICONS

```tsx
import {
  // Navigation
  ChevronRight, ChevronDown, Plus, X, RotateCw,
  
  // Files
  FileSearch, FileVideo, Download, Upload,
  File, FileText, Image,
  
  // Actions
  Check, CheckCircle, Play, Pause, SkipForward,
  
  // Flow
  GitBranch, ArrowRight, ArrowDown, RefreshCw,
  Workflow, Activity, Zap, Gauge,
  
  // Status
  Circle, Loader2, Clock, AlertCircle,
  
  // Misc
  Share2, Copy, ExternalLink, Settings,
} from 'lucide-react'
```

## Flow to Image/Video Checklist

- [ ] Mermaid.js flow generation
- [ ] SVG to PNG export
- [ ] SVG to WebP/AVIF export
- [ ] Animated flow component
- [ ] Canvas recording to video
- [ ] Linear flow visualization
- [ ] Branch/decision flow
- [ ] Cycle/circular flow
- [ ] Funnel flow
- [ ] Google Drawings integration
- [ ] Google Slides integration
- [ ] Google Docs integration
- [ ] Step-by-step reveal animation
- [ ] SVG path animation
- [ ] Export as PNG
- [ ] Export as SVG
- [ ] Export as PDF
- [ ] Export as GIF
- [ ] Export as WebM video
- [ ] Responsive layout
- [ ] Dark mode support
- [ ] Touch-friendly controls
- [ ] Keyboard navigation
- [ ] Print-optimized layout
- [ ] Custom theme/styling
