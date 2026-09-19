<template>
  <div class="flex h-screen overflow-hidden bg-white">

    <!-- Left side: Form -->
    <div class="w-full lg:w-1/2 flex flex-col justify-center px-8 md:px-16 xl:px-32 bg-white overflow-y-auto py-4">
      <div class="max-w-md w-full mx-auto">
        <!-- Brand/Logo -->
        <router-link to="/" class="flex items-center space-x-2 text-trust-blue mb-6">
          <img src="/logo.jpg" alt="CareerBridge Logo" class="h-8 w-8 object-cover rounded-md shadow-sm" />
          <span class="font-heading font-bold text-2xl tracking-tight text-gray-900">Career<span class="text-premium-gold">Bridge</span></span>
        </router-link>

        <div class="mb-4">
          <h2 class="text-2xl font-heading font-bold text-gray-900 mb-1">Create an Account</h2>
          <p class="text-gray-500 text-sm">Join CareerBridge and start your journey</p>
        </div>

        <div v-if="successMessage" class="mb-4 bg-green-50 border-l-4 border-green-500 p-3 rounded flex items-center">
          <CheckCircle class="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
          <p class="text-sm text-green-700 font-medium">{{ successMessage }}</p>
        </div>

        <div v-if="errorMessage" class="mb-4 bg-red-50 border-l-4 border-red-500 p-3 rounded flex items-center">
          <AlertCircle class="w-5 h-5 text-red-500 mr-2 flex-shrink-0" />
          <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
        </div>

        <form v-if="!isVerifying" @submit.prevent="register" class="space-y-3">
          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">I am a...</label>
            <div class="grid grid-cols-2 gap-4">
              <label class="relative flex items-center justify-center p-2.5 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="role === 'student' ? 'border-trust-blue bg-blue-50/50 text-trust-blue' : 'border-gray-200 text-gray-500'">
                <input type="radio" v-model="role" value="student" class="sr-only">
                <span class="font-medium text-sm flex items-center">
                  <User class="w-4 h-4 mr-2" /> Student
                </span>
              </label>
              <label class="relative flex items-center justify-center p-2.5 border rounded-xl cursor-pointer hover:bg-gray-50 transition-colors" :class="role === 'company' ? 'border-trust-blue bg-blue-50/50 text-trust-blue' : 'border-gray-200 text-gray-500'">
                <input type="radio" v-model="role" value="company" class="sr-only">
                <span class="font-medium text-sm flex items-center">
                  <Building2 class="w-4 h-4 mr-2" /> Company
                </span>
              </label>
            </div>
          </div>

          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Full Name / Company Name</label>
            <input type="text" v-model="name" required class="block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition sm:text-sm" placeholder="John Doe / Acme Corp">
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input type="email" v-model="email" required class="block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition sm:text-sm" placeholder="you@example.com">
          </div>

          <!-- Password with show/hide toggle -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                @input="checkPassword"
                required
                class="block w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition sm:text-sm"
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

            <!-- Live Password Checklist -->
            <div v-if="password.length > 0" class="mt-2 space-y-1 bg-gray-50 rounded-lg p-2.5 border border-gray-100">
              <div v-for="rule in passwordRules" :key="rule.label" class="flex items-center space-x-2 text-xs transition-colors duration-200" :class="rule.met ? 'text-green-600' : 'text-red-500'">
                <CheckCircle v-if="rule.met" class="w-3.5 h-3.5 flex-shrink-0" />
                <XCircle v-else class="w-3.5 h-3.5 flex-shrink-0" />
                <span>{{ rule.label }}</span>
              </div>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading || !allRulesMet"
            class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-md text-sm font-bold text-white bg-trust-blue hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-trust-blue transition disabled:opacity-50 mt-4"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin mr-2" />
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <!-- OTP Verification Form -->
        <form v-if="isVerifying" @submit.prevent="verifyOtp" class="space-y-6">
          <div class="text-center mb-6">
            <h3 class="text-xl font-bold text-gray-800">Verify Your Email</h3>
            <p class="text-sm text-gray-600 mt-2">We've sent a 6-digit code to <strong>{{ email }}</strong></p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Enter OTP</label>
            <input type="text" v-model="otp" required maxlength="6" class="block w-full px-4 py-4 border border-gray-300 rounded-lg focus:ring-trust-blue focus:border-trust-blue text-center text-2xl tracking-widest shadow-sm font-mono" placeholder="••••••">
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-md text-sm font-bold text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-600 transition disabled:opacity-50"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin mr-2" />
            {{ loading ? 'Verifying...' : 'Verify OTP' }}
          </button>
        </form>

        <div v-if="!isVerifying" class="mt-4 relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-200"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500 font-medium">Or continue with</span>
          </div>
        </div>

        <div v-if="!isVerifying" class="mt-4">
          <GoogleLogin :callback="handleGoogleLogin" class="w-full flex justify-center" />
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/login" class="font-bold text-trust-blue hover:text-blue-800 transition">Sign in</router-link>
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
import { AlertCircle, CheckCircle, XCircle, Loader2, User, Building2, Eye, EyeOff } from "lucide-vue-next"

export default {
  name: "Register",
  components: { AlertCircle, CheckCircle, XCircle, Loader2, User, Building2, Eye, EyeOff },
  data() {
    return {
      name: "", email: "", password: "", role: "student",
      successMessage: "", errorMessage: "", loading: false,
      isVerifying: false, otp: "",
      showPassword: false,
      passwordRules: [
        { label: "At least 8 characters", regex: /.{8,}/, met: false },
        { label: "At least 1 uppercase letter", regex: /[A-Z]/, met: false },
        { label: "At least 1 lowercase letter", regex: /[a-z]/, met: false },
        { label: "At least 1 number", regex: /\d/, met: false },
        { label: "At least 1 special character (@$!%*?&)", regex: /[@$!%*?&]/, met: false },
      ]
    }
  },
  computed: {
    allRulesMet() {
      return this.passwordRules.every(r => r.met)
    }
  },
  methods: {
    checkPassword() {
      this.passwordRules.forEach(rule => {
        rule.met = rule.regex.test(this.password)
      })
    },
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
    async register() {
      this.successMessage = ""
      this.errorMessage = ""
      this.loading = true

      try {
        const response = await api.post("/auth/register", {
          email: this.email,
          password: this.password,
          name: this.name,
          role: this.role
        })
        this.successMessage = response.data.message
        this.isVerifying = true
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
          token: response.credential,
          role: this.role
        })
        this.handleLoginSuccess(result.data)
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Google sign-in failed. Please try again."
      } finally {
        // Always reset loading so the button is usable again for retry
        this.loading = false
      }
    },
    async verifyOtp() {
      this.successMessage = ""
      this.errorMessage = ""
      this.loading = true

      try {
        const response = await api.post("/auth/verify-email", {
          email: this.email,
          otp: this.otp
        })
        this.successMessage = response.data.message
        setTimeout(() => { this.$router.push("/login") }, 1500)
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Invalid OTP'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
