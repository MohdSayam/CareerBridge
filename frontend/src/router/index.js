import { createRouter, createWebHistory } from "vue-router"
import PublicLayout from "../layouts/PublicLayout.vue"
import Home from "../views/public_views/Home.vue"
import Login from "../views/public_views/Login.vue";
import Register from "../views/public_views/Register.vue";
import AdminLayout from "../layouts/AdminLayout.vue";
import CompanyLayout from "../layouts/CompanyLayout.vue";
import StudentLayout from "../layouts/StudentLayout.vue";
import AdminDashboard from "../views/admin_views/AdminDashboard.vue"

import AdminPlacements from "../views/admin_views/AdminPlacements.vue";
import Students from "../views/admin_views/Students.vue";
import Companies from "../views/admin_views/Companies.vue";
import Jobs from "../views/admin_views/Jobs.vue";
import Applications from "../views/admin_views/Applications.vue";
import AdminInterviews from "../views/admin_views/AdminInterviews.vue";
import PendingApproval from "../views/company_views/PendingApproval.vue";
import CompanyDashboard from "../views/company_views/CompanyDashboard.vue";
import CompanyJobs from "../views/company_views/CompanyJobs.vue";
import CompanyProfile from "../views/company_views/CompanyProfile.vue";
import CompanyApplicants from "../views/company_views/CompanyApplicants.vue";
import CompanyApplicantDetails from "../views/company_views/CompanyApplicantDetails.vue";
import CompanyInterviews from "../views/company_views/CompanyInterviews.vue";
import StudentDashboard from "../views/student_views/StudentDashboard.vue"
import StudentJobs from "../views/student_views/StudentJobs.vue"
import StudentJobDetails from "../views/student_views/StudentJobDetails.vue"
import StudentApplications from "../views/student_views/StudentApplications.vue"
import StudentPlacements from "../views/student_views/StudentPlacements.vue"
import StudentProfile from "../views/student_views/StudentProfile.vue"
import StudentOnboarding from "../views/student_views/StudentOnboarding.vue"
import InterviewRoom from "../views/InterviewRoom.vue"


const routes = [
    {
        path: "/",
        component: PublicLayout,

        children: [
            {
                path: "",
                name: "Home",
                component: Home
            }
        ]
    },

    {
        path: '/login',
        name: 'Login',
        component: Login
    },

    {
        path: '/register',
        name: 'Register',
        component: Register
    },

    {
        path: "/admin",
        component: AdminLayout,
        meta: {
            requiresAuth: true,
            role: "admin"
        },

        children: [
            {
                path: "",
                component: AdminDashboard
            },
            {
                path: "students",
                component: Students
            },
            {
                path: "companies",
                component: Companies
            },
            {
                path: "jobs",
                component: Jobs
            },
            {
                path: "applications",
                component: Applications
            },
            {
                path: "placements",
                component: AdminPlacements
            },
            {
                path: "interviews",
                component: AdminInterviews
            }
        ]
    },

    {
        path: "/company",
        component: CompanyLayout,
        meta: {
            requiresAuth: true,
            role: "company"
        },

        children: [
            {
                path: "",
                component: CompanyDashboard
            },

            {
                path: "pending",
                component: PendingApproval
            },

            {
                path: "jobs",
                component: CompanyJobs
            },

            {
                path: "profile",
                component: CompanyProfile
            },

            {
                path: "applicants",
                component: CompanyApplicants
            },
            {
                path: "applicant/:id",
                component: CompanyApplicantDetails
            },

            {
                path: "interviews",
                component: CompanyInterviews
            },

            {
                path: "interview/:id",
                component: InterviewRoom
            }
        ]
    },

    {
        path: "/student",
        component: StudentLayout,
        meta: {
            requiresAuth: true,
            role: "student"
        },

        children: [
            {
                path: "",
                component: StudentDashboard
            },

            {
                path: "applications",
                component: StudentApplications
            },

            {
                path: "jobs",
                component: StudentJobs
            },
            {
                path: "job/:id",
                component: StudentJobDetails
            },

            {
                path: "placements",
                component: StudentPlacements
            },

            {
                path: "profile",
                component: StudentProfile
            },
            {
                path: "onboarding",
                component: StudentOnboarding
            },

            {
                path: "interview/:id",
                component: InterviewRoom
            }
        ]
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("access_token")
    const role = localStorage.getItem("role")

    if (to.meta.requiresAuth && !token) {
        return next("/login")
    }

    if (to.meta.role && role !== to.meta.role) {
        return next("/login")
    }

    // Enforce profile completion for students
    if (role === "student" && to.path.startsWith("/student") && to.path !== "/student/onboarding") {
        const profileComplete = localStorage.getItem("profile_complete")
        if (profileComplete === "false") {
            return next("/student/onboarding")
        }
    }

    next()
})

export default router;