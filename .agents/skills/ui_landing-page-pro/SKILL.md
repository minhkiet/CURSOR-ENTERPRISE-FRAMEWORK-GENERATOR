---
name: landing-page-pro
description: "Professional Landing Page Skill cho SaaS, Products, E-commerce. Sections: Hero, Features, Products, Pricing, Blog, Contact, Auth. 3D effects, smooth animations, SEO content, image generation integration. Anti-AI-slop, distinctive design."
---

# Landing Page Pro Skill

Build distinctive, conversion-focused landing pages that don't look AI-generated.

## 1. Landing Page Architecture

### 1.1 Section Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│ LANDING PAGE SECTIONS                                            │
├─────────────────────────────────────────────────────────────────┤
│ 1. Navigation (Sticky)     │ Header, Menu, CTA                │
│ 2. Hero                   │ Headline, Subhead, CTA, Visual    │
│ 3. Social Proof           │ Logos, Stats, Testimonials        │
│ 4. Problem/Solution       │ Pain points, How it works         │
│ 5. Features               │ Benefits, Capabilities            │
│ 6. Product Showcase       │ Demo, Gallery, Before/After       │
│ 7. Pricing                │ Plans, Comparison, FAQ            │
│ 8. Testimonials           │ Reviews, Case studies              │
│ 9. Blog/Resources        │ Posts, Guides, Downloads           │
│ 10. CTA Section           │ Final conversion push              │
│ 11. Contact/Forms         │ Lead capture, Support             │
│ 12. Footer               │ Links, Social, Legal               │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 SaaS Landing Sections

```
┌─────────────────────────────────────────────────────────────────┐
│ SaaS LANDING                                                     │
├─────────────────────────────────────────────────────────────────┤
│ • Hero with product demo/video                                   │
│ • Feature highlights (3-4 key)                                  │
│ • How it works (3 steps)                                         │
│ • Testimonials with avatars                                      │
│ • Pricing tiers (3-4 plans)                                      │
│ • FAQ accordion                                                 │
│ • Final CTA with urgency                                         │
│ • Footer with links                                             │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 E-commerce Landing Sections

```
┌─────────────────────────────────────────────────────────────────┐
│ E-COMMERCE LANDING                                               │
├─────────────────────────────────────────────────────────────────┤
│ • Hero with featured product/collection                          │
│ • Best sellers carousel                                          │
│ • Category cards with images                                     │
│ • New arrivals grid                                             │
│ • Promotion banner (ticker/banner)                               │
│ • Featured collection                                           │
│ • Trust badges                                                 │
│ • Newsletter signup                                             │
│ • Instagram/Social feed                                          │
│ • Footer with links                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Navigation

```tsx
// ✅ NAVIGATION SPECIFICATION
const Navigation = () => (
  <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between h-16">
        {/* Logo */}
        <Logo />
        
        {/* Desktop Menu */}
        <div className="hidden md:flex items-center gap-8">
          <NavLink href="/features">Features</NavLink>
          <NavLink href="/pricing">Pricing</NavLink>
          <NavLink href="/blog">Blog</NavLink>
          <NavLink href="/about">About</NavLink>
        </div>
        
        {/* Auth & CTA */}
        <div className="flex items-center gap-4">
          <Button variant="ghost">Sign in</Button>
          <Button variant="primary">Get Started</Button>
        </div>
        
        {/* Mobile Menu */}
        <MobileMenu />
      </div>
    </div>
  </nav>
)
```

### 2.2 Hero Section

For more hero variations and 3D effects, see:
- [HERO-SECTIONS.md](./HERO-SECTIONS.md) - 7 distinctive hero variations
- [3D-EFFECTS.md](./3D-EFFECTS.md) - Complete 3D image effects library

