import { FormEvent, useEffect, useState } from "react";
import { createProject, fetchProjects } from "../api/projects";
import type { Project } from "../types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const load = () => fetchProjects().then(setProjects);

  useEffect(() => {
    load();
  }, []);

  const onCreate = async (e: FormEvent) => {
    e.preventDefault();
    await createProject(name, description);
    setName("");
    setDescription("");
    load();
  };

  return (
    <div>
      <h1>Projects</h1>
      <form className="card" onSubmit={onCreate}>
        <div className="form-group">
          <label>Name</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>
        <button className="btn" type="submit">
          Create project
        </button>
      </form>
      <div className="card">
        {projects.map((p) => (
          <div key={p.id} className="task-row">
            <div>
              <strong>{p.name}</strong>
              <div style={{ color: "var(--muted)" }}>{p.description}</div>
            </div>
            {p.is_public && <span className="badge">Public</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
