<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Manage Jobs</h2>
    </div>

    <!-- Alerts -->
    <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 p-4 rounded flex items-center">
      <CheckCircle class="w-5 h-5 text-green-500 mr-2" />
      <p class="text-sm text-green-700 font-medium">{{ successMessage }}</p>
    </div>
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Data Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
        <h3 class="font-medium text-gray-700">All Job Postings</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Details</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Requirements</th>
              <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="bg-white divide-y divide-gray-200">
            <tr v-for="i in 5" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
                  <div class="ml-4">
                    <div class="h-4 bg-gray-200 rounded w-32 mb-2"></div>
                    <div class="h-3 bg-gray-200 rounded w-24"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-20 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-40"></div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center"><div class="h-5 bg-gray-200 rounded-full w-16 mx-auto"></div></td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-8 bg-gray-200 rounded w-24 ml-auto"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="bg-white divide-y divide-gray-200">
            <tr v-for="job in jobs" :key="job.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-indigo-50 rounded-full flex items-center justify-center border border-indigo-100">
                    <Briefcase class="w-5 h-5 text-indigo-500" />
                  </div>
                  <div class="ml-4">
                    <div class="font-medium text-gray-900">{{ job.title }}</div>
                    <div class="text-sm text-gray-500">
                      <span class="font-medium text-gray-700">{{ job.company_name }}</span> | Job ID: #{{ job.id }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 font-medium">{{ job.salary_range }}</div>
                <div class="text-sm text-gray-500">Min CGPA: {{ job.minimum_cgpa }} | Branches: {{ job.eligible_branch }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span v-if="job.status === 'approved'" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Approved</span>
                <span v-else-if="job.status === 'pending'" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Pending</span>
                <span v-else-if="job.status === 'rejected'" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">Rejected</span>
                <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">Closed</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <select 
                  :value="job.status" 
                  @change="updateStatus(job.id, $event.target.value)"
                  class="block w-32 ml-auto pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-trust-blue focus:border-trust-blue rounded-md shadow-sm"
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                  <option value="closed">Closed</option>
                </select>
              </td>
            </tr>
            <tr v-if="jobs.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                No jobs found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { Briefcase, AlertCircle, CheckCircle } from "lucide-vue-next"

export default {
  name: "Jobs",
  components: { Briefcase, AlertCircle, CheckCircle },
  data() {
    return {
      jobs: [],
      loading: true,
      successMessage: "",
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadJobs()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async loadJobs() {
      this.loading = true
      try {
        const response = await api.get("/admin/jobs", { headers: this.getHeaders() })
        this.jobs = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
        this.successMessage = ""
      } finally {
        this.loading = false
      }
    },
    async updateStatus(jobId, status) {
      try {
        const response = await api.patch(`/admin/job/${jobId}/status`, { status: status }, {
          headers: this.getHeaders()
        })
        this.successMessage = response.data.message
        this.errorMessage = ""
        await this.loadJobs()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
        this.successMessage = ""
      }
    }
  }
}
</script>