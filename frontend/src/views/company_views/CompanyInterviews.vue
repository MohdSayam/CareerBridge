<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Recruitment</p>
        <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">All Interviews</h2>
      </div>
      <button @click="loadInterviews" class="flex items-center px-4 py-2 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition text-slate-600 font-semibold text-sm shadow-sm">
        <RefreshCcw class="w-4 h-4 mr-2" :class="{ 'animate-spin': loading }" /> Refresh
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 shrink-0" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Filter Tabs -->
    <div class="flex gap-2 bg-slate-100 p-1 rounded-xl w-fit">
      <button v-for="tab in tabs" :key="tab.value" @click="activeTab = tab.value"
        class="px-4 py-2 rounded-lg text-sm font-semibold transition-all"
        :class="activeTab === tab.value ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'">
        {{ tab.label }}
        <span v-if="counts[tab.value]" class="ml-1.5 px-1.5 py-0.5 text-xs font-bold rounded-full"
          :class="activeTab === tab.value ? 'bg-trust-blue text-white' : 'bg-slate-200 text-slate-500'">
          {{ counts[tab.value] }}
        </span>
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="bg-white rounded-2xl border border-slate-100 p-5 animate-pulse h-24"></div>
    </div>

    <!-- Interview Cards -->
    <div v-else class="space-y-3">
      <div v-for="interview in filteredInterviews" :key="interview.application_id"
        class="bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-5">
          <!-- Avatar -->
          <div class="w-12 h-12 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-xl flex items-center justify-center text-indigo-700 font-bold text-lg shrink-0">
            {{ interview.student_name?.charAt(0) }}
          </div>
          <!-- Info -->
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <h3 class="font-bold text-slate-900">{{ interview.student_name }}</h3>
              <span :class="getStatusClass(interview.status)" class="px-2.5 py-0.5 text-xs font-bold rounded-full border capitalize">{{ interview.status }}</span>
            </div>
            <div class="flex flex-wrap gap-4 text-sm text-slate-500">
              <span class="flex items-center gap-1.5"><Briefcase class="w-3.5 h-3.5" />{{ interview.job_title }}</span>
              <span class="flex items-center gap-1.5"><CalendarDays class="w-3.5 h-3.5" />{{ formatIST(interview.interview_date) }}</span>
              <span class="flex items-center gap-1.5 font-semibold" :class="getCountdown(interview.interview_date) === 'Passed' ? 'text-slate-400' : 'text-indigo-600'">
                <Clock class="w-3.5 h-3.5" />{{ getCountdown(interview.interview_date) }}
              </span>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex items-center gap-2 shrink-0">
            <router-link :to="`/company/applicant/${interview.application_id}`"
              class="px-3 py-2 text-sm font-semibold text-slate-600 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl transition">
              Profile
            </router-link>
            <router-link v-if="interview.status === 'interview'" :to="`/company/interview/${interview.application_id}`"
              class="flex items-center gap-2 px-4 py-2 text-sm font-bold text-white bg-slate-900 hover:bg-indigo-600 rounded-xl transition shadow-sm">
              <Video class="w-4 h-4" /> Join Room
            </router-link>
          </div>
        </div>
      </div>

      <div v-if="filteredInterviews.length === 0" class="py-20 flex flex-col items-center justify-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
        <CalendarDays class="w-12 h-12 text-slate-200 mb-3" />
        <p class="font-semibold">No interviews {{ activeTab === 'all' ? 'scheduled yet' : 'in this category' }}</p>
        <p class="text-sm mt-1">Schedule interviews from the applicant detail page.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios.js"
import { handleCompanyAccess } from "../../utils/companyAccess.js"
import { formatIST } from "../../utils/formatDate.js"
import { RefreshCcw, AlertCircle, Briefcase, CalendarDays, Clock, Video } from "lucide-vue-next"

export default {
  name: "CompanyInterviews",
  components: { RefreshCcw, AlertCircle, Briefcase, CalendarDays, Clock, Video },
  data() {
    return {
      interviews: [],
      loading: true,
      errorMessage: "",
      activeTab: "upcoming",
      tabs: [
        { label: "Upcoming", value: "upcoming" },
        { label: "Passed", value: "passed" },
        { label: "All", value: "all" }
      ]
    }
  },
  async mounted() { await this.loadInterviews() },
  computed: {
    filteredInterviews() {
      return this.interviews.filter(i => {
        if (this.activeTab === "all") return true
        const normalized = (i.interview_date || '').endsWith('Z') || (i.interview_date || '').includes('+') ? i.interview_date : (i.interview_date || '') + '+05:30'
        const isPassed = new Date(normalized) < new Date()
        if (this.activeTab === "passed") return isPassed
        if (this.activeTab === "upcoming") return !isPassed
        return true
      })
    },
    counts() {
      const now = new Date()
      return {
        upcoming: this.interviews.filter(i => {
          const n = (i.interview_date || '').endsWith('Z') || (i.interview_date || '').includes('+') ? i.interview_date : (i.interview_date || '') + '+05:30'
          return new Date(n) >= now
        }).length,
        passed: this.interviews.filter(i => {
          const n = (i.interview_date || '').endsWith('Z') || (i.interview_date || '').includes('+') ? i.interview_date : (i.interview_date || '') + '+05:30'
          return new Date(n) < now
        }).length,
        all: this.interviews.length
      }
    }
  },
  methods: {
    formatIST,
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadInterviews() {
      this.loading = true
      try {
        const response = await api.get("/company/interviews", { headers: this.getHeaders() })
        this.interviews = response.data
        this.errorMessage = ""
      } catch (error) {
        const msg = error.response?.data?.message
        if (handleCompanyAccess(this, msg)) return
        this.errorMessage = msg || "Unable to load interviews."
      } finally {
        this.loading = false
      }
    },
    getCountdown(dateStr) {
      if (!dateStr) return "—"
      const normalized = dateStr.endsWith('Z') || dateStr.includes('+') ? dateStr : dateStr + '+05:30'
      const diffMs = new Date(normalized) - new Date()
      if (diffMs < 0) return "Passed"
      const mins = Math.floor(diffMs / 60000)
      const hours = Math.floor(mins / 60)
      const days = Math.floor(hours / 24)
      if (days > 0) return `In ${days}d ${hours % 24}h`
      if (hours > 0) return `In ${hours}h ${mins % 60}m`
      return `In ${mins}m`
    },
    getStatusClass(status) {
      const s = (status || '').toLowerCase()
      if (s === 'interview') return 'bg-indigo-50 text-indigo-700 border-indigo-200'
      if (s === 'selected')  return 'bg-amber-50 text-amber-700 border-amber-200'
      if (s === 'placed')    return 'bg-emerald-50 text-emerald-700 border-emerald-200'
      if (s === 'rejected')  return 'bg-red-50 text-red-700 border-red-200'
      return 'bg-slate-50 text-slate-600 border-slate-200'
    }
  }
}
</script>
