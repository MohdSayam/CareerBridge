<template>
  <div class="space-y-8 animate-in fade-in duration-500">
    <!-- Header -->
    <div class="flex items-center justify-between mb-2">
      <div>
        <div class="inline-flex items-center px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-xs font-bold uppercase tracking-widest mb-3">
          <span class="w-1.5 h-1.5 rounded-full bg-teal-500 mr-2 animate-pulse"></span>
          Overview
        </div>
        <h2 class="text-4xl font-heading font-extrabold text-slate-900 tracking-tight">Dashboard</h2>
      </div>
      <button @click="loadDashboard" class="flex items-center px-5 py-2.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:border-teal-300 hover:text-teal-700 transition-all text-slate-600 font-semibold text-sm shadow-sm group">
        <RefreshCcw class="w-4 h-4 mr-2 group-hover:rotate-180 transition-transform duration-500 text-slate-400 group-hover:text-teal-600" :class="{ 'animate-spin': loading }" /> Refresh
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 shrink-0" />
      <p class="text-red-700 font-medium text-sm">{{ errorMessage }}</p>
    </div>

    <!-- Premium Skeleton -->
    <div v-if="loading" class="space-y-8">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="relative overflow-hidden bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-100 shadow-sm h-32 animate-pulse">
          <div class="w-8 h-8 bg-slate-200/70 rounded-xl mb-4"></div>
          <div class="w-20 h-4 bg-slate-200/70 rounded-md mb-2"></div>
          <div class="w-12 h-6 bg-slate-200/70 rounded-md"></div>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="i in 3" :key="i" class="relative overflow-hidden bg-white/80 backdrop-blur-xl rounded-2xl p-6 border border-slate-100 shadow-sm h-28 animate-pulse">
           <div class="flex items-center gap-4">
             <div class="w-14 h-14 bg-slate-200/70 rounded-2xl"></div>
             <div class="space-y-2 flex-1">
               <div class="w-24 h-4 bg-slate-200/70 rounded-md"></div>
               <div class="w-16 h-6 bg-slate-200/70 rounded-md"></div>
             </div>
           </div>
        </div>
      </div>
    </div>

    <div v-else class="space-y-8">
      <!-- KPI Cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Available Jobs -->
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
          <div class="absolute -right-8 -top-8 bg-teal-50/60 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
          <div class="relative flex items-start justify-between mb-6">
            <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Open Roles</h3>
            <div class="p-2 bg-teal-50 text-teal-600 rounded-xl">
              <Briefcase class="w-5 h-5" />
            </div>
          </div>
          <div class="relative flex items-end justify-between">
            <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.available_jobs || 0 }}</p>
          </div>
          <p class="text-xs font-semibold text-slate-400 mt-1 relative">Available Jobs</p>
        </div>

        <!-- Applications -->
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
          <div class="absolute -right-8 -top-8 bg-amber-50/60 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
          <div class="relative flex items-start justify-between mb-6">
            <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Applied</h3>
            <div class="p-2 bg-amber-50 text-amber-600 rounded-xl">
              <FileText class="w-5 h-5" />
            </div>
          </div>
          <div class="relative flex items-end justify-between">
            <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.applications || 0 }}</p>
          </div>
          <p class="text-xs font-semibold text-slate-400 mt-1 relative">Total Applications</p>
        </div>

        <!-- Shortlisted -->
        <div class="bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 ring-1 ring-slate-900/5 relative overflow-hidden group">
          <div class="absolute -right-8 -top-8 bg-violet-50/60 rounded-full w-32 h-32 group-hover:scale-125 transition-transform duration-700 blur-2xl"></div>
          <div class="relative flex items-start justify-between mb-6">
            <h3 class="text-slate-500 font-medium text-sm uppercase tracking-wider">Shortlisted</h3>
            <div class="p-2 bg-violet-50 text-violet-600 rounded-xl">
              <ListChecks class="w-5 h-5" />
            </div>
          </div>
          <div class="relative flex items-end justify-between">
            <p class="text-4xl font-bold text-slate-800 tracking-tight">{{ dashboard.shortlisted || 0 }}</p>
          </div>
          <p class="text-xs font-semibold text-slate-400 mt-1 relative">Profiles Shortlisted</p>
        </div>

        <!-- Placements (Highlight) -->
        <div class="bg-gradient-to-br from-slate-900 via-teal-950 to-emerald-900 rounded-2xl p-6 shadow-lg shadow-teal-900/20 text-white relative overflow-hidden group hover:-translate-y-1 transition-all duration-300">
          <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-emerald-500/20 rounded-full blur-3xl group-hover:bg-emerald-400/30 transition-colors duration-700"></div>
          <div class="absolute top-0 right-0 w-full h-full bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-white/10 via-transparent to-transparent opacity-40"></div>
          <div class="relative flex items-start justify-between mb-6">
            <h3 class="text-emerald-200 font-medium text-sm uppercase tracking-wider">Placed</h3>
            <div class="p-2 bg-emerald-500/20 backdrop-blur-md rounded-xl border border-emerald-400/20">
              <Award class="w-5 h-5 text-emerald-300" />
            </div>
          </div>
          <div class="relative">
            <p class="text-4xl font-bold text-white tracking-tight">{{ dashboard.placed || 0 }}</p>
            <p class="text-xs font-semibold text-emerald-300 mt-1">Offers Received</p>
          </div>
        </div>
      </div>

      <!-- Upcoming Interviews -->
      <div v-if="dashboard.upcoming_interviews && dashboard.upcoming_interviews.length > 0">
        <h3 class="text-lg font-bold text-slate-800 mb-5 flex items-center">
          <CalendarDays class="w-5 h-5 mr-2 text-teal-600" /> Upcoming Interviews
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="interview in dashboard.upcoming_interviews" :key="interview.application_id"
            class="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-200 relative overflow-hidden group">
            <div class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-teal-500 to-emerald-600 rounded-l-2xl"></div>
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 bg-teal-50 border border-teal-100 rounded-xl flex items-center justify-center text-teal-700 font-extrabold text-base shrink-0">
                {{ interview.company_name.charAt(0) }}
              </div>
              <div class="min-w-0">
                <p class="font-bold text-slate-900 truncate">{{ interview.job_title }}</p>
                <p class="text-slate-500 text-xs truncate flex items-center gap-1">
                  <Building2 class="w-3 h-3" />{{ interview.company_name }}
                </p>
              </div>
            </div>
            <div class="bg-slate-50 rounded-xl px-3 py-2.5 mb-4 border border-slate-100">
              <p class="text-xs text-slate-400 font-semibold uppercase tracking-widest mb-0.5">Scheduled</p>
              <p class="text-sm font-semibold text-slate-800">{{ formatIST(interview.interview_date) }}</p>
              <p class="text-xs font-bold mt-0.5 text-teal-600">{{ getCountdown(interview.interview_date) }}</p>
            </div>
            <router-link :to="`/interview/${interview.application_id}`"
              class="flex items-center justify-center gap-2 text-sm font-bold text-white bg-slate-900 hover:bg-teal-700 transition-colors rounded-xl px-4 py-2.5 w-full">
              <Video class="w-4 h-4" /> Join Room
            </router-link>
          </div>
        </div>
      </div>

      <!-- Pipeline Stats -->
      <div>
        <h3 class="text-lg font-bold text-slate-800 mb-5">Placement Pipeline</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Interviews -->
          <div class="bg-gradient-to-br from-teal-900 to-slate-900 rounded-2xl p-6 shadow-lg shadow-teal-900/10 text-white flex items-center justify-between border border-teal-800">
            <div>
              <p class="text-xs font-semibold text-teal-300 uppercase tracking-widest mb-2">Interviews</p>
              <p class="text-4xl font-extrabold">{{ dashboard.interviews || 0 }}</p>
            </div>
            <div class="bg-white/10 p-4 rounded-2xl backdrop-blur-md">
              <CalendarDays class="w-8 h-8 text-teal-200" />
            </div>
          </div>

          <!-- Selected -->
          <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 shadow-lg text-white flex items-center justify-between border border-slate-700">
            <div>
              <p class="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Selected</p>
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
              <p class="text-xs font-semibold text-emerald-300 uppercase tracking-widest mb-2">Placements</p>
              <p class="text-4xl font-extrabold">{{ dashboard.placed || 0 }}</p>
            </div>
            <div class="bg-emerald-500/20 p-4 rounded-2xl backdrop-blur-md border border-emerald-400/20 relative z-10">
              <Award class="w-8 h-8 text-emerald-300" />
            </div>
          </div>
        </div>
      </div>

      <!-- Two Column Layout for Latest Jobs & Applications -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Latest Jobs -->
        <div v-if="dashboard.latest_jobs && dashboard.latest_jobs.length > 0" class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div class="flex items-center justify-between p-6 border-b border-slate-50">
            <h3 class="text-base font-bold text-slate-800 flex items-center">
              <Briefcase class="w-4 h-4 mr-2 text-teal-600" /> Latest Opportunities
            </h3>
            <router-link to="/student/jobs" class="text-sm font-semibold text-teal-600 hover:text-teal-700 transition flex items-center gap-1">
              View all <span aria-hidden>→</span>
            </router-link>
          </div>
          <div class="divide-y divide-slate-50">
            <router-link v-for="job in dashboard.latest_jobs" :key="job.id" :to="`/student/job/${job.id}`"
              class="flex items-center justify-between p-4 hover:bg-slate-50 transition-colors group">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-teal-50 border border-teal-100 rounded-xl flex items-center justify-center text-teal-700 font-extrabold text-base shrink-0">
                  {{ job.company.charAt(0) }}
                </div>
                <div>
                  <p class="font-bold text-slate-900 group-hover:text-teal-700 transition-colors">{{ job.title }}</p>
                  <p class="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <Building2 class="w-3 h-3" /> {{ job.company }}
                  </p>
                </div>
              </div>
              <span class="text-xs font-extrabold text-teal-700 bg-teal-50 border border-teal-100 px-2.5 py-1 rounded-lg whitespace-nowrap">{{ job.salary_range }}</span>
            </router-link>
          </div>
        </div>

        <!-- Recent Applications -->
        <div v-if="dashboard.latest_applications && dashboard.latest_applications.length > 0" class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div class="flex items-center justify-between p-6 border-b border-slate-50">
            <h3 class="text-base font-bold text-slate-800 flex items-center">
              <FileText class="w-4 h-4 mr-2 text-violet-500" /> Recent Applications
            </h3>
            <router-link to="/student/applications" class="text-sm font-semibold text-violet-600 hover:text-violet-700 transition flex items-center gap-1">
              View all <span aria-hidden>→</span>
            </router-link>
          </div>
          <div class="divide-y divide-slate-50">
            <div v-for="app in dashboard.latest_applications" :key="app.id"
              class="flex items-center justify-between p-4 hover:bg-slate-50 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-violet-50 border border-violet-100 rounded-xl flex items-center justify-center text-violet-700 font-extrabold text-base shrink-0">
                  {{ app.company_name.charAt(0) }}
                </div>
                <div>
                  <p class="font-bold text-slate-900">{{ app.job_title }}</p>
                  <p class="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <Building2 class="w-3 h-3" /> {{ app.company_name }}
                  </p>
                </div>
              </div>
              <span class="px-2.5 py-1 text-xs font-bold rounded-full capitalize" :class="getStatusClass(app.status)">
                {{ app.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios.js"
import { formatIST } from "../../utils/formatDate.js"
import { Briefcase, FileText, ListChecks, RefreshCcw, AlertCircle, CalendarDays, CheckCircle, Award, Video, Clock, Building2 } from "lucide-vue-next"

export default {
  name: "StudentDashboard",
  components: { Briefcase, FileText, ListChecks, RefreshCcw, AlertCircle, CalendarDays, CheckCircle, Award, Video, Clock, Building2 },
  data() {
    return { dashboard: {}, loading: true, errorMessage: "", countdownInterval: null }
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
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadDashboard() {
      this.loading = true
      this.errorMessage = ""
      try {
        const response = await api.get("/student/dashboard", { headers: this.getHeaders() })
        this.dashboard = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
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
      if (diffMs < 0) return "Interview has passed"
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
      if (s === 'interview')   return 'bg-teal-50 text-teal-700 border border-teal-200'
      if (s === 'selected')    return 'bg-violet-50 text-violet-700 border border-violet-200'
      if (s === 'placed')      return 'bg-emerald-50 text-emerald-700 border border-emerald-200'
      if (s === 'rejected')    return 'bg-red-50 text-red-700 border border-red-200'
      return 'bg-slate-50 text-slate-600 border border-slate-200'
    }
  }
}
</script>