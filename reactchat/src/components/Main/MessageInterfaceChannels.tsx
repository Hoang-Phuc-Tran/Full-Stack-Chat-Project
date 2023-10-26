import {
  AppBar,
  Toolbar,
  Box,
  ListItemAvatar,
  Avatar,
  Typography,
  IconButton,
  Drawer,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { MEDIA_URL } from "../../config";
import { Server } from "../../@types/server.d";
import { useParams } from "react-router-dom";
import ServerChannels from "../SecondaryDraw/ServerChannels";
import { useEffect, useState } from "react";
import MoreVertIcon from "@mui/icons-material/MoreVert";

interface ServerChannelProps {
  data: Server[];
}

// Define a functional component for rendering a list of server channels.
const MessageInterfaceChannels = (props: ServerChannelProps) => {
  // Destructure the 'data' property from props.
  const { data } = props;

  // Access the theme from the UI library.
  const theme = useTheme();

  // Extract 'serverId' and 'channelId' from the URL parameters.
  const { serverId, channelId } = useParams();

  // Define state variable to manage the side menu's visibility.
  const [sideMenu, setSideMenu] = useState(false);

  // Determine the channel name based on the provided data, or set it to "home" if not found.
  const channelName =
    data
      ?.find((server) => server.id == Number(serverId))
      ?.channel_server?.find((channel) => channel.id === Number(channelId))?.name || "home";

  // Determine if the screen is small based on the media query.
  const isSmallScreen = useMediaQuery(theme.breakpoints.up("sm"));

  // Close the side menu when transitioning to a small screen.
  useEffect(() => {
    if (isSmallScreen && sideMenu) {
      setSideMenu(false);
    }
  }, [isSmallScreen]);

  // Function to toggle the side menu's visibility.
  const toggleDrawer = (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
    if (
      event.type === "keydown" &&
      ((event as React.KeyboardEvent).key === "Tab" ||
        (event as React.KeyboardEvent).key === "Shift")
    ) {
      return;
    }
    setSideMenu(open);
  };

  // Function to render the list of server channels within the side menu.
  const list = () => (
    <Box
      sx={{ paddingTop: `${theme.primaryAppBar.height}px`, minWidth: 200 }}
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <ServerChannels data={data} />
    </Box>
  );

  return (
    <>
      <AppBar
        sx={{
          backgroundColor: theme.palette.background.default,
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
        color="default"
        position="sticky"
        elevation={0}
      >
        <Toolbar
          variant="dense"
          sx={{
            minHeight: theme.primaryAppBar.height,
            height: theme.primaryAppBar.height,
            display: "flex",
            alignItems: "center",
          }}
        >
          <Box sx={{ display: { xs: "block", sm: "none" } }}>
            <ListItemAvatar sx={{ minWidth: "40px" }}>
              <Avatar
                alt="Server Icon"
                src={`${MEDIA_URL}${data?.[0]?.icon}`}
                sx={{ width: 30, height: 30 }}
              />
            </ListItemAvatar>
          </Box>

          <Typography noWrap component="div">
            {channelName}
          </Typography>

          <Box sx={{ flexGrow: 1 }}></Box>
          <Box sx={{ display: { xs: "block", sm: "none" } }}>
            <IconButton color="inherit" onClick={toggleDrawer(true)} edge="end">
              <MoreVertIcon />
            </IconButton>
          </Box>
          <Drawer anchor="left" open={sideMenu} onClose={toggleDrawer(false)}>
            {list()}
          </Drawer>
        </Toolbar>
      </AppBar>
    </>
  );
};
export default MessageInterfaceChannels;
