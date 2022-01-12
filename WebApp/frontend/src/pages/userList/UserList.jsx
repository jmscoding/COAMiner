import "./userList.css"
import { DataGrid } from '@mui/x-data-grid';
import { DeleteForever } from "@mui/icons-material";

export default function UserList(){
    const columns = [
        { field: 'id', headerName: 'ID', width: 70 },
        { field: 'userName', headerName: 'UserName', width: 130 , renderCell: (params)=> {
            return(
                <div className="userListUser">
                    <img className="userListImage" src={params.row.avatar} alt="" />
                    {params.row.userName}
                </div>
            )
        }},
        {
          field: 'password',
          headerName: 'Password',
          description: 'Here is the password of the user',
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
                        <button className="userListEdit">Edit</button>
                        <DeleteForever />
                    </>
                );
            },
        },
      ];
      
      const rows = [
        { id: 1, userName: 'Snow', password: 'Jon', avatar: "https://trendsinusa.com/wp-content/uploads/2018/01/Anonymous-hacker-profile-picture.jpg"},
      ];
      
    return(
        <div className="userList">
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