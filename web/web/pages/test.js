import Layout from "../components/layout/layout";
import { menu1,menu2 } from "../components/menu/menu";
import { useState } from "react";


const Home = () => {

    const [open, setOpen] = useState(false);
    return (
        <Layout title={"CAPC"} open={open} menu1={menu1} menu2={menu2}>
        </Layout>
    )

}

export default Home;