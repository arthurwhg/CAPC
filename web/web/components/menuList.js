import { ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material"
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import Button from "@mui/material";

const MenuList = ({ menuitems, open }) => {

  const onclick = (action) => {
    console.log(typeof(action));
    if (typeof(action) === 'function') {
        console.log("action is a function");
        action()}
    else if (typeof(action) === 'string') {
        console.log("action is an URL")
        window.location.replace(action);
    }
  }  
  return (
    <>
        {  menuitems.map((item, index) => (
            <ListItem key={item.title} disablePadding sx={{ display: 'block' }}>
                <ListItemButton
                    sx={{
                        minHeight: 48,
                        justifyContent: open ? 'initial' : 'center',
                        px: 2.5,
                    }}
                >
                    <ListItemIcon
                        sx={{
                            minWidth: 0,
                            mr: open ? 3 : 'auto',
                            justifyContent: 'center',
                        }}
                    >
                        {item.icon && item.icon()}
                    </ListItemIcon>
                    <ListItemText primary={item.title} onClick={() => onclick(item.action)} sx={{ opacity: open ? 1 : 0 }} />
                </ListItemButton>
            </ListItem>
            ))
        }
    </>
  );
};
//<ListItemText primary={item.title} sx={{ opacity: open ? 1 : 0 }} />
export default MenuList;