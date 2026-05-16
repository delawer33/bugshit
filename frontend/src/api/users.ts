import { api } from "./client";
import type { User } from "../types";

export async function fetchMe(): Promise<User> {
  return api.get<User>("/users/me");
}

export async function fetchUser(id: number): Promise<User> {
  return api.get<User>(`/users/${id}`);
}

export async function updateMe(payload: Partial<User>): Promise<User> {
  return api.patch<User>("/users/me", payload);
}

export async function listUsers(): Promise<User[]> {
  return api.get<User[]>("/users/");
}
