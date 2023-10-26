// Import necessary components and libraries from React, Material-UI, and context.
import { useContext } from "react";
import { ColorModeContext } from "../../../context/DarkModeContext";
import { useTheme } from "@mui/material/styles";
import { IconButton, Typography } from "@mui/material";
import ToggleOffIcon from "@mui/icons-material/ToggleOff";
import ToggleOnIcon from "@mui/icons-material/ToggleOn";
import Brightness4Icon from "@mui/icons-material/Brightness4";

// Define the DarkModeSwitch component.
const DarkModeSwitch = () => {
  // Access the theme from Material-UI.
  const theme = useTheme();

  // Access the color mode context using useContext.
  const colorMode = useContext(ColorModeContext);

  // Render the DarkModeSwitch component's JSX.
  return (
    <>
      {/* Render the Brightness4Icon for the dark mode toggle. */}
      <Brightness4Icon sx={{ marginRight: "6px", fontSize: "20px" }} />

      {/* Render the typography to display the current mode (dark/light). */}
      <Typography variant="body2" sx={{ textTransform: "capitalize" }}>
        {theme.palette.mode} mode
      </Typography>

      {/* Render the IconButton for toggling dark/light mode. */}
      <IconButton sx={{ m: 0, p: 0, pl: 2 }} onClick={colorMode.toggleColorMode} color="inherit">
        {/* Render the ToggleOffIcon for light mode and ToggleOnIcon for dark mode. */}
        {theme.palette.mode === "dark" ? (
          <ToggleOffIcon sx={{ fontSize: "2.5rem", p: 0 }} />
        ) : (
          <ToggleOnIcon sx={{ fontSize: "2.5rem" }} />
        )}
      </IconButton>
    </>
  );
};

// Export the DarkModeSwitch component as the default export.
export default DarkModeSwitch;
