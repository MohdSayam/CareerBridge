<template>
  <div class="space-y-6 flex flex-col h-[calc(100vh-6rem)]">
    <!-- Header -->
    <div class="flex justify-between items-center flex-shrink-0">
      <div>
        <h2 class="text-2xl font-heading font-bold text-gray-800">Applicant Tracking (ATS)</h2>
        <p v-if="selectedJob" class="text-sm text-gray-500 mt-1 flex items-center">
          <button @click="selectedJob = null; applications = []" class="text-emerald-600 hover:underline flex items-center mr-2 font-semibold">
            <ArrowLeft class="w-3.5 h-3.5 mr-1" /> Back to jobs
          </button>
          Viewing Pipeline for: <span class="font-bold text-gray-800 ml-1">{{ selectedJobTitle }}</span>
        </p>
      </div>
    </div>

    <!-- Alert -->
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center shadow-sm flex-shrink-0">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- ========= STEP 1: Job Cards ========= -->
    <div v-if="!selectedJob" class="flex-1 overflow-auto">
      <div v-if="loadingJobs" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 3" :key="i" class="bg-white rounded-xl border border-gray-100 p-5 animate-pulse shadow-sm">
          <div class="h-5 bg-gray-200 rounded w-2/3 mb-3"></div>
          <div class="h-3 bg-gray-100 rounded w-1/2 mb-2"></div>
          <div class="h-3 bg-gray-100 rounded w-1/3"></div>
        </div>
      </div>

      <div v-else-if="jobs.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-6">
        <button
          v-for="job in jobs"
          :key="job.id"
          @click="selectJob(job)"
          class="bg-white rounded-xl border border-gray-100 p-6 text-left hover:border-emerald-400 hover:shadow-lg hover:-translate-y-1 transition-all group"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="w-12 h-12 bg-emerald-50 rounded-xl flex items-center justify-center group-hover:bg-emerald-100 transition">
              <Briefcase class="w-6 h-6 text-emerald-600" />
            </div>
            <span class="text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider shadow-sm" :class="job.status === 'approved' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
              {{ job.status }}
            </span>
          </div>
          <h3 class="font-bold text-gray-900 text-lg group-hover:text-emerald-700 transition mb-1">{{ job.title }}</h3>
          <p class="text-sm text-gray-500 mb-4">Deadline: {{ job.application_deadline ? job.application_deadline.substring(0,10) : 'N/A' }}</p>
          <div class="flex items-center text-emerald-600 text-sm font-bold bg-emerald-50 px-4 py-2 rounded-lg group-hover:bg-emerald-100 transition">
            View ATS Pipeline <ArrowRight class="w-4 h-4 ml-2" />
          </div>
        </button>
      </div>

      <div v-else class="bg-gray-50 border-2 border-dashed border-gray-200 rounded-xl p-12 flex flex-col items-center text-center">
        <Briefcase class="w-12 h-12 text-gray-300 mb-3" />
        <h3 class="text-lg font-bold text-gray-700 mb-1">No jobs posted yet</h3>
        <p class="text-sm text-gray-500">Post a job first to start managing applicants.</p>
      </div>
    </div>

    <!-- ========= STEP 2: ATS Kanban Board ========= -->
    <div v-else class="flex-1 flex overflow-x-auto pb-4 gap-6 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
      <!-- Loading -->
      <div v-if="loading" class="w-full flex justify-center items-center min-h-[400px]">
        <div class="flex flex-col items-center">
          <Loader2 class="w-10 h-10 animate-spin text-emerald-500 mb-3" />
          <p class="text-gray-500 font-medium">Loading applicant pipeline...</p>
        </div>
      </div>

      <!-- Columns -->
      <template v-else>
        <div v-for="column in kanbanColumns" :key="column.status" class="w-80 flex-shrink-0 flex flex-col h-full bg-gray-50/80 rounded-2xl border border-gray-200/60 shadow-sm overflow-hidden">
          
          <!-- Column Header -->
          <div class="p-4 border-b border-gray-200/80 bg-white flex justify-between items-center shadow-sm z-10">
            <h3 class="font-bold text-gray-800 capitalize flex items-center text-sm tracking-wide">
              <div class="w-2.5 h-2.5 rounded-full mr-2.5" :class="column.colorClass"></div>
              {{ column.label }}
            </h3>
            <span class="bg-gray-100 text-gray-600 py-0.5 px-2.5 rounded-full text-xs font-bold border border-gray-200">
              {{ column.apps.length }}
            </span>
          </div>

          <!-- Cards Area -->
          <div class="flex-1 overflow-y-auto p-4 space-y-4">
             <div v-if="column.apps.length === 0" class="h-full flex flex-col items-center justify-center text-center opacity-60">
                <div class="w-12 h-12 border-2 border-dashed border-gray-300 rounded-full flex items-center justify-center mb-2">
                  <Users class="w-5 h-5 text-gray-400" />
                </div>
                <p class="text-xs font-medium text-gray-500">No candidates here</p>
             </div>
             
             <!-- Candidate Card -->
             <div 
               v-for="app in column.apps" 
               :key="app.application_id" 
               @click="$router.push(`/company/applicant/${app.application_id}`)"
               class="bg-white p-4 rounded-xl shadow-sm border border-gray-200 hover:border-emerald-400 hover:shadow-md cursor-pointer transition group"
             >
               <div class="flex items-start mb-3">
                 <div v-if="app.profile_picture_url" class="w-10 h-10 rounded-full overflow-hidden mr-3 border border-gray-100 shadow-sm flex-shrink-0">
                   <img :src="app.profile_picture_url" alt="Profile" class="w-full h-full object-cover">
                 </div>
                 <div v-else class="w-10 h-10 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-600 font-bold mr-3 border border-emerald-100 shadow-sm flex-shrink-0">
                   {{ app.student_name.charAt(0) }}
                 </div>
                 <div class="overflow-hidden">
                   <h4 class="font-bold text-gray-800 text-sm group-hover:text-emerald-700 transition truncate">{{ app.student_name }}</h4>
                   <p class="text-[11px] text-gray-500 mt-0.5 truncate">{{ app.branch }}</p>
                 </div>
               </div>
               
               <div class="flex items-center justify-between mt-2 pt-3 border-t border-gray-50">
                 <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-gray-50 text-gray-600 border border-gray-100 flex items-center">
                   <Target class="w-3 h-3 mr-1 text-emerald-500" /> {{ app.cgpa }} CGPA
                 </span>
                 <span class="text-[10px] font-bold text-emerald-600 group-hover:underline flex items-center">
                   Manage <ArrowRight class="w-3 h-3 ml-0.5" />
                 </span>
               </div>
             </div>
          </div>

        </div>
      </template>
    </div>

  </div>
