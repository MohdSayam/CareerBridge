<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-heading font-bold text-gray-800">Manage Students</h2>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded flex items-center mb-6">
      <AlertCircle class="w-5 h-5 text-red-500 mr-2" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Search Card -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center">
        <Search class="w-4 h-4 text-gray-500 mr-2" />
        <h3 class="font-medium text-gray-700">Search Directory</h3>
      </div>
      <div class="p-6 flex flex-col md:flex-row gap-4">
        <input 
          type="text" 
          class="flex-1 rounded-lg border-gray-300 focus:ring-trust-blue focus:border-trust-blue shadow-sm"
          placeholder="Search by name or branch..." 
          v-model="search"
          @keyup.enter="searchStudents"
        >
        <button @click="searchStudents" class="bg-trust-blue hover:bg-trust-blue-light text-white px-6 py-2 rounded-lg font-medium transition shadow-sm flex items-center justify-center">
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
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student Details</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Academics</th>
              <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Resume</th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          
          <tbody v-if="loading" class="bg-white divide-y divide-gray-200">
            <tr v-for="i in 5" :key="'skel'+i" class="animate-pulse">
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-4 bg-gray-200 rounded w-8"></div></td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-32 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-24"></div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="h-4 bg-gray-200 rounded w-20 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-28"></div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-5 bg-gray-200 rounded-full w-20 mx-auto"></div></td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-4 bg-gray-200 rounded w-16"></div></td>
              <td class="px-6 py-4 whitespace-nowrap"><div class="h-8 bg-gray-200 rounded w-8 ml-auto"></div></td>
            </tr>
          </tbody>

          <tbody v-else class="bg-white divide-y divide-gray-200">
            <tr v-for="student in students" :key="student.id" class="hover:bg-gray-50 transition">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{{ student.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="font-medium text-gray-900">{{ student.full_name }}</div>
                <div class="text-sm text-gray-500">{{ student.branch }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900 font-medium">{{ student.cgpa }} CGPA</div>
                <div class="text-sm text-gray-500">Class of {{ student.graduation_year }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-center">
                <span v-if="student.is_blacklisted" class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                  Blacklisted
                </span>
                <span v-else class="px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <a v-if="student.resume_path" :href="student.resume_path" target="_blank" class="text-trust-blue hover:text-blue-800 flex items-center font-medium">
                  <FileText class="w-4 h-4 mr-1" /> View Resume
                </a>
                <span v-else class="text-gray-400 italic">Not Uploaded</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button 
                  @click="toggleBlacklist(student.id)"
                  :title="student.is_blacklisted ? 'Remove Blacklist' : 'Blacklist Student'"
                  :class="student.is_blacklisted ? 'bg-gray-100 text-gray-700 hover:bg-gray-200' : 'bg-red-50 text-red-600 hover:bg-red-100'"
                  class="p-2 rounded-lg transition border border-transparent shadow-sm"
                >
                  <ShieldAlert v-if="!student.is_blacklisted" class="w-4 h-4" />
                  <ShieldCheck v-else class="w-4 h-4" />
                </button>
              </td>
            </tr>
            <tr v-if="students.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                No students found.
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
import { toast } from "../../components/Toast.vue"
import { Search, AlertCircle, ShieldAlert, ShieldCheck, FileText } from "lucide-vue-next"

export default {
  name: "Students",
  components: { Search, AlertCircle, ShieldAlert, ShieldCheck, FileText },
  data() {
    return {
      students: [],
      search: "",
      loading: true,
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadStudents()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },
    async loadStudents() {
      this.loading = true
      try {
        const response = await api.get("/admin/students", { headers: this.getHeaders() })
        this.students = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    async searchStudents() {
      this.loading = true
      try {
        const response = await api.get("/admin/students/search", {
          headers: this.getHeaders(),
          params: { search: this.search }
        })
        this.students = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      } finally {
        this.loading = false
      }
    },
    async resetSearch() {
      this.search = ""
      await this.loadStudents()
    },
    async toggleBlacklist(studentId) {
      try {
        const response = await api.patch(`/admin/student/${studentId}/blacklist`, {}, {
          headers: this.getHeaders()
        })
        toast(response.data.message, "success")
        this.errorMessage = ""
        await this.loadStudents()
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to connect to server"
      }
    }
  }
}
</script>