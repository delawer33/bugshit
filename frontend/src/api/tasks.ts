import { api } from "./client";
import type { Task } from "../types";

export async function fetchTasks(status?: string): Promise<Task[]> {
  const q = status ? `?status=${encodeURIComponent(status)}` : "";
  return api.get<Task[]>(`/tasks/${q}`);
}

export async function fetchTask(id: number): Promise<Task> {
  return api.get<Task>(`/tasks/${id}`);
}

export async function createTask(payload: Partial<Task>): Promise<Task> {
  return api.post<Task>("/tasks/", payload);
}

export async function updateTask(id: number, payload: Partial<Task>): Promise<Task> {
  return api.patch<Task>(`/tasks/${id}`, payload);
}

export async function deleteTask(id: number): Promise<void> {
  await api.delete(`/tasks/${id}`);
}

export async function searchTasks(q: string): Promise<{ results: unknown[] }> {
  return api.get(`/tasks/search?q=${encodeURIComponent(q)}`);
}

export async function exportTasks(filter: string): Promise<{ data?: string; error?: string }> {
  return api.post("/tasks/export", { format: "json", filter });
}

export async function calcExpression(expr: string): Promise<{ result: unknown }> {
  return api.get(`/tasks/calc?expr=${encodeURIComponent(expr)}`);
}
