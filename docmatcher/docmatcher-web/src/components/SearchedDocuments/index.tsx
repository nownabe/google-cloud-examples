import { Skeleton, Stack } from "@mui/material";
import { useCallback, useEffect, useState } from "react";

import ErrorSnackbar from "../ErrorSnackbar";

import SearchedDocument from "./SearchedDocument";

import { searchDocuments } from "@/api";
import { Document } from "@/api/client";

interface Props {
  content: string;
  onSearchFinished: () => void;
}

const SearchedDocuments = ({ content, onSearchFinished }: Props) => {
  const [documents, setDocuments] = useState<Array<Document> | null>(null);
  const [error, setError] = useState<null | string>(null);

  useEffect(() => {
    (async () => {
      const response = await searchDocuments(content);
      if (response.ok) {
        setDocuments(response.data);
      } else {
        console.error(response.error);
        setError(response.error.detail);
      }
      onSearchFinished();
    })();
  }, [setDocuments, content, setError, onSearchFinished]);

  const onErrorClose = useCallback(() => {
    setError(null);
  }, [setError]);

  if (documents === null) {
    return (
      <Stack spacing={2}>
        <Stack spacing={0}>
          <Skeleton variant="text" />
          <Skeleton variant="text" />
          <Skeleton variant="text" />
        </Stack>
        <Stack spacing={0}>
          <Skeleton variant="text" />
          <Skeleton variant="text" />
          <Skeleton variant="text" />
        </Stack>
        <Stack spacing={0}>
          <Skeleton variant="text" />
          <Skeleton variant="text" />
          <Skeleton variant="text" />
        </Stack>
      </Stack>
    );
  }

  return (
    <>
      <Stack spacing={2}>
        {documents.map((doc, i) => (
          <SearchedDocument key={i} document={doc} content={content} />
        ))}
      </Stack>
      <ErrorSnackbar
        open={!!error}
        message={error ?? ""}
        onClose={onErrorClose}
      />
    </>
  );
};

export default SearchedDocuments;
