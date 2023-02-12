import {
  ThumbDown,
  ThumbDownOutlined,
  ThumbUp,
  ThumbUpOutlined,
} from "@mui/icons-material";
import {
  Card,
  CardActions,
  CardContent,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material";

import FeedbackButton from "./FeedbackButton";

import { Document } from "@/api/client";

interface Props {
  content: string;
  document: Document;
}

const SearchedDocument = ({ content, document }: Props) => {
  return (
    <Card>
      <CardContent>
        <Typography color="text.secondary">{document.id}</Typography>
        <Typography variant="h6" component="article">
          {document.content}
        </Typography>
      </CardContent>
      <CardActions>
        <FeedbackButton
          defaultIcon={<ThumbUpOutlined />}
          pressedIcon={<ThumbUp />}
          pressedColor="primary"
          label="like"
          tooltip="You think it's similar"
          content={content}
          documentId={document.id}
          score={1.0}
        />
        <FeedbackButton
          defaultIcon={<ThumbDownOutlined />}
          pressedIcon={<ThumbDown />}
          pressedColor="error"
          label="like"
          tooltip="You think it's similar"
          content={content}
          documentId={document.id}
          score={1.0}
        />
      </CardActions>
    </Card>
  );
};

export default SearchedDocument;
