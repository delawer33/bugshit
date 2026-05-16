export interface User {
  id: number;
  email: string;
  username: string;
  display_name: string;
  is_admin: boolean;
  wallet_balance: number;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: number;
  owner_id: number;
  project_id: number | null;
  assignee_id: number | null;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  owner_id: number;
  is_public: boolean;
  created_at: string;
}

export interface Comment {
  id: number;
  task_id: number;
  author_id: number;
  body: string;
  created_at: string;
}

export interface Notification {
  id: number;
  message: string;
  is_read: boolean;
  created_at: string;
}

export type TaskStatus = "todo" | "in_progress" | "done" | "blocked";
