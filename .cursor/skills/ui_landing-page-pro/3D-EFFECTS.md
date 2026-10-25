# 3D Image Effects Library

Professional 3D image effects for landing pages and hero sections.

## 1. 3D Image Transforms

### 1.1 Basic 3D Image Tilt

```tsx
// ✅ 3D IMAGE TILT ON HOVER
const ImageTilt3D = ({ src, alt, intensity = 10 }) => {
  const containerRef = useRef(null)
  const imgRef = useRef(null)
  
  useEffect(() => {
    const container = containerRef.current
    const img = imgRef.current
    if (!container || !img) return
    
    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      
      const centerX = rect.width / 2
      const centerY = rect.height / 2
      
      const rotateX = ((y - centerY) / centerY) * -intensity
      const rotateY = ((x - centerX) / centerX) * intensity
      
      img.style.transform = `
        perspective(1000px) 
        rotateX(${rotateX}deg) 
        rotateY(${rotateY}deg)
        scale(1.05)
      `
      
      // Move reflection/shine
      const shine = container.querySelector('.shine')
      if (shine) {
        const percentX = (x / rect.width) * 100
        const percentY = (y / rect.height) * 100
        shine.style.background = `
          radial-gradient(circle at ${percentX}% ${percentY}%, 
            rgba(255,255,255,0.3) 0%, 
            transparent 60%)
        `
        shine.style.opacity = '1'
      }
    }
    
    const handleMouseLeave = () => {
      img.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)'
      const shine = container.querySelector('.shine')
      if (shine) shine.style.opacity = '0'
    }
    
    container.addEventListener('mousemove', handleMouseMove)
    container.addEventListener('mouseleave', handleMouseLeave)
    
    return () => {
      container.removeEventListener('mousemove', handleMouseMove)
      container.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [intensity])
  
  return (
    <div 
      ref={containerRef}
      className="relative overflow-hidden rounded-2xl cursor-pointer"
      style={{ perspective: '1000px' }}
    >
      <img
        ref={imgRef}
        src={src}
        alt={alt}
        className="w-full h-full object-cover transition-transform duration-200 ease-out"
        style={{ transformStyle: 'preserve-3d' }}
      />
      {/* Shine overlay */}
      <div className="shine absolute inset-0 opacity-0 pointer-events-none transition-opacity duration-300" />
    </div>
  )
}
```

### 1.2 Multi-Layer 3D Parallax

```tsx
// ✅ MULTI-LAYER 3D PARALLAX IMAGE
const ParallaxImage3D = ({ layers }) => {
  const containerRef = useRef(null)
  
  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    
    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect()
      const centerX = rect.width / 2
      const centerY = rect.height / 2
      
      const mouseX = e.clientX - rect.left - centerX
      const mouseY = e.clientY - rect.top - centerY
      
      // Each layer moves at different speed
      const layerElements = container.querySelectorAll('[data-depth]')
      layerElements.forEach((el) => {
        const depth = parseFloat(el.dataset.depth)
        const moveX = mouseX * depth * 0.1
        const moveY = mouseY * depth * 0.1
        el.style.transform = `translate(${moveX}px, ${moveY}px)`
      })
    }
    
    const handleMouseLeave = () => {
      const layerElements = container.querySelectorAll('[data-depth]')
      layerElements.forEach((el) => {
        el.style.transform = 'translate(0, 0)'
      })
    }
    
    container.addEventListener('mousemove', handleMouseMove)
    container.addEventListener('mouseleave', handleMouseLeave)
    
    return () => {
      container.removeEventListener('mousemove', handleMouseMove)
      container.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [])
  
  return (
    <div 
      ref={containerRef}
      className="relative overflow-hidden rounded-2xl"
      style={{ height: '500px' }}
    >
      {layers.map((layer, i) => (
        <div
          key={i}
          data-depth={layer.depth}
          className="absolute inset-0 transition-transform duration-100 ease-out"
          style={{ zIndex: i + 1 }}
        >
          {layer.type === 'image' ? (
            <img 
              src={layer.src} 
              alt={layer.alt || ''}
              className={layer.className || 'w-full h-full object-cover'}
            />
          ) : (
            <div className={layer.className}>
              {layer.content}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// Usage
const HeroWithParallax = () => (
  <ParallaxImage3D
    layers={[
      { type: 'image', src: '/bg-mountain.jpg', depth: 0.1, className: 'w-full h-full object-cover' },
      { type: 'image', src: '/clouds.png', depth: 0.3, className: 'w-full h-full object-cover' },
      { type: 'image', src: '/foreground-trees.png', depth: 0.6, className: 'w-full h-full object-cover' },
      { type: 'content', depth: 0.2, content: <div className="absolute inset-0 flex items-center justify-center"><h1>Your Text</h1></div> }
    ]}
  />
)
```

