import {
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField,
} from "@mui/material";
import { useState, useCallback, useRef } from "react";

import ErrorSnackbar from "../ErrorSnackbar";

import { createDocument } from "@/api";

interface Props {
  open: boolean;
  onClose: () => void;
}

const AddDocumentDialog = ({ open, onClose }: Props) => {
  const contentRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<null | string>(null);

  const onCancelClicked = useCallback(() => {
    onClose();
    if (contentRef.current) {
      contentRef.current.value = "";
    }
  }, [onClose]);

  const onAddClicked = useCallback(async () => {
    if (!contentRef.current) {
      return;
    }

    const content = contentRef.current.value;

    setLoading(true);

    const resp = await createDocument(content);

    if (resp.ok) {
      onClose();
      setLoading(false);
      contentRef.current.value = "";
    } else {
      console.error(resp.error);
      setLoading(false);
      setError(resp.error.detail);
    }
  }, [setLoading, setError, onClose]);

  const onErrorClose = useCallback(() => {
    setError(null);
  }, [setError]);

  return (
    <>
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogTitle>Add new document</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Enter the content of the new document as a plain text.
          </DialogContentText>
          <TextField
            fullWidth
            multiline
            rows={10}
            autoFocus
            sx={{ mt: 2 }}
            defaultValue=""
            inputRef={contentRef}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={onCancelClicked} disabled={loading}>
            Cancel
          </Button>
          <Box sx={{ m: 1, position: "relative" }}>
            <Button
              variant="contained"
              onClick={onAddClicked}
              disabled={loading}
            >
              Add
            </Button>
            {loading && (
              <CircularProgress
                size={24}
                sx={{
                  position: "absolute",
                  top: "50%",
                  left: "50%",
                  marginTop: "-12px",
                  marginLeft: "-12px",
                }}
              />
            )}
          </Box>
        </DialogActions>
      </Dialog>
      <ErrorSnackbar
        open={!!error}
        message={error ?? ""}
        onClose={onErrorClose}
      />
    </>
  );
};

export default AddDocumentDialog;
