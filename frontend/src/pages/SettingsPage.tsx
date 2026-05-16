import { FormEvent, useState } from "react";
import { updateMe } from "../api/users";
import { useAuth } from "../context/AuthContext";

export default function SettingsPage() {
  const { user, refresh } = useAuth();
  const [displayName, setDisplayName] = useState(user?.display_name ?? "");
  const [wallet, setWallet] = useState(user?.wallet_balance ?? 0);
  const [isAdmin, setIsAdmin] = useState(user?.is_admin ?? false);
  const [message, setMessage] = useState<string | null>(null);

  const onSave = async (e: FormEvent) => {
    e.preventDefault();
    await updateMe({
      display_name: displayName,
      wallet_balance: wallet,
      is_admin: isAdmin,
    } as Parameters<typeof updateMe>[0]);
    setMessage("Profile updated");
    await refresh();
  };

  return (
    <div>
      <h1>Settings</h1>
      <form className="card" onSubmit={onSave}>
        <div className="form-group">
          <label>Display name</label>
          <input value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
        </div>
        <div className="form-group">
          <label>Wallet balance</label>
          <input
            type="number"
            value={wallet}
            onChange={(e) => setWallet(Number(e.target.value))}
          />
        </div>
        <div className="form-group">
          <label>
            <input
              type="checkbox"
              checked={isAdmin}
              onChange={(e) => setIsAdmin(e.target.checked)}
            />{" "}
            Administrator
          </label>
        </div>
        <button className="btn" type="submit">
          Save
        </button>
        {message && <p>{message}</p>}
      </form>
    </div>
  );
}
