import "@/styles/globals.css";
import type { AppProps } from "next/app";
import Head from "next/head";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <title>Athena Playground</title>
        <link rel="icon" href="/logo.png" sizes="any" />
      </Head>
      <Component {...pageProps} />
      <footer className="p-4 text-white border-t border-opacity-10 text-xs">
        {
          process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA ? <>
            <a href={`https://github.com/ls1intum/Athena/tree/${process.env.ATHENA_BRANCH}`} target="_blank">
              Branch:&nbsp;{process.env.NEXT_PUBLIC_ATHENA_BRANCH}&nbsp;- 
            </a>
            <span>
              Commit:&nbsp;{process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA}&nbsp;-
            </span>
          </> : (
            <span>Local build</span>
          )
        }
      </footer>
    </>
  );
}
