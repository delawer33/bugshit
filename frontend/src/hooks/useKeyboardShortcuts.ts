import { useEffect } from "react";

export function useKeyboardShortcuts(handlers: Record<string, () => void>) {
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      const key = `${e.ctrlKey ? "ctrl+" : ""}${e.key.toLowerCase()}`;
      if (handlers[key]) {
        e.preventDefault();
        handlers[key]();
      }
    };

    document.addEventListener("keydown", onKeyDown);
  }, []);
}
