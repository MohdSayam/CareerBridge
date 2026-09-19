<template>
  <div class="flex flex-col bg-gray-950 rounded-2xl overflow-hidden shadow-2xl" style="height: 90vh;">
    
    <!-- Header Bar -->
    <div class="bg-gray-900 border-b border-gray-800 px-6 py-3 flex items-center justify-between flex-shrink-0">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center shadow-md">
          <Video class="w-5 h-5 text-white" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h2 class="text-white font-bold text-base">Virtual Interview Room</h2>
            <span v-if="callActive" class="flex items-center space-x-1 px-2 py-0.5 bg-green-600/20 border border-green-500/30 rounded-full">
              <span class="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
              <span class="text-green-400 text-[10px] font-bold uppercase tracking-wider">Live</span>
            </span>
            <span v-else-if="connectionState === 'connecting'" class="px-2 py-0.5 bg-yellow-500/20 border border-yellow-500/30 rounded-full text-yellow-400 text-[10px] font-bold uppercase tracking-wider">
              Connecting...
            </span>
            <span v-else class="px-2 py-0.5 bg-gray-700 rounded-full text-gray-400 text-[10px] font-bold uppercase tracking-wider">
              Waiting for peer...
            </span>
          </div>
          <p class="text-gray-400 text-xs mt-0.5">
            {{ role === 'company' 
              ? 'Candidate: ' + (applicationDetails?.student_name || 'Loading...') 
              : 'Company: ' + (applicationDetails?.job?.company_name || applicationDetails?.company_name || 'Loading...') }}
          </p>
        </div>
      </div>

      <!-- Call Timer & End -->
      <div class="flex items-center space-x-3">
        <div v-if="callActive" class="text-gray-300 text-sm font-mono bg-gray-800 px-3 py-1.5 rounded-lg border border-gray-700">
          {{ callDuration }}
        </div>
        <button @click="endCall" class="flex items-center px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg transition shadow-md">
          <PhoneOff class="w-4 h-4 mr-2" /> End Call
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex overflow-hidden">
      
      <!-- Video Area -->
      <div class="flex-1 relative bg-gray-950 flex flex-col">
        
        <!-- Waiting / Error State -->
        <div v-if="!callActive" class="absolute inset-0 flex flex-col items-center justify-center text-center px-8 z-10">
          <div v-if="statusMessage" class="flex flex-col items-center">
            <div class="w-20 h-20 bg-indigo-600/10 border-2 border-indigo-500/30 rounded-full flex items-center justify-center mb-6">
              <Loader2 v-if="connectionState === 'connecting'" class="w-10 h-10 text-indigo-400 animate-spin" />
              <Users v-else class="w-10 h-10 text-indigo-400" />
            </div>
            <h3 class="text-white text-xl font-bold mb-2">{{ statusMessage }}</h3>
            <p class="text-gray-400 text-sm max-w-sm">{{ statusSubtext }}</p>
          </div>
        </div>

        <!-- Remote Video (full screen) -->
        <video 
          ref="remoteVideo"
          autoplay 
          playsinline
          class="w-full h-full object-cover transition-opacity duration-500"
          :class="callActive ? 'opacity-100' : 'opacity-0'"
        ></video>

        <!-- Remote video placeholder when active but no stream -->
        <div v-if="callActive && !remoteStreamActive" class="absolute inset-0 flex items-center justify-center bg-gray-900">
          <div class="text-center">
            <div class="w-24 h-24 bg-gray-700 rounded-full flex items-center justify-center mx-auto mb-3">
              <User class="w-12 h-12 text-gray-400" />
            </div>
            <p class="text-gray-400 text-sm">Camera is off</p>
          </div>
        </div>

        <!-- Local Video (Picture-in-Picture) -->
        <div class="absolute bottom-4 right-4 w-44 h-32 bg-gray-800 rounded-xl overflow-hidden shadow-2xl border-2 border-gray-700 cursor-move z-20">
          <video 
            ref="localVideo" 
            autoplay 
            muted 
            playsinline
            class="w-full h-full object-cover"
            :class="videoEnabled ? 'opacity-100' : 'opacity-0'"
          ></video>
          <div v-if="!videoEnabled" class="absolute inset-0 flex items-center justify-center bg-gray-800">
            <VideoOff class="w-8 h-8 text-gray-500" />
          </div>
          <span class="absolute bottom-1.5 left-2 text-white text-[9px] font-bold bg-black/60 px-1.5 py-0.5 rounded">
            You ({{ role }})
          </span>
        </div>

        <!-- Controls Bar -->
        <div class="absolute bottom-0 left-0 right-0 pb-4 flex justify-center z-20">
          <div class="flex items-center space-x-3 bg-gray-900/90 backdrop-blur-sm border border-gray-800 rounded-2xl px-6 py-3 shadow-2xl">
            
            <!-- Mic -->
            <button 
              @click="toggleMic"
              class="w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-lg"
              :class="micEnabled ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-red-600 hover:bg-red-700 text-white'"
              :title="micEnabled ? 'Mute' : 'Unmute'"
            >
              <Mic v-if="micEnabled" class="w-5 h-5" />
              <MicOff v-else class="w-5 h-5" />
            </button>

            <!-- Camera -->
            <button 
              @click="toggleVideo"
              class="w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-lg"
              :class="videoEnabled ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-red-600 hover:bg-red-700 text-white'"
              :title="videoEnabled ? 'Turn off camera' : 'Turn on camera'"
            >
              <Video v-if="videoEnabled" class="w-5 h-5" />
              <VideoOff v-else class="w-5 h-5" />
            </button>

            <!-- Screen Share -->
            <button 
              @click="toggleScreenShare"
              class="w-12 h-12 rounded-full flex items-center justify-center transition-all shadow-lg"
              :class="screenSharing ? 'bg-indigo-600 hover:bg-indigo-700 text-white' : 'bg-gray-700 hover:bg-gray-600 text-white'"
              :title="screenSharing ? 'Stop sharing' : 'Share screen'"
            >
              <MonitorUp class="w-5 h-5" />
            </button>

            <!-- End Call (center, prominent) -->
            <button 
              @click="endCall"
              class="w-14 h-14 bg-red-600 hover:bg-red-700 text-white rounded-full flex items-center justify-center transition shadow-xl scale-110"
            >
              <PhoneOff class="w-6 h-6" />
            </button>

          </div>
        </div>
      </div>

      <!-- Right Panel: Notes / Candidate Info -->
      <div class="w-80 bg-gray-900 border-l border-gray-800 flex flex-col overflow-hidden flex-shrink-0">
        
        <!-- Candidate Info (Company View) -->
        <div v-if="role === 'company' && applicationDetails" class="p-4 border-b border-gray-800">
          <h3 class="text-gray-300 text-xs font-bold uppercase tracking-wider mb-3 flex items-center">
            <User class="w-3.5 h-3.5 mr-1.5 text-indigo-400" /> Candidate Overview
          </h3>
          <div class="bg-gray-800 rounded-xl p-3 space-y-2">
            <div class="flex items-center space-x-2">
              <img v-if="applicationDetails.profile_picture_url" :src="applicationDetails.profile_picture_url" class="w-10 h-10 rounded-full object-cover border border-gray-700" />
              <div v-else class="w-10 h-10 rounded-full bg-indigo-600/30 flex items-center justify-center text-indigo-300 font-bold">
                {{ applicationDetails.student_name?.charAt(0) }}
              </div>
              <div>
                <p class="text-white text-sm font-bold">{{ applicationDetails.student_name }}</p>
                <p class="text-gray-400 text-xs">{{ applicationDetails.branch }} • {{ applicationDetails.cgpa }} CGPA</p>
              </div>
            </div>
            <a v-if="applicationDetails.resume_path" :href="applicationDetails.resume_path" target="_blank" class="flex items-center justify-center w-full py-1.5 bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 text-xs font-bold rounded-lg border border-indigo-500/20 transition">
              <FileText class="w-3.5 h-3.5 mr-1.5" /> View Resume
            </a>
          </div>
        </div>

        <!-- Notes / Tips -->
        <div class="flex-1 p-4 flex flex-col overflow-hidden">
          <h3 class="text-gray-300 text-xs font-bold uppercase tracking-wider mb-3 flex items-center">
            <ClipboardList class="w-3.5 h-3.5 mr-1.5 text-amber-400" />
            {{ role === 'company' ? 'Private Notes' : 'Interview Tips' }}
          </h3>

          <!-- Company: Note taking -->
          <div v-if="role === 'company'" class="flex-1 flex flex-col">
            <textarea 
              v-model="notes" 
              class="flex-1 w-full bg-gray-800 border border-gray-700 text-gray-200 rounded-xl p-3 text-sm resize-none focus:outline-none focus:border-indigo-500 placeholder-gray-600"
              placeholder="Technical skills, communication, red flags..."
            ></textarea>
            <button 
              @click="saveNotes" 
              :disabled="savingNotes"
              class="mt-3 w-full py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold text-sm rounded-xl transition flex items-center justify-center"
            >
              <Check v-if="notesSaved" class="w-4 h-4 mr-2 text-green-300" />
              <Loader2 v-else-if="savingNotes" class="w-4 h-4 mr-2 animate-spin" />
              {{ notesSaved ? 'Saved!' : savingNotes ? 'Saving...' : 'Save Notes' }}
            </button>
          </div>

          <!-- Student: Tips -->
          <div v-else class="space-y-3">
            <div v-for="tip in interviewTips" :key="tip.title" class="flex items-start space-x-3 bg-gray-800 rounded-xl p-3 border border-gray-700">
              <div class="w-8 h-8 bg-green-600/20 rounded-lg flex items-center justify-center flex-shrink-0">
                <Check class="w-4 h-4 text-green-400" />
              </div>
              <div>
                <p class="text-white text-sm font-bold">{{ tip.title }}</p>
                <p class="text-gray-400 text-xs mt-0.5 leading-relaxed">{{ tip.desc }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- Company: Actions -->
        <div v-if="role === 'company' && applicationDetails" class="border-t border-gray-800 p-4">
          <h3 class="text-gray-300 text-xs font-bold uppercase tracking-wider mb-3 flex items-center">
            <Check class="w-3.5 h-3.5 mr-1.5 text-green-400" /> Quick Actions
          </h3>
          <div class="grid grid-cols-2 gap-2 mb-3">
            <button @click="updateStatus('shortlisted')"
              :disabled="updatingStatus"
              class="py-2 rounded-lg text-xs font-bold transition border" 
              :class="currentStatus === 'shortlisted' ? 'bg-blue-600 text-white border-blue-500' : 'bg-gray-800 text-gray-300 border-gray-700 hover:border-blue-500 hover:text-blue-300'"
            >Shortlist</button>
            <button @click="updateStatus('interview')"
              :disabled="updatingStatus"
              class="py-2 rounded-lg text-xs font-bold transition border"
              :class="currentStatus === 'interview' ? 'bg-indigo-600 text-white border-indigo-500' : 'bg-gray-800 text-gray-300 border-gray-700 hover:border-indigo-500 hover:text-indigo-300'"
            >In Progress</button>
            <button @click="updateStatus('selected')"
              :disabled="updatingStatus"
              class="py-2 rounded-lg text-xs font-bold transition border"
              :class="currentStatus === 'selected' ? 'bg-amber-600 text-white border-amber-500' : 'bg-gray-800 text-gray-300 border-gray-700 hover:border-amber-500 hover:text-amber-300'"
            >Select ✓</button>
            <button @click="updateStatus('rejected')"
              :disabled="updatingStatus"
              class="py-2 rounded-lg text-xs font-bold transition border"
              :class="currentStatus === 'rejected' ? 'bg-red-700 text-white border-red-600' : 'bg-gray-800 text-gray-300 border-gray-700 hover:border-red-500 hover:text-red-300'"
            >Reject ✗</button>
          </div>
          <p v-if="statusUpdated" class="text-green-400 text-xs font-semibold text-center mt-1">✓ Status updated</p>
          <p v-if="updatingStatus" class="text-gray-400 text-xs text-center mt-1">Updating...</p>
        </div>

      </div>
    </div>

    <!-- Post-Interview Outcome Banner -->
    <div v-if="showOutcomeBanner" class="absolute inset-0 bg-gray-950/90 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-gray-900 border border-gray-700 rounded-3xl p-8 max-w-md w-full mx-4 text-center shadow-2xl">
        <div class="w-16 h-16 bg-indigo-600/20 rounded-full flex items-center justify-center mx-auto mb-4">
          <PhoneOff class="w-8 h-8 text-indigo-400" />
        </div>
        <h3 class="text-white text-xl font-bold mb-2">Interview Ended</h3>
        <p class="text-gray-400 text-sm mb-6">The call has ended. {{ role === 'company' ? 'Please update the candidate status before leaving.' : 'Thank you for attending! You will hear back from the company soon.' }}</p>
        <div v-if="role === 'company'" class="grid grid-cols-2 gap-3 mb-4">
          <button @click="quickUpdateAndLeave('selected')" class="py-3 px-4 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-bold text-sm transition">Mark Selected</button>
          <button @click="quickUpdateAndLeave('rejected')" class="py-3 px-4 bg-red-700 hover:bg-red-800 text-white rounded-xl font-bold text-sm transition">Mark Rejected</button>
        </div>
        <button @click="leaveRoom" class="w-full py-3 px-6 bg-gray-700 hover:bg-gray-600 text-white rounded-xl font-semibold text-sm transition">Leave Room</button>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from "socket.io-client"
import api from '../api/axios.js'
import { Video, VideoOff, PhoneOff, Mic, MicOff, MonitorUp, ClipboardList, User, FileText, Check, Loader2, Users } from "lucide-vue-next"

const ICE_SERVERS = {
  iceServers: [
    // Free Google STUN servers (works for same-network calls)
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun1.l.google.com:19302" },
    // Local TURN server — configure IP in frontend/.env (run fix_turn_config.sh)
    ...(import.meta.env.VITE_TURN_SERVER ? [{
      urls: import.meta.env.VITE_TURN_SERVER,
      username: import.meta.env.VITE_TURN_USERNAME,
      credential: import.meta.env.VITE_TURN_CREDENTIAL
    }] : [])
  ]
}

export default {
  name: "InterviewRoom",
  components: { Video, VideoOff, PhoneOff, Mic, MicOff, MonitorUp, ClipboardList, User, FileText, Check, Loader2, Users },
  data() {
    return {
      applicationId: this.$route.params.id,
      role: localStorage.getItem("role"),
      applicationDetails: null,
      
      // WebRTC
      peerConnection: null,
      localStream: null,
      socket: null,
      
      // UI States
      callActive: false,
      remoteStreamActive: false,
      connectionState: "waiting",
      micEnabled: true,
      videoEnabled: true,
      screenSharing: false,
      
      // Notes
      notes: "",
      savingNotes: false,
      notesSaved: false,
      
      // Company Actions
      currentStatus: "",
      updatingStatus: false,
      statusUpdated: false,
      showOutcomeBanner: false,
      
      // Timer
      callStartTime: null,
      callDuration: "00:00",
      timerInterval: null,

      interviewTips: [
        { title: "Be Confident", desc: "Speak clearly and maintain eye contact with the camera." },
        { title: "Have Resume Ready", desc: "Be prepared to walk through any project in detail." },
        { title: "Ask Questions", desc: "Interviewing is a two-way street — your questions matter." },
        { title: "Good Lighting", desc: "Make sure your face is well lit. Sit facing a window." }
      ]
    }
  },
  computed: {
    statusMessage() {
      if (this.connectionState === "connecting") return "Setting up your camera..."
      if (this.connectionState === "waiting") return "Waiting for the other participant..."
      if (this.connectionState === "error") return "Connection Error"
      return ""
    },
    statusSubtext() {
      if (this.connectionState === "connecting") return "Please allow camera and microphone access when prompted."
      if (this.connectionState === "waiting") return "Share this link with the other participant. The call will start automatically when they join."
      return ""
    }
  },
  async mounted() {
    await this.fetchDetails()
    await this.startLocalMedia()
    this.connectSignaling()
  },
  beforeUnmount() {
    this.cleanupAll()
  },
  methods: {
    getHeaders() {
      return { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    },

    async fetchDetails() {
      try {
        if (this.role === 'student') {
          const res = await api.get('/student/applications', { headers: this.getHeaders() })
          this.applicationDetails = res.data.find(a => a.application_id == this.applicationId)
        } else {
          const res = await api.get(`/company/application/${this.applicationId}`, { headers: this.getHeaders() })
          this.applicationDetails = res.data
        }
        if (this.applicationDetails?.feedback) {
          this.notes = this.applicationDetails.feedback
        }
        if (this.applicationDetails?.status) {
          this.currentStatus = this.applicationDetails.status
        }
      } catch (e) {
        console.error("Failed to fetch details:", e)
      }
    },

    async startLocalMedia() {
      this.connectionState = "connecting"
      try {
        this.localStream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 1280 }, height: { ideal: 720 } },
          audio: { echoCancellation: true, noiseSuppression: true }
        })
        this.$refs.localVideo.srcObject = this.localStream
        this.connectionState = "waiting"
      } catch (err) {
        console.error("Camera/mic access denied:", err)
        this.connectionState = "error"
      }
    },

    connectSignaling() {
      const baseUrl = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api").replace(/\/api\/?$/, "")
      this.socket = io(baseUrl, {
        transports: ["websocket", "polling"]
      })

      this.socket.on("connect", () => {
        console.log("Connected to signaling server")
        this.socket.emit("join_interview", {
          room_id: this.applicationId,
          role: this.role
        })
      })

      this.socket.on("room_joined", (data) => {
        console.log("Room joined:", data)
        if (data.should_initiate) {
          // We are the second to join — create offer
          this.createPeerConnection()
          this.createOffer()
        }
      })

      this.socket.on("peer_joined", async (data) => {
        console.log("Peer joined, setting up peer connection")
        if (!this.peerConnection) {
          this.createPeerConnection()
        }
      })

      this.socket.on("webrtc_offer", async (data) => {
        console.log("Received offer")
        if (!this.peerConnection) this.createPeerConnection()
        await this.peerConnection.setRemoteDescription(new RTCSessionDescription(data.sdp))
        const answer = await this.peerConnection.createAnswer()
        await this.peerConnection.setLocalDescription(answer)
        this.socket.emit("webrtc_answer", {
          room_id: this.applicationId,
          sdp: answer
        })
      })

      this.socket.on("webrtc_answer", async (data) => {
        console.log("Received answer")
        await this.peerConnection.setRemoteDescription(new RTCSessionDescription(data.sdp))
      })

      this.socket.on("ice_candidate", async (data) => {
        if (data.candidate && this.peerConnection) {
          try {
            await this.peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
          } catch (e) {
            console.warn("ICE candidate error:", e)
          }
        }
      })

      this.socket.on("peer_disconnected", () => {
        console.log("Peer disconnected")
        this.callActive = false
        this.remoteStreamActive = false
        this.connectionState = "waiting"
        if (this.$refs.remoteVideo) this.$refs.remoteVideo.srcObject = null
        if (this.peerConnection) {
          this.peerConnection.close()
          this.peerConnection = null
        }
        this.stopTimer()
      })
    },

    createPeerConnection() {
      this.peerConnection = new RTCPeerConnection(ICE_SERVERS)

      // Add local tracks
      if (this.localStream) {
        this.localStream.getTracks().forEach(track => {
          this.peerConnection.addTrack(track, this.localStream)
        })
      }

      // Handle ICE candidates
      this.peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
          this.socket.emit("ice_candidate", {
            room_id: this.applicationId,
            candidate: event.candidate
          })
        }
      }

      // Handle remote stream
      this.peerConnection.ontrack = (event) => {
        console.log("Remote track received")
        const [remoteStream] = event.streams
        if (this.$refs.remoteVideo) {
          this.$refs.remoteVideo.srcObject = remoteStream
        }
        this.callActive = true
        this.remoteStreamActive = true
        this.startTimer()
      }

      this.peerConnection.onconnectionstatechange = () => {
        const state = this.peerConnection.connectionState
        console.log("Connection state:", state)
        if (state === "disconnected" || state === "failed" || state === "closed") {
          this.callActive = false
          this.stopTimer()
        }
      }
    },

    async createOffer() {
      const offer = await this.peerConnection.createOffer({
        offerToReceiveAudio: true,
        offerToReceiveVideo: true
      })
      await this.peerConnection.setLocalDescription(offer)
      this.socket.emit("webrtc_offer", {
        room_id: this.applicationId,
        sdp: offer
      })
    },

    toggleMic() {
      if (this.localStream) {
        const track = this.localStream.getAudioTracks()[0]
        if (track) {
          track.enabled = !track.enabled
          this.micEnabled = track.enabled
        }
      }
    },

    toggleVideo() {
      if (this.localStream) {
        const track = this.localStream.getVideoTracks()[0]
        if (track) {
          track.enabled = !track.enabled
          this.videoEnabled = track.enabled
        }
      }
    },

    async toggleScreenShare() {
      if (!this.screenSharing) {
        try {
          const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true })
          const screenTrack = screenStream.getVideoTracks()[0]
          
          if (this.peerConnection) {
            const sender = this.peerConnection.getSenders().find(s => s.track?.kind === "video")
            if (sender) sender.replaceTrack(screenTrack)
          }
          
          this.$refs.localVideo.srcObject = screenStream
          this.screenSharing = true

          screenTrack.onended = () => {
            this.stopScreenShare()
          }
        } catch (e) {
          console.error("Screen share failed:", e)
        }
      } else {
        this.stopScreenShare()
      }
    },

    async stopScreenShare() {
      this.screenSharing = false
      if (this.localStream && this.peerConnection) {
        const videoTrack = this.localStream.getVideoTracks()[0]
        const sender = this.peerConnection.getSenders().find(s => s.track?.kind === "video")
        if (sender && videoTrack) sender.replaceTrack(videoTrack)
        this.$refs.localVideo.srcObject = this.localStream
      }
    },

    endCall() {
      if (this.socket) {
        this.socket.emit("leave_interview", { room_id: this.applicationId })
      }
      this.cleanupAll()
      // Show outcome banner instead of immediately going back
      this.showOutcomeBanner = true
    },

    leaveRoom() {
      this.$router.go(-1)
    },

    async updateStatus(newStatus) {
      if (this.updatingStatus) return
      this.updatingStatus = true
      this.statusUpdated = false
      try {
        await api.patch(`/company/application/${this.applicationId}`, {
          status: newStatus
        }, { headers: this.getHeaders() })
        this.currentStatus = newStatus
        this.statusUpdated = true
        setTimeout(() => { this.statusUpdated = false }, 3000)
      } catch (e) {
        console.error("Failed to update status:", e)
      } finally {
        this.updatingStatus = false
      }
    },

    async quickUpdateAndLeave(newStatus) {
      await this.updateStatus(newStatus)
      this.$router.go(-1)
    },

    cleanupAll() {
      this.stopTimer()
      if (this.localStream) {
        this.localStream.getTracks().forEach(t => t.stop())
      }
      if (this.peerConnection) {
        this.peerConnection.close()
      }
      if (this.socket) {
        this.socket.disconnect()
      }
    },

    startTimer() {
      this.callStartTime = Date.now()
      this.timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - this.callStartTime) / 1000)
        const m = String(Math.floor(elapsed / 60)).padStart(2, "0")
        const s = String(elapsed % 60).padStart(2, "0")
        this.callDuration = `${m}:${s}`
      }, 1000)
    },

    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval)
        this.timerInterval = null
      }
    },

    async saveNotes() {
      if (!this.notes.trim()) return
      this.savingNotes = true
      this.notesSaved = false
      try {
        await api.patch(`/company/application/${this.applicationId}`, {
          feedback: this.notes
        }, { headers: this.getHeaders() })
        this.notesSaved = true
        setTimeout(() => { this.notesSaved = false }, 3000)
      } catch (e) {
        console.error("Failed to save notes:", e)
      } finally {
        this.savingNotes = false
      }
    }
  }
}
</script>
