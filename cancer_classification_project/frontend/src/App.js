// import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
// import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
// import Home from "./Home";
// import Upload from "./Upload";
// import BackgroundImage from "./images/backgroundimage.png"; // 👈 Import your background image

// function App() {
//   return (
//     <Box
//       sx={{
//         display: "flex",
//         flexDirection: "column",
//         minHeight: "100vh",
//         backgroundImage: `url(${BackgroundImage})`,
//         backgroundSize: "cover",
//         backgroundRepeat: "no-repeat",
//         backgroundPosition: "center",
//         backgroundAttachment: "fixed",
//         color: "text.primary",
//         backgroundColor: "rgba(0, 0, 0, 0.3)", // Optional dark overlay
//         backgroundBlendMode: "darken",
//       }}
//     >
//       <BrowserRouter>
//         {/* ✅ Navbar */}
//         <AppBar position="static" sx={{ backgroundColor: "#AC1634" }}>
//           <Toolbar>
//             <Typography variant="h6" sx={{ flexGrow: 1 }}>
//               CancerXAI
//             </Typography>
//             <Button color="inherit" component={Link} to="/">Home</Button>
//             <Button color="inherit" component={Link} to="/upload">Upload</Button>
//           </Toolbar>
//         </AppBar>

//         {/* ✅ Page Content */}
//         <Container sx={{ mt: 4 }}>
//           <Routes>
//             <Route path="/" element={<Home />} />
//             <Route path="/upload" element={<Upload />} />
//           </Routes>
//         </Container>

//         {/* ✅ Footer */}
//         <Box component="footer" sx={{
//           mt: "auto",  // Push to bottom
//           py: 3,
//           textAlign: "center"
//         }}>
//           © Cancer Subtype Predictor 2025
//         </Box>
//       </BrowserRouter>
//     </Box>
//   );
// }

// export default App;


// import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
// import { useState } from "react";
// import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
// import Home from "./Home";
// import Results from "./Results";
// import Upload from "./Upload";
// import BackgroundImage from "./images/backgroundimage.png";
// import './index.css';

// function App() {
//   const [predictions, setPredictions] = useState([]);
//   const [downloadLink, setDownloadLink] = useState("");

//   return (
//     <Box
//       sx={{
//         display: "flex",
//         flexDirection: "column",
//         minHeight: "100vh",
//         backgroundImage: `url(${BackgroundImage})`,
//         backgroundSize: "cover",
//         backgroundRepeat: "no-repeat",
//         backgroundPosition: "center",
//         backgroundAttachment: "fixed",
//         color: "text.primary",
//         backgroundColor: "rgba(0, 0, 0, 0.3)",
//         backgroundBlendMode: "darken",
//       }}
//     >
//       <BrowserRouter>
//         <AppBar position="static" sx={{ backgroundColor: "#AC1634" }}>
//           <Toolbar>
//             <Typography variant="h6" sx={{ flexGrow: 1 }}>
//               CancerXAI
//             </Typography>
//             <Button color="inherit" component={Link} to="/">Home</Button>
//             <Button color="inherit" component={Link} to="/upload">Upload</Button>
//           </Toolbar>
//         </AppBar>

//         <Container sx={{ mt: 4 }}>
//           <Routes>
//             <Route path="/" element={<Home />} />
//             <Route
//               path="/upload"
//               element={
//                 <Upload
//                   setPredictions={setPredictions}
//                   setDownloadLink={setDownloadLink}
//                 />
//               }
//             />
//             <Route
//               path="/results"
//               element={
//                 <Results
//                   predictions={predictions}
//                   downloadUrl={downloadLink}
//                 />
//               }
//             />
//           </Routes>
//         </Container>

//         <Box component="footer" sx={{ mt: "auto", py: 3, textAlign: "center" }}>
//           © Cancer Subtype Predictor 2025
//         </Box>
//       </BrowserRouter>
//     </Box>
//   );
// }

// export default App;




import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
import { useState } from "react";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Home from "./Home";
import Results from "./Results";
import Upload from "./Upload";
import BackgroundImage from "./images/backgroundimage.png";
import './index.css'; // Keep Tailwind/base styles or your custom styles

function App() {
  const [predictions, setPredictions] = useState([]);
  const [downloadLink, setDownloadLink] = useState("");

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        minHeight: "100vh",
        backgroundImage: `url(${BackgroundImage})`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        backgroundAttachment: "fixed",
        color: "text.primary",
        backgroundColor: "rgba(0, 0, 0, 0.3)",
        backgroundBlendMode: "darken",
      }}
    >
      <BrowserRouter>
        <AppBar position="static" sx={{ backgroundColor: "#AC1634" }}>
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              CancerXAI
            </Typography>
            <Button color="inherit" component={Link} to="/">Home</Button>
            <Button color="inherit" component={Link} to="/upload">Upload</Button>
          </Toolbar>
        </AppBar>

        <Container sx={{ mt: 4 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route
              path="/upload"
              element={
                <Upload
                  setPredictions={setPredictions}
                  setDownloadLink={setDownloadLink}
                />
              }
            />
            <Route
              path="/results"
              element={
                <Results
                  predictions={predictions}
                  downloadUrl={downloadLink}
                />
              }
            />
          </Routes>
        </Container>

        <Box component="footer" sx={{ mt: "auto", py: 3, textAlign: "center" }}>
          © Cancer Subtype Predictor 2025
        </Box>
      </BrowserRouter>
    </Box>
  );
}

export default App;
