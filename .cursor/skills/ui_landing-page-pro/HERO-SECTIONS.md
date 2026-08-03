# Hero Section Library - Eye-Catching Designs

Collection of distinctive, conversion-focused Hero sections that don't look templated.

## Hero Variation 1: Glassmorphism Floating

```tsx
// ✅ GLASS FLOATING HERO
const HeroGlassFloat = () => (
  <section className="relative min-h-screen overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950">
    {/* Animated gradient background */}
    <div className="absolute inset-0">
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/30 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000" />
      <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl animate-pulse delay-500" />
    </div>
    
    {/* Floating glass cards */}
    <div className="absolute top-20 left-10 animate-float">
      <GlassCard icon={<Zap />} label="Lightning Fast" value="10x" />
    </div>
    <div className="absolute top-40 right-20 animate-float-delayed">
      <GlassCard icon={<Shield />} label="Secure" value="100%" />
    </div>
    <div className="absolute bottom-40 left-20 animate-float-delayed-more">
      <GlassCard icon={<Users />} label="Active Users" value="50K+" />
    </div>
    
    {/* Main content */}
    <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
      <div className="text-center max-w-5xl mx-auto space-y-8">
        {/* Eyebrow */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
          <Sparkles className="w-4 h-4 text-yellow-400" />
          <span className="text-sm text-white/90">Introducing Version 2.0</span>
        </div>
        
        {/* Headline */}
        <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
          Build Products
          <span className="block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            That Stand Out
          </span>
        </h1>
        
        {/* Subheadline */}
        <p className="text-xl text-slate-300 max-w-2xl mx-auto">
          The all-in-one platform that helps teams ship faster, collaborate better, 
          and create products users actually love.
        </p>
        
        {/* CTAs */}
        <div className="flex flex-wrap items-center justify-center gap-4">
          <button className="group px-8 py-4 bg-white text-slate-900 rounded-xl font-semibold hover:bg-blue-50 transition-all hover:scale-105 shadow-2xl shadow-blue-500/25">
            <span className="flex items-center gap-2">
              Get Started Free
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </span>
          </button>
          <button className="px-8 py-4 rounded-xl font-semibold text-white border border-white/30 hover:bg-white/10 backdrop-blur-sm transition-all">
            Watch Demo
          </button>
        </div>
        
        {/* Social proof */}
        <div className="pt-8 flex items-center justify-center gap-8">
          <div className="flex -space-x-3">
            {['👨‍💼', '👩‍💻', '👨‍🎨', '👩‍🔬', '👨‍🚀'].map((emoji, i) => (
              <div key={i} className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-lg border-2 border-slate-900">
                {emoji}
              </div>
            ))}
          </div>
          <div className="text-left">
            <div className="flex items-center gap-1 text-yellow-400">
              {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
            </div>
            <p className="text-sm text-slate-400">Loved by <span className="text-white font-medium">50,000+</span> teams</p>
          </div>
        </div>
      </div>
    </div>
    
    {/* Product mockup */}
    <div className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1/3 w-full max-w-4xl">
      <div className="relative">
        <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-white/10 p-4 shadow-2xl">
          <img src="/product-mockup.png" alt="Product" className="rounded-lg w-full" />
        </div>
        {/* Glow effect */}
        <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-3xl blur-2xl opacity-30 -z-10" />
      </div>
    </div>
  </section>
)

// Glass Card Component
const GlassCard = ({ icon, label, value }) => (
  <div className="bg-white/10 backdrop-blur-xl rounded-xl p-4 border border-white/20 shadow-xl">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white">
        {icon}
      </div>
      <div>
        <p className="text-xs text-white/60">{label}</p>
        <p className="text-lg font-bold text-white">{value}</p>
      </div>
    </div>
  </div>
)
```

## Hero Variation 2: Split 3D Tilt

