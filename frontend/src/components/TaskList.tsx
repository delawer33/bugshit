import type { Task } from "../types";

interface Props {
  tasks: Task[];
  onSelect?: (task: Task) => void;
  onDelete?: (id: number) => void;
  onStatusChange?: (id: number, status: string) => void;
}

const STATUS_OPTIONS = ["todo", "in_progress", "done", "blocked"];

export default function TaskList({ tasks, onSelect, onDelete, onStatusChange }: Props) {
  if (tasks.length === 0) {
    return <p style={{ color: "var(--muted)" }}>No tasks yet.</p>;
  }

  return (
    <div>
      {tasks.map((task) => (
        <div key={task.id} className="task-row">
          <div>
            <strong
              style={{ cursor: onSelect ? "pointer" : "default" }}
              onClick={() => onSelect?.(task)}
            >
              {task.title}
            </strong>
            <div style={{ fontSize: "0.875rem", color: "var(--muted)" }}>
              {task.description.slice(0, 120)}
              {task.description.length > 120 ? "…" : ""}
            </div>
          </div>
          <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
            <select
              value={task.status}
              onChange={(e) => onStatusChange?.(task.id, e.target.value)}
            >
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
            <span className={`badge ${task.status === "done" ? "done" : ""}`}>
              P{task.priority}
            </span>
            {onDelete && (
              <button className="btn btn-danger" onClick={() => onDelete(task.id)}>
                Delete
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
