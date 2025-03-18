import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import HelpIcon from "@mui/icons-material/Help";
import PsychologyIcon from "@mui/icons-material/Psychology"; // ✅ Fix import name
import OndemandVideoIcon from "@mui/icons-material/OndemandVideo";
import AutoStoriesIcon from "@mui/icons-material/AutoStories";
import BookIcon from "@mui/icons-material/Book";
import {menu1, menu2} from "../../components/menu/menu";
import Button from '@mui/material/Button';
import {useEffect, useState } from "react";
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
// import TabPanel from "@mui/lab/TabPanel";   // ✅ Fix import name
// import TabContext from "@mui/lab/TabContext"; // ✅ Fix import name
import Layout from "../../components/layout/layout";


const open = false;
const Index = () => {

    const [box2, setBox2] = useState(true);
    const [question, setQuestion] = useState('ask a question');
    const [response, setResponse] = useState('how to response');
    const [showQuestion, setShowQuestion] = useState(false);

    // tab conrol
    const [tabValue, setTabValue] = useState('1');

    const handleTabChange = (event, newValue) => {
      setTabValue(newValue); 
      if (newValue === '1') {
        setShowQuestion(true);
      }
    };

    const show_queston= () => {
            return(
            <>
                {showQuestion && <Box sx={{ display: 'flex', flexDirection: 'row', p: 2 }}>
                        <TextField 
                        id="question" 
                        label="question" 
                        variant="outlined" 
                        value={question}
                        size="small" 
                        inputProps={{ maxLength: 20 }}
                        onChange={(e)=>setQuestion(e.target.value)} 
                        fullWidth />
                        <Button variant="contained" type="submit" onClick={()=>handlesubmit()}>Submit</Button>
                </Box>}
            </>
            )
    }

    const show_tabs = () => {
        return(
            <Box sx={{ width: '100%', typography: 'body1' }}>
                <Tabs value={tabValue} onChange={handleTabChange}>
                    <Tab value="1" label="Prayer"></Tab>
                    <Tab value="2" label="Assistant"></Tab>
                </Tabs>
            </Box>
        )
    }

    const handlesubmit = () => {
        setBox2(true);
    }

    return (
        <Layout title={"Question & Answer"} open={open} menu1={menu1} menu2={menu2} >
            {show_tabs()}
            {show_queston()}
            <Box>
                {tabValue === '1' && <Typography>Item One</Typography>}
                {tabValue === '2' && <Typography>Item Two</Typography>}
                {tabValue === '3' && <Typography>Item Three</Typography>}
            </Box>
        </Layout>
    );
};

export default Index;