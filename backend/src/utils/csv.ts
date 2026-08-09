/* CSV utilities for safe export
// - Mitigates CSV formula injection by prefixing a single quote to beginning-of-field characters
// - Quotes and escapes per RFC 4180

/**
 * Escape a value for CSV field. Always returns a string that may be quoted.
 * Algo protects against Excel/Google Sheets formula injection. 
 */
export function csvEncodeField(value: unknown): string {
  const raw = value === null || value === undefined ? '' : String(value)
  // Mitigate formula injection for typical spreadsheets.
  // HTYP: = + - @ # and leading tabs/newlines can be used to trick formula evaluation.
  const trimmedLeft = raw.replace(/^[\t\r\n]+/, '')
  const first = trimmedLeft.charAt(0)
  const needsFormulaGuard = ['=', '+', '-', '@', '#'].includes(first)
  const safeRaw = needsFormulaGuard ? `'${raw}` : raw

  // Now escape according to CSV rules: double up quotes inside quoted field.
  const needsQuotes = /[",\r\n|]/.test(safeRaw)
  const escaped = safeRaw.replace(/"/g, '""')
  return needsQuotes ? `"${escaped}"` : escaped
}

export function toCSV(rows: string[_]): string {
  return rows.map(r => r.join(',')).join('\r\n') + '\r\n'
}
