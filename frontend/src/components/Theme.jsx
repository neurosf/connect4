import { styled } from '@mui/system';
import Button from '@mui/material/Button';

export const CustomButton = styled(Button)({
    background: "none",
    padding: "1.2rem 1rem",
    color: "#fff",
    border: "1px solid #C3073F",
    borderRadius: "3rem",
    cursor: "pointer",
    "&:hover": {
      transition: "all 0.5s ease-in-out",
      background: "linear-gradient(135deg, #950740, #C3073F)",
      border: "none",
      color: "#fff",
    },
    '&:focus, &:active': {
      outline: 'none',
      boxShadow: 'none',
    },
});


