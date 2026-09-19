<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Loader />
    </div>
    
    <div v-else-if="job" class="max-w-4xl mx-auto space-y-6">
      <button @click="$router.push('/student/jobs')" class="text-gray-500 hover:text-gray-900 flex items-center font-medium transition">
        <ArrowLeft class="w-4 h-4 mr-1" /> Back to Jobs
      </button>

      <!-- Header Card -->
      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-6">
          <div>
            <div class="flex items-center space-x-3 mb-2">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                Active
              </span>
              <span class="text-sm text-gray-500 font-medium">Deadline: {{ job.application_deadline ? job.application_deadline.substring(0, 10) : 'None' }}</span>
            </div>
            <h1 class="text-3xl font-heading font-bold text-gray-900 mb-2">{{ job.title }}</h1>
            <p class="text-trust-blue font-medium text-lg flex items-center">
              <Building2 class="w-5 h-5 mr-2" /> {{ job.company?.name || 'Company Name' }}
            </p>
          </div>
          <div class="w-full md:w-auto flex-shrink-0">
            <button 
              @click="applyJob(job.id)"
              :disabled="applying"
              class="w-full md:w-auto bg-trust-blue hover:bg-blue-800 disabled:bg-gray-400 text-white font-medium py-3 px-8 rounded-xl transition shadow-md flex justify-center items-center text-lg"
            >
              <Loader v-if="applying" class="w-5 h-5 mr-2" />
              <Send v-else class="w-5 h-5 mr-2" /> 
              {{ applying ? 'Applying...' : 'Apply Now' }}
            </button>
            <p v-if="successMessage" class="mt-2 text-sm text-green-600 font-medium text-center">{{ successMessage }}</p>
            <p v-if="errorMessage" class="mt-2 text-sm text-red-600 font-medium text-center">{{ errorMessage }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 pt-8 border-t border-gray-100">
          <div>
            <p class="text-sm text-gray-500 mb-1">Salary Range</p>
            <p class="font-medium text-gray-900 flex items-center"><DollarSign class="w-4 h-4 mr-1 text-gray-400"/>{{ job.salary_range }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Min CGPA</p>
            <p class="font-medium text-gray-900 flex items-center"><GraduationCap class="w-4 h-4 mr-1 text-gray-400"/>{{ job.minimum_cgpa }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Eligible Branches</p>
            <p class="font-medium text-gray-900 flex items-center"><BookOpen class="w-4 h-4 mr-1 text-gray-400"/>{{ job.eligible_branch || 'Any' }}</p>
          </div>
          <div>
            <p class="text-sm text-gray-500 mb-1">Graduation Year</p>
            <p class="font-medium text-gray-900 flex items-center"><Calendar class="w-4 h-4 mr-1 text-gray-400"/>{{ job.eligible_year || 'Any' }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Job Details -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <h2 class="text-xl font-bold text-gray-900 mb-4">Job Description</h2>
            <div class="prose max-w-none text-gray-600 whitespace-pre-wrap">
              {{ job.description }}
            </div>
            
            <div class="mt-8 space-y-6">
              <div v-if="job.skills_required">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Required Skills</h3>
                <p class="text-gray-600">{{ job.skills_required }}</p>
              </div>
              <div v-if="job.experience_required">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Experience Requirements</h3>
                <p class="text-gray-600">{{ job.experience_required }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Company Details -->
        <div class="lg:col-span-1 space-y-6">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
            <h2 class="text-xl font-bold text-gray-900 mb-4">About the Company</h2>
            <div v-if="job.company" class="space-y-4">
              <div>
                <p class="text-sm text-gray-500 mb-1">Industry</p>
                <p class="font-medium text-gray-900">{{ job.company.industry || 'Not specified' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 mb-1">Location</p>
                <p class="font-medium text-gray-900 flex items-center"><MapPin class="w-4 h-4 mr-1 text-gray-400"/>{{ job.company.location || 'Not specified' }}</p>
              </div>
              <div v-if="job.company.website">
                <p class="text-sm text-gray-500 mb-1">Website</p>
                <a :href="job.company.website" target="_blank" class="font-medium text-trust-blue hover:underline flex items-center">
                  <Globe class="w-4 h-4 mr-1"/> Visit Website
                </a>
              </div>
              <div v-if="job.company.description" class="pt-4 border-t border-gray-100">
                <p class="text-sm text-gray-600 whitespace-pre-wrap">{{ job.company.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-20 text-gray-500 font-medium">
      Job not found or no longer available.
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import Loader from "../../components/Loader.vue"
import { ArrowLeft, Building2, Send, DollarSign, GraduationCap, BookOpen, Calendar, MapPin, Globe } from "lucide-vue-next"

export default {
  name: "StudentJobDetails",
  components: { Loader, ArrowLeft, Building2, Send, DollarSign, GraduationCap, BookOpen, Calendar, MapPin, Globe },
  data() {
    return {
      job: null,
      loading: true,
      applying: false,
      successMessage: "",
      errorMessage: ""
    }
  },
  async mounted() {
    await this.fetchJobDetails()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async fetchJobDetails() {
      const jobId = this.$route.params.id;
      try {
        const response = await api.get(`/student/job/${jobId}`, { headers: this.getHeaders() })
        this.job = response.data
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async applyJob(jobId) {
      if (this.applying) return;
      this.applying = true;
      try {
        const response = await api.post(`/student/job/${jobId}/apply`, {}, { headers: this.getHeaders() })
        this.successMessage = response.data.message
        this.errorMessage = ""
        setTimeout(() => { this.successMessage = "" }, 5000)
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to apply for this job."
        this.successMessage = ""
        setTimeout(() => { this.errorMessage = "" }, 5000)
      } finally {
        this.applying = false;
      }
    }
  }
}
</script>
