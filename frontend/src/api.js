import axios from "axios";

const LOCAL_API = "http://127.0.0.1:8000";
const PROD_API = "https://sawakart.onrender.com";

let baseURL = LOCAL_API;

// Test local API availability
try {
  const res = await fetch(`${LOCAL_API}/docs`);
  if (!res.ok) baseURL = PROD_API;
} catch {
  baseURL = PROD_API;
}

const api = axios.create({
  baseURL,
  withCredentials: true,
});

export default api;