```tsx
// ✅ SPLIT 3D TILT HERO
const HeroSplit3D = () => {
  return (
    <section className="relative min-h-screen bg-white overflow-hidden">
      <div className="grid lg:grid-cols-2 min-h-screen">
        {/* Left: Content */}
        <div className="flex flex-col justify-center px-8 lg:px-16 py-24">
          <div className="max-w-xl">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-50 text-rose-600 text-sm font-medium mb-6">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500" />
              </span>
              New Feature Released
            </div>
            
            {/* Headline */}
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
              Design without
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-rose-600">
                limits
              </span>
            </h1>
            
            {/* Description */}
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Create stunning interfaces in minutes. Our AI-powered design system 
              adapts to your brand and helps you ship faster than ever before.
            </p>
            
            {/* Form */}
            <form className="flex gap-3 mb-8">
              <input 
                type="email" 
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"
              />
              <button className="px-6 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 transition-colors whitespace-nowrap">
                Get Started
              </button>
            </form>
            
            {/* Trust */}
            <p className="text-sm text-gray-500">
              Free 14-day trial. No credit card required.
            </p>
          </div>
        </div>
        
        {/* Right: 3D Visual */}
        <div className="relative flex items-center justify-center p-8 bg-gradient-to-br from-violet-50 to-rose-50">
          <TiltCard3D className="w-full max-w-lg">
            <div className="bg-white rounded-3xl shadow-2xl p-6 space-y-6">
              {/* UI Preview */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                </div>
                <div className="flex gap-2">
                  {['Dashboard', 'Analytics', 'Settings'].map(tab => (
                    <span key={tab} className="px-3 py-1 text-xs text-gray-500 bg-gray-100 rounded-full">
                      {tab}
                    </span>
                  ))}
                </div>
              </div>
              
              {/* Chart */}
              <div className="h-48 bg-gradient-to-br from-violet-100 to-rose-100 rounded-2xl flex items-end justify-around p-4">
                {[40, 65, 45, 80, 55, 90, 70].map((h, i) => (
                  <div 
                    key={i} 
                    className="w-8 bg-gradient-to-t from-violet-500 to-rose-500 rounded-t-lg transition-all hover:scale-y-110"
                    style={{ height: `${h}%` }}
                  />
                ))}
              </div>
              
              {/* Stats */}
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: 'Revenue', value: '$124K', change: '+12%' },
                  { label: 'Users', value: '8,549', change: '+8%' },
                  { label: 'Growth', value: '23%', change: '+5%' },
                ].map(stat => (
                  <div key={stat.label} className="text-center p-3 bg-gray-50 rounded-xl">
                    <p className="text-xs text-gray-500">{stat.label}</p>
                    <p className="text-lg font-bold text-gray-900">{stat.value}</p>
                    <p className="text-xs text-green-600">{stat.change}</p>
                  </div>
                ))}
              </div>
            </div>
          </TiltCard3D>
          
          {/* Floating elements */}
          <div className="absolute top-10 right-10 animate-bounce">
            <div className="bg-white rounded-xl shadow-lg px-4 py-2 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-sm font-medium">Design saved!</span>
            </div>
          </div>
          <div className="absolute bottom-20 left-10 animate-bounce delay-500">
            <div className="bg-white rounded-xl shadow-lg px-4 py-2 flex items-center gap-2">
              <div className="w-6 h-6 bg-gradient-to-br from-violet-500 to-rose-500 rounded-full flex items-center justify-center text-white text-xs">
                ✓
              </div>
              <span className="text-sm font-medium">Export ready</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

// 3D Tilt Component
const TiltCard3D = ({ children, className }) => {
  const ref = useRef(null)
  
  useEffect(() => {
    const card = ref.current
    if (!card) return
    
    const handleMouseMove = (e) => {
      const rect = card.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      const centerX = rect.width / 2
      const centerY = rect.height / 2
      
      const rotateX = (y - centerY) / centerY * -15
      const rotateY = (x - centerX) / centerX * 15
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
    }
    
    const handleMouseLeave = () => {
      card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)'
    }
    
    card.addEventListener('mousemove', handleMouseMove)
    card.addEventListener('mouseleave', handleMouseLeave)
    
    return () => {
      card.removeEventListener('mousemove', handleMouseMove)
      card.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [])
  
  return (
    <div 
      ref={ref}
      className={`transition-transform duration-200 ease-out ${className}`}
    >
      {children}
    </div>
  )
}
```

