import Profile from "./component/profile"
import axios from "axios"
const URL = "localhost:8080/?profile="
const getThreads = async (profile) => {
  const fullUrl = URL + profile
  const response = await axios.get(fullUrl)
}

export default function Home() {
  return (
    <div className="page-container">
      <Profile></Profile>
    </div>
  )
}
