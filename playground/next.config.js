/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  basePath: '/playground',
  async redirects() {
    // redirect from / to /playground for simpler local development
    return [
        {
            source: '/',
            destination: '/playground',
            basePath: false,
            permanent: false
        }
    ]
  }
};

module.exports = nextConfig;
