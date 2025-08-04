// import AirIcon from "@mui/icons-material/Air";
// import CheckCircleIcon from "@mui/icons-material/CheckCircle";
// import FemaleIcon from "@mui/icons-material/Female";
// import HealthAndSafetyIcon from "@mui/icons-material/HealthAndSafety";
// import MaleIcon from "@mui/icons-material/Male";
// import StopIcon from "@mui/icons-material/Stop";
// import UploadFileIcon from "@mui/icons-material/UploadFile";
// import {
//   Alert,
//   Box,
//   Button,
//   Card,
//   CardContent,
//   Chip,
//   CircularProgress,
//   Fade,
//   Paper,
//   Table,
//   TableBody,
//   TableCell,
//   TableContainer,
//   TableHead,
//   TableRow,
//   Typography
// } from "@mui/material";
// import axios from "axios";
// import { useRef, useState } from "react";
// import { useNavigate } from "react-router-dom";

// function Upload({ setPredictions, setDownloadLink }) {
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");
//   const cancelTokenSource = useRef(null);
//   const navigate = useNavigate();

//   const handleUpload = () => {
//     if (!file) {
//       setError("Please select a file first.");
//       return;
//     }

//     setLoading(true);
//     setResult([]);
//     setError("");

//     const formData = new FormData();
//     formData.append("file", file);

//     cancelTokenSource.current = axios.CancelToken.source();

//     axios
//       .post("http://127.0.0.1:8000/api/predict/", formData, {
//         cancelToken: cancelTokenSource.current.token,
//       })
//       .then((response) => {
//         const { predictions, download_url } = response.data;
//         setResult(predictions);
//         setPredictions(predictions);
//         setDownloadLink(download_url || "");
//         navigate("/results"); // 👉 Redirect to results page
//       })
//       .catch((error) => {
//         if (axios.isCancel(error)) {
//           setError("Upload or Processing cancelled.");
//         } else {
//           console.error("🔴 Server error:", error.response?.data);
//           setError("Upload failed. Please try again.");
//         }
//       })
//       .finally(() => {
//         setLoading(false);
//       });
//   };

//   const handleStop = () => {
//     if (cancelTokenSource.current) {
//       cancelTokenSource.current.cancel();
//       cancelTokenSource.current = null;
//       setLoading(false);
//       setResult([]);
//     }
//   };

//   const getChip = (type) => {
//     if (!type || typeof type !== "string") return <Chip label="Unknown" />;
//     switch (type.toLowerCase()) {
//       case "breast":
//         return <Chip icon={<FemaleIcon />} label="Breast" color="secondary" />;
//       case "ovarian":
//         return <Chip icon={<HealthAndSafetyIcon />} label="Ovarian" color="warning" />;
//       case "prostate":
//         return <Chip icon={<MaleIcon />} label="Prostate" color="primary" />;
//       case "lung":
//         return <Chip icon={<AirIcon />} label="Lung" color="info" />;
//       case "colorectal":
//         return <Chip icon={<HealthAndSafetyIcon />} label="Colorectal" color="success" />;
//       case "kidney":
//         return <Chip icon={<HealthAndSafetyIcon />} label="Kidney" color="default" />;
//       default:
//         return <Chip label={type} />;
//     }
//   };

//   return (
//     <Box mt={5} minHeight="80vh" display="flex" flexDirection="column" alignItems="center" justifyContent="center">
//       <Typography variant="h4" gutterBottom color="textPrimary">
//         <UploadFileIcon sx={{ mr: 1, verticalAlign: "middle" }} />
//         Please Upload Gene Expression CSV
//       </Typography>

//       <Card
//         sx={{
//           p: 3,
//           mb: 3,
//           backgroundColor: "rgba(0, 0, 0, 0.7)",
//           color: "#fff",
//           backdropFilter: "blur(8px)",
//           textAlign: "center",
//           width: "400px",
//           borderRadius: "20px"
//         }}
//       >
//         <CardContent>
//           <input
//             accept=".csv"
//             id="contained-button-file"
//             type="file"
//             style={{ display: "none" }}
//             onChange={(e) => setFile(e.target.files[0])}
//           />
//           <label htmlFor="contained-button-file">
//             <Button
//               variant="outlined"
//               color="secondary"
//               component="span"
//               startIcon={<UploadFileIcon />}
//               sx={{ mb: 2 }}
//               fullWidth
//             >
//               {file ? file.name : "Select CSV File"}
//             </Button>
//           </label>

