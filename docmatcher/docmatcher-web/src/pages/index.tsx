import { Button, Container, TextField, Stack, Box } from "@mui/material";
import Head from "next/head";

import Header from "@/components/Header";

export default function Home() {
  return (
    <>
      <Head>
        <title>Doc Matcher Demo</title>
      </Head>
      <Header />
      <main>
        <Container sx={{ mt: 4 }}>
          <Stack spacing={2}>
            <TextField label="document text" multiline rows={10} fullWidth />
            <Box style={{ display: "flex" }}>
              <div style={{ flexGrow: 1 }} />
              <Button variant="contained">Search similar document</Button>
            </Box>
          </Stack>
        </Container>
      </main>
    </>
  );
}
