<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <h2 class="text-3xl font-heading font-bold text-trust-blue">Admin Overview</h2>
      <div class="flex space-x-2">
        <button @click="loadDashboard" class="p-2 bg-platinum-grey rounded-full hover:bg-gray-200 transition text-trust-blue">
          <RefreshCcw class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-md flex items-center">
      <AlertCircle class="w-6 h-6 text-red-500 mr-3" />
      <p class="text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
      <div v-for="i in 4" :key="'kpi'+i" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-32">
        <div class="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div class="h-8 bg-gray-200 rounded w-1/3"></div>
      </div>
    </div>
    
    <!-- KPI Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Students -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] hover:-translate-y-1 transition duration-300 border border-gray-100 relative overflow-hidden group">
        <div class="absolute -right-6 -top-6 bg-blue-50 rounded-full w-24 h-24 group-hover:scale-110 transition duration-500"></div>
        <div class="relative flex items-center justify-between mb-4">
          <h3 class="text-gray-500 font-medium">Total Students</h3>
          <Users class="w-6 h-6 text-trust-blue" />
        </div>
        <p class="text-4xl font-heading font-bold text-gray-800 relative">{{ dashboard.student_count || 0 }}</p>
      </div>

      <!-- Companies -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] hover:-translate-y-1 transition duration-300 border border-gray-100 relative overflow-hidden group">
        <div class="absolute -right-6 -top-6 bg-green-50 rounded-full w-24 h-24 group-hover:scale-110 transition duration-500"></div>
        <div class="relative flex items-center justify-between mb-4">
          <h3 class="text-gray-500 font-medium">Companies</h3>
          <Building2 class="w-6 h-6 text-emerald-green" />
        </div>
        <p class="text-4xl font-heading font-bold text-gray-800 relative">{{ dashboard.company_count || 0 }}</p>
        <p class="text-sm text-emerald-green font-medium mt-2 relative">{{ dashboard.approved_companies || 0 }} Approved</p>
      </div>

      <!-- Jobs -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] hover:-translate-y-1 transition duration-300 border border-gray-100 relative overflow-hidden group">
        <div class="absolute -right-6 -top-6 bg-purple-50 rounded-full w-24 h-24 group-hover:scale-110 transition duration-500"></div>
        <div class="relative flex items-center justify-between mb-4">
          <h3 class="text-gray-500 font-medium">Jobs Posted</h3>
          <Briefcase class="w-6 h-6 text-purple-500" />
        </div>
        <p class="text-4xl font-heading font-bold text-gray-800 relative">{{ dashboard.job_count || 0 }}</p>
      </div>

      <!-- Applications -->
      <div class="bg-white rounded-2xl p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] hover:-translate-y-1 transition duration-300 border border-gray-100 relative overflow-hidden group">
        <div class="absolute -right-6 -top-6 bg-orange-50 rounded-full w-24 h-24 group-hover:scale-110 transition duration-500"></div>
        <div class="relative flex items-center justify-between mb-4">
          <h3 class="text-gray-500 font-medium">Applications</h3>
          <FileText class="w-6 h-6 text-premium-gold" />
        </div>
        <p class="text-4xl font-heading font-bold text-gray-800 relative">{{ dashboard.application_count || 0 }}</p>
      </div>
    </div>

    <!-- Application Funnel Stats -->
    <h3 class="text-xl font-heading font-semibold text-gray-800 mt-8 mb-4">Placement Funnel</h3>
    
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-pulse">
      <div v-for="i in 4" :key="'funnel'+i" class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-40"></div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      
      <!-- Shortlisted -->
      <div class="bg-gradient-to-br from-blue-50 to-white rounded-2xl p-6 shadow-sm border border-blue-100 flex flex-col items-center justify-center text-center">
        <div class="bg-blue-100 p-3 rounded-full mb-3 text-trust-blue">
          <ListChecks class="w-6 h-6" />
        </div>
        <p class="text-3xl font-bold text-gray-800">{{ dashboard.shortlisted || 0 }}</p>
        <p class="text-sm font-medium text-gray-500 uppercase tracking-wider mt-1">Shortlisted</p>
      </div>

      <!-- Interviews -->
      <div class="bg-gradient-to-br from-yellow-50 to-white rounded-2xl p-6 shadow-sm border border-yellow-100 flex flex-col items-center justify-center text-center">
        <div class="bg-yellow-100 p-3 rounded-full mb-3 text-yellow-600">
          <CalendarDays class="w-6 h-6" />
        </div>
        <p class="text-3xl font-bold text-gray-800">{{ dashboard.interviews || 0 }}</p>
        <p class="text-sm font-medium text-gray-500 uppercase tracking-wider mt-1">Interviews</p>
      </div>

      <!-- Selected -->
      <div class="bg-gradient-to-br from-emerald-50 to-white rounded-2xl p-6 shadow-sm border border-emerald-100 flex flex-col items-center justify-center text-center">
        <div class="bg-emerald-100 p-3 rounded-full mb-3 text-emerald-green">
          <CheckCircle class="w-6 h-6" />
        </div>
        <p class="text-3xl font-bold text-gray-800">{{ dashboard.selected || 0 }}</p>
        <p class="text-sm font-medium text-gray-500 uppercase tracking-wider mt-1">Selected</p>
      </div>

      <!-- Placed -->
      <div class="bg-gradient-to-br from-green-50 to-white rounded-2xl p-6 shadow-sm border border-green-200 flex flex-col items-center justify-center text-center relative overflow-hidden">
        <div class="absolute top-0 w-full h-1 bg-emerald-green"></div>
        <div class="bg-green-100 p-3 rounded-full mb-3 text-green-700">
          <Award class="w-6 h-6" />
        </div>
        <p class="text-3xl font-bold text-gray-800">{{ dashboard.placed_students || 0 }}</p>
        <p class="text-sm font-medium text-green-700 uppercase tracking-wider mt-1">Total Placed</p>
      </div>

    </div>

    <!-- Analytics Chart -->
    <h3 class="text-xl font-heading font-semibold text-gray-800 mt-8 mb-4">Placements Overview</h3>
    <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-8 h-80">
      <Bar v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
      <div v-else class="h-full flex items-center justify-center text-gray-400">Loading chart data...</div>
    </div>

  </div>
</template>

<script>
import api from "../../api/axios"
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { 
  Users, Building2, Briefcase, FileText, 
  RefreshCcw, AlertCircle, ListChecks, 
  CalendarDays, CheckCircle, Award 
} from "lucide-vue-next"

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: "AdminDashboard",
  components: {
    Users, Building2, Briefcase, FileText,
    RefreshCcw, AlertCircle, ListChecks,
    CalendarDays, CheckCircle, Award,
    Bar
  },
  data() {
    return {
      dashboard: {},
      errorMessage: "",
      loading: true,
      chartData: {
        labels: [],
        datasets: [{ data: [], backgroundColor: '#10b981', borderRadius: 8 }]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true }
        }
      }
    }
  },
  async mounted() {
    await this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      this.errorMessage = ""
      this.loading = true
      try {
        const token = localStorage.getItem("access_token")
        const response = await api.get("/admin/dashboard", {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.dashboard = response.data
        
        // Populate chart
        this.chartData.labels = ['Shortlisted', 'Interviews', 'Selected', 'Placed']
        this.chartData.datasets[0].data = [
          this.dashboard.shortlisted || 0,
          this.dashboard.interviews || 0,
          this.dashboard.selected || 0,
          this.dashboard.placed_students || 0
        ]
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.message
        } else {
          this.errorMessage = "Unable to connect to server"
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>