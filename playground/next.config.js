/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  basePath: process.env.PLAYGROUND_BASE_PATH || '',
};

module.exports = nextConfig;
