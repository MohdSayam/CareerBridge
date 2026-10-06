<template>
  <div class="flex h-screen overflow-hidden">
    
    <!-- Left side: Form -->
    <div class="w-full lg:w-[45%] flex flex-col justify-center px-8 md:px-12 xl:px-16 bg-white overflow-y-auto">
      <div class="max-w-md w-full mx-auto">
        <!-- Brand/Logo -->
        <router-link to="/" class="flex items-center space-x-2.5 mb-10">
          <img src="/favicon.svg" alt="CareerBridge" class="w-8 h-8" />
          <span class="font-extrabold text-xl tracking-tight text-gray-900">CareerBridge</span>
        </router-link>

        <div class="mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-1.5 tracking-tight">Welcome Back</h2>
          <p class="text-gray-500 text-sm">Sign in to your CareerBridge account</p>
        </div>

        <!-- Cold-start notice -->
        <div class="flex items-start gap-2.5 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 mb-6">
          <span class="text-amber-500 text-base leading-none mt-0.5">⚡</span>
          <p class="text-xs text-amber-800 leading-relaxed">
            <strong>First-time tip:</strong> Backend runs on a free server that sleeps when idle. Your first action may take up to <strong>60 seconds</strong>. Just wait — don't refresh!
          </p>
        </div>

        <div v-if="successMessage" class="mb-5 bg-green-50 border border-green-200 p-3.5 rounded-xl flex items-center gap-2.5">
          <CheckCircle class="w-4 h-4 text-green-500 shrink-0" />
          <p class="text-sm text-green-700 font-medium">{{ successMessage }}</p>
        </div>

        <div v-if="errorMessage" class="mb-5 bg-red-50 border border-red-200 p-3.5 rounded-xl flex items-center gap-2.5">
          <AlertCircle class="w-4 h-4 text-red-500 shrink-0" />
          <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
        </div>

        <form @submit.prevent="login" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
            <input type="email" v-model="email" required
              class="block w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition text-sm bg-gray-50/50 placeholder-gray-400"
              placeholder="you@example.com">
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Password</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                required
                class="block w-full px-4 py-3 pr-11 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition text-sm bg-gray-50/50 placeholder-gray-400"
                placeholder="••••••••"
              >
              <button type="button" @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 flex items-center pr-3.5 text-gray-400 hover:text-gray-600 transition" tabindex="-1">
                <Eye v-if="!showPassword" class="w-4 h-4" />
                <EyeOff v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 cursor-pointer">
              <input id="remember-me" type="checkbox" class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
              <span class="text-sm text-gray-600">Remember me</span>
            </label>
            <a href="#" class="text-sm font-semibold text-indigo-600 hover:text-indigo-800 transition">Forgot password?</a>
          </div>

          <button type="submit" :disabled="loading"
            class="w-full flex justify-center items-center py-3.5 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 focus:ring-4 focus:ring-indigo-500/20 transition disabled:opacity-50 shadow-lg shadow-indigo-500/20">
            <Loader2 v-if="loading" class="w-4 h-4 animate-spin mr-2" />
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </form>

        <div class="mt-6 relative flex items-center">
          <div class="flex-1 border-t border-gray-200"></div>
          <span class="px-4 text-sm text-gray-400 bg-white font-medium">Or continue with</span>
          <div class="flex-1 border-t border-gray-200"></div>
        </div>

        <div class="mt-5 flex justify-center">
          <GoogleLogin :callback="handleGoogleLogin" />
        </div>

        <p class="mt-8 text-center text-sm text-gray-500">
          Don't have an account?
          <router-link to="/register" class="font-bold text-indigo-600 hover:text-indigo-800 transition ml-1">Create an account</router-link>
        </p>
      </div>
    </div>

    <!-- Right side: Visual Panel -->
    <div class="hidden lg:block lg:flex-1 relative bg-gray-50 overflow-hidden">
      <!-- Full background image -->
      <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=1000&auto=format&fit=crop" alt="Professional working" class="absolute inset-0 w-full h-full object-cover" />
      
      <!-- Gradient overlay to ensure text readability -->
      <div class="absolute inset-0 bg-gradient-to-t from-gray-900/90 via-gray-900/40 to-transparent"></div>

      <!-- Content -->
      <div class="absolute inset-0 flex flex-col justify-between p-14">
        <!-- Logo -->
        <div class="flex items-center gap-2.5 z-10">
          <img src="/favicon.svg" alt="CareerBridge" class="w-8 h-8 filter brightness-0 invert" />
          <span class="font-extrabold text-white text-xl">CareerBridge</span>
        </div>

        <!-- Bottom Content -->
        <div class="relative z-10 max-w-md">
          <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-6 mb-8">
            <h2 class="text-3xl font-bold text-white mb-3 leading-tight">
              Access top-tier campus talent and premium opportunities.
            </h2>
            <p class="text-gray-200 text-sm leading-relaxed">
              Join thousands of verified students and verified companies bridging the gap between campus and career.
            </p>
          </div>

          <!-- Bottom testimonial card -->
          <div class="bg-white rounded-2xl p-6 shadow-xl">
            <div class="flex items-center gap-3 mb-3">
              <div class="flex -space-x-2.5">
                <img class="w-8 h-8 rounded-full border-2 border-white object-cover" src="https://i.pravatar.cc/100?img=11" alt="User">
                <img class="w-8 h-8 rounded-full border-2 border-white object-cover" src="https://i.pravatar.cc/100?img=22" alt="User">
                <img class="w-8 h-8 rounded-full border-2 border-white object-cover" src="https://i.pravatar.cc/100?img=33" alt="User">
              </div>
              <div class="flex items-center gap-1">
                <span v-for="n in 5" :key="n" class="text-amber-400 text-sm">★</span>
              </div>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed italic mb-3">
              "The most seamless hiring experience we've had on any campus. The in-browser video interviews are game-changing."
            </p>
            <p class="text-indigo-600 text-xs font-bold uppercase tracking-wide">— Hiring Manager, TechCorp</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import api from '../../api/axios.js'
