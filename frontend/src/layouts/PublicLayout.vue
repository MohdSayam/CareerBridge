<template>
  <div class="min-h-screen flex flex-col font-sans bg-gray-50">
    <!-- Navbar -->
    <nav class="bg-trust-blue shadow-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-2 text-white">
              <span class="font-heading font-bold text-2xl tracking-tight">Career<span class="text-premium-gold">Bridge</span></span>
            </router-link>
          </div>
          <div class="flex items-center space-x-6">
            <router-link 
              to="/login" 
              class="text-white hover:text-premium-gold transition font-medium text-sm"
              active-class="text-premium-gold"
            >
              Login
            </router-link>
            <router-link 
              to="/register" 
              class="bg-premium-gold hover:bg-yellow-500 text-white px-4 py-2 rounded-lg font-medium text-sm transition shadow-sm"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-center items-center">
        <p class="text-gray-500 text-sm">
          &copy; {{ new Date().getFullYear() }} CareerBridge. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'PublicLayout'
}
</script>