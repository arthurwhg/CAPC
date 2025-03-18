export const getTopicsbyIds= async (ids) => {
  const api ="http://localhost:8000/llm/api/v1/topics/byids/?ids="
  const ids_str = ids.join(',');
  const fullURI = `${api}${ids_str}`
  const getMethod = {
    method: "GET", 
    headers: {"Content-Type": "application/json"},
  }
  console.log("fetching", fullURI)
  try {
    const res = await fetch(fullURI, getMethod);
    if (res.status === 200) {
      console.log(fullURI);
      console.log("fetch results:",res);
      //const rest = await res.json().hints
      const rest_text = await res.text();
      console.log("return from llm:",JSON.parse(rest_text));
      return(JSON.parse(rest_text));
    } else {
      // error handling
      console.error('Something went wrong', res);
      return null;
    }  
  } catch (error) {
    console.error('Error:', error);
    return null;
  } 
}

