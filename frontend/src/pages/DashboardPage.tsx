import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTasks } from "../hooks/useTasks";
import TaskList from "../components/TaskList";

export default function DashboardPage() {
  const { user } = useAuth();
  const { tasks, loading, update } = useTasks();
  const [stats, setStats] = useState({ todo: 0, done: 0, total: 0 });

  useEffect(() => {
    const todo = tasks.filter((t) => t.status === "todo").length;
    const done = tasks.filter((t) => t.status === "done").length;
    setStats({ todo, done, total: tasks.length });
  }, [tasks]);

  return (
    <div>
      <h1>Welcome, {user?.display_name}</h1>
      <p style={{ color: "var(--muted)" }}>
        Wallet: ${user?.wallet_balance?.toFixed(2) ?? "0.00"}
      </p>
      <div className="grid-2" style={{ marginBottom: "1.5rem" }}>
        <div className="card">
          <h3>Open tasks</h3>
          <p style={{ fontSize: "2rem", margin: 0 }}>{stats.todo}</p>
        </div>
        <div className="card">
          <h3>Completed</h3>
          <p style={{ fontSize: "2rem", margin: 0 }}>{stats.done}</p>
        </div>
      </div>
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <h3>Recent tasks</h3>
          <Link to="/tasks">View all</Link>
        </div>
        {loading ? (
          <p>Loading…</p>
        ) : (
          <TaskList
            tasks={tasks.slice(0, 5)}
            onStatusChange={(id, status) => update(id, { status })}
          />
        )}
      </div>
    </div>
  );
}
