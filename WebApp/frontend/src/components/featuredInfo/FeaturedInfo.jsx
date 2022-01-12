import "./featuredInfo.css"
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';

export default function FeaturedInfo() {
    return (
        <div className="featured">
            <div className="featuredItem">
                <span className="featuredTitle">Ravenue</span> 
                <div className="featuredMoneyContainer">
                    <span className="featuredMoney">$2,415</span>
                    <span className="featuredMoneyRate">-11.4 <ArrowDownwardIcon className="featuredIcon negative"/></span>
                </div> 
                <span className="featuredSub">Compared to last month</span>  
            </div>
             

        </div>
    )
}
