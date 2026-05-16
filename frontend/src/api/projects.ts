import { api } from "./client";
import type { Project } from "../types";

export async function fetchProjects(): Promise<Project[]> {
  return api.get<Project[]>("/projects/");
}

export async function createProject(
  name: string,
  description: string
): Promise<Project> {
  return api.post<Project>("/projects/", { name, description });
}
