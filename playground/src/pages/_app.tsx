import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Head from "next/head";
import { QueryClient, QueryClientProvider } from "react-query"
import { BaseInfoProvider } from "@/hooks/base_info_context";

const queryClient = new QueryClient()

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Athena Playground</title>
        <link rel="icon" href="/logo.png" sizes="any" />
      </Head>
      <QueryClientProvider client={queryClient}>
        <BaseInfoProvider>
          <Component {...pageProps} />
        </BaseInfoProvider>
      </QueryClientProvider>
    </>
  );
}
