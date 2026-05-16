import { FormEvent, useState } from "react";

interface Props {
  onSubmit: (data: {
    title: string;
    description: string;
    status: string;
    priority: number;
  }) => Promise<void>;
}

export default function TaskForm({ onSubmit }: Props) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("todo");
  const [priority, setPriority] = useState(1);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await onSubmit({ title, description, status, priority });
      setTitle("");
      setDescription("");
      setStatus("todo");
      setPriority(1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h3>New task</h3>
      {error && <p className="error-text">{error}</p>}
      <div className="form-group">
        <label>Title</label>
        <input value={title} onChange={(e) => setTitle(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>Description</label>
        <textarea
          rows={3}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <div className="grid-2">
        <div className="form-group">
          <label>Status</label>
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="todo">To do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
            <option value="blocked">Blocked</option>
          </select>
        </div>
        <div className="form-group">
          <label>Priority</label>
          <input
            type="number"
            min={1}
            max={5}
            value={priority}
            onChange={(e) => setPriority(Number(e.target.value))}
          />
        </div>
      </div>
      <button className="btn" type="submit" disabled={busy}>
        {busy ? "Saving…" : "Create task"}
      </button>
    </form>
  );
}
