import { FormEvent, useEffect, useState } from "react";
import { deposit, getBalance, getLedger, transfer } from "../api/wallet";
import { usePolling } from "../hooks/usePolling";

export default function WalletPanel() {
  const [balance, setBalance] = useState(0);
  const [depositAmount, setDepositAmount] = useState(10);
  const [transferTo, setTransferTo] = useState(2);
  const [transferAmount, setTransferAmount] = useState(5);
  const [ledger, setLedger] = useState<unknown[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const refresh = async () => {
    const b = await getBalance();
    setBalance(b.balance);
    const l = await getLedger();
    setLedger(l.entries);
  };

  useEffect(() => {
    refresh();
  }, []);

  usePolling(refresh, 5000, true);

  const onDeposit = async (e: FormEvent) => {
    e.preventDefault();
    const res = await deposit(depositAmount);
    setBalance(res.balance);
    setMessage(`Deposited ${depositAmount}`);
    refresh();
  };

  const onTransfer = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const res = await transfer(transferTo, transferAmount);
      setMessage(res.message);
      refresh();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Transfer failed");
    }
  };

  return (
    <div>
      <div className="card">
        <h3>Wallet</h3>
        <p style={{ fontSize: "2rem", margin: 0 }}>${balance.toFixed(2)}</p>
        {message && <p className="error-text">{message}</p>}
      </div>
      <div className="grid-2">
        <form className="card" onSubmit={onDeposit}>
          <h4>Deposit</h4>
          <input
            type="number"
            value={depositAmount}
            onChange={(e) => setDepositAmount(Number(e.target.value))}
          />
          <button className="btn" type="submit" style={{ marginTop: "0.5rem" }}>
            Add funds
          </button>
        </form>
        <form className="card" onSubmit={onTransfer}>
          <h4>Transfer</h4>
          <div className="form-group">
            <label>To user ID</label>
            <input
              type="number"
              value={transferTo}
              onChange={(e) => setTransferTo(Number(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>Amount</label>
            <input
              type="number"
              value={transferAmount}
              onChange={(e) => setTransferAmount(Number(e.target.value))}
            />
          </div>
          <button className="btn" type="submit">
            Send
          </button>
        </form>
      </div>
      <div className="card">
        <h4>Ledger (global)</h4>
        <pre style={{ fontSize: "0.75rem", overflow: "auto", maxHeight: 200 }}>
          {JSON.stringify(ledger, null, 2)}
        </pre>
      </div>
    </div>
  );
}
