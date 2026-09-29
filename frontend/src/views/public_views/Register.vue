<template>
  <div class="flex h-screen overflow-hidden">

    <!-- Left side: Form -->
    <div class="w-full lg:w-[45%] flex flex-col justify-center px-8 md:px-12 xl:px-16 bg-white overflow-y-auto py-8">
      <div class="max-w-md w-full mx-auto">
        <!-- Brand/Logo -->
        <router-link to="/" class="flex items-center space-x-2.5 mb-8">
          <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow shadow-indigo-500/30">
            <span class="text-white font-black text-xs">CB</span>
          </div>
          <span class="font-bold text-xl tracking-tight text-gray-900">Career<span class="text-indigo-600">Bridge</span></span>
        </router-link>

        <div class="mb-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-1 tracking-tight">Create an Account</h2>
          <p class="text-gray-500 text-sm">Join CareerBridge and start your journey</p>
        </div>

        <!-- Cold-start notice -->
        <div class="flex items-start gap-2.5 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 mb-5">
          <span class="text-amber-500 text-base leading-none mt-0.5">⚡</span>
          <p class="text-xs text-amber-800 leading-relaxed">
            <strong>First-time tip:</strong> The server may take up to <strong>60 seconds</strong> to respond on your first action. Just wait — don't refresh!
          </p>
        </div>

        <div v-if="successMessage" class="mb-4 bg-green-50 border border-green-200 p-3.5 rounded-xl flex items-center gap-2.5">
          <CheckCircle class="w-4 h-4 text-green-500 shrink-0" />
          <p class="text-sm text-green-700 font-medium">{{ successMessage }}</p>
        </div>

        <div v-if="errorMessage" class="mb-4 bg-red-50 border border-red-200 p-3.5 rounded-xl flex items-center gap-2.5">
          <AlertCircle class="w-4 h-4 text-red-500 shrink-0" />
          <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
        </div>

        <form v-if="!isVerifying" @submit.prevent="register" class="space-y-4">
          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">I am a...</label>
            <div class="grid grid-cols-2 gap-3">
              <label class="relative flex items-center justify-center p-3 border-2 rounded-xl cursor-pointer transition-all"
                :class="role === 'student' ? 'border-indigo-500 bg-indigo-50 text-indigo-700' : 'border-gray-200 text-gray-500 hover:border-gray-300'">
                <input type="radio" v-model="role" value="student" class="sr-only">
                <span class="font-semibold text-sm flex items-center gap-2">
                  <User class="w-4 h-4" /> Student
                </span>
              </label>
              <label class="relative flex items-center justify-center p-3 border-2 rounded-xl cursor-pointer transition-all"
                :class="role === 'company' ? 'border-indigo-500 bg-indigo-50 text-indigo-700' : 'border-gray-200 text-gray-500 hover:border-gray-300'">
                <input type="radio" v-model="role" value="company" class="sr-only">
                <span class="font-semibold text-sm flex items-center gap-2">
                  <Building2 class="w-4 h-4" /> Company
                </span>
              </label>
            </div>
          </div>

          <!-- Name -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Full Name / Company Name</label>
            <input type="text" v-model="name" required
              class="block w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition text-sm bg-gray-50/50 placeholder-gray-400"
              placeholder="John Doe / Acme Corp">
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Email Address</label>
            <input type="email" v-model="email" required
              class="block w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition text-sm bg-gray-50/50 placeholder-gray-400"
              placeholder="you@example.com">
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Password</label>
            <div class="relative">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                @input="checkPassword"
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

            <!-- Live Password Checklist -->
            <div v-if="password.length > 0" class="mt-2 space-y-1 bg-gray-50 rounded-xl p-3 border border-gray-100">
              <div v-for="rule in passwordRules" :key="rule.label" class="flex items-center gap-2 text-xs transition-colors"
                :class="rule.met ? 'text-green-600' : 'text-gray-400'">
                <CheckCircle v-if="rule.met" class="w-3.5 h-3.5 shrink-0 text-green-500" />
                <XCircle v-else class="w-3.5 h-3.5 shrink-0 text-gray-300" />
                <span>{{ rule.label }}</span>
              </div>
            </div>
          </div>

          <button type="submit" :disabled="loading || !allRulesMet"
            class="w-full flex justify-center items-center py-3.5 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 focus:ring-4 focus:ring-indigo-500/20 transition disabled:opacity-50 shadow-lg shadow-indigo-500/20 mt-2">
            <Loader2 v-if="loading" class="w-4 h-4 animate-spin mr-2" />
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <!-- OTP Verification -->
        <form v-if="isVerifying" @submit.prevent="verifyOtp" class="space-y-5">
          <div class="text-center mb-4 bg-indigo-50 border border-indigo-100 rounded-2xl p-5">
            <div class="w-12 h-12 bg-indigo-600/10 rounded-full flex items-center justify-center mx-auto mb-3">
              <CheckCircle class="w-6 h-6 text-indigo-500" />
            </div>
            <h3 class="text-lg font-bold text-gray-800">Check your inbox</h3>
            <p class="text-sm text-gray-500 mt-1">We sent a 6-digit code to <strong class="text-gray-700">{{ email }}</strong></p>
            <p class="text-xs text-amber-600 mt-2">Can't find it? Check your spam or promotions folder.</p>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1.5">Enter OTP</label>
            <input type="text" v-model="otp" required maxlength="6"
              class="block w-full px-4 py-4 border-2 border-gray-200 focus:border-indigo-500 rounded-xl text-center text-3xl tracking-widest font-mono focus:ring-2 focus:ring-indigo-500/20 transition"
              placeholder="000000">
          </div>

          <button type="submit" :disabled="loading"
            class="w-full flex justify-center items-center py-3.5 rounded-xl text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 focus:ring-4 focus:ring-indigo-500/20 transition disabled:opacity-50">
            <Loader2 v-if="loading" class="w-4 h-4 animate-spin mr-2" />
            {{ loading ? 'Verifying...' : 'Verify & Continue' }}
          </button>
        </form>

        <div v-if="!isVerifying" class="mt-5 relative flex items-center">
          <div class="flex-1 border-t border-gray-200"></div>
          <span class="px-4 text-sm text-gray-400 bg-white font-medium">Or continue with</span>
          <div class="flex-1 border-t border-gray-200"></div>
        </div>

        <div v-if="!isVerifying" class="mt-4 flex justify-center">
          <GoogleLogin :callback="handleGoogleLogin" />
        </div>

        <p class="mt-6 text-center text-sm text-gray-500">
          Already have an account?
          <router-link to="/login" class="font-bold text-indigo-600 hover:text-indigo-800 transition ml-1">Sign in</router-link>
        </p>
      </div>
    </div>

    <!-- Right side: Visual Panel -->
    <div class="hidden lg:flex lg:flex-1 relative bg-gray-950 overflow-hidden flex-col justify-between p-14">
      <!-- Background gradients -->
      <div class="absolute inset-0">
        <div class="absolute top-1/4 left-1/3 w-80 h-80 bg-indigo-600/25 rounded-full blur-3xl"></div>
        <div class="absolute bottom-1/3 right-1/4 w-64 h-64 bg-violet-600/20 rounded-full blur-3xl"></div>
        <div class="absolute top-2/3 left-1/2 w-48 h-48 bg-cyan-600/10 rounded-full blur-3xl"></div>
      </div>

      <!-- Logo -->
      <div class="relative flex items-center gap-2.5 z-10">
        <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
          <span class="text-white font-black text-xs">CB</span>
        </div>
        <span class="font-bold text-white text-lg">CareerBridge</span>
      </div>

      <!-- Center content -->
      <div class="relative z-10 flex-1 flex flex-col justify-center">
        <h2 class="text-4xl font-black text-white leading-tight tracking-tight mb-5">
          Start your placement<br/>
          <span class="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">journey today.</span>
        </h2>
        <p class="text-gray-400 text-base leading-relaxed max-w-sm mb-10">
          Students get matched with eligible jobs. Companies get a complete hiring pipeline. Everything in one place.
        </p>

        <!-- Steps -->
        <div class="flex flex-col gap-4">
          <div v-for="(step, i) in steps" :key="i" class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400 font-bold text-sm">
              {{ i + 1 }}
            </div>
            <div>
              <p class="text-white font-semibold text-sm">{{ step.title }}</p>
              <p class="text-gray-500 text-xs mt-0.5">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom social proof card -->
      <div class="relative z-10 bg-white/8 border border-white/10 backdrop-blur-xl rounded-2xl p-6">
        <div class="flex items-center gap-3 mb-3">
          <div class="flex -space-x-2.5">
            <img class="w-8 h-8 rounded-full border-2 border-gray-900 object-cover" src="https://i.pravatar.cc/100?img=44" alt="User">
            <img class="w-8 h-8 rounded-full border-2 border-gray-900 object-cover" src="https://i.pravatar.cc/100?img=55" alt="User">
            <img class="w-8 h-8 rounded-full border-2 border-gray-900 object-cover" src="https://i.pravatar.cc/100?img=66" alt="User">
            <div class="w-8 h-8 rounded-full border-2 border-gray-900 bg-indigo-600 flex items-center justify-center text-white text-xs font-bold">+k</div>
          </div>
          <p class="text-gray-300 text-sm">Students already registered</p>
        </div>
        <div class="flex items-center gap-1 mb-1">
          <span v-for="n in 5" :key="n" class="text-amber-400 text-sm">★</span>
        </div>
        <p class="text-white text-sm leading-relaxed italic">
          "Found my placement through CareerBridge. The whole process from applying to the interview was in one tab."
        </p>
        <p class="text-indigo-400 text-xs font-semibold mt-2">— Final Year CS Student</p>
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
      ],
      steps: [
        { title: "Create your profile", desc: "Add your education, skills, and upload your résumé." },
        { title: "Browse eligible jobs", desc: "See only jobs you qualify for based on your CGPA and branch." },
        { title: "Apply and get placed", desc: "Track your application and join video interviews right in the browser." },
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
          token: response.credential,
          role: this.role
        })
        this.handleLoginSuccess(result.data)
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Google sign-in failed. Please try again."
      } finally {
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