```tsx
// ✅ HERO SPECIFICATION
const Hero = ({ headline, subheadline, ctas, visual }) => (
  <section className="relative min-h-[90vh] flex items-center overflow-hidden">
    {/* Background */}
    <div className="absolute inset-0 bg-gradient-to-br from-gray-50 via-white to-blue-50" />

    {/* Abstract shapes */}
    <div className="absolute top-20 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
    <div className="absolute bottom-20 left-0 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl" />
    
    <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div className="grid lg:grid-cols-2 gap-12 items-center">
        {/* Content */}
        <div className="space-y-8">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900">
            {headline}
          </h1>
          <p className="text-xl text-gray-600 max-w-xl">
            {subheadline}
          </p>
          
          {/* CTAs */}
          <div className="flex flex-wrap gap-4">
            {ctas.map((cta, i) => (
              <Button key={i} variant={i === 0 ? 'primary' : 'outline'} size="lg">
                {cta.text}
              </Button>
            ))}
          </div>
          
          {/* Social proof */}
          <div className="flex items-center gap-4 pt-4">
            <div className="flex -space-x-3">
              {[...avatars].map((src, i) => (
                <img key={i} src={src} className="w-10 h-10 rounded-full border-2 border-white" />
              ))}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">2,500+ teams</p>
              <p className="text-sm text-gray-500">trust our platform</p>
            </div>
          </div>
        </div>
        
        {/* Visual */}
        <div className="relative">
          {visual}
          {/* Floating elements */}
          <div className="absolute -top-4 -right-4 p-4 bg-white rounded-xl shadow-lg animate-float" />
          <div className="absolute -bottom-4 -left-4 p-4 bg-white rounded-xl shadow-lg animate-float-delayed" />
        </div>
      </div>
    </div>
  </section>
)
```

### 2.3 Feature Cards

```tsx
// ✅ FEATURE CARD SPECIFICATION
const FeatureCard = ({ icon, title, description }) => (
  <div className="group p-6 bg-white rounded-2xl border border-gray-200 hover:border-gray-300 hover:shadow-lg transition-all duration-300">
    {/* Icon */}
    <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-100 transition-colors">
      {icon}
    </div>
    
    {/* Title */}
    <h3 className="text-lg font-semibold text-gray-900 mb-2">
      {title}
    </h3>
    
    {/* Description */}
    <p className="text-gray-600 leading-relaxed">
      {description}
    </p>
  </div>
)

// Usage with 3D tilt effect
const FeatureWithTilt = ({ feature }) => (
  <TiltCard className="preserve-3d">
    <FeatureCard {...feature} />
  </TiltCard>
)
```

### 2.4 Product Card

```tsx
// ✅ PRODUCT CARD SPECIFICATION
const ProductCard = ({ product }) => (
  <article className="group">
    {/* Image */}
    <div className="relative aspect-[4/5] bg-gray-100 rounded-2xl overflow-hidden mb-4">
      <img 
        src={product.image} 
        alt={product.name}
        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      
      {/* Badges */}
      <div className="absolute top-4 left-4 flex gap-2">
        {product.badge && (
          <span className="px-3 py-1 bg-black text-white text-xs font-medium rounded-full">
            {product.badge}
          </span>
        )}
      </div>
      
      {/* Quick actions */}
      <div className="absolute inset-x-4 bottom-4 flex justify-center opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="flex gap-2">
          <Button variant="secondary" size="sm" icon={<HeartIcon />}>
            Wishlist
          </Button>
          <Button variant="primary" size="sm" icon={<CartIcon />}>
            Add to Cart
          </Button>
        </div>
      </div>
    </div>
    
    {/* Info */}
    <div className="space-y-2">
      <p className="text-sm text-gray-500">{product.category}</p>
      <h3 className="font-semibold text-gray-900">{product.name}</h3>
      <div className="flex items-center gap-2">
        <span className="font-bold text-lg">{product.price}</span>
        {product.originalPrice && (
          <span className="text-sm text-gray-400 line-through">{product.originalPrice}</span>
        )}
      </div>
    </div>
  </article>
)
```

### 2.5 Pricing Card

```tsx
// ✅ PRICING CARD SPECIFICATION
const PricingCard = ({ plan, featured }) => (
  <div className={cn(
    "relative p-8 rounded-2xl border-2 transition-all duration-300",
    featured 
      ? "bg-gray-900 text-white border-gray-900 scale-105 shadow-2xl"
      : "bg-white border-gray-200 hover:border-gray-300"
  )}>
    {featured && (
      <div className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-blue-500 text-white text-sm font-medium rounded-full">
        Most Popular
      </div>
    )}
    
    {/* Plan name */}
    <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
    <p className={cn("text-sm mb-6", featured ? "text-gray-400" : "text-gray-500")}>
      {plan.description}
    </p>
    
    {/* Price */}
    <div className="mb-6">
      <span className="text-4xl font-bold">{plan.price}</span>
      {plan.price !== 'Free' && <span className={cn("text-sm", featured ? "text-gray-400" : "text-gray-500")}>/month</span>}
    </div>
    
    {/* Features */}
    <ul className="space-y-3 mb-8">
      {plan.features.map((feature, i) => (
        <li key={i} className="flex items-center gap-3">
          <CheckIcon className={cn("w-5 h-5", featured ? "text-blue-400" : "text-green-500")} />
          <span className={featured ? "text-gray-300" : "text-gray-600"}>{feature}</span>
        </li>
      ))}
    </ul>
    
    {/* CTA */}
    <Button 
      variant={featured ? "primary" : "outline"} 
      className="w-full"
    >
      {plan.cta}
    </Button>
  </div>
)
```

