<template>
  <div class="bg-white text-slate-900 overflow-x-hidden">

    <!-- NAV -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-slate-100">
      <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-trust-blue rounded-lg flex items-center justify-center">
            <span class="text-white font-black text-sm">CB</span>
          </div>
          <span class="font-heading font-bold text-xl tracking-tight">CareerBridge</span>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/login" class="text-slate-600 hover:text-slate-900 font-medium transition px-4 py-2 rounded-lg hover:bg-slate-50">Sign In</router-link>
          <router-link to="/register" class="bg-slate-900 hover:bg-slate-700 text-white font-semibold px-5 py-2.5 rounded-xl transition text-sm">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="pt-32 pb-20 px-6">
      <div class="max-w-4xl mx-auto text-center">
        <div class="inline-flex items-center gap-2 bg-trust-blue/8 border border-trust-blue/15 text-trust-blue px-4 py-2 rounded-full text-sm font-semibold mb-8">
          <div class="w-2 h-2 bg-trust-blue rounded-full animate-pulse"></div>
          Campus Placement Platform
        </div>
        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-heading font-black tracking-tight text-slate-900 leading-[1.05] mb-6">
          Where talent meets <br class="hidden sm:block"/>
          <span class="text-trust-blue">opportunity</span>
        </h1>
        <p class="text-xl text-slate-500 max-w-2xl mx-auto leading-relaxed mb-10">
          A modern placement portal built for colleges, students, and companies. Streamlined applications, live interviews, and real-time tracking — all in one place.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <router-link to="/register" class="inline-flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-700 text-white font-bold px-8 py-4 rounded-2xl transition text-lg">
            Start for free <ArrowRight class="w-5 h-5" />
          </router-link>
          <router-link to="/login" class="inline-flex items-center justify-center gap-2 bg-white border-2 border-slate-200 hover:border-slate-900 text-slate-700 font-bold px-8 py-4 rounded-2xl transition text-lg">
            Sign in
          </router-link>
        </div>
        <p class="text-slate-400 text-sm mt-6">No credit card required · Free for students</p>
      </div>
    </section>

    <!-- HERO VISUAL: Dashboard Preview -->
    <section class="pb-24 px-6">
      <div class="max-w-5xl mx-auto">
        <div class="bg-slate-900 rounded-3xl p-1 shadow-2xl ring-1 ring-slate-900/10">
          <div class="bg-slate-800 rounded-[22px] overflow-hidden">
            <!-- Fake browser bar -->
            <div class="bg-slate-700/50 px-4 py-3 flex items-center gap-2 border-b border-slate-700">
              <div class="flex gap-1.5">
                <div class="w-3 h-3 rounded-full bg-red-400 opacity-70"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-400 opacity-70"></div>
                <div class="w-3 h-3 rounded-full bg-green-400 opacity-70"></div>
              </div>
              <div class="flex-1 bg-slate-700 rounded-lg mx-3 px-3 py-1 text-slate-400 text-xs">app.careerbridge.in/company</div>
            </div>
            <!-- Fake App UI -->
            <div class="flex min-h-[380px]">
              <!-- Sidebar -->
              <div class="hidden sm:flex w-48 bg-slate-900 flex-col p-4 gap-1">
                <div class="flex items-center gap-2 px-3 py-2 mb-4">
                  <div class="w-6 h-6 bg-trust-blue rounded"></div>
                  <span class="text-white font-bold text-sm">CareerBridge</span>
                </div>
                <div class="px-3 py-2 bg-trust-blue/20 border border-trust-blue/30 rounded-xl flex items-center gap-2">
                  <div class="w-3.5 h-3.5 bg-trust-blue rounded opacity-80"></div>
                  <span class="text-blue-300 text-xs font-semibold">Dashboard</span>
                </div>
                <div class="px-3 py-2 rounded-xl flex items-center gap-2 opacity-40">
                  <div class="w-3.5 h-3.5 bg-slate-400 rounded opacity-60"></div>
                  <span class="text-slate-400 text-xs">Jobs</span>
                </div>
                <div class="px-3 py-2 rounded-xl flex items-center gap-2 opacity-40">
                  <div class="w-3.5 h-3.5 bg-slate-400 rounded opacity-60"></div>
                  <span class="text-slate-400 text-xs">Applicants</span>
                </div>
              </div>
              <!-- Main -->
              <div class="flex-1 bg-slate-50 p-6">
                <div class="flex items-center justify-between mb-6">
                  <div>
                    <div class="h-3 w-20 bg-slate-300 rounded mb-2 opacity-60"></div>
                    <div class="h-5 w-36 bg-slate-800 rounded opacity-80"></div>
                  </div>
                  <div class="w-9 h-9 bg-trust-blue rounded-xl opacity-80"></div>
                </div>
                <!-- Stats -->
                <div class="grid grid-cols-3 gap-3 mb-5">
                  <div v-for="(col, i) in ['bg-trust-blue', 'bg-indigo-500', 'bg-emerald-500']" :key="i"
                    class="bg-white rounded-xl p-4 border border-slate-200 shadow-sm">
                    <div class="h-2.5 w-16 bg-slate-200 rounded mb-3"></div>
                    <div class="h-7 w-10 rounded" :class="col" style="opacity:0.85"></div>
                  </div>
                </div>
                <!-- Table rows -->
                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                  <div class="flex items-center px-4 py-2.5 border-b border-slate-100 bg-slate-50">
                    <div class="h-2.5 w-20 bg-slate-200 rounded mr-auto"></div>
                    <div class="h-2.5 w-14 bg-slate-200 rounded mr-6"></div>
                    <div class="h-2.5 w-14 bg-slate-200 rounded"></div>
                  </div>
                  <div v-for="j in 3" :key="j" class="flex items-center px-4 py-3 border-b border-slate-50 last:border-0">
                    <div class="w-7 h-7 rounded-full mr-3 shrink-0" :class="['bg-blue-100', 'bg-purple-100', 'bg-green-100'][j-1]"></div>
                    <div class="flex-1"><div class="h-3 rounded mb-1" :class="['bg-slate-200 w-28', 'bg-slate-200 w-36', 'bg-slate-200 w-24'][j-1]"></div></div>
                    <div class="h-5 w-16 rounded-full mr-5" :class="['bg-blue-100', 'bg-amber-100', 'bg-emerald-100'][j-1]"></div>
                    <div class="h-5 w-20 bg-trust-blue/80 rounded-lg"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURES – compact section -->
    <section class="py-20 px-6 bg-slate-50 border-t border-b border-slate-100">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-14">
          <h2 class="text-4xl font-heading font-black tracking-tight text-slate-900 mb-4">Built for the whole pipeline</h2>
          <p class="text-xl text-slate-500 max-w-xl mx-auto">From first application to final offer, everything your placement cell needs — in one tool.</p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feat in features" :key="feat.title"
            class="bg-white rounded-2xl p-6 border border-slate-100 hover:border-slate-300 hover:shadow-md transition-all duration-200 group">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-4 text-white" :class="feat.color">
              <component :is="feat.icon" class="w-5 h-5" />
            </div>
            <h3 class="font-bold text-slate-900 mb-2">{{ feat.title }}</h3>
            <p class="text-slate-500 text-sm leading-relaxed">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FOR STUDENTS / COMPANIES split -->
    <section class="py-24 px-6">
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Students -->
          <div class="bg-trust-blue rounded-3xl p-8 text-white relative overflow-hidden">
            <div class="absolute -right-8 -bottom-8 w-48 h-48 bg-white/5 rounded-full"></div>
            <div class="relative">
              <div class="inline-flex items-center gap-2 bg-white/15 px-3 py-1.5 rounded-full text-sm font-semibold mb-6">
                <GraduationCap class="w-4 h-4" /> For Students
              </div>
              <h3 class="text-2xl font-bold mb-3 leading-snug">Launch your career with confidence</h3>
              <p class="text-blue-100 text-sm leading-relaxed mb-6">Build your profile, discover opportunities that match your skills, and track every step of your application journey — no more guessing.</p>
              <ul class="space-y-2.5">
                <li v-for="item in studentFeatures" :key="item" class="flex items-center gap-2.5 text-sm">
                  <CheckCircle class="w-4 h-4 text-blue-200 shrink-0" /><span class="text-blue-50">{{ item }}</span>
                </li>
              </ul>
              <router-link to="/register?role=student" class="mt-8 inline-flex items-center gap-2 bg-white text-trust-blue font-bold px-6 py-3 rounded-xl text-sm hover:bg-blue-50 transition">
                Register as Student <ArrowRight class="w-4 h-4" />
              </router-link>
            </div>
          </div>
          <!-- Companies -->
          <div class="bg-slate-900 rounded-3xl p-8 text-white relative overflow-hidden">
            <div class="absolute -right-8 -bottom-8 w-48 h-48 bg-white/5 rounded-full"></div>
            <div class="relative">
              <div class="inline-flex items-center gap-2 bg-white/15 px-3 py-1.5 rounded-full text-sm font-semibold mb-6">
                <Briefcase class="w-4 h-4" /> For Companies
              </div>
              <h3 class="text-2xl font-bold mb-3 leading-snug">Hire better, faster.</h3>
              <p class="text-slate-300 text-sm leading-relaxed mb-6">Post jobs, review applicants inline, schedule video interviews, and move candidates through your pipeline — all without leaving the platform.</p>
              <ul class="space-y-2.5">
                <li v-for="item in companyFeatures" :key="item" class="flex items-center gap-2.5 text-sm">
                  <CheckCircle class="w-4 h-4 text-slate-400 shrink-0" /><span class="text-slate-200">{{ item }}</span>
                </li>
              </ul>
              <router-link to="/register?role=company" class="mt-8 inline-flex items-center gap-2 bg-white text-slate-900 font-bold px-6 py-3 rounded-xl text-sm hover:bg-slate-100 transition">
                Register your Company <ArrowRight class="w-4 h-4" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS BAR -->
    <section class="py-16 px-6 bg-slate-50 border-t border-slate-100">
      <div class="max-w-4xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label">
            <p class="text-4xl font-heading font-black text-slate-900 mb-1">{{ stat.value }}</p>
            <p class="text-slate-500 text-sm">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-28 px-6">
      <div class="max-w-2xl mx-auto text-center">
        <h2 class="text-4xl sm:text-5xl font-heading font-black tracking-tight text-slate-900 mb-6">Ready to get started?</h2>
        <p class="text-xl text-slate-500 mb-10">Join students and companies already using CareerBridge to make campus placements effortless.</p>
        <router-link to="/register" class="inline-flex items-center gap-2 bg-slate-900 hover:bg-slate-700 text-white font-bold px-10 py-5 rounded-2xl transition text-lg">
          Create Free Account <ArrowRight class="w-5 h-5" />
        </router-link>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="border-t border-slate-100 py-12 px-6 bg-white">
      <div class="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 bg-trust-blue rounded-lg flex items-center justify-center">
            <span class="text-white font-black text-xs">CB</span>
          </div>
          <span class="font-heading font-bold text-lg tracking-tight">CareerBridge</span>
          <span class="text-slate-300 mx-2">·</span>
          <span class="text-slate-400 text-sm">&copy; {{ new Date().getFullYear() }}</span>
        </div>
        <div class="flex items-center gap-6 text-sm text-slate-500">
          <a href="#" class="hover:text-slate-900 transition">Privacy</a>
          <a href="#" class="hover:text-slate-900 transition">Terms</a>
          <router-link to="/login" class="hover:text-slate-900 transition">Login</router-link>
          <router-link to="/register" class="hover:text-slate-900 transition font-semibold text-trust-blue">Register</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ArrowRight, Video, Activity, Briefcase, ShieldCheck, BarChart3, Users, GraduationCap, CheckCircle } from "lucide-vue-next"

