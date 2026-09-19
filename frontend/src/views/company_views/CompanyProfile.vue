<template>
  <div class="w-full space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">Company Profile</h2>
      <button v-if="!isEditing" @click="openEdit" class="flex items-center px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition-all shadow-md hover:-translate-y-0.5">
        <Edit class="w-4 h-4 mr-2" /> Edit Profile
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center shadow-sm">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <!-- Read-Only View -->
    <div v-if="!isEditing" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
      <!-- Banner -->
      <div class="h-44 relative bg-gradient-to-r from-indigo-900 via-purple-900 to-slate-900 overflow-hidden">
        <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-slate-900/70 to-transparent"></div>
      </div>
      <div class="px-8 sm:px-12 pb-10">
        <div class="relative -mt-14 flex flex-col sm:flex-row items-center sm:items-end mb-10 z-10">
          <div class="relative group cursor-pointer w-28 h-28 sm:w-32 sm:h-32 bg-white rounded-2xl flex items-center justify-center shadow-2xl ring-4 ring-white overflow-hidden shrink-0">
            <img v-if="company.profile_picture_url" :src="company.profile_picture_url" alt="Logo" class="w-full h-full object-cover" />
            <Building2 v-else class="w-14 h-14 text-slate-300" />
            <div class="absolute inset-0 bg-slate-900/60 hidden group-hover:flex items-center justify-center transition-all backdrop-blur-sm">
              <div class="text-center">
                <Upload class="w-5 h-5 text-white mx-auto mb-1" />
                <span class="text-xs text-white font-bold uppercase">Upload</span>
              </div>
              <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" accept="image/png, image/jpeg, image/jpg" @change="handleImageUpload">
            </div>
          </div>
          <div class="mt-4 sm:mt-0 sm:ml-6 text-center sm:text-left flex-1">
            <h3 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">{{ company.company_name || '...' }}</h3>
            <p class="text-indigo-600 flex items-center justify-center sm:justify-start mt-1 font-semibold">
              <MapPin class="w-4 h-4 mr-1.5" /> {{ company.location || 'Location not set' }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 bg-slate-50 rounded-2xl p-8 border border-slate-100">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Industry</p>
            <p class="text-slate-800 font-semibold flex items-center"><Briefcase class="w-4 h-4 mr-2 text-purple-500" />{{ company.industry || 'Not specified' }}</p>
          </div>
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Website</p>
            <p class="text-slate-800 font-semibold flex items-center truncate">
              <Globe class="w-4 h-4 mr-2 text-indigo-500 shrink-0" />
              <a v-if="company.website" :href="company.website" target="_blank" class="text-indigo-600 hover:underline truncate">{{ company.website }}</a>
              <span v-else class="text-slate-400 italic">Not specified</span>
            </p>
          </div>
          <div class="md:col-span-2 lg:col-span-3 pt-4 border-t border-slate-200/60">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">About Company</p>
            <p class="text-slate-700 leading-relaxed whitespace-pre-line">{{ company.description || 'No description provided.' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Inline Edit Form -->
    <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden animate-in fade-in duration-300">
      <div class="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h3 class="text-xl font-bold text-slate-900">Edit Company Profile</h3>
        <button @click="isEditing = false" class="text-slate-400 hover:text-slate-700 bg-white hover:bg-slate-100 p-2 rounded-full transition border border-slate-200">
          <X class="w-5 h-5" />
        </button>
      </div>
      <div class="p-8">
        <form @submit.prevent="saveProfileChanges" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Industry <span class="text-red-500">*</span></label>
              <input type="text" v-model="form.industry" placeholder="e.g. Technology, Finance" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition sm:text-sm text-slate-900 font-medium">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Location <span class="text-red-500">*</span></label>
              <input type="text" v-model="form.location" placeholder="City, Country" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition sm:text-sm text-slate-900 font-medium">
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Website URL</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none"><Globe class="h-5 w-5 text-slate-400" /></div>
                <input type="url" v-model="form.website" placeholder="https://www.example.com" class="block w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition sm:text-sm text-slate-900 font-medium">
              </div>
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Company Description</label>
              <textarea v-model="form.description" rows="5" placeholder="Tell us about your company..." class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition sm:text-sm text-slate-900 font-medium resize-none"></textarea>
            </div>
          </div>
          <div class="pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button type="button" @click="isEditing = false" class="px-6 py-3 rounded-xl font-semibold text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 transition">Cancel</button>
            <button type="submit" :disabled="saving" class="px-8 py-3 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 transition shadow-md flex items-center">
              <svg v-if="saving" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
              <Save v-else class="w-4 h-4 mr-2" />
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios.js"
import { toast } from "../../components/Toast.vue"
import { handleCompanyAccess } from "../../utils/companyAccess.js"
import { AlertCircle, CheckCircle, Building2, MapPin, Save, Edit, X, Globe, Upload, Briefcase } from "lucide-vue-next"

export default {
  name: "CompanyProfile",
  components: { AlertCircle, CheckCircle, Building2, MapPin, Save, Edit, X, Globe, Upload, Briefcase },
  data() {
    return {
      company: {},
      form: { industry: '', location: '', website: '', description: '' },
      isEditing: false,
      saving: false,
      errorMessage: ""
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadProfile() {
      try {
        const response = await api.get("/company/profile", { headers: this.getHeaders() })
        this.company = response.data
        this.form = {
          industry: this.company.industry || '',
          location: this.company.location || '',
          website: this.company.website || '',
          description: this.company.description || ''
        }
      } catch (error) {
        if (handleCompanyAccess(this, error.response?.data?.message)) return
        this.errorMessage = error.response?.data?.message || "Unable to load profile."
      }
    },
    openEdit() {
      this.form = {
        industry: this.company.industry || '',
        location: this.company.location || '',
        website: this.company.website || '',
        description: this.company.description || ''
      }
      this.isEditing = true
    },
    async saveProfileChanges() {
      this.saving = true
      try {
        const response = await api.patch("/company/profile", {
          industry: this.form.industry,
          location: this.form.location,
          website: this.form.website,
          description: this.form.description
        }, { headers: this.getHeaders() })
        toast(response.data.message, "success")
        this.company = { ...this.company, ...this.form }
        this.isEditing = false
        this.errorMessage = ""
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to update profile."
      } finally {
        this.saving = false
      }
    },
    async handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      const formData = new FormData()
      formData.append("file", file)
      try {
        const response = await api.post("/upload/image", formData, {
          headers: { ...this.getHeaders(), "Content-Type": "multipart/form-data" }
        })
        this.company.profile_picture_url = response.data.url
        toast("Company logo updated!", "success")
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Image upload failed."
      }
    }
  }
}
</script>