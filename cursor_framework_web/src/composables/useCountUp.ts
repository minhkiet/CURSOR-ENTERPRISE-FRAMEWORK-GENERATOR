import { ref, onMounted, onUnmounted } from 'vue'

interface UseCountUpOptions {
  end: number
  duration?: number
  start?: number
  decimals?: number
}

/**
 * Animate a numeric value from `start` to `end` when the element is in view.
 * Respects prefers-reduced-motion.
 */
export function useCountUp(options: UseCountUpOptions) {
  const {
    end,
    duration = 1600,
    start = 0,
    decimals = 0
  } = options

  const current = ref(start)
  const elRef = ref<HTMLElement | null>(null)
  const reduceMotion = typeof window !== 'undefined'
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
    : false

  let observer: IntersectionObserver | null = null
  let rafId: number | null = null
  let hasRun = false

  function format(value: number): string {
    return value.toFixed(decimals)
  }

  function animate() {
    if (reduceMotion) {
      current.value = end
      return
    }

    const startTime = performance.now()
    const ease = (t: number): number => 1 - Math.pow(1 - t, 4)

    function step(now: number) {
      const elapsed = now - startTime
      const progress = Math.min(elapsed / duration, 1)
      current.value = start + (end - start) * ease(progress)
      if (progress < 1) {
        rafId = requestAnimationFrame(step)
      }
    }

    rafId = requestAnimationFrame(step)
  }

  onMounted(() => {
    if (reduceMotion) {
      current.value = end
      return
    }

    if (!elRef.value) return

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasRun) {
            hasRun = true
            animate()
            observer?.disconnect()
          }
        })
      },
      { threshold: 0.4 }
    )

    observer.observe(elRef.value)
  })

  onUnmounted(() => {
    if (rafId !== null) cancelAnimationFrame(rafId)
    observer?.disconnect()
  })

  return {
    elRef,
    value: current,
    display: () => format(current.value)
  }
}