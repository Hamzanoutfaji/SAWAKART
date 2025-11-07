import axios from "axios";

const LOCAL_API = "http://127.0.0.1:8000";
const PROD_API = "https://sawakart-docker.onrender.com";
const baseURL = PROD_API;

const api = axios.create({
  baseURL,
  withCredentials: true,
});

export default api;