//           <Button
//             variant="contained"
//             startIcon={!loading && <UploadFileIcon />}
//             onClick={handleUpload}
//             disabled={loading}
//             fullWidth
//             sx={{
//               borderRadius: "30px",
//               transition: "all 0.3s ease",
//               "&:hover": {
//                 transform: "scale(1.05)",
//                 backgroundColor: "#AB3743"
//               }
//             }}
//           >
//             {loading ? (
//               <>
//                 <CircularProgress size={20} sx={{ mr: 1, color: "white" }} />
//                 Uploading...
//               </>
//             ) : "Upload & Predict"}
//           </Button>

//           {loading && (
//             <Button
//               variant="outlined"
//               color="error"
//               startIcon={<StopIcon />}
//               onClick={handleStop}
//               sx={{ mt: 2 }}
//               fullWidth
//             >
//               Stop
//             </Button>
//           )}
//         </CardContent>
//       </Card>

//       {error && (
//         <Alert severity="error" sx={{ mt: 2, width: "60%" }}>
//           {error}
//         </Alert>
//       )}

//       {/* Optional preview below */}
//       {!loading && result.length > 0 && (
//         <Fade in={true}>
//           <Paper sx={{ mt: 5, p: 3, width: "80%", borderRadius: "20px" }}>
//             <Typography variant="h5" gutterBottom>
//               Predictions Preview <CheckCircleIcon color="success" />
//             </Typography>

//             <TableContainer>
//               <Table>
//                 <TableHead>
//                   <TableRow sx={{ backgroundColor: "primary.main" }}>
//                     <TableCell sx={{ color: "white" }}>Sample #</TableCell>
//                     <TableCell sx={{ color: "white" }}>Predicted Subtype</TableCell>
//                     <TableCell sx={{ color: "white" }}>Cancer Type</TableCell>
//                   </TableRow>
//                 </TableHead>
//                 <TableBody>
//                   {result.map((row, index) => (
//                     <TableRow key={index}>
//                       <TableCell>{row.sample}</TableCell>
//                       <TableCell>{row.subtype}</TableCell>
//                       <TableCell>{getChip(row.cancer_type)}</TableCell>
//                     </TableRow>
//                   ))}
//                 </TableBody>
//               </Table>
//             </TableContainer>
//           </Paper>
//         </Fade>
//       )}
//     </Box>
//   );
// }

// export default Upload;


