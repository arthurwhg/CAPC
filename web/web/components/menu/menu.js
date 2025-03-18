import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import HelpIcon from '@mui/icons-material/Help';
import PsychologyAltIcon from '@mui/icons-material/PsychologyAlt';
import OndemandVideoIcon from '@mui/icons-material/OndemandVideo';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import BookIcon from '@mui/icons-material/Book';


export const menu1 = [
    {
        title: 'Home', 
        icon: ()=><PeopleAltIcon/>,
        action: '/' 
    },
    {
        title: 'Help on prayer', 
        icon: ()=><PeopleAltIcon/>,
        action: '/prayer' 
    },
    {
        title:'Q&A',
        icon: ()=><PsychologyAltIcon/>,
        action: '/qa'
    },
    {
        title: 'Videos',
        icon: ()=><OndemandVideoIcon/>,
        action: ''
    },
    {
        title: 'Books',
        icon: ()=><BookIcon/>,
        action: ''
    }];

export const menu2 = [
        {
            title: 'Update Topics',
            icon: ()=><HelpIcon/>,
            action: ''
        },
        {
            title: 'Update Videos', 
            icon: ()=><OndemandVideoIcon/>,
            action: ''
        },
        {
            title: 'Update Books',
            icon: ()=><BookIcon/>,
            action: ''
        },
    ];