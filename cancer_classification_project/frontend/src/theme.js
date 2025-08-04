import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#CEB5D4",
    },
    secondary: {
      main: "#AB3743",
    },
    background: {
      default: "#0B0F28",
      paper: "rgba(255, 255, 255, 0.2)",  // 👈 Transparent white for glassmorphism
    },
    text: {
      primary: "#ECEFF1",
    },
    warning: {
      main: "#FF6F00",
    },
  },
  typography: {
    fontFamily: "'Poppins', 'Roboto', sans-serif",  // 👈 Modern clean font
  },
});

export default theme;