## 2. 3D Image Reveal Animations

### 2.1 Clip Path Reveal

```tsx
// ✅ CLIP PATH IMAGE REVEAL
const RevealImageClip = ({ src, direction = 'up' }) => {
  const [isVisible, setIsVisible] = useState(false)
  const ref = useRef(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.3 }
    )
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])
  
  const clipPaths = {
    up: 'inset(100% 0 0 0) → inset(0% 0 0 0)',
    down: 'inset(0 0 100% 0) → inset(0 0 0% 0)',
    left: 'inset(0 0 0 100%) → inset(0 0 0 0%)',
    right: 'inset(0 100% 0 0) → inset(0 0 0 0)',
    center: 'circle(0% at 50% 50%) → circle(75% at 50% 50%)',
    diagonal: 'polygon(50% 50% 50% 50% 50% 50%) → polygon(0% 0% 100% 0% 100% 100% 0% 100%)',
  }
  
  return (
    <div 
      ref={ref}
      className="overflow-hidden rounded-2xl"
    >
      <img
        src={src}
        alt=""
        className="w-full h-full object-cover transition-all duration-1000 ease-out"
        style={{
          clipPath: isVisible ? 'inset(0 0 0 0)' : 'inset(100% 0 0 0)',
        }}
      />
    </div>
  )
}
```

### 2.2 Curtain Reveal

```tsx
// ✅ CURTAIN REVEAL IMAGE
const CurtainReveal = ({ src, revealPercent = 50 }) => {
  const [isVisible, setIsVisible] = useState(false)
  const ref = useRef(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.3 }
    )
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])
  
  return (
    <div 
      ref={ref}
      className="relative overflow-hidden rounded-2xl"
      style={{ paddingBottom: `${revealPercent}%` }}
    >
      {/* Bottom image (revealed) */}
      <img
        src={src}
        alt=""
        className="absolute inset-0 w-full h-full object-cover"
        style={{
          clipPath: isVisible ? 'inset(0)' : 'inset(100% 0 0 0)',
          transition: 'clip-path 1.2s cubic-bezier(0.77, 0, 0.175, 1)',
        }}
      />
      {/* Top image (revealing) */}
      <img
        src={src}
        alt=""
        className="absolute inset-0 w-full h-full object-cover"
        style={{
          clipPath: isVisible ? 'inset(0 0 100% 0)' : 'inset(0)',
          transition: 'clip-path 1.2s cubic-bezier(0.77, 0, 0.175, 1) 0.1s',
        }}
      />
    </div>
  )
}
```

### 2.3 3D Flip Reveal

```tsx
// ✅ 3D FLIP REVEAL
const FlipReveal3D = ({ frontSrc, backSrc, revealDelay = 0 }) => {
  const [isFlipped, setIsFlipped] = useState(false)
  const ref = useRef(null)
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => setIsFlipped(true), revealDelay)
          observer.disconnect()
        }
      },
      { threshold: 0.3 }
    )
    
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [revealDelay])
  
  return (
    <div 
      ref={ref}
      className="relative h-96 cursor-pointer"
      style={{ perspective: '1000px' }}
    >
      <div
        className="absolute inset-0 transition-transform duration-1000"
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
      >
        {/* Front */}
        <div 
          className="absolute inset-0 rounded-2xl overflow-hidden backface-hidden"
          style={{ backfaceVisibility: 'hidden' }}
        >
          <img src={frontSrc} alt="" className="w-full h-full object-cover" />
        </div>
        {/* Back */}
        <div 
          className="absolute inset-0 rounded-2xl overflow-hidden backface-hidden"
          style={{ 
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)'
          }}
        >
          <img src={backSrc} alt="" className="w-full h-full object-cover" />
        </div>
      </div>
    </div>
  )
}
```

