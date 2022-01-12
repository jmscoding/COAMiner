import "./sidebar.css"
import {LineStyle,Timeline,SettingsApplications,Person} from '@mui/icons-material';
import { Link } from "react-router-dom";

export default function Sidebar(){
    return(
        <div className="sidebar">
            <div className="sidebarWrapper">
                <div className="sidbarMenu">
                    <h3 className="sidebarTitle">Dashboard</h3>
                    <ul className="sidebarList">
                        <li className="sidebarListItem">
                            <LineStyle className="sidebarIcon"/>
                            <Link to={"/"}>Relevant Articles</Link>                         
                        </li>
                        <li className="sidebarListItem">
                            <Timeline className="sidebarIcon"/>
                            <Link to={"/userList"}>Courses of Action</Link>                           
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    )
}