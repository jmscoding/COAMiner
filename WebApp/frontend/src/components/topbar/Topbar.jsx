import React from 'react'
import "./topbar.css"
import {NotificationsNone, Language, Settings, AccountCircle} from '@mui/icons-material';

export default function Topbar() {
    return (
        <div className="topbar">
            <div className="topbarWrapper">
                <div className="topLeft">
                    <span className="logo">CoAMiner</span>
                </div>    
                {/*<div className="topRight">
                    <div className="topbarIconContainer">
                        <NotificationsNone />
                        <span className="topIconBadge">2</span>
                    </div>
                    <div className="topbarIconContainer">
                        <Language/>
                        <span className="topIconBadge">2</span>
                    </div>
                    <div className="topbarIconContainer">
                        <Settings />
                    </div>
                    <div className="topbarIconContainer">
                        <AccountCircle />
                    </div>
                </div>*/}
            </div>
        </div>
    )
}
