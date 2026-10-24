"""
Image Presentation Skill

Provides CSS and JavaScript effects for image presentation including:
- Reveal animations (fade, slide, zoom)
- Gallery layouts (grid, masonry, carousel, slider)
- Lightbox and zoom effects
- Parallax and hover effects
- Before/after comparisons

All effects use native browser APIs and CSS, no external dependencies required.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EffectType(Enum):
    """Types of image presentation effects."""
    REVEAL = "reveal"
    GALLERY = "gallery"
    CAROUSEL = "carousel"
    LIGHTBOX = "lightbox"
    ZOOM = "zoom"
    PARALLAX = "parallax"
    HOVER = "hover"
    MASONRY = "masonry"
    SLIDER = "slider"
    BEFORE_AFTER = "before_after"


class RevealAnimation(Enum):
    """Reveal animation types."""
    FADE_IN = "fade_in"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    BLUR_IN = "blur_in"
    SCALE_IN = "scale_in"


@dataclass
class EffectMetadata:
    """Metadata for an image effect."""
    effect: str
    duration: int = 700  # milliseconds
    delay: int = 100  # milliseconds between items
    easing: str = "ease-out"
    iterations: int = 1
    lazy_loading: bool = True
    responsive: bool = True
    accessibility: bool = True
    prefers_reduced_motion: bool = True


@dataclass
class RevealEffect:
    """Reveal/fade-in animation effect."""
    animation: RevealAnimation = RevealAnimation.FADE_IN
    threshold: float = 0.1  # IntersectionObserver threshold
    once: bool = True  # Animate only once
    metadata: EffectMetadata = field(default_factory=lambda: EffectMetadata(effect="reveal"))
    
    def to_css(self) -> str:
        """Generate CSS for this effect."""
        animations = {
            RevealAnimation.FADE_IN: """
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
.reveal-fade-in {
    opacity: 0;
    animation: fadeIn var(--reveal-duration, 700ms) var(--reveal-easing, ease-out) forwards;
    animation-delay: var(--reveal-delay, 0ms);
}""",
            RevealAnimation.SLIDE_UP: """
@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.reveal-slide-up {
    opacity: 0;
    animation: slideUp var(--reveal-duration, 700ms) var(--reveal-easing, ease-out) forwards;
    animation-delay: var(--reveal-delay, 0ms);
}""",
            RevealAnimation.ZOOM_IN: """
@keyframes zoomIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
.reveal-zoom-in {
    opacity: 0;
    animation: zoomIn var(--reveal-duration, 700ms) var(--reveal-easing, ease-out) forwards;
    animation-delay: var(--reveal-delay, 0ms);
}""",
            RevealAnimation.BLUR_IN: """
@keyframes blurIn {
    from { opacity: 0; filter: blur(10px); }
    to { opacity: 1; filter: blur(0); }
}
.reveal-blur-in {
    opacity: 0;
    animation: blurIn var(--reveal-duration, 700ms) var(--reveal-easing, ease-out) forwards;
    animation-delay: var(--reveal-delay, 0ms);
}""",
        }
        return animations.get(self.animation, animations[RevealAnimation.FADE_IN])
    
    def to_js(self) -> str:
        """Generate JavaScript for IntersectionObserver."""
        return f"""
