import React, { useState, useEffect } from 'react';
import { Container, Grid, IconButton, Typography, Box, TextField, CircularProgress, Button, Paper, Link } from '@mui/material';
import { ArrowBack, ArrowForward, CloudUpload } from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import mammoth from 'mammoth';
import Lottie from 'react-lottie-player';

// Define the brand colors for the Hong Kong Productivity Council
const primaryColor = '#0072bc'; // Blue
const secondaryColor = '#8dc63f'; // Green

const steps = [
  'Step 1 Input Phase',
  'Step 2 Preview',
  'Step 3 Deploy'
];
const stepMessages = [
  'Welcome to Step 1: Please upload your document.',
  'Welcome to Step 2: Please review.',
  'Welcome to Step 3: Please finalize and submit your document.'
];
const waitingMessages = [
  'Analysing...',
  'Personalization...',
  'Reducing Bias...',
  'Just wait...'
];

// AI-related Lottie animation URL
const animationUrl = 'https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json'; // Replace with the new AI character animation URL

const SurveyBuilder = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [wordContent, setWordContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [animationData, setAnimationData] = useState(null);
  const [backendResponse, setBackendResponse] = useState('');
  const [currentDir, setCurrentDir] = useState(''); // Save current_dir
  const [deploymentUrl, setDeploymentUrl] = useState(''); // Save deployment URL
  const [waitingMessageIndex, setWaitingMessageIndex] = useState(0);
  const [customMessage, setCustomMessage] = useState(stepMessages[0]);
  const [tempBackendResponse, setTempBackendResponse] = useState(''); // Temporarily store backend returned Markdown content
  const [contentModified, setContentModified] = useState(false); // Track if document content has been modified

  useEffect(() => {
    // Fetch the animation data once when the component mounts
    const fetchAnimationData = async () => {
      try {
        const response = await fetch(animationUrl);
        const data = await response.json();
        setAnimationData(data);
      } catch (error) {
        console.error('Error fetching animation data:', error);
      }
    };

    fetchAnimationData();
  }, []);

  useEffect(() => {
    if (activeStep === 1) {
      // Set waiting messages
      const interval = setInterval(() => {
        setWaitingMessageIndex((prevIndex) => (prevIndex + 1) % waitingMessages.length);
      }, 2000);

      return () => clearInterval(interval);
    }
  }, [activeStep]);

  useEffect(() => {
    if (!loading && activeStep === 1) {
      setBackendResponse(tempBackendResponse); // Update backend returned Markdown content
    }
  }, [loading, activeStep, tempBackendResponse]);

  const fetchWithTimeout = async (url, options, timeout = 300000) => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  };

  const sendDataToBackend = async () => {
    setLoading(true);
    try {
      const response = await fetchWithTimeout('/generate_preview', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: wordContent })
      }, 300000); // Set timeout to 5 minutes
      const data = await response.json();
      console.log('Backend response:', data); // Debug information
      setTempBackendResponse(data.preview_content); // Temporarily store backend returned Markdown content
      setCurrentDir(data.current_dir); // Save current_dir
    } catch (error) {
      console.error('Error sending data to backend:', error);
      setError('The number of people asking for my help right now is too many. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (activeStep === 0) {
      if (contentModified) {
        // Send request to the backend on clicking next in step one

        sendDataToBackend();
      } else {
        setBackendResponse(tempBackendResponse); // Use previously stored result
      }
    }

    setActiveStep((prevActiveStep) => {
      const nextStep = prevActiveStep + 1;
      setCustomMessage(stepMessages[nextStep]);
      return nextStep;
    });

    // Reset modification flag
    setContentModified(false);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => {
      const prevStep = activeStep === 2 ? 0 : prevActiveStep - 1;
      setCustomMessage(stepMessages[prevStep]);
      return prevStep;
    });
  };

  const handleRetry = () => {
    setError('');
    if(activeStep === 2){
      sendCurrentDirToBackend();
    }else{
      sendDataToBackend();
    }
  };

  const sendCurrentDirToBackend = async () => {
    setLoading(true);
    setCustomMessage('Deploying...');
    try {
      const response = await fetchWithTimeout('/deploy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ current_dir: currentDir })
      }, 300000); // Set timeout to 5 minutes
      const data = await response.json();
      setDeploymentUrl(data.address); // Assume the backend returns the URL in data.address
      setCustomMessage('The survey has been created and deployed. You can access it by clicking the link. \
        If you are not satisfied with the results, you can click the Back button to modify your input and regenerate the survey.\
        ');
      setError('just to retry')
    } catch (error) {
      console.error('Error sending current_dir to backend:', error);
      setError('The number of people asking for my help right now is too many. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeStep === 2) {
      sendCurrentDirToBackend();
    }
  }, [activeStep, currentDir]);

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      setError('');
      mammoth.extractRawText({ arrayBuffer: file })
        .then((result) => {
          setWordContent(result.value);
          setLoading(false);
          setCustomMessage('You can edit the document content. Once confirmed, click next to analyze and generate the survey.');
          setContentModified(true); // Mark content as modified
        })
        .catch((err) => {
          setError('Failed to read file');
          setLoading(false);
        });
    }
  };

  const handleContentChange = (event) => {
    setWordContent(event.target.value);
    setContentModified(true); // Mark content as modified
  };

  return (
    <Container style={{ position: 'relative', minHeight: '100vh', overflow: 'hidden', paddingTop: '20px', background: '#f0f0f0' }}>
      <Typography variant="h4" align="center" gutterBottom style={{ marginBottom: '20px', color: primaryColor }}>
        Survey Creation Tasks and Analysis Using AI Agents
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={3}>
          <Box>
            {steps.map((label, index) => (
              <Paper
                key={label}
                elevation={3}
                style={{
                  padding: '10px',
                  marginBottom: '10px',
                  borderRadius: '10px',
                  border: `1px solid ${primaryColor}`,
                  backgroundColor: activeStep === index ? secondaryColor : 'white',
                }}
              >
                <Typography>{label}</Typography>
              </Paper>
            ))}
            <Box mt={2} display="flex" flexDirection="column" alignItems="center">
              {animationData && (
                <Lottie
                  loop
                  play
                  animationData={animationData}
                  style={{ width: 150, height: 150 }}
                />
              )}
              <Typography variant="body1" align="center" style={{ marginTop: '10px', color: primaryColor }}>
                {activeStep === 1 && loading
                  ? waitingMessages[waitingMessageIndex]
                  : activeStep === 2 && deploymentUrl
                  ? 'The survey has been created and deployed. You can access it by clicking the link. \
        If you are not satisfied with the results, you can click the Back button to modify your input and regenerate the survey.\
        '
                  : error
                  ? error
                  : customMessage}
              </Typography>
              {error && (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleRetry}
                  style={{ marginTop: '10px', backgroundColor: primaryColor }}
                >
                  Retry
                </Button>
              )}
            </Box>
          </Box>
        </Grid>
        <Grid item xs={9}>
          {activeStep === 0 && (
            <Box bgcolor="white" p={2} borderRadius={2} mb={2} boxShadow={3} border={`1px solid ${primaryColor}`} display="flex" alignItems="center">
              <IconButton component="label" style={{ color: primaryColor }}>
                <CloudUpload />
                <input type="file" hidden onChange={handleUpload} />
              </IconButton>
              <Typography variant="body1" style={{ marginLeft: '10px', color: primaryColor }}>
                Click to upload the original document (word)
              </Typography>
              {loading && activeStep === 0 && <CircularProgress size={24} style={{ color: primaryColor, marginLeft: '10px' }} />}
            </Box>
          )}
          <Grid container spacing={2}>
            {activeStep === 0 && (
              <Grid item xs={6}>
                <Typography variant="h6" style={{ marginBottom: '10px', color: primaryColor }}>
                  Original Document
                </Typography>
                <Box bgcolor="white" p={2} borderRadius={2} height="400px" overflow="auto" boxShadow={3} border={`1px solid ${primaryColor}`} mb={2}>
                  <TextField
                    multiline
                    fullWidth
                    variant="outlined"
                    value={wordContent}
                    onChange={handleContentChange}
                    placeholder="Edit the content here"
                    style={{ height: '100%' }}
                    InputProps={{ style: { color: '#000' } }}
                  />
                </Box>
              </Grid>
            )}
            {activeStep === 0 && (
              <Grid item xs={6}>
                <Typography variant="h6" style={{ marginBottom: '10px', color: primaryColor }}>
                  Markdown (Live)
                </Typography>
                <Box bgcolor="white" p={2} borderRadius={2} height="400px" overflow="auto" boxShadow={3} border={`1px solid ${primaryColor}`} mb={2}>
                  <ReactMarkdown>{wordContent}</ReactMarkdown>
                </Box>
              </Grid>
            )}
            {activeStep === 1 && (
              <Grid item xs={12}>
                <Typography variant="h6" style={{ marginBottom: '10px', color: primaryColor }}>
                  {loading ? 'Loading Preview...' : 'Markdown (Live)'}
                </Typography>
                <Box bgcolor="white" p={2} borderRadius={2} height="400px" overflow="auto" boxShadow={3} border={`1px solid ${primaryColor}`} mb={2}>
                  {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                      <CircularProgress size={48} style={{ color: primaryColor }} />
                    </Box>
                  ) : (
                    <ReactMarkdown>{backendResponse}</ReactMarkdown>
                  )}
                </Box>
              </Grid>
            )}
            {activeStep === 2 && (
              <Grid item xs={12}>
                <Typography variant="h6" style={{ marginBottom: '10px', color: primaryColor }}>
                  Deployment Result
                </Typography>
                <Box bgcolor="white" p={2} borderRadius={2} height="400px" overflow="auto" boxShadow={3} border={`1px solid ${primaryColor}`} mb={2}>
                  {deploymentUrl ? (
                    <>
                      <Link href={deploymentUrl} target="_blank" rel="noopener noreferrer">
                        {deploymentUrl}
                      </Link>
                      <iframe src={deploymentUrl} title="Deployment Result" style={{ width: '100%', height: '100%', border: 'none', marginTop: '10px' }} />
                    </>
                  ) : (
                    <Box display="flex" justifyContent="center" alignItems="center" height="100%">
                      <Typography variant="body1" align="center" style={{ color: primaryColor }}>
                        Generating...
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Grid>
            )}
          </Grid>
          <Box mt={2} display="flex" justifyContent="center">
            {activeStep > 0 && (
              <Button
                variant="contained"
                color="primary"
                onClick={handleBack}
                disabled={loading}
                startIcon={<ArrowBack />}
                style={{ marginRight: '10px', backgroundColor: primaryColor }}
              >
                Back
              </Button>
            )}
            {activeStep < 2 && (
              <Button
                variant="contained"
                color="primary"
                onClick={handleNext}
                endIcon={<ArrowForward />}
                style={{ backgroundColor: primaryColor }}
                disabled={(activeStep === 1 && loading) || (activeStep === 2)}
              >
                Next
              </Button>
            )}
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default SurveyBuilder;