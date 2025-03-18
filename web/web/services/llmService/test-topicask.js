import {askTopic} from "./topicask.js"

const test = async () =>{
    const result = await askTopic("love");
    console.log(typeof(result))    
    console.log("final ...",result)    
}

test()