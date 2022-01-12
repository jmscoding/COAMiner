import { DataGrid } from '@mui/x-data-grid';
import { DeleteForever } from "@mui/icons-material";
import './relevantArticle.css'

export default function relevanArticle(){
    const columns = [
        { field: 'id', headerName: 'ID', width: 70 },
        { field: 'title', headerName: 'Title', width: 130 },
        {
            field: 'text',
            headerName: 'Text',
            description: 'Here is the text of the article.',
            sortable: false,
            width: 160,
        },
        {
            field: 'author',
            headerName: 'Author',
            description: 'Author of the Article.',
            sortable: false,
            width: 160,
        },
        {
            field: 'blog',
            headerName: 'Blog',
            description: 'Name of the blog.',
            sortable: false,
            width: 160,
        },
        {
            field: 'url',
            headerName: 'URL',
            description: 'URL of the blog article.',
            sortable: false,
            width: 160,
        },
        {
            field: "action",
            headerName: "Action",
            width: 150,
            renderCell: (params)=>{
                return(
                    <>
                        <button className="articleEdit">Edit</button>
                        <DeleteForever />
                    </>
                );
            },
        },
    ];
    const rows = [
        { id: 1, title: "Massive rise in DDoS attacks post-COVID-19", text: "As people found solace within the safe boundaries of their homes after Coronavirus caused havoc worldwide, it was a time for hackers to be active.\nAccording to a report by NexusGuard, a whopping 542 percent  jump in DDoS attacks was reported in the first quarter of 2020 over the previous quarter. People were forced to work from home to stop the rise of the pandemic. As the reliance on remote services increased, hackers deemed it a perfect opportunity to up the ante and cause disruption.\nState-run agencies have also confirmed the rise in the cyber pandemic, ie DDoS attacks. The Federal Bureau of Investigation (FBI) warned in July this year of the likely surge in the DDoS attacks, especially those targetting US-based organisations through amplification techniques.\nRecent research has also found \u201cinvisible killers\u201d entering into the equation due to negligence on the part of the internet service providers. The ISPs generally turn a blind eye to small-sized and short attacks. This is why they find it easier to disrupt the online services.\nMore DDoS attacks likely\nKaspersky estimates that the high level of DDoS attacks is likely to continue in the third quarter as professionals are still working from home. In a recent report they highlighted that the fourth quarter traditionally sees an increased number of attacks because of the holidays and shopping season.\nThe worst attack to date\nThe worst DDoS attack was reported in February this year when Amazon Web Service\u2019s infrastructure was disrupted with a whopping 2.3TB per second attack (20.6 million requests a second). Another massive attack was reported recently against a large European bank which generated  809 million packets per second.\nISPs at the battlefront\nGlobal internet service providers have so far done a fine job in the prevention of these attacks. However, the rise of invisible killers and reflection attacks pegged them back during the pandemic. ISPs have also found it hard to deal with invisible killers and reflection attacks because the volume of traffic is constantly rising due to work-from-home activity. The good news is that in recent weeks, ISPs have turned their focus on these silent attacks because a failure to tackle such attacks would result in widespread DDoS strikes.\nHow to prevent the cresting cyber pandemic?\nBusinesses with staff working from home need to set up protocols to ensure the security of their systems and data. Among actions they can take to limit DDoS and similar attacks are:\nTrain your workforce: Education is the biggest protection against any criminal activity. Companies must invest in the education of their employees, especially on the work-from-home best practices and security protocols. No business can afford to lose precious data due to failing to ensure security during work-from-home activity. One way of controlling the situation would be to make employees use only corporate devices. These devices generally have excellent security protocols which defends them against most kinds of cyberattacks. Security staff need to enable and install the latest security patches and updates on these devices.\nStrengthen your email protection: Email phishing is a favourite tools for hackers and spammers so companies should strengthen their corporate email protection settings. This would help prevent spam emails from finding their way into employees\u2019 inboxes. Online training sessions with employees should be designed to educate them about different kinds of phishing emails and how to not click on suspicious or malicious links.\nKeep a close eye on traffic: Ensure 24/7 monitoring of the network traffic particularly SaaS traffic as these have been subject to large data breaches in the past. As a business, it is your responsibility to tell your employees to refrain from unauthorised transferring of any data.\nEnforce tenant access control: Data breaches and illegal or unauthorised data access are key risks for businesses in the post-COVID19-world. An effective way to ensure security is by enforcing the Tenant Access Control. You can simply buy DLP capabilities, provided by SaaS providers, which will let you enjoy an additional layer of data protection.\nTime to utilise TLS/SSL: Many companies have aTLS/SSL inspection solution but often they hardly utilise it. It is time now to get the best value out of this solution. TLS/SSL deployment will block encrypted attacks and data breaches in the real-time environment.  TLS/SSL inspection tools will go a long way in ensuring the security of your remote work environment by encrypting data. It is also a wise idea to get your employees to conduct daily work assignments on VPN networks.\nRemote SaaS users must use corporate network: Today\u2019s remote work environment is all about remote users who go about their job and work from a distance over the internet. It is crucial to ensure that your remote users only access SaaS applications via a corporate network. If your remote users access SaaS applications through their domestic internet connection, this is nothing less than a recipe for disaster. Once your remote users access SaaS applications through the corporate network, your network administrators would be able to keep a close eye on all the traffic in the cloud.\nThe final word\nThe first and the most important rule for establishing and maintaining a secure remote work environment is a \u201cZero Trust Model\u201d. Even the top hierarchy of a company should stay within the network security protocols during the pandemic. Always make sure that no employee has access to data not relevant to their work. Access restriction will help you win the battle against the cyber pandemic.\nContributed by Sama Denaa, Blogger at Blockdos writing about web security.\n5\nArticle Rating\nFacebook\nTweet\nLinkedIn", author: "Sama Denaa"},
      ];

    return(
        <div className="relevantArticle">
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={5}
                rowsPerPageOptions={[5]}
                checkboxSelection
            />
        </div>
    )
}