import { AlertCircle, CheckCircle, Loader2, Eye, EyeOff } from "lucide-vue-next"

export default {
  name: "Login",
  components: { AlertCircle, CheckCircle, Loader2, Eye, EyeOff },
  data() {
    return {
      email: "", password: "", successMessage: "",
      errorMessage: "", loading: false, showPassword: false,
      panelFeatures: [
        { icon: "🎯", text: "Smart eligibility filtering for jobs", bg: "bg-indigo-600/20" },
        { icon: "📹", text: "Live peer-to-peer video interviews", bg: "bg-violet-600/20" },
        { icon: "📧", text: "Automated email notifications", bg: "bg-cyan-600/20" },
        { icon: "📊", text: "Real-time application tracking", bg: "bg-emerald-600/20" },
      ]
    }
  },
  methods: {
    handleLoginSuccess(data) {
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("role", data.role)
      if (data.profile_complete !== undefined) {
        localStorage.setItem("profile_complete", data.profile_complete)
      }
      
      if (data.role === "admin") this.$router.push("/admin")
      else if (data.role === "company") {
        if (data.profile_complete === false) this.$router.push("/company/profile")
        else this.$router.push("/company")
      }
      else if (data.role === "student") {
        if (data.profile_complete === false) this.$router.push("/student/onboarding")
        else this.$router.push("/student")
      }
    },
    async login() {
      this.successMessage = ""
      this.errorMessage = ""
      this.loading = true

      try {
        const response = await api.post("/auth/login", {
          email: this.email,
          password: this.password
        })
        
        this.successMessage = response.data.message
        this.handleLoginSuccess(response.data)

      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Unable to connect to server. The server may be waking up — please try again in 30 seconds.'
      } finally {
        this.loading = false
      }
    },
    async handleGoogleLogin(response) {
      this.successMessage = ""
      this.errorMessage = ""
      this.loading = true
      
      try {
        const result = await api.post("/auth/google/login", {
          token: response.credential
        })
        this.handleLoginSuccess(result.data)
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Google Login failed"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>