<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast"
      tag="div"
      style="position: fixed; top: 1.25rem; right: 1.25rem; z-index: 99999;"
      class="flex flex-col space-y-3 pointer-events-none"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-start w-80 max-w-sm shadow-2xl rounded-xl p-4 border"
        :class="[
          toast.type === 'success' ? 'bg-white border-green-200 text-green-800' : '',
          toast.type === 'error' ? 'bg-white border-red-200 text-red-800' : '',
          toast.type === 'info' ? 'bg-white border-blue-200 text-blue-800' : ''
        ]"
      >
        <div class="flex-shrink-0 mr-3 mt-0.5">
          <CheckCircle v-if="toast.type === 'success'" class="w-5 h-5 text-green-500" />
          <XCircle v-else-if="toast.type === 'error'" class="w-5 h-5 text-red-500" />
          <Info v-else-if="toast.type === 'info'" class="w-5 h-5 text-blue-500" />
        </div>
        <p class="text-sm font-medium leading-snug flex-1">{{ toast.message }}</p>
        <button @click="removeToast(toast.id)" class="ml-2 text-gray-400 hover:text-gray-600 flex-shrink-0 transition">
          <X class="w-4 h-4" />
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script>
import { CheckCircle, XCircle, X, Info } from 'lucide-vue-next'

let _instance = null

export function toast(message, type = 'success') {
  if (_instance) _instance.addToast(message, type)
}

export default {
  name: 'ToastContainer',
  components: { CheckCircle, XCircle, X, Info },
  data() {
    return { toasts: [] }
  },
  mounted() {
    _instance = this
  },
  beforeUnmount() {
    _instance = null
  },
  methods: {
    addToast(message, type = 'success') {
      const id = Date.now() + Math.random()
      this.toasts.push({ id, message, type })
      setTimeout(() => this.removeToast(id), 3500)
    },
    removeToast(id) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    }
  }
}
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.35s cubic-bezier(0.21, 1.02, 0.73, 1);
}
.toast-leave-active {
  transition: all 0.25s ease-in;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
.toast-move {
  transition: transform 0.3s ease;
}
</style>
