import {getTopicsbyIds} from "./topics.js"

const test = async () =>{
    console.log("start place API call...")
    const result = await getTopicsbyIds([1,2]);
    console.log(typeof(result))    
    console.log("final ...",result)    
}

await test()