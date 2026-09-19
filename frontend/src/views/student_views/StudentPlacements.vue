<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">My Placements</h2>
    </div>

    <!-- Alerts -->
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Placements Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="placement in placements" :key="placement.id" class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden relative group hover:shadow-lg transition duration-300">
        <!-- Confetti/Celebratory background accent -->
        <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-gradient-to-br from-yellow-300 to-yellow-500 rounded-full opacity-20 group-hover:scale-150 transition duration-700"></div>
        
        <div class="p-8 relative z-10">
          <div class="flex items-center justify-between mb-6">
            <div class="bg-premium-gold/10 p-3 rounded-2xl">
              <Award class="w-8 h-8 text-premium-gold" />
            </div>
            <span class="bg-green-100 text-green-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
              Offer Accepted
            </span>
          </div>
          
          <h3 class="text-2xl font-bold text-gray-900 mb-1">Company Offer</h3>
          <p class="text-gray-500 text-sm mb-6 pb-6 border-b border-gray-100">Placement Record #{{ placement.id }}</p>

          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-gray-500 flex items-center text-sm"><DollarSign class="w-4 h-4 mr-2 text-gray-400" /> Package</span>
              <span class="font-bold text-emerald-600 text-lg">{{ placement.salary }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-gray-500 flex items-center text-sm"><CalendarDays class="w-4 h-4 mr-2 text-gray-400" /> Placed On</span>
              <span class="font-medium text-gray-900">{{ placement.placed_on.substring(0, 10) }}</span>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-gray-500 flex items-center text-sm"><Briefcase class="w-4 h-4 mr-2 text-gray-400" /> Joining Date</span>
              <span class="font-medium text-gray-900">{{ placement.joining_date || 'To be decided' }}</span>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-gray-100">
            <a 
              v-if="placement.offer_letter_path" 
              :href="placement.offer_letter_path" 
              target="_blank"
              class="w-full flex items-center justify-center bg-gray-900 hover:bg-black text-white font-medium py-2.5 rounded-lg transition shadow-sm"
            >
              <FileDown class="w-4 h-4 mr-2" /> Download Offer Letter
            </a>
            <button 
              v-else 
              disabled
              class="w-full flex items-center justify-center bg-gray-100 text-gray-400 font-medium py-2.5 rounded-lg cursor-not-allowed"
            >
              <FileX class="w-4 h-4 mr-2" /> No Offer Letter Uploaded
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="placements.length === 0" class="col-span-full py-16 flex flex-col items-center justify-center text-center bg-white rounded-2xl border border-gray-100 border-dashed">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
          <Award class="w-8 h-8 text-gray-300" />
        </div>
        <h3 class="text-lg font-bold text-gray-700 mb-1">No Placements Yet</h3>
        <p class="text-gray-500 max-w-sm">Keep applying and preparing for interviews. Your success story is just around the corner!</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { AlertCircle, Award, DollarSign, CalendarDays, Briefcase, FileDown, FileX } from "lucide-vue-next"

export default {
  name: "StudentPlacements",
  components: { AlertCircle, Award, DollarSign, CalendarDays, Briefcase, FileDown, FileX },
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
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadPlacements() {
      try {
        const response = await api.get("/student/placements", { headers: this.getHeaders() })
        this.placements = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      }
    }
  }
}
</script>