import { Add } from "@mui/icons-material";
import {
  Toolbar,
  AppBar,
  Typography,
  Button,
  Container,
  TextField,
  Stack,
  Box,
  Grid,
} from "@mui/material";
import Head from "next/head";
import Image from "next/image";

export default function Home() {
  return (
    <>
      <Head>
        <title>Doc Matcher Demo</title>
      </Head>
      <AppBar position="static" sx={{ bgcolor: "white" }}>
        <Toolbar>
          <Image src="/vertexai.png" alt="Vertex AI" width="48" height="48" />
          <Typography
            variant="h6"
            component="h1"
            sx={{ flexGrow: 1, ml: 2, color: "black" }}
          >
            Doc Matcher Demo
          </Typography>
          <Button startIcon={<Add />}>Add Document</Button>
        </Toolbar>
      </AppBar>
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
