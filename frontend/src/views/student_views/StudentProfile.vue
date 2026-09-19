<template>
  <div class="w-full space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">My Profile</h2>
      <button v-if="!isEditing" @click="openEdit" class="flex items-center px-4 py-2.5 bg-trust-blue hover:bg-blue-700 text-white font-semibold rounded-xl transition-all shadow-md hover:-translate-y-0.5">
        <Edit class="w-4 h-4 mr-2" /> Edit Profile
      </button>
    </div>

    <div v-if="errorMessage" class="bg-red-50 border border-red-100 p-4 rounded-xl flex items-center shadow-sm">
      <AlertCircle class="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
      <p class="text-sm text-red-700 font-medium">{{ errorMessage }}</p>
    </div>

    <div v-if="isProfileIncomplete" class="bg-amber-50 border border-amber-100 p-4 rounded-xl flex items-center shadow-sm">
      <AlertCircle class="w-5 h-5 text-amber-500 mr-3 flex-shrink-0" />
      <p class="text-sm text-amber-700 font-medium">Please complete your profile details to access the dashboard and apply for jobs.</p>
    </div>

    <!-- Read-Only View -->
    <div v-if="!isEditing" class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
      <div class="h-44 relative bg-gradient-to-r from-trust-blue via-indigo-700 to-purple-800 overflow-hidden">
        <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20"></div>
        <div class="absolute inset-0 bg-gradient-to-t from-slate-900/70 to-transparent"></div>
      </div>
      <div class="px-8 sm:px-12 pb-10">
        <div class="relative -mt-14 flex flex-col sm:flex-row items-center sm:items-end mb-10 z-10">
          <div class="relative group cursor-pointer w-28 h-28 sm:w-32 sm:h-32 bg-white rounded-2xl flex items-center justify-center shadow-2xl ring-4 ring-white overflow-hidden shrink-0">
            <img v-if="student.profile_picture_url" :src="student.profile_picture_url" alt="Profile" class="w-full h-full object-cover" />
            <UserCircle v-else class="w-16 h-16 text-slate-300" />
            <div class="absolute inset-0 bg-slate-900/60 hidden group-hover:flex items-center justify-center transition-all backdrop-blur-sm">
              <div class="text-center">
                <Upload class="w-5 h-5 text-white mx-auto mb-1" />
                <span class="text-xs text-white font-bold uppercase">Photo</span>
              </div>
              <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" accept="image/png, image/jpeg, image/jpg" @change="handleImageUpload">
            </div>
          </div>
          <div class="mt-4 sm:mt-0 sm:ml-6 text-center sm:text-left flex-1">
            <h3 class="text-3xl font-heading font-extrabold text-slate-900 tracking-tight">{{ student.full_name || 'Loading...' }}</h3>
            <p class="text-trust-blue flex items-center justify-center sm:justify-start mt-1 font-semibold">
              <GraduationCap class="w-4 h-4 mr-1.5" /> {{ student.education || 'Degree' }} · {{ student.branch || 'Branch' }} · {{ student.graduation_year || 'YYYY' }}
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 bg-slate-50 rounded-2xl p-8 border border-slate-100">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">CGPA</p>
            <p class="text-slate-800 font-semibold flex items-center"><Target class="w-4 h-4 mr-2 text-emerald-500" />{{ student.cgpa || 'N/A' }}</p>
          </div>
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Resume</p>
            <p class="text-slate-800 font-semibold flex items-center truncate">
              <FileText class="w-4 h-4 mr-2 text-rose-500 shrink-0" />
              <a v-if="student.resume_path" :href="student.resume_path" target="_blank" class="text-trust-blue hover:underline truncate">View Document</a>
              <span v-else class="text-slate-400 italic">Not uploaded</span>
            </p>
          </div>
          <div class="lg:col-span-3 mt-2">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Skills</p>
            <div class="flex flex-wrap gap-2">
              <span v-if="!student.skills" class="text-slate-400 italic text-sm">No skills added</span>
              <span v-for="s in (student.skills ? student.skills.split(',') : [])" :key="s" class="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-lg text-sm font-semibold border border-indigo-100">{{ s.trim() }}</span>
            </div>
          </div>
          <div class="md:col-span-2 lg:col-span-3 pt-4 border-t border-slate-200/60">
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Experience & Projects</p>
            <p class="text-slate-700 leading-relaxed max-w-4xl whitespace-pre-line">{{ student.experience || 'No experience details provided.' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Inline Edit Form -->
    <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden animate-in fade-in duration-300">
      <div class="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
        <h3 class="text-xl font-bold text-slate-900">Edit Profile</h3>
        <button @click="isEditing = false" class="text-slate-400 hover:text-slate-700 bg-white hover:bg-slate-100 p-2 rounded-full transition border border-slate-200">
          <X class="w-5 h-5" />
        </button>
      </div>
      <div class="p-8">
        <form @submit.prevent="saveProfileChanges" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Full Name</label>
              <input type="text" v-model="student.full_name" disabled class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-400 cursor-not-allowed sm:text-sm font-medium">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Education <span class="text-red-500">*</span></label>
              <input type="text" v-model="form.education" placeholder="e.g. B.Tech, MCA" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Branch <span class="text-red-500">*</span></label>
              <select v-model="form.branch" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium">
                <option value="" disabled>Select Branch</option>
                <option>CSE</option><option>IT</option><option>ECE</option><option>EEE</option><option>Mechanical</option><option>Civil</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Graduation Year <span class="text-red-500">*</span></label>
              <select v-model="form.graduation_year" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium">
                <option value="" disabled>Select Year</option>
                <option>2024</option><option>2025</option><option>2026</option><option>2027</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">CGPA <span class="text-red-500">*</span></label>
              <input type="number" step="0.01" min="0" max="10" v-model="form.cgpa" placeholder="e.g. 8.5" required class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Skills (comma separated)</label>
              <input type="text" v-model="form.skills" placeholder="Python, Vue.js, SQL" class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium">
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-slate-700 mb-1.5 flex items-center justify-between">
                Resume (PDF)
                <a v-if="student.resume_path" :href="student.resume_path" target="_blank" class="text-xs font-bold text-trust-blue hover:underline bg-blue-50 px-3 py-1 rounded-full border border-blue-100">View Current</a>
              </label>
              <input type="file" @change="handleResumeUpload" accept=".pdf" class="block w-full px-4 py-3 border border-slate-200 rounded-xl bg-slate-50 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-bold file:bg-blue-50 file:text-trust-blue hover:file:bg-blue-100 transition cursor-pointer sm:text-sm">
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-semibold text-slate-700 mb-1.5">Experience & Projects</label>
              <textarea v-model="form.experience" rows="5" placeholder="Describe your internships, projects and open source contributions..." class="block w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-trust-blue/20 focus:border-trust-blue transition sm:text-sm text-slate-900 font-medium resize-none"></textarea>
            </div>
          </div>
          <div class="pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button type="button" @click="isEditing = false" class="px-6 py-3 rounded-xl font-semibold text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 transition">Cancel</button>
            <button type="submit" :disabled="saving" class="px-8 py-3 rounded-xl font-bold text-white bg-trust-blue hover:bg-blue-700 disabled:opacity-60 transition shadow-md flex items-center">
              <svg v-if="saving" class="animate-spin w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/></svg>
              <Save v-else class="w-4 h-4 mr-2" />
              {{ saving ? 'Saving...' : 'Save Profile' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { toast } from "../../components/Toast.vue"
import { AlertCircle, GraduationCap, UserCircle, Save, Edit, X, Target, FileText, Upload } from "lucide-vue-next"

export default {
  name: "StudentProfile",
  components: { AlertCircle, GraduationCap, UserCircle, Save, Edit, X, Target, FileText, Upload },
  data() {
    return {
      student: {},
      form: { education: '', branch: '', cgpa: '', graduation_year: '', skills: '', experience: '' },
      isEditing: false,
      saving: false,
      errorMessage: "",
      isProfileIncomplete: localStorage.getItem("profile_complete") === "false"
    }
  },
  async mounted() { await this.loadProfile() },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    async loadProfile() {
      try {
        const response = await api.get("/student/profile", { headers: this.getHeaders() })
        this.student = response.data
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Unable to load profile."
      }
    },
    openEdit() {
      this.form = {
        education: this.student.education || '',
        branch: this.student.branch || '',
        cgpa: this.student.cgpa || '',
        graduation_year: this.student.graduation_year || '',
        skills: this.student.skills || '',
        experience: this.student.experience || ''
      }
      this.isEditing = true
    },
    async saveProfileChanges() {
      this.saving = true
      try {
        const response = await api.patch("/student/profile", {
          education: this.form.education,
          branch: this.form.branch,
          cgpa: this.form.cgpa,
          graduation_year: this.form.graduation_year,
          skills: this.form.skills,
          experience: this.form.experience
        }, { headers: this.getHeaders() })
        toast(response.data.message, "success")
        this.student = { ...this.student, ...this.form }
        this.isEditing = false
        this.errorMessage = ""
        if (this.isProfileIncomplete) {
          localStorage.setItem("profile_complete", "true")
          this.isProfileIncomplete = false
          setTimeout(() => { this.$router.push("/student") }, 1500)
        }
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
        this.student.profile_picture_url = response.data.url
        toast("Profile photo updated!", "success")
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Image upload failed."
      }
    },
    async handleResumeUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      const formData = new FormData()
      formData.append("file", file)
      try {
        const response = await api.post("/upload/resume", formData, {
          headers: { ...this.getHeaders(), "Content-Type": "multipart/form-data" }
        })
        this.student.resume_path = response.data.url
        toast("Resume uploaded!", "success")
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Resume upload failed."
      }
    }
  }
}
</script>