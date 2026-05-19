import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://10.30.1.219:8080/api/v1"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
