import { Box, Button, Fade, Paper, Typography } from "@mui/material";
import React from "react";
import { Link } from "react-router-dom";
import { Typewriter } from 'react-simple-typewriter';

function Home() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "text.primary",
        px: 3,
        position: "relative",
      }}
    >
      {/* Optional subtle background shapes */}
      <Box
        sx={{
          position: "absolute",
          width: "100%",
          height: "100%",
          background: "radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 70%), radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 70%)",
          zIndex: -1
        }}
      />

      <Fade in timeout={1000}>
        <Paper elevation={6} sx={{
          p: 6,
          backgroundColor: "rgba(255, 255, 255, 0.2)",
          backdropFilter: "blur(10px)",
          textAlign: "center",
          maxWidth: "700px",
          borderRadius: "20px"
        }}>
          <Typography variant="h2" gutterBottom>
            🧬 Cancer Subtype Predictor
          </Typography>

          <Typography variant="h5" color="textSecondary" sx={{ mb: 3 }}>
            <Typewriter
              words={[
                "AI-powered cancer subtype classification.",
                "Upload your gene expression data.",
                "Get fast and explainable predictions."
              ]}
              loop={0}
              cursor
              cursorStyle='_'
              typeSpeed={50}
              deleteSpeed={30}
              delaySpeed={1000}
            />
          </Typography>

          <Button
            variant="contained"
            size="large"
            component={Link}
            to="/upload"
            sx={{
              mt: 3,
              borderRadius: "30px",
              px: 5,
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "scale(1.05)",
                backgroundColor: "#AB3743"
              }
            }}
          >
            Get Started
          </Button>

          <Typography variant="body2" color="textSecondary" sx={{ mt: 4 }}>
            Empowering researchers and clinicians with Explainable AI.
          </Typography>
        </Paper>
      </Fade>
    </Box>
  );
}

export default Home;
