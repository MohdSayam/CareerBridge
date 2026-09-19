<template>
  <div class="flex flex-col items-center justify-center p-4">
    <!-- Spinning Loader SVG -->
    <svg 
      class="animate-spin text-trust-blue" 
      :class="sizeClass"
      xmlns="http://www.w3.org/2000/svg" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle 
        class="opacity-25" 
        cx="12" 
        cy="12" 
        r="10" 
        stroke="currentColor" 
        stroke-width="4"
      ></circle>
      <path 
        class="opacity-75" 
        fill="currentColor" 
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
    <p v-if="text" class="mt-3 text-sm font-medium text-gray-500 animate-pulse">{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: "Loader",
  props: {
    size: {
      type: String,
      default: "md" // sm, md, lg
    },
    text: {
      type: String,
      default: "" // Optional text below loader
    }
  },
  computed: {
    sizeClass() {
      switch(this.size) {
        case 'sm': return 'h-5 w-5';
        case 'lg': return 'h-12 w-12';
        case 'xl': return 'h-16 w-16';
        default: return 'h-8 w-8';
      }
    }
  }
}
</script>