## 3. 3D Image Gallery Effects

### 3.1 3D Carousel

```tsx
// ✅ 3D IMAGE CAROUSEL
const Carousel3D = ({ images }) => {
  const [activeIndex, setActiveIndex] = useState(0)
  const [isAutoPlaying, setIsAutoPlaying] = useState(true)
  
  useEffect(() => {
    if (!isAutoPlaying) return
    
    const interval = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % images.length)
    }, 4000)
    
    return () => clearInterval(interval)
  }, [isAutoPlaying, images.length])
  
  return (
    <div 
      className="relative h-96"
      style={{ perspective: '1200px' }}
      onMouseEnter={() => setIsAutoPlaying(false)}
      onMouseLeave={() => setIsAutoPlaying(true)}
    >
      <div className="absolute inset-0 flex items-center justify-center">
        {images.map((img, i) => {
          const offset = i - activeIndex
          const absOffset = Math.abs(offset)
          
          return (
            <div
              key={i}
              className="absolute transition-all duration-700 ease-out"
              style={{
                transform: `
                  translateX(${offset * 60}%) 
                  translateZ(${-absOffset * 200}px)
                  rotateY(${offset * -15}deg)
                  scale(${1 - absOffset * 0.2})
                `,
                opacity: absOffset > 2 ? 0 : 1,
                zIndex: images.length - absOffset,
              }}
            >
              <img 
                src={img} 
                alt=""
                className="h-80 w-80 object-cover rounded-2xl shadow-2xl"
              />
            </div>
          )
        })}
      </div>
      
      {/* Dots */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
        {images.map((_, i) => (
          <button
            key={i}
            onClick={() => setActiveIndex(i)}
            className={`w-2 h-2 rounded-full transition-all ${
              i === activeIndex ? 'bg-white w-6' : 'bg-white/50'
            }`}
          />
        ))}
      </div>
    </div>
  )
}
```

### 3.2 Perspective Grid Gallery

```tsx
// ✅ PERSPECTIVE GALLERY GRID
const PerspectiveGallery = ({ images }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null)
  
  return (
    <div 
      className="grid grid-cols-3 gap-4"
      style={{ 
        perspective: '1000px',
        transformStyle: 'preserve-3d'
      }}
    >
      {images.map((img, i) => {
        const isHovered = hoveredIndex === i
        const row = Math.floor(i / 3)
        const col = i % 3
        
        return (
          <div
            key={i}
            className={cn(
              "relative aspect-square rounded-xl overflow-hidden cursor-pointer transition-all duration-300",
              (row + col) % 2 === 0 ? "rotate-1" : "-rotate-1",
              isHovered && "scale-110 z-10"
            )}
            style={{
              transform: `
                perspective(1000px)
                rotateY(${isHovered ? (col - 1) * 5 : 0}deg)
                rotateX(${isHovered ? (1 - row) * 5 : 0}deg)
                ${(row + col) % 2 === 0 ? 'rotate-1' : '-rotate-1'}
              `,
              transformOrigin: 'center center',
            }}
            onMouseEnter={() => setHoveredIndex(i)}
            onMouseLeave={() => setHoveredIndex(null)}
          >
            <img 
              src={img} 
              alt=""
              className="w-full h-full object-cover transition-transform duration-300"
              style={{
                transform: isHovered ? 'scale(1.1)' : 'scale(1)',
              }}
            />
            
            {/* Overlay on hover */}
            <div className={cn(
              "absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end p-4 transition-opacity",
              isHovered ? "opacity-100" : "opacity-0"
            )}>
              <p className="text-white font-medium">Image {i + 1}</p>
            </div>
          </div>
        )
      })}
    </div>
  )
}
```

## 4. 3D Image Masks

### 4.1 Perspective Image

