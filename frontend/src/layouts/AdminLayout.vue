<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden font-sans">
    
    <!-- Mobile Sidebar Backdrop -->
    <div v-if="isMobileMenuOpen" class="fixed inset-0 z-50 bg-black/50 lg:hidden backdrop-blur-sm" @click="isMobileMenuOpen = false"></div>

    <!-- Sidebar -->
    <aside :class="['fixed inset-y-0 left-0 z-50 w-64 bg-gray-900 text-white flex flex-col transition-transform duration-300 ease-in-out lg:static lg:translate-x-0', isMobileMenuOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full']">
      
      <!-- Brand -->
      <div class="h-20 flex items-center justify-between px-6 border-b border-gray-800/50">
        <router-link to="/admin" class="flex items-center space-x-3" @click="isMobileMenuOpen = false">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center shadow-lg border border-emerald-400/30">
            <Shield class="w-6 h-6 text-white" />
          </div>
          <span class="font-heading font-bold text-xl tracking-tight text-white">Career<span class="text-emerald-500">Bridge</span></span>
        </router-link>
        <button @click="isMobileMenuOpen = false" class="lg:hidden text-gray-400 hover:text-white transition">
          <X class="w-6 h-6" />
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 space-y-2 overflow-y-auto custom-scrollbar">
        <router-link v-for="link in navLinks" :key="link.path" :to="link.path" @click="isMobileMenuOpen = false"
          class="flex items-center px-4 py-3 rounded-xl transition-all duration-200 group"
          :class="[isLinkActive(link) ? 'bg-gray-800 text-white font-semibold shadow-inner border border-gray-700/50' : 'text-gray-400 hover:bg-gray-800/50 hover:text-gray-200']">
          <component :is="link.icon" class="w-5 h-5 mr-3 transition-transform group-hover:scale-110" :class="[isLinkActive(link) ? 'text-emerald-500' : 'text-gray-500']" />
          {{ link.label }}
        </router-link>
      </nav>

      <!-- Footer Action -->
      <div class="p-4 border-t border-gray-800/50">
        <button @click="logout" class="flex items-center w-full px-4 py-3 rounded-xl text-gray-400 hover:bg-red-500/10 hover:text-red-400 transition-all duration-200 group border border-transparent hover:border-red-500/30">
          <LogOut class="w-5 h-5 mr-3 transition-transform group-hover:-translate-x-1" />
          <span class="font-medium">Logout</span>
        </button>
      </div>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden relative">
      
      <!-- Mobile Header -->
      <header class="h-14 bg-white border-b border-gray-100 flex items-center justify-between px-4 lg:hidden shadow-sm z-30">
        <div class="flex items-center space-x-2">
          <Shield class="w-6 h-6 text-emerald-600" />
          <span class="font-heading font-bold text-lg text-gray-800">Career<span class="text-emerald-600">Bridge</span></span>
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto bg-gray-50/50 p-4 pb-20 sm:p-6 lg:p-8 lg:pb-8 w-full custom-scrollbar">
        <div class="max-w-7xl mx-auto h-full">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>

      <!-- Mobile Bottom Navigation -->
      <nav class="lg:hidden fixed bottom-0 w-full bg-white border-t border-gray-200 flex justify-around items-center h-16 z-40 pb-safe shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <router-link v-for="link in bottomNavLinks" :key="link.path" :to="link.path"
          class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors"
          :class="[$route.path === link.path ? 'text-emerald-600' : 'text-gray-500 hover:text-gray-900']">
          <component :is="link.icon" class="w-6 h-6" :class="[$route.path === link.path ? 'text-emerald-600' : 'text-gray-400']" />
          <span class="text-[10px] font-medium">{{ link.label }}</span>
        </router-link>
        
        <button @click="isMobileMenuOpen = true" class="flex flex-col items-center justify-center w-full h-full space-y-1 text-gray-500 hover:text-gray-900 transition-colors">
          <Menu class="w-6 h-6 text-gray-400" />
          <span class="text-[10px] font-medium">Menu</span>
        </button>
      </nav>

    </div>
  </div>
</template>

<script>
import { 
  Shield, LayoutDashboard, Users, Building2, 
  Briefcase, FileText, Award, Video, LogOut, Menu, X
} from "lucide-vue-next"

export default {
  name: "AdminLayout",
  components: {
    Shield, LogOut, Menu, X
  },
  data() {
    return {
      isMobileMenuOpen: false,
      navLinks: [
        { path: '/admin', label: 'Dashboard', icon: LayoutDashboard },
        { path: '/admin/students', label: 'Students', icon: Users },
        { path: '/admin/companies', label: 'Companies', icon: Building2 },
        { path: '/admin/jobs', label: 'Jobs', icon: Briefcase },
        { path: '/admin/applications', label: 'Applications', icon: FileText },
        { path: '/admin/interviews', label: 'Interviews', icon: Video },
        { path: '/admin/placements', label: 'Placements', icon: Award }
      ]
    }
  },
  computed: {
    bottomNavLinks() {
      // Show first 4 links in bottom nav
      return this.navLinks.slice(0, 4);
    }
  },
  methods: {
    isLinkActive(link) {
      // Exact match for root dashboard route to avoid prefix collision
      if (link.path === '/admin') {
        return this.$route.path === '/admin'
      }
      return this.$route.path === link.path || this.$route.path.startsWith(link.path + '/')
    },
    logout() {
      localStorage.removeItem("access_token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 20px;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
}
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .pb-safe {
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>