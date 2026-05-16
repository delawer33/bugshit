import { api } from "./client";

export async function getBalance(): Promise<{ balance: number }> {
  return api.get("/wallet/balance");
}

export async function deposit(amount: number): Promise<{ balance: number }> {
  return api.post("/wallet/deposit", { amount });
}

export async function transfer(
  toUserId: number,
  amount: number
): Promise<{ message: string }> {
  return api.post("/wallet/transfer", { to_user_id: toUserId, amount });
}

export async function getLedger(): Promise<{ entries: unknown[] }> {
  return api.get("/wallet/ledger");
}
