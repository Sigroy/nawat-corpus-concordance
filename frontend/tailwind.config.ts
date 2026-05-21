import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#20231f",
        paper: "#f7f3ec",
        bone: "#fffdf8",
        line: "#ded6c8",
        moss: "#66745c",
        teal: "#176b6a",
        claret: "#8f2f3f",
        gold: "#b6872d"
      },
      boxShadow: {
        soft: "0 18px 50px rgba(32, 35, 31, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;
