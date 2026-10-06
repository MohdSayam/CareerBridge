<template>
  <div class="bg-white text-gray-900 font-sans antialiased overflow-x-hidden">
    
    <!-- NAVBAR -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white transition-all duration-300"
         :class="{'shadow-sm border-b border-gray-100 py-3': scrolled, 'py-5': !scrolled}">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" alt="CareerBridge" class="w-8 h-8" />
          <span class="font-extrabold text-2xl tracking-tight text-gray-900">CareerBridge</span>
        </div>
        
        <div class="hidden md:flex items-center gap-8 text-sm font-semibold text-gray-600">
          <a href="#students" @click.prevent="scrollTo('students')" class="hover:text-indigo-600 transition-colors">For Candidates</a>
          <a href="#companies" @click.prevent="scrollTo('companies')" class="hover:text-indigo-600 transition-colors">For Employers</a>
        </div>
        
        <div class="flex items-center gap-4">
          <router-link to="/login" class="hidden md:block text-gray-600 font-semibold text-sm hover:text-indigo-600 transition">Login</router-link>
          <router-link to="/register" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold px-6 py-3 rounded-full transition-all shadow-md hover:shadow-lg">
            Sign Up Free
          </router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="relative pt-24 pb-16 lg:pt-32 lg:pb-24 px-6 lg:px-8 overflow-hidden min-h-[90vh] flex items-center">
      <!-- Subtle background pattern -->
      <div class="absolute inset-0 z-0 opacity-[0.15]" style="background-image: radial-gradient(#9ca3af 1px, transparent 1px); background-size: 24px 24px;"></div>
      
      <div class="max-w-7xl mx-auto w-full relative z-10 flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
        <div class="flex-1 text-center lg:text-left">
          <div class="inline-block bg-indigo-50 text-indigo-700 font-bold px-4 py-1.5 rounded-full text-sm mb-6 border border-indigo-100">
            India's Premium Campus Hiring Platform
          </div>
          <h1 class="text-5xl lg:text-7xl font-extrabold tracking-tight text-gray-900 leading-[1.1] mb-6">
            Find your dream job.<br />
            <span class="text-indigo-600">Without the hassle.</span>
          </h1>
          <p class="text-lg lg:text-xl text-gray-500 max-w-2xl mx-auto lg:mx-0 mb-10 leading-relaxed">
            CareerBridge connects premium campus talent with top-tier companies. Verified profiles, automated eligibility checks, and live video interviews — all in one platform.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <router-link to="/register?role=student" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg px-8 py-4 rounded-full transition-all shadow-lg hover:shadow-xl text-center flex items-center justify-center gap-2">
              Apply as Candidate <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </router-link>
            <router-link to="/register?role=company" class="bg-white border-2 border-gray-200 hover:border-gray-300 text-gray-800 font-bold text-lg px-8 py-4 rounded-full transition-all text-center">
              Hire Top Talent
            </router-link>
          </div>
          <div class="mt-8 text-sm text-gray-500 font-medium">
            Join 10,000+ students and 500+ top companies
          </div>
        </div>
        
        <div class="flex-1 w-full max-w-lg lg:max-w-none relative">
          <!-- Abstract blob behind image -->
          <div class="absolute inset-0 bg-indigo-100 rounded-full blur-3xl opacity-60 transform translate-x-10 translate-y-10"></div>
          
          <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=1000&auto=format&fit=crop" alt="Students collaborating" class="relative rounded-[2rem] shadow-2xl border border-gray-100 object-cover w-full h-[400px] lg:h-[520px]" />
          
          <!-- Floating UI Card - Offer -->
          <div class="absolute -bottom-6 -left-6 bg-white p-5 rounded-2xl shadow-xl border border-gray-100 flex items-center gap-4 hidden sm:flex">
            <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl">🎉</div>
            <div>
              <div class="font-bold text-gray-900 text-sm">Offer Accepted!</div>
              <div class="text-xs text-gray-500 font-medium">Software Engineer at TechCorp</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- LOGOS -->
    <section class="py-12 border-y border-gray-100 bg-gray-50">
      <div class="max-w-7xl mx-auto px-6 lg:px-8 text-center">
        <p class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-8">Trusted by companies hiring on campus</p>
        <div class="flex flex-wrap justify-center items-center gap-10 md:gap-20 opacity-50 grayscale hover:grayscale-0 transition-all duration-500">
          <!-- Text-based logos for clean look -->
          <span class="text-2xl font-bold text-gray-800 font-serif">Google</span>
          <span class="text-2xl font-black text-gray-800 tracking-tighter">Microsoft</span>
          <span class="text-2xl font-bold text-gray-800">Amazon</span>
          <span class="text-2xl font-extrabold text-gray-800 italic">Swiggy</span>
          <span class="text-2xl font-bold text-gray-800">TCS</span>
          <span class="text-2xl font-bold text-gray-800 tracking-widest">INFOSYS</span>
        </div>
      </div>
    </section>

    <!-- FOR STUDENTS -->
    <section id="students" class="py-24 px-6 lg:px-8 bg-white">
      <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16">
        <div class="flex-1 order-2 lg:order-1 relative">
          <img src="https://images.unsplash.com/photo-1543269865-cbf427effbad?q=80&w=1000&auto=format&fit=crop" alt="Student matching" class="rounded-[2rem] shadow-xl object-cover h-[500px] w-full" />
          
          <div class="absolute top-1/2 -right-8 bg-white p-5 rounded-2xl shadow-xl border border-gray-100 max-w-xs hidden sm:block">
             <div class="flex items-center gap-2 text-indigo-600 font-bold text-sm mb-2">
               <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
               Smart Match
             </div>
             <p class="text-gray-600 text-xs font-medium leading-relaxed">Based on your 8.5 CGPA and CS branch, you have 14 new eligible jobs today.</p>
          </div>
        </div>
        
        <div class="flex-1 order-1 lg:order-2">
          <div class="text-indigo-600 font-bold tracking-widest uppercase text-sm mb-4">For Candidates</div>
          <h2 class="text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-[1.15]">Your premium profile, presented to the best.</h2>
          <p class="text-lg text-gray-500 mb-10 leading-relaxed">
            Stop filling out endless forms. Create one powerful profile, and let our smart matching engine connect you with roles you are actually eligible for. No spam, no false hope.
          </p>
          
          <ul class="space-y-8 mb-10">
            <li class="flex items-start gap-5">
               <div class="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 shrink-0 mt-1 border border-indigo-100">
                 <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-xl mb-1">Verified Eligibility</h4>
                 <p class="text-gray-500 text-base leading-relaxed">See only the jobs where you meet the CGPA and branch criteria. Apply with a single click.</p>
               </div>
            </li>
            <li class="flex items-start gap-5">
               <div class="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 shrink-0 mt-1 border border-indigo-100">
                 <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-xl mb-1">Live In-Browser Interviews</h4>
                 <p class="text-gray-500 text-base leading-relaxed">No Zoom links or software downloads. Join video interviews instantly from your dashboard when shortlisted.</p>
               </div>
            </li>
          </ul>
          
          <router-link to="/register?role=student" class="text-indigo-600 font-bold text-lg hover:text-indigo-800 flex items-center gap-2 transition-colors">
            Create your profile <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- FOR COMPANIES -->
    <section id="companies" class="py-24 px-6 lg:px-8 bg-gray-50 border-t border-gray-100">
      <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center gap-16">
        
        <div class="flex-1">
          <div class="text-emerald-600 font-bold tracking-widest uppercase text-sm mb-4">For Employers</div>
          <h2 class="text-4xl lg:text-5xl font-extrabold text-gray-900 mb-6 leading-[1.15]">Hire top campus talent, 5x faster.</h2>
          <p class="text-lg text-gray-500 mb-10 leading-relaxed">
            CareerBridge gives you a complete Applicant Tracking System (ATS). Set your criteria, review curated profiles inline, and conduct interviews seamlessly.
          </p>
          
          <ul class="space-y-8 mb-10">
            <li class="flex items-start gap-5">
               <div class="w-12 h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0 mt-1 border border-emerald-100">
                 <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-xl mb-1">Strict Eligibility Filters</h4>
                 <p class="text-gray-500 text-base leading-relaxed">Set hard cutoffs for CGPA and branch. The platform automatically filters out unqualified applicants.</p>
               </div>
            </li>
            <li class="flex items-start gap-5">
               <div class="w-12 h-12 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600 shrink-0 mt-1 border border-emerald-100">
                 <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path></svg>
               </div>
               <div>
                 <h4 class="font-bold text-gray-900 text-xl mb-1">Kanban Pipeline & Resumes</h4>
                 <p class="text-gray-500 text-base leading-relaxed">Drag and drop candidates across stages. View resumes directly in your browser without downloading.</p>
               </div>
            </li>
          </ul>
          
          <router-link to="/register?role=company" class="text-emerald-600 font-bold text-lg hover:text-emerald-700 flex items-center gap-2 transition-colors">
            Start hiring now <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </router-link>
        </div>

        <div class="flex-1 relative">
          <img src="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&w=1000&auto=format&fit=crop" alt="Employer hiring" class="rounded-[2rem] shadow-xl object-cover h-[500px] w-full" />
          
          <div class="absolute bottom-10 -left-8 bg-white p-5 rounded-2xl shadow-xl border border-gray-100 max-w-xs hidden sm:block">
             <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gray-200">
                  <img src="https://i.pravatar.cc/100?img=33" class="rounded-full" />
                </div>
                <div>
                  <div class="text-gray-900 font-bold text-sm">Priya Sharma</div>
                  <div class="text-emerald-600 text-xs font-bold mt-0.5 uppercase tracking-wide">Shortlisted for Interview</div>
                </div>
             </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIAL / CTA -->
    <section class="py-24 px-6 lg:px-8 bg-indigo-600 text-white text-center">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-4xl lg:text-5xl font-extrabold mb-8 leading-tight tracking-tight">Ready to bridge the gap?</h2>
        <p class="text-xl text-indigo-100 mb-12 max-w-2xl mx-auto leading-relaxed">
          Whether you are a student looking for the perfect launchpad, or a company seeking the brightest minds, CareerBridge is your platform.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link to="/register?role=student" class="bg-white text-indigo-600 hover:bg-gray-50 font-bold text-lg px-8 py-4 rounded-full transition-all shadow-lg text-center">
            I'm a Candidate
          </router-link>
          <router-link to="/register?role=company" class="bg-indigo-700 hover:bg-indigo-800 border border-indigo-500 text-white font-bold text-lg px-8 py-4 rounded-full transition-all text-center shadow-lg">
            I'm an Employer
          </router-link>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-gray-900 text-gray-400 py-12 px-6 lg:px-8">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-3">
          <img src="/favicon.svg" class="w-6 h-6 grayscale opacity-70" alt="CareerBridge" />
          <span class="font-bold text-white text-lg tracking-tight">CareerBridge</span>
        </div>
        <div class="text-sm font-medium">
          &copy; {{ new Date().getFullYear() }} CareerBridge. MIT Licensed.
        </div>
        <div class="flex items-center gap-6 text-sm font-semibold">
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