</template>

<script>
import api from "../../api/axios.js"
import { handleCompanyAccess } from "../../utils/companyAccess.js"
import { AlertCircle, Briefcase, ArrowRight, ArrowLeft, Users, Loader2, Target } from "lucide-vue-next"

export default {
  name: "CompanyApplicants",
  components: { AlertCircle, Briefcase, ArrowRight, ArrowLeft, Users, Loader2, Target },
  data() {
    return {
      jobs: [],
      selectedJob: null,
      selectedJobTitle: "",
      applications: [],
      loading: false,
      loadingJobs: true,
      errorMessage: ""
    }
  },
  computed: {
    kanbanColumns() {
      // Define the fixed columns we want in our Kanban board
      const columns = [
        { status: 'applied', label: 'New Applied', colorClass: 'bg-blue-400' },
        { status: 'shortlisted', label: 'Shortlisted', colorClass: 'bg-indigo-400' },
        { status: 'interview', label: 'Interviewing', colorClass: 'bg-purple-400' },
        { status: 'selected', label: 'Selected', colorClass: 'bg-teal-400' },
        { status: 'placed', label: 'Placed / Hired', colorClass: 'bg-green-500' },
        { status: 'rejected', label: 'Rejected', colorClass: 'bg-red-400' }
      ]

      // Group applications by status
      const groups = {}
      this.applications.forEach(app => {
        if (!groups[app.status]) groups[app.status] = []
        groups[app.status].push(app)
      })

      // Map to columns with their apps
      return columns.map(col => ({
        ...col,
        apps: groups[col.status] || []
      }))
    }
  },
  async mounted() {
    await this.loadJobs()
  },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadJobs() {
      this.loadingJobs = true
      try {
        const response = await api.get("/company/jobs", { headers: this.getHeaders() })
        this.jobs = response.data
      } catch (error) {
        if (handleCompanyAccess(this, error.response?.data?.message)) return
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loadingJobs = false
      }
    },
    async selectJob(job) {
      this.selectedJob = job.id
      this.selectedJobTitle = job.title
      this.applications = []
      await this.loadApplications()
    },
    async loadApplications() {
      if (!this.selectedJob) return
      this.loading = true
      try {
        const response = await api.get(`/company/job/${this.selectedJob}/applications`, { headers: this.getHeaders() })
        this.applications = response.data
        this.errorMessage = ""
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to load applications"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>