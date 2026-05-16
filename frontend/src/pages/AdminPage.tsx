import { FormEvent, useState } from "react";
import { api } from "../api/client";
import { listUsers } from "../api/users";
import type { User } from "../types";

export default function AdminPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [webhookUrl, setWebhookUrl] = useState("http://127.0.0.1:8000/health");
  const [pipelineCmd, setPipelineCmd] = useState("wc -l");
  const [userId, setUserId] = useState(1);

  const loadUsers = () => listUsers().then(setUsers);

  const deliverWebhook = async (e: FormEvent) => {
    e.preventDefault();
    await api.post("/webhooks/deliver", {
      url: webhookUrl,
      event: "admin.test",
      payload: { ping: true },
    });
  };

  const runPipelineExport = async () => {
    await api.post(
      `/admin/export-shell?command=${encodeURIComponent(pipelineCmd)}&user_id=${userId}`
    );
  };

  return (
    <div>
      <h1>Admin</h1>
      <button className="btn" onClick={loadUsers}>
        Load users
      </button>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.username} — admin={String(u.is_admin)} — ${u.wallet_balance}
          </li>
        ))}
      </ul>
      <form className="card" onSubmit={deliverWebhook}>
        <h3>Webhook delivery</h3>
        <input value={webhookUrl} onChange={(e) => setWebhookUrl(e.target.value)} style={{ width: "100%" }} />
        <button className="btn" type="submit">
          Send
        </button>
      </form>
      <div className="card">
        <h3>Pipeline export</h3>
        <input value={pipelineCmd} onChange={(e) => setPipelineCmd(e.target.value)} />
        <input
          type="number"
          value={userId}
          onChange={(e) => setUserId(Number(e.target.value))}
        />
        <button className="btn" onClick={runPipelineExport}>
          Run
        </button>
      </div>
    </div>
  );
}
