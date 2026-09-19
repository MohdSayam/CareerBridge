<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Placements Tracker</h2>
    </div>

    <!-- Error/Success states -->
    <div v-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center shadow-sm">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ error }}</p>
    </div>

    <!-- Stats summary -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center">
        <div class="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center mr-4">
          <Award class="w-6 h-6 text-emerald-600" />
        </div>
        <div>
          <p class="text-sm text-gray-500 font-medium">Total Placements</p>
          <h4 class="text-2xl font-bold text-gray-900">{{ placements.length }}</h4>
        </div>
      </div>
    </div>

    <!-- Placements Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div v-if="!loading && placements.length === 0" class="p-12 text-center">
        <div class="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <Briefcase class="w-10 h-10 text-gray-400" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-1">No placements yet</h3>
        <p class="text-gray-500">When students are hired, their placements will appear here.</p>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="text-xs text-gray-500 uppercase bg-gray-50/50 border-b border-gray-100">
            <tr>
              <th class="px-6 py-4 font-medium">Candidate</th>
              <th class="px-6 py-4 font-medium">Role & Company</th>
              <th class="px-6 py-4 font-medium">Salary</th>
              <th class="px-6 py-4 font-medium">Joining Date</th>
              <th class="px-6 py-4 font-medium">Placed On</th>
              <th class="px-6 py-4 font-medium">Offer Letter</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="divide-y divide-gray-100">
            <tr v-for="i in 5" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></td>
              <td class="px-6 py-4">
                <div class="h-4 bg-gray-200 rounded w-32 mb-1"></div>
                <div class="h-3 bg-gray-200 rounded w-20"></div>
              </td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-16"></div></td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-24"></div></td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-28"></div></td>
              <td class="px-6 py-4"><div class="h-4 bg-gray-200 rounded w-20"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="divide-y divide-gray-100">
            <tr v-for="placement in placements" :key="placement.id" class="hover:bg-gray-50/50 transition-colors">
              <td class="px-6 py-4 font-medium text-gray-900">{{ placement.student_name }}</td>
              <td class="px-6 py-4 text-gray-600">
                <div class="font-medium text-gray-800">{{ placement.job_title }}</div>
                <div class="text-xs text-gray-500 mt-1">{{ placement.company_name }}</div>
              </td>
              <td class="px-6 py-4 font-medium text-emerald-600">{{ placement.salary }}</td>
              <td class="px-6 py-4 text-gray-600">{{ formatDate(placement.joining_date) }}</td>
              <td class="px-6 py-4 text-gray-500 text-xs">{{ formatDateTime(placement.placed_on) }}</td>
              <td class="px-6 py-4">
                <a v-if="placement.offer_letter_path" :href="placement.offer_letter_path" target="_blank" class="inline-flex items-center text-trust-blue hover:text-blue-800 transition">
                  <FileText class="w-4 h-4 mr-1" /> View Offer
                </a>
                <span v-else class="text-gray-400 text-xs">Not provided</span>
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
import { AlertCircle, Loader2, Award, Briefcase, FileText } from "lucide-vue-next"

export default {
  name: "AdminPlacements",
  components: {
    AlertCircle, Loader2, Award, Briefcase, FileText
  },
  data() {
    return {
      placements: [],
      loading: true,
      error: ""
    }
  },
  async mounted() {
    await this.fetchPlacements()
  },
  methods: {
    async fetchPlacements() {
      this.loading = true
      this.error = ""
      try {
        const response = await api.get("/admin/placements", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`
          }
        })
        this.placements = response.data
      } catch (err) {
        this.error = err.response?.data?.message || "Failed to load placements"
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return "N/A"
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
    },
    formatDateTime(dateString) {
      if (!dateString) return "N/A"
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>