```tsx
// ✅ PERSPECTIVE IMAGE TRANSFORM
const PerspectiveImage = ({ src, angle = 10, direction = 'right' }) => {
  const rotateY = direction === 'right' ? angle : -angle
  
  return (
    <div 
      className="relative"
      style={{ 
        perspective: '1000px',
        perspectiveOrigin: direction === 'right' ? 'left center' : 'right center'
      }}
    >
      <img
        src={src}
        alt=""
        className="w-full h-full object-cover"
        style={{
          transform: `rotateY(${rotateY}deg)`,
          transformOrigin: direction === 'right' ? 'left center' : 'right center',
          transformStyle: 'preserve-3d',
        }}
      />
      {/* Shadow */}
      <div 
        className="absolute inset-0 -translate-z-10"
        style={{
          background: 'linear-gradient(to bottom, rgba(0,0,0,0.3), transparent)',
          filter: 'blur(20px)',
          transform: `rotateY(${rotateY}deg) translateZ(-50px) scale(0.9)`,
        }}
      />
    </div>
  )
}
```

### 4.2 Cylinder/MacBook Effect

```tsx
// ✅ MACBOOK/DEVICE FRAME IMAGE
const DeviceFrameImage = ({ src, device = 'macbook' }) => {
  const devices = {
    macbook: {
      frame: 'bg-gray-900 rounded-t-2xl p-3 pb-0',
      screen: 'bg-gray-800 rounded-lg overflow-hidden',
      notch: '',
      aspect: 'aspect-[16/10]',
    },
    iphone: {
      frame: 'bg-gray-900 rounded-[3rem] p-2',
      screen: 'bg-white rounded-[2.5rem] overflow-hidden',
      notch: 'w-24 h-6 bg-black rounded-full mx-auto',
      aspect: 'aspect-[9/19.5]',
    },
    ipad: {
      frame: 'bg-gray-900 rounded-2xl p-4',
      screen: 'bg-white rounded-xl overflow-hidden',
      notch: '',
      aspect: 'aspect-[4/3]',
    },
  }
  
  const d = devices[device]
  
  return (
    <div className={d.frame}>
      {d.notch && <div className={d.notch} />}
      <div className={cn(d.screen, d.aspect)}>
        <img 
          src={src} 
          alt=""
          className="w-full h-full object-cover"
        />
      </div>
      {device === 'macbook' && (
        <div className="h-4 bg-gray-900 rounded-b-lg -mx-3" />
        <div className="h-1 bg-gray-800 rounded-b-lg -mx-3 -mt-1" />
      )}
    </div>
  )
}
```

## 5. 3D Depth Effects

### 5.1 Depth Map Effect

```tsx
// ✅ DEPTH MAP / DOF EFFECT
const DepthEffectImage = ({ src, depthSrc, focusPoint = { x: 50, y: 50 } }) => {
  const [isLoaded, setIsLoaded] = useState(false)
  
  return (
    <div className="relative overflow-hidden rounded-2xl">
      {/* Base image */}
      <img
        src={src}
        alt=""
        className="w-full h-full object-cover"
        onLoad={() => setIsLoaded(true)}
      />
      
      {/* Depth overlay */}
      <img
        src={depthSrc}
        alt=""
        className="absolute inset-0 w-full h-full object-cover mix-blend-soft-light opacity-50"
        style={{
          filter: `blur(${(1 - focusPoint.y / 100) * 10}px)`,
          transform: `scale(${(1 - focusPoint.y / 100) * 0.5 + 1})`,
        }}
      />
      
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
    </div>
  )
}
```

### 5.2 Floating Layers Effect

