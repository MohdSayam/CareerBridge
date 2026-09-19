<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Manage Companies</h2>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center mb-6">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Search Card -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center">
        <Search class="w-4 h-4 text-gray-500 mr-2" />
        <h3 class="font-medium text-gray-700">Search Companies</h3>
      </div>
      <div class="p-6 flex flex-col md:flex-row gap-4">
        <input 
          type="text" 
          class="flex-1 rounded-lg border-gray-300 focus:ring-trust-blue focus:border-trust-blue shadow-sm"
          placeholder="Search by name or industry..." 
          v-model="search"
          @keyup.enter="searchCompanies"
        >
        <button @click="searchCompanies" class="bg-trust-blue hover:bg-trust-blue-light text-white px-6 py-2 rounded-lg font-medium transition shadow-sm flex items-center justify-center">
          Search
        </button>
        <button @click="resetSearch" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-medium transition flex items-center justify-center">
          Reset
        </button>
      </div>
    </div>

    <!-- Data Table -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Industry & Location</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact Details</th>
              <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="bg-white divide-y divide-gray-200">
            <tr v-for="i in 5" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
                  <div class="ml-4">
                    <div class="h-4 bg-gray-200 rounded w-32 mb-2"></div>
                    <div class="h-3 bg-gray-200 rounded w-16"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-24 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-32"></div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-4 bg-gray-200 rounded w-28"></div></td>
              <td class="px-6 py-4 whitespace-nowrap text-center"><div class="h-5 bg-gray-200 rounded-full w-20 mx-auto"></div></td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-8 bg-gray-200 rounded w-24 ml-auto"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="bg-white divide-y divide-gray-200">
            <tr v-for="company in companies" :key="company.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-gray-100 rounded-full flex items-center justify-center border border-gray-200">
                    <Building2 class="w-5 h-5 text-gray-500" />
                  </div>
                  <div class="ml-4">
                    <div class="font-medium text-gray-900">{{ company.company_name }}</div>
                    <div class="text-sm text-gray-500">ID: #{{ company.id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ company.industry }}</div>
                <div class="text-sm text-gray-500 flex items-center mt-1">
                  <MapPin class="w-3 h-3 mr-1" /> {{ company.location }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <a v-if="company.website" :href="company.website" target="_blank" class="text-sm text-trust-blue hover:text-blue-800 flex items-center font-medium">
                  <ExternalLink class="w-4 h-4 mr-1" /> Visit Website
                </a>
                <span v-else class="text-sm text-gray-400 italic">No Website</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center space-y-2">
                <div>
                  <span v-if="company.approval_status === 'approved'" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Approved</span>
                  <span v-else-if="company.approval_status === 'pending'" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Pending</span>
                  <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">Rejected</span>
                </div>
                <div v-if="company.is_blacklisted">
                  <span class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-white">Blacklisted</span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium flex items-center justify-end space-x-3">
                <select 
                  :value="company.approval_status" 
                  @change="updateStatus(company.id, $event.target.value)"
                  class="block w-32 pl-3 pr-10 py-1 text-sm border-gray-300 focus:outline-none focus:ring-trust-blue focus:border-trust-blue rounded-md"
                >
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
                <button 
                  @click="toggleBlacklist(company.id)"
                  :title="company.is_blacklisted ? 'Remove Blacklist' : 'Blacklist Company'"
                  :class="company.is_blacklisted ? 'bg-gray-100 text-gray-700 hover:bg-gray-200' : 'bg-red-50 text-red-600 hover:bg-red-100'"
                  class="p-2 rounded-lg transition border border-transparent shadow-sm"
                >
                  <ShieldAlert v-if="!company.is_blacklisted" class="w-4 h-4" />
                  <ShieldCheck v-else class="w-4 h-4" />
                </button>
              </td>
            </tr>
            <tr v-if="companies.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-gray-500">
                No companies found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../../api/axios'
import { toast } from '../../components/Toast.vue'
import { Search, AlertCircle, CheckCircle, Building2, MapPin, ShieldAlert, ShieldCheck, ExternalLink } from "lucide-vue-next"

export default {
  name: "Companies",
  components: { Search, AlertCircle, CheckCircle, Building2, MapPin, ShieldAlert, ShieldCheck, ExternalLink },
  data() {
    return {
      companies: [],
      search: "",
      loading: true,
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadCompanies()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async loadCompanies() {
      this.loading = true
      try {
        const response = await api.get("/admin/companies", { headers: this.getHeaders() })
        this.companies = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    async searchCompanies() {
      this.loading = true
      try {
        const response = await api.get("/admin/companies/search", {
          headers: this.getHeaders(),
          params: { search: this.search }
        })
        this.companies = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    async resetSearch() {
      this.search = ""
      await this.loadCompanies()
    },
    async updateStatus(companyId, status) {
      try {
        const response = await api.patch(`/admin/company/${companyId}/status`,
          { approval_status: status },
          { headers: this.getHeaders() }
        )
        toast(response.data.message, "success")
        this.errorMessage = ""
        await this.loadCompanies()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      }
    },
    async toggleBlacklist(companyId) {
      try {
        const response = await api.patch(`/admin/company/${companyId}/blacklist`, {}, {
          headers: this.getHeaders()
        })
        toast(response.data.message, "success")
        this.errorMessage = ""
        await this.loadCompanies()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Unable to connect to server'
      }
    }
  }
}
</script>