import AirIcon from "@mui/icons-material/Air";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DashboardIcon from '@mui/icons-material/Dashboard';
import FemaleIcon from "@mui/icons-material/Female";
import HealthAndSafetyIcon from "@mui/icons-material/HealthAndSafety";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";
import MaleIcon from "@mui/icons-material/Male";
import StopIcon from "@mui/icons-material/Stop";
import UploadFileIcon from '@mui/icons-material/UploadFile';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Fade,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography
} from "@mui/material";
import axios from "axios";
import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Upload({ setPredictions, setDownloadLink }) {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [uploadProgress, setUploadProgress] = useState(0);
  const cancelTokenSource = useRef(null);
  const navigate = useNavigate();

  const handleUpload = () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setLoading(true);
    setResult([]);
    setError("");
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("file", file);

    cancelTokenSource.current = axios.CancelToken.source();

    axios
      .post("http://127.0.0.1:8000/api/predict/", formData, {
        cancelToken: cancelTokenSource.current.token,
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        }
      })
      .then((response) => {
        const { predictions, download_url, report_url } = response.data;
        setResult(predictions);
        setPredictions(predictions);
        
        // Set download link for basic results
        setDownloadLink({
          basic: download_url || "",
          comprehensive: report_url || "" // This might come from the backend or be generated on the frontend
        });
        
        navigate("/results"); // Redirect to results page
      })
      .catch((error) => {
        if (axios.isCancel(error)) {
          setError("Upload or Processing cancelled.");
        } else {
          console.error("🔴 Server error:", error.response?.data);
          setError("Upload failed. Please try again.");
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const handleStop = () => {
    if (cancelTokenSource.current) {
      cancelTokenSource.current.cancel();
      cancelTokenSource.current = null;
      setLoading(false);
      setResult([]);
      setUploadProgress(0);
    }
  };

  const getChip = (type) => {
    if (!type || typeof type !== "string") return "Unknown";
    
    const icons = {
      breast: <FemaleIcon sx={{ fontSize: 18, color: "#e91e63" }} />,
      ovarian: <HealthAndSafetyIcon sx={{ fontSize: 18, color: "#ff9800" }} />,
      prostate: <MaleIcon sx={{ fontSize: 18, color: "#2196f3" }} />,
      lung: <AirIcon sx={{ fontSize: 18, color: "#03a9f4" }} />,
      colorectal: <HealthAndSafetyIcon sx={{ fontSize: 18, color: "#4caf50" }} />,
      kidney: <HealthAndSafetyIcon sx={{ fontSize: 18, color: "#9e9e9e" }} />
    };
    
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
        {icons[type.toLowerCase()] || null}
        <Typography variant="body2">{type}</Typography>
      </Box>
    );
  };

  return (
    <Box mt={5} minHeight="80vh" display="flex" flexDirection="column" alignItems="center" justifyContent="center">
      <Typography variant="h4" gutterBottom color="textPrimary" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <UploadFileIcon />
        Upload Gene Expression Data
        <Tooltip title="Upload a CSV file containing gene expression data. The file should have samples as rows and genes as columns.">
          <IconButton size="small">
            <HelpOutlineIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Typography>

      <Card
        sx={{
          p: 3,
          mb: 3,
          backgroundColor: "rgba(0, 0, 0, 0.7)",
          color: "#fff",
          backdropFilter: "blur(8px)",
          textAlign: "center",
          width: "400px",
          borderRadius: "20px"
        }}
      >
        <CardContent>
          <input
            accept=".csv"
            id="contained-button-file"
            type="file"
            style={{ display: "none" }}
            onChange={(e) => setFile(e.target.files[0])}
          />
          <label htmlFor="contained-button-file">
            <Button
              variant="outlined"
              color="secondary"
              component="span"
              startIcon={<UploadFileIcon />}
              sx={{ mb: 2 }}
              fullWidth
            >
              {file ? file.name : "Select CSV File"}
            </Button>
          </label>

          {file && (
            <Typography variant="caption" sx={{ display: 'block', mb: 2, color: '#bbb' }}>
              File size: {(file.size / 1024).toFixed(2)} KB
            </Typography>
          )}

          <Button
            variant="contained"
            startIcon={!loading && <UploadFileIcon />}
            onClick={handleUpload}
            disabled={loading}
            fullWidth
            sx={{
              borderRadius: "30px",
              transition: "all 0.3s ease",
              "&:hover": {
                transform: "scale(1.05)",
                backgroundColor: "#AB3743"
              }
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1, color: "white" }} />
                Processing... {uploadProgress}%
              </>
            ) : "Upload & Predict"}
          </Button>

          {loading && (
            <Box sx={{ width: '100%', mt: 2 }}>
              <Box sx={{ position: 'relative', height: '4px', backgroundColor: 'rgba(255,255,255,0.2)', borderRadius: '2px' }}>
                <Box 
                  sx={{ 
                    position: 'absolute', 
                    height: '100%', 
                    backgroundColor: 'white',
                    width: `${uploadProgress}%`,
                    borderRadius: '2px',
                    transition: 'width 0.3s ease'
                  }} 
                />
              </Box>
              
              <Button
                variant="outlined"
                color="error"
                startIcon={<StopIcon />}
                onClick={handleStop}
                sx={{ mt: 2 }}
                size="small"
                fullWidth
              >
                Cancel
              </Button>
            </Box>
          )}

          {file && !loading && (
            <Typography variant="body2" sx={{ mt: 2, color: '#aaa' }}>
              After uploading, you'll receive comprehensive analysis including cancer type prediction, subtype classification, and molecular insights.
            </Typography>
          )}
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mt: 2, width: "60%" }}>
          {error}
        </Alert>
      )}

      {/* Optional preview below */}
      {!loading && result.length > 0 && (
        <Fade in={true}>
          <Paper sx={{ mt: 5, p: 3, width: "80%", borderRadius: "20px" }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" sx={{ display: 'flex', alignItems: 'center' }}>
                <CheckCircleIcon color="success" sx={{ mr: 1 }} /> Predictions Preview
              </Typography>
              
              <Button 
                variant="contained" 
                color="primary" 
                startIcon={<DashboardIcon />}
                onClick={() => navigate('/results')}
                sx={{ 
                  backgroundColor: "#AC1634",
                  '&:hover': {
                    backgroundColor: "#8B0000"
                  }
                }}
              >
                View Full Results
              </Button>
            </Box>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow sx={{ backgroundColor: "#f5f5f5" }}>
                    <TableCell>Sample #</TableCell>
                    <TableCell>Predicted Subtype</TableCell>
                    <TableCell>Cancer Type</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {result.slice(0, 5).map((row, index) => (
                    <TableRow key={index}>
                      <TableCell>{row.sample}</TableCell>
                      <TableCell>{row.subtype}</TableCell>
                      <TableCell>{getChip(row.cancer_type)}</TableCell>
                    </TableRow>
                  ))}
                  {result.length > 5 && (
                    <TableRow>
                      <TableCell colSpan={3} align="center">
                        <Typography variant="body2" color="textSecondary">
                          {result.length - 5} more results available in the full report...
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Fade>
      )}
    </Box>
  );
}

export default Upload;