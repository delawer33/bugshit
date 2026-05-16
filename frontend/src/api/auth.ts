import { api, setToken } from "./client";
import type { User } from "../types";

interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(username: string, password: string): Promise<void> {
  const res = await api.post<TokenResponse>("/auth/login", { username, password });
  setToken(res.access_token);
}

export async function register(
  email: string,
  username: string,
  password: string
): Promise<User> {
  return api.post<User>("/auth/register", {
    email,
    username,
    password,
    display_name: username,
  });
}
