import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',  // Enable static HTML export for GitHub Pages
  basePath: '/Real_estate_PricePredictor_ML',  // Match your GitHub repo name
  assetPrefix: '/Real_estate_PricePredictor_ML/',
  images: {
    unoptimized: true,  // GitHub Pages doesn't support Next.js Image Optimization
  },
};

export default nextConfig;
