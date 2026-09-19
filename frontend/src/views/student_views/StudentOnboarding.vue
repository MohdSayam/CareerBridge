<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-3xl w-full bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden relative">
      
      <!-- Progress Bar -->
      <div class="absolute top-0 left-0 h-1 bg-trust-blue transition-all duration-500 ease-in-out" :style="{ width: progressPercentage + '%' }"></div>
      
      <!-- Header -->
      <div class="bg-gradient-to-r from-trust-blue to-purple-800 p-8 text-white">
        <h1 class="text-3xl font-heading font-bold mb-2">Welcome, {{ student.full_name || 'Student' }}!</h1>
        <p class="text-blue-100 text-lg">Let's complete your profile so you can start applying for jobs.</p>
        
        <!-- Step Indicators -->
        <div class="flex items-center justify-between mt-8 max-w-lg">
          <div v-for="step in 4" :key="step" class="flex flex-col items-center relative z-10">
            <div 
              class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors duration-300 border-2"
              :class="currentStep === step ? 'bg-white text-trust-blue border-white' : currentStep > step ? 'bg-emerald-400 text-white border-emerald-400' : 'bg-transparent text-blue-200 border-blue-300'"
            >
              <Check v-if="currentStep > step" class="w-5 h-5" />
              <span v-else>{{ step }}</span>
            </div>
            <span class="text-xs mt-2 font-medium" :class="currentStep >= step ? 'text-white' : 'text-blue-300'">
              {{ stepTitles[step - 1] }}
            </span>
          </div>
          <!-- Connecting Line -->
          <div class="absolute top-5 left-8 right-8 h-0.5 bg-blue-300/30 -z-10"></div>
        </div>
      </div>

      <!-- Content Area -->
      <div class="p-8 min-h-[400px] flex flex-col justify-between">
        
        <form @submit.prevent="nextStep">
          <!-- Step 1: Avatar -->
          <div v-if="currentStep === 1" class="animate-in fade-in slide-in-from-right-4 duration-500">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Your Profile Photo</h2>
            <div class="flex flex-col items-center">
              <div class="relative group cursor-pointer w-32 h-32 bg-gray-50 rounded-full shadow-lg border-4 border-white overflow-hidden mb-6 flex items-center justify-center">
                <img v-if="student.profile_picture_url" :src="student.profile_picture_url" alt="Profile" class="w-full h-full object-cover" />
                <UserCircle v-else class="w-full h-full text-gray-300" />
                <div class="absolute inset-0 bg-black/50 hidden group-hover:flex items-center justify-center backdrop-blur-sm transition-all">
                  <span class="text-white text-sm font-bold">Upload New</span>
                  <input type="file" class="absolute inset-0 opacity-0 cursor-pointer" accept="image/png, image/jpeg, image/jpg" @change="handleImageUpload">
                </div>
              </div>
              <p class="text-gray-500 text-center max-w-md">We've generated a default avatar for you. You can click it to upload a real photo of yourself if you'd like!</p>
            </div>
          </div>

          <!-- Step 2: Academics -->
          <div v-if="currentStep === 2" class="animate-in fade-in slide-in-from-right-4 duration-500">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Academic Details</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Degree / Education *</label>
                <input type="text" v-model="student.education" required placeholder="e.g. B.Tech, MCA" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Branch / Specialization *</label>
                <input type="text" v-model="student.branch" required placeholder="e.g. Computer Science" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Current CGPA *</label>
                <input type="number" step="0.01" min="0" max="10" v-model="student.cgpa" required placeholder="e.g. 8.5" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Graduation Year *</label>
                <input type="number" min="2020" max="2030" v-model="student.graduation_year" required class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition">
              </div>
            </div>
          </div>

          <!-- Step 3: Skills & Experience -->
          <div v-if="currentStep === 3" class="animate-in fade-in slide-in-from-right-4 duration-500">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Professional Profile</h2>
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Skills</label>
                <input type="text" v-model="student.skills" placeholder="Python, Vue.js, Machine Learning (comma separated)" class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Experience & Projects</label>
                <textarea v-model="student.experience" rows="4" placeholder="Briefly describe your key projects or past internships..." class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:ring-trust-blue focus:border-trust-blue transition resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Step 4: Resume -->
          <div v-if="currentStep === 4" class="animate-in fade-in slide-in-from-right-4 duration-500">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Upload Resume</h2>
            <div class="border-2 border-dashed border-blue-200 rounded-xl p-10 bg-blue-50/50 flex flex-col items-center justify-center text-center group hover:bg-blue-50 transition-colors">
              <div class="w-16 h-16 bg-white rounded-full flex items-center justify-center mb-4 shadow-sm group-hover:scale-110 transition-transform">
                <FileText class="w-8 h-8 text-trust-blue" />
              </div>
              <h3 class="text-lg font-medium text-gray-800 mb-2">Upload your latest Resume</h3>
              <p class="text-sm text-gray-500 mb-6">PDF format only (Max 5MB)</p>
              
              <div class="relative">
                <input type="file" @change="handleResumeUpload" accept=".pdf" class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-6 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-trust-blue file:text-white hover:file:bg-blue-800 cursor-pointer transition">
              </div>
              
              <div v-if="student.resume_path" class="mt-4 px-4 py-2 bg-green-50 text-green-700 rounded-lg text-sm font-medium flex items-center">
                <Check class="w-4 h-4 mr-2" /> Resume uploaded successfully
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="mt-6 bg-red-50 text-red-600 p-4 rounded-lg flex items-center text-sm font-medium">
            <AlertCircle class="w-5 h-5 mr-2 shrink-0" /> {{ errorMessage }}
          </div>

          <!-- Navigation Buttons -->
          <div class="flex justify-between items-center mt-10 pt-6 border-t border-gray-100">
            <button 
              type="button" 
              @click="prevStep" 
              class="px-6 py-2.5 text-gray-600 font-medium hover:bg-gray-100 rounded-lg transition flex items-center disabled:opacity-0"
              :disabled="currentStep === 1 || loading"
            >
              <ArrowLeft class="w-4 h-4 mr-2" /> Back
            </button>

            <button 
              v-if="currentStep < 4" 
              type="submit" 
              class="px-8 py-2.5 bg-trust-blue text-white font-bold rounded-lg hover:bg-blue-800 transition shadow-md flex items-center"
            >
              Continue <ArrowRight class="w-4 h-4 ml-2" />
            </button>

            <button 
              v-if="currentStep === 4" 
              type="button" 
              @click="submitProfile" 
              class="px-8 py-2.5 bg-emerald-500 text-white font-bold rounded-lg hover:bg-emerald-600 transition shadow-md flex items-center disabled:opacity-70 disabled:cursor-not-allowed"
              :disabled="loading"
            >
              <Loader2 v-if="loading" class="w-4 h-4 mr-2 animate-spin" />
              <span v-else>Complete Profile <Check class="w-4 h-4 ml-2" /></span>
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
import { Check, UserCircle, FileText, ArrowRight, ArrowLeft, AlertCircle, Loader2 } from "lucide-vue-next"

