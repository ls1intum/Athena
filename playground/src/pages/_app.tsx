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
          process.env.NEXT_PUBLIC_ATHENA_IS_DEVELOP ? <>
            <span>develop</span>&nbsp;-&nbsp;
            <a href={`https://github.com/ls1intum/Athena/commit/${process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA}`} target="_blank" className="hover:underline">
              Commit:&nbsp;{(process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA ?? '').slice(0, 7)}
            </a>&nbsp;-&nbsp;
            </> : (
            process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA ? <>
              <a href={`https://github.com/ls1intum/Athena/pull/${process.env.NEXT_PUBLIC_ATHENA_PR_NUMBER}`} target="_blank" className="hover:underline">
                PR&nbsp;#{process.env.NEXT_PUBLIC_ATHENA_PR_NUMBER}:&nbsp;
                {process.env.NEXT_PUBLIC_ATHENA_PR_TITLE}
              </a>&nbsp;-&nbsp;
              <a href={`https://github.com/ls1intum/Athena/pull/${process.env.NEXT_PUBLIC_ATHENA_PR_NUMBER}/commits/${process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA}`} target="_blank" className="hover:underline">
                Commit:&nbsp;{(process.env.NEXT_PUBLIC_ATHENA_COMMIT_SHA ?? '').slice(0, 7)}
              </a>&nbsp;-&nbsp;
              <span>
                Last update:&nbsp;{process.env.NEXT_PUBLIC_ATHENA_PR_LAST_UPDATE}
              </span>
            </> : (
              <span>Local build</span>
            )
          )
        }
      </footer>
    </>
  );
}
