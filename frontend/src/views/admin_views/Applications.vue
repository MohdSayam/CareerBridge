<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">All Applications</h2>
    </div>

    <!-- Alerts -->
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Data Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Candidate & Role</th>
              <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timeline</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feedback</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="bg-white divide-y divide-gray-200">
            <tr v-for="i in 5" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-32 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-48"></div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center"><div class="h-6 bg-gray-200 rounded-full w-20 mx-auto"></div></td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-28 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-36"></div>
              </td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-40"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="bg-white divide-y divide-gray-200">
            <tr v-for="app in applications" :key="app.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-gray-900">{{ app.student_name }}</div>
                <div class="text-sm text-gray-500 font-medium mt-0.5">
                  {{ app.job_title }} <span class="font-normal text-gray-400">at</span> {{ app.company_name }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border" :class="getStatusBadgeClass(app.status)">
                  {{ app.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">Applied: {{ formatDate(app.applied_at) }}</div>
                <div class="text-sm text-gray-500 flex items-center mt-1">
                  <CalendarDays class="w-3 h-3 mr-1" /> Interview: {{ formatDate(app.interview_date) || "Not Scheduled" }}
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-500 truncate max-w-xs" :title="app.feedback">
                  {{ app.feedback || "No feedback yet" }}
                </div>
              </td>
            </tr>
            <tr v-if="applications.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-gray-500">
                No applications found.
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
import { AlertCircle, CalendarDays } from "lucide-vue-next"

export default {
  name: "Applications",
  components: { AlertCircle, CalendarDays },
  data() {
    return {
      applications: [],
      loading: true,
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadApplications()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async loadApplications() {
      this.loading = true
      try {
        const response = await api.get("/admin/applications", { headers: this.getHeaders() })
        this.applications = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return null;
      return new Date(dateStr).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    },
    getStatusBadgeClass(status) {
      const s = (status || "").toLowerCase()
      if (s === 'applied') return 'bg-blue-50 text-blue-700 border-blue-200'
      if (s === 'shortlisted') return 'bg-purple-50 text-purple-700 border-purple-200'
      if (s === 'interview') return 'bg-indigo-50 text-indigo-700 border-indigo-200'
      if (s === 'selected') return 'bg-yellow-50 text-yellow-700 border-yellow-200'
      if (s === 'placed') return 'bg-green-50 text-green-700 border-green-200'
      if (s === 'rejected') return 'bg-red-50 text-red-700 border-red-200'
      return 'bg-gray-50 text-gray-700 border-gray-200'
    }
  }
}
</script>