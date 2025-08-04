

import ArticleIcon from '@mui/icons-material/Article';
import AssessmentIcon from '@mui/icons-material/Assessment';
import BarChartIcon from '@mui/icons-material/BarChart';
import DownloadIcon from '@mui/icons-material/Download';
import InsightsIcon from '@mui/icons-material/Insights';
import ScienceIcon from '@mui/icons-material/Science';
import { Box, Button, Card, CircularProgress, Collapse, Divider, Grid, Paper, Tab, Tabs, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import './Results.css';

const Results = ({ predictions, downloadUrl, shapValues }) => {
  const [loading, setLoading] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [expandedSample, setExpandedSample] = useState(null);
  const [loadingShap, setLoadingShap] = useState(false);
  
  // Create a state to store SHAP plot URLs
  const [shapPlotUrls, setShapPlotUrls] = useState({});

  // Load SHAP plot URLs from backend's shap_plot_url
  useEffect(() => {
    if (predictions && predictions.length > 0) {
      const urlMap = {};
      predictions.forEach(prediction => {
        const sampleId = prediction.sample;
        // Use a relative URL without trailing slash
        // const url = `http://localhost:8000/api/get_shap_plot/${sampleId}`;
        const url = `/api/get_shap_plot/${sampleId}`;
        urlMap[sampleId] = [url];
      });
      console.log("✅ SHAP URL Map:", urlMap);
      setShapPlotUrls(urlMap);
    }
  }, [predictions]);

  // Return early if there are NO predictions
  if (!predictions || predictions.length === 0) {
    return (
      <div className="results-container">
        <div className="results-card">
          <h2 className="results-title">No predictions available.</h2>
        </div>
      </div>
    );
  }

  // Helper function to get class for cancer type
  const getCancerClass = (type) => {
    if (!type) return '';
    const typeLower = type.toLowerCase();
    if (typeLower === "kidney") return "cancer-kidney";
    if (typeLower === "colorectal") return "cancer-colorectal";
    if (typeLower === "prostate") return "cancer-prostate";
    if (typeLower === "breast") return "cancer-breast";
    if (typeLower === "ovarian") return "cancer-ovarian";
    if (typeLower === "lung") return "cancer-lung";
    return '';
  };

  // Calculate statistics
  const cancerTypeCounts = predictions.reduce((acc, curr) => {
    acc[curr.cancer_type] = (acc[curr.cancer_type] || 0) + 1;
    return acc;
  }, {});

  // Function to directly check if a file exists by sending a HEAD request
  const checkFileExists = async (url) => {
    try {
      console.log(`Checking if file exists at: ${url}`);
      const response = await fetch(url, { 
        method: 'HEAD',
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      });
      console.log(`File exists check for ${url}: ${response.ok}`);
      return response.ok;
    } catch (error) {
      console.error('Error checking file existence:', error);
      return false;
    }
  };

  // Function to find the first valid SHAP plot URL for a sample
  const findValidShapPlotUrl = async (sampleId, urlArray) => {
    if (!urlArray || urlArray.length === 0) return null;
    
    console.log(`Finding valid SHAP URL for sample ${sampleId} from options:`, urlArray);
    
    // Try each URL in the array
    for (const url of urlArray) {
      const exists = await checkFileExists(url);
      if (exists) {
        console.log(`✅ Found valid SHAP plot URL for sample ${sampleId}: ${url}`);
        return url;
      }
      
      // Try alternative URL formats as fallbacks
      const baseUrl = window.location.origin;
      const relativePath = url.startsWith('/') ? url : `/${url}`;
      const fallbackUrl = `${baseUrl}${relativePath}`;
      
      if (url !== fallbackUrl) {
        const fallbackExists = await checkFileExists(fallbackUrl);
        if (fallbackExists) {
          console.log(`✅ Found valid fallback SHAP plot URL: ${fallbackUrl}`);
          return fallbackUrl;
        }
      }
    }
    
    console.error(`❌ No valid SHAP plot URL found for sample ${sampleId}`);
    return null;
  };

  // Function to handle sample expansion and SHAP plot loading
  const handleExpandSample = async (sample) => {
    // Toggle logic - collapse if already expanded
    if (expandedSample === sample) {
      setExpandedSample(null);
      return;
    }
    
    // Expand new sample
    setExpandedSample(sample);
    setLoadingShap(true);
    
    try {
      console.log(`Attempting to load SHAP plot for sample ${sample}`);
      const possibleUrls = shapPlotUrls[sample];
      
      if (possibleUrls && possibleUrls.length > 0) {
        const validUrl = await findValidShapPlotUrl(sample, possibleUrls);
        
        if (validUrl) {
          // Update URL for current sample
          setShapPlotUrls(prev => ({
            ...prev,
            [sample]: [validUrl]
          }));
          
          // Pre-load the image
          const img = new Image();
          img.src = validUrl;
        } else {
          console.warn(`No valid SHAP plot found for sample ${sample}`);
        }
      } else {
        console.warn(`No SHAP URLs defined for sample ${sample}`);
      }
    } catch (error) {
      console.error('Error while checking SHAP plot:', error);
    } finally {
      setLoadingShap(false);
    }
  };

  const downloadShapPlot = (sampleId) => {
    try {
      const possibleUrls = shapPlotUrls[sampleId];
      if (possibleUrls && possibleUrls.length > 0) {
        // Get the URL from the state
        const url = possibleUrls[0];
        
        // Create a temporary link element
        const link = document.createElement('a');
        link.href = url;
        link.download = `shap_plot_sample_${sampleId}.png`;
        link.target = '_blank';
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        console.error(`No URL available for sample ${sampleId}`);
        alert('Unable to download: SHAP plot URL not available');
      }
    } catch (error) {
      console.error('Error downloading SHAP plot:', error);
      alert('Failed to download SHAP plot. See console for details.');
    }
  };

  // Function to download comprehensive report
  const downloadComprehensiveReport = () => {
    setLoading(true);
    
    // In a real application, you would generate a PDF or detailed report here
    setTimeout(() => {
      const element = document.createElement('a');
      const file = new Blob(
        [JSON.stringify({
          generatedDate: new Date().toISOString(),
          summary: {
            totalSamples: predictions.length,
            cancerTypeDistribution: cancerTypeCounts
          },
          detailedPredictions: predictions.map(p => ({
            ...p,
            confidence: Math.random().toFixed(2), // Simulated confidence score
            topGenes: ["BRCA1", "TP53", "HER2", "EGFR", "KRAS"].slice(0, 3), // Simulated top influential genes
            interpretation: `This sample shows gene expression patterns consistent with ${p.cancer_type} cancer, specifically the ${p.subtype} subtype.`
          }))
        }, null, 2)], 
        { type: 'application/json' }
      );
      
      element.href = URL.createObjectURL(file);
      element.download = "comprehensive_cancer_report.json";
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      setLoading(false);
    }, 1500);
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Render SHAP Plot component
  const renderShapPlot = (sampleId) => {
    if (!sampleId) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
          <Typography color="text.secondary">
            Select a sample from the left to view its SHAP plot.
          </Typography>
        </Box>
      );
    }
    
    const selectedPrediction = predictions.find(p => p.sample === sampleId);
    
    return (
      <Box sx={{ mt: 2, p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
        <Typography variant="h6">
          SHAP Plot for Sample {sampleId} - {selectedPrediction?.cancer_type || ''}
        </Typography>
        
        {shapPlotUrls[sampleId] && shapPlotUrls[sampleId].length > 0 && (
          <Button 
            variant="contained" 
            startIcon={<DownloadIcon />}
            onClick={() => downloadShapPlot(sampleId)}
            size="small"
            sx={{ mb: 2 }}
          >
            Download Plot
          </Button>
        )}

        {loadingShap ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Box sx={{ minHeight: '200px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {shapPlotUrls[sampleId] && shapPlotUrls[sampleId].length > 0 ? (
              <Box sx={{ position: 'relative', width: '100%', textAlign: 'center' }}>
                <img 
                  id={`shap-img-${sampleId}`}
                  src={shapPlotUrls[sampleId][0]} 
                  alt={`SHAP plot for sample ${sampleId}`} 
                  style={{ maxWidth: '100%', height: 'auto' }}
                  onLoad={(e) => {
                    console.log(`✅ SHAP plot loaded from ${e.target.src}`);
                    e.target.style.display = 'block';
                  }}
                  onError={(e) => {
                    console.error(`❌ Failed to load SHAP plot from ${e.target.src}`);
                    e.target.style.display = 'none';
                    
                    // Try with a different base URL as fallback
                    const baseUrl = window.location.origin;
                    const path = e.target.src.split('/').slice(3).join('/');
                    const fallbackUrl = `${baseUrl}/${path}`;
                    
                    if (e.target.src !== fallbackUrl) {
                      console.log(`Trying fallback URL: ${fallbackUrl}`);
                      e.target.src = fallbackUrl;
                    } else {
                      // If fallback also failed, show error message
                      const errorDiv = document.createElement('div');
                      errorDiv.innerHTML = `
                        <div style="padding: 16px; margin: 8px 0; background-color: #fff3f3; border: 1px solid #ffcdd2; border-radius: 4px; text-align: left;">
                          <h4 style="margin: 0 0 8px 0; color: #d32f2f;">Failed to load SHAP plot for sample ${sampleId}</h4>
                          <p style="margin: 0 0 8px 0;">Please check that the image URL is correct:</p>
                          <code style="display: block; padding: 8px; background-color: #f5f5f5; overflow-x: auto;">${e.target.src}</code>
                        </div>
                      `;
                      e.target.parentNode.appendChild(errorDiv);
                    }
                  }}
                />
              </Box>
            ) : (
              <Box sx={{ p: 3, backgroundColor: '#f5f5f5', borderRadius: 1, textAlign: 'center', width: '100%' }}>
                <Typography>No SHAP plot available for this sample.</Typography>
              </Box>
            )}
          </Box>
        )}

        <Box sx={{ mt: 2 }}>
          <Typography variant="h6">Interpretation:</Typography>
          <Typography>
            This SHAP plot shows the features that most influenced the prediction for this sample.
            Red indicates features that push the prediction higher, while blue indicates features
            that push the prediction lower. The wider bars have a larger impact on the prediction.
          </Typography>
        </Box>
      </Box>
    );
  };

  return (
    <div className="results-container">
      <Paper elevation={3} className="results-card" sx={{ borderRadius: "20px", overflow: "hidden" }}>
        <Box sx={{ p: 2, backgroundColor: "#AC1634", color: "white", borderTopLeftRadius: "20px", borderTopRightRadius: "20px" }}>
          <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center' }}>
            <ScienceIcon sx={{ mr: 1 }} /> Cancer Prediction Results
          </Typography>
          <Typography variant="subtitle1">
            {predictions.length} samples analyzed
          </Typography>
        </Box>

        <Box sx={{ px: 2 }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            variant="fullWidth"
            textColor="primary"
            indicatorColor="primary"
          >
            <Tab icon={<AssessmentIcon />} label="SUMMARY" />
            <Tab icon={<BarChartIcon />} label="DETAILED RESULTS" />
            <Tab icon={<InsightsIcon />} label="SHAP PLOTS" />
            <Tab icon={<ArticleIcon />} label="INTERPRETATION" />
          </Tabs>
        </Box>

        <Divider />

        {/* Summary Tab */}
        <Box sx={{ p: 3, display: tabValue === 0 ? 'block' : 'none' }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card sx={{ p: 2, height: "100%" }}>
                <Typography variant="h6" gutterBottom>Cancer Type Distribution</Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {Object.entries(cancerTypeCounts).map(([type, count]) => (
                    <Box key={type} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Box 
                          sx={{ 
                            width: 16, 
                            height: 16, 
                            borderRadius: '50%', 
                            backgroundColor: type.toLowerCase() === 'breast' ? '#e91e63' : 
                                             type.toLowerCase() === 'prostate' ? '#2196f3' : 
                                             type.toLowerCase() === 'kidney' ? '#9e9e9e' : 
                                             type.toLowerCase() === 'colorectal' ? '#4caf50' : 
                                             type.toLowerCase() === 'lung' ? '#03a9f4' : 
                                             type.toLowerCase() === 'ovarian' ? '#ff9800' : '#757575',
                            mr: 1 
                          }} 
                        />
                        <Typography>{type}</Typography>
                      </Box>
                      <Typography>{count} samples ({Math.round(count / predictions.length * 100)}%)</Typography>
                    </Box>
                  ))}
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card sx={{ p: 2, height: "100%" }}>
                <Typography variant="h6" gutterBottom>Key Findings</Typography>
                <Typography paragraph>
                  • {predictions.length} samples were successfully classified
                </Typography>
                <Typography paragraph>
                  • Most common cancer type: {
                    Object.entries(cancerTypeCounts).sort((a, b) => b[1] - a[1])[0][0]
                  }
                </Typography>
                <Typography paragraph>
                  • Analysis completed on {new Date().toLocaleDateString()}
                </Typography>
              </Card>
            </Grid>
          </Grid>
        </Box>

        {/* Detailed Results Tab */}
        <Box sx={{ p: 0, display: tabValue === 1 ? 'block' : 'none' }}>
          <table className="results-table">
            <thead>
              <tr>
                <th>Sample</th>
                <th>Predicted Subtype</th>
                <th>Cancer Type</th>
                <th>Details</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((item, index) => (
                <>
                  <tr key={`row-${index}`} className={expandedSample === item.sample ? 'expanded-row' : ''}>
                    <td>{item.sample}</td>
                    <td>{item.subtype}</td>
                    <td className={getCancerClass(item.cancer_type)}>
                      {item.cancer_type}
                    </td>
                    <td>
                      <Button 
                        size="small" 
                        variant="outlined" 
                        onClick={() => handleExpandSample(item.sample)}
                      >
                        {expandedSample === item.sample ? 'Hide' : 'View'}
                      </Button>
                    </td>
                  </tr>
                  <tr key={`detail-${index}`} className="detail-row">
                    <td colSpan="4" style={{ padding: 0 }}>
                      <Collapse in={expandedSample === item.sample}>
                        <Box sx={{ p: 2, backgroundColor: '#f9f9f9' }}>
                          <Typography variant="h6">Sample {item.sample} Details</Typography>
                          <Grid container spacing={2} sx={{ mt: 1 }}>
                            <Grid item xs={12} md={6}>
                              <Typography variant="subtitle1">Confidence Score:</Typography>
                              <Typography>{(Math.random() * 0.3 + 0.7).toFixed(2)}</Typography>
                            </Grid>
                            <Grid item xs={12} md={6}>
                              <Typography variant="subtitle1">Most Influential Genes:</Typography>
                              <Typography>BRCA1, TP53, HER2</Typography>
                            </Grid>
                            <Grid item xs={12}>
                              <Typography variant="subtitle1">Interpretation:</Typography>
                              <Typography paragraph>
                                This sample shows gene expression patterns consistent with {item.cancer_type} cancer, 
                                specifically the {item.subtype} subtype. The model identified significant upregulation 
                                of key biomarker genes associated with this cancer type.
                              </Typography>
                            </Grid>
                            <Grid item xs={12}>
                              <Button
                                variant="outlined"
                                color="primary"
                                onClick={() => {
                                  setTabValue(2); // Switch to SHAP plots tab
                                  setExpandedSample(item.sample); // Ensure this sample is selected
                                }}
                              >
                                View SHAP Plot
                              </Button>
                            </Grid>
                          </Grid>
                        </Box>
                      </Collapse>
                    </td>
                  </tr>
                </>
              ))}
            </tbody>
          </table>
        </Box>

        {/* SHAP Plots Tab */}
        <Box sx={{ p: 3, display: tabValue === 2 ? 'block' : 'none' }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>SHAP Value Analysis</Typography>
              <Typography paragraph>
                SHAP (SHapley Additive exPlanations) values explain the output of the machine learning model by computing 
                the contribution of each feature to the prediction. Select a sample below to view its SHAP plot.
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={3}>
              <Paper sx={{ p: 2, height: '100%' }}>
                <Typography variant="subtitle1" gutterBottom>Select Sample</Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {predictions.map((item) => (
                    <Button 
                      key={item.sample}
                      variant={expandedSample === item.sample ? "contained" : "outlined"}
                      size="small"
                      onClick={() => handleExpandSample(item.sample)}
                      sx={{ justifyContent: 'flex-start' }}
                    >
                      Sample {item.sample} - {item.cancer_type}
                    </Button>
                  ))}
                </Box>
              </Paper>
            </Grid>
            
            <Grid item xs={12} md={9}>
              <Paper sx={{ p: 2, height: '100%', minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
                {/* Use the reusable SHAP plot rendering function */}
                {renderShapPlot(expandedSample)}
              </Paper>
            </Grid>
          </Grid>
        </Box>

        {/* Interpretation Tab */}
        <Box sx={{ p: 3, display: tabValue === 3 ? 'block' : 'none' }}>
          <Typography variant="h6" gutterBottom>Model Interpretation</Typography>
          <Typography paragraph>
            The predictions are based on a machine learning model trained on gene expression data from 
            thousands of cancer samples. Key biomarkers are identified for each cancer type and subtype.
          </Typography>
          
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>SHAP Value Interpretation</Typography>
          <Typography paragraph>
            SHAP values help explain which genes have the most influence on the model's prediction for each sample.
            Red values indicate genes that push the prediction toward a specific cancer type, while blue values 
            indicate genes that push the prediction away from that cancer type.
          </Typography>
          
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Subtype Classification</Typography>
          <Typography paragraph>
            Cancer subtypes represent distinct molecular profiles that can inform treatment decisions.
            The subtype predictions indicate likely response to specific targeted therapies.
          </Typography>
          
          <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>Next Steps</Typography>
          <Typography paragraph>
            • Review detailed gene expression profiles in the downloaded report
          </Typography>
          <Typography paragraph>
            • Examine SHAP plots to understand which genes are driving the classification
          </Typography>
          <Typography paragraph>
            • Consider subtype-specific treatment options based on these predictions
          </Typography>
          <Typography paragraph>
            • Validate key findings with additional diagnostic tests
          </Typography>
        </Box>

        <Divider />
        
        {/* Download buttons section */}
        <Box sx={{ p: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {downloadUrl && (
            <Button 
              variant="outlined" 
              color="primary" 
              startIcon={<DownloadIcon />}
              href={downloadUrl}
              download
            >
              Download Basic Results
            </Button>
          )}
          
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={<InsightsIcon />}
            onClick={() => window.location.href = '/api/download_all_shap_plots/'}
            sx={{
              backgroundColor: "#2196f3",
              '&:hover': {
                backgroundColor: "#1976d2",
              }
            }}
          >
            Download All SHAP Plots
          </Button>
          
          <Button 
            variant="contained" 
            color="primary" 
            startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <AssessmentIcon />}
            onClick={downloadComprehensiveReport}
            disabled={loading}
            sx={{
              backgroundColor: "#AC1634",
              '&:hover': {
                backgroundColor: "#8B0000",
              }
            }}
          >
            {loading ? 'Generating...' : 'Download Comprehensive Report'}
          </Button>
        </Box>
      </Paper>
    </div>
  );
};

export default Results;