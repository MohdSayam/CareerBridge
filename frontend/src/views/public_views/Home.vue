<template>
  <div class="bg-[#080B14] text-white overflow-x-hidden" style="font-family: 'Inter', sans-serif;">

    <!-- ══════════════════════════════════════════════
         NAVBAR — sticky, glassmorphism
    ═══════════════════════════════════════════════ -->
    <nav class="fixed top-0 left-0 right-0 z-50 border-b border-white/[0.06]"
         :class="scrolled ? 'bg-[#080B14]/95 backdrop-blur-xl' : 'bg-transparent'">
      <div class="max-w-7xl mx-auto px-5 sm:px-8 h-[68px] flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" alt="CareerBridge" class="w-7 h-7" />
          <span class="font-bold text-lg tracking-tight text-white">CareerBridge</span>
        </div>
        <div class="hidden md:flex items-center gap-8">
          <a href="#features" @click.prevent="scrollTo('features')" class="text-gray-400 hover:text-white text-sm font-medium transition-colors">Features</a>
          <a href="#how" @click.prevent="scrollTo('how')" class="text-gray-400 hover:text-white text-sm font-medium transition-colors">How it works</a>
          <a href="#roles" @click.prevent="scrollTo('roles')" class="text-gray-400 hover:text-white text-sm font-medium transition-colors">For you</a>
        </div>
        <div class="flex items-center gap-3">
          <router-link to="/login" class="text-gray-400 hover:text-white text-sm font-medium transition-colors px-4 py-2">Sign In</router-link>
          <router-link to="/register"
            class="bg-violet-600 hover:bg-violet-500 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-all shadow-lg shadow-violet-500/25 hover:shadow-violet-500/40 hover:-translate-y-px">
            Get Started →
          </router-link>
        </div>
      </div>
    </nav>

    <!-- ══════════════════════════════════════════════
         HERO
    ═══════════════════════════════════════════════ -->
    <section class="relative min-h-screen flex flex-col items-center justify-center pt-24 pb-16 px-5 overflow-hidden">

      <!-- Background mesh/grid -->
      <div class="absolute inset-0 pointer-events-none" style="background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.04) 1px, transparent 0); background-size: 40px 40px;"></div>

      <!-- Glow orbs -->
      <div class="absolute top-[20%] left-[15%] w-[500px] h-[500px] bg-violet-700/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div class="absolute top-[30%] right-[10%] w-[400px] h-[400px] bg-indigo-700/15 rounded-full blur-[100px] pointer-events-none"></div>
      <div class="absolute bottom-[10%] left-[40%] w-[300px] h-[300px] bg-cyan-700/10 rounded-full blur-[80px] pointer-events-none"></div>

      <div class="relative max-w-5xl mx-auto text-center z-10">

        <!-- Badge -->
        <div class="inline-flex items-center gap-2.5 bg-violet-500/10 border border-violet-500/25 text-violet-300 px-4 py-2 rounded-full text-sm font-medium mb-8 animate-fade-in">
          <span class="w-2 h-2 bg-violet-400 rounded-full animate-pulse"></span>
          Campus Placement Platform — Built for India's colleges
        </div>

        <!-- Headline -->
        <h1 class="text-5xl sm:text-6xl lg:text-[80px] font-black tracking-[-0.03em] leading-[1.02] mb-7 animate-fade-in-up">
          Where campus talent<br/>
          <span class="bg-gradient-to-r from-violet-400 via-indigo-400 to-cyan-400 bg-clip-text text-transparent">meets real opportunity</span>
        </h1>

        <!-- Subheadline -->
        <p class="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed mb-10 animate-fade-in-up" style="animation-delay: 0.1s">
          CareerBridge is a full-stack campus placement portal — students apply for jobs they actually qualify for, companies run their entire hiring pipeline, and admins get a bird's-eye view of every placement.
        </p>

        <!-- CTAs -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in-up" style="animation-delay: 0.2s">
          <router-link to="/register"
            class="inline-flex items-center justify-center gap-2 bg-violet-600 hover:bg-violet-500 text-white font-bold px-8 py-4 rounded-2xl transition-all shadow-2xl shadow-violet-500/30 hover:shadow-violet-500/50 hover:-translate-y-0.5 text-base">
            Start for free
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
          </router-link>
          <router-link to="/login"
            class="inline-flex items-center justify-center gap-2 bg-white/[0.06] border border-white/[0.1] hover:bg-white/[0.1] text-white font-semibold px-8 py-4 rounded-2xl transition-all text-base">
            Sign in to your account
          </router-link>
        </div>

        <p class="text-gray-600 text-sm mt-5 animate-fade-in-up" style="animation-delay: 0.3s">Free for students · No credit card</p>
      </div>

      <!-- Hero image — dashboard screenshot -->
      <div class="relative max-w-6xl w-full mx-auto mt-20 px-4 z-10 animate-fade-in-up" style="animation-delay: 0.35s">
        <!-- Glow under card -->
        <div class="absolute -bottom-8 left-1/2 -translate-x-1/2 w-2/3 h-32 bg-violet-600/20 blur-3xl rounded-full"></div>

        <!-- Browser frame -->
        <div class="relative bg-[#111827]/90 border border-white/[0.08] rounded-2xl overflow-hidden shadow-2xl shadow-black/60 backdrop-blur-md">
          <!-- Browser top bar -->
          <div class="flex items-center gap-3 px-5 py-3.5 bg-[#1a2133]/80 border-b border-white/[0.06]">
            <div class="flex gap-1.5">
              <div class="w-3 h-3 rounded-full bg-red-500/70"></div>
              <div class="w-3 h-3 rounded-full bg-yellow-500/70"></div>
              <div class="w-3 h-3 rounded-full bg-green-500/70"></div>
            </div>
            <div class="flex-1 bg-[#0d1526]/70 rounded-lg px-4 py-1.5 text-gray-500 text-xs font-mono">
              careerbridge.app/company/dashboard
            </div>
            <div class="flex gap-2">
              <div class="w-4 h-4 rounded bg-white/5"></div>
              <div class="w-4 h-4 rounded bg-white/5"></div>
            </div>
          </div>

          <!-- App UI mockup -->
          <div class="flex" style="min-height: 360px;">
            <!-- Sidebar -->
            <div class="hidden sm:flex w-52 bg-[#0d1424] flex-col p-4 gap-1 border-r border-white/[0.05] shrink-0">
              <div class="flex items-center gap-2.5 px-3 py-2.5 mb-3">
                <img src="/favicon.svg" class="w-5 h-5" alt="CB" />
                <span class="text-white font-bold text-sm">CareerBridge</span>
              </div>
              <div v-for="(item, i) in sidebarItems" :key="i"
                class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-xs font-medium transition-all"
                :class="i === 0 ? 'bg-violet-600/20 text-violet-300 border border-violet-500/20' : 'text-gray-500 hover:text-gray-300'">
                <span class="w-1.5 h-1.5 rounded-full" :class="i === 0 ? 'bg-violet-400' : 'bg-gray-600'"></span>
                {{ item }}
              </div>
            </div>

            <!-- Main content area -->
            <div class="flex-1 bg-[#0b1120] p-6 overflow-hidden">
              <!-- Top bar -->
              <div class="flex items-center justify-between mb-6">
                <div>
                  <div class="text-gray-500 text-xs font-medium mb-1">Good morning,</div>
                  <div class="text-white font-bold text-lg">Company Dashboard</div>
                </div>
                <div class="flex items-center gap-3">
                  <div class="px-3 py-1.5 bg-violet-600/20 border border-violet-500/20 rounded-xl text-violet-300 text-xs font-semibold">+ Post Job</div>
                  <div class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-indigo-600 flex items-center justify-center text-xs font-bold">TC</div>
                </div>
              </div>

              <!-- Stat cards -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                <div v-for="(stat, i) in dashStats" :key="i" class="bg-[#111827]/80 border border-white/[0.06] rounded-xl p-4">
                  <div class="text-gray-500 text-xs mb-2">{{ stat.label }}</div>
                  <div class="font-black text-xl" :class="stat.color">{{ stat.value }}</div>
                  <div class="text-xs mt-1" :class="stat.color" style="opacity:0.7">{{ stat.trend }}</div>
                </div>
              </div>

              <!-- Applicant list -->
              <div class="bg-[#111827]/60 border border-white/[0.06] rounded-xl overflow-hidden">
                <div class="flex items-center px-4 py-2.5 border-b border-white/[0.04] bg-[#0d1526]/50">
                  <span class="text-gray-400 text-xs font-semibold flex-1">Recent Applicants</span>
                  <span class="text-gray-600 text-xs">Status</span>
                </div>
                <div v-for="(app, i) in mockApplicants" :key="i" class="flex items-center px-4 py-3 border-b border-white/[0.03] last:border-0 hover:bg-white/[0.02] transition-colors">
                  <div class="w-7 h-7 rounded-full mr-3 shrink-0 flex items-center justify-center text-xs font-bold"
                    :class="app.color">{{ app.initials }}</div>
                  <div class="flex-1 min-w-0">
                    <div class="text-white text-xs font-semibold truncate">{{ app.name }}</div>
                    <div class="text-gray-500 text-xs">{{ app.role }}</div>
                  </div>
                  <div class="hidden sm:flex items-center gap-1.5 mr-4">
                    <div class="w-1.5 h-1.5 rounded-full" :class="app.dotColor"></div>
                    <span class="text-xs font-medium" :class="app.textColor">{{ app.status }}</span>
                  </div>
                  <div class="w-16 h-6 bg-violet-600/70 rounded-lg text-xs font-semibold flex items-center justify-center text-white">Review</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         LOGOS / TRUST BAR
    ═══════════════════════════════════════════════ -->
    <section class="py-14 px-5 border-t border-white/[0.05]">
      <div class="max-w-4xl mx-auto text-center">
        <p class="text-gray-600 text-sm font-medium mb-8 uppercase tracking-widest">Connects students with companies across India</p>
        <div class="flex flex-wrap items-center justify-center gap-x-12 gap-y-6">
          <div v-for="company in companies" :key="company"
            class="text-gray-600 font-bold text-sm tracking-wide hover:text-gray-300 transition-colors cursor-default">{{ company }}</div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         FEATURES GRID
    ═══════════════════════════════════════════════ -->
    <section id="features" class="py-28 px-5 relative">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-violet-900/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="max-w-7xl mx-auto relative z-10">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 px-4 py-1.5 rounded-full text-sm font-medium mb-5">
            Platform Capabilities
          </div>
          <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-5">Everything your placement cell needs</h2>
          <p class="text-gray-400 text-xl max-w-2xl mx-auto">From first application to final offer letter, the entire campus hiring flow — in one tab.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <div v-for="feat in features" :key="feat.title"
            class="group bg-white/[0.03] border border-white/[0.07] rounded-2xl p-7 hover:bg-white/[0.06] hover:border-white/[0.12] transition-all duration-300 hover:-translate-y-1">
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center mb-5 text-2xl" :class="feat.bg">
              {{ feat.emoji }}
            </div>
            <h3 class="font-bold text-white text-lg mb-2.5">{{ feat.title }}</h3>
            <p class="text-gray-400 text-sm leading-relaxed">{{ feat.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         HOW IT WORKS
    ═══════════════════════════════════════════════ -->
    <section id="how" class="py-28 px-5 bg-[#060910] border-y border-white/[0.05]">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-5">How it works</h2>
          <p class="text-gray-400 text-xl max-w-xl mx-auto">Three simple steps from sign-up to placement.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          <!-- Connector line (desktop) -->
          <div class="hidden md:block absolute top-10 left-[16.67%] right-[16.67%] h-px bg-gradient-to-r from-violet-500/0 via-violet-500/50 to-violet-500/0"></div>

          <div v-for="(step, i) in howSteps" :key="i" class="flex flex-col items-center text-center relative">
            <div class="w-20 h-20 rounded-3xl flex items-center justify-center mb-6 relative z-10 text-3xl border" :class="step.bg">
              {{ step.emoji }}
            </div>
            <div class="text-violet-400 text-xs font-bold uppercase tracking-widest mb-2">Step {{ i + 1 }}</div>
            <h3 class="text-white font-bold text-xl mb-3">{{ step.title }}</h3>
            <p class="text-gray-400 text-sm leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         ROLES (SPLIT CARDS)
    ═══════════════════════════════════════════════ -->
    <section id="roles" class="py-28 px-5">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-5">Built for every role</h2>
          <p class="text-gray-400 text-xl max-w-xl mx-auto">Three dashboards. One platform. Everyone gets exactly what they need.</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <!-- Student -->
          <div class="relative bg-gradient-to-br from-violet-950/70 to-indigo-950/50 border border-violet-500/20 rounded-3xl p-8 overflow-hidden group hover:border-violet-500/40 transition-all duration-300">
            <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-violet-600/10 rounded-full blur-2xl group-hover:bg-violet-600/20 transition-all duration-500"></div>
            <div class="relative">
              <div class="text-4xl mb-5">👨‍🎓</div>
              <h3 class="text-xl font-bold text-white mb-2">For Students</h3>
              <p class="text-violet-200/70 text-sm mb-6 leading-relaxed">See only jobs you qualify for. Apply in one click. Join video interviews without leaving the browser.</p>
              <ul class="space-y-2.5 mb-7">
                <li v-for="item in studentFeatures" :key="item" class="flex items-start gap-2.5 text-sm text-violet-100">
                  <svg class="w-4 h-4 text-violet-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                  {{ item }}
                </li>
              </ul>
              <router-link to="/register?role=student" class="inline-flex items-center gap-2 text-sm font-bold text-violet-300 hover:text-white transition-colors">
                Register as Student →
              </router-link>
            </div>
          </div>

          <!-- Company — Featured -->
          <div class="relative bg-gradient-to-br from-[#151b2e] to-[#0d1120] border border-indigo-500/30 rounded-3xl p-8 overflow-hidden lg:-mt-4 lg:mb-4 shadow-2xl shadow-indigo-900/40 group hover:border-indigo-500/50 transition-all duration-300">
            <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/60 to-transparent"></div>
            <div class="absolute -right-8 -bottom-8 w-48 h-48 bg-indigo-600/10 rounded-full blur-2xl group-hover:bg-indigo-600/20 transition-all duration-500"></div>
            <div class="absolute top-5 right-5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-bold px-3 py-1 rounded-full">Most used</div>
            <div class="relative">
              <div class="text-4xl mb-5">🏢</div>
              <h3 class="text-xl font-bold text-white mb-2">For Companies</h3>
              <p class="text-gray-300/70 text-sm mb-6 leading-relaxed">Post jobs with eligibility filters, manage your hiring pipeline, conduct video interviews, and mark candidates placed — all in one place.</p>
              <ul class="space-y-2.5 mb-7">
                <li v-for="item in companyFeatures" :key="item" class="flex items-start gap-2.5 text-sm text-gray-200">
                  <svg class="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                  {{ item }}
                </li>
              </ul>
              <router-link to="/register?role=company" class="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-bold px-5 py-2.5 rounded-xl transition-all shadow-lg shadow-indigo-500/20">
                Register your Company →
              </router-link>
            </div>
          </div>

          <!-- Admin -->
          <div class="relative bg-gradient-to-br from-emerald-950/60 to-teal-950/40 border border-emerald-500/20 rounded-3xl p-8 overflow-hidden group hover:border-emerald-500/40 transition-all duration-300">
            <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-emerald-600/10 rounded-full blur-2xl group-hover:bg-emerald-600/20 transition-all duration-500"></div>
            <div class="relative">
              <div class="text-4xl mb-5">🔑</div>
              <h3 class="text-xl font-bold text-white mb-2">For Admins</h3>
              <p class="text-emerald-100/60 text-sm mb-6 leading-relaxed">Full visibility across the platform. Approve companies, monitor placements, and receive automated weekly reports.</p>
              <ul class="space-y-2.5 mb-7">
                <li v-for="item in adminFeatures" :key="item" class="flex items-start gap-2.5 text-sm text-emerald-100">
                  <svg class="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                  {{ item }}
                </li>
              </ul>
              <span class="text-sm text-emerald-400/70 font-medium">Admin credentials provided by institute</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         INTERVIEW SECTION — Real image
    ═══════════════════════════════════════════════ -->
    <section class="py-28 px-5 bg-[#060910] border-t border-white/[0.05] overflow-hidden">
      <div class="max-w-6xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          <!-- Left: copy -->
          <div>
            <div class="inline-flex items-center gap-2 bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
              📹 Built-in Video Interviews
            </div>
            <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-6 leading-tight">
              No Zoom.<br/>No Google Meet.<br/>
              <span class="bg-gradient-to-r from-cyan-400 to-indigo-400 bg-clip-text text-transparent">Just one tab.</span>
            </h2>
            <p class="text-gray-400 text-lg leading-relaxed mb-8">
              CareerBridge has a fully built-in WebRTC video calling system. When a company schedules an interview, both sides get a direct link. Camera, mic, and screen sharing — all inside the browser. No accounts, no downloads.
            </p>
            <div class="space-y-4">
              <div v-for="item in interviewFeats" :key="item.text" class="flex items-center gap-3.5">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0 text-lg" :class="item.bg">{{ item.icon }}</div>
                <span class="text-gray-300 font-medium text-sm">{{ item.text }}</span>
              </div>
            </div>
          </div>

          <!-- Right: screenshot from Unsplash (video call scene) -->
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-br from-cyan-600/10 to-indigo-600/10 rounded-3xl blur-3xl -z-10 scale-105"></div>
            <div class="relative rounded-2xl overflow-hidden border border-white/[0.08] shadow-2xl shadow-black/50">
              <img
                src="https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=700&q=80&auto=format&fit=crop"
                alt="Live video interview in browser"
                class="w-full object-cover"
                style="max-height: 400px; object-position: center top;"
              />
              <!-- Overlay badge -->
              <div class="absolute bottom-5 left-5 right-5">
                <div class="bg-[#080B14]/90 border border-white/10 backdrop-blur-xl rounded-xl p-4 flex items-center gap-3">
                  <div class="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse shrink-0"></div>
                  <div>
                    <div class="text-white font-bold text-sm">Interview in progress</div>
                    <div class="text-gray-400 text-xs">Peer-to-peer · Encrypted · No third-party</div>
                  </div>
                  <div class="ml-auto bg-red-500/20 border border-red-500/30 text-red-400 text-xs font-bold px-2.5 py-1 rounded-lg">● LIVE</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         EMAIL NOTIFICATIONS SECTION
    ═══════════════════════════════════════════════ -->
    <section class="py-28 px-5">
      <div class="max-w-6xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

          <!-- Left: image of someone receiving email on phone -->
          <div class="relative order-2 lg:order-1">
            <div class="absolute inset-0 bg-gradient-to-br from-violet-600/10 to-pink-600/10 rounded-3xl blur-3xl -z-10 scale-105"></div>
            <div class="relative rounded-2xl overflow-hidden border border-white/[0.08] shadow-2xl shadow-black/50">
              <img
                src="https://images.unsplash.com/photo-1596526131083-e8c633c948d2?w=700&q=80&auto=format&fit=crop"
                alt="Email notification on phone"
                class="w-full object-cover"
                style="max-height: 400px;"
              />
              <!-- Email preview overlay -->
              <div class="absolute top-5 right-5 left-5">
                <div class="bg-[#080B14]/90 border border-white/10 backdrop-blur-xl rounded-xl p-4">
                  <div class="flex items-center gap-2 mb-2">
                    <img src="/favicon.svg" class="w-4 h-4" alt="CB" />
                    <span class="text-white text-xs font-bold">CareerBridge</span>
                    <span class="ml-auto text-gray-500 text-xs">now</span>
                  </div>
                  <div class="text-white text-sm font-semibold">🎉 Interview Scheduled!</div>
                  <div class="text-gray-400 text-xs mt-0.5">Your interview with TechCorp is set for Oct 12, 2PM IST</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: copy -->
          <div class="order-1 lg:order-2">
            <div class="inline-flex items-center gap-2 bg-violet-500/10 border border-violet-500/20 text-violet-400 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
              📧 Automated Emails
            </div>
            <h2 class="text-4xl sm:text-5xl font-black tracking-tight text-white mb-6 leading-tight">
              Everyone gets notified<br/>
              <span class="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">at the right moment.</span>
            </h2>
            <p class="text-gray-400 text-lg leading-relaxed mb-8">
              CareerBridge sends real emails via Brevo SMTP — OTP verification, interview reminders, offer letters, weekly placement digests. Students and companies always know what's happening without having to log in.
            </p>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="mail in emailTypes" :key="mail" class="bg-white/[0.04] border border-white/[0.08] rounded-xl px-4 py-3 text-sm text-gray-300 font-medium">
                {{ mail }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         STATS
    ═══════════════════════════════════════════════ -->
    <section class="py-20 px-5 border-t border-white/[0.05] bg-[#060910]">
      <div class="max-w-5xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label">
            <div class="text-4xl sm:text-5xl font-black mb-2" :class="stat.color">{{ stat.value }}</div>
            <div class="text-gray-500 text-sm">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         TECH STACK
    ═══════════════════════════════════════════════ -->
    <section class="py-24 px-5 border-t border-white/[0.05]">
      <div class="max-w-5xl mx-auto text-center">
        <div class="text-gray-600 text-sm font-medium uppercase tracking-widest mb-10">Open source · Built with production-grade tech</div>
        <div class="flex flex-wrap items-center justify-center gap-3">
          <div v-for="tech in techStack" :key="tech.name"
            class="flex items-center gap-2 bg-white/[0.04] border border-white/[0.08] px-4 py-2.5 rounded-full text-sm font-semibold text-gray-300 hover:border-white/20 hover:text-white transition-all cursor-default">
            <span>{{ tech.icon }}</span>{{ tech.name }}
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         CTA SECTION
    ═══════════════════════════════════════════════ -->
    <section class="py-28 px-5 relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-violet-700/15 rounded-full blur-[100px]"></div>
      </div>
      <div class="relative max-w-3xl mx-auto text-center">
        <h2 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white mb-6">
          Your placement journey<br/>starts here.
        </h2>
        <p class="text-gray-400 text-xl mb-10 max-w-xl mx-auto">
          Join CareerBridge free. Students, companies, and college admins — everyone has a home here.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register"
            class="inline-flex items-center justify-center gap-2 bg-violet-600 hover:bg-violet-500 text-white font-bold px-10 py-5 rounded-2xl transition-all shadow-2xl shadow-violet-500/30 hover:shadow-violet-500/50 hover:-translate-y-0.5 text-lg">
            Create Free Account →
          </router-link>
          <a href="https://github.com/MohdSayam/CareerBridge" target="_blank" rel="noopener"
            class="inline-flex items-center justify-center gap-2 bg-white/[0.06] border border-white/[0.1] hover:bg-white/[0.10] text-white font-semibold px-10 py-5 rounded-2xl transition-all text-lg">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            View on GitHub
          </a>
        </div>
        <p class="text-gray-600 text-sm mt-6">Free forever for students · MIT Licensed · Open Source</p>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════
         FOOTER
    ═══════════════════════════════════════════════ -->
    <footer class="border-t border-white/[0.05] py-10 px-5 bg-[#060910]">
      <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" class="w-6 h-6" alt="CareerBridge" />
          <span class="font-bold text-white">CareerBridge</span>
          <span class="text-gray-700">·</span>
          <span class="text-gray-600 text-sm">© {{ new Date().getFullYear() }} · MIT License</span>
        </div>
        <div class="flex items-center gap-6 text-sm text-gray-500">
          <a href="https://github.com/MohdSayam/CareerBridge" target="_blank" class="hover:text-white transition-colors">GitHub</a>
          <router-link to="/login" class="hover:text-white transition-colors">Login</router-link>
          <router-link to="/register" class="hover:text-white transition-colors font-semibold text-violet-400">Register</router-link>
        </div>
      </div>
    </footer>

  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      scrolled: false,
      sidebarItems: ["Dashboard", "Job Listings", "Applicants", "Interviews", "Analytics", "Settings"],
      dashStats: [
        { label: "Active Jobs", value: "12", color: "text-violet-400", trend: "↑ 3 this week" },
        { label: "Applicants", value: "284", color: "text-indigo-400", trend: "↑ 47 today" },
        { label: "Interviewed", value: "61", color: "text-cyan-400", trend: "↑ 8 this week" },
        { label: "Placed", value: "23", color: "text-emerald-400", trend: "↑ 5 this month" },
      ],
      mockApplicants: [
        { initials: "AS", name: "Aryan Sharma", role: "Software Engineer", status: "Interview", dotColor: "bg-indigo-400", textColor: "text-indigo-400", color: "bg-indigo-900/60 text-indigo-300" },
        { initials: "PK", name: "Priya Kapoor", role: "Product Manager", status: "Shortlisted", dotColor: "bg-amber-400", textColor: "text-amber-400", color: "bg-amber-900/60 text-amber-300" },
        { initials: "RM", name: "Rahul Mehra", role: "Data Analyst", status: "Applied", dotColor: "bg-gray-500", textColor: "text-gray-400", color: "bg-gray-800/60 text-gray-300" },
      ],
      companies: ["TCS", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "Cognizant", "Capgemini"],
      features: [
        { emoji: "🎯", title: "Smart Job Matching", desc: "Jobs are filtered by your CGPA, branch, and graduation year. Students only see roles they're actually eligible for — no more irrelevant listings.", bg: "bg-violet-600/20" },
        { emoji: "📹", title: "Built-in Video Interviews", desc: "Peer-to-peer WebRTC video calling right in the browser. No Zoom, no third-party APIs. Company and student connect directly — camera, mic, and screen share included.", bg: "bg-indigo-600/20" },
        { emoji: "📊", title: "Real-time Pipeline Tracking", desc: "Every application moves through Applied → Shortlisted → Interview → Selected → Placed. Both sides see status updates the moment they happen.", bg: "bg-cyan-600/20" },
        { emoji: "📧", title: "Automated Email Notifications", desc: "OTP verification, interview reminders, offer letters, weekly placement digests — all sent automatically via Brevo SMTP to real email inboxes.", bg: "bg-amber-600/20" },
        { emoji: "🔒", title: "Role-based Access Control", desc: "JWT-secured authentication with three completely isolated dashboards — students, companies, and admin each see only what they should.", bg: "bg-emerald-600/20" },
        { emoji: "📄", title: "Monthly Placement Reports", desc: "Automated CSV reports of all placement activity sent to admin and company dashboards on a scheduled basis via Celery Beat.", bg: "bg-rose-600/20" },
      ],
      howSteps: [
        { emoji: "📝", title: "Create your profile", desc: "Sign up with email + OTP or Google OAuth. Build your profile with education, skills, CGPA and upload your résumé.", bg: "bg-violet-600/20 border-violet-500/20 text-white" },
        { emoji: "🔍", title: "Find your match", desc: "Students browse eligible jobs. Companies post opportunities with filters. The system connects the right people automatically.", bg: "bg-indigo-600/20 border-indigo-500/20 text-white" },
        { emoji: "🏆", title: "Get placed", desc: "Interview directly in the app. Status updates flow in real time. Offer letters arrive by email. The entire process — start to finish.", bg: "bg-emerald-600/20 border-emerald-500/20 text-white" },
      ],
      studentFeatures: [
        "One-click apply for eligible jobs",
        "Real-time application status",
        "Interview countdown timer",
        "Join video room in one click",
        "Resume inline viewer",
      ],
      companyFeatures: [
        "Post jobs with eligibility filters",
        "Kanban-style hiring pipeline",
        "View résumés without downloading",
        "Schedule & run video interviews",
        "Private notes on candidates",
      ],
      adminFeatures: [
        "Global placement statistics",
        "Approve/reject company registrations",
        "Weekly automated digest emails",
        "Full student & company oversight",
      ],
      interviewFeats: [
        { icon: "🎥", text: "Camera & microphone control in-call", bg: "bg-cyan-600/20" },
        { icon: "🖥️", text: "Screen sharing for technical interviews", bg: "bg-indigo-600/20" },
        { icon: "📝", text: "Company takes private notes during the call", bg: "bg-violet-600/20" },
        { icon: "⚡", text: "Update candidate status without leaving the room", bg: "bg-emerald-600/20" },
      ],
      emailTypes: ["✉️ OTP Verification", "📅 Interview Reminder", "🎉 Offer Letter PDF", "📊 Weekly Digest"],
      stats: [
        { value: "3", label: "Roles supported", color: "text-violet-400" },
        { value: "100%", label: "Free for students", color: "text-emerald-400" },
        { value: "6", label: "Free-tier services", color: "text-indigo-400" },
        { value: "0₹", label: "Cost to deploy", color: "text-cyan-400" },
      ],
      techStack: [
        { icon: "🐍", name: "Python + Flask" },
        { icon: "⚡", name: "Vue 3 + Vite" },
        { icon: "🐘", name: "PostgreSQL (Neon)" },
        { icon: "🔴", name: "Redis (Upstash)" },
        { icon: "🌿", name: "Celery + Beat" },
        { icon: "📡", name: "WebRTC + Socket.IO" },
        { icon: "☁️", name: "Cloudinary" },
        { icon: "📧", name: "Brevo SMTP" },
        { icon: "🔐", name: "JWT + Google OAuth" },
        { icon: "🐋", name: "Docker + Supervisord" },
        { icon: "▲", name: "Vercel" },
        { icon: "🎨", name: "Render" },
      ],
    }
  },
  mounted() {
    window.addEventListener("scroll", this.onScroll)
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.onScroll)
  },
  methods: {
    onScroll() {
      this.scrolled = window.scrollY > 20
    },
    scrollTo(id) {
      const el = document.getElementById(id)
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" })
    }
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.7s ease both;
}
.animate-fade-in-up {
  animation: fade-in-up 0.7s ease both;
}
</style>