```tsx
// ✅ FLOATING LAYERS IMAGE
const FloatingLayersImage = ({ layers }) => {
  return (
    <div className="relative h-96">
      {layers.map((layer, i) => (
        <div
          key={i}
          className={cn(
            "absolute transition-all duration-500",
            layer.position
          )}
          style={{
            animation: `float${i + 1} ${3 + i * 0.5}s ease-in-out infinite`,
            animationDelay: `${i * 0.3}s`,
          }}
        >
          <div className={cn(
            "rounded-2xl overflow-hidden shadow-2xl",
            layer.shadowColor && `shadow-[0_20px_50px_${layer.shadowColor}]`
          )}>
            <img 
              src={layer.src} 
              alt=""
              className={layer.className || 'w-auto h-auto'}
            />
          </div>
        </div>
      ))}
      
      <style>{`
        @keyframes float1 {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-15px) rotate(2deg); }
        }
        @keyframes float2 {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(-3deg); }
        }
        @keyframes float3 {
          0%, 100% { transform: translateY(0) rotate(0deg); }
          50% { transform: translateY(-10px) rotate(1deg); }
        }
      `}</style>
    </div>
  )
}

// Usage
const FloatingHero = () => (
  <FloatingLayersImage
    layers={[
      { src: '/product-main.png', position: 'top-0 left-1/2 -translate-x-1/2 z-30', className: 'h-80' },
      { src: '/product-float-1.png', position: 'top-10 left-0 z-20', className: 'h-40' },
      { src: '/product-float-2.png', position: 'top-20 right-0 z-20', className: 'h-48' },
      { src: '/product-float-3.png', position: 'bottom-10 left-10 z-10', className: 'h-32' },
    ]}
  />
)
```

## 6. 3D Hover Interactions

### 6.1 Image Magnetic Effect

```tsx
// ✅ MAGNETIC IMAGE HOVER
const MagneticImage = ({ src, strength = 0.3 }) => {
  const ref = useRef(null)
  
  useEffect(() => {
    const el = ref.current
    if (!el) return
    
    const handleMouseMove = (e) => {
      const rect = el.getBoundingClientRect()
      const centerX = rect.left + rect.width / 2
      const centerY = rect.top + rect.height / 2
      
      const deltaX = (e.clientX - centerX) * strength
      const deltaY = (e.clientY - centerY) * strength
      
      el.querySelector('img').style.transform = `
        translate(${deltaX}px, ${deltaY}px) 
        scale(1.05)
      `
    }
    
    const handleMouseLeave = () => {
      el.querySelector('img').style.transform = 'translate(0, 0) scale(1)'
    }
    
    el.addEventListener('mousemove', handleMouseMove)
    el.addEventListener('mouseleave', handleMouseLeave)
    
    return () => {
      el.removeEventListener('mousemove', handleMouseMove)
      el.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [strength])
  
  return (
    <div ref={ref} className="overflow-hidden rounded-2xl cursor-pointer">
      <img src={src} alt="" className="w-full h-full object-cover transition-transform duration-200" />
    </div>
  )
}
```

### 6.2 Image Split Hover

```tsx
// ✅ SPLIT IMAGE HOVER
const SplitImageHover = ({ src }) => {
  return (
    <div className="grid grid-cols-2 gap-2 h-80 rounded-2xl overflow-hidden cursor-pointer">
      <div className="relative overflow-hidden group">
        <img 
          src={src} 
          alt="" 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:-translate-x-full"
        />
      </div>
      <div className="relative overflow-hidden group">
        <img 
          src={src} 
          alt="" 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:translate-x-full"
        />
      </div>
    </div>
  )
}
```

## 7. 3D Image Sequences

### 7.1 Mouse Following 3D

```tsx
// ✅ MOUSE FOLLOWING 3D EFFECT
const MouseFollow3D = ({ frames }) => {
  const [currentFrame, setCurrentFrame] = useState(0)
  const containerRef = useRef(null)
  
  useEffect(() => {
    const container = containerRef.current
    if (!container) return
    
    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect()
      const x = (e.clientX - rect.left) / rect.width
      const frameIndex = Math.min(
        Math.floor(x * frames.length),
        frames.length - 1
      )
      setCurrentFrame(frameIndex)
    }
    
    container.addEventListener('mousemove', handleMouseMove)
    return () => container.removeEventListener('mousemove', handleMouseMove)
  }, [frames])
  
  return (
    <div 
      ref={containerRef}
      className="relative h-80 cursor-pointer"
      style={{ perspective: '500px' }}
    >
      {frames.map((frame, i) => (
        <img
          key={i}
          src={frame}
          alt=""
          className="absolute inset-0 w-full h-full object-cover transition-opacity duration-100"
          style={{
            opacity: i === currentFrame ? 1 : 0,
            transform: `translateZ(${(i - currentFrame) * 10}px)`,
          }}
        />
      ))}
      
      {/* Reflection */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent to-white/20 pointer-events-none" />
    </div>
  )
}
```

