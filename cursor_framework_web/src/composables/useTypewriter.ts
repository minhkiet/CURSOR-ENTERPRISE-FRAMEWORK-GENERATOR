import { ref, onMounted, onUnmounted } from 'vue'

interface UseTypewriterOptions {
  text: string
  speed?: number
  startDelay?: number
  enabled?: boolean
}

/**
 * Type out text character-by-character with optional cursor.
 * Respects prefers-reduced-motion (renders full text instantly).
 */
export function useTypewriter(options: UseTypewriterOptions) {
  const { text, speed = 18, startDelay = 200 } = options
  const displayed = ref('')
  const isTyping = ref(false)
  const isDone = ref(false)
  const reduceMotion = ref(false)

  let observer: IntersectionObserver | null = null
  let timeoutId: number | null = null
  let hasRun = false
  const elRef = ref<HTMLElement | null>(null)

  function start() {
    if (reduceMotion.value) {
      displayed.value = text
      isDone.value = true
      return
    }

    isTyping.value = true
    let i = 0
    function tick() {
      if (i < text.length) {
        displayed.value = text.slice(0, i + 1)
        i += 1
        timeoutId = window.setTimeout(tick, speed)
      } else {
        isTyping.value = false
        isDone.value = true
      }
    }
    timeoutId = window.setTimeout(tick, startDelay)
  }

  onMounted(() => {
    reduceMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (reduceMotion.value) {
      start()
      return
    }

    if (!elRef.value) {
      start()
      return
    }

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasRun) {
            hasRun = true
            start()
            observer?.disconnect()
          }
        })
      },
      { threshold: 0.4 }
    )

    observer.observe(elRef.value)
  })

  onUnmounted(() => {
    if (timeoutId !== null) clearTimeout(timeoutId)
    observer?.disconnect()
  })

  return {
    elRef,
    displayed,
    isTyping,
    isDone
  }
}