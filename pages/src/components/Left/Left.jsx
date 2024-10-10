import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import './Left.css'
import Card from '../ui/Card';
import Rondo from '../ui/Rondo';

const Left = () => {
  return (
    <div id="Left">
        {/* <Tabs defaultValue="account" className="w-[400px]">
        <TabsList>
            <TabsTrigger value="account">Account</TabsTrigger>
            <TabsTrigger value="password">Password</TabsTrigger>
        </TabsList>
        <TabsContent value="account">Make changes to your account here.</TabsContent>
        <TabsContent value="password">Change your password here.</TabsContent>
        </Tabs> */}
    
        {/* <Card /> */}
        <Rondo />
    </div>
  )
}

export default Left