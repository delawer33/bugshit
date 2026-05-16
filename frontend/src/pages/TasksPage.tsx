import { useState } from "react";
import { useNavigate } from "react-router-dom";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import { useTasks } from "../hooks/useTasks";
import type { Task } from "../types";

export default function TasksPage() {
  const navigate = useNavigate();
  const [filter, setFilter] = useState<string>("");
  const { tasks, loading, error, create, update, remove } = useTasks(
    filter || undefined
  );

  const handleCreate = async (data: {
    title: string;
    description: string;
    status: string;
    priority: number;
  }) => {
    await create(data as Partial<Task>);
  };

  return (
    <div>
      <h1>Tasks</h1>
      <div style={{ marginBottom: "1rem" }}>
        <label>Filter by status </label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="">All</option>
          <option value="todo">Todo</option>
          <option value="in_progress">In progress</option>
          <option value="done">Done</option>
        </select>
      </div>
      {error && <p className="error-text">{error}</p>}
      <TaskForm onSubmit={handleCreate} />
      <div className="card">
        <h3>Your tasks</h3>
        {loading ? (
          <p>Loading…</p>
        ) : (
          <TaskList
            tasks={tasks}
            onSelect={(t) => navigate(`/tasks/${t.id}`)}
            onDelete={remove}
            onStatusChange={(id, status) => update(id, { status })}
          />
        )}
      </div>
    </div>
  );
}
