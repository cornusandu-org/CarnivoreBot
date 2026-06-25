import axios, { type Method } from "axios";
import { settings } from "./getSettings.js";

export async function callBackend<T = unknown>(
  api: string,
  method: string,
  data?: Record<string, unknown>,
): Promise<T> {
  const response = await axios.request<T>({
    url: settings.Local.Backend.Base + api,
    method,
    data,
    headers: {
      "Content-Type": "application/json",
    },
  });

  return response.data;
}
