import { Box, CircularProgress } from "@mui/material";
import Button, { ButtonProps } from "@mui/material/Button";

type Props = ButtonProps & {
  loading: boolean;
};

const ProgressButton = ({ loading, disabled, children, ...props }: Props) => {
  const isDisabled = loading || disabled;

  return (
    <Box sx={{ m: 1, position: "relative" }}>
      <Button {...props} disabled={isDisabled}>
        {children}
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
  );
};

export default ProgressButton;
