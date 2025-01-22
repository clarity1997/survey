import React, { useState } from 'react';
import { Button, Box } from '@mui/material';
import { styled } from '@mui/system';
import SurveyBuilder from './SurveyBuilder'; // 确保路径正确

const App = () => {
  const [showComponent, setShowComponent] = useState(false);

  const handleButtonClick = () => {
    setShowComponent(true);
  };

  return (
    <>
      {!showComponent ? (
        <StyledBackground>
          <StyledContainer>
            <Box textAlign="center">
              <StyledImage src="/fronted/intro.png" alt="Central" />
              <Box mt={2}>
                <StyledButton onClick={handleButtonClick}>
                  探索更多
                </StyledButton>
              </Box>
            </Box>
          </StyledContainer>
        </StyledBackground>
      ) : (
          <SurveyBuilder />
      )}
    </>
  );
};

const StyledBackground = styled(Box)({
  width: '100vw',
  height: '100vh',
  background: 'linear-gradient(135deg, #0070c0, #00b050)', // 假设的 HKPC 蓝色和绿色
  backgroundSize: '400% 400%',
  animation: 'GradientAnimation 6s ease infinite',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  '@keyframes GradientAnimation': {
    '0%': { backgroundPosition: '0% 50%' },
    '50%': { backgroundPosition: '100% 50%' },
    '100%': { backgroundPosition: '0% 50%' },
  },
});

const StyledContainer = styled(Box)({
  textAlign: 'center',
  fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
  color: '#ffffff',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
  background: 'rgba(0, 0, 0, 0.5)', // Optional: Adds a dark overlay for better text visibility
  padding: '20px',
  borderRadius: '10px',
});

const StyledImage = styled('img')({
  width: '75vw', // 占据视图宽度的 75%
  height: '75vh', // 占据视图高度的 75%
  objectFit: 'contain', // 保持图片的纵横比
  borderRadius: '10px',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
});

const StyledButton = styled(Button)({
  fontSize: '16px',
  padding: '10px 20px',
  borderRadius: '25px',
  background: 'linear-gradient(135deg, #0070c0, #00b050)', // 假设的 HKPC 蓝色和绿色
  color: '#ffffff',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
  '&:hover': {
    background: 'linear-gradient(135deg, #005a9e, #008a3e)', // 假设的 HKPC 深蓝色和深绿色
    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.3)',
  },
});

const PlainBackground = styled(Box)({
  width: '100vw',
  height: '100vh',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  background: '#ffffff', // 或者你想要的任何其他背景颜色
});

export default App;