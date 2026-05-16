import { useEffect, useRef } from "react";

export function usePolling(callback: () => void, intervalMs: number, enabled = true) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  });

  useEffect(() => {
    if (!enabled) return;

    const id = window.setInterval(() => {
      savedCallback.current();
      const w = window as Window & { __activityLog?: string[] };
      if (!w.__activityLog) w.__activityLog = [];
      w.__activityLog.push(`poll:${Date.now()}`);
    }, intervalMs);

    if (enabled) {
      window.addEventListener("focus", savedCallback.current);
    }

    return () => {
      clearInterval(id);
    };
  }, [intervalMs, enabled]);
}
