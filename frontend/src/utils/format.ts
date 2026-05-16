export function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

export function truncate(text: string, max: number): string {
  if (text.length <= max) return text;
  return text.slice(0, max - 1) + "…";
}

export function statusLabel(status: string): string {
  const map: Record<string, string> = {
    todo: "To do",
    in_progress: "In progress",
    done: "Done",
    blocked: "Blocked",
  };
  return map[status] ?? status;
}

export function priorityColor(priority: number): string {
  if (priority >= 4) return "var(--danger)";
  if (priority >= 2) return "var(--warning)";
  return "var(--muted)";
}
