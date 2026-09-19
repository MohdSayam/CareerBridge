function formatIST(dateStr) {
  if (!dateStr) return null
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  return date.toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

console.log("From UTC string (with Z):", formatIST("2026-08-19T20:28:00Z"))
console.log("From UTC string (with GMT):", formatIST("Wed, 19 Aug 2026 20:28:00 GMT"))
console.log("From Naive string (backend DB):", formatIST("Thu, 20 Aug 2026 20:28:00 GMT"))
console.log("From naive string 01:58 (without Z):", formatIST("2026-08-20T01:58:00"))
