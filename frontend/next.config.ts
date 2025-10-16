import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',  // Enable static HTML export for GitHub Pages
  basePath: '/Real_Estate',  // GitHub Pages subdirectory (change if repo name differs)
  assetPrefix: '/Real_Estate/',
  images: {
    unoptimized: true, // GitHub Pages doesn't support Next.js Image Optimization
  },
};

export default nextConfig;
