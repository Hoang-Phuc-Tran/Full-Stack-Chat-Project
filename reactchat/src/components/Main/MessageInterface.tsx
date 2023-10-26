import { useState } from "react";
import { useParams } from "react-router-dom";
import useWebSocket from "react-use-websocket";
import useCrud from "../../hooks/useCrud";
import { Server } from "../../@types/server.d";
import {
  Avatar,
  Box,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  TextField,
  Typography,
  useTheme,
} from "@mui/material";
import MessageInterfaceChannels from "./MessageInterfaceChannels";
import Scroll from "./Scroll";
import React from "react";

interface SendMessageData {
  type: string;
  message: string;
  [key: string]: any;
}

interface ServerChannelProps {
  data: Server[];
}

interface Message {
  sender: string;
  content: string;
  timestamp: string;
}

// Define a functional component for rendering a chat interface.
const messageInterface = (props: ServerChannelProps) => {
  // Destructure the 'data' property from props.
  const { data } = props;

  // Access the theme from the UI library.
  const theme = useTheme();

  // Define state variables for managing new messages and the input message.
  const [newMessage, setNewMessage] = useState<Message[]>([]);
  const [message, setMessage] = useState("");

  // Extract 'serverId' and 'channelId' from the URL parameters.
  const { serverId, channelId } = useParams();

  // Define a default server name if data is not available.
  const server_name = data?.[0]?.name ?? "Server";

  // Define a custom hook to fetch data related to the server.
  const { fetchData } = useCrud<Server>([], `/messages/?channel_id=${channelId}`);

  // Construct the WebSocket URL based on the server and channel.
  const socketUrl = channelId ? `ws://127.0.0.1:8000/${serverId}/${channelId}` : null;

  // Initialize a WebSocket connection and handle various WebSocket events.
  const { sendJsonMessage } = useWebSocket(socketUrl, {
    onOpen: async () => {
      try {
        // Fetch initial data when the WebSocket connection is established.
        const data = await fetchData();
        setNewMessage([]);
        setNewMessage(Array.isArray(data) ? data : []);
        console.log("Connected!!!");
      } catch (error) {
        console.log(error);
      }
    },
    onClose: () => {
      console.log("Closed!");
    },
    onError: () => {
      console.log("Error!");
    },
    onMessage: (msg) => {
      // Parse and process incoming WebSocket messages.
      const data = JSON.parse(msg.data);
      setNewMessage((prev_msg) => [...prev_msg, data.new_message]);
      setMessage("");
    },
  });

  // Handle the 'Enter' key press to send a message.
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (message !== "") {
        // Just check if the message is not empty
        sendJsonMessage({
          type: "message",
          message,
        } as SendMessageData);
      }
    }
  };

  // Handle form submission to send a message.
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Check if the message is not empty before sending.
    if (message !== "") {
      sendJsonMessage({
        type: "message",
        message,
      } as SendMessageData);
    }
  };

  // Function to format a timestamp string for display.
  function formatTimeStamp(timestamp: string): string {
    const date = new Date(Date.parse(timestamp));
    const formattedDate = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;

    const formattedTime = date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });

    return `${formattedDate} at ${formattedTime}`;
  }

  return (
    <>
      <MessageInterfaceChannels data={data} />
      {channelId == undefined ? (
        <Box
          sx={{
            overflow: "hidden",
            p: { xs: 0 },
            height: `calc(80vh)`,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Box sx={{ textAlign: "center" }}>
            <Typography
              variant="h4"
              fontWeight={700}
              letterSpacing={"-0.5px"}
              sx={{ px: 5, maxWidth: "600px" }}
            >
              Welcome to {server_name}
            </Typography>
            <Typography>{data?.[0]?.description ?? "This is our home"}</Typography>
          </Box>
        </Box>
      ) : (
        <>
          <Scroll>
            <List sx={{ width: "100%", bgcolor: "background.paper" }}>
              {newMessage.map((msg: Message, index: number) => {
                return (
                  <ListItem key={index} alignItems="flex-start">
                    <ListItemAvatar>
                      <Avatar alt="user image" />
                    </ListItemAvatar>
                    <ListItemText
                      primaryTypographyProps={{
                        fontSize: "12px",
                        variant: "body2",
                      }}
                      primary={
                        <>
                          <Typography
                            component="span"
                            variant="body1"
                            color="text.primary"
                            sx={{ display: "inline", fontW: 600 }}
                          >
                            {msg.sender}
                          </Typography>
                          <Typography component="span" variant="caption" color="textSecondary">
                            {" at "}
                            {formatTimeStamp(msg.timestamp)}
                          </Typography>
                        </>
                      }
                      secondary={
                        <>
                          <Typography
                            variant="body1"
                            style={{
                              overflowWrap: "break-word",
                              paddingRight: "69px",
                              whiteSpace: "normal",
                              textOverflow: "clip",
                              width: "100%", // Ensure Typography takes up full width
                              display: "block", // Ensure Typography behaves as a block-level element
                            }}
                            sx={{
                              display: "inline",
                              lineHeight: 1.2,
                              fontWeight: 400,
                              letterSpacing: "-0.2px",
                            }}
                            component="div"
                            color="text.primary"
                          >
                            {msg.content}
                          </Typography>
                        </>
                      }
                    />
                  </ListItem>
                );
              })}
            </List>
          </Scroll>
          <Box sx={{ position: "sticky", bottom: 0, width: "100%" }}>
            <form
              onSubmit={handleSubmit}
              style={{
                bottom: 0,
                right: 0,
                padding: "1rem",
                backgroundColor: theme.palette.background.default,
                zIndex: 1,
              }}
            >
              <Box sx={{ display: "flex" }}>
                <TextField
                  fullWidth
                  multiline
                  value={message}
                  minRows={1}
                  maxRows={4}
                  onKeyDown={handleKeyDown}
                  onChange={(e) => setMessage(e.target.value)}
                  sx={{ flexGrow: 1 }}
                />
              </Box>
            </form>
          </Box>
        </>
      )}
    </>
  );
};
export default messageInterface;
