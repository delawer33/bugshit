import { useCallback, useEffect, useState } from "react";
import * as tasksApi from "../api/tasks";
import type { Task } from "../types";

export function useTasks(statusFilter?: string) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await tasksApi.fetchTasks(statusFilter);
      setTasks(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    load();
  }, [load]);

  const create = async (payload: Partial<Task>) => {
    const created = await tasksApi.createTask(payload);
    setTasks((prev) => [created, ...prev]);
    return created;
  };

  const update = async (id: number, payload: Partial<Task>) => {
    const updated = await tasksApi.updateTask(id, payload);
    setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
    return updated;
  };

  const remove = async (id: number) => {
    await tasksApi.deleteTask(id);
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  return { tasks, loading, error, reload: load, create, update, remove };
}