## Hero Variation 3: Animated Typography

```tsx
// ✅ ANIMATED TYPOGRAPHY HERO
const HeroAnimatedType = () => (
  <section className="relative min-h-screen bg-gray-950 overflow-hidden flex items-center justify-center">
    {/* Animated grid background */}
    <div className="absolute inset-0">
      <div 
        className="absolute inset-0 opacity-20"
        style={{
          backgroundImage: `
            linear-gradient(to right, #ffffff08 1px, transparent 1px),
            linear-gradient(to bottom, #ffffff08 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px'
        }}
      />
      {/* Floating orbs */}
      <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-float-delayed" />
    </div>
    
    {/* Content */}
    <div className="relative z-10 text-center px-4 max-w-5xl mx-auto">
      {/* Animated eyebrow */}
      <div className="overflow-hidden mb-6">
        <p className="text-sm md:text-base font-medium tracking-widest uppercase text-blue-400 animate-reveal">
          Welcome to the future
        </p>
      </div>
      
      {/* Animated headline */}
      <h1 className="text-6xl md:text-8xl font-black text-white mb-6 leading-none">
        <span className="block overflow-hidden">
          <span className="block animate-slide-up">We build</span>
        </span>
        <span className="block overflow-hidden">
          <span 
            className="block bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 animate-slide-up delay-100"
          >
            digital products
          </span>
        </span>
        <span className="block overflow-hidden">
          <span className="block animate-slide-up delay-200">that matter</span>
        </span>
      </h1>
      
      {/* Subheadline */}
      <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-12 animate-fade-in delay-500">
        We combine strategy, design, and engineering to create products that 
        transform businesses and delight users.
      </p>
      
      {/* CTA buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in delay-700">
        <button className="group relative px-8 py-4 bg-white text-gray-900 rounded-full font-semibold overflow-hidden">
          <span className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500 opacity-0 group-hover:opacity-100 transition-opacity" />
          <span className="relative flex items-center gap-2">
            Start Your Project
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </span>
        </button>
        <button className="group px-8 py-4 text-white rounded-full font-semibold border border-white/20 hover:bg-white/10 transition-colors">
          View Our Work
        </button>
      </div>
      
      {/* Stats */}
      <div className="mt-20 grid grid-cols-3 gap-8 animate-fade-in delay-1000">
        {[
          { number: '150+', label: 'Projects Delivered' },
          { number: '$2.5B', label: 'Client Revenue' },
          { number: '98%', label: 'Client Satisfaction' },
        ].map((stat, i) => (
          <div key={i} className="text-center">
            <p className="text-3xl md:text-4xl font-bold text-white mb-2">{stat.number}</p>
            <p className="text-sm text-gray-500">{stat.label}</p>
          </div>
        ))}
      </div>
    </div>
    
    {/* Scroll indicator */}
    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
      <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
        <div className="w-1 h-3 bg-white/50 rounded-full animate-scroll" />
      </div>
    </div>
    
    <style>{`
      @keyframes slide-up {
        from { transform: translateY(100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }
      @keyframes fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes scroll {
        0%, 100% { transform: translateY(0); opacity: 1; }
        50% { transform: translateY(8px); opacity: 0.3; }
      }
      .animate-slide-up { animation: slide-up 0.8s ease-out forwards; }
      .animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
      .animate-scroll { animation: scroll 1.5s ease-in-out infinite; }
      .delay-100 { animation-delay: 0.1s; }
      .delay-200 { animation-delay: 0.2s; }
      .delay-500 { animation-delay: 0.5s; }
      .delay-700 { animation-delay: 0.7s; }
      .delay-1000 { animation-delay: 1s; }
    `}</style>
  </section>
)
```

## Hero Variation 4: Bento Grid

```tsx
// ✅ BENTO GRID HERO
const HeroBentoGrid = () => (
  <section className="relative py-24 px-4 bg-gradient-to-b from-gray-50 to-white">
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center mb-16">
        <span className="inline-block px-4 py-1 rounded-full bg-blue-50 text-blue-600 text-sm font-medium mb-4">
          Simple, transparent pricing
        </span>
        <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Everything you need
        </h2>
        <p className="text-lg text-gray-600 max-w-xl mx-auto">
          Choose the plan that fits your team. All plans include a 14-day free trial.
        </p>
      </div>
      
      {/* Bento Grid */}
      <div className="grid md:grid-cols-4 gap-6 auto-rows-[200px]">
        {/* Large Feature Card */}
        <div className="md:col-span-2 md:row-span-2 bg-gradient-to-br from-violet-500 to-purple-600 rounded-3xl p-8 text-white relative overflow-hidden group">
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors" />
          <Sparkles className="w-10 h-10 mb-4" />
          <h3 className="text-2xl font-bold mb-2">AI-Powered Tools</h3>
          <p className="text-white/80 mb-6">
            Let AI handle the repetitive tasks while you focus on what matters.
          </p>
          <div className="absolute bottom-8 right-8">
            <div className="flex gap-2">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                🤖
              </div>
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                ⚡
              </div>
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-2xl">
                🎯
              </div>
            </div>
          </div>
        </div>
        
        {/* Stats Card */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-start justify-between mb-4">
            <TrendingUp className="w-8 h-8 text-green-500" />
            <span className="text-xs text-green-600 font-medium bg-green-50 px-2 py-1 rounded-full">
              +24%
            </span>
          </div>
          <p className="text-3xl font-bold text-gray-900 mb-1">$45.2K</p>
          <p className="text-sm text-gray-500">Revenue this month</p>
          {/* Mini chart */}
          <svg className="w-full h-12 mt-4" viewBox="0 0 100 40">
            <path 
              d="M0 35 Q 20 30 35 25 T 70 20 T 100 10" 
              fill="none" 
              stroke="#22c55e" 
              strokeWidth="2"
            />
            <path 
              d="M0 35 Q 20 30 35 25 T 70 20 T 100 10 V 40 H 0 Z" 
              fill="url(#greenGradient)" 
            />
            <defs>
              <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#22c55e" stopOpacity="0.2" />
                <stop offset="100%" stopColor="#22c55e" stopOpacity="0" />
              </linearGradient>
            </defs>
          </svg>
        </div>
        
        {/* User Card */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <img 
              src="https://i.pravatar.cc/100?img=1" 
              alt="User" 
              className="w-12 h-12 rounded-full"
            />
            <div>
              <p className="font-medium text-gray-900">Sarah Chen</p>
              <p className="text-sm text-gray-500">Product Designer</p>
            </div>
          </div>
          <p className="text-sm text-gray-600 italic">
            "This tool has completely transformed how our team works together."
          </p>
        </div>
        
        {/* Feature Cards */}
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-orange-100 rounded-xl flex items-center justify-center">
              <Zap className="w-5 h-5 text-orange-500" />
            </div>
            <span className="font-medium text-gray-900">Lightning Fast</span>
          </div>
          <p className="text-sm text-gray-600">10x faster than traditional tools</p>
        </div>
        
        <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col justify-between">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
              <Shield className="w-5 h-5 text-blue-500" />
            </div>
            <span className="font-medium text-gray-900">Secure</span>
          </div>
          <p className="text-sm text-gray-600">Enterprise-grade security</p>
        </div>
        
        {/* Wide Feature */}
        <div className="md:col-span-2 bg-white rounded-3xl p-6 border border-gray-100 shadow-sm flex items-center gap-6">
          <div className="flex-1">
            <h4 className="font-semibold text-gray-900 mb-2">Real-time Collaboration</h4>
            <p className="text-sm text-gray-600">Work together with your team in real-time, anywhere in the world.</p>
          </div>
          <div className="flex -space-x-3">
            {['👨‍💻', '👩‍💻', '👨‍🎨', '👩‍🔬'].map((emoji, i) => (
              <div key={i} className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-lg border-4 border-white">
                {emoji}
              </div>
            ))}
            <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center text-sm font-medium text-gray-600 border-4 border-white">
              +12
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
)
```

## Hero Variation 5: Video Background

```tsx
// ✅ VIDEO BACKGROUND HERO
const HeroVideoBg = () => (
  <section className="relative min-h-screen overflow-hidden">
    {/* Video Background */}
    <div className="absolute inset-0">
      <video 
        autoPlay 
        loop 
        muted 
        playsInline 
        className="w-full h-full object-cover"
      >
        <source src="/hero-video.mp4" type="video/mp4" />
      </video>
      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/60 to-transparent" />
    </div>
    
    {/* Content */}
    <div className="relative z-10 min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 py-24">
        <div className="max-w-2xl">
          {/* Eyebrow */}
          <div className="flex items-center gap-3 mb-6">
            <div className="h-px w-12 bg-gradient-to-r from-transparent to-white/50" />
            <span className="text-sm font-medium text-white/80 tracking-wider uppercase">
              Introducing Our New Platform
            </span>
          </div>
          
          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
            Create Without
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
              Boundaries
            </span>
          </h1>
          
          {/* Sub */}
          <p className="text-xl text-gray-300 mb-8 leading-relaxed">
            The next generation of creative tools is here. Unleash your imagination 
            and build products that push the limits of what's possible.
          </p>
          
          {/* CTA */}
          <div className="flex flex-wrap gap-4">
            <button className="group px-8 py-4 bg-white text-gray-900 rounded-xl font-semibold hover:bg-gray-100 transition-all flex items-center gap-2">
              Explore Platform
              <Play className="w-5 h-5" />
            </button>
            <button className="group px-8 py-4 rounded-xl font-semibold text-white border border-white/30 hover:bg-white/10 backdrop-blur-sm transition-all flex items-center gap-2">
              <span className="w-10 h-10 rounded-full border-2 border-white/50 flex items-center justify-center group-hover:border-white transition-colors">
                <Play className="w-4 h-4 ml-0.5" />
              </span>
              Watch Trailer
            </button>
          </div>
          
          {/* Logos */}
          <div className="mt-16">
            <p className="text-sm text-gray-400 mb-4">Trusted by innovative teams at</p>
            <div className="flex flex-wrap items-center gap-8 opacity-60">
              {['Vercel', 'Stripe', 'Linear', 'Notion', 'Figma'].map(brand => (
                <span key={brand} className="text-xl font-bold text-white">
                  {brand}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    {/* Scroll */}
    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-10">
      <div className="flex flex-col items-center gap-2 text-white/60">
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <ChevronDown className="w-5 h-5 animate-bounce" />
      </div>
    </div>
  </section>
)
```

## Hero Variation 6: Geometric Shapes

```tsx
// ✅ GEOMETRIC SHAPES HERO
const HeroGeometric = () => (
  <section className="relative min-h-screen bg-gray-900 overflow-hidden">
    {/* Animated geometric shapes */}
    <div className="absolute inset-0 overflow-hidden">
      {/* Circle 1 */}
      <div className="absolute -top-20 -left-20 w-96 h-96">
        <div className="w-full h-full border-2 border-cyan-500/30 rounded-full animate-spin-slow" />
        <div className="absolute inset-8 border-2 border-purple-500/30 rounded-full animate-spin-reverse" />
      </div>
      
      {/* Circle 2 */}
      <div className="absolute -bottom-40 -right-20 w-[600px] h-[600px]">
        <div className="w-full h-full border-2 border-pink-500/20 rounded-full animate-spin-slow" />
      </div>
      
      {/* Squares */}
      <div className="absolute top-1/4 right-1/4 w-32 h-32 border border-yellow-500/20 rotate-45 animate-float" />
      <div className="absolute bottom-1/3 left-1/4 w-24 h-24 border border-blue-500/20 -rotate-12 animate-float-delayed" />
      
      {/* Dots pattern */}
      <div 
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: 'radial-gradient(circle, #fff 1px, transparent 1px)',
          backgroundSize: '30px 30px'
        }}
      />
    </div>
    
    {/* Content */}
    <div className="relative z-10 min-h-screen flex items-center">
      <div className="max-w-7xl mx-auto px-4 py-24 grid lg:grid-cols-2 gap-16 items-center">
        {/* Left */}
        <div className="space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
            </span>
            <span className="text-sm text-white/80">Now in Public Beta</span>
          </div>
          
          {/* Headline */}
          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight">
            Where ideas
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400">
              become reality
            </span>
          </h1>
          
          {/* Sub */}
          <p className="text-lg text-gray-400 leading-relaxed">
            Join thousands of creators who are building the future. 
            Start with a blank canvas and let your imagination guide you.
          </p>
          
          {/* CTA */}
          <div className="flex flex-wrap gap-4">
            <button className="group px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-xl font-semibold hover:opacity-90 transition-opacity">
              <span className="flex items-center gap-2">
                Start Creating
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </span>
            </button>
            <button className="px-8 py-4 text-white font-semibold border border-white/20 rounded-xl hover:bg-white/5 transition-colors">
              View Examples
            </button>
          </div>
          
          {/* Stats */}
          <div className="flex gap-8 pt-8 border-t border-white/10">
            {[
              { value: '100K+', label: 'Creators' },
              { value: '500+', label: 'Templates' },
              { value: '4.9★', label: 'Rating' },
            ].map(stat => (
              <div key={stat.label}>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-sm text-gray-500">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
        
        {/* Right: Abstract visual */}
        <div className="relative aspect-square">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-full blur-3xl" />
          
          {/* Central shape */}
          <div className="absolute inset-8 flex items-center justify-center">
            <div className="relative w-64 h-64">
              {/* Rotating border */}
              <div className="absolute inset-0 border-2 border-dashed border-cyan-500/50 rounded-full animate-spin-slow" />
              
              {/* Inner shapes */}
              <div className="absolute inset-4 bg-gradient-to-br from-gray-800 to-gray-900 rounded-3xl shadow-2xl flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-cyan-400 to-purple-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-white" />
                  </div>
                  <p className="text-white font-semibold">Start Here</p>
                </div>
              </div>
              
              {/* Orbiting elements */}
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 bg-yellow-500 rounded-full shadow-lg shadow-yellow-500/50 animate-orbit" />
              <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 w-6 h-6 bg-pink-500 rounded-full shadow-lg shadow-pink-500/50 animate-orbit-reverse" />
              <div className="absolute top-1/2 -left-4 -translate-y-1/2 w-5 h-5 bg-blue-500 rounded-full shadow-lg shadow-blue-500/50 animate-orbit" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <style>{`
      @keyframes spin-slow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
      }
      @keyframes spin-reverse {
        from { transform: rotate(360deg); }
        to { transform: rotate(0deg); }
      }
      @keyframes orbit {
        from { transform: rotate(0deg) translateX(140px) rotate(0deg); }
        to { transform: rotate(360deg) translateX(140px) rotate(-360deg); }
      }
      .animate-spin-slow { animation: spin-slow 20s linear infinite; }
      .animate-spin-reverse { animation: spin-reverse 15s linear infinite; }
      .animate-orbit { animation: orbit 8s linear infinite; }
      .animate-orbit-reverse { animation: orbit 6s linear infinite reverse; }
    `}</style>
  </section>
)
```

## Hero Variation 7: Minimalist Clean

```tsx
// ✅ MINIMALIST CLEAN HERO
const HeroMinimalist = () => (
  <section className="relative py-32 bg-stone-50">
    <div className="max-w-6xl mx-auto px-4">
      <div className="grid lg:grid-cols-2 gap-16 items-center">
        {/* Left: Text */}
        <div className="space-y-8">
          <div>
            <p className="text-sm font-medium text-stone-500 tracking-wider uppercase mb-4">
              Est. 2024
            </p>
            <h1 className="text-5xl md:text-6xl font-bold text-stone-900 leading-[1.1] mb-6">
              Thoughtfully
              <br />
              <span className="text-stone-400">crafted</span>
              <br />
              for you
            </h1>
          </div>
          
          <p className="text-lg text-stone-600 leading-relaxed max-w-md">
            We believe in the power of simplicity. Every detail is considered, 
            every element has purpose. This is design without compromise.
          </p>
          
          <div className="flex items-center gap-4">
            <button className="px-6 py-3 bg-stone-900 text-white rounded-full font-medium hover:bg-stone-800 transition-colors">
              Explore Collection
            </button>
            <button className="flex items-center gap-2 text-stone-600 hover:text-stone-900 transition-colors">
              <span>Watch story</span>
              <Play className="w-4 h-4" />
            </button>
          </div>
        </div>
        
        {/* Right: Image Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-4">
            <div className="aspect-[4/5] bg-stone-200 rounded-2xl overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400" 
                alt="Art 1"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          <div className="space-y-4 pt-8">
            <div className="aspect-[3/4] bg-stone-300 rounded-2xl overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=400" 
                alt="Art 2"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
      
      {/* Bottom strip */}
      <div className="mt-24 pt-12 border-t border-stone-200 flex flex-wrap justify-between items-center gap-8">
        <div className="flex items-center gap-8">
          <div>
            <p className="text-3xl font-bold text-stone-900">12</p>
            <p className="text-sm text-stone-500">Collections</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-stone-900">48</p>
            <p className="text-sm text-stone-500">Products</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-stone-900">∞</p>
            <p className="text-sm text-stone-500">Possibilities</p>
          </div>
        </div>
        <div className="flex -space-x-2">
          {[1, 2, 3, 4, 5].map(i => (
            <img 
              key={i}
              src={`https://i.pravatar.cc/100?img=${i + 10}`}
              alt="Customer"
              className="w-10 h-10 rounded-full border-2 border-stone-50"
            />
          ))}
        </div>
      </div>
    </div>
  </section>
)
```

## Common Animation Keyframes

```css
/* Add to your global CSS or tailwind.config.js */

/* Float animation */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}
.animate-float { animation: float 6s ease-in-out infinite; }
.animate-float-delayed { animation: float 6s ease-in-out 2s infinite; }
.animate-float-delayed-more { animation: float 6s ease-in-out 4s infinite; }

/* Spin slow */
@keyframes spin-slow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin-slow { animation: spin-slow 20s linear infinite; }
.animate-spin-reverse { animation: spin-slow 15s linear infinite reverse; }

/* Bounce */
.animate-bounce { animation: bounce 2s ease-in-out infinite; }

/* Pulse glow */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.3); }
  50% { box-shadow: 0 0 40px rgba(59, 130, 246, 0.6); }
}
.animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
```

## Design Principles

| Principle | Do | Don't |
|-----------|-----|-------|
| **Background** | Gradient mesh, animated shapes | Generic stock photo |
| **Typography** | Bold headlines, gradient text | Centered everything |
| **Visuals** | 3D mockups, floating elements | Generic illustrations |
| **Colors** | Single accent, dark mode | Rainbow, purple-everything |
| **Layout** | Asymmetric, split | Always centered hero |
| **Motion** | Subtle, purposeful | Excessive, distracting |
| **Social Proof** | Real stats, real avatars | Fake numbers |

## Checklist - Hero Quality

- [ ] No gradient purple/blue mesh background
- [ ] No centered everything layout
- [ ] No Inter font (use Geist, Satoshi, etc.)
- [ ] No generic CTA buttons
- [ ] No fake stock photo backgrounds
- [ ] No excessive animations
- [ ] No glassmorphism everywhere
- [ ] Distinctive headline (not "We help you...")
- [ ] Real social proof with names
- [ ] Mobile responsive
- [ ] Fast loading (optimized images/video)
- [ ] Accessible contrast ratios
