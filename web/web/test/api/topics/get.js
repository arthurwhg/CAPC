export const testTopics = async (ids) => {    
 const ids_str = ids.join(',');
const api ="api/topics/"
const url = "http://localhost:3000";
const fullURI = `${url}/${api}${ids_str}`;
console.log("start to fetch by ", fullURI);
const getMethod = {
  method: "GET", 
  headers: {"Content-Type": "application/json"},
}
const res = await fetch(fullURI, getMethod);
console.log(fullURI);
console.log(res);
const rest = await res.json()
console.log(rest);
if (res.status === 200) {
  return(rest.hints);
} else {
  // error handling
  //console.error('Something went wrong');
  return null;
}
}

testTopics([1,3,2])