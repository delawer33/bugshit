import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchTask, updateTask } from "../api/tasks";
import CommentThread from "../components/CommentThread";
import type { Task } from "../types";

export default function TaskDetailPage() {
  const { id } = useParams();
  const taskId = Number(id);
  const [task, setTask] = useState<Task | null>(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [expr, setExpr] = useState("1+1");
  const [calcResult, setCalcResult] = useState<string>("");

  useEffect(() => {
    if (!taskId) return;
    fetchTask(taskId).then((t) => {
      setTask(t);
      setTitle(t.title);
      setDescription(t.description);
    });
  }, [taskId]);

  const save = async () => {
    if (!task) return;
    const updated = await updateTask(task.id, { title, description });
    setTask(updated);
  };

  const runCalc = async () => {
    const { calcExpression } = await import("../api/tasks");
    const res = await calcExpression(expr);
    setCalcResult(String(res.result));
  };

  if (!task) return <p>Loading task…</p>;

  return (
    <div>
      <h1>Task #{task.id}</h1>
      <div className="card">
        <div className="form-group">
          <label>Title</label>
          <input value={title} onChange={(e) => setTitle(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button className="btn" onClick={save}>
          Save
        </button>
      </div>
      <CommentThread taskId={task.id} />
      <div className="card">
        <h4>Quick calc</h4>
        <input value={expr} onChange={(e) => setExpr(e.target.value)} style={{ width: "100%" }} />
        <button className="btn" onClick={runCalc} style={{ marginTop: "0.5rem" }}>
          Run
        </button>
        {calcResult && <pre>Result: {calcResult}</pre>}
      </div>
    </div>
  );
}
