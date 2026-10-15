<template>
  <div class="bg-white text-gray-900 font-sans antialiased overflow-x-hidden w-full">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md transition-all duration-300"
         :class="{'shadow-sm border-b border-gray-100 py-2.5 sm:py-3': scrolled, 'py-3 sm:py-5': !scrolled}">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-2">
        <router-link to="/" class="flex items-center gap-2 sm:gap-3 shrink-0">
          <img src="/favicon.svg" alt="CareerBridge" class="w-7 h-7 sm:w-8 h-8" />
          <span class="font-extrabold text-lg sm:text-2xl tracking-tight text-gray-900">CareerBridge</span>
        </router-link>
        
        <div class="hidden md:flex items-center gap-8 text-sm font-semibold text-gray-600">
          <a href="#students" @click.prevent="scrollTo('students')" class="hover:text-indigo-600 transition-colors">For Candidates</a>
          <a href="#companies" @click.prevent="scrollTo('companies')" class="hover:text-indigo-600 transition-colors">For Employers</a>
        </div>
        
        <div class="flex items-center gap-1.5 sm:gap-4 shrink-0">
          <router-link to="/login" class="text-gray-600 hover:text-indigo-600 font-semibold text-xs sm:text-sm px-2.5 py-1.5 transition whitespace-nowrap">
            Login
          </router-link>
          <router-link to="/register" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs sm:text-sm font-bold px-3.5 sm:px-6 py-2 sm:py-2.5 rounded-full transition-all shadow-md hover:shadow-lg whitespace-nowrap shrink-0">
            Sign Up Free
          </router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="relative pt-24 pb-12 sm:pt-28 sm:pb-16 lg:pt-36 lg:pb-24 px-4 sm:px-6 lg:px-8 overflow-hidden min-h-[85vh] lg:min-h-[90vh] flex items-center">
      <!-- Subtle background pattern -->
      <div class="absolute inset-0 z-0 opacity-[0.15]" style="background-image: radial-gradient(#9ca3af 1px, transparent 1px); background-size: 24px 24px;"></div>
      
      <div class="max-w-7xl mx-auto w-full relative z-10 flex flex-col lg:flex-row items-center gap-10 lg:gap-16">
        <div class="flex-1 text-center lg:text-left">
          <div class="inline-block bg-indigo-50 text-indigo-700 font-bold px-3.5 py-1.5 sm:px-4 sm:py-1.5 rounded-full text-xs sm:text-sm mb-4 sm:mb-6 border border-indigo-100 max-w-full">
            India's Premium Campus Hiring Platform
          </div>
          <h1 class="text-3xl sm:text-5xl lg:text-7xl font-extrabold tracking-tight text-gray-900 leading-[1.15] mb-4 sm:mb-6">
            Find your dream job.<br />
            <span class="text-indigo-600">Without the hassle.</span>
          </h1>
          <p class="text-base sm:text-lg lg:text-xl text-gray-500 max-w-2xl mx-auto lg:mx-0 mb-8 sm:mb-10 leading-relaxed">
            CareerBridge connects premium campus talent with top-tier companies. Verified profiles, automated eligibility checks, and live video interviews — all in one platform.
          </p>
          <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center lg:justify-start w-full sm:w-auto">
            <router-link to="/register?role=student" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-base sm:text-lg px-6 sm:px-8 py-3.5 sm:py-4 rounded-full transition-all shadow-lg hover:shadow-xl text-center flex items-center justify-center gap-2">
              Apply as Candidate <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </router-link>
            <router-link to="/register?role=company" class="bg-white border-2 border-gray-200 hover:border-gray-300 text-gray-800 font-bold text-base sm:text-lg px-6 sm:px-8 py-3.5 sm:py-4 rounded-full transition-all text-center">
              Hire Top Talent
            </router-link>
          </div>
          <div class="mt-6 sm:mt-8 text-xs sm:text-sm text-gray-500 font-medium">
            Join 10,000+ students and 500+ top companies
          </div>
        </div>
        
        <div class="flex-1 w-full max-w-lg lg:max-w-none relative mt-2 sm:mt-0">
          <!-- Abstract blob behind image -->
          <div class="absolute inset-0 bg-indigo-100 rounded-full blur-3xl opacity-60 transform translate-x-4 translate-y-4 sm:translate-x-10 sm:translate-y-10 pointer-events-none"></div>
          
          <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1000&auto=format&fit=crop" alt="Students collaborating" class="relative rounded-2xl sm:rounded-[2rem] shadow-xl sm:shadow-2xl border border-gray-100 object-cover w-full h-[280px] sm:h-[400px] lg:h-[520px]" />
          
          <!-- Floating UI Card - Offer -->
          <div class="absolute -bottom-4 left-4 sm:-bottom-6 sm:-left-6 bg-white p-3.5 sm:p-5 rounded-xl sm:rounded-2xl shadow-xl border border-gray-100 flex items-center gap-3 sm:gap-4">
            <div class="w-10 h-10 sm:w-12 sm:h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-lg sm:text-xl shrink-0">🎉</div>
            <div>
              <div class="font-bold text-gray-900 text-xs sm:text-sm">Offer Accepted!</div>
              <div class="text-[11px] sm:text-xs text-gray-500 font-medium">Software Engineer at TechCorp</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- LOGOS -->
    <section class="py-8 sm:py-12 border-y border-gray-100 bg-gray-50 overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-wider mb-6 sm:mb-8">Trusted by companies hiring on campus</p>
        <div class="flex flex-wrap justify-center items-center gap-6 sm:gap-10 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
          <!-- Text-based logos for clean look -->
          <span class="text-lg sm:text-2xl font-bold text-gray-800 font-serif">Google</span>
          <span class="text-lg sm:text-2xl font-black text-gray-800 tracking-tighter">Microsoft</span>
          <span class="text-lg sm:text-2xl font-bold text-gray-800">Amazon</span>
          <span class="text-lg sm:text-2xl font-extrabold text-gray-800 italic">Swiggy</span>
          <span class="text-lg sm:text-2xl font-bold text-gray-800">TCS</span>
          <span class="text-lg sm:text-2xl font-bold text-gray-800 tracking-widest">INFOSYS</span>
        </div>
      </div>
    </section>

    <!-- FOR STUDENTS -->
    <section id="students" class="py-16 sm:py-24 px-4 sm:px-6 lg:px-8 bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-10 sm:gap-16">
        <div class="flex-1 order-2 lg:order-1 relative w-full">
          <img src="https://images.unsplash.com/photo-1543269865-cbf427effbad?q=80&w=1000&auto=format&fit=crop" alt="Student matching" class="rounded-2xl sm:rounded-[2rem] shadow-xl object-cover h-[280px] sm:h-[400px] lg:h-[500px] w-full" />
          
          <div class="absolute top-4 right-4 sm:top-1/2 sm:-right-4 lg:-right-6 bg-white p-3.5 sm:p-5 rounded-xl sm:rounded-2xl shadow-xl border border-gray-100 max-w-[260px] sm:max-w-xs">
             <div class="flex items-center gap-2 text-indigo-600 font-bold text-xs sm:text-sm mb-1 sm:mb-2">
               <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
               Smart Match
             </div>
             <p class="text-gray-600 text-[11px] sm:text-xs font-medium leading-relaxed">Based on your 8.5 CGPA and CS branch, you have 14 new eligible jobs today.</p>
          </div>
        </div>
        
        <div class="flex-1 order-1 lg:order-2">
          <div class="text-indigo-600 font-bold tracking-widest uppercase text-xs sm:text-sm mb-2 sm:mb-4">For Candidates</div>
          <h2 class="text-2xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-4 sm:mb-6 leading-[1.2]">Your premium profile, presented to the best.</h2>
          <p class="text-base sm:text-lg text-gray-500 mb-6 sm:mb-10 leading-relaxed">
            Stop filling out endless forms. Create one powerful profile, and let our smart matching engine connect you with roles you are actually eligible for. No spam, no false hope.
          </p>
          
          <ul class="space-y-6 sm:space-y-8 mb-8 sm:mb-10">
            <li class="flex items-start gap-3 sm:gap-5">
               <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 shrink-0 mt-0.5 border border-indigo-100">
                 <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-lg sm:text-xl mb-1">Verified Eligibility</h4>
                 <p class="text-gray-500 text-sm sm:text-base leading-relaxed">See only the jobs where you meet the CGPA and branch criteria. Apply with a single click.</p>
               </div>
            </li>
            <li class="flex items-start gap-3 sm:gap-5">
               <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 shrink-0 mt-0.5 border border-indigo-100">
                 <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-lg sm:text-xl mb-1">Live In-Browser Interviews</h4>
                 <p class="text-gray-500 text-sm sm:text-base leading-relaxed">No Zoom links or software downloads. Join video interviews instantly from your dashboard when shortlisted.</p>
               </div>
            </li>
          </ul>
          
          <router-link to="/register?role=student" class="text-indigo-600 font-bold text-base sm:text-lg hover:text-indigo-800 inline-flex items-center gap-2 transition-colors">
            Create your profile <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- FOR COMPANIES -->
    <section id="companies" class="py-16 sm:py-24 px-4 sm:px-6 lg:px-8 bg-gray-50 border-t border-gray-100 overflow-hidden">
      <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-10 sm:gap-16">
        
        <div class="flex-1">
          <div class="text-emerald-600 font-bold tracking-widest uppercase text-xs sm:text-sm mb-2 sm:mb-4">For Employers</div>
          <h2 class="text-2xl sm:text-4xl lg:text-5xl font-extrabold text-gray-900 mb-4 sm:mb-6 leading-[1.2]">Hire top campus talent, 5x faster.</h2>
          <p class="text-base sm:text-lg text-gray-500 mb-6 sm:mb-10 leading-relaxed">
            CareerBridge gives you a complete Applicant Tracking System (ATS). Set your criteria, review curated profiles inline, and conduct interviews seamlessly.
          </p>
          
          <ul class="space-y-6 sm:space-y-8 mb-8 sm:mb-10">
            <li class="flex items-start gap-3 sm:gap-5">
               <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0 mt-0.5 border border-emerald-100">
                 <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-lg sm:text-xl mb-1">Strict Eligibility Filters</h4>
                 <p class="text-gray-500 text-sm sm:text-base leading-relaxed">Set hard cutoffs for CGPA and branch. The platform automatically filters out unqualified applicants.</p>
               </div>
            </li>
            <li class="flex items-start gap-3 sm:gap-5">
               <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0 mt-0.5 border border-emerald-100">
                 <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-lg sm:text-xl mb-1">Kanban Pipeline & Resumes</h4>
                 <p class="text-gray-500 text-sm sm:text-base leading-relaxed">Drag and drop candidates across stages. View resumes directly in your browser without downloading.</p>
               </div>
            </li>
          </ul>
          
          <router-link to="/register?role=company" class="text-emerald-600 font-bold text-base sm:text-lg hover:text-emerald-700 inline-flex items-center gap-2 transition-colors">
            Start hiring now <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>

        <div class="flex-1 relative w-full">
          <img src="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&w=1000&auto=format&fit=crop" alt="Employer hiring" class="rounded-2xl sm:rounded-[2rem] shadow-xl object-cover h-[280px] sm:h-[400px] lg:h-[500px] w-full" />
          
          <div class="absolute bottom-4 left-4 sm:bottom-10 sm:-left-4 lg:-left-6 bg-white p-3.5 sm:p-5 rounded-xl sm:rounded-2xl shadow-xl border border-gray-100 max-w-[260px] sm:max-w-xs">
             <div class="flex items-center gap-2.5 sm:gap-3">
                <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-gray-200 shrink-0">
                  <img src="https://i.pravatar.cc/100?img=33" class="rounded-full w-full h-full object-cover" />
                </div>
                <div>
                  <div class="text-gray-900 font-bold text-xs sm:text-sm">Priya Sharma</div>
                  <div class="text-emerald-600 text-[10px] sm:text-xs font-bold mt-0.5 uppercase tracking-wide">Shortlisted for Interview</div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIAL / CTA -->
    <section class="py-16 sm:py-24 px-4 sm:px-6 lg:px-8 bg-indigo-600 text-white text-center">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-2xl sm:text-4xl lg:text-5xl font-extrabold mb-4 sm:mb-8 leading-tight tracking-tight">Ready to bridge the gap?</h2>
        <p class="text-base sm:text-xl text-indigo-100 mb-8 sm:mb-12 max-w-2xl mx-auto leading-relaxed">
          Whether you are a student looking for the perfect launchpad, or a company seeking the brightest minds, CareerBridge is your platform.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center w-full sm:w-auto">
          <router-link to="/register?role=student" class="bg-white text-indigo-600 hover:bg-gray-50 font-bold text-base sm:text-lg px-8 py-3.5 sm:py-4 rounded-full transition-all shadow-lg text-center">
            I'm a Candidate
          </router-link>
          <router-link to="/register?role=company" class="bg-indigo-700 hover:bg-indigo-800 border border-indigo-500 text-white font-bold text-base sm:text-lg px-8 py-3.5 sm:py-4 rounded-full transition-all text-center shadow-lg">
            I'm an Employer
          </router-link>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-gray-900 text-gray-400 py-10 sm:py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6 text-center md:text-left">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" class="w-6 h-6 grayscale opacity-70" alt="CareerBridge" />
          <span class="font-bold text-white text-lg tracking-tight">CareerBridge</span>
        </div>
        <div class="text-xs sm:text-sm font-medium">
          &copy; {{ new Date().getFullYear() }} CareerBridge. MIT Licensed.
        </div>
        <div class="flex items-center gap-6 text-xs sm:text-sm font-semibold">
          <a href="https://github.com/MohdSayam/CareerBridge" target="_blank" class="hover:text-white transition-colors">GitHub</a>
          <router-link to="/login" class="hover:text-white transition-colors">Login</router-link>
          <router-link to="/register" class="hover:text-white transition-colors">Register</router-link>
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
      if (el) {
        const y = el.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top: y, behavior: 'smooth' });
      }
    }
  }
}
</script>