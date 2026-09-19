<template>
  <div class="space-y-8 animate-in fade-in duration-500">
    <!-- Header -->
    <div class="flex items-center justify-between mb-2">
      <div>
        <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">Overview</h2>
        <p class="text-slate-500 mt-1">Monitor your recruitment pipeline and active opportunities.</p>
      </div>
      <button @click="loadDashboard" class="p-2.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:shadow-sm transition-all text-slate-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
        <RefreshCcw class="w-5 h-5" :class="{ 'animate-spin': loading }" />
      </button>
    </div>

    <!-- Error State -->
    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center shadow-sm">
      <AlertCircle class="w-6 h-6 text-red-500 mr-3 flex-shrink-0" />
      <p class="text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="i in 4" :key="i" class="bg-white/60 backdrop-blur-xl rounded-2xl p-6 border border-white shadow-sm animate-pulse">
        <div class="flex justify-between items-center mb-4">
          <div class="h-4 bg-slate-200 rounded w-24"></div>
          <div class="w-10 h-10 bg-slate-200 rounded-xl"></div>
        </div>
        <div class="h-10 bg-slate-200 rounded w-16 mt-4"></div>
      </div>
    </div>

    <!-- KPI Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- Total Jobs -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
        <div class="absolute -right-8 -top-8 bg-indigo-50/50 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
        <div class="relative flex items-start justify-between mb-6">
          <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Total Jobs</h3>
          <div class="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
            <Briefcase class="w-5 h-5" />
          </div>
        </div>
        <div class="relative flex items-end justify-between">
          <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.jobs || 0 }}</p>
        </div>
      </div>

      <!-- Active Jobs -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
        <div class="absolute -right-8 -top-8 bg-emerald-50/50 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
        <div class="relative flex items-start justify-between mb-6">
          <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Active Jobs</h3>
          <div class="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
            <Activity class="w-5 h-5" />
          </div>
        </div>
        <div class="relative flex items-end justify-between">
          <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.active_jobs || 0 }}</p>
        </div>
      </div>

      <!-- Applications -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
        <div class="absolute -right-8 -top-8 bg-blue-50/50 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
        <div class="relative flex items-start justify-between mb-6">
          <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Applications</h3>
          <div class="p-2 bg-blue-50 text-blue-600 rounded-xl">
            <FileText class="w-5 h-5" />
          </div>
        </div>
        <div class="relative flex items-end justify-between">
          <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.applications || 0 }}</p>
        </div>
      </div>

      <!-- Shortlisted -->
      <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
        <div class="absolute -right-8 -top-8 bg-purple-50/50 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
        <div class="relative flex items-start justify-between mb-6">
          <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Shortlisted</h3>
          <div class="p-2 bg-purple-50 text-purple-600 rounded-xl">
            <ListChecks class="w-5 h-5" />
          </div>
        </div>
        <div class="relative flex items-end justify-between">
          <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.shortlisted || 0 }}</p>
        </div>
      </div>

    </div>

    <!-- Pipeline Stats -->
    <div class="mt-10">
      <h3 class="text-lg font-bold text-slate-800 mb-5">Recruitment Pipeline</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        <!-- Interviews -->
        <div class="bg-gradient-to-br from-indigo-900 to-slate-900 rounded-2xl p-6 shadow-lg shadow-indigo-900/10 text-white flex items-center justify-between border border-indigo-800">
          <div>
            <p class="text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-2">Interviews Scheduled</p>
            <p class="text-4xl font-extrabold">{{ dashboard.interviews || 0 }}</p>
          </div>
          <div class="bg-white/10 p-4 rounded-2xl backdrop-blur-md">
            <CalendarDays class="w-8 h-8 text-indigo-200" />
          </div>
        </div>

        <!-- Selected -->
        <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 shadow-lg text-white flex items-center justify-between border border-slate-700">
          <div>
            <p class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Offers Extended</p>
            <p class="text-4xl font-extrabold">{{ dashboard.selected || 0 }}</p>
          </div>
          <div class="bg-white/5 p-4 rounded-2xl backdrop-blur-md border border-white/10">
            <CheckCircle class="w-8 h-8 text-slate-300" />
          </div>
        </div>

        <!-- Placed -->
        <div class="bg-gradient-to-br from-emerald-900 to-slate-900 rounded-2xl p-6 shadow-lg text-white flex items-center justify-between border border-emerald-800 relative overflow-hidden">
          <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10"></div>
          <div class="relative z-10">
            <p class="text-xs font-semibold text-emerald-300 uppercase tracking-widest mb-2">Successfully Placed</p>
            <p class="text-4xl font-extrabold">{{ dashboard.placed || 0 }}</p>
          </div>
          <div class="bg-emerald-500/20 p-4 rounded-2xl backdrop-blur-md border border-emerald-400/20 relative z-10">
            <Award class="w-8 h-8 text-emerald-300" />
          </div>
        </div>

      </div>
    </div>

    <!-- Upcoming Interviews Panel -->
    <div v-if="!loading && dashboard.upcoming_interviews && dashboard.upcoming_interviews.length > 0" class="pt-4">
      <div class="flex items-center justify-between mb-5">
        <h3 class="text-lg font-bold text-slate-800">Upcoming Interviews</h3>
        <router-link to="/company/interviews" class="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition flex items-center gap-1">
          View all <span aria-hidden>&rarr;</span>
        </router-link>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="interview in dashboard.upcoming_interviews" :key="interview.application_id"
          class="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all duration-200 relative overflow-hidden"
        >
          <div class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-indigo-500 to-purple-600 rounded-l-2xl"></div>
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-indigo-50 border border-indigo-100 rounded-xl flex items-center justify-center text-indigo-700 font-extrabold text-base shrink-0">
              {{ interview.student_name.charAt(0) }}
            </div>
            <div class="min-w-0">
              <p class="font-bold text-slate-900 truncate">{{ interview.student_name }}</p>
              <p class="text-slate-500 text-xs truncate flex items-center gap-1">
                <Briefcase class="w-3 h-3" />{{ interview.job_title }}
              </p>
            </div>
          </div>
          <div class="bg-slate-50 rounded-xl px-3 py-2.5 mb-4 border border-slate-100">
            <p class="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-0.5">Scheduled</p>
            <p class="text-sm font-semibold text-slate-800">{{ formatIST(interview.interview_date) }}</p>
            <p class="text-xs font-bold mt-0.5" :class="getCountdown(interview.interview_date) === 'Passed' ? 'text-red-400' : 'text-indigo-500'">
              {{ getCountdown(interview.interview_date) === 'Passed' ? '⚠ Interview Passed' : '⏰ ' + getCountdown(interview.interview_date) }}
            </p>
          </div>
          <router-link :to="`/company/interview/${interview.application_id}`"
            class="flex items-center justify-center gap-2 text-sm font-bold text-white bg-slate-900 hover:bg-indigo-600 transition rounded-xl px-4 py-2.5 w-full"
          >
            <Video class="w-4 h-4" /> Join Room
          </router-link>
        </div>
      </div>
    </div>

    <!-- Recent Applications Panel -->
    <div v-if="!loading && dashboard.recent_applications && dashboard.recent_applications.length > 0" class="pt-4">
      <div class="flex items-center justify-between mb-5">
        <h3 class="text-lg font-bold text-slate-800">Recent Applications</h3>
        <router-link to="/company/applicants" class="text-sm font-semibold text-indigo-600 hover:text-indigo-700 transition flex items-center gap-1">
          View all <span aria-hidden>&rarr;</span>
        </router-link>
      </div>
      
      <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
        <div class="divide-y divide-slate-100">
          <div v-for="app in dashboard.recent_applications" :key="app.id" class="flex items-center justify-between p-4 hover:bg-slate-50 transition-colors">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-indigo-50 border border-indigo-100 rounded-xl flex items-center justify-center text-indigo-700 font-extrabold text-base shrink-0">
                {{ app.student_name.charAt(0) }}
              </div>
              <div>
                <p class="font-bold text-slate-900">{{ app.student_name }}</p>
                <div class="flex items-center mt-0.5 text-xs text-slate-500">
                  <Briefcase class="w-3 h-3 mr-1" />
                  <span>{{ app.job_title }}</span>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <span class="px-2.5 py-1 text-xs font-bold rounded-full capitalize" :class="getStatusClass(app.status)">
                {{ app.status }}
              </span>
              <router-link :to="`/company/applicant/${app.id}`"
                class="px-3 py-1.5 text-xs font-bold text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 transition rounded-lg"
              >
                View
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios.js"
import { handleCompanyAccess } from "../../utils/companyAccess.js";
import { formatIST } from "../../utils/formatDate.js"
import { 
  Briefcase, Activity, FileText, ListChecks, 
  RefreshCcw, AlertCircle, CalendarDays, 
  CheckCircle, Award, Video
} from "lucide-vue-next"

