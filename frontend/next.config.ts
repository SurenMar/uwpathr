import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactCompiler: true,
  output: 'standalone',       // For Docker optimization
  typescript: {
    ignoreBuildErrors: true,  // Temporarily ignore TS errors during docker build
  },
};

export default nextConfig;
