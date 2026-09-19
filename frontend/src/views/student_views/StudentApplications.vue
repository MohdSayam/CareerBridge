<template>
  <div class="space-y-6">
    <div>
      <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Track</p>
      <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">My Applications</h2>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 shrink-0" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="bg-white rounded-2xl border border-slate-100 p-5 animate-pulse flex items-center gap-4">
        <div class="w-12 h-12 bg-slate-100 rounded-xl shrink-0"></div>
        <div class="flex-1 space-y-2"><div class="h-4 bg-slate-100 rounded w-1/3"></div><div class="h-3 bg-slate-100 rounded w-1/4"></div></div>
        <div class="h-6 bg-slate-100 rounded-full w-20"></div>
      </div>
    </div>

    <!-- Application Cards -->
    <div v-else class="space-y-3">
      <div v-for="app in applications" :key="app.application_id"
        class="bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden">
        <div class="p-5 flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <!-- Icon -->
          <div class="w-12 h-12 bg-slate-50 border border-slate-100 rounded-xl flex items-center justify-center shrink-0">
            <FileText class="w-5 h-5 text-slate-400" />
          </div>
          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h3 class="font-bold text-slate-900 truncate">{{ app.job_title }}</h3>
              <span :class="getStatusClass(app.status)" class="px-2.5 py-0.5 text-xs font-bold rounded-full border whitespace-nowrap capitalize">{{ app.status }}</span>
            </div>
            <div class="flex flex-wrap gap-4 text-sm text-slate-500">
              <span class="flex items-center gap-1.5"><Clock class="w-3.5 h-3.5" /> Applied {{ formatIST(app.applied_at) }}</span>
              <span v-if="app.interview_date" class="flex items-center gap-1.5 text-indigo-600 font-semibold">
                <CalendarDays class="w-3.5 h-3.5" /> Interview: {{ formatIST(app.interview_date) }}
              </span>
            </div>
            <p v-if="app.feedback" class="mt-2 text-sm text-slate-600 bg-slate-50 border border-slate-100 rounded-lg px-3 py-1.5 max-w-md truncate" :title="app.feedback">
              {{ app.feedback }}
            </p>
          </div>
          <!-- Action -->
          <button v-if="app.status === 'interview'" @click="joinInterview(app.application_id)"
            class="flex items-center text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2.5 rounded-xl transition shadow-sm shrink-0">
            <Video class="w-4 h-4 mr-1.5" /> Join Room
          </button>
        </div>
      </div>

      <div v-if="applications.length === 0" class="py-20 flex flex-col items-center justify-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
        <FileText class="w-12 h-12 text-slate-200 mb-3" />
        <p class="font-semibold">No applications yet</p>
        <p class="text-sm mt-1">Browse the job board and start applying.</p>
        <router-link to="/student/jobs" class="mt-4 px-5 py-2.5 bg-trust-blue text-white rounded-xl font-semibold text-sm hover:bg-blue-700 transition">Browse Jobs</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { formatIST } from "../../utils/formatDate"
import { AlertCircle, FileText, Video, Clock, CalendarDays } from "lucide-vue-next"

export default {
  name: "StudentApplications",
  components: { AlertCircle, FileText, Video, Clock, CalendarDays },
  data() {
    return { applications: [], loading: true, errorMessage: "" }
  },
  async mounted() { await this.loadApplications() },
  methods: {
    formatIST,
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadApplications() {
      this.loading = true
      try {
        const response = await api.get("/student/applications", { headers: this.getHeaders() })
        this.applications = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    getStatusClass(status) {
      const s = (status || '').toLowerCase()
      if (s === 'applied')     return 'bg-slate-50 text-slate-600 border-slate-200'
      if (s === 'shortlisted') return 'bg-blue-50 text-blue-700 border-blue-200'
      if (s === 'interview')   return 'bg-indigo-50 text-indigo-700 border-indigo-200'
      if (s === 'selected')    return 'bg-amber-50 text-amber-700 border-amber-200'
      if (s === 'placed')      return 'bg-emerald-50 text-emerald-700 border-emerald-200'
      if (s === 'rejected')    return 'bg-red-50 text-red-700 border-red-200'
      return 'bg-slate-50 text-slate-600 border-slate-200'
    },
    joinInterview(appId) { this.$router.push(`/interview/${appId}`) }
  }
}
</script>