(function() {{
    const observerOptions = {{
        threshold: {self.threshold},
        rootMargin: '0px 0px -50px 0px'
    }};
    
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                {'entry.target.classList.add("revealed");' if self.once else 'entry.target.style.opacity = "1";'}
                {'observer.unobserve(entry.target);' if self.once else ''}
            }}
        }});
    }}, observerOptions);
    
    document.querySelectorAll('.reveal-fade-in, .reveal-slide-up, .reveal-zoom-in, .reveal-blur-in').forEach(el => {{
        observer.observe(el);
    }});
    
    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
        document.querySelectorAll('.reveal-fade-in, .reveal-slide-up, .reveal-zoom-in, .reveal-blur-in').forEach(el => {{
            el.style.opacity = '1';
            el.style.animation = 'none';
        }});
    }}
}})();
"""


@dataclass  
class LightboxEffect:
    """Lightbox/modal image viewer."""
    show_caption: bool = True
    show_counter: bool = True
    enable_zoom: bool = True
    enable_download: bool = False
    keyboard_navigation: bool = True
    close_on_escape: bool = True
    close_on_backdrop: bool = True
    metadata: EffectMetadata = field(default_factory=lambda: EffectMetadata(effect="lightbox"))
    
    def to_html(self) -> str:
        """Generate lightbox HTML structure."""
        return '''
<div id="lightbox" class="lightbox" aria-hidden="true" role="dialog" aria-modal="true">
    <div class="lightbox-backdrop"></div>
    <button class="lightbox-close" aria-label="Close">&times;</button>
    <button class="lightbox-prev" aria-label="Previous image">&#10094;</button>
    <button class="lightbox-next" aria-label="Next image">&#10095;</button>
    <div class="lightbox-content">
        <img class="lightbox-image" src="" alt="">
        <div class="lightbox-caption"></div>
        <div class="lightbox-counter"></div>
    </div>
</div>
'''
    
    def to_css(self) -> str:
        """Generate lightbox CSS styles."""
        return '''
.lightbox {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease;
}
.lightbox.active {
    opacity: 1;
    visibility: visible;
}
.lightbox-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.95);
    cursor: pointer;
}
.lightbox-content {
    position: relative;
    max-width: 90vw;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.lightbox-image {
    max-width: 100%;
    max-height: calc(90vh - 60px);
    object-fit: contain;
    border-radius: 4px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}
.lightbox-caption {
    color: #fff;
    text-align: center;
    padding: 16px 0 0;
    font-size: 14px;
    max-width: 600px;
}
.lightbox-counter {
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    padding: 8px 0 0;
}
.lightbox-close,
.lightbox-prev,
.lightbox-next {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: #fff;
    cursor: pointer;
    padding: 12px 16px;
    font-size: 24px;
    transition: background 0.2s ease;
    z-index: 10;
}
.lightbox-close:hover,
.lightbox-prev:hover,
.lightbox-next:hover {
    background: rgba(255, 255, 255, 0.2);
}
.lightbox-close { top: 20px; right: 20px; }
.lightbox-prev { left: 20px; top: 50%; transform: translateY(-50%); }
.lightbox-next { right: 20px; top: 50%; transform: translateY(-50%); }
'''

    def to_js(self) -> str:
        """Generate lightbox JavaScript."""
        close = "this.parentElement.classList.remove('active'); this.parentElement.setAttribute('aria-hidden', 'true');"
        return f'''
(function() {{
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;
    
    const img = lightbox.querySelector('.lightbox-image');
    const caption = lightbox.querySelector('.lightbox-caption');
    const counter = lightbox.querySelector('.lightbox-counter');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');
    const backdrop = lightbox.querySelector('.lightbox-backdrop');
    
    let currentIndex = 0;
    let images = [];
    
    function openLightbox(index) {{
        currentIndex = index;
        updateImage();
        lightbox.classList.add('active');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }}
    
    function closeLightbox() {{
        lightbox.classList.remove('active');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }}
    
    function updateImage() {{
        const current = images[currentIndex];
        if (current) {{
            img.src = current.src;
            img.alt = current.alt || '';
            caption.textContent = current.alt || '';
            counter.textContent = `{currentIndex + 1} / {images.length}`;
        }}
    }}
    
    function nextImage() {{
        currentIndex = (currentIndex + 1) % images.length;
        updateImage();
    }}
    
    function prevImage() {{
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateImage();
    }}
    
    // Event listeners
    backdrop.addEventListener('click', closeLightbox);
    closeBtn.addEventListener('click', closeLightbox);
    prevBtn.addEventListener('click', prevImage);
    nextBtn.addEventListener('click', nextImage);
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {{
        if (!lightbox.classList.contains('active')) return;
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') nextImage();
        if (e.key === 'ArrowLeft') prevImage();
    }});
    
    // Initialize with gallery images
    document.querySelectorAll('img[data-lightbox]').forEach((el, i) => {{
        images.push({{ src: el.src, alt: el.alt || el.title || '' }});
        el.style.cursor = 'pointer';
        el.addEventListener('click', () => openLightbox(i));
    }});
    
    window.openLightbox = openLightbox;
}})();
'''


@dataclass
class MasonryLayout:
    """Masonry grid layout."""
    columns: int = 3
    gap: int = 16
    min_column_width: int = 250
    metadata: EffectMetadata = field(default_factory=lambda: EffectMetadata(effect="masonry"))
    
    def to_css(self) -> str:
        """Generate masonry CSS."""
        return f'''
.masonry {{
    column-count: {self.columns};
    column-gap: {self.gap}px;
}}
.masonry-item {{
    break-inside: avoid;
    margin-bottom: {self.gap}px;
}}
.masonry-item img {{
    width: 100%;
    height: auto;
    border-radius: 8px;
    display: block;
}}
@media (max-width: 768px) {{
    .masonry {{ column-count: 2; }}
}}
@media (max-width: 480px) {{
    .masonry {{ column-count: 1; }}
}}
'''

    def to_js(self) -> str:
        """Generate resize handler."""
        return f'''
(function() {{
    const masonry = document.querySelector('.masonry');
    if (!masonry) return;
    
    function updateColumns() {{
        const width = masonry.offsetWidth;
        const columns = Math.max(1, Math.floor(width / {self.min_column_width}));
        masonry.style.columnCount = columns;
    }}
    
    updateColumns();
    window.addEventListener('resize', updateColumns);
}})();
'''


@dataclass
class BeforeAfterComparison:
    """Before/after image comparison slider."""
    show_handle: bool = True
    show_labels: bool = True
    initial_position: float = 0.5
    metadata: EffectMetadata = field(default_factory=lambda: EffectMetadata(effect="before_after"))
    
    def to_html(self, before_src: str, after_src: str, before_label: str = "Before", after_label: str = "After") -> str:
        """Generate comparison HTML."""
        return f'''
<div class="comparison" data-position="{self.initial_position}">
    <div class="comparison-before">
        <img src="{before_src}" alt="{before_label}">
        <span class="comparison-label comparison-label-before">{before_label}</span>
    </div>
    <div class="comparison-after">
        <img src="{after_src}" alt="{after_label}">
        <span class="comparison-label comparison-label-after">{after_label}</span>
    </div>
    <div class="comparison-slider">
        <div class="comparison-line"></div>
        <div class="comparison-handle">&#8644;</div>
    </div>
</div>
'''
    
    def to_css(self) -> str:
        """Generate comparison CSS."""
        return '''
.comparison {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    user-select: none;
    touch-action: none;
}
.comparison-before,
.comparison-after {
    display: block;
}
.comparison-before img,
.comparison-after img {
    display: block;
    width: 100%;
    height: auto;
}
.comparison-after {
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    overflow: hidden;
}
.comparison-slider {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 4px;
    cursor: ew-resize;
}
.comparison-line {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 2px;
    background: #fff;
    transform: translateX(-50%);
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}
.comparison-handle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 40px;
    height: 40px;
    background: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #333;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
.comparison-label {
    position: absolute;
    top: 16px;
    padding: 4px 12px;
    background: rgba(0,0,0,0.7);
    color: #fff;
    font-size: 12px;
    border-radius: 4px;
}
.comparison-label-before { left: 16px; }
.comparison-label-after { right: 16px; }
'''

    def to_js(self) -> str:
        """Generate comparison JavaScript."""
        return '''
(function() {
    const comparisons = document.querySelectorAll('.comparison');
    
    comparisons.forEach(comp => {
        const slider = comp.querySelector('.comparison-slider');
        const after = comp.querySelector('.comparison-after');
        const initialPos = parseFloat(comp.dataset.position || 0.5);
        
        after.style.width = (initialPos * 100) + '%';
        slider.style.left = (initialPos * 100) + '%';
        
        let isDragging = false;
        
        function updatePosition(clientX) {
            const rect = comp.getBoundingClientRect();
            let pos = (clientX - rect.left) / rect.width;
            pos = Math.max(0, Math.min(1, pos));
            after.style.width = (pos * 100) + '%';
            slider.style.left = (pos * 100) + '%';
        }
        
        slider.addEventListener('mousedown', (e) => {
            isDragging = true;
            e.preventDefault();
        });
        
        document.addEventListener('mousemove', (e) => {
            if (isDragging) updatePosition(e.clientX);
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        // Touch support
        slider.addEventListener('touchstart', (e) => {
            isDragging = true;
        });
        
        document.addEventListener('touchmove', (e) => {
            if (isDragging) updatePosition(e.touches[0].clientX);
        });
        
        document.addEventListener('touchend', () => {
            isDragging = false;
        });
    });
})();
'''


@dataclass
class ParallaxEffect:
    """Parallax scroll effect."""
    speed: float = 0.5  # 0-1, lower = slower
    enable_on_mobile: bool = False
    metadata: EffectMetadata = field(default_factory=lambda: EffectMetadata(effect="parallax"))
    
    def to_css(self) -> str:
        """Generate parallax CSS."""
        return f'''
.parallax {{
    position: relative;
    overflow: hidden;
}}
.parallax-bg {{
    position: absolute;
    top: -50%;
    left: 0;
    width: 100%;
    height: 200%;
    object-fit: cover;
    will-change: transform;
}}
@media (prefers-reduced-motion: no-preference) {{
    .parallax-bg {{
        transform: translateY(calc(var(--scroll-y, 0) * {self.speed}));
    }}
}}
'''

    def to_js(self) -> str:
        """Generate parallax scroll handler."""
        return '''
(function() {
    const parallaxElements = document.querySelectorAll('.parallax-bg');
    
    if (parallaxElements.length === 0) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    
    let ticking = false;
    
    function updateParallax() {
        parallaxElements.forEach(el => {
            const rect = el.parentElement.getBoundingClientRect();
            const scrollY = window.scrollY;
            el.style.setProperty('--scroll-y', scrollY + 'px');
        });
        ticking = false;
    }
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });
})();
'''


class ImagePresentationSkill:
    """
    Unified image presentation skill supporting multiple effects.
    
    Provides methods to generate CSS, HTML, and JavaScript for:
    - Reveal animations with IntersectionObserver
    - Lightbox modal viewers
    - Masonry grid layouts
    - Before/after comparisons
    - Parallax scrolling
    - Custom CSS effects
    
    Usage:
        >>> from cursor_framework.skills.image_presentation import ImagePresentationSkill
        >>> skill = ImagePresentationSkill()
        >>> reveal = RevealEffect(animation=RevealAnimation.FADE_IN)
        >>> print(reveal.to_css())
    """
    
    def __init__(self):
        self.effects = {}
    
    def generate_reveal_css(self, animation: RevealAnimation = RevealAnimation.FADE_IN) -> str:
        """Generate CSS for reveal effect."""
        effect = RevealEffect(animation=animation)
        return effect.to_css()
    
    def generate_reveal_js(self, animation: RevealAnimation = RevealAnimation.FADE_IN) -> str:
        """Generate JavaScript for reveal effect."""
        effect = RevealEffect(animation=animation)
        return effect.to_js()
    
    def generate_lightbox_html(self) -> str:
        """Generate lightbox HTML structure."""
        effect = LightboxEffect()
        return effect.to_html()
    
    def generate_lightbox_css(self) -> str:
        """Generate lightbox CSS styles."""
        effect = LightboxEffect()
        return effect.to_css()
    
    def generate_lightbox_js(self) -> str:
        """Generate lightbox JavaScript."""
        effect = LightboxEffect()
        return effect.to_js()
    
    def generate_masonry_css(self, columns: int = 3, gap: int = 16) -> str:
        """Generate masonry layout CSS."""
        effect = MasonryLayout(columns=columns, gap=gap)
        return effect.to_css()
    
    def generate_comparison(
        self,
        before_src: str,
        after_src: str,
        before_label: str = "Before",
        after_label: str = "After"
    ) -> dict:
        """Generate before/after comparison HTML, CSS, and JS."""
        effect = BeforeAfterComparison()
        return {
            "html": effect.to_html(before_src, after_src, before_label, after_label),
            "css": effect.to_css(),
            "js": effect.to_js(),
        }
    
    def generate_parallax_css(self, speed: float = 0.5) -> str:
        """Generate parallax effect CSS."""
        effect = ParallaxEffect(speed=speed)
        return effect.to_css()
    
    def generate_parallax_js(self, speed: float = 0.5) -> str:
        """Generate parallax scroll handler JS."""
        effect = ParallaxEffect(speed=speed)
        return effect.to_js()
    
    def get_metadata(self, effect_type: EffectType) -> EffectMetadata:
        """Get metadata for an effect type."""
        defaults = {
            EffectType.REVEAL: EffectMetadata(effect="reveal", duration=700),
            EffectType.LIGHTBOX: EffectMetadata(effect="lightbox", duration=300),
            EffectType.MASONRY: EffectMetadata(effect="masonry", duration=0),
            EffectType.BEFORE_AFTER: EffectMetadata(effect="before_after", duration=0),
            EffectType.PARALLAX: EffectMetadata(effect="parallax", duration=0),
        }
        return defaults.get(effect_type, EffectMetadata(effect=effect_type.value))
    
    def to_dict(self) -> dict:
        """Convert skill capabilities to dictionary."""
        return {
            "supportedEffects": [e.value for e in EffectType],
            "revealAnimations": [a.value for a in RevealAnimation],
            "features": {
                "lazyLoading": True,
                "responsive": True,
                "accessibility": True,
                "prefersReducedMotion": True,
            },
        }


# Export classes
__all__ = [
    "EffectType",
    "RevealAnimation",
    "EffectMetadata",
    "RevealEffect",
    "LightboxEffect",
    "MasonryLayout",
    "BeforeAfterComparison",
    "ParallaxEffect",
    "ImagePresentationSkill",
]
