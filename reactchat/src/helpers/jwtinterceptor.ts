// Import necessary libraries and dependencies.
import axios, { AxiosInstance } from "axios";
import { useNavigate } from "react-router-dom";
import { BASE_URL } from "../config";

// Define the base URL for API requests.
const API_BASE_URL = BASE_URL;

// Define a custom React hook for creating an Axios instance with an interceptor.
const useAxiosWithInterceptor = (): AxiosInstance => {
  // Create an Axios instance with the specified base URL.
  const jwtAxios = axios.create({ baseURL: API_BASE_URL });

  // Access the React Router's navigation function.
  const navigate = useNavigate();

  // Add a response interceptor to handle certain error cases, e.g., 403 Forbidden.
  jwtAxios.interceptors.response.use(
    (response) => {
      // If the response is successful, return it.
      return response;
    },
    async (error) => {
      // Access the original request configuration.
      const originalRequest = error.config;

      // Check if the error response has a status code of 403 (Forbidden).
      if (error.response?.status === 403) {
        // Define a function to navigate to a specific route (e.g., "/test").
        const goRoot = () => navigate("/test");

        // Trigger the navigation function to redirect to the desired route.
        goRoot();
      }

      // Throw the error to propagate it further if needed.
      throw error;
    }
  );

  // Return the Axios instance with the interceptor.
  return jwtAxios;
};

// Export the custom hook as the default export.
export default useAxiosWithInterceptor;
