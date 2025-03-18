export const askTopic = async (question) => {
  const api = "llm/api/v1/topicanswer/question/"
  const res = await fetch(`http://localhost:8000/${api}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "question": question,
    }),
  });

  const data = await res.json();
  const ds = data.hints;
  console.log(data)
  if (res.status === 200) {
    return (data);
  } else {
    // error handling
    //console.error('Something went wrong');
    return null;
  }
}