### 2.6 Testimonial

```tsx
// ✅ TESTIMONIAL SPECIFICATION
const Testimonial = ({ quote, author, role, company, avatar }) => (
  <figure className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
    {/* Quote */}
    <blockquote className="text-lg text-gray-700 mb-6 leading-relaxed">
      "{quote}"
    </blockquote>
    
    {/* Author */}
    <figcaption className="flex items-center gap-4">
      <img 
        src={avatar} 
        alt={author}
        className="w-12 h-12 rounded-full object-cover"
      />
      <div>
        <p className="font-semibold text-gray-900">{author}</p>
        <p className="text-sm text-gray-500">{role}, {company}</p>
      </div>
    </figcaption>
  </figure>
)
```

### 2.7 Contact Form

```tsx
// ✅ CONTACT FORM SPECIFICATION
const ContactForm = () => (
  <form className="space-y-6">
    <div className="grid sm:grid-cols-2 gap-6">
      <Input 
        label="Full name" 
        placeholder="John Doe"
        required 
      />
      <Input 
        label="Email address" 
        type="email"
        placeholder="john@company.com"
        required
      />
    </div>
    
    <Select 
      label="Subject"
      options={[
        { value: 'sales', label: 'Sales Inquiry' },
        { value: 'support', label: 'Technical Support' },
        { value: 'partnership', label: 'Partnership' },
      ]}
      placeholder="Select a subject"
    />
    
    <Textarea 
      label="Message"
      placeholder="Tell us how we can help..."
      rows={5}
      required
    />
    
    <Button type="submit" variant="primary" className="w-full">
      Send Message
    </Button>
    
    <p className="text-sm text-gray-500 text-center">
      We typically respond within 24 hours
    </p>
  </form>
)
```

### 2.8 Auth Forms (Login/Register)

```tsx
// ✅ LOGIN FORM SPECIFICATION
const LoginForm = () => (
  <div className="space-y-6">
    {/* Social Login */}
    <div className="grid grid-cols-2 gap-4">
      <Button variant="outline" icon={<GoogleIcon />}>
        Google
      </Button>
      <Button variant="outline" icon={<GithubIcon />}>
        GitHub
      </Button>
    </div>
    
    <div className="relative">
      <div className="absolute inset-0 flex items-center">
        <div className="w-full border-t border-gray-200" />
      </div>
      <div className="relative flex justify-center">
        <span className="px-4 bg-white text-sm text-gray-500">or continue with</span>
      </div>
    </div>
    
    {/* Email/Password */}
    <div className="space-y-4">
      <Input 
        label="Email"
        type="email"
        placeholder="you@example.com"
      />
      <div className="relative">
        <Input 
          label="Password"
          type={showPassword ? 'text' : 'password'}
          placeholder="Enter password"
        />
        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="absolute right-3 top-9 text-gray-400 hover:text-gray-600"
        >
          {showPassword ? <EyeOffIcon /> : <EyeIcon />}
        </button>
      </div>
    </div>
    
    {/* Remember & Forgot */}
    <div className="flex items-center justify-between">
      <label className="flex items-center gap-2">
        <Checkbox />
        <span className="text-sm text-gray-600">Remember me</span>
      </label>
      <Link href="/forgot-password" className="text-sm text-blue-600 hover:text-blue-700">
        Forgot password?
      </Link>
    </div>
    
    <Button type="submit" variant="primary" className="w-full">
      Sign in
    </Button>
    
    <p className="text-center text-sm text-gray-600">
      Don't have an account? <Link href="/register" className="text-blue-600 hover:text-blue-700 font-medium">Sign up</Link>
    </p>
  </div>
)
```

---

## 3. Animation System

### 3.1 Animation Presets

```css
/* Landing Page Animations */
:root {
  /* Timing */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --duration-slower: 700ms;
  
  /* Easing */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Fade In Up */
.animate-fade-in-up {
  animation: fadeInUp 0.6s var(--ease-out) forwards;
}

/* Float */
.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float 6s ease-in-out 2s infinite;
}

/* Scale In */
.animate-scale-in {
  animation: scaleIn 0.4s var(--ease-out) forwards;
}

/* Slide In */
.animate-slide-in-left {
  animation: slideInLeft 0.6s var(--ease-out) forwards;
}
```

### 3.2 Scroll Animations

```tsx
// ✅ SCROLL ANIMATION WRAPPER
const ScrollReveal = ({ children, delay = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 30 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-100px" }}
    transition={{ duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] }}
  >
    {children}
  </motion.div>
)

// Usage
<ScrollReveal delay={0.1}>
  <FeatureCard {...feature} />
</ScrollReveal>
```

### 3.3 3D Effects

```tsx
// ✅ 3D TILT CARD
const TiltCard = ({ children, className, tiltIntensity = 10 }) => {
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
      
      const rotateX = (y - centerY) / centerY * -tiltIntensity
      const rotateY = (x - centerX) / centerX * tiltIntensity
      
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`
    }
    
    const handleMouseLeave = () => {
      card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)'
    }
    
    card.addEventListener('mousemove', handleMouseMove)
    card.addEventListener('mouseleave', handleMouseLeave)
    
    return () => {
      card.removeEventListener('mousemove', handleMouseMove)
      card.removeEventListener('mouseleave', handleMouseLeave)
    }
  }, [tiltIntensity])
  
  return <div ref={ref} className={cn('transition-transform duration-200', className)}>{children}</div>
}
```

### 3.4 Parallax Effects

```tsx
// ✅ PARALLAX SECTION
const ParallaxSection = ({ background, children }) => (
  <section className="relative overflow-hidden">
    <div 
      className="absolute inset-0 bg-cover bg-center"
      style={{ 
        backgroundImage: `url(${background})`,
        transform: `translateY(${scrollY * 0.5}px)`
      }}
    />
    <div className="relative z-10">
      {children}
    </div>
  </section>
)
```

---

## 4. Image Generation

### 4.1 Image Prompt Template

```markdown
## IMAGE PROMPT TEMPLATE

### Hero Images
```
[Aerial/top-down] view of [specific scene] with [specific lighting], 
[specific color palette], [specific mood], ultra-detailed, 8K, 
photorealistic, professional photography
```

### Product Images
```
[Product name] on [surface] with [background elements], 
[specific angle], studio lighting, [specific style], 
commercial photography, high resolution
```

### Background Images
```
[Scene type] with [mood], [color temperature], 
[depth of field], [texture], seamless, [purpose: hero/gradient/texture]
```

