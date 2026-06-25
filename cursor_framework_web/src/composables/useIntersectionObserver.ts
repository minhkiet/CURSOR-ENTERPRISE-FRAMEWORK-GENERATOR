import { onUnmounted, type Ref } from 'vue'

interface UseIntersectionObserverReturn {
  observe: (
    target: Ref<HTMLElement | null> | HTMLElement | null,
    callback: (entry: IntersectionObserverEntry) => void,
    options?: IntersectionObserverInit
  ) => void
  unobserve: (target: HTMLElement) => void
}

export function useIntersectionObserver(): UseIntersectionObserverReturn {
  let observer: IntersectionObserver | null = null

  function observe(
    target: Ref<HTMLElement | null> | HTMLElement | null,
    callback: (entry: IntersectionObserverEntry) => void,
    options: IntersectionObserverInit = {}
  ): void {
    if (!observer) {
      observer = new IntersectionObserver((entries) => {
        entries.forEach(callback)
      }, options)
    }

    const element = target && 'value' in target ? target.value : target
    if (element) {
      observer.observe(element)
    }
  }

  function unobserve(target: HTMLElement): void {
    if (observer) {
      observer.unobserve(target)
    }
  }

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
  })

  return {
    observe,
    unobserve
  }
}