export default {
  name: "StudentOnboarding",
  components: { Check, UserCircle, FileText, ArrowRight, ArrowLeft, AlertCircle, Loader2 },
  data() {
    return {
      currentStep: 1,
      stepTitles: ["Avatar", "Academics", "Experience", "Resume"],
      student: {
        full_name: "",
        profile_picture_url: "",
        education: "",
        branch: "",
        cgpa: "",
        graduation_year: new Date().getFullYear() + 1,
        skills: "",
        experience: "",
        resume_path: ""
      },
      loading: false,
      errorMessage: ""
    }
  },
  computed: {
    progressPercentage() {
      return (this.currentStep / 4) * 100;
    }
  },
  async mounted() {
    await this.loadInitialProfile()
  },
  methods: {
    getHeaders() { return { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
    
    async loadInitialProfile() {
      try {
        const response = await api.get("/student/profile", { headers: this.getHeaders() })
        // Merge fetched data with our data model
        this.student = { ...this.student, ...response.data }
      } catch (error) {
        console.error("Could not fetch profile details", error)
      }
    },

    nextStep() {
      if (this.currentStep < 4) {
        this.currentStep++;
        this.errorMessage = "";
      }
    },

    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.errorMessage = "";
      }
    },

    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append("file", file);
      
      try {
        this.errorMessage = "";
        toast("Uploading avatar...", "info")
        const response = await api.post("/upload/image", formData, {
          headers: {
            ...this.getHeaders(),
            "Content-Type": "multipart/form-data"
          }
        });
        this.student.profile_picture_url = response.data.url;
        toast("Avatar uploaded successfully!", "success")
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Failed to upload image.";
      }
    },

    async handleResumeUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);
      
      try {
        this.errorMessage = "";
        toast("Uploading resume...", "info")
        const response = await api.post("/upload/resume", formData, {
          headers: {
            ...this.getHeaders(),
            "Content-Type": "multipart/form-data"
          }
        });
        this.student.resume_path = response.data.url;
        toast("Resume uploaded successfully!", "success")
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Failed to upload resume.";
      }
    },

    async submitProfile() {
      this.loading = true;
      this.errorMessage = "";
      
      try {
        await api.patch("/student/profile", {
          education: this.student.education,
          branch: this.student.branch,
          cgpa: this.student.cgpa,
          graduation_year: this.student.graduation_year,
          skills: this.student.skills,
          resume_path: this.student.resume_path,
          experience: this.student.experience
        }, {
          headers: this.getHeaders()
        });
        
        localStorage.setItem("profile_complete", "true");
        toast("Profile completed! Welcome aboard.", "success")
        this.$router.push("/student");
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Failed to save profile. Please check all fields.";
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
