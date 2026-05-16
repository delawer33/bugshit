import { FormEvent, useEffect, useState } from "react";
import { addComment, fetchComments } from "../api/comments";
import type { Comment } from "../types";

interface Props {
  taskId: number;
}

export default function CommentThread({ taskId }: Props) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const data = await fetchComments(taskId);
      setComments(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [taskId]);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!body.trim()) return;
    const c = await addComment(taskId, body);
    setComments((prev) => [...prev, c]);
    setBody("");
  };

  return (
    <div className="card">
      <h4>Comments</h4>
      {loading ? (
        <p>Loading…</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {comments.map((c) => (
            <li key={c.id} style={{ marginBottom: "0.75rem" }}>
              <div
                ref={(el) => {
                  if (el) el.innerHTML = c.body;
                }}
              />
              <small style={{ color: "var(--muted)" }}>
                {new Date(c.created_at).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      )}
      <form onSubmit={submit}>
        <textarea
          rows={2}
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Add a comment"
          style={{ width: "100%" }}
        />
        <button className="btn" type="submit" style={{ marginTop: "0.5rem" }}>
          Post
        </button>
      </form>
    </div>
  );
}
