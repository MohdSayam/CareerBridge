/**
 * Format an IST datetime string for display.
 * The backend stores all datetimes as IST-naive (no "Z", no "+05:30").
 * We parse the string manually to avoid JavaScript treating it as UTC.
 * 
 * Output: "18 Sep 2026, 06:15 PM"
 */
export function formatIST(dateStr) {
  if (!dateStr) return null

  // Parse the ISO string manually as IST by appending +05:30 if no timezone info
  let normalized = dateStr
  const hasTimezone = dateStr.endsWith('Z') || dateStr.includes('+') || (dateStr.length > 19 && dateStr[19] === '-')
  if (!hasTimezone) {
    // No timezone info → backend sent IST naive → add IST offset explicitly
    normalized = dateStr + '+05:30'
  }

  const date = new Date(normalized)
  if (isNaN(date.getTime())) return dateStr

  return date.toLocaleString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZone: 'Asia/Kolkata'
  })
}

/**
 * Format date-only in Indian format.
 * Output: "18 Sep 2026"
 */
export function formatISTDate(dateStr) {
  if (!dateStr) return null

  let normalized = dateStr
  const hasTimezone = dateStr.endsWith('Z') || dateStr.includes('+') || (dateStr.length > 19 && dateStr[19] === '-')
  if (!hasTimezone) {
    normalized = dateStr + '+05:30'
  }

  const date = new Date(normalized)
  if (isNaN(date.getTime())) return dateStr

  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    timeZone: 'Asia/Kolkata'
  })
}
