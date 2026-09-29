<template>
  <div class="bg-gray-950 text-white overflow-x-hidden">

    <!-- NAV -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-gray-950/80 backdrop-blur-xl border-b border-white/5">
      <div class="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <span class="text-white font-black text-sm">CB</span>
          </div>
          <span class="font-bold text-lg tracking-tight text-white">CareerBridge</span>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/login" class="text-gray-400 hover:text-white font-medium transition px-4 py-2 text-sm">Sign In</router-link>
          <router-link to="/register" class="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-4 py-2 rounded-xl transition text-sm shadow-lg shadow-indigo-500/20">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="relative min-h-screen flex flex-col items-center justify-center pt-16 px-5 overflow-hidden">
      <!-- Gradient orbs -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute top-1/3 left-1/4 w-72 h-72 bg-violet-600/15 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute top-1/3 right-1/4 w-72 h-72 bg-cyan-600/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="relative max-w-4xl mx-auto text-center z-10">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 px-4 py-1.5 rounded-full text-sm font-medium mb-8">
          <span class="w-1.5 h-1.5 bg-indigo-400 rounded-full animate-pulse"></span>
          Campus Placement Platform
        </div>

        <h1 class="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.05] mb-6">
          Where talent<br/>
          meets <span class="bg-gradient-to-r from-indigo-400 via-violet-400 to-cyan-400 bg-clip-text text-transparent">opportunity</span>
        </h1>

        <p class="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed mb-10">
          The modern placement portal built for students, companies, and colleges. Apply, interview, and get placed — all in one place.
        </p>

        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register" class="inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-8 py-4 rounded-2xl transition text-base shadow-2xl shadow-indigo-500/30">
            Start for free <ArrowRight class="w-5 h-5" />
          </router-link>
          <router-link to="/login" class="inline-flex items-center justify-center gap-2 bg-white/5 border border-white/10 hover:bg-white/10 text-white font-semibold px-8 py-4 rounded-2xl transition text-base">
            Sign in
          </router-link>
        </div>
        <p class="text-gray-600 text-sm mt-6">No credit card required · 100% free for students</p>
      </div>

      <!-- Dashboard Preview Card -->
      <div class="relative max-w-5xl w-full mx-auto mt-16 z-10 px-2">
        <div class="bg-gray-900/80 border border-white/10 rounded-2xl overflow-hidden shadow-2xl shadow-black/40 backdrop-blur-xl">
          <!-- Fake browser bar -->
          <div class="bg-gray-800/60 px-5 py-3 flex items-center gap-3 border-b border-white/5">
            <div class="flex gap-1.5">
              <div class="w-3 h-3 rounded-full bg-red-500/70"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500/70"></div>
              <div class="w-3 h-3 rounded-full bg-green-500/70"></div>
            </div>
            <div class="flex-1 bg-gray-700/50 rounded-lg px-4 py-1.5 text-gray-400 text-xs font-mono">app.careerbridge.in/company/dashboard</div>
          </div>
          <!-- Fake Dashboard UI -->
          <div class="flex min-h-[320px]">
            <!-- Sidebar -->
            <div class="hidden sm:flex w-44 bg-gray-900 flex-col p-4 gap-1 border-r border-white/5">
              <div class="flex items-center gap-2 px-2 py-2 mb-3">
                <div class="w-6 h-6 bg-indigo-600 rounded-md"></div>
                <span class="text-white font-bold text-xs">CareerBridge</span>
              </div>
              <div class="px-3 py-2 bg-indigo-600/20 border border-indigo-500/20 rounded-xl flex items-center gap-2">
                <div class="w-3 h-3 bg-indigo-400 rounded opacity-80"></div>
                <span class="text-indigo-300 text-xs font-semibold">Dashboard</span>
              </div>
              <div v-for="label in ['Applicants', 'Interviews', 'Analytics']" :key="label" class="px-3 py-2 rounded-xl flex items-center gap-2 opacity-35">
                <div class="w-3 h-3 bg-gray-500 rounded"></div>
                <span class="text-gray-400 text-xs">{{ label }}</span>
              </div>
            </div>
            <!-- Main Content -->
            <div class="flex-1 bg-gray-950/40 p-6">
              <!-- Header -->
              <div class="flex items-center justify-between mb-5">
                <div>
                  <div class="h-2.5 w-14 bg-gray-700 rounded mb-2 opacity-50"></div>
                  <div class="h-5 w-32 bg-gray-600 rounded opacity-60"></div>
                </div>
                <div class="w-9 h-9 bg-indigo-600/70 rounded-xl"></div>
              </div>
              <!-- Stats row -->
              <div class="grid grid-cols-3 gap-3 mb-4">
                <div v-for="(col, i) in ['from-indigo-600 to-indigo-500', 'from-violet-600 to-violet-500', 'from-emerald-600 to-emerald-500']" :key="i"
                  class="bg-gray-800/50 border border-white/5 rounded-xl p-4">
                  <div class="h-2 w-14 bg-gray-600 rounded mb-3 opacity-50"></div>
                  <div class="h-7 w-10 rounded-lg bg-gradient-to-br" :class="col" style="opacity:0.8"></div>
                </div>
              </div>
              <!-- Table -->
              <div class="bg-gray-800/40 border border-white/5 rounded-xl overflow-hidden">
                <div class="flex items-center px-4 py-2.5 border-b border-white/5 bg-gray-800/30">
                  <div class="h-2 w-16 bg-gray-600 rounded mr-auto opacity-40"></div>
                  <div class="h-2 w-12 bg-gray-600 rounded mr-5 opacity-40"></div>
                  <div class="h-2 w-12 bg-gray-600 rounded opacity-40"></div>
                </div>
                <div v-for="j in 3" :key="j" class="flex items-center px-4 py-3 border-b border-white/5 last:border-0">
                  <div class="w-7 h-7 rounded-full mr-3 shrink-0 opacity-60" :class="['bg-indigo-900', 'bg-violet-900', 'bg-cyan-900'][j-1]"></div>
                  <div class="flex-1">
                    <div class="h-2.5 rounded opacity-30" :class="['bg-gray-400 w-24', 'bg-gray-400 w-32', 'bg-gray-400 w-20'][j-1]"></div>
                  </div>
                  <div class="h-5 w-14 rounded-full mr-5 opacity-50" :class="['bg-indigo-900', 'bg-amber-900', 'bg-emerald-900'][j-1]"></div>
                  <div class="h-5 w-16 bg-indigo-600/60 rounded-lg"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Glow under card -->
        <div class="absolute -bottom-10 left-1/2 -translate-x-1/2 w-3/4 h-24 bg-indigo-600/20 blur-3xl rounded-full pointer-events-none"></div>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="py-24 px-5 relative">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-14">
          <p class="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">Platform Features</p>
          <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-4">Built for the whole pipeline</h2>
          <p class="text-gray-400 text-xl max-w-xl mx-auto">From first application to final offer — everything your placement cell needs in one tool.</p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="feat in features" :key="feat.title"
            class="bg-white/5 border border-white/10 rounded-2xl p-6 hover:border-indigo-500/40 hover:bg-white/8 transition-all duration-200 group">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-4 text-white" :class="feat.color">
              <component :is="feat.icon" class="w-5 h-5" />
            </div>
            <h3 class="font-bold text-white mb-2">{{ feat.title }}</h3>
            <p class="text-gray-400 text-sm leading-relaxed">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- STUDENTS / COMPANIES -->
    <section class="py-16 px-5">
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- Students -->
          <div class="bg-gradient-to-br from-indigo-900/80 to-violet-900/50 border border-indigo-500/20 rounded-3xl p-8 relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-indigo-500/15 rounded-full blur-2xl pointer-events-none"></div>
            <div class="relative">
              <div class="inline-flex items-center gap-2 bg-white/10 border border-white/10 px-3 py-1.5 rounded-full text-sm font-semibold mb-6 text-indigo-200">
                <GraduationCap class="w-4 h-4" /> For Students
              </div>
              <h3 class="text-2xl font-bold mb-3 text-white">Launch your career with confidence</h3>
              <p class="text-indigo-200 text-sm leading-relaxed mb-6">Build your profile, discover opportunities that match your skills, and track every step — no more guessing where you stand.</p>
              <ul class="space-y-2.5 mb-8">
                <li v-for="item in studentFeatures" :key="item" class="flex items-center gap-2.5 text-sm">
                  <CheckCircle class="w-4 h-4 text-indigo-300 shrink-0" /><span class="text-indigo-100">{{ item }}</span>
                </li>
              </ul>
              <router-link to="/register?role=student" class="inline-flex items-center gap-2 bg-white text-indigo-700 font-bold px-6 py-3 rounded-xl text-sm hover:bg-indigo-50 transition">
                Register as Student <ArrowRight class="w-4 h-4" />
              </router-link>
            </div>
          </div>
          <!-- Companies -->
          <div class="bg-gradient-to-br from-gray-800/80 to-gray-900/80 border border-white/10 rounded-3xl p-8 relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
            <div class="relative">
              <div class="inline-flex items-center gap-2 bg-white/10 border border-white/10 px-3 py-1.5 rounded-full text-sm font-semibold mb-6 text-gray-200">
                <Briefcase class="w-4 h-4" /> For Companies
              </div>
              <h3 class="text-2xl font-bold mb-3 text-white">Hire better, faster.</h3>
              <p class="text-gray-300 text-sm leading-relaxed mb-6">Post jobs, review applicants, schedule video interviews, and move candidates through your pipeline — all without leaving the platform.</p>
              <ul class="space-y-2.5 mb-8">
                <li v-for="item in companyFeatures" :key="item" class="flex items-center gap-2.5 text-sm">
                  <CheckCircle class="w-4 h-4 text-gray-400 shrink-0" /><span class="text-gray-200">{{ item }}</span>
                </li>
              </ul>
              <router-link to="/register?role=company" class="inline-flex items-center gap-2 bg-white text-gray-900 font-bold px-6 py-3 rounded-xl text-sm hover:bg-gray-100 transition">
                Register your Company <ArrowRight class="w-4 h-4" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- STATS -->
    <section class="py-16 px-5 border-t border-white/5">
      <div class="max-w-4xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label">
            <p class="text-4xl font-black text-white mb-1">{{ stat.value }}</p>
            <p class="text-gray-500 text-sm">{{ stat.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-24 px-5 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-indigo-900/30 via-violet-900/20 to-transparent pointer-events-none"></div>
      <div class="relative max-w-2xl mx-auto text-center">
        <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-6">Ready to get started?</h2>
        <p class="text-xl text-gray-400 mb-10">Join students and companies already using CareerBridge to make campus placements effortless.</p>
        <router-link to="/register" class="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-10 py-5 rounded-2xl transition text-lg shadow-2xl shadow-indigo-500/30">
          Create Free Account <ArrowRight class="w-5 h-5" />
        </router-link>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="border-t border-white/5 py-10 px-5">
      <div class="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <div class="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-black text-xs">CB</span>
          </div>
          <span class="font-bold text-base text-white">CareerBridge</span>
          <span class="text-gray-700 mx-2">·</span>
          <span class="text-gray-600 text-sm">© {{ new Date().getFullYear() }}</span>
        </div>
        <div class="flex items-center gap-6 text-sm text-gray-500">
          <router-link to="/login" class="hover:text-white transition">Login</router-link>
          <router-link to="/register" class="hover:text-white transition font-semibold text-indigo-400">Register</router-link>
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
        { icon: Video, title: "Live Video Interviews", desc: "One-click WebRTC video rooms. Host interviews directly on the platform, no third-party app needed.", color: "bg-indigo-600" },
        { icon: Activity, title: "Real-Time Pipeline", desc: "Move candidates from Applied to Hired with full visibility at every stage for students and companies.", color: "bg-violet-600" },
        { icon: Briefcase, title: "Smart Job Board", desc: "Post detailed jobs with CGPA, branch, and experience filters. Students see only the opportunities they qualify for.", color: "bg-amber-600" },
        { icon: ShieldCheck, title: "Secure & Isolated", desc: "Role-based access control with JWT authentication. Student, company, and admin data are strictly separated.", color: "bg-emerald-600" },
        { icon: BarChart3, title: "Automated Reports", desc: "Auto-generated monthly placement reports sent straight to admin and company dashboards.", color: "bg-rose-600" },
        { icon: Users, title: "Three-Role System", desc: "Dedicated dashboards for Students, Companies, and Administrators — each with exactly the tools they need.", color: "bg-cyan-600" },
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