### Section Images
```
[Concept visualization] of [subject], minimal composition, 
[color scheme], modern aesthetic, [style: flat/illustrated/photographic]
```
```

### 4.2 Image Sourcing Priority

```tsx
// Priority order for images
const ImageSource = {
  // 1. Generated with AI (for specific, contextual images)
  // Use: Flux, Midjourney, DALL-E, Stable Diffusion
  
  // 2. Real photography (for authentic, emotional connection)
  // Use: Unsplash, Pexels with specific search terms
  
  // 3. Custom illustrations (for unique, brand-aligned visuals)
  // Use: Custom SVG, illustration style matching brand
  
  // 4. Stock with customization (if real images unavailable)
  // Use: Edit, composite, add brand elements
  
  // NEVER: Generic stock photos of people smiling at laptops
  // NEVER: Obvious AI-generated looking images
}
```

### 4.3 Background Patterns

```css
/* Landing Page Backgrounds */
.bg-grid-pattern {
  background-image: 
    linear-gradient(to right, #e5e7eb 1px, transparent 1px),
    linear-gradient(to bottom, #e5e7eb 1px, transparent 1px);
  background-size: 40px 40px;
}

.bg-dots-pattern {
  background-image: radial-gradient(#d1d5db 1px, transparent 1px);
  background-size: 20px 20px;
}

.bg-gradient-mesh {
  background: 
    radial-gradient(at 40% 20%, hsla(210, 100%, 50%, 0.1) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsla(180, 100%, 50%, 0.08) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsla(280, 100%, 50%, 0.1) 0px, transparent 50%);
}
```

---

## 5. SEO Optimization

### 5.1 Page Structure

```tsx
// ✅ SEO STRUCTURE
const SEOHead = ({ page }) => (
  <head>
    <title>{page.title} | {siteName}</title>
    <meta name="description" content={page.description} />
    
    {/* Open Graph */}
    <meta property="og:title" content={page.title} />
    <meta property="og:description" content={page.description} />
    <meta property="og:image" content={page.image} />
    <meta property="og:type" content="website" />
    
    {/* Twitter */}
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={page.title} />
    <meta name="twitter:description" content={page.description} />
    <meta name="twitter:image" content={page.image} />
    
    {/* Structured Data */}
    <script type="application/ld+json">
      {JSON.stringify(page.structuredData)}
    </script>
  </head>
)
```

### 5.2 Content Guidelines

```tsx
// SEO Content Rules
const SEOContent = {
  // Headlines
  headlineRules: [
    "H1: One per page, 50-60 characters, includes primary keyword",
    "H2: 3-6 per page, 30-60 characters, includes secondary keywords",
    "H3: For subsections, 20-40 characters",
  ],
  
  // Meta descriptions
  metaRules: [
    "150-160 characters",
    "Include primary keyword early",
    "Include value proposition",
    "End with a call-to-action or period",
  ],
  
  // Content length
  contentLength: {
    hero: "20-30 words headline, 50-100 words subheadline",
    feature: "2-3 sentences per feature",
    pricing: "20-30 words per plan description",
    testimonial: "50-150 words quote",
    blog: "1500-2500 words (search intent dependent)",
  },
  
  // Keywords
  keywordDensity: {
    primary: "1-2% (once per 100 words)",
    secondary: "2-4 occurrences per page",
    avoid: " keyword stuffing - write for humans first",
  }
}
```

### 5.3 Blog Post Template

```tsx
// ✅ BLOG POST STRUCTURE
const BlogPost = ({ post }) => (
  <article className="max-w-3xl mx-auto">
    {/* Header */}
    <header className="mb-12">
      <div className="flex items-center gap-4 mb-4">
        <Badge>{post.category}</Badge>
        <time className="text-sm text-gray-500">{post.date}</time>
        <span className="text-sm text-gray-500">{post.readTime} min read</span>
      </div>
      <h1 className="text-4xl font-bold text-gray-900 mb-6">
        {post.title}
      </h1>
      {/* Author */}
      <div className="flex items-center gap-4">
        <img src={post.author.avatar} className="w-12 h-12 rounded-full" />
        <div>
          <p className="font-medium text-gray-900">{post.author.name}</p>
          <p className="text-sm text-gray-500">{post.author.role}</p>
        </div>
      </div>
    </header>
    
    {/* Featured Image */}
    <figure className="mb-12">
      <img 
        src={post.featuredImage} 
        alt={post.title}
        className="w-full aspect-video object-cover rounded-2xl"
      />
    </figure>
    
    {/* Content */}
    <div 
      className="prose prose-lg max-w-none"
      dangerouslySetInnerHTML={{ __html: post.content }}
    />
    
    {/* Share & CTA */}
    <ShareButtons post={post} />
    <NewsletterSignup />
  </article>
)
```

---

## 6. E-commerce Components

### 6.1 Quick Cart

```tsx
// ✅ QUICK CART DRAWER
const CartDrawer = ({ isOpen, onClose }) => (
  <Drawer open={isOpen} onOpenChange={onClose} title="Your Cart">
    <div className="flex flex-col h-full">
      {/* Items */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {cartItems.map(item => (
          <CartItem key={item.id} item={item} />
        ))}
      </div>
      
      {/* Summary */}
      <div className="border-t p-4 space-y-4">
        <div className="flex justify-between text-lg font-bold">
          <span>Subtotal</span>
          <span>${subtotal}</span>
        </div>
        <Button variant="primary" className="w-full" icon={<CartIcon />}>
          Checkout - ${subtotal}
        </Button>
        <Button variant="ghost" className="w-full" onClick={onClose}>
          Continue Shopping
        </Button>
      </div>
    </div>
  </Drawer>
)
```

### 6.2 Quick View Modal

```tsx
// ✅ QUICK VIEW MODAL
const QuickViewModal = ({ product }) => (
  <Dialog>
    <Dialog.Content className="max-w-4xl p-0">
      <div className="grid md:grid-cols-2">
        {/* Image */}
        <div className="aspect-square bg-gray-100">
          <img src={product.images[0]} className="w-full h-full object-cover" />
        </div>
        
        {/* Info */}
        <div className="p-8 space-y-6">
          <div>
            <Badge>{product.category}</Badge>
            <h2 className="text-2xl font-bold mt-2">{product.name}</h2>
          </div>
          
          <div className="text-3xl font-bold">${product.price}</div>
          
          <p className="text-gray-600">{product.shortDescription}</p>
          
          {/* Options */}
          <ProductOptions product={product} />
          
          {/* Actions */}
          <div className="flex gap-4">
            <Button variant="primary" className="flex-1" icon={<CartIcon />}>
              Add to Cart
            </Button>
            <Button variant="outline" icon={<HeartIcon />} />
          </div>
        </div>
      </div>
    </Dialog.Content>
  </Dialog>
)
```

---

## 7. Footer Specification

```tsx
// ✅ FOOTER SPECIFICATION
const Footer = () => (
  <footer className="bg-gray-900 text-gray-300">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-8">
        {/* Brand */}
        <div className="col-span-2">
          <Logo variant="light" />
          <p className="mt-4 text-sm text-gray-400 max-w-xs">
            Building the future of [industry], one product at a time.
          </p>
          <SocialLinks className="mt-6" />
        </div>
        
        {/* Links */}
        {footerLinks.map(group => (
          <div key={group.title}>
            <h4 className="font-semibold text-white mb-4">{group.title}</h4>
            <ul className="space-y-3">
              {group.links.map(link => (
                <li key={link.href}>
                  <Link href={link.href} className="text-sm hover:text-white transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      
      {/* Bottom */}
      <div className="mt-12 pt-8 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p className="text-sm text-gray-500">
          © {new Date().getFullYear()} Company. All rights reserved.
        </p>
        <div className="flex gap-6 text-sm text-gray-500">
          <Link href="/privacy">Privacy Policy</Link>
          <Link href="/terms">Terms of Service</Link>
          <Link href="/cookies">Cookie Policy</Link>
        </div>
      </div>
    </div>
  </footer>
)
```

---

## 8. Design Tokens

### 8.1 Landing Page Colors

```css
/* Landing Page Color System */
:root {
  /* Primary - Blue */
  --primary-50: #eff6ff;
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  
  /* Neutrals - Warm gray */
  --gray-50: #fafaf9;
  --gray-100: #f5f5f4;
  --gray-200: #e7e5e4;
  --gray-900: #1c1917;
  
  /* Accent - Rose (use ONE accent) */
  --accent-500: #f43f5e;
  --accent-600: #e11d48;
  
  /* Gradients (use sparingly) */
  --gradient-hero: linear-gradient(135deg, #eff6ff 0%, #faf5ff 100%);
  --gradient-dark: linear-gradient(135deg, #1f2937 0%, #111827 100%);
}
```

### 8.2 Typography for Landing

```css
/* Landing Page Typography */
.headline-xl {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  font-weight: 800;
}

.headline-lg {
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.2;
  letter-spacing: -0.01em;
  font-weight: 700;
}

.headline-md {
  font-size: clamp(1.5rem, 3vw, 2rem);
  line-height: 1.3;
  font-weight: 600;
}

.body-lg {
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--gray-600);
}
```

---

## 9. Checklist - Landing Page Quality

### Pre-Implementation
- [ ] Design read declared (aesthetic direction)
- [ ] Brand colors selected
- [ ] Typography scale defined
- [ ] Icon library selected
- [ ] Section order planned
- [ ] Image assets sourced/generated

### Content
- [ ] Headline specific, not generic
- [ ] Subheadline explains value
- [ ] CTAs action-oriented
- [ ] SEO meta tags complete
- [ ] Structured data added
- [ ] Blog posts indexed

### Design
- [ ] Anti-slop check passed
- [ ] No gradients滥用
- [ ] Consistent spacing
- [ ] Mobile responsive
- [ ] Animations smooth (60fps)
- [ ] 3D effects optional (tasteful)

### Functionality
- [ ] Forms validate
- [ ] Auth flows complete
- [ ] Cart works
- [ ] Navigation works
- [ ] CTAs trackable
- [ ] Analytics setup

### Performance
- [ ] Images optimized
- [ ] Fonts preloaded
- [ ] CSS minimal
- [ ] JS lazy loaded
- [ ] Core Web Vitals pass

---

## 10. Integration Stack

```
┌─────────────────────────────────────────────────────────────┐
│ LANDING PAGE STACK                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  landing-page-pro (this skill)                              │
│       ↓                                                     │
│  frontend-taste (base design rules)                         │
│       ↓                                                     │
│  hallmark (anti-slop validation)                            │
│       ↓                                                     │
│  ai-copywriter (human copy)                                │
│       ↓                                                     │
│  simple-english (clarity)                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Auto-trigger keywords:
- landing page, homepage, SaaS landing
- product page, e-commerce
- portfolio, launch page
- marketing site, campaign
```
