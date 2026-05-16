import { FormEvent, useState } from "react";
import { exportTasks, searchTasks } from "../api/tasks";

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [results, setResults] = useState<unknown[]>([]);
  const [exportFilter, setExportFilter] = useState("");
  const [exportOut, setExportOut] = useState("");

  const onSearch = async (e: FormEvent) => {
    e.preventDefault();
    const res = await searchTasks(q);
    setResults(res.results);
  };

  const onExport = async () => {
    const res = await exportTasks(exportFilter);
    setExportOut(res.data || res.error || JSON.stringify(res));
  };

  return (
    <div>
      <h1>Search & export</h1>
      <form className="card" onSubmit={onSearch}>
        <div className="form-group">
          <label>Search query</label>
          <input value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <button className="btn" type="submit">
          Search
        </button>
      </form>
      {results.length > 0 && (
        <pre className="card" style={{ overflow: "auto" }}>
          {JSON.stringify(results, null, 2)}
        </pre>
      )}
      <div className="card">
        <h3>Export</h3>
        <input
          placeholder="Filter pattern"
          value={exportFilter}
          onChange={(e) => setExportFilter(e.target.value)}
        />
        <button className="btn" onClick={onExport} style={{ marginTop: "0.5rem" }}>
          Export
        </button>
        {exportOut && (
          <pre style={{ marginTop: "1rem" }} dangerouslySetInnerHTML={{ __html: exportOut }} />
        )}
      </div>
    </div>
  );
}