## 8. Combined 3D Hero Section

```tsx
// ✅ COMPLETE 3D HERO SECTION
const Hero3D = () => {
  return (
    <section className="relative min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>
      
      <div className="relative z-10 grid lg:grid-cols-2 min-h-screen items-center">
        {/* Left: Content */}
        <div className="px-8 lg:px-16 py-24 space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm text-white/90">New: 3D Product Viewer</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight">
            Experience
            <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              in 3D
            </span>
          </h1>
          
          <p className="text-lg text-slate-300 max-w-md">
            Interactive 3D product visualization that converts visitors into customers. 
            Rotate, zoom, and explore every detail.
          </p>
          
          <div className="flex gap-4">
            <button className="px-6 py-3 bg-white text-slate-900 rounded-xl font-semibold hover:bg-blue-50 transition-colors">
              Try Demo
            </button>
            <button className="px-6 py-3 rounded-xl font-semibold text-white border border-white/30 hover:bg-white/10 transition-colors">
              Learn More
            </button>
          </div>
        </div>
        
        {/* Right: 3D Image */}
        <div className="relative px-8 lg:px-16">
          <div className="relative" style={{ perspective: '1000px' }}>
            {/* Main product image with 3D tilt */}
            <ImageTilt3D
              src="/product-3d.jpg"
              alt="3D Product"
              intensity={8}
              className="rounded-2xl shadow-2xl"
            />
            
            {/* Floating accent images */}
            <div 
              className="absolute -top-8 -right-8 w-32 h-32 animate-float"
              style={{ perspective: '500px', transform: 'rotateY(-15deg)' }}
            >
              <img 
                src="/feature-1.png" 
                alt=""
                className="w-full h-full object-cover rounded-xl shadow-xl"
              />
            </div>
            
            <div 
              className="absolute -bottom-6 -left-6 w-40 h-40 animate-float-delayed"
              style={{ perspective: '500px', transform: 'rotateY(15deg)' }}
            >
              <img 
                src="/feature-2.png" 
                alt=""
                className="w-full h-full object-cover rounded-xl shadow-xl"
              />
            </div>
            
            {/* Glow effect */}
            <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-3xl blur-2xl opacity-30 -z-10" />
          </div>
        </div>
      </div>
    </section>
  )
}
```

## Animation Keyframes

```css
/* Add to tailwind.config.js or global CSS */

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(2deg); }
}

@keyframes float-delayed {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(-2deg); }
}

@keyframes float-delayed-more {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-25px); }
}

@keyframes pulse-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes orbit {
  from { transform: rotate(0deg) translateX(120px) rotate(0deg); }
  to { transform: rotate(360deg) translateX(120px) rotate(-360deg); }
}

/* Utilities */
.animate-float { animation: float 6s ease-in-out infinite; }
.animate-float-delayed { animation: float-delayed 6s ease-in-out 2s infinite; }
.animate-float-delayed-more { animation: float-delayed-more 6s ease-in-out 4s infinite; }
.animate-pulse-glow { animation: pulse-glow 3s ease-in-out infinite; }
.animate-spin-slow { animation: spin-slow 20s linear infinite; }
.animate-orbit { animation: orbit 8s linear infinite; }

/* 3D transforms */
.preserve-3d { transform-style: preserve-3d; }
.backface-hidden { backface-visibility: hidden; }
.perspective-1000 { perspective: 1000px; }
```

## 3D Effects Checklist

- [ ] 3D Tilt effect on images
- [ ] Parallax layers
- [ ] Reveal animations (clip-path, curtain, flip)
- [ ] 3D Carousel
- [ ] Perspective transforms
- [ ] Device frame mockups
- [ ] Floating layers
- [ ] Magnetic hover
- [ ] Mouse-following 3D
- [ ] Performance optimized (will-change, GPU acceleration)
- [ ] Mobile fallback (reduce/remove 3D on touch devices)
