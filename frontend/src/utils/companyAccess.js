export function handleCompanyAccess(vm, message){

    const blockedMessages = [
        "Company profile is waiting for admin approval",
        "Your company has been blacklisted.",
        "Your account is inactive."
    ]

    if(blockedMessages.includes(message)){
        vm.$router.push({
            path: "/company/pending",
            query: {
                message: message
            }
        })

        return true
    }

    return false
}