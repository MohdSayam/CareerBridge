<template>
  <div class="space-y-6">
    <div class="flex justify-between items-start">
      <div>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Opportunities</p>
        <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">Job Board</h2>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="i in 6" :key="i" class="bg-white rounded-2xl border border-slate-100 p-6 animate-pulse h-64">
        <div class="flex gap-3 mb-5">
          <div class="w-12 h-12 bg-slate-100 rounded-xl shrink-0"></div>
          <div class="flex-1 space-y-2 pt-1">
            <div class="h-4 bg-slate-100 rounded w-3/4"></div>
            <div class="h-3 bg-slate-100 rounded w-1/2"></div>
          </div>
        </div>
        <div class="space-y-2">
          <div class="h-3 bg-slate-100 rounded"></div>
          <div class="h-3 bg-slate-100 rounded w-5/6"></div>
          <div class="h-3 bg-slate-100 rounded w-4/6"></div>
        </div>
      </div>
    </div>

    <!-- Job Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <div v-for="job in jobs" :key="job.id"
        class="bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 overflow-hidden flex flex-col group">
        <div class="p-6 flex-grow">
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-11 h-11 bg-gradient-to-br from-trust-blue/10 to-indigo-100 rounded-xl flex items-center justify-center shrink-0">
                <Briefcase class="w-5 h-5 text-trust-blue" />
              </div>
              <div>
                <h3 class="font-bold text-slate-900 text-lg leading-tight line-clamp-1">{{ job.title }}</h3>
                <p class="text-trust-blue font-semibold text-sm flex items-center mt-0.5">
                  <Building2 class="w-3.5 h-3.5 mr-1" />{{ job.company }}
                </p>
              </div>
            </div>
            <span class="px-2.5 py-1 bg-emerald-50 text-emerald-700 border border-emerald-100 text-xs font-bold rounded-full whitespace-nowrap">Active</span>
          </div>

          <div class="grid grid-cols-2 gap-2 mb-4">
            <div class="flex items-center bg-slate-50 rounded-lg px-3 py-2">
              <DollarSign class="w-3.5 h-3.5 text-slate-400 mr-1.5 shrink-0" />
              <span class="text-xs text-slate-700 font-medium truncate">{{ job.salary_range }}</span>
            </div>
            <div class="flex items-center bg-slate-50 rounded-lg px-3 py-2">
              <GraduationCap class="w-3.5 h-3.5 text-slate-400 mr-1.5 shrink-0" />
              <span class="text-xs text-slate-700 font-medium">{{ job.minimum_cgpa }}+ CGPA</span>
            </div>
            <div class="flex items-center bg-slate-50 rounded-lg px-3 py-2">
              <BookOpen class="w-3.5 h-3.5 text-slate-400 mr-1.5 shrink-0" />
              <span class="text-xs text-slate-700 font-medium truncate">{{ job.eligible_branch }}</span>
            </div>
            <div class="flex items-center bg-amber-50 rounded-lg px-3 py-2">
              <Calendar class="w-3.5 h-3.5 text-amber-500 mr-1.5 shrink-0" />
              <span class="text-xs text-amber-700 font-semibold">{{ formatDeadline(job.application_deadline) }}</span>
            </div>
          </div>

          <p class="text-sm text-slate-500 line-clamp-2 leading-relaxed">{{ job.description }}</p>
        </div>

        <div class="px-6 py-4 border-t border-slate-100 bg-slate-50/50 flex gap-2">
          <router-link :to="`/student/job/${job.id}`"
            class="flex-1 bg-white border border-slate-200 text-slate-700 hover:border-trust-blue hover:text-trust-blue font-semibold py-2.5 px-4 rounded-xl transition text-center text-sm">
            View Details
          </router-link>
          <button @click="applyJob(job.id)"
            :disabled="applying.has(job.id)"
            class="flex-1 bg-trust-blue hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-2.5 px-4 rounded-xl transition text-sm flex justify-center items-center shadow-sm">
            <svg v-if="applying.has(job.id)" class="animate-spin w-3.5 h-3.5 mr-1.5" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
            <Send v-else class="w-3.5 h-3.5 mr-1.5" />
            {{ applying.has(job.id) ? 'Applying...' : 'Apply' }}
          </button>
        </div>
      </div>

      <div v-if="jobs.length === 0" class="col-span-full py-20 flex flex-col items-center justify-center text-slate-400 bg-white rounded-2xl border border-dashed border-slate-200">
        <Briefcase class="w-12 h-12 text-slate-200 mb-3" />
        <p class="font-semibold">No jobs currently available</p>
        <p class="text-sm mt-1">Check back soon for new opportunities.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { toast } from "../../components/Toast.vue"
import { formatISTDate } from "../../utils/formatDate"
import { Briefcase, Building2, DollarSign, GraduationCap, BookOpen, Calendar, Send } from "lucide-vue-next"

export default {
  name: "StudentJobs",
  components: { Briefcase, Building2, DollarSign, GraduationCap, BookOpen, Calendar, Send },
  data() {
    return { jobs: [], loading: true, applying: new Set() }
  },
  async mounted() { await this.loadJobs() },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadJobs() {
      try {
        this.loading = true
        const response = await api.get("/student/jobs", { headers: this.getHeaders() })
        this.jobs = response.data
      } catch (error) {
        toast(error.response?.data?.message || "Unable to load jobs.", "error")
      } finally {
        this.loading = false
      }
    },
    formatDeadline(dateStr) {
      if (!dateStr) return 'No deadline'
      return formatISTDate(dateStr)
    },
    async applyJob(jobId) {
      if (this.applying.has(jobId)) return
      this.applying = new Set([...this.applying, jobId])
      try {
        const response = await api.post(`/student/job/${jobId}/apply`, {}, { headers: this.getHeaders() })
        toast(response.data.message || 'Applied successfully!', 'success')
      } catch (error) {
        toast(error.response?.data?.message || 'Unable to apply.', 'error')
      } finally {
        const next = new Set(this.applying)
        next.delete(jobId)
        this.applying = next
      }
    }
  }
}
</script>