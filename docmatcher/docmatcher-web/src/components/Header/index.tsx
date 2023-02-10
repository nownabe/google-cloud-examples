import { Add } from "@mui/icons-material";
import { Toolbar, AppBar, Typography, Button } from "@mui/material";
import Image from "next/image";
import { useState } from "react";

import AddDocumentDialog from "./AddDocumentDialog";

const Header = () => {
  const [dialogOpen, setDialogOpen] = useState(false);

  const handleClickAddDocument = () => setDialogOpen(true);
  const onDialogClose = () => setDialogOpen(false);

  return (
    <>
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
          <Button startIcon={<Add />} onClick={handleClickAddDocument}>
            Add Document
          </Button>
        </Toolbar>
      </AppBar>
      <AddDocumentDialog open={dialogOpen} onClose={onDialogClose} />
    </>
  );
};

export default Header;
