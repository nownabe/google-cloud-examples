import type { AppProps } from "next/app";

import { CacheProvider, EmotionCache } from "@emotion/react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import Head from "next/head";

import createEmotionCache from "@/createEmotionCache";
import theme from "@/theme";

const clientSideEmotionCache = createEmotionCache();

interface Props extends AppProps {
  emotionCache?: EmotionCache;
}

export default function App(props: Props) {
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;

  return (
    <CacheProvider value={emotionCache}>
      <Head>
        <meta name="viewpoint" content="initial-scale=1, width=device-width" />
      </Head>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Component {...pageProps} />
      </ThemeProvider>
    </CacheProvider>
  );
}
