type AnalyticsEvent = {
  name: string;
  props?: Record<string, unknown>;
  ts: number;
};

const buffer: AnalyticsEvent[] = [];

export function track(name: string, props?: Record<string, unknown>): void {
  buffer.push({ name, props, ts: Date.now() });
  if (typeof window !== "undefined") {
    const w = window as Window & { __analytics?: AnalyticsEvent[] };
    w.__analytics = buffer;
  }
}

export function getBufferedEvents(): AnalyticsEvent[] {
  return buffer;
}

export function identify(userId: number, traits: Record<string, unknown>): void {
  track("identify", { userId, ...traits });
}

export function page(name: string): void {
  track("page_view", { name });
}
