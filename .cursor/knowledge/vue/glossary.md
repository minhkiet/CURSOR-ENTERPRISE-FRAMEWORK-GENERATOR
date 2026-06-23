# Vue Glossary - Từ Điển Thuật Ngữ Vue.js

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành Vue.js, framework JavaScript phổ biến cho việc xây dựng giao diện người dùng.

## Các thuật ngữ cơ bản

### 1. Vue Component (Thành Phần Vue)

Vue Component là khối xây dựng cơ bản trong Vue.js, là một instance Vue có thể tái sử dụng. Components có thể chứa template, logic, và styles. Single-File Components (SFC) sử dụng `.vue` extension và chứa template, script, và style trong một file. Components có thể được nested để tạo thành component tree.

Props cho phép truyền data từ parent xuống child. Events cho phép child communicate up với parent. Slots cho phép content distribution. Composition API cung cấp cách linh hoạt hơn để organize logic trong components.

### 2. Reactive System (Hệ Thống Phản Ứng)

Vue's reactive system tự động track dependencies và update UI khi data thay đổi. `ref()` tạo reactive reference cho primitive values. `reactive()` tạo reactive object. `computed()` tạo computed properties tự động update khi dependencies thay đổi. Vue 3 sử dụng ES Proxy-based reactivity.

`watch()` và `watchEffect()` cho phép side effects khi reactive state thay đổi. `toRefs()` convert reactive object thành plain refs. `$nextTick()` cho phép code run sau khi DOM update.

### 3. Composition API

Composition API là feature mới trong Vue 3, cung cấp cách linh hoạt để organize logic trong components. `setup()` function là entry point cho Composition API. `ref()` và `reactive()` cho reactive state. `computed()` cho computed properties. `watch()` cho side effects.

Benefits của Composition API: better code reuse (composables), better TypeScript support, better organization for complex components. Options API vẫn được supported và có thể mix với Composition API.

### 4. Vue Router

Vue Router là official routing library cho Vue.js. Route definitions map URLs to components. Dynamic route segments: `/users/:id`. Nested routes cho complex layouts. Navigation guards cho authentication và guards. Scroll behavior control.

`router-link` cho declarative navigation. `router-view` là component render matched route. Programmatic navigation với `router.push()`. Route params và query params có thể access qua composables.

### 5. Pinia (State Management)

Pinia là official state management library cho Vue 3. Store definitions use `defineStore()`. Stores có state, getters, và actions. Composables-style API với setup stores. Devtools integration cho debugging. Hot Module Replacement support.

Stores có thể accessed từ any component. `storeToRefs()` maintain reactivity khi destructuring. Plugins cho persisting state, etc. Pinia thay thế Vuex vì simpler API và better TypeScript support.

### 6. Vuex (State Management Legacy)

Vuex là legacy state management library (Vue 2 primary, Vue 3 possible but Pinia recommended). State, Getters, Mutations, Actions, Modules structure. Strict mode enforce mutations through mutations only. Plugins cho persisting, logging. Devtools integration.

Vuex patterns: namespaced modules, action multiplexing, cross-module actions. Migration path to Pinia available. Vuex still used in many Vue 2 projects.

### 7. Directives (Chỉ Thị)

Directives là special attributes prefixed với `v-` cung cấp reusable template logic. Built-in directives: `v-if`, `v-for`, `v-bind`, `v-on`, `v-model`, `v-show`, `v-slot`, `v-cloak`. Custom directives có lifecycle hooks: created, beforeMount, mounted, beforeUpdate, updated, beforeUnmount, unmounted.

Directives useful cho DOM manipulation, focus management, lazy loading, permissions. Global directives registered with `app.directive()`. Directive arguments và modifiers cung cấp additional configuration.

### 8. Lifecycle Hooks

Lifecycle Hooks cho phép code execute tại specific points in component lifecycle. Creation: `beforeCreate`, `created`. Mounting: `beforeMount`, `mounted`. Updating: `beforeUpdate`, `updated`. Unmounting: `beforeUnmount`, `unmounted`. Error: `onErrorCaptured`.

In Composition API, lifecycle hooks được import từ vue: `onMounted`, `onUpdated`, `onUnmounted`, etc. `onErrorCaptured` for error handling. `onRenderTracked`, `onRenderTriggered` for debugging.

### 9. Slots và Composables

Slots cho phép component composition và content distribution. Default slot nhận props từ parent. Named slots cho multiple slot outlets. Scoped slots truyền props từ child đến parent slot content. `v-slot` directive cho named và scoped slots.

Composables là functions sử dụng Vue Composition API's reactivity features để reuse stateful logic. Custom hooks naming convention: `use` prefix (useCounter, useFetch). Composables có thể use other composables. Shared reactive state across composables.

### 10. Vue CLI và Vite

Vue CLI là command-line tool cho scaffolding Vue projects. `vue create` command. Plugin system cho add features. GUI option với Vue UI. Build options: webpack, etc. Vue CLI 3+ sử dụng Vue CLI Service.

Vite là next-generation build tool, recommended cho Vue 3. Fast HMR với native ESM. Instant server start. Optimized builds với Rollup. Vue Plugin officially maintained. Vite is default tooling for Nuxt 3.

### 11. Vue Devtools

Vue Devtools là browser extension cho debugging Vue applications. Component inspection: state, props, computed. Timeline của events và mutations. Performance profiling. Routing inspection. Vuex/Pinia state inspection.

Vue 3 Devtools có improved UI và performance. Network inspection for API requests. Settings cho customization. Mobile debugging support.

### 12. Transition và Animation

Vue's transition system animate elements entering/leaving DOM. `<transition>` component for single elements. `<transition-group>` for lists. CSS transition classes: `v-enter-active`, `v-leave-active`, etc. JavaScript hooks for complex animations.

Built-in transition modes prevent both elements being visible simultaneously. Dynamic transitions với `:is` attribute. Transition effects: fade, slide, scale. Animated lists với `<transition-group>`.

### 13. Vue Server-Side Rendering (SSR)

Vue SSR renders Vue components trên server và hydrate trên client. Nuxt.js là full-stack framework với SSR built-in. VueUse functions cho SSR-compatible utilities. `createSSRApp()` cho manual SSR setup. Streaming SSR for better performance.

SSR benefits: SEO, faster first contentful paint, better perceived performance. Considerations: server-only code detection, hydration mismatches, state serialization.

### 14. TypeScript Support

Vue 3 có native TypeScript support. Volar is recommended VS Code extension. Type inference for props, emits, reactive state. `defineComponent()` with types. `PropType` for complex prop types. `ref()` generic types.

Best practices: Use TypeScript for better DX. Define interfaces for component APIs. Use `withDefaults()` for default props. Generic components for reusable logic.

### 15. Vue Test Utils

Vue Test Utils là official testing library for Vue components. `mount()` và `shallowMount()` for component rendering. `find()`, `findAll()` for querying DOM. `trigger()` for simulating user events. `setProps()` for updating props.

Testing strategies: Unit tests for components, integration tests for features. Mocking dependencies. Testing async behavior. Snapshot testing. Best practices: Test behavior, not implementation.

### 16. Nuxt.js Integration

Nuxt.js là full-stack framework built on top of Vue. File-based routing. SSR, SSG, SPA modes. Auto-imports. Data fetching composables. Server routes. Middleware. Modules ecosystem.

Nuxt 3 sử dụng Vue 3 và Vite. Hybrid rendering modes. Server engine có thể là Nitro. Nuxt Modules cho extend functionality.

## Kết luận

Từ điển thuật ngữ này cung cấp nền tảng kiến thức vững chắc về Vue.js.
