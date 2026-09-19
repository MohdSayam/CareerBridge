<template>
  <div class="space-y-6 animate-in fade-in duration-500">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">Job Postings</h2>
        <p class="text-slate-500 mt-1">Create and manage your open opportunities.</p>
      </div>
      <button @click="showForm = true" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl font-bold transition-all shadow-md shadow-indigo-600/20 hover:shadow-lg hover:-translate-y-0.5 flex items-center">
        <PlusCircle class="w-5 h-5 mr-2" /> Create New Job
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center mb-6 shadow-sm">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Job Form Modal -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="showForm" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 bg-slate-900/40 backdrop-blur-sm" @click.self="resetForm">
          <transition name="scale" appear>
            <div class="bg-white rounded-2xl shadow-2xl border border-slate-100 w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
              <!-- Modal Header -->
              <div class="px-8 py-5 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
                <div class="flex items-center">
                  <div class="p-2 bg-indigo-100 text-indigo-600 rounded-lg mr-4">
                    <Edit v-if="editingJobId" class="w-5 h-5" />
                    <PlusCircle v-else class="w-5 h-5" />
                  </div>
                  <div>
                    <h3 class="font-bold text-lg text-slate-900">{{ editingJobId ? "Edit Job Posting" : "Create New Job Posting" }}</h3>
                    <p class="text-sm text-slate-500">{{ editingJobId ? "Update the details for this position." : "Fill out the details below to publish a new opportunity." }}</p>
                  </div>
                </div>
                <button @click="resetForm" class="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition">
                  <X class="w-5 h-5" />
                </button>
              </div>
              
              <!-- Modal Body (Scrollable) -->
              <div class="p-8 overflow-y-auto custom-scrollbar flex-1 bg-white">
                <form @submit.prevent="editingJobId ? updateJob() : createJob()" class="space-y-6" id="job-form">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Job Title <span class="text-red-500">*</span></label>
                      <input type="text" v-model="form.title" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors sm:text-sm text-slate-900 font-medium">
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Salary Range <span class="text-red-500">*</span></label>
                      <select v-model="form.salary_range" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900 appearance-none">
                        <option value="" disabled>Select Salary Range</option>
                        <option value="0-5 LPA">0-5 LPA</option>
                        <option value="5-10 LPA">5-10 LPA</option>
                        <option value="10-15 LPA">10-15 LPA</option>
                        <option value="15-20 LPA">15-20 LPA</option>
                        <option value="20+ LPA">20+ LPA</option>
                      </select>
                    </div>
                    <div class="md:col-span-2">
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Job Description <span class="text-red-500">*</span></label>
                      <textarea v-model="form.description" rows="4" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors sm:text-sm text-slate-900 font-medium resize-none"></textarea>
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Skills Required</label>
                      <input type="text" v-model="form.skills_required" class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors sm:text-sm text-slate-900 font-medium" placeholder="e.g. Python, Vue, SQL">
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Experience Required <span class="text-red-500">*</span></label>
                      <select v-model="form.experience_required" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900 appearance-none">
                        <option value="" disabled>Select Experience</option>
                        <option value="Fresher">Fresher</option>
                        <option value="0-1 Years">0-1 Years</option>
                        <option value="1-2 Years">1-2 Years</option>
                        <option value="2-3 Years">2-3 Years</option>
                        <option value="3-5 Years">3-5 Years</option>
                        <option value="5+ Years">5+ Years</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Minimum CGPA <span class="text-red-500">*</span></label>
                      <input type="number" step="0.1" min="0" max="10" v-model="form.minimum_cgpa" placeholder="e.g. 7.5" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900">
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Eligible Branch <span class="text-red-500">*</span></label>
                      <select v-model="form.eligible_branch" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900 appearance-none">
                        <option value="" disabled>Select Branch</option>
                        <option value="All Branches">All Branches</option>
                        <option value="CSE">CSE</option>
                        <option value="IT">IT</option>
                        <option value="ECE">ECE</option>
                        <option value="EEE">EEE</option>
                        <option value="Mechanical">Mechanical</option>
                        <option value="Civil">Civil</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Eligible Year <span class="text-red-500">*</span></label>
                      <select v-model="form.eligible_year" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900 appearance-none">
                        <option value="" disabled>Select Year</option>
                        <option value="2024">2024</option>
                        <option value="2025">2025</option>
                        <option value="2026">2026</option>
                        <option value="2027">2027</option>
                        <option value="2024,2025">2024 & 2025</option>
                        <option value="2025,2026">2025 & 2026</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-semibold text-slate-700 mb-1.5">Application Deadline <span class="text-red-500">*</span></label>
                      <input type="datetime-local" v-model="form.application_deadline" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl sm:text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-colors font-medium text-slate-900">
                    </div>
                  </div>
                </form>
              </div>

              <!-- Modal Footer -->
              <div class="px-8 py-5 border-t border-slate-100 bg-slate-50/50 flex items-center justify-end space-x-3">
                <button type="button" @click="resetForm" class="px-6 py-2.5 rounded-xl font-bold text-slate-600 hover:bg-slate-200 hover:text-slate-900 transition-colors">
                  Cancel
                </button>
                <button type="submit" form="job-form" :disabled="saving" class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white px-8 py-2.5 rounded-xl font-bold transition-all shadow-md shadow-indigo-600/20 flex items-center">
                  <Loader2 v-if="saving" class="animate-spin h-5 w-5 mr-2" />
                  {{ saving ? 'Saving...' : (editingJobId ? 'Update Job' : 'Publish Job') }}
                </button>
              </div>
            </div>
          </transition>
        </div>
      </transition>
    </Teleport>

    <!-- Elite Job Cards -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
      <div v-for="i in 6" :key="i" class="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm animate-pulse h-64">
        <div class="h-6 bg-slate-200 rounded w-3/4 mb-4"></div>
        <div class="h-4 bg-slate-100 rounded w-1/2 mb-6"></div>
        <div class="space-y-3">
          <div class="h-4 bg-slate-100 rounded w-full"></div>
          <div class="h-4 bg-slate-100 rounded w-5/6"></div>
        </div>
      </div>
    </div>
    
    <div v-else-if="jobs.length === 0" class="bg-white rounded-2xl p-16 text-center border border-slate-100 shadow-sm mt-8">
      <div class="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center mx-auto mb-6">
        <Briefcase class="w-10 h-10 text-indigo-300" />
      </div>
      <h4 class="text-2xl font-bold text-slate-900 mb-2">No Jobs Posted Yet</h4>
      <p class="text-slate-500 mb-8 max-w-md mx-auto">Create your first job posting to start attracting top talent from across the globe.</p>
      <button @click="showForm = true" class="text-white font-bold bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-xl transition-all shadow-md hover:shadow-lg">
        Create Your First Job
      </button>
    </div>

    <div v-else class="grid grid-cols-1 xl:grid-cols-2 2xl:grid-cols-3 gap-8 mt-8">
      <div v-for="job in jobs" :key="job.id" 
           class="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1 transition-all duration-500 border border-slate-100 overflow-hidden flex flex-col group relative ring-1 ring-slate-900/5">
        
        <!-- Top Gradient Accent -->
        <div class="h-1.5 w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 opacity-60 group-hover:opacity-100 transition-opacity"></div>
        
        <div class="p-7 flex-1 flex flex-col relative">
          <!-- Absolute Floating Actions -->
          <div class="absolute top-6 right-6 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-4 group-hover:translate-x-0">
            <button @click="editJob(job)" class="w-10 h-10 rounded-full bg-white text-slate-600 hover:text-indigo-600 shadow-md border border-slate-100 flex items-center justify-center hover:scale-110 transition-transform focus:outline-none focus:ring-2 focus:ring-indigo-500 tooltip-trigger" title="Edit Job">
              <Edit class="w-4 h-4" />
            </button>
            <button v-if="job.status === 'approved'" @click="updateJobStatus(job.id, 'closed')" class="w-10 h-10 rounded-full bg-white text-slate-600 hover:text-red-500 shadow-md border border-slate-100 flex items-center justify-center hover:scale-110 transition-transform focus:outline-none focus:ring-2 focus:ring-red-500 tooltip-trigger" title="Close Job">
              <XCircle class="w-4 h-4" />
            </button>
            <button v-if="job.status === 'closed'" @click="updateJobStatus(job.id, 'approved')" class="w-10 h-10 rounded-full bg-white text-slate-600 hover:text-emerald-500 shadow-md border border-slate-100 flex items-center justify-center hover:scale-110 transition-transform focus:outline-none focus:ring-2 focus:ring-emerald-500 tooltip-trigger" title="Re-open Job">
              <CheckCircle class="w-4 h-4" />
            </button>
          </div>

          <!-- Header (Title & ID) -->
          <div class="mb-5 pr-32">
            <h3 class="text-2xl font-black text-slate-900 tracking-tight leading-none mb-2 group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-indigo-600 group-hover:to-purple-600 transition-all">{{ job.title }}</h3>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">ID: #{{ job.id }}</p>
          </div>

          <!-- Status Badge - Premium Glowing Style -->
          <div class="mb-6 flex items-center space-x-3">
            <div v-if="job.status === 'approved'" class="relative inline-flex items-center px-4 py-1.5 rounded-full overflow-hidden">
              <div class="absolute inset-0 bg-emerald-500 opacity-10"></div>
              <div class="absolute inset-0 border border-emerald-500/20 rounded-full"></div>
              <span class="relative flex h-2 w-2 mr-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span class="relative text-xs font-bold text-emerald-700 uppercase tracking-widest">Active</span>
            </div>
            
            <div v-else-if="job.status === 'pending'" class="relative inline-flex items-center px-4 py-1.5 rounded-full overflow-hidden">
              <div class="absolute inset-0 bg-amber-500 opacity-10"></div>
              <div class="absolute inset-0 border border-amber-500/20 rounded-full"></div>
              <span class="relative h-2 w-2 rounded-full bg-amber-500 mr-2 shadow-[0_0_8px_rgba(245,158,11,0.8)]"></span>
              <span class="relative text-xs font-bold text-amber-700 uppercase tracking-widest">Pending Review</span>
            </div>

            <div v-else-if="job.status === 'rejected'" class="relative inline-flex items-center px-4 py-1.5 rounded-full overflow-hidden">
              <div class="absolute inset-0 bg-red-500 opacity-10"></div>
              <div class="absolute inset-0 border border-red-500/20 rounded-full"></div>
              <span class="relative h-2 w-2 rounded-full bg-red-500 mr-2"></span>
              <span class="relative text-xs font-bold text-red-700 uppercase tracking-widest">Rejected</span>
            </div>

            <div v-else class="relative inline-flex items-center px-4 py-1.5 rounded-full overflow-hidden">
              <div class="absolute inset-0 bg-slate-500 opacity-10"></div>
              <div class="absolute inset-0 border border-slate-500/20 rounded-full"></div>
              <span class="relative h-2 w-2 rounded-full bg-slate-500 mr-2"></span>
              <span class="relative text-xs font-bold text-slate-700 uppercase tracking-widest">Closed</span>
            </div>
          </div>

          <!-- Main Info Tags -->
          <div class="flex flex-wrap gap-3 mb-8">
            <div class="inline-flex items-center px-4 py-2 rounded-xl bg-slate-50 text-slate-800 text-sm font-bold border border-slate-200/60 shadow-sm">
              <Banknote class="w-4 h-4 mr-2 text-indigo-500" /> {{ job.salary_range }}
            </div>
            <div class="inline-flex items-center px-4 py-2 rounded-xl bg-slate-50 text-slate-800 text-sm font-bold border border-slate-200/60 shadow-sm">
              <Calendar class="w-4 h-4 mr-2 text-purple-500" /> 
              {{ job.application_deadline ? new Date(job.application_deadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No Deadline' }}
            </div>
          </div>

          <!-- Detailed Info Grid - Premium Neumorphic inset -->
          <div class="bg-slate-50 rounded-2xl p-5 mb-6 border border-slate-100 shadow-inner space-y-4 flex-1">
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Experience</span>
                <span class="font-bold text-slate-800">{{ job.experience_required || 'Fresher' }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Min CGPA</span>
                <span class="font-bold text-slate-800">{{ job.minimum_cgpa || 'None' }}</span>
              </div>
              <div class="col-span-2 flex flex-col">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Eligible Branches</span>
                <span class="font-bold text-slate-800 truncate" :title="job.eligible_branch">{{ job.eligible_branch || 'All Branches' }}</span>
              </div>
            </div>
          </div>

          <!-- Footer Timestamp -->
          <div class="mt-auto pt-5 border-t border-slate-100/60 flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center mr-3">
                <Briefcase class="w-4 h-4 text-indigo-500" />
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest leading-none">Posted On</span>
                <span class="text-sm font-bold text-slate-700 mt-1">
                  {{ job.created_at ? new Date(job.created_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) : 'Recently' }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios.js"
import { toast } from "../../components/Toast.vue"
import { handleCompanyAccess } from "../../utils/companyAccess.js"
import { AlertCircle, CheckCircle, PlusCircle, Edit, Calendar, XCircle, Loader2, Briefcase, X, Banknote } from "lucide-vue-next"

export default {
  name: "CompanyJobs",
  components: { AlertCircle, CheckCircle, PlusCircle, Edit, Calendar, XCircle, Loader2, Briefcase, X, Banknote },
  data() {
    return {
      jobs: [],
      loading: true,
      saving: false,
      showForm: false,
      editingJobId: null,
      form: {
        title: "", description: "", salary_range: "", skills_required: "",
        experience_required: "", minimum_cgpa: "", eligible_branch: "",
        eligible_year: "", application_deadline: ""
      },
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadJobs()
  },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadJobs() {
      this.loading = true
      try {
        const response = await api.get("/company/jobs", { headers: this.getHeaders() })
        this.jobs = response.data
      } catch (error) {
        if (handleCompanyAccess(this, error.response?.data?.message)) return
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    async createJob() {
      this.saving = true
      try {
        const response = await api.post("/company/jobs", this.form, { headers: this.getHeaders() })
        toast(response.data.message, "success")
        this.errorMessage = ""
        this.resetForm()
        await this.loadJobs()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.saving = false
      }
    },
    editJob(job) {
      this.showForm = true
      this.editingJobId = job.id
      this.form = {
        ...job,
        application_deadline: job.application_deadline ? job.application_deadline.substring(0, 16) : ""
      }
    },
    async updateJob() {
      this.saving = true
      try {
        const response = await api.patch(`/company/job/${this.editingJobId}`, this.form, { headers: this.getHeaders() })
        toast(response.data.message, "success")
        this.errorMessage = ""
        this.resetForm()
        await this.loadJobs()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.saving = false
      }
    },
    async updateJobStatus(id, status) {
      try {
        const response = await api.patch(`/company/job/${id}/status`, { status }, { headers: this.getHeaders() })
        toast(response.data.message || `Job ${status} successfully`, "success")
        this.errorMessage = ""
        await this.loadJobs()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      }
    },
    resetForm() {
      this.showForm = false
      this.editingJobId = null
      this.form = {
        title: "", description: "", salary_range: "", skills_required: "",
        experience_required: "", minimum_cgpa: "", eligible_branch: "",
        eligible_year: "", application_deadline: ""
      }
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}
</style>