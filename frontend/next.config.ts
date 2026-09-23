import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Standalone output for docker (does not affect SST; OpenNext does its own build)
  output: "standalone",
};

export default nextConfig;
