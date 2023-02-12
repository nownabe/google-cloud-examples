import { Tooltip, IconButton, IconButtonProps } from "@mui/material";
import { useCallback, useState } from "react";

import ErrorSnackbar from "../ErrorSnackbar";

import { createFeedback } from "@/api";

interface Props {
  defaultIcon: JSX.Element;
  pressedIcon: JSX.Element;
  pressedColor: IconButtonProps["color"];
  label: string;
  tooltip: string;
  content: string;
  documentId: string;
  score: number;
}

const FeedbackButton = (props: Props) => {
  const [pressed, setPressed] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onClick = useCallback(async () => {
    setPressed(true);
    const response = await createFeedback(
      props.content,
      props.documentId,
      props.score
    );
    if (!response.ok) {
      setError(response.error.detail);
      setPressed(false);
    }
  }, [setPressed, props.content, props.documentId, props.score, setError]);

  const handleCancel = useCallback(async () => {
    setPressed(false);
    const response = await createFeedback(
      props.content,
      props.documentId,
      -props.score
    );
    if (!response.ok) {
      setError(response.error.detail);
      setPressed(true);
    }
  }, [setPressed, props.content, props.documentId, props.score, setError]);

  const onErrorClosed = useCallback(() => setError(null), [setError]);

  return (
    <>
      <Tooltip title="You think it's similar">
        {pressed ? (
          <IconButton
            aria-label="like"
            color={props.pressedColor}
            onClick={handleCancel}
          >
            {props.pressedIcon}
          </IconButton>
        ) : (
          <IconButton aira-label="like" color="default" onClick={onClick}>
            {props.defaultIcon}
          </IconButton>
        )}
      </Tooltip>
      <ErrorSnackbar
        open={!!error}
        message={error ?? ""}
        onClose={onErrorClosed}
      />
    </>
  );
};

export default FeedbackButton;
