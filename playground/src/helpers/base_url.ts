// dynamic lookup to be able to change the url at runtime,
// see https://nextjs.org/docs/pages/building-your-application/configuring/environment-variables#exposing-environment-variables-to-the-browser
const athenaDomainFromEnv = process.env["NEXT_PUBLIC_ATHENA_DOMAIN"];

const baseUrl = (athenaDomainFromEnv ? `//${athenaDomainFromEnv}` : 'http://localhost:3000') + '/playground';
export default baseUrl;