export default {
  name: "Home",
  components: { ArrowRight, GraduationCap, Briefcase, CheckCircle },
  data() {
    return {
      features: [
        { icon: Video, title: "Live Video Interviews", desc: "One-click WebRTC video rooms. Host interviews directly on the platform, no third-party app needed.", color: "bg-trust-blue" },
        { icon: Activity, title: "Real-Time Pipeline", desc: "Move candidates from Applied to Hired with full visibility at every stage for students and companies.", color: "bg-indigo-500" },
        { icon: Briefcase, title: "Smart Job Board", desc: "Post detailed jobs with CGPA, branch, and experience filters. Students see only the opportunities they qualify for.", color: "bg-amber-500" },
        { icon: ShieldCheck, title: "Secure & Isolated", desc: "Role-based access control with JWT authentication. Student, company, and admin data are strictly separated.", color: "bg-emerald-500" },
        { icon: BarChart3, title: "Automated Reports", desc: "Auto-generated monthly placement reports sent straight to admin and company dashboards.", color: "bg-rose-500" },
        { icon: Users, title: "Three-Role System", desc: "Dedicated dashboards for Students, Companies, and Administrators — each with the exact tools they need.", color: "bg-violet-500" },
      ],
      studentFeatures: ["Transparent application status", "Interview countdown timer", "One-tap video room access", "Resume inline viewer"],
      companyFeatures: ["Post jobs in under 2 minutes", "View resumes without downloading", "Integrated AM/PM scheduler", "Private notes on candidates"],
      stats: [
        { value: "1,200+", label: "Students placed" },
        { value: "300+", label: "Partner companies" },
        { value: "5,000+", label: "Applications processed" },
        { value: "99.9%", label: "Uptime" },
      ]
    }
  }
}
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}
</style>