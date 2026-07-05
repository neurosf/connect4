import React, { useState } from "react";
import { Grid, Typography, Box, Modal } from "@mui/material";
import { Link } from "react-router-dom";
import "../fonts/fonts.css";
import { CustomButton } from "../components/Theme";

function Home() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          backgroundColor: "#1A1A1D",
          width: "100vw",
          height: "100vh",
        }}
      >
        <Modal
          open={showModal}
          onClose={() => {
            setShowModal(false);
          }}
          aria-labelledby="winner-modal"
          aria-describedby="winner-modal-description"
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "#0d0d0e", // Black background with transparency
            boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.5)", // Shadow effect
            borderRadius: "8px", // Optional: Adds rounded corners
            outline: "none", // Optional: Remove default outline
            maxWidth: { xs: "50%", md: "30%" }, // Optional: Limit maximum width
            maxHeight: "max-content", // Optional: Limit maximum height
            margin: "auto", // Center horizontally and vertically
            padding: "20px", // Optional: Add padding
            overflow: "auto", // Enable scrolling if content overflows
          }}
        >
          <Grid
            container
            spacing={2}
            sx={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Grid item>
              <CustomButton
                component={Link}
                to="/humanfirst"
                sx={{
                  fontSize: { xs: "0.8rem", md: "0.8rem" },
                  textAlign: "center",
                  border: "none",
                  borderRadius: '0',
                  "&:hover": {
                    transition: "all 0.2s ease-in-out",
                    background: '#FFFFFF08'
                  }
                }}
              >
                You play first
              </CustomButton>
            </Grid>

            <Grid item>
              <CustomButton
                component={Link}
                to="/botfirst"
                sx={{
                  fontSize: { xs: "0.8rem", md: "0.8rem" },
                  textAlign: "center",
                  border: "none",
                  borderRadius: '0',
                  "&:hover": {
                    transition: "all 0.2s ease-in-out",
                    background: '#FFFFFF08'
                  }
                }}
              >
                AI bot play first
              </CustomButton>
            </Grid>
          </Grid>
        </Modal>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Typography
            variant="h3"
            sx={{
              fontSize: { xs: "3rem", md: "5rem" },
              marginBottom: "0.3rem",
              color: "#C3073F",
              fontFamily: "Robus, sans-serif",
            }}
          >
            Connect Four Game
          </Typography>
          <Typography
            sx={{
              fontSize: "1rem",
              marginBottom: "1.5rem",
              fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
              fontWeight: "400",
              color: "white",
              marginRight: { xs: "2rem" },
              marginLeft: { xs: "2rem" },
            }}
          >
            a classic strategy game in which two players go head-to-head in a
            battle to own the grid!
          </Typography>
        </Box>
        <Grid
          container
          spacing={{ xs: 2, md: -30, lg: -70 }}
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            width: "100vw",
          }}
        >
          <Grid
            item
            xs={12}
            md={6}
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CustomButton
              onClick={() => setShowModal(true)}
              sx={{
                fontSize: { xs: "0.8rem", md: "1.2rem" },
                "&:hover": {
                  transform: "scale(1.1)",
                },
              }}
            >
              Human vs. AI bot
            </CustomButton>
          </Grid>

          <Grid
            item
            xs={12}
            md={6}
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <CustomButton
              component={Link}
              to="/bots"
              sx={{
                fontSize: { xs: "0.8rem", md: "1.2rem" },
                "&:hover": {
                  transform: "scale(1.1)",
                },
              }}
            >
              AI bot 1 vs. AI bot 2
            </CustomButton>
          </Grid>
        </Grid>
      </Box>
    </>
  );
}

export default Home;
