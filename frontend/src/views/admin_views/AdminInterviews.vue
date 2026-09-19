<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Interviews Tracking</h2>
    </div>

    <!-- Alert -->
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center shadow-sm">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Stats Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-indigo-50 border border-indigo-100 rounded-xl p-4 shadow-sm">
        <p class="text-xs text-indigo-600 font-bold uppercase tracking-wider mb-1">Total Interviews</p>
        <p class="text-2xl font-bold text-indigo-900">{{ interviews.length }}</p>
      </div>
      <div class="bg-yellow-50 border border-yellow-100 rounded-xl p-4 shadow-sm">
        <p class="text-xs text-yellow-600 font-bold uppercase tracking-wider mb-1">Upcoming / Ongoing</p>
        <p class="text-2xl font-bold text-yellow-900">{{ pendingCount }}</p>
      </div>
      <div class="bg-green-50 border border-green-100 rounded-xl p-4 shadow-sm">
        <p class="text-xs text-green-600 font-bold uppercase tracking-wider mb-1">Selected / Placed</p>
        <p class="text-2xl font-bold text-green-900">{{ successCount }}</p>
      </div>
      <div class="bg-red-50 border border-red-100 rounded-xl p-4 shadow-sm">
        <p class="text-xs text-red-600 font-bold uppercase tracking-wider mb-1">Rejected</p>
        <p class="text-2xl font-bold text-red-900">{{ rejectedCount }}</p>
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Candidate & Role</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Interview Date</th>
              <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company Feedback</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="bg-white divide-y divide-gray-200">
            <tr v-for="i in 4" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
                  <div class="ml-4">
                    <div class="h-4 bg-gray-200 rounded w-32 mb-2"></div>
                    <div class="h-3 bg-gray-200 rounded w-48"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-4 bg-gray-200 rounded w-28"></div></td>
              <td class="px-6 py-4 whitespace-nowrap text-center"><div class="h-5 bg-gray-200 rounded-full w-20 mx-auto"></div></td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-40"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="bg-white divide-y divide-gray-200">
            <tr v-for="interview in sortedInterviews" :key="interview.application_id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-indigo-50 rounded-full flex items-center justify-center border border-indigo-100">
                    <Video class="w-5 h-5 text-indigo-600" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-bold text-gray-900">{{ interview.student_name }}</div>
                    <div class="text-xs text-gray-500 font-medium">{{ interview.job_title }} at <span class="text-gray-800">{{ interview.company_name }}</span></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ formatIST(interview.interview_date) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span :class="getStatusBadgeClass(interview.status)" class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide border">
                  {{ interview.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-600 bg-gray-50 p-2 rounded border border-gray-100 max-w-xs line-clamp-2" :title="interview.feedback">
                  {{ interview.feedback || "No feedback yet" }}
                </div>
              </td>
            </tr>
            <tr v-if="interviews.length === 0">
              <td colspan="4" class="px-6 py-12 text-center text-gray-500">
                <Calendar class="w-12 h-12 mx-auto text-gray-300 mb-3" />
                <p class="text-lg font-medium text-gray-700">No interviews scheduled yet</p>
                <p class="text-sm">When companies schedule interviews, they will appear here.</p>
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
import { formatIST } from "../../utils/formatDate"
import { AlertCircle, Video, Calendar } from "lucide-vue-next"

export default {
  name: "AdminInterviews",
  components: { AlertCircle, Video, Calendar },
  data() {
    return {
      interviews: [],
      loading: true,
      errorMessage: ""
    }
  },
  computed: {
    sortedInterviews() {
      // Sort by newest interview date first
      return [...this.interviews].sort((a, b) => new Date(b.interview_date) - new Date(a.interview_date))
    },
    pendingCount() {
      return this.interviews.filter(i => i.status === 'interview').length
    },
    successCount() {
      return this.interviews.filter(i => i.status === 'selected' || i.status === 'placed').length
    },
    rejectedCount() {
      return this.interviews.filter(i => i.status === 'rejected').length
    }
  },
  async mounted() {
    await this.loadInterviews()
  },
  methods: {
    formatIST,
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadInterviews() {
      this.loading = true
      try {
        const response = await api.get("/admin/interviews", { headers: this.getHeaders() })
        this.interviews = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to load interviews"
      } finally {
        this.loading = false
      }
    },
    getStatusBadgeClass(status) {
      const s = status.toLowerCase()
      if (s === 'interview') return 'bg-indigo-100 text-indigo-800 border-indigo-200'
      if (s === 'selected') return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      if (s === 'placed') return 'bg-green-100 text-green-800 border-green-200'
      if (s === 'rejected') return 'bg-red-100 text-red-800 border-red-200'
      return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }
}
</script>
