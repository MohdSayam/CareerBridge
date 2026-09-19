<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Placements</h2>
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
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Placement Details</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Salary & Offer</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Dates</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="placement in placements" :key="placement.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-green-50 rounded-full flex items-center justify-center border border-green-100">
                    <Award class="w-5 h-5 text-green-500" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">Placement ID: #{{ placement.id }}</div>
                    <div class="text-sm text-gray-500">App ID: #{{ placement.application_id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-bold text-emerald-600">{{ placement.salary }}</div>
                <div class="text-sm text-gray-500 flex items-center mt-1">
                  <FileCheck class="w-3 h-3 mr-1" /> {{ placement.offer_letter_path || "No offer letter uploaded" }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">Placed On: {{ placement.placed_on }}</div>
                <div class="text-sm text-gray-500 mt-1">Joining Date: {{ placement.joining_date || "TBD" }}</div>
              </td>
            </tr>
            <tr v-if="placements.length === 0">
              <td colspan="3" class="px-6 py-8 text-center text-gray-500">
                No placements found.
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
import { AlertCircle, Award, FileCheck } from "lucide-vue-next"

export default {
  name: "Placements",
  components: { AlertCircle, Award, FileCheck },
  data() {
    return {
      placements: [],
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadPlacements()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async loadPlacements() {
      try {
        const response = await api.get("/admin/placements", { headers: this.getHeaders() })
        this.placements = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      }
    }
  }
}
</script>