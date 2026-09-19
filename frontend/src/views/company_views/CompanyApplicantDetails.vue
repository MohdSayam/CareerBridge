<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center">
        <router-link to="/company/applicants" class="p-2 mr-3 bg-white border border-gray-200 text-gray-500 rounded-lg hover:bg-gray-50 hover:text-emerald-600 transition shadow-sm">
          <ArrowLeft class="w-5 h-5" />
        </router-link>
        <div>
          <h2 class="text-2xl font-heading font-bold text-gray-800">Application Details</h2>
          <p class="text-sm text-gray-500 font-medium">Tracking candidate progress for <span class="text-emerald-600 font-bold">{{ app.job_title || 'loading...' }}</span></p>
        </div>
      </div>
      <span class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm" :class="getStatusBadgeClass(app.status)">
        {{ app.status || 'loading...' }}
      </span>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="flex justify-center items-center py-20 bg-white rounded-2xl border border-gray-100 shadow-sm">
      <Loader2 class="w-8 h-8 animate-spin text-emerald-500" />
      <span class="ml-3 text-emerald-700 font-medium">Loading candidate profile...</span>
    </div>

    <div v-else-if="errorMessage" class="bg-red-50 text-red-600 p-6 rounded-xl flex items-center border border-red-100">
      <AlertCircle class="w-6 h-6 mr-3" />
      <span class="font-medium">{{ errorMessage }}</span>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Left Panel: Profile Overview (Col span 7) -->
      <div class="lg:col-span-7 space-y-6">
        <!-- Identity Card -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 flex flex-col sm:flex-row items-center sm:items-start relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-emerald-50 rounded-bl-full -z-10 opacity-50"></div>
          
          <div class="w-28 h-28 rounded-2xl overflow-hidden border-4 border-emerald-50 shadow-md flex-shrink-0 mb-4 sm:mb-0 sm:mr-6">
            <img v-if="app.profile_picture_url" :src="app.profile_picture_url" class="w-full h-full object-cover" alt="Avatar">
            <div v-else class="w-full h-full bg-emerald-100 flex items-center justify-center text-4xl font-bold text-emerald-600">
              {{ app.student_name ? app.student_name.charAt(0) : '?' }}
            </div>
          </div>
          
          <div class="text-center sm:text-left flex-1">
            <h3 class="text-2xl font-bold text-gray-900">{{ app.student_name }}</h3>
            <p class="text-emerald-600 font-medium text-sm mt-1">{{ app.education }} in {{ app.branch }}</p>
            
            <div class="flex flex-wrap justify-center sm:justify-start gap-4 mt-4">
              <div class="flex items-center text-gray-600 text-sm bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100">
                <Target class="w-4 h-4 mr-2 text-emerald-500" />
                <span class="font-bold mr-1">{{ app.cgpa }}</span> CGPA
              </div>
              <div class="flex items-center text-gray-600 text-sm bg-gray-50 px-3 py-1.5 rounded-lg border border-gray-100">
                <GraduationCap class="w-4 h-4 mr-2 text-emerald-500" />
                Class of <span class="font-bold ml-1">{{ app.graduation_year }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Skills & Experience -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <h4 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <Code2 class="w-5 h-5 mr-2 text-emerald-500" /> Top Skills
          </h4>
          <div class="flex flex-wrap gap-2 mb-8">
            <span v-for="skill in (app.skills ? app.skills.split(',') : [])" :key="skill" class="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-lg text-sm font-semibold border border-emerald-100">
              {{ skill.trim() }}
            </span>
            <span v-if="!app.skills" class="text-gray-400 text-sm italic">No skills listed</span>
          </div>

          <h4 class="text-lg font-bold text-gray-800 mb-3 flex items-center">
            <Briefcase class="w-5 h-5 mr-2 text-emerald-500" /> Projects & Experience
          </h4>
          <p class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap bg-gray-50 p-4 rounded-xl border border-gray-100">{{ app.experience || 'No experience detailed provided.' }}</p>
        </div>

        <!-- Resume -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
           <div class="flex items-center justify-between mb-4">
             <h4 class="text-lg font-bold text-gray-800 flex items-center">
               <FileText class="w-5 h-5 mr-2 text-emerald-500" /> Resume Document
             </h4>
             <a v-if="app.resume_path" :href="app.resume_path" target="_blank" class="flex items-center text-sm font-bold text-emerald-600 hover:text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg transition">
               <Download class="w-4 h-4 mr-1" /> Download Resume (If viewer fails)
             </a>
           </div>
           
           <div v-if="app.resume_path" class="w-full h-[600px] border border-gray-200 rounded-xl overflow-hidden bg-white shadow-inner">
             <iframe :src="`https://docs.google.com/viewer?url=${encodeURIComponent(app.resume_path)}&embedded=true`" class="w-full h-full" frameborder="0"></iframe>
           </div>
           <div v-else class="p-8 text-center bg-gray-50 border border-dashed border-gray-300 rounded-xl">
             <p class="text-gray-500">No resume uploaded</p>
           </div>
        </div>
      </div>

      <!-- Right Panel: ATS Timeline & Action Center (Col span 5) -->
      <div class="lg:col-span-5 space-y-6">
        
        <!-- Timeline Component -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-32 h-32 bg-indigo-50 rounded-bl-full -z-10 opacity-50"></div>
          
          <h3 class="text-lg font-bold text-gray-800 mb-6 flex items-center">
            <GitCommit class="w-5 h-5 mr-2 text-indigo-500" /> Application Journey
          </h3>

          <div class="relative pl-6 space-y-8 before:absolute before:inset-0 before:ml-8 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-200 before:to-transparent">
            
            <!-- Stage 1: Applied -->
            <div class="relative flex items-center justify-between">
              <div class="flex items-center">
                <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="isStageActive('applied') ? 'border-emerald-500' : 'border-emerald-200 bg-emerald-500'"></div>
                <div>
                  <h4 class="text-sm font-bold" :class="isStageActive('applied') ? 'text-emerald-700' : 'text-gray-800'">Applied</h4>
                  <p class="text-xs text-gray-500 mt-0.5">{{ formatDate(app.applied_at) }}</p>
                </div>
              </div>
            </div>

            <!-- Stage 2: Shortlisted -->
            <div class="relative flex items-center justify-between">
              <div class="flex items-center">
                <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="getStageClass('shortlisted')"></div>
                <div>
                  <h4 class="text-sm font-bold" :class="isStageActive('shortlisted') ? 'text-indigo-700' : 'text-gray-800'">Shortlisted</h4>
                </div>
              </div>
              <button v-if="app.status === 'applied'" @click="updateStatus('shortlisted')" class="px-3 py-1 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 text-xs font-bold rounded-lg transition border border-indigo-100">
                Shortlist Candidate
              </button>
            </div>

            <!-- Stage 3: Interview -->
            <div class="relative flex flex-col justify-center">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="getStageClass('interview')"></div>
                  <div>
                    <h4 class="text-sm font-bold" :class="isStageActive('interview') ? 'text-indigo-700' : 'text-gray-800'">Interview</h4>
                    <p v-if="app.interview_date" class="text-xs text-indigo-600 font-medium mt-0.5">{{ formatDate(app.interview_date) }}</p>
                  </div>
                </div>
                <button v-if="app.status === 'shortlisted'" @click="showActionForm = 'interview'" class="px-3 py-1 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 text-xs font-bold rounded-lg transition border border-indigo-100">
                  Schedule Interview
                </button>
              </div>

              <!-- Interview Action Form -->
              <div v-if="showActionForm === 'interview'" class="mt-4 p-4 bg-gray-50 border border-gray-200 rounded-xl animate-in slide-in-from-top-2">
                <div class="mb-3">
                  <label class="block text-xs font-bold text-gray-700 mb-1">Date & Time</label>
                  <div class="flex gap-2">
                    <input type="date" v-model="actionData.interview_date" class="w-full text-sm px-2 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500">
                    <select v-model="actionData.interview_hour" class="w-16 text-sm px-1 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 text-center">
                      <option v-for="h in 12" :key="h" :value="h.toString().padStart(2, '0')">{{ h }}</option>
                    </select>
                    <span class="py-2 font-bold text-gray-500">:</span>
                    <select v-model="actionData.interview_minute" class="w-16 text-sm px-1 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 text-center">
                      <option value="00">00</option>
                      <option value="15">15</option>
                      <option value="30">30</option>
                      <option value="45">45</option>
                    </select>
                    <select v-model="actionData.interview_ampm" class="w-16 text-sm px-1 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 text-center">
                      <option value="AM">AM</option>
                      <option value="PM">PM</option>
                    </select>
                  </div>
                </div>
                <div class="mb-4">
                  <label class="block text-xs font-bold text-gray-700 mb-1">Meeting Link (optional)</label>
                  <input type="url" v-model="actionData.interview_link" placeholder="https://meet.google.com/..." class="w-full text-sm px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500">
                </div>
                <div class="flex gap-2">
                  <button @click="submitAction('interview')" class="flex-1 bg-indigo-600 text-white text-xs font-bold py-2 rounded-lg hover:bg-indigo-700 transition" :disabled="actionLoading">
                    <Loader2 v-if="actionLoading" class="w-3 h-3 animate-spin mx-auto" />
                    <span v-else>Confirm Schedule</span>
                  </button>
                  <button @click="showActionForm = null" class="px-3 bg-gray-200 text-gray-600 text-xs font-bold rounded-lg hover:bg-gray-300 transition">Cancel</button>
                </div>
              </div>
            </div>

            <!-- Stage 4: Selected -->
            <div class="relative flex items-center justify-between">
              <div class="flex items-center">
                <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="getStageClass('selected')"></div>
                <div>
                  <h4 class="text-sm font-bold" :class="isStageActive('selected') ? 'text-teal-700' : 'text-gray-800'">Selected</h4>
                </div>
              </div>
              <button v-if="app.status === 'interview'" @click="updateStatus('selected')" class="px-3 py-1 bg-teal-50 text-teal-700 hover:bg-teal-100 text-xs font-bold rounded-lg transition border border-teal-100">
                Mark Selected
              </button>
            </div>

            <!-- Stage 5: Placed -->
            <div class="relative flex flex-col justify-center">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="getStageClass('placed')"></div>
                  <div>
                    <h4 class="text-sm font-bold" :class="isStageActive('placed') ? 'text-green-700' : 'text-gray-800'">Placed</h4>
                  </div>
                </div>
                <button v-if="app.status === 'selected'" @click="showActionForm = 'placed'" class="px-3 py-1 bg-green-500 text-white hover:bg-green-600 shadow-sm text-xs font-bold rounded-lg transition border border-green-600">
                  Generate Offer
                </button>
              </div>

              <!-- Placement Action Form -->
              <div v-if="showActionForm === 'placed'" class="mt-4 p-4 bg-green-50 border border-green-200 rounded-xl animate-in slide-in-from-top-2">
                <div class="mb-4">
                  <label class="block text-xs font-bold text-green-800 mb-1">Joining Date</label>
                  <input type="date" v-model="actionData.joining_date" :min="minDate" required class="w-full text-sm px-3 py-2 border border-green-300 rounded-lg focus:ring-green-500 focus:border-green-500">
                </div>
                <div class="flex gap-2">
                  <button @click="submitAction('placed')" class="flex-1 bg-green-600 text-white text-xs font-bold py-2 rounded-lg hover:bg-green-700 shadow-sm transition" :disabled="actionLoading">
                    <Loader2 v-if="actionLoading" class="w-3 h-3 animate-spin mx-auto" />
                    <span v-else>Confirm Placement</span>
                  </button>
                  <button @click="showActionForm = null" class="px-3 bg-green-200 text-green-800 text-xs font-bold rounded-lg hover:bg-green-300 transition">Cancel</button>
                </div>
              </div>
            </div>

            <!-- Rejection (Only visible if rejected or can be rejected) -->
            <div class="relative flex items-center justify-between pt-4 mt-4 border-t border-gray-100">
              <div class="flex items-center">
                <div class="absolute -left-6 w-4 h-4 rounded-full border-4 bg-white" :class="app.status === 'rejected' ? 'border-red-500' : 'border-gray-200'"></div>
                <div>
                  <h4 class="text-sm font-bold" :class="app.status === 'rejected' ? 'text-red-600' : 'text-gray-500'">Rejected</h4>
                </div>
              </div>
              <button v-if="app.status !== 'rejected' && app.status !== 'placed'" @click="updateStatus('rejected')" class="text-xs font-bold text-red-500 hover:text-red-700 hover:underline transition">
                Reject Candidate
              </button>
            </div>
            
          </div>
        </div>

        <!-- Notes / Feedback Center -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <MessageSquare class="w-5 h-5 mr-2 text-amber-500" /> Private Notes
          </h3>
          <p class="text-xs text-gray-500 mb-3">These notes are visible only to your company team.</p>
          <textarea v-model="app.feedback" rows="4" class="w-full text-sm p-4 bg-amber-50 border border-amber-100 rounded-xl focus:bg-white focus:ring-2 focus:ring-amber-200 focus:border-amber-200 resize-none transition shadow-inner placeholder-amber-200" placeholder="Jot down interview impressions, strengths, weaknesses..."></textarea>
          <div class="flex justify-end mt-3">
            <button @click="saveNotes" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-bold rounded-lg transition flex items-center" :disabled="actionLoading">
              <Save class="w-4 h-4 mr-2" /> Save Notes
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import api from "../../api/axios"
import { toast } from "../../components/Toast.vue"
import { ArrowLeft, Loader2, AlertCircle, Target, GraduationCap, Code2, Briefcase, FileText, Download, GitCommit, MessageSquare, Save } from "lucide-vue-next"

export default {
  name: "CompanyApplicantDetails",
  components: { ArrowLeft, Loader2, AlertCircle, Target, GraduationCap, Code2, Briefcase, FileText, Download, GitCommit, MessageSquare, Save },
  data() {
    return {
      app: {},
      loading: true,
      errorMessage: "",
      showActionForm: null,
      actionLoading: false,
      actionData: {
        interview_date: "",
        interview_hour: "10",
        interview_minute: "00",
        interview_ampm: "AM",
        interview_link: "",
        joining_date: ""
      },
      stages: ["applied", "shortlisted", "interview", "selected", "placed"]
    }
  },
  async mounted() {
    await this.fetchApplicationDetails();
  },
  computed: {
    minDate() {
      return new Date().toLocaleDateString('en-CA', { timeZone: 'Asia/Kolkata' });
    }
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` };
    },
    async fetchApplicationDetails() {
      const id = this.$route.params.id;
      try {
        const response = await api.get(`/company/application/${id}`, { headers: this.getHeaders() });
        this.app = response.data;
        this.loading = false;
      } catch (error) {
        this.errorMessage = error.response?.data?.message || "Failed to load application details.";
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    },
    getStatusBadgeClass(status) {
      switch (status) {
        case 'applied': return 'bg-gray-100 text-gray-600 border border-gray-200';
        case 'shortlisted': return 'bg-indigo-50 text-indigo-700 border border-indigo-200';
        case 'interview': return 'bg-blue-50 text-blue-700 border border-blue-200';
        case 'selected': return 'bg-teal-50 text-teal-700 border border-teal-200';
        case 'placed': return 'bg-green-100 text-green-800 border border-green-300';
        case 'rejected': return 'bg-red-50 text-red-700 border border-red-200';
        default: return 'bg-gray-100 text-gray-800';
      }
    },
    // Timeline logic
    isStageActive(stage) {
      return this.app.status === stage;
    },
    isStagePassed(stage) {
      if (this.app.status === 'rejected') return false; // Rejected breaks the chain
      const currentIndex = this.stages.indexOf(this.app.status);
      const stageIndex = this.stages.indexOf(stage);
      return stageIndex < currentIndex;
    },
    getStageClass(stage) {
      if (this.isStageActive(stage)) return 'border-indigo-500 shadow-md';
      if (this.isStagePassed(stage)) return 'border-indigo-200 bg-indigo-500';
      return 'border-gray-200';
    },
    // Actions
    async updateStatus(newStatus) {
      try {
        this.actionLoading = true;
        await api.patch(`/company/application/${this.app.application_id}`, {
          status: newStatus
        }, { headers: this.getHeaders() });
        
        this.app.status = newStatus;
        toast(`Candidate marked as ${newStatus}`, "success");
      } catch (error) {
        toast(error.response?.data?.message || "Failed to update status", "error");
      } finally {
        this.actionLoading = false;
      }
    },
    async submitAction(actionType) {
      try {
        this.actionLoading = true;
        const payload = { status: actionType };
        
        if (actionType === 'interview') {
          if (!this.actionData.interview_date) {
            toast("Please select an interview date", "error");
            this.actionLoading = false;
            return;
          }
          let h = parseInt(this.actionData.interview_hour);
          if (this.actionData.interview_ampm === 'PM' && h !== 12) h += 12;
          if (this.actionData.interview_ampm === 'AM' && h === 12) h = 0;
          
          const combinedDate = `${this.actionData.interview_date}T${h.toString().padStart(2, '0')}:${this.actionData.interview_minute}:00`;
          
          payload.interview_date = combinedDate;
          payload.interview_link = this.actionData.interview_link;
        } else if (actionType === 'placed') {
          if (!this.actionData.joining_date) {
            toast("Please select a joining date", "error");
            this.actionLoading = false;
            return;
          }
          payload.joining_date = `${this.actionData.joining_date}T00:00:00`;
        }

        await api.patch(`/company/application/${this.app.application_id}`, payload, { headers: this.getHeaders() });
        
        this.app.status = actionType;
        if (actionType === 'interview') this.app.interview_date = this.actionData.interview_date;
        
        this.showActionForm = null;
        toast(`Candidate moved to ${actionType} successfully`, "success");
      } catch (error) {
        toast(error.response?.data?.message || `Failed to process ${actionType}`, "error");
      } finally {
        this.actionLoading = false;
      }
    },
    async saveNotes() {
      try {
        this.actionLoading = true;
        await api.patch(`/company/application/${this.app.application_id}`, {
          feedback: this.app.feedback
        }, { headers: this.getHeaders() });
        toast("Notes saved securely.", "success");
      } catch (error) {
        toast("Failed to save notes.", "error");
      } finally {
        this.actionLoading = false;
      }
    }
  }
}
</script>
