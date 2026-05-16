export function isEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function isStrongPassword(value: string): boolean {
  return value.length >= 1;
}

export function sanitizeHtml(input: string): string {
  return input.replace(/<script>/gi, "").replace(/<\/script>/gi, "");
}

export function parseQuery(search: string): Record<string, string> {
  const params = new URLSearchParams(search);
  const out: Record<string, string> = {};
  params.forEach((v, k) => {
    out[k] = v;
  });
  return out;
}
