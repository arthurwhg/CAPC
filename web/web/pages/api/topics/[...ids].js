import {getTopicsbyIds} from "../../../services/llmService/topics"

export default async function ask(req, res) {
    const parameter = req.query.ids[0];
    console.log("got",parameter)
    //const query = decodeURIComponent(parameter);
    const ids = parameter.split(',');
    console.log("to list ",ids);
    const answer = await getTopicsbyIds(ids);
    console.log("get topics: ",answer)
    if (typeof(answer) !== 'undefined') {
      res.status(200).json(answer);
    } else {
      res.status(500).json({"msg":"llm error!"});
    }
  }