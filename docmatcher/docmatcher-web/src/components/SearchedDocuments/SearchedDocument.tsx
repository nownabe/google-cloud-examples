import { ThumbDownOutlined, ThumbUpOutlined } from "@mui/icons-material";
import {
  Card,
  CardActions,
  CardContent,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material";

import { Document } from "@/api/client";

interface Props {
  document: Document;
}

const SearchedDocument = ({ document }: Props) => {
  return (
    <Card>
      <CardContent>
        <Typography color="text.secondary">{document.id}</Typography>
        <Typography variant="h6" component="article">
          {document.content}
        </Typography>
      </CardContent>
      <CardActions>
        <Tooltip title="You think it's similar">
          <IconButton aira-label="like">
            <ThumbUpOutlined />
          </IconButton>
        </Tooltip>
        <Tooltip title="You don't think it's similar">
          <IconButton aira-label="dislike">
            <ThumbDownOutlined />
          </IconButton>
        </Tooltip>
      </CardActions>
    </Card>
  );
};

export default SearchedDocument;