export default {
  name: "CompanyDashboard",
  components: {
    Briefcase, Activity, FileText, ListChecks,
    RefreshCcw, AlertCircle, CalendarDays,
    CheckCircle, Award, Video
  },
  data() {
    return {
      dashboard: {},
      loading: true,
      errorMessage: "",
      countdownInterval: null
    }
  },
  async mounted() {
    await this.loadDashboard()
    this.countdownInterval = setInterval(() => { this.$forceUpdate() }, 60000)
  },
  beforeUnmount() {
    if (this.countdownInterval) clearInterval(this.countdownInterval)
  },
  methods: {
    formatIST,
    async loadDashboard() {
      this.loading = true
      try {
        const token = localStorage.getItem("access_token")
        const response = await api.get("/company/dashboard", {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.dashboard = response.data 
        this.errorMessage = ""
      } catch (error) {
        const message = error.response?.data?.message 
        if (handleCompanyAccess(this, message)){
          return
        }
        this.errorMessage = message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    getCountdown(dateStr) {
      if (!dateStr) return ""
      const normalized = dateStr.endsWith('Z') || dateStr.includes('+') ? dateStr : dateStr + '+05:30'
      const now = new Date()
      const target = new Date(normalized)
      const diffMs = target - now
      if (diffMs < 0) return "Passed"
      const diffMins = Math.floor(diffMs / 60000)
      const diffHours = Math.floor(diffMins / 60)
      const diffDays = Math.floor(diffHours / 24)
      if (diffDays > 0) return `In ${diffDays}d ${diffHours % 24}h`
      if (diffHours > 0) return `In ${diffHours}h ${diffMins % 60}m`
      return `In ${diffMins}m`
    },
    getStatusClass(status) {
      const s = (status || '').toLowerCase()
      if (s === 'applied')     return 'bg-blue-50 text-blue-700 border border-blue-200'
      if (s === 'shortlisted') return 'bg-amber-50 text-amber-700 border border-amber-200'
      if (s === 'interview')   return 'bg-indigo-50 text-indigo-700 border border-indigo-200'
      if (s === 'selected')    return 'bg-teal-50 text-teal-700 border border-teal-200'
      if (s === 'placed')      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
      if (s === 'rejected')    return 'bg-red-50 text-red-700 border border-red-200'
      return 'bg-slate-50 text-slate-600 border border-slate-200'
    }
  }
}
</script>