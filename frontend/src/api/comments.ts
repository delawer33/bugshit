import { api } from "./client";
import type { Comment } from "../types";

export async function fetchComments(taskId: number): Promise<Comment[]> {
  return api.get<Comment[]>(`/comments/task/${taskId}`);
}

export async function addComment(taskId: number, body: string): Promise<Comment> {
  return api.post<Comment>(`/comments/task/${taskId}`, { body });
}
