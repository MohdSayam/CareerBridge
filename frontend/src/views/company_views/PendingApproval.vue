<template>
  <div class="min-h-[80vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden text-center">
      <div class="bg-amber-100 py-8 px-6 flex justify-center border-b border-amber-200">
        <div class="bg-amber-200 p-4 rounded-full">
          <Clock class="w-12 h-12 text-amber-700" />
        </div>
      </div>
      <div class="px-8 py-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Pending Approval</h2>
        <p class="text-gray-600 mb-8">
          {{ message }}
        </p>
        <button @click="logout" class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition">
          <LogOut class="w-5 h-5 mr-2" />
          Logout Safely
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Clock, LogOut } from "lucide-vue-next"

export default {
  name: "PendingApproval",
  components: { Clock, LogOut },
  data() {
    return {
      message: this.$route.query.message || "Your company account is currently pending administrative approval. You will receive an email once your portal access is granted."
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("access_token")
      localStorage.removeItem("role")
      this.$router.push("/login")
    }
  }
}
</script>