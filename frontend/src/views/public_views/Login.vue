<template>
  <div class="flex h-screen overflow-hidden bg-white">
    
    <!-- Left side: Form -->
    <div class="w-full lg:w-1/2 flex flex-col justify-center px-8 md:px-16 xl:px-32 bg-white overflow-y-auto">
      <div class="max-w-md w-full mx-auto">
        <!-- Brand/Logo -->
        <router-link to="/" class="flex items-center space-x-2 text-trust-blue mb-12">
          <img src="/logo.jpg" alt="CareerBridge Logo" class="h-8 w-8 object-cover rounded-md shadow-sm" />
          <span class="font-heading font-bold text-2xl tracking-tight text-gray-900">Career<span class="text-premium-gold">Bridge</span></span>
        </router-link>

        <div class="mb-10">
          <h2 class="text-3xl font-heading font-bold text-gray-900 mb-2">Welcome Back</h2>
          <p class="text-gray-500 text-sm">Sign in to your CareerBridge account</p>
        </div>

        <div v-if="successMessage" class="mb-6 bg-green-50 border-l-4 border-green-500 p-4 rounded flex items-center">
          <CheckCircle class="w-5 h-5 text-green-500 mr-2" />
          <p class="text-sm text-green-700 font-medium">{{ successMessage }}</p>
        </div>

        <div v-if="errorMessage" class="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center">
          <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
          <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
        </div>

        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input type="email" v-model="email" required class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition sm:text-sm" placeholder="you@example.com">
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                required
                class="block w-full px-4 py-3 pr-10 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition sm:text-sm"
                placeholder="••••••••"
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 transition"
                tabindex="-1"
              >
                <Eye v-if="!showPassword" class="w-4 h-4" />
                <EyeOff v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-trust-blue focus:ring-trust-blue border-gray-300 rounded">
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div class="text-sm">
              <a href="#" class="font-medium text-trust-blue hover:text-blue-800 transition">
                Forgot your password?
              </a>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-md text-sm font-bold text-white bg-trust-blue hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-trust-blue transition disabled:opacity-50"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin mr-2" />
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </form>

        <div class="mt-8 relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500 font-medium">Or continue with</span>
          </div>
        </div>

        <div class="mt-6">
          <GoogleLogin :callback="handleGoogleLogin" class="w-full flex justify-center" />
        </div>

        <div class="mt-10 text-center">
          <p class="text-sm text-gray-600">
            Don't have an account? 
            <router-link to="/register" class="font-bold text-trust-blue hover:text-blue-800 transition">Create an account</router-link>
          </p>
        </div>
      </div>
    </div>

    <!-- Right side: Marketing -->
    <div class="hidden lg:block lg:w-1/2 relative bg-trust-blue">
      <img src="/auth-bg.jpg" class="absolute inset-0 w-full h-full object-cover opacity-80 mix-blend-overlay" alt="CareerBridge Authentication" />
      <div class="absolute inset-0 bg-gradient-to-br from-trust-blue/80 via-indigo-900/50 to-purple-900/60 mix-blend-multiply"></div>
      
      <!-- Content overlay -->
      <div class="absolute inset-0 flex flex-col justify-end p-16 pb-24">
        <div class="bg-white/10 backdrop-blur-md border border-white/20 p-8 rounded-2xl max-w-lg shadow-2xl">
          <h3 class="text-3xl font-heading font-bold leading-tight mb-4 text-white text-shadow-sm">Connecting Top Talent with Premium Opportunities.</h3>
          <p class="text-lg text-blue-100">Join thousands of students and companies streamlining their placement process with CareerBridge.</p>
          
          <div class="flex items-center mt-6 space-x-4">
            <div class="flex -space-x-3">
              <img class="w-10 h-10 rounded-full border-2 border-trust-blue object-cover" src="https://i.pravatar.cc/100?img=1" alt="Avatar">
              <img class="w-10 h-10 rounded-full border-2 border-trust-blue object-cover" src="https://i.pravatar.cc/100?img=2" alt="Avatar">
              <img class="w-10 h-10 rounded-full border-2 border-trust-blue object-cover" src="https://i.pravatar.cc/100?img=3" alt="Avatar">
              <div class="w-10 h-10 rounded-full border-2 border-trust-blue bg-white flex justify-center items-center font-bold text-trust-blue text-xs">+1k</div>
            </div>
            <p class="text-sm font-medium text-white">Loved by professionals</p>
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
      errorMessage: "", loading: false, showPassword: false
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
        this.errorMessage = error.response?.data?.message || 'Unable to connect to server'
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