import { Button, Container, TextField, Stack, Box } from "@mui/material";
import Head from "next/head";
import React, { useState, useCallback, useRef } from "react";

import Header from "@/components/Header";
import ProgressButton from "@/components/ProgressButton";
import SearchedDocuments from "@/components/SearchedDocuments";

export default function Home() {
  const contentRef = useRef<HTMLInputElement>(null);

  const [searching, setSearching] = useState(false);
  const [isSearchClicked, setIsSearchClicked] = useState(false);
  const [content, setContent] = useState("");

  const onClearClicked = useCallback(() => {
    if (contentRef.current) {
      contentRef.current.value = "";
    }
  }, []);

  const onSearchClicked = useCallback(() => {
    if (contentRef.current) {
      setSearching(true);
      setIsSearchClicked(true);
      setContent(contentRef.current.value);
    }
  }, [setSearching, setIsSearchClicked, setContent]);

  const onSearchFinished = useCallback(() => {
    setSearching(false);
  }, [setSearching]);

  return (
    <>
      <Head>
        <title>Doc Matcher Demo</title>
      </Head>
      <Header />
      <main>
        <Container sx={{ mt: 4 }}>
          <Stack spacing={2}>
            <TextField
              multiline
              rows={10}
              fullWidth
              placeholder="document content you want to search for similar documents as a plain text"
              inputRef={contentRef}
            />
            <Box style={{ display: "flex" }}>
              <div style={{ flexGrow: 1 }} />
              <Button onClick={onClearClicked} disabled={searching}>
                Clear
              </Button>
              <ProgressButton
                variant="contained"
                onClick={onSearchClicked}
                loading={searching}
              >
                Search similar documents
              </ProgressButton>
            </Box>
            {isSearchClicked ? (
              <SearchedDocuments
                content={content}
                onSearchFinished={onSearchFinished}
              />
            ) : null}
          </Stack>
        </Container>
      </main>
    </>